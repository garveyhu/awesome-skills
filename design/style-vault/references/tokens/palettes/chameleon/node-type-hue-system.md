---
id: tokens/palettes/chameleon/node-type-hue-system
type: token
name: 节点类型 hue 系统
description: 工作流画布每种节点一套互相咬合的 5 槽配色（700 前景 / 200 ring / 50 图标底 / 50/40 整卡色温 / 500 连线 hex）+ 变量类型 6 色 chip
platforms:
- web
theme: light
tags:
  aesthetic:
  - minimal
  - industrial
  mood:
  - calm
  - serious
  stack:
  - shadcn-radix
uses:
- tokens/palettes/waveflow/warm-paper-ink-blue
preview: /preview/tokens/palettes/chameleon/node-type-hue-system
---

# Chameleon Node Type Hue System

> 工作流画布每种节点类型一套**互相咬合的 5 阶配色**：图标前景 `text-{hue}-700` / 选中环 `ring-{hue}-200` / 图标块底 `bg-{hue}-50` / 整卡极淡色温 `bg-{hue}-50/40` / 连线高亮 `#{hue}-500 hex`。23 种节点类型各占一个 hue，是画布「色彩锚点」signature 的数据底座。底层主色 blue-600 复用 waveflow 暖纸墨蓝板。

## Tokens

```json
{
  "node-slots": {
    "color": "text-{hue}-700  (图标前景，700 阶在白底上沉稳)",
    "ring": "ring-{hue}-200  (选中态环)",
    "bg": "bg-{hue}-50  (图标块底，仅图标方块这一小块)",
    "cardTint": "bg-{hue}-50/40  (整卡极淡色温，slate/stone/green 用 50/50)",
    "edgeColor": "#{hue}-500 hex  (相邻边高亮，500 阶在细线上最亮)"
  },
  "node-hues": {
    "start":         { "hue": "emerald", "color": "text-emerald-700", "ring": "ring-emerald-200", "bg": "bg-emerald-50", "cardTint": "bg-emerald-50/40", "edge": "#10b981" },
    "end":           { "hue": "stone",   "color": "text-stone-700",   "ring": "ring-stone-300",   "bg": "bg-stone-50",   "cardTint": "bg-stone-50/50",   "edge": "#78716c" },
    "llm":           { "hue": "violet",  "color": "text-violet-700",  "ring": "ring-violet-200",  "bg": "bg-violet-50",  "cardTint": "bg-violet-50/40",  "edge": "#8b5cf6" },
    "image_gen":     { "hue": "purple",  "color": "text-purple-700",  "ring": "ring-purple-200",  "bg": "bg-purple-50",  "cardTint": "bg-purple-50/40",  "edge": "#a855f7" },
    "kb":            { "hue": "emerald", "color": "text-emerald-700", "ring": "ring-emerald-200", "bg": "bg-emerald-50", "cardTint": "bg-emerald-50/40", "edge": "#10b981" },
    "tool":          { "hue": "orange",  "color": "text-orange-700",  "ring": "ring-orange-200",  "bg": "bg-orange-50",  "cardTint": "bg-orange-50/40",  "edge": "#f97316" },
    "if_else":       { "hue": "amber",   "color": "text-amber-700",   "ring": "ring-amber-200",   "bg": "bg-amber-50",   "cardTint": "bg-amber-50/40",   "edge": "#f59e0b" },
    "agent_debate":  { "hue": "fuchsia", "color": "text-fuchsia-700", "ring": "ring-fuchsia-200", "bg": "bg-fuchsia-50", "cardTint": "bg-fuchsia-50/40", "edge": "#d946ef" },
    "iteration":     { "hue": "sky",     "color": "text-sky-700",     "ring": "ring-sky-200",     "bg": "bg-sky-50",     "cardTint": "bg-sky-50/40",     "edge": "#0ea5e9" },
    "parallel":      { "hue": "indigo",  "color": "text-indigo-700",  "ring": "ring-indigo-200",  "bg": "bg-indigo-50",  "cardTint": "bg-indigo-50/40",  "edge": "#6366f1" },
    "human_input":   { "hue": "pink",    "color": "text-pink-700",    "ring": "ring-pink-200",    "bg": "bg-pink-50",    "cardTint": "bg-pink-50/40",    "edge": "#ec4899" },
    "http":          { "hue": "cyan",    "color": "text-cyan-700",    "ring": "ring-cyan-200",    "bg": "bg-cyan-50",    "cardTint": "bg-cyan-50/40",    "edge": "#06b6d4" },
    "aggregator":    { "hue": "amber",   "color": "text-amber-800",   "ring": "ring-amber-200",   "bg": "bg-amber-50",   "cardTint": "bg-amber-50/40",   "edge": "#f59e0b" },
    "assign":        { "hue": "rose",    "color": "text-rose-700",    "ring": "ring-rose-200",    "bg": "bg-rose-50",    "cardTint": "bg-rose-50/40",    "edge": "#f43f5e" },
    "classifier":    { "hue": "lime",    "color": "text-lime-700",    "ring": "ring-lime-200",    "bg": "bg-lime-50",    "cardTint": "bg-lime-50/40",    "edge": "#84cc16" },
    "param_extract": { "hue": "blue",    "color": "text-blue-700",    "ring": "ring-blue-200",    "bg": "bg-blue-50",    "cardTint": "bg-blue-50/40",    "edge": "#3b82f6" },
    "subflow":       { "hue": "indigo",  "color": "text-indigo-700",  "ring": "ring-indigo-200",  "bg": "bg-indigo-50",  "cardTint": "bg-indigo-50/40",  "edge": "#6366f1" },
    "list_op":       { "hue": "cyan",    "color": "text-cyan-800",    "ring": "ring-cyan-200",    "bg": "bg-cyan-50",    "cardTint": "bg-cyan-50/40",    "edge": "#06b6d4" },
    "doc_extract":   { "hue": "orange",  "color": "text-orange-700",  "ring": "ring-orange-200",  "bg": "bg-orange-50",  "cardTint": "bg-orange-50/40",  "edge": "#f97316" },
    "code":          { "hue": "slate",   "color": "text-slate-700",   "ring": "ring-slate-300",   "bg": "bg-slate-50",   "cardTint": "bg-slate-50/50",   "edge": "#64748b" },
    "template":      { "hue": "teal",    "color": "text-teal-700",    "ring": "ring-teal-200",    "bg": "bg-teal-50",    "cardTint": "bg-teal-50/40",    "edge": "#14b8a6" },
    "answer":        { "hue": "green",   "color": "text-green-700",   "ring": "ring-green-200",   "bg": "bg-green-50",   "cardTint": "bg-green-50/40",   "edge": "#22c55e" },
    "noop":          { "hue": "stone",   "color": "text-stone-500",   "ring": "ring-stone-200",   "bg": "bg-white",      "cardTint": "bg-stone-50/50",   "edge": "#78716c" }
  },
  "var-type-chip": {
    "string":  "bg-sky-50 text-sky-600",
    "number":  "bg-amber-50 text-amber-600",
    "boolean": "bg-rose-50 text-rose-600",
    "object":  "bg-violet-50 text-violet-600",
    "array":   "bg-emerald-50 text-emerald-600",
    "any":     "bg-stone-100 text-stone-400",
    "shape":   "rounded px-1 py-px font-mono text-[9px] leading-none tracking-wide"
  }
}
```

