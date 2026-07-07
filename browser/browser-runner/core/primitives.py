"""浏览器操作原语 —— 流程里复用的通用操作手法。

写操作（上传/填字/点击）+ 读操作（抽文本/属性/链接/截图）。
选择器易变的留给各 flow；这里只放跨站稳定的通用能力。
"""
from __future__ import annotations

from typing import Any


def upload_file(page: Any, selector: str, path: str) -> None:
    """给 file input 喂本地路径 —— 走 **CDP 原生 DOM.setFileInputFiles**，无大小限制。

    为什么不用 Playwright 的 set_input_files：connect_over_cdp 时它会把文件内容传给浏览器，
    有 50MB 上限。CDP 原生 setFileInputFiles 是把**本地路径**直接给浏览器让它自己读磁盘
    （同机可见），无传输、无上限。file input 隐藏也能设，不去点会弹原生文件框的「上传」按钮。
    """
    client = page.context.new_cdp_session(page)
    client.send("DOM.enable")
    client.send("Runtime.enable")
    res = client.send(
        "Runtime.evaluate",
        {"expression": f"document.querySelector({selector!r})", "returnByValue": False},
    )
    object_id = res.get("result", {}).get("objectId")
    if not object_id:
        raise RuntimeError(f"file input 未找到: {selector}")
    client.send("DOM.setFileInputFiles", {"files": [path], "objectId": object_id})


def safe_fill(page: Any, selector: str, value: str, timeout: int = 15000, clear: bool = True) -> None:
    """等元素可见后填值（contenteditable 富文本框也兼容——先聚焦再逐字输入）。"""
    if not value:
        return
    loc = page.locator(selector).first
    loc.wait_for(state="visible", timeout=timeout)
    try:
        if clear:
            loc.fill("")
        loc.fill(value)
    except Exception:  # noqa: BLE001 — 富文本不支持 fill，退回逐字输入
        loc.click()
        page.keyboard.press("Meta+A")
        page.keyboard.press("Delete")
        loc.type(value, delay=15)


def click_text(page: Any, text: str, exact: bool = False, timeout: int = 3000) -> bool:
    """按可见文本点击。点到返 True，点不到返 False（不抛，方便 flow 里做降级）。"""
    try:
        page.get_by_text(text, exact=exact).first.click(timeout=timeout)
        return True
    except Exception:  # noqa: BLE001
        return False


def wait_idle(page: Any, ms: int = 1500) -> None:
    """给页面一点反应时间（异步渲染/进度条），非严格等待。"""
    try:
        page.wait_for_timeout(ms)
    except Exception:  # noqa: BLE001
        pass


def extract_all(page: Any, selector: str, attr: str | None = None, limit: int = 50) -> list[str]:
    """抓所有匹配元素：attr=None 取可见文本，否则取该属性（如 href/src）。去空、按 limit 截断。"""
    js = """([sel, attr, limit]) => {
        const out = [];
        for (const el of document.querySelectorAll(sel)) {
            let v = attr ? el.getAttribute(attr) : (el.innerText || el.textContent || '');
            v = (v || '').trim();
            if (v) out.push(v);
            if (out.length >= limit) break;
        }
        return out;
    }"""
    return page.evaluate(js, [selector, attr, limit])


def extract_text(page: Any, selector: str, timeout: int = 8000) -> str | None:
    """取第一个匹配元素的可见文本；无则 None。"""
    try:
        loc = page.locator(selector).first
        loc.wait_for(state="visible", timeout=timeout)
        return (loc.inner_text() or "").strip() or None
    except Exception:  # noqa: BLE001
        return None


def screenshot(page: Any, path: str, full_page: bool = True) -> None:
    """整页截图存到 path。"""
    page.screenshot(path=path, full_page=full_page)
