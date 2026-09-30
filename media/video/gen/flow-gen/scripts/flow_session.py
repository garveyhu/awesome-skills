"""Flow 会话：在用户真实 Chrome 里准备一个 Flow 项目标签页，注入 flow_page.js，暴露 RPC 调用。

职责：标签页生命周期 + 页面就绪等待 + 调 window.__flowgen。不做模型挑选、不做下载。
浏览器操作全部经 bridges.BrowserBridge 接口，不关心底下是哪个通道。
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any
from urllib.parse import unquote_plus

from bridges import BridgeError, BrowserBridge, get_bridge

FLOW_HOME = "https://flow.google.com/"
SESSION = "flow-gen"
GROUP_TITLE = "Flow 视频生成"
STATE_FILE = Path(os.environ.get("FLOW_GEN_STATE", "~/.config/flow-gen/state.json")).expanduser()
PAGE_JS = (Path(__file__).parent / "flow_page.js").read_text(encoding="utf-8")
SUBMIT_RPC = "YhhmEf"  # 文生视频提交的 RPC id（抓包实测）


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
            self._wait_ready(need_recaptcha=False)
            projects = self.call("projects")
            if not projects:
                raise FlowError("这个账号在 Flow 里还没有项目：先在 flow.google.com 手动建一个")
            self.project_id = projects[0]["id"]
            self.bridge.navigate(project_url(self.project_id))
        else:
            self.bridge.open_tab(project_url(self.project_id), GROUP_TITLE)
            if project_url(self.project_id) not in (self.bridge.evaluate("location.href") or ""):
                self.bridge.navigate(project_url(self.project_id))  # 复用的标签页可能停在别的 Flow 页面
        self._wait_ready(need_recaptcha=True)
        self.state["project_id"] = self.project_id
        _save_state(self.state)
        return self

    # ---------- 提交（走页面自己的「生成」按钮） ----------
    def submit_t2v(self, prompt: str, family_name: str, model_key: str, expected_cost: int,
                   aspect: str, duration: int | None, resolution: str, count: int) -> dict:
        shown = self.call("configureVideo", {
            "familyName": family_name, "aspect": aspect, "duration": duration,
            "resolution": resolution, "count": count,
        })
        if shown.get("cost") != expected_cost * count:
            raise FlowError(f"页面显示 {shown.get('cost')} 点，和预期 {expected_cost * count} 点对不上，"
                            f"没有提交（页面设置：{shown.get('summary')}）")
        self.bridge.fill(".ProseMirror", prompt)
        self.bridge.capture_start(SUBMIT_RPC)
        try:
            self.call("clickSubmit")
            return self._captured_submit(model_key)
        finally:
            self.bridge.capture_stop()

    def _captured_submit(self, model_key: str, timeout: float = 60) -> dict:
        deadline = time.time() + timeout
        while time.time() < deadline:
            done = [r for r in self.bridge.capture_list(SUBMIT_RPC) if r.completed]
            if done:
                detail = self.bridge.capture_detail(done[-1].request_id)
                sent = unquote_plus(detail.request_body)
                if model_key not in sent:
                    raise FlowError(f"页面提交的模型不是 {model_key}，请到 Flow 里核对")
                data = _parse_batch(detail.response_body, SUBMIT_RPC)
                return {
                    "creditsLeft": data[1],
                    "mediaIds": [item[0] for item in data[3] or []],
                }
            time.sleep(1)
        raise FlowError("点了「生成」但没抓到提交请求：去 Flow 页面看看是不是弹了提示")

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