## 视觉特征

- **5 槽同 hue 不同阶**：图标前景取 **700 阶**（白底上沉稳不刺眼）、ring 取 **200 阶**（选中态柔和）、图标块底取 **50 阶**（最浅）、整卡色温取 **50/40**（几乎是白、只有一丝色温）、连线取 **500 阶 hex**（细线上最亮，700 在线上偏暗发闷）
- **cardTint 是整卡染色不是色条**：用 `bg-{hue}-50/40` 把**整张卡**均匀微染，色彩成为卡片自身表面色，整卡一体、无任何分界缝——取代了被否的「左色条」方案；更强的类型信号靠彩色图标块 + 类型副标题色承载
- **特例阶**：`aggregator` 前景用 800（比常规 700 更深、与同 hue 的 if_else 700 区分）；`list_op` 前景用 cyan-800（与 http 的 cyan-700 区分）；`code` 用 slate（中性偏冷的"程序感"）ring 取 300；`noop` 图标底用纯 `bg-white`、前景仅 500（最弱信号，占位/调试）
- **同 hue 多节点靠副标题 + 图标区分**：emerald 同时给 start/kb、indigo 同时给 parallel/subflow、cyan 给 http/list_op、orange 给 tool/doc_extract、amber 给 if_else/aggregator——hue 复用但节点图标与中文标签不同
- **变量类型 6 色 chip**：`string` sky / `number` amber / `boolean` rose / `object` violet / `array` emerald / `any` stone，统一 `rounded px-1 py-px font-mono text-[9px]`，是节点 hue 之外另一套独立的类型编码
- **底层主色复用 waveflow**：画布外的常规 UI（按钮 / 链接 / 选中）仍走 blue-600 暖纸墨蓝，节点 hue 只活在画布内

## 适配指南

- 取某节点配色：`const meta = TYPE_META[node.type]`，拿 `meta.color` / `ring` / `bg` / `cardTint` / `edgeColor` 五槽
- 节点卡：根容器 `cardTint` 整卡染色 + 选中时叠 `ring-2 {meta.ring}`；图标方块单独 `{meta.bg}` 底 + `{meta.color}` 图标
- 连线高亮：选中/hover 节点时取焦点节点类型的 `edgeColor` 写进 `edge.data.highlightColor`，不在 edge 组件里散落硬编码
- 新增节点类型：同时在 catalog（palette 视图：color/bg）和 node-meta（canvas/inspector：5 槽全）补齐，两处对齐避免漂移
- 变量类型 chip：`<VarTypeChip type="string" />`，缺省落 `any`

## 反模式

- ❌ 连线用 700 阶——细线上偏暗发闷，必须 500
- ❌ 把 cardTint 做成左侧色条/色边——破坏整卡一体，回到被否的拼接缝方案
- ❌ 图标前景用 500/600——白底上要么太浅要么太冲，固定 700（特例 800）
- ❌ 节点 hue 外溢到画布外的常规 UI——画布外只走 blue 主色
- ❌ 新增节点只在 catalog 补不补 node-meta——两处漂移
