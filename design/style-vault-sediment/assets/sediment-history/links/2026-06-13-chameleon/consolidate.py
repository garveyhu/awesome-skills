#!/usr/bin/env python3
"""把 126 个 discovery 候选合并成连贯的最终沉淀计划。"""
import json, sys
from pathlib import Path

# 这次沉淀的工作目录 = 本文件所在目录（历史存档，与 discovery-raw.json / plan.md 同放）。
# 原先写死绝对路径，随 skill 公开分发时既无效又暴露本地布局。
WORK = str(Path(__file__).resolve().parent)
raw = json.load(open(WORK + "/discovery-raw.json"))
cands = {c["proposed_id"]: c for c in raw["candidates"]}  # 注意有重名，后者覆盖；下面 from 用列表合并

# 重新建按 id 收集（同 id 多份合并 source/spec）
multi = {}
for c in raw["candidates"]:
    multi.setdefault(c["proposed_id"], []).append(c)

# ── 最终条目定义：id / layer / dedup / ref / sig / from(原候选 id 列表) ──
# dedup: new | ref | variant ;  ref=被复用的 waveflow id（variant/ref 用）
FINAL = [
 # ===== TOKENS (5 新建/variant) =====
 ("tokens/palettes/chameleon/themeable-8x4-system","token","variant","tokens/palettes/waveflow/warm-paper-ink-blue",1,
   ["tokens/palettes/chameleon/themeable-8x4-system","tokens/palettes/chameleon/themeable-neutral-accent-switch","tokens/palettes/chameleon/warm-paper-ink-blue"]),
 ("tokens/motion/chameleon/neon-ai-suite","token","new","",1,
   ["tokens/motion/chameleon/neon-ai-loader","tokens/motion/chameleon/neon-ai-gradient-suite"]),
 ("tokens/motion/chameleon/keyframes-anim-modes","token","variant","tokens/motion/waveflow/keyframes-suite",0,
   ["tokens/motion/chameleon/keyframes-suite","tokens/motion/chameleon/theme-anim-modes"]),
 ("tokens/palettes/chameleon/node-type-hue-system","token","new","",1,
   ["tokens/palettes/chameleon/node-type-hue-system"]),
 ("tokens/motion/chameleon/canvas-edge-dash-flow","token","new","",1,
   ["tokens/motion/chameleon/canvas-edge-dash-flow"]),

 # ===== COMPONENTS (~21) =====
 ("components/buttons/chameleon/themeable-cva-button","component","variant","components/buttons/waveflow/cva-engineer-button",1,
   ["components/buttons/chameleon/themeable-cva-button"]),
 ("components/inputs/chameleon/themeable-text-fields","component","variant","components/inputs/waveflow/blue-focus-input",0,
   ["components/inputs/chameleon/compact-textarea","components/inputs/chameleon/themeable-label","components/inputs/waveflow/blue-focus-input"]),
 ("components/toggles/chameleon/themeable-switch","component","variant","components/toggles/waveflow/emerald-switch",0,
   ["components/toggles/chameleon/themeable-switch"]),
 ("components/toggles/chameleon/sliding-thumb-segmented","component","new","",1,
   ["components/toggles/chameleon/sliding-thumb-segmented"]),
 ("components/tags-badges/chameleon/cva-semantic-badge","component","variant","components/tags-badges/waveflow/code-status-badge",0,
   ["components/tags-badges/chameleon/cva-semantic-badge"]),
 ("components/tags-badges/chameleon/orchestration-kind-badge","component","variant","components/tags-badges/waveflow/glue-type-badge-duo",0,
   ["components/tags-badges/chameleon/orchestration-kind-badge"]),
 ("components/indicators/chameleon/status-pill-ping-dot","component","variant","components/indicators/waveflow/status-dot-ring",0,
   ["components/indicators/chameleon/status-pill-ping-dot"]),
 ("components/selects/chameleon/radix-single-select","component","new","",0,
   ["components/selects/chameleon/radix-single-select"]),
 ("components/selects/chameleon/agent-picker-popover","component","new","",0,
   ["components/selects/chameleon/paginated-category-agent-picker","components/selects/chameleon/agent-picker-category-popover"]),
 ("components/selects/chameleon/model-picker-popover","component","new","",0,
   ["components/selects/chameleon/model-picker-provider-popover","components/selects/chameleon/image-model-inline-select"]),
 ("components/inputs/chameleon/param-slider","component","new","",0,
   ["components/inputs/chameleon/param-slider"]),
 ("components/inputs/chameleon/codemirror-json-editor","component","new","",1,
   ["components/inputs/chameleon/codemirror-json-editor"]),
 ("components/inputs/chameleon/dayjs-range-picker","component","variant","components/inputs/waveflow/datetime-range-presets",0,
   ["components/inputs/chameleon/dayjs-range-picker","components/inputs/chameleon/month-calendar-range","components/inputs/chameleon/calendar-range-presets"]),
 ("components/inputs/chameleon/inline-edit-cell","component","new","",0,
   ["components/inputs/chameleon/inline-edit-cell"]),
 ("components/inputs/chameleon/graph-config-field-kit","component","new","",1,
   ["components/inputs/chameleon/prompt-var-editor","components/inputs/chameleon/var-tree-picker","components/inputs/chameleon/const-var-switch-field","components/inputs/chameleon/table-editor","components/inputs/chameleon/code-mirror-field","components/inputs/chameleon/slider-number-field"]),
 ("components/display/chameleon/paper-card-shell","component","new","",0,
   ["components/display/chameleon/paper-card-shell"]),
 ("components/display/chameleon/stat-tile-delta","component","new","",0,
   ["components/display/chameleon/stat-tile","components/display/chameleon/stat-tile-delta","components/display/chameleon/icon-mono-mini-stat","components/display/chameleon/hairline-stat-bar"]),
 ("components/display/chameleon/recharts-time-series","component","new","",1,
   ["components/display/chameleon/recharts-time-series"]),
 ("components/display/chameleon/json-viewer-cell","component","new","",0,
   ["components/display/chameleon/json-cell-collapsible","components/feedback/chameleon/zero-dep-json-viewer"]),
 ("components/display/chameleon/distribution-score-bars","component","new","",0,
   ["components/display/chameleon/distribution-top-bars-card","components/indicators/chameleon/channel-score-bars","components/tags-badges/chameleon/score-heat-cell"]),
 ("components/feedback/chameleon/radix-overlay-primitives","component","new","",0,
   ["components/feedback/chameleon/radix-dialog-shell","components/feedback/chameleon/radix-popover-shell","components/feedback/chameleon/radix-dropdown-menu","components/feedback/chameleon/dark-tooltip"]),
 ("components/feedback/chameleon/modal-sheet-confirm","component","new","",0,
   ["components/feedback/chameleon/sized-modal-shell","components/feedback/chameleon/right-slide-sheet","components/feedback/chameleon/imperative-confirm"]),
 ("components/feedback/chameleon/neon-loader","component","new","",1,
   ["components/feedback/chameleon/neon-loader","components/feedback/chameleon/neon-loader-conic-glow"]),
 ("components/feedback/chameleon/loading-skeleton-kit","component","new","",0,
   ["components/feedback/chameleon/shimmer-skeleton-kit","components/feedback/chameleon/image-gen-loading-skeleton","components/feedback/chameleon/image-gen-skeleton-loader"]),
 ("components/feedback/chameleon/amber-nav-progress","component","variant","blocks/feedback/waveflow/top-progress-bar",0,
   ["components/feedback/chameleon/amber-climb-nav-progress","blocks/feedback/chameleon/amber-creep-progress-bar"]),
 ("components/avatars-icons/chameleon/provider-bot-avatar","component","new","",0,
   ["components/avatars-icons/chameleon/provider-brand-avatar","components/avatars-icons/chameleon/gradient-bot-avatar"]),
 ("components/display/chameleon/dynamic-virtual-list","component","new","",0,
   ["components/display/chameleon/dynamic-virtual-list"]),

 # ===== BLOCKS · canvas (xyflow 工作流画布 signature suite) =====
 ("blocks/canvas/chameleon/node-palette","block","new","",1,
   ["blocks/canvas/chameleon/node-palette"]),
 ("blocks/canvas/chameleon/graph-node-card","block","new","",1,
   ["blocks/canvas/chameleon/graph-node-card","components/indicators/chameleon/node-handle-dot"]),
 ("blocks/canvas/chameleon/bezier-edge-add","block","new","",1,
   ["blocks/canvas/chameleon/bezier-edge-add"]),
 ("blocks/canvas/chameleon/config-panel-inspector","block","new","",1,
   ["blocks/canvas/chameleon/config-panel-inspector","blocks/canvas/chameleon/if-else-condition-builder","components/feedback/chameleon/node-hover-toolbar"]),
 ("blocks/canvas/chameleon/subflow-group-editor","block","new","",1,
   ["blocks/canvas/chameleon/subflow-group-editor"]),
 ("blocks/canvas/chameleon/canvas-controls-menus","block","new","",0,
   ["blocks/canvas/chameleon/canvas-floating-controls","blocks/canvas/chameleon/canvas-context-menus"]),
 ("blocks/canvas/chameleon/ai-copilot-panel","block","new","",1,
   ["blocks/canvas/chameleon/ai-copilot-panel"]),
 ("blocks/form/chameleon/graph-run-dialog","block","new","",0,
   ["blocks/form/chameleon/graph-run-dialog","blocks/layout/chameleon/version-history-drawer"]),

 # ===== BLOCKS · nav/layout (导航重构) =====
 ("blocks/layout/chameleon/domain-tab-app-shell","block","variant","tokens/layout/waveflow/data-console-shell",1,
   ["blocks/layout/chameleon/domain-tab-app-shell"]),
 ("blocks/nav/chameleon/domain-tab-topbar-account","block","variant","blocks/nav/waveflow/topbar-search-ping",1,
   ["blocks/nav/chameleon/domain-tab-topbar-account"]),
 ("blocks/nav/chameleon/borderless-bookmark-rail","block","variant","blocks/nav/waveflow/tree-line-sidebar",1,
   ["blocks/nav/chameleon/borderless-bookmark-rail"]),
 ("blocks/nav/chameleon/cmdk-grouped-palette","block","variant","blocks/nav/waveflow/cmdk-search-modal",0,
   ["blocks/nav/chameleon/cmdk-grouped-palette"]),
 ("blocks/nav/chameleon/detail-left-tab-rail","block","new","",0,
   ["blocks/nav/chameleon/detail-left-tab-rail","blocks/nav/chameleon/graph-app-rail"]),

 # ===== BLOCKS · display =====
 ("blocks/display/chameleon/responsive-overlay-data-table","block","variant","blocks/display/waveflow/data-table-leftbar-shimmer",1,
   ["blocks/display/chameleon/responsive-overlay-data-table","components/typography-atoms/chameleon/hint-column-header"]),
 ("blocks/display/chameleon/trace-observation-tree-gantt","block","new","",1,
   ["blocks/display/chameleon/trace-observation-tree","blocks/display/chameleon/trace-gantt-timeline"]),
 ("blocks/display/chameleon/eval-spreadsheet-airtable","block","new","",1,
   ["blocks/display/chameleon/eval-spreadsheet-airtable"]),
 ("blocks/display/chameleon/run-compare-heatmap-matrix","block","new","",1,
   ["blocks/display/chameleon/run-compare-heatmap-matrix"]),
 ("blocks/display/chameleon/kb-chunking-3pane-preview","block","new","",1,
   ["blocks/display/chameleon/kb-chunking-3pane-preview"]),
 ("blocks/display/chameleon/kb-hit-test-3pane","block","new","",1,
   ["blocks/display/chameleon/kb-hit-test-3pane"]),
 ("blocks/display/chameleon/kb-chunk-card-wall","block","new","",0,
   ["blocks/display/chameleon/kb-chunk-card-wall"]),
 ("blocks/display/chameleon/app-card-gallery-grid","block","new","",1,
   ["blocks/display/chameleon/app-card-gallery-grid"]),
 ("blocks/layout/chameleon/run-master-detail-rail-overlay","block","variant","blocks/layout/waveflow/master-detail-list-aside",0,
   ["blocks/layout/chameleon/run-master-detail-rail-overlay"]),

 # ===== BLOCKS · chat (playground/对话/embed signature) =====
 ("blocks/chat/chameleon/message-list-bubble-thread","block","new","",1,
   ["blocks/chat/chameleon/message-list-bubble-thread","blocks/chat/chameleon/playground-message-bubbles"]),
 ("blocks/chat/chameleon/markdown-message-citation","block","new","",0,
   ["blocks/chat/chameleon/markdown-message-lite","blocks/chat/chameleon/citation-collapse-row"]),
 ("blocks/chat/chameleon/message-actions-bar","block","new","",1,
   ["blocks/chat/chameleon/message-actions-bar"]),
 ("blocks/chat/chameleon/hitl-human-input-prompt","block","new","",1,
   ["blocks/chat/chameleon/hitl-human-input-prompt"]),
 ("blocks/chat/chameleon/composer-attach-send","block","new","",0,
   ["blocks/chat/chameleon/composer-attach-send","blocks/chat/chameleon/playground-param-panel"]),
 ("blocks/chat/chameleon/embed-widget-bubble-shell","block","new","",1,
   ["blocks/chat/chameleon/embed-widget-bubble-shell"]),

 # ===== BLOCKS · form/filters/feedback (variants + 独有表单) =====
 ("blocks/form/chameleon/json-schema-dynamic-form","block","new","",1,
   ["blocks/form/chameleon/json-schema-dynamic-form"]),
 ("blocks/form/chameleon/generation-panel","block","new","",1,
   ["blocks/form/chameleon/generation-panel"]),
 ("blocks/filters/chameleon/table-toolbar-refresh-leading","block","variant","blocks/filters/waveflow/table-toolbar-tri",0,
   ["blocks/filters/chameleon/table-toolbar-refresh-leading"]),
 ("blocks/feedback/chameleon/flair-glow-empty-state","block","variant","blocks/feedback/waveflow/empty-dashed-state",1,
   ["blocks/feedback/chameleon/flair-glow-empty-state"]),
 ("blocks/form/chameleon/select-summary-cron-builder","block","variant","blocks/form/waveflow/cron-builder-modal",0,
   ["blocks/form/chameleon/select-summary-cron-builder"]),

 # ===== PAGES (9 独特页) =====
 ("pages/editor/chameleon/workflow-graph-editor","page","new","",1,
   ["pages/editor/chameleon/workflow-graph-editor"]),
 ("pages/playground/chameleon/model-compare-chat-lab","page","new","",1,
   ["pages/playground/chameleon/model-compare-chat-lab","pages/playground/chameleon/playground-chat-single-compare"]),
 ("pages/dashboard/chameleon/observability-overview-tabs","page","new","",1,
   ["pages/dashboard/chameleon/observability-overview-tabs"]),
 ("pages/detail/chameleon/trace-detail-tree-gantt","page","new","",1,
   ["pages/detail/chameleon/trace-detail-tree-gantt"]),
 ("pages/detail/chameleon/kb-detail-tabbed-workbench","page","new","",1,
   ["pages/detail/chameleon/kb-detail-tabbed-workbench"]),
 ("pages/detail/chameleon/eval-dataset-detail-spreadsheet","page","new","",1,
   ["pages/detail/chameleon/eval-dataset-detail-spreadsheet"]),
 ("pages/detail/chameleon/eval-run-detail-master-detail","page","new","",0,
   ["pages/detail/chameleon/eval-run-detail-master-detail"]),
 ("pages/list-table/chameleon/app-card-library","page","new","",0,
   ["pages/list-table/chameleon/app-card-library"]),
 ("pages/chat/chameleon/embed-fullscreen-chat","page","new","",0,
   ["pages/chat/chameleon/embed-fullscreen-chat","pages/chat/chameleon/conversation-detail-bubbles"]),
]

