#!/usr/bin/env python3
"""给 ComfyUI 工作流(UI 格式 .json)加**彩色分组框 + 说明 Note**,产出"分组版"高质量工作流。
这是 skill 的工作流出厂标准(见 reference/workflow-style.md):每个画布工作流都必须分组 + 带说明。

用法:
  python groupify.py <workflow.json> --spec <spec.json> [--inplace]
spec.json:
  {
    "groups": [
      {"title":"① 上传图片", "nodes":[1], "color":"#3f789e"},
      {"title":"② 加载模型", "nodes":[2,3,4], "color":"#444"}
    ],
    "note": "用法说明…(多行用 \\n)",
    "note_pos": [20, -200]            # 可选,默认工作流左上方
  }
每个 group 的 bounding 由其成员节点的实际 pos+size 自动算出(留 padding),所以**先排好节点再 groupify**。
"""
import argparse
import json

PAD_X, PAD_TOP, PAD_BOT = 24, 56, 24   # 组框内边距(顶部多留给标题)
DEFAULT_COLOR = "#3f789e"


def _bounds(nodes_by_id, ids):
    xs, ys, x2s, y2s = [], [], [], []
    for nid in ids:
        n = nodes_by_id.get(nid)
        if not n:
            continue
        x, y = n["pos"][0], n["pos"][1]
        w, h = (n.get("size") or [200, 100])[:2]
        xs.append(x); ys.append(y); x2s.append(x + w); y2s.append(y + h)
    if not xs:
        return None
    x, y = min(xs) - PAD_X, min(ys) - PAD_TOP
    return [x, y, max(x2s) + PAD_X - x, max(y2s) + PAD_BOT - y]


def groupify(wf, spec):
    nodes_by_id = {n["id"]: n for n in wf.get("nodes", [])}
    groups = []
    for i, g in enumerate(spec.get("groups", []), 1):
        b = _bounds(nodes_by_id, g["nodes"])
        if not b:
            continue
        groups.append({"id": i, "title": g["title"], "bounding": b,
                       "color": g.get("color", DEFAULT_COLOR), "font_size": 24, "flags": {}})
    wf["groups"] = groups
    note = spec.get("note")
    if note:
        wf["nodes"] = [n for n in wf["nodes"] if n.get("type") != "Note" or not n.get("_groupify")]
        nid = max([n["id"] for n in wf["nodes"]] + [0]) + 1
        px, py = spec.get("note_pos", [min(n["pos"][0] for n in wf["nodes"]),
                                       min(n["pos"][1] for n in wf["nodes"]) - 280])
        wf["nodes"].append({"id": nid, "type": "Note", "_groupify": True, "pos": [px, py],
                            "size": [1080, 240], "flags": {}, "order": 999, "mode": 0,
                            "inputs": [], "outputs": [], "properties": {}, "color": "#432",
                            "bgcolor": "#653", "widgets_values": [note]})
        wf["last_node_id"] = max(wf.get("last_node_id", 0), nid)
    return wf


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workflow")
    ap.add_argument("--spec", required=True)
    ap.add_argument("--inplace", action="store_true")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()
    wf = json.load(open(a.workflow))
    spec = json.load(open(a.spec))
    wf = groupify(wf, spec)
    out = a.workflow if a.inplace else (a.out or a.workflow.replace(".json", ".grouped.json"))
    json.dump(wf, open(out, "w"), ensure_ascii=False, indent=2)
    print(f"✓ 分组 {len(wf['groups'])} 组 + {'Note' if spec.get('note') else '无Note'} → {out}")


if __name__ == "__main__":
    main()
