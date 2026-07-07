"""CDP 连接层 —— attach 到「你真实在用、已登录」的 Chrome（不开无头、不存 cookie）。

前提：Chrome 以 `--remote-debugging-port` 启动（见 core/chrome_debug.sh）。
`connect_over_cdp` 连上后，`browser.contexts[0]` 就是你真实浏览器的默认 context——
所有平台登录态、代理、指纹原样复用，这正是「封控风险最低」的来源。

自检：  python3 core/attach.py --selfcheck
"""
from __future__ import annotations

import argparse
import sys

try:
    from . import config
except ImportError:  # 脚本直跑（core 在 sys.path）
    import config


def connect(port: int | None = None):
    """连到真实 Chrome，返回 (playwright, browser)。调用方负责 browser.close()/pw.stop()。

    只 attach、不新开浏览器：close() 只断开 CDP 连接，不会关掉你的 Chrome。
    """
    from playwright.sync_api import sync_playwright

    port = port or config.debug_port()
    pw = sync_playwright().start()
    try:
        browser = pw.chromium.connect_over_cdp(f"http://localhost:{port}", timeout=8000)
    except Exception as e:  # noqa: BLE001
        pw.stop()
        raise RuntimeError(
            f"连不上 Chrome 调试端口 {port}：{e}\n"
            f"→ 先 `bash core/chrome_debug.sh` 用调试端口起 Chrome，"
            f"再 `curl -s http://localhost:{port}/json/version` 自检。"
        ) from e
    return pw, browser


def default_context(browser):
    """真实浏览器的默认 context（含全部登录态）。attach 场景取已存在的第一个。"""
    return browser.contexts[0] if browser.contexts else browser.new_context()


def open_page(context, url: str = "", reuse_host: bool = True):
    """开/复用一个标签页。url 为空则取一个空白页复用。

    reuse_host=True 时优先复用同域已开标签，避免开一堆重复页。
    """
    if url and reuse_host:
        host = url.split("/")[2] if "//" in url else url
        for pg in context.pages:
            try:
                if host and host in (pg.url or ""):
                    pg.bring_to_front()
                    return pg
            except Exception:  # noqa: BLE001
                continue
    if not url:
        # 复用一个 about:blank，没有就开一个
        for pg in context.pages:
            try:
                if (pg.url or "about:blank") in ("about:blank", ""):
                    return pg
            except Exception:  # noqa: BLE001
                continue
        return context.new_page()
    page = context.new_page()
    page.goto(url, wait_until="domcontentloaded")
    return page


def selfcheck(port: int | None = None) -> int:
    port = port or config.debug_port()
    try:
        pw, browser = connect(port)
    except RuntimeError as e:
        sys.stderr.write(f"❌ {e}\n")
        return 1
    try:
        ctx = default_context(browser)
        pages = ctx.pages
        print(f"✅ 已连上真实 Chrome（端口 {port}），当前 {len(pages)} 个标签页：")
        for pg in pages:
            try:
                print(f"   · {pg.url}")
            except Exception:  # noqa: BLE001
                pass
        return 0
    finally:
        browser.close()  # 只断开 CDP，不关你的 Chrome
        pw.stop()


def main() -> int:
    ap = argparse.ArgumentParser(description="CDP 连接层自检")
    ap.add_argument("--selfcheck", action="store_true")
    ap.add_argument("--port", type=int, default=None)
    args = ap.parse_args()
    if args.selfcheck:
        return selfcheck(args.port)
    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