# ── 打包：每条最终条目汇聚其 from 候选的 source/spec ──
consumed = set()
entries = []
missing = []
for fid, layer, dedup, ref, sig, froms in FINAL:
    srcs=[]; specs=[]; descs=[]; uses=set(); aes=set(); mds=set()
    for fr in froms:
        consumed.add(fr)
        if fr not in multi:
            missing.append((fid, fr)); continue
        for c in multi[fr]:
            srcs += c.get("source_files",[])
            if c.get("visual_spec"): specs.append(f"[{fr}] "+c["visual_spec"])
            if c.get("description"): descs.append(c["description"])
            for u in c.get("refs_uses",[]) or []: uses.add(u)
            for a in c.get("tags_aesthetic",[]) or []: aes.add(a)
            for m in c.get("tags_mood",[]) or []: mds.add(m)
    entries.append({
        "id":fid,"layer":layer,"dedup":dedup,"ref_target":ref,"signature":bool(sig),
        "name":"", "source_files":sorted(set(srcs)),
        "visual_spec":"\n\n".join(specs),"descriptions":descs,
        "refs_uses":sorted(uses),"tags_aesthetic":sorted(aes),"tags_mood":sorted(mds),
    })

# 收集 product 要 cross-namespace ref 的 waveflow 条目（来自纯 ref 候选 + variant 的 ref_target）
ref_waveflow=set()
for c in raw["candidates"]:
    pid=c["proposed_id"]
    if pid in consumed:
        # variant 的 ref_target 也加入复用清单
        continue
    if c.get("dedup","").startswith("ref:"):
        ref_waveflow.add(c["dedup"].split("ref:",1)[1].strip())
for e in entries:
    if e["dedup"] in ("ref","variant") and e["ref_target"]:
        ref_waveflow.add(e["ref_target"])

# 未被任何最终条目消费的候选（审计漏网）
unconsumed=[c["proposed_id"] for c in raw["candidates"] if c["proposed_id"] not in consumed]

out={"entries":entries,"ref_waveflow":sorted(ref_waveflow),
     "stats":{"total":len(entries),
              "by_layer":{l:sum(1 for e in entries if e["layer"]==l) for l in ["token","component","block","page"]},
              "by_dedup":{d:sum(1 for e in entries if e["dedup"]==d) for d in ["new","variant","ref"]},
              "signature":sum(1 for e in entries if e["signature"])}}
json.dump(out, open(WORK+"/plan-entries.json","w"), ensure_ascii=False, indent=1)

print("最终条目:", out["stats"]["total"], out["stats"]["by_layer"], out["stats"]["by_dedup"], "| signature:", out["stats"]["signature"])
print("product 复用 waveflow:", len(ref_waveflow), "条")
if missing: print("!! from 未匹配:", missing)
print("\n未被消费的原候选 (",len(unconsumed),"):")
for u in unconsumed: print("   ?", u)
