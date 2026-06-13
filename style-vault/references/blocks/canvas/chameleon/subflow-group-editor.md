---
id: blocks/canvas/chameleon/subflow-group-editor
type: block
name: 子图编辑入口（摘要按钮 + 全屏子图 modal）
description: iteration.body / parallel.branches 的可视化子图编辑入口 - 摘要按钮（N 节点·N 边 + Network 图标 + 编辑笔）打开全屏子图 modal（独立 SubgraphCanvas，与主画布视觉一致但本地选中 + 私有剪贴板隔离）；parallel 分支列表增删改 key
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
- blocks/canvas/chameleon/bezier-edge-add
- blocks/canvas/chameleon/config-panel-inspector
- blocks/canvas/chameleon/graph-node-card
- blocks/canvas/chameleon/node-palette
preview: /preview/blocks/canvas/chameleon/subflow-group-editor
---

# 子图编辑入口（摘要按钮 + 全屏子图 modal）

> iteration.body / parallel.branches 的可视化编辑入口（替代裸 JSON）。摘要按钮显示「N 节点 · N 边」+ Network 图标 + 编辑笔，点开全屏子图 modal（独立 SubgraphCanvas，与主画布视觉一致，但本地选中 + 私有剪贴板隔离）。parallel 分支列表可增删改 key。

源码：`subgraph-fields.tsx`（`SubgraphField` / `ParallelBranchesField`）+ `subgraph-editor-modal.tsx` + `subgraph-canvas.tsx`。

## 视觉特征

### SubgraphField 摘要按钮（iteration.body）

- 标签 `mb-1 block text-[11px] text-stone-600`
- 按钮 `flex w-full items-center gap-2 rounded-md border border-slate-200 bg-white px-2 py-2 text-left text-[11.5px] hover:border-blue-200 hover:bg-blue-50`
  - `Network h-3.5 text-sky-600`（`#0284c7`）
  - 「子图」`flex-1 text-stone-700`
  - 摘要 `font-mono text-[10.5px] text-stone-400`（「N 节点 · N 边」）
  - `Pencil h-3 text-stone-400`
- hint：`mt-1 text-[10.5px] leading-relaxed text-stone-400`

### ParallelBranchesField 分支列表

- 标签「分支（2–20 条，同一 input fork 后并发跑）」
- 分支行 `flex items-center gap-1.5 rounded-md border border-slate-200 bg-white px-1.5 py-1.5`：
  - key Input `h-8 w-24 font-mono text-[11.5px]`
  - 摘要 `flex-1 truncate font-mono text-[10.5px] text-stone-400`
  - 编辑钮 `Pencil h-3.5`（hover `bg-stone-100`）+ 删除钮 `Trash2 h-3.5`（hover `bg-rose-50 text-rose-600`）
- 空态 `rounded-md border border-dashed border-slate-200 px-2 py-3 text-center text-[11px] text-stone-400`
- 添加 outline Button（`mt-1.5 w-full`）+ `Plus h-3`「添加分支」

### 全屏子图 modal（SubgraphEditorModal）

- ModalContent `h-[88vh] w-[min(1180px,94vw)] bg-slate-50`（冷白外壳对齐主画布），`closeOnBackdrop=false`
- ModalHeader 标题 + 内含 SubgraphCanvas（占 `min-h-0 flex-1`）+ ModalFooter（取消 ghost / 应用 primary）

### SubgraphCanvas（modal 内画布）

- 背景 `BackgroundVariant.Dots` gap 16 size 1 color `var(--color-slate-200)`（冷白点阵，对齐主画布）
- `Controls showInteractive={false}` + `MiniMap pannable zoomable className="!bg-slate-100"`
- 自动整理 Panel（top-right）：`flex items-center gap-1 rounded-lg border border-stone-200/70 bg-white/90 px-2 py-1 text-[11.5px] text-stone-600 shadow-md backdrop-blur hover:bg-stone-50` + `LayoutGrid h-3.5`「自动整理」
- defaultEdgeOptions：`type 'graphEdge'`、markerEnd ArrowClosed 14×14 `#d6d3d1`、connectionLineComponent GraphConnectionLine（贝塞尔，对齐主画布）
- 含 NodePalette + NodeInspector + 三态右键菜单（与主画布同款，但私有剪贴板隔离）

## 核心代码

```tsx
// 摘要按钮（iteration.body）
<button className="flex w-full items-center gap-2 rounded-md border border-slate-200 bg-white px-2 py-2 text-[11.5px] hover:border-blue-200 hover:bg-blue-50">
  <Network className="h-3.5 w-3.5 text-sky-600" />
  <span className="flex-1 text-stone-700">子图</span>
  <span className="font-mono text-[10.5px] text-stone-400">{spec.nodes.length} 节点 · {spec.edges.length} 边</span>
  <Pencil className="h-3 w-3 text-stone-400" />
</button>

// 全屏 modal
<ModalContent className="h-[88vh] w-[min(1180px,94vw)] bg-slate-50" closeOnBackdrop={false}>
```

## 适配指南

- 任何「字段里嵌套一张可视化子图 / 子流程」场景套用（Dify iteration / parallel 套路）
- 摘要按钮用「N 节点 · N 边」font-mono 摘要给用户一眼看到子图规模，不必打开
- 全屏 modal 画布外壳用冷白 `bg-slate-50` 对齐主画布，复用同款 palette / inspector / 节点卡 / 贝塞尔连线
- 子图编辑器与主画布选中 + 剪贴板隔离（本地态），避免互相串
- parallel 分支 key 用 font-mono Input，编辑 + 删除各一个图标钮

## 反模式

- ❌ 子图配置裸 JSON 编辑 —— 提供可视化子图画布 modal
- ❌ modal 外壳用暖白 paper —— 用冷白 slate-50 对齐主画布
- ❌ 子图画布另起一套视觉 —— 复用主画布的 palette / inspector / 节点卡 / 连线，保持一致
- ❌ 摘要按钮不显规模 —— 「N 节点 · N 边」是关键扫读信息
