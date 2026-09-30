"""浏览器通道注册表。选择顺序：参数 > 环境变量 FLOW_GEN_BRIDGE > 默认 kimi。

新增通道：写一个 BrowserBridge 子类，在 _REGISTRY 里加一行。
"""

from __future__ import annotations

import os
from typing import Callable

from .base import BridgeError, BrowserBridge, CapturedDetail, CapturedRequest
from .kimi import KimiBridge

DEFAULT_BRIDGE = "kimi"

_REGISTRY: dict[str, Callable[[str], BrowserBridge]] = {
    "kimi": KimiBridge,
}


def available() -> list[str]:
    return sorted(_REGISTRY)


def get_bridge(session: str, name: str | None = None) -> BrowserBridge:
    key = name or os.environ.get("FLOW_GEN_BRIDGE") or DEFAULT_BRIDGE
    if key not in _REGISTRY:
        raise BridgeError(f"未知浏览器通道「{key}」，可选：{', '.join(available())}")
    return _REGISTRY[key](session)


__all__ = [
    "BridgeError", "BrowserBridge", "CapturedDetail", "CapturedRequest",
    "available", "get_bridge",
]
