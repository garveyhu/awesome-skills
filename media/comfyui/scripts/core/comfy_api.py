"""ComfyUI HTTP API 客户端。

单一职责：只负责与一个运行中的 ComfyUI 实例通信（提交工作流、轮询进度、
上传/下载文件、查询节点信息），不含任何"某架构该怎么搭工作流"的知识。
仅依赖标准库，Mac 上无需 pip 装任何东西。
"""

from __future__ import annotations

import json
import os
import shutil
import time
import uuid
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_HOST = os.environ.get("COMFYUI_HOST", "http://127.0.0.1:8188")


class ComfyError(RuntimeError):
    """ComfyUI 交互过程中的错误（连接失败、执行报错、超时等）。"""


class ComfyClient:
    """一个轻量 ComfyUI REST 客户端。"""

    def __init__(self, host: str = DEFAULT_HOST, timeout: int = 30) -> None:
        self.host = host.rstrip("/")
        self.timeout = timeout
        # client_id 让同一会话的提交可被服务端关联（也便于将来接 websocket 进度）
        self.client_id = str(uuid.uuid4())

    # ---- 底层 HTTP ----------------------------------------------------------

    def _get(self, path: str, timeout: int | None = None) -> dict:
        url = f"{self.host}{path}"
        try:
            with urllib.request.urlopen(url, timeout=timeout or self.timeout) as r:
                return json.load(r)
        except urllib.error.URLError as e:
            raise ComfyError(f"GET {url} 失败: {e}") from e

    def _post(self, path: str, payload: dict) -> dict:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.host}{path}",
            data=data,
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                raw = r.read()
                # 部分端点（/free /interrupt）返回空 body，不是 JSON
                return json.loads(raw) if raw.strip() else {}
        except urllib.error.HTTPError as e:
            # ComfyUI 校验工作流失败时会返回 400 + JSON 错误体，原样抛出方便定位
            body = e.read().decode("utf-8", "replace")
            raise ComfyError(f"POST {path} 被拒绝 ({e.code}):\n{body}") from e
        except urllib.error.URLError as e:
            raise ComfyError(f"POST {path} 失败: {e}") from e

    # ---- 健康检查 / 元信息 --------------------------------------------------

    def ping(self) -> dict:
        """返回 /system_stats；连不上会抛 ComfyError。"""
        return self._get("/system_stats", timeout=5)

    def object_info(self, node: str | None = None) -> dict:
        """获取节点定义。node=None 时返回全部（很大，慎用）。"""
        return self._get(f"/object_info/{node}" if node else "/object_info")

    # ---- 提交 / 轮询 --------------------------------------------------------

    def queue_prompt(self, workflow: dict) -> str:
        """提交一个 API 格式工作流，返回 prompt_id。"""
        resp = self._post("/prompt", {"prompt": workflow, "client_id": self.client_id})
        # 即使 200 也可能带 node_errors（部分节点校验失败），及早暴露
        node_errors = resp.get("node_errors") or {}
        if node_errors:
            raise ComfyError(f"工作流校验失败 node_errors: {json.dumps(node_errors, ensure_ascii=False)}")
        pid = resp.get("prompt_id")
        if not pid:
            raise ComfyError(f"提交未返回 prompt_id: {resp}")
        return pid

    def history(self, prompt_id: str) -> dict:
        return self._get(f"/history/{prompt_id}")

    def queue(self) -> dict:
        """当前队列：{queue_running:[...], queue_pending:[...]}，用于看积压。"""
        return self._get("/queue")

    def list_models(self, model_type: str) -> list[str]:
        """列出某类已安装模型（checkpoints/loras/vae/diffusion_models/clip/...）。"""
        try:
            return self._get(f"/models/{model_type}")
        except ComfyError:
            return []

    def interrupt(self) -> None:
        """中断当前正在执行的任务。"""
        self._post("/interrupt", {})

    def free(self, unload_models: bool = True, free_memory: bool = True) -> None:
        """释放显存/统一内存（大任务之间调用，缓解 Mac 上的内存碎片/OOM）。"""
        self._post("/free", {"unload_models": unload_models, "free_memory": free_memory})

    def wait(
        self,
        prompt_id: str,
        poll: float = 2.0,
        timeout: int = 1800,
        on_tick=None,
    ) -> dict:
        """阻塞轮询直到该 prompt 完成，返回它的 history entry。

        on_tick(elapsed_seconds) 可选回调，用于打印进度。
        """
        start = time.time()
        while True:
            hist = self.history(prompt_id)
            entry = hist.get(prompt_id)
            if entry:
                status = entry.get("status", {})
                if status.get("status_str") == "error":
                    raise ComfyError(f"工作流执行出错: {json.dumps(status, ensure_ascii=False)}")
                # 完成判定：有 outputs 或 status 标记 completed/success
                if entry.get("outputs") or status.get("completed") or status.get("status_str") == "success":
                    return entry
            elapsed = time.time() - start
            if elapsed > timeout:
                raise ComfyError(f"等待超时 {timeout}s（prompt {prompt_id} 仍未完成）")
            if on_tick:
                on_tick(elapsed)
            time.sleep(poll)

    # ---- 产物下载 -----------------------------------------------------------

    def download(self, filename: str, subfolder: str, ftype: str, out_dir: str) -> str:
        q = urllib.parse.urlencode({"filename": filename, "subfolder": subfolder, "type": ftype})
        url = f"{self.host}/view?{q}"
        os.makedirs(out_dir, exist_ok=True)
        dest = os.path.join(out_dir, os.path.basename(filename))
        # 反向软链场景:ComfyUI 原生 SaveImage 已经把文件写到 dest 了。已有非空文件
        # 就直接复用,绝不让一次半截的 /view 下载把它覆盖成 0 字节。
        if os.path.isfile(dest) and os.path.getsize(dest) > 0:
            return dest
        # 否则下到临时文件、完整才原子替换;失败重试,半截内容不落地。
        tmp = dest + ".part"
        last: Exception | None = None
        for _ in range(3):
            try:
                with urllib.request.urlopen(url, timeout=self.timeout) as r, open(tmp, "wb") as f:
                    shutil.copyfileobj(r, f)
                os.replace(tmp, dest)
                return dest
            except Exception as e:  # IncompleteRead / 连接中断等
                last = e
        if os.path.exists(tmp):
            os.remove(tmp)
        raise ComfyError(f"下载产物失败 {filename}: {last}")

    def collect_outputs(self, entry: dict, out_dir: str) -> list[str]:
        """把一次执行产生的所有文件（图片/视频/gif/音频）下载到 out_dir。

        不假设输出键名，遍历每个输出节点里所有"看起来像文件清单"的字段，
        因此对 SaveImage / SaveVideo / VHS 等不同保存节点都通用。
        """
        saved: list[str] = []
        for _node_id, out in entry.get("outputs", {}).items():
            for _key, items in out.items():
                if not isinstance(items, list):
                    continue
                for item in items:
                    if isinstance(item, dict) and item.get("filename"):
                        saved.append(
                            self.download(
                                item["filename"],
                                item.get("subfolder", ""),
                                item.get("type", "output"),
                                out_dir,
                            )
                        )
        return saved

    # ---- 上传输入图（i2v / inpaint 等需要） ---------------------------------

    def upload_image(self, path: str, overwrite: bool = True) -> str:
        """上传一张图片到 ComfyUI 的 input 目录，返回服务端文件名。"""
        if not os.path.isfile(path):
            raise ComfyError(f"找不到要上传的图片: {path}")
        boundary = f"----comfyskill{uuid.uuid4().hex}"
        filename = os.path.basename(path)
        with open(path, "rb") as f:
            file_bytes = f.read()

        parts: list[bytes] = []
        def field(name: str, value: str) -> None:
            parts.append(f"--{boundary}\r\n".encode())
            parts.append(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode())
            parts.append(f"{value}\r\n".encode())

        field("overwrite", "true" if overwrite else "false")
        parts.append(f"--{boundary}\r\n".encode())
        parts.append(
            f'Content-Disposition: form-data; name="image"; filename="{filename}"\r\n'.encode()
        )
        parts.append(b"Content-Type: application/octet-stream\r\n\r\n")
        parts.append(file_bytes)
        parts.append(f"\r\n--{boundary}--\r\n".encode())
        body = b"".join(parts)

        req = urllib.request.Request(
            f"{self.host}/upload/image",
            data=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                resp = json.load(r)
        except urllib.error.URLError as e:
            raise ComfyError(f"上传图片失败: {e}") from e
        name = resp.get("name", filename)
        sub = resp.get("subfolder", "")
        return f"{sub}/{name}" if sub else name
