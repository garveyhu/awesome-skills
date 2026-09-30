"""Flow 会话：在用户真实 Chrome 里准备一个 Flow 项目标签页，注入 flow_page.js，暴露 RPC 调用。

职责：标签页生命周期 + 页面就绪等待 + 调 window.__flowgen。不做模型挑选、不做下载。
浏览器操作全部经 bridges.BrowserBridge 接口，不关心底下是哪个通道。
"""

from __future__ import annotations

import json
import os
import shutil
import tempfile
import time
import uuid
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote_plus, urlparse

from bridges import BridgeError, BrowserBridge, get_bridge

FLOW_HOME = "https://flow.google.com/"
SESSION = "flow-gen"
GROUP_TITLE = "Flow 视频生成"
STATE_FILE = Path(os.environ.get("FLOW_GEN_STATE", "~/.config/flow-gen/state.json")).expanduser()
PAGE_JS = (Path(__file__).parent / "flow_page.js").read_text(encoding="utf-8")
BATCH_FILTER = "batchexecute"
# 提交用的 RPC id 因模式而异（实测 YhhmEf=文生 eb1hJf=首帧 ogiZ0b=出图），不写死：
# 抓到的请求里「请求体含预期 modelKey + 响应结构对得上」的就是提交
FRAME_SLOTS = ("首帧", "尾帧")


class FlowError(RuntimeError):
    pass


def _load_state() -> dict:
    try:
        return json.loads(STATE_FILE.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))


def _parse_batch(text: str, rpcid: str) -> Any:
    """从 batchexecute 响应文本里取出指定 RPC 的结果；被拒时抛出带错误码的 FlowError。"""
    for line in text.splitlines():
        if not line.startswith("[["):
            continue
        try:
            rows = json.loads(line)
        except json.JSONDecodeError:
            continue
        for row in rows:
            if row[0] == "wrb.fr" and row[1] == rpcid:
                if row[2] is None:
                    raise FlowError(f"{rpcid} 被服务端拒绝: {json.dumps(row, ensure_ascii=False)[:500]}")
                return json.loads(row[2])
    raise FlowError(f"{rpcid} 响应里没有结果: {text[:300]}")


def _extract_video(data: Any) -> dict | None:
    # 视频提交响应：[_, 剩余点数, _, [[mediaId, ...], ...]]
    if isinstance(data, list) and len(data) > 3 and data[3]:
        return {"creditsLeft": data[1], "mediaIds": [item[0] for item in data[3]]}
    return None


def _find_string(node: Any, prefix: str) -> str | None:
    if isinstance(node, str):
        return node if node.startswith(prefix) else None
    if isinstance(node, list):
        for child in node:
            hit = _find_string(child, prefix)
            if hit:
                return hit
    return None


def _extract_image(data: Any) -> dict | None:
    # 出图响应：[[[mediaId, _, workflowId, ..., [[..., 签名图片地址, ...]], ...], ...], ...]
    # 条目长度会变（有时带 [宽, 高]、有时不带），所以地址按前缀搜，不按固定下标取
    if not (isinstance(data, list) and data and isinstance(data[0], list)):
        return None
    images = []
    for item in data[0]:
        if not (isinstance(item, list) and item and isinstance(item[0], str)):
            continue
        url = _find_string(item, "https://flow-content.google/image/")
        if url:
            images.append({"mediaId": item[0], "url": url})
    return {"images": images} if images else None


def project_url(project_id: str) -> str:
    return f"{FLOW_HOME}project/{project_id}"


