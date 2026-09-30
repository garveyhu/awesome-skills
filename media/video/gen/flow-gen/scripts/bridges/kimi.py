"""kimi-webbridge 通道：通过本机 daemon + Chrome 扩展控制用户真实的 Chrome（带登录态）。

daemon 地址：环境变量 WEBBRIDGE_URL > `kimi-webbridge status` 报告的端口 > 127.0.0.1:10086。
只会自动 `start` daemon；stop / restart / upgrade 属于用户操作，这里绝不调用。
"""

from __future__ import annotations

import json
import os
import subprocess
import urllib.error
import urllib.request
from typing import Any

from .base import BridgeError, BrowserBridge, CapturedDetail, CapturedRequest

DAEMON_BIN = os.path.expanduser("~/.kimi-webbridge/bin/kimi-webbridge")
DEFAULT_URL = "http://127.0.0.1:10086"


def _cli(*args: str) -> str:
    if not os.path.exists(DAEMON_BIN):
        raise BridgeError("kimi-webbridge 未安装：先装 kimi-webbridge skill 和 Chrome 扩展")
    proc = subprocess.run([DAEMON_BIN, *args], capture_output=True, text=True, timeout=30)
    return proc.stdout


def _discover_url() -> str:
    if os.environ.get("WEBBRIDGE_URL"):
        return os.environ["WEBBRIDGE_URL"]
    try:
        status = json.loads(_cli("status"))
        if status.get("port"):
            return f"http://127.0.0.1:{status['port']}"
    except (BridgeError, json.JSONDecodeError, subprocess.SubprocessError):
        pass
    return DEFAULT_URL


class KimiBridge(BrowserBridge):
    name = "kimi"

    def __init__(self, session: str, timeout: float = 120):
        self.session = session
        self.timeout = timeout
        self.url = _discover_url()

    # ---------- 底层 ----------
    def _status(self) -> dict:
        with urllib.request.urlopen(f"{self.url}/status", timeout=5) as resp:
            return json.loads(resp.read().decode())

    def _command(self, action: str, **args: Any) -> dict:
        body = json.dumps({"action": action, "args": args, "session": self.session}).encode()
        req = urllib.request.Request(
            f"{self.url}/command", data=body, headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                out = json.loads(resp.read().decode())
        except urllib.error.URLError as e:
            raise BridgeError(f"连不上 kimi-webbridge daemon（{self.url}）: {e}") from e
        if not out.get("ok"):
            err = out.get("error") or {}
            raise BridgeError(f"{action} 失败: {err.get('message') or err}")
        return out.get("data") or {}

    # ---------- 接口实现 ----------
    def ensure_ready(self) -> None:
        try:
            status = self._status()
        except (urllib.error.URLError, ConnectionError):
            _cli("start")
            self.url = _discover_url()
            try:
                status = self._status()
            except (urllib.error.URLError, ConnectionError) as e:
                raise BridgeError(f"kimi-webbridge daemon 启动失败: {e}") from e
        if not status.get("extension_connected"):
            raise BridgeError("Kimi 浏览器扩展没连上：确认 Chrome 开着且扩展已启用")

    def open_tab(self, url: str, group_title: str) -> None:
        try:
            self._command("find_tab", url=url)  # 按 host 匹配本 session 开过的标签页
            return
        except BridgeError:
            pass
        self._command("navigate", url=url, newTab=True, group_title=group_title)

    def navigate(self, url: str) -> None:
        self._command("navigate", url=url)

    def evaluate(self, code: str) -> Any:
        return self._command("evaluate", code=code).get("value")

    def fill(self, selector: str, value: str) -> None:
        self._command("fill", selector=selector, value=value)

    def capture_start(self, url_filter: str) -> None:
        self._command("network", cmd="stop")
        self._command("network", cmd="start", filter=url_filter)

    def capture_list(self, url_filter: str) -> list[CapturedRequest]:
        data = self._command("network", cmd="list", filter=url_filter)
        return [
            CapturedRequest(request_id=r["requestId"], url=r.get("url", ""), completed=bool(r.get("completed")))
            for r in data.get("requests", [])
        ]

    def capture_detail(self, request_id: str) -> CapturedDetail:
        data = self._command("network", cmd="detail", requestId=request_id)
        if data.get("bodyError"):
            raise BridgeError(f"取不到响应体: {data['bodyError']}")
        return CapturedDetail(request_body=data.get("requestBody") or "", response_body=data.get("body") or "")

    def capture_stop(self) -> None:
        self._command("network", cmd="stop")
