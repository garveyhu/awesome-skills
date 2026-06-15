#!/usr/bin/env python3
"""把 ComfyUI 的 UI/Litegraph 格式工作流转成 API/prompt 格式。

为什么需要：ComfyUI 自带的 443 个官方模板、以及网上绝大多数分享的工作流，
都是 UI 格式（网页编辑器保存的，带 nodes/links/坐标/widgets_values）。
要让本 skill 的引擎直接 POST /prompt 自动执行，必须先转成扁平的 API 格式。

转换规则（与 ComfyUI 前端逻辑对齐）：
- links 数组 [link_id, src_node, src_slot, dst_node, dst_slot, type] → 目标节点输入填 [src_id, src_slot]
- widgets_values 按节点 inputs[] 里"widget 输入"出现顺序回填到对应输入名
- **幽灵 widget**：带 seed 的节点其后会插一个 control_after_generate（值如 "randomize"），
  API 格式没有这个字段，必须丢弃——这是 UI↔API 转换最常见的翻车点
- 用运行中 ComfyUI 的 /object_info 校验输入名，丢掉任何非法输入（兜底清除其它幽灵 widget）

局限：不展开 subgraph、不解析 Primitive/Reroute 节点（新式官方模板常用）。
遇到这些会明确报错，提示改用扁平模板或手写。LingyiChen 系列与多数简单官方模板均为扁平结构，可直接转。
"""

from __future__ import annotations

import json
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "core"))

# 这些是 UI 专用、非执行节点，转换时跳过
SKIP_TYPES = {"Note", "MarkdownNote"}
# 这些节点会让扁平转换失真，遇到直接报错让用户知情
UNSUPPORTED_TYPES = {
    "Reroute", "PrimitiveNode", "PrimitiveInt", "PrimitiveFloat",
    "PrimitiveString", "PrimitiveStringMultiline", "PrimitiveBoolean", "GetNode", "SetNode",
}
# 永远要丢弃的幽灵 widget（即使 object_info 不可用）
GHOST_WIDGETS = {"control_after_generate", "control_before_generate"}


class ConvertError(RuntimeError):
    pass


def _build_link_map(ui: dict) -> dict:
    """link_id -> (src_node_id, src_slot)。"""
    links = {}
    for l in ui.get("links", []) or []:
        if isinstance(l, list) and len(l) >= 3:
            links[l[0]] = (l[1], l[2])
        elif isinstance(l, dict):  # 个别新格式 links 是对象
            links[l.get("id")] = (l.get("origin_id"), l.get("origin_slot"))
    return links


def convert(ui: dict, valid_inputs: dict | None = None) -> dict:
    """UI dict -> API dict。valid_inputs: {class_type: set(合法输入名)}，可选校验。"""
    if ui.get("definitions", {}).get("subgraphs"):
        raise ConvertError(
            "该工作流含 subgraph（子图），扁平转换器不支持。\n"
            "  请在 ComfyUI 网页里展开子图后另存，或改用本 skill 的内置构建器。"
        )
    links = _build_link_map(ui)
    api: dict = {}
    for node in ui.get("nodes", []):
        ctype = node.get("type")
        if ctype in SKIP_TYPES:
            continue
        if ctype in UNSUPPORTED_TYPES:
            raise ConvertError(
                f"节点 {ctype}(id={node.get('id')}) 是 Primitive/Reroute/子图引用，扁平转换器不支持。\n"
                f"  请改用扁平结构的模板，或手写该工作流的 API 格式。"
            )
        valid = valid_inputs.get(ctype) if valid_inputs else None
        inputs: dict = {}
        wv = node.get("widgets_values") or []
        wi = 0
        for inp in node.get("inputs", []) or []:
            name = inp.get("name")
            link = inp.get("link")
            has_widget = "widget" in inp
            # 幽灵 widget(control_after/before_generate)的值在 widgets_values 里**紧跟 seed**,
            # 与它在 inputs 数组里的位置无关。所以这里不按 inputs 顺序消费它(否则 inputs 把它
            # 排到末尾时会让 seed 后的 'fixed' 错配给 steps,导致整列偏移)——改在 seed 处跳过。
            if name in GHOST_WIDGETS:
                continue
            if link is not None and link in links:
                src_id, src_slot = links[link]
                inputs[name] = [str(src_id), src_slot]
                # 被"转为输入"的 widget 不在 widgets_values 里占位，不推进 wi
            elif has_widget:
                if wi >= len(wv):
                    continue
                val = wv[wi]
                wi += 1
                # seed/noise_seed 后若紧跟 control_after_generate 的值,跳过它
                if name in ("seed", "noise_seed") and wi < len(wv) \
                        and isinstance(wv[wi], str) \
                        and wv[wi] in ("fixed", "randomize", "increment", "decrement"):
                    wi += 1
                if valid is not None and name not in valid:
                    continue  # 丢弃其它非法/幽灵 widget
                inputs[name] = val
        api[str(node.get("id"))] = {"class_type": ctype, "inputs": inputs}
    if not api:
        raise ConvertError("转换结果为空：可能不是有效的 UI 格式工作流")
    return api


def _load_valid_inputs() -> dict | None:
    """连得上 ComfyUI 时，拉取每个节点的合法输入名用于校验；连不上则返回 None。"""
    try:
        from comfy_api import ComfyClient
        c = ComfyClient()
        full = c.object_info()
        out = {}
        for ctype, info in full.items():
            req = (info.get("input", {}).get("required") or {}).keys()
            opt = (info.get("input", {}).get("optional") or {}).keys()
            out[ctype] = set(req) | set(opt)
        return out
    except Exception:
        return None


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("用法: python ui2api.py <ui_workflow.json> [out_api.json]\n"
                 "  不给输出路径则打印到 stdout。")
    src = sys.argv[1]
    with open(src) as f:
        ui = json.load(f)
    # 已经是 API 格式（扁平 dict，值含 class_type）就直接透传
    if isinstance(ui, dict) and "nodes" not in ui and all(
        isinstance(v, dict) and "class_type" in v for v in ui.values()
    ):
        api = ui
    else:
        api = convert(ui, _load_valid_inputs())
    out = json.dumps(api, ensure_ascii=False, indent=2)
    if len(sys.argv) >= 3:
        with open(sys.argv[2], "w") as f:
            f.write(out)
        print(f"✓ 已写出 API 格式: {sys.argv[2]}  ({len(api)} 个节点)")
    else:
        print(out)


if __name__ == "__main__":
    main()
