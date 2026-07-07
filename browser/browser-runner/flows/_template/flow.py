"""新流程骨架。实现 run(page, params, ctx) 即可——core 已在 sys.path。

可直接 import 的内核能力：
  from primitives import upload_file, safe_fill, click_text, wait_idle, extract_all, extract_text, screenshot
  from llm import chat            # 需要大模型时（key 从 ~/.browser-runner/secrets.toml 取）

约定：
  · 写操作流程（write_ops=true）**填到「提交按钮前」就停，绝不自己点提交**——最后一下交回给人。
  · 拿不准/交互失败别硬崩：try/except → ctx.log 记一句 → 返回 dict 里带 todo，交人工补。
  · 产物写进 ctx.workdir（本次运行的专属目录）。
"""
from __future__ import annotations

from primitives import safe_fill, wait_idle  # noqa: F401 —— 按需增删


def run(page, params, ctx):
    ctx.log("开始")

    # 1) 导航（若 flow.toml 没设 landing_url 就在这 goto）
    # page.goto("https://example.com", wait_until="domcontentloaded")
    wait_idle(page, 800)

    # 2) 干活（读/填/点…）。dry_run 时只定位、不动作：
    # if not ctx.dry_run:
    #     safe_fill(page, 'input[name="q"]', params.get("example") or "")

    # 3) 写操作停在提交前（示例）：
    # page.get_by_text("提交").first.scroll_into_view_if_needed()

    todo: list[str] = []
    return {"stopped_at": "提交按钮前（请核对后手动点）", "todo": todo}