class FlowSession:
    def __init__(self, project_id: str | None = None, bridge: BrowserBridge | None = None):
        self.bridge = bridge or get_bridge(SESSION)
        self.state = _load_state()
        self.project_id = project_id or self.state.get("project_id")

    # ---------- 标签页 ----------
    def _wait_ready(self, need_recaptcha: bool, timeout: float = 40) -> None:
        deadline = time.time() + timeout
        last = None
        while time.time() < deadline:
            try:
                self.bridge.evaluate(PAGE_JS)
                info = json.loads(self.bridge.evaluate("window.__flowgen.ready()"))
                if not need_recaptcha or info.get("recaptcha"):
                    return
                last = "reCAPTCHA 还没加载"
            except (BridgeError, TypeError, json.JSONDecodeError) as e:
                last = str(e)
            time.sleep(1.5)
        raise FlowError(f"Flow 页面没准备好（{last}）：确认 Chrome 里已登录 Flow")

    def open(self) -> "FlowSession":
        self.bridge.ensure_ready()
        if not self.project_id:
            self.bridge.open_tab(FLOW_HOME, GROUP_TITLE)
            self.bridge.set_foreground(True)
            self._wait_ready(need_recaptcha=False)
            projects = self.call("projects")
            if not projects:
                raise FlowError("这个账号在 Flow 里还没有项目：先在 flow.google.com 手动建一个")
            self.project_id = projects[0]["id"]
            self.bridge.navigate(project_url(self.project_id))
        else:
            self.bridge.open_tab(project_url(self.project_id), GROUP_TITLE)
            # 总是重新载入项目页：复用的标签页可能停在编辑页 / 残留弹窗 / 没清的帧（这些都不改 URL）
            self.bridge.navigate(project_url(self.project_id))
        self.bridge.set_foreground(True)  # 后台标签页的定时器会被节流，页面里的等待会拖成几分钟
        self._wait_ready(need_recaptcha=True)
        self.state["project_id"] = self.project_id
        _save_state(self.state)
        return self

    def close(self) -> None:
        """还原标签页的后台状态；失败不影响结果。"""
        try:
            self.bridge.set_foreground(False)
        except BridgeError:
            pass

    # ---------- 提交（走页面自己的「生成」按钮） ----------
    def submit_video(self, prompt: str, family_name: str, model_key: str, expected_cost: int,
                     aspect: str, duration: int | None, resolution: str, count: int,
                     frames: list[str | None], refs: list[str], agree_rights: bool) -> dict:
        """视频：frames=[首帧, 尾帧]（「帧」模式，全 None 即文生）；refs=参考图（「素材」模式）。

        返回 {rpcid, creditsLeft, mediaIds}；视频是异步的，之后轮询 mediaIds。
        """
        settings = {
            "media": "video", "composition": "ingredients" if refs else "frames",
            "familyName": family_name, "aspect": aspect, "duration": duration,
            "resolution": resolution, "count": count,
        }
        uploads = [("frame", slot, path) for slot, path in enumerate(frames) if path]
        uploads += [("ingredient", 0, path) for path in refs]
        return self._submit(prompt, settings, uploads, model_key, expected_cost * count,
                            agree_rights, _extract_video, timeout=90)

    def submit_image(self, prompt: str, family_name: str, model_key: str, expected_cost: int,
                     aspect: str, count: int, refs: list[str], agree_rights: bool) -> dict:
        """图片：同步出图，返回 {rpcid, images:[{mediaId, url, width, height}]}。"""
        settings = {"media": "image", "familyName": family_name, "aspect": aspect, "count": count}
        uploads = [("ingredient", 0, path) for path in refs]
        return self._submit(prompt, settings, uploads, model_key, expected_cost * count,
                            agree_rights, _extract_image, timeout=300)

    def _submit(self, prompt: str, settings: dict, uploads: list[tuple[str, int, str]], model_key: str,
                expected_total: int, agree_rights: bool, extract, timeout: float) -> dict:
        """设参数 → 核对点数 → 上传图片 → 填提示词 → 真实点击生成 → 从抓包里取结果。"""
        shown = self.call("configure", settings)
        if shown.get("cost") != expected_total:
            raise FlowError(f"页面显示 {shown.get('cost')} 点，和预期 {expected_total} 点对不上，"
                            f"没有提交（页面设置：{shown.get('summary')}）")
        image_ids = [self._upload(target, slot, path, agree_rights) for target, slot, path in uploads]
        self.bridge.fill(".ProseMirror", prompt)
        point = self.call("submitPoint")
        self.bridge.capture_start(BATCH_FILTER)
        try:
            self.bridge.click_at(point["x"], point["y"])  # 出图只认真实点击
            return self._captured_submit(model_key, image_ids, extract, timeout)
        finally:
            self.bridge.capture_stop()

    def _upload(self, target: str, slot: int, path: str, agree_rights: bool) -> str:
        """上传一张图并放进输入框（首/尾帧格子或素材），返回 Flow 给这张图的 mediaId。

        先复制成唯一文件名再传：选择框里同名旧图会导致点错。
        """
        label = FRAME_SLOTS[slot] if target == "frame" else "素材图"
        src = Path(path).expanduser().resolve()
        tmpdir = Path(tempfile.mkdtemp(prefix="flowgen-"))
        unique = tmpdir / f"flowgen-{uuid.uuid4().hex[:8]}{src.suffix.lower()}"
        shutil.copyfile(src, unique)
        try:
            selector = self.call("openUpload", {"target": target, "slot": slot})["selector"]
            self.bridge.upload(selector, [str(unique)])
            return self.call("finishUpload", {
                "target": target, "slot": slot, "agreeRights": agree_rights, "fileName": unique.name,
            })["mediaId"]
        except FlowError as e:
            self.call("closeOverlays")
            if "RIGHTS_CONFIRM_REQUIRED" in str(e):
                raise FlowError("Flow 要求确认「你对上传图片拥有必要权利」：确认后加 --agree-rights "
                                "（或设 FLOW_GEN_AGREE_RIGHTS=1）再跑") from e
            raise FlowError(f"{label}（{src.name}）上传失败：{e}") from e
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def _captured_submit(self, model_key: str, image_ids: list[str], extract, timeout: float) -> dict:
        deadline = time.time() + timeout
        seen: set[str] = set()
        while time.time() < deadline:
            for req in self.bridge.capture_list(BATCH_FILTER):
                if not req.completed or req.request_id in seen:
                    continue
                seen.add(req.request_id)
                rpcid = parse_qs(urlparse(req.url).query).get("rpcids", [""])[0]
                detail = self.bridge.capture_detail(req.request_id)
                sent = unquote_plus(detail.request_body)
                if model_key not in sent:
                    continue
                missing = [mid for mid in image_ids if mid not in sent]
                if missing:
                    raise FlowError(f"已提交，但请求里的图不是刚上传的（缺 {missing}），请到 Flow 核对这条")
                result = extract(_parse_batch(detail.response_body, rpcid))
                if result is not None:
                    return {"rpcid": rpcid, **result}
            time.sleep(1)
        raise FlowError("点了「生成」但没抓到提交结果：去 Flow 页面看看是不是弹了提示")

    # ---------- RPC ----------
    def call(self, method: str, arg: object = None) -> Any:
        self.bridge.evaluate(PAGE_JS)  # 页面刷新过也能自愈
        arg_js = "" if arg is None else json.dumps(arg, ensure_ascii=False)
        code = (
            f"window.__flowgen.{method}({arg_js})"
            ".catch(e => JSON.stringify({__error: String(e && e.message || e)}))"
        )
        raw = self.bridge.evaluate(code)
        if raw is None:
            raise FlowError(f"{method} 没有返回值")
        out = json.loads(raw)
        if isinstance(out, dict) and "__error" in out:
            raise FlowError(out["__error"])
        return out
