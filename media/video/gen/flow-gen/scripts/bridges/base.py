"""浏览器通道接口：flow-gen 需要「在用户真实 Chrome 的某个标签页里」做的全部事情。

换通道（kimi-webbridge → 别的扩展 / CDP …）只需新写一个实现类并在 bridges/__init__.py 注册，
flow_session / flow_gen 不用动。
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


class BridgeError(RuntimeError):
    """通道不可用或某条命令执行失败。"""


@dataclass(frozen=True)
class CapturedRequest:
    request_id: str
    url: str
    completed: bool


@dataclass(frozen=True)
class CapturedDetail:
    request_body: str
    response_body: str


class BrowserBridge(ABC):
    """一个通道实例绑定一个「当前标签页」；所有页面操作都作用在它上面。"""

    name: str = "abstract"

    @abstractmethod
    def ensure_ready(self) -> None:
        """确认通道可用（必要时拉起本地服务），否则抛 BridgeError。"""

    @abstractmethod
    def open_tab(self, url: str, group_title: str) -> None:
        """复用本通道之前开的标签页，没有就新开一个并设为当前标签页。"""

    @abstractmethod
    def navigate(self, url: str) -> None:
        """当前标签页跳转到 url。"""

    @abstractmethod
    def evaluate(self, code: str) -> Any:
        """在当前页面执行 JS 表达式（可返回 Promise），返回其结果值。"""

    @abstractmethod
    def fill(self, selector: str, value: str) -> None:
        """往输入框 / contenteditable 填文本（触发页面的输入事件）。"""

    @abstractmethod
    def capture_start(self, url_filter: str) -> None:
        """开始记录当前标签页的网络请求（清掉之前的记录）。"""

    @abstractmethod
    def capture_list(self, url_filter: str) -> list[CapturedRequest]:
        """列出已记录、URL 含 url_filter 的请求。"""

    @abstractmethod
    def capture_detail(self, request_id: str) -> CapturedDetail:
        """取某条请求的请求体与响应体；必须在 capture_stop 之前调用。"""

    @abstractmethod
    def capture_stop(self) -> None:
        """停止记录。"""
