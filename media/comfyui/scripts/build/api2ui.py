#!/usr/bin/env python3
"""把 API/prompt 格式工作流转成 UI/Litegraph 格式(画布可打开)。

ui2api 的逆操作。用运行中 ComfyUI 的 /object_info 拿每个节点的真实输入顺序/类型/
输出,生成扁平 litegraph 图:
- widget 输入按 schema 顺序放进 inputs[](带 "widget" 标记)+ widgets_values 对齐
- seed/noise_seed 后注入前端幽灵 widget control_after_generate(画布显示才不串位)
- 连接的"目标槽号"按**插入幽灵 widget 之后的最终 inputs[] 下标**算(画布画线靠槽号,
  错位就画不出线——这是逆转换最容易翻车的点)
- 自动栅格布点

用法: python api2ui.py <api.json> <out_ui.json>
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "core"))
from comfy_api import ComfyClient

WIDGET_TYPES = {"INT", "FLOAT", "STRING", "BOOLEAN", "COMBO"}
GHOST_AFTER = {"seed", "noise_seed"}  # 这些 widget 后前端会插 control_after_generate


def is_widget(spec):
    # forceInput 的输入强制当"连接口"(不是控件),如 SaveImageClean 的 name
    if isinstance(spec, list) and len(spec) > 1 and isinstance(spec[1], dict) and spec[1].get("forceInput"):
        return False
    t = spec[0] if isinstance(spec, list) and spec else spec
    if isinstance(t, list):       # 旧版 COMBO:选项列表当 type
        return True
    return t in WIDGET_TYPES      # 含新版 IO 的字符串 "COMBO"


def _type_of(spec):
    t = spec[0] if isinstance(spec, list) and spec else spec
    return "COMBO" if isinstance(t, list) else t


def _default(spec):
    if isinstance(spec, list) and len(spec) > 1 and isinstance(spec[1], dict):
        d = spec[1]
        if "default" in d:
            return d["default"]
        if isinstance(d.get("options"), list) and d["options"]:
            return d["options"][0]
    if isinstance(spec, list) and spec and isinstance(spec[0], list) and spec[0]:
        return spec[0][0]
    return ""


def main():
    api = json.load(open(sys.argv[1]))
    api = {k: v for k, v in api.items() if isinstance(v, dict) and "class_type" in v}
    oi = ComfyClient().object_info()

    node_inputs, node_widgets = {}, {}     # nid -> inputs[](link 待填) / widgets_values
    link_reqs = []                         # (dst_id, dst_slot, src_id, src_slot, type)

    # 第一遍:按 schema 顺序构造每个节点的最终 inputs[](含幽灵 widget),
    # 连接输入记录它在最终 inputs[] 里的真实下标。
    for nid, node in api.items():
        info = oi.get(node["class_type"], {})
        req = info.get("input", {}).get("required") or {}
        opt = info.get("input", {}).get("optional") or {}
        uin, wv = [], []
        for name, spec in list(req.items()) + list(opt.items()):
            typ = _type_of(spec)
            if is_widget(spec):
                uin.append({"name": name, "type": typ, "widget": {"name": name}, "link": None})
                wv.append(node["inputs"].get(name, _default(spec)))
                if name in GHOST_AFTER:
                    uin.append({"name": "control_after_generate", "type": "COMBO",
                                "widget": {"name": "control_after_generate"}, "link": None})
                    wv.append("fixed")
            else:
                slot = len(uin)                      # ← 最终 inputs[] 下标
                uin.append({"name": name, "type": typ, "link": None})
                val = node["inputs"].get(name)
                if isinstance(val, list) and len(val) == 2:
                    link_reqs.append((nid, slot, str(val[0]), val[1], typ))
        node_inputs[nid], node_widgets[nid] = uin, wv

    # 第二遍:建 links,回填每个输入的 link 与每个输出的 links。
    links, out_links, lid = [], {nid: {} for nid in api}, 0
    for dst, dslot, src, sslot, typ in link_reqs:
        lid += 1
        links.append([lid, int(src), sslot, int(dst), dslot, typ])
        node_inputs[dst][dslot]["link"] = lid
        out_links[src].setdefault(sslot, []).append(lid)

    # 拓扑分层布点:列 = 距源头(无输入连接的 loader)的最长路径,行 = 列内序号。
    # 画布从左到右就是数据流向(loader→编码→采样→解码→保存),可读性强。
    preds = {nid: [] for nid in api}
    for l in links:                       # [lid, src, sslot, dst, dslot, type]
        preds[str(l[3])].append(str(l[1]))
    memo = {}
    def column(nid, seen=()):
        if nid in memo:
            return memo[nid]
        if nid in seen:                   # 防环
            return 0
        ps = preds.get(nid, [])
        c = 0 if not ps else 1 + max(column(p, seen + (nid,)) for p in ps)
        memo[nid] = c
        return c
    cols = {nid: column(nid) for nid in api}
    row_of, rowcount = {}, {}
    for nid in api:
        c = cols[nid]
        row_of[nid] = rowcount.get(c, 0)
        rowcount[c] = row_of[nid] + 1
    x0, y0, dx, dy = 60, 80, 380, 320

    # 第三遍:组装节点(输出槽按 schema output 顺序;无幽灵,下标即 schema 序)。
    nodes = []
    for i, (nid, node) in enumerate(api.items()):
        info = oi.get(node["class_type"], {})
        outs = info.get("output") or []
        onames = info.get("output_name") or outs
        ui_out = [{"name": onames[j] if j < len(onames) else outs[j], "type": outs[j],
                   "links": out_links[nid].get(j, []), "slot_index": j} for j in range(len(outs))]
        nodes.append({
            "id": int(nid), "type": node["class_type"],
            "pos": [x0 + cols[nid] * dx, y0 + row_of[nid] * dy], "size": [320, 220],
            "flags": {}, "order": i, "mode": 0,
            "inputs": node_inputs[nid], "outputs": ui_out,
            "properties": {"Node name for S&R": node["class_type"]},
            "widgets_values": node_widgets[nid],
        })

    ui = {"last_node_id": max(int(n) for n in api), "last_link_id": lid,
          "nodes": nodes, "links": links, "groups": [], "config": {}, "extra": {}, "version": 0.4}
    json.dump(ui, open(sys.argv[2], "w"), ensure_ascii=False, indent=2)
    print(f"✓ UI 格式已写出: {sys.argv[2]} ({len(nodes)} 节点, {lid} 连接)")


if __name__ == "__main__":
    main()
