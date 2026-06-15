---
id: blocks/canvas/chameleon/graph-node-card
type: block
name: 工作流画布节点卡（整卡微染 + 多出口分支）
description: 画布 signature 视觉单元 - 14px 圆角卡用类型 cardTint 整卡均匀微染（无边界色块、无拼接缝），彩色图标块 + 标题 + 类型副标题色 + 配置摘要灰字；多出口模式（经典 / if_else 真假双 handle / classifier 多分类 / human_input 选项 / fail 红出边 / 悬挂容错）；运行态边框语义染色；精致连接点小圆点
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
- tokens/motion/chameleon/canvas-edge-dash-flow
- tokens/palettes/chameleon/node-type-hue-system
- tokens/shadow/waveflow/soft-card-pop-trio
preview: /preview/blocks/canvas/chameleon/graph-node-card
---

# 工作流画布节点卡（整卡微染 + 多出口分支）

> 工作流画布的 signature 视觉单元。圆角 14px 卡片用类型 `cardTint`（极淡类型色温，如 `bg-violet-50/40`）把整张卡均匀微染 —— 色彩是卡片自身的表面色，不是贴在白卡上的色块，整卡一体、无任何分界线 / 拼接缝。头部彩色图标块 + 标题 + 类型副标题色 + 配置摘要灰字。多出口模式与运行态边框语义染色。

源码：`src/system/graphs/components/nodes/graph-node.tsx`（`GraphNode` / `BranchHandleRow` / `SubflowRefLine`）；hue 数据 `lib/node-meta.ts`（`TYPE_META`）。

## 视觉特征

### 卡片本体

- **容器** `group relative min-w-[180px] rounded-[14px] border px-2.5 pb-2 pt-2 text-[11.5px]` + `meta.cardTint`（整卡微染，如 violet `bg-violet-50/40`）+ `shadow-soft transition-all duration-150`
- **hover**：`-translate-y-px hover:shadow-card`（轻浮起）
- **默认边**：`border-stone-200/70`
- **selected**：`-translate-y-px shadow-card ring-2 ring-offset-2 ring-offset-warm` + `meta.ring`（类型色 ring）
- **运行态边框 STATUS_COLOR**（叠在 cardTint 上）：pending `border-stone-300` / running `border-primary-400 animate-pulse` / success `border-emerald-400` / failed `border-rose-500` / skipped `border-stone-200` / errorHandled `border-amber-400`
- **头部行** `relative z-10 flex items-center gap-2`：
  - 图标块 `h-[26px] w-[26px] rounded-[9px] ring-1 ring-inset ring-stone-900/5` + `meta.bg`，图标 `h-3.5 w-3.5` + `meta.color` `strokeWidth 2`
  - 标题 `truncate text-[12.5px] font-semibold tracking-tight text-stone-800`
  - 类型副标题 `text-[9.5px] font-medium uppercase tracking-wide leading-tight` + `meta.color`
- **摘要行** `mt-1 truncate text-[10px] leading-tight text-stone-400`
- **subflow ref 行**：`mt-1 truncate font-mono text-[10px] text-indigo-600`「↳ 图名 · v0」
- **running 附注** `mt-1 text-[10px] text-blue-600`「⟳ …」；**error** `mt-1 text-[10px] text-rose-600`「✗ …」

### 类型 hue 系统（TYPE_META 摘录）

| 类型 | bg | color | edge(500) |
|------|----|-------|-----------|
| llm 大模型 | violet-50 | violet-700 | #8b5cf6 |
| kb 知识库 | emerald-50 | emerald-700 | #10b981 |
| if_else 条件分支 | amber-50 | amber-700 | #f59e0b |
| classifier 意图分类 | lime-50 | lime-700 | #84cc16 |
| http HTTP请求 | cyan-50 | cyan-700 | #06b6d4 |
| code 代码 | slate-50 | slate-700 | #64748b |
| start 开始 | emerald-50 | emerald-700 | #10b981 |
| end 结束 | stone-50 | stone-700 | #78716c |

cardTint = 对应 hue `50/40`（极淡）；ring = `200`；图标块 bg = `50`。

### 多出口模式

- **经典单出口**：右侧一个 source handle
- **if_else 真假双 handle**：true `top 35% border-emerald-400` / false `top 70% border-rose-400`，右侧 `text-[9px]`「真 →」(emerald-600) /「假 →」(rose-500)
- **classifier 多出口**：每分类一行 `BranchHandleRow` tone=branch（lime）
- **human_input 选项**：每选项一行 tone=branch
- **多 CASE if_else**：IF/ELIF 行 tone=case（amber）+ ELSE 行 tone=else（stone）
- **fail 出边**：成功 + 失败双 handle，失败 `border-rose-400` + 「失败」/「失败 →」rose
- **悬挂容错**：tone=dangling（amber）「… · 悬挂」

### 连接点小圆点（HANDLE）

- **HANDLE_BASE**：`!h-2.5 !w-2.5`（10px）`!rounded-full !border-[1.5px] !bg-white !shadow-sm transition-all duration-150 hover:!h-3.5 hover:!w-3.5`（hover 放大到 14px）
- **target 入口**：`!border-stone-300 hover:!border-primary-400`
- **source 出口**：`!border-primary-300 hover:!border-primary-500`
- **行内出口** handle：`style top:50% right:-15`
- **tone 边色**：branch `!border-lime-500` / case `!border-amber-400` / else `!border-stone-400` / fail `!border-rose-400` / dangling `!border-amber-400`，对应文字 `font-mono text-[9px]`
- `!` 前缀覆盖 React Flow 内联样式

### 行内出口标签行（BranchHandleRow）

- `relative flex items-center justify-end text-[9px]` + tone 文字色，标签 `max-w-[160px] truncate font-mono`「label →」

## 核心代码

```tsx
// 整卡微染 + 状态边框叠加（核心：cardTint 是卡片表面色，不是色块）
className={cn(
  'group relative min-w-[180px] rounded-[14px] border px-2.5 pb-2 pt-2 text-[11.5px]',
  meta.cardTint,            // bg-violet-50/40 等
  'shadow-soft transition-all duration-150 hover:-translate-y-px hover:shadow-card',
  statusCls || 'border-stone-200/70',
  isSelected && cn('-translate-y-px shadow-card ring-2 ring-offset-2 ring-offset-warm', meta.ring),
)}

// 精致 handle：默认 10px 白底细边，hover 放大 14px 高亮
const HANDLE_BASE = '!h-2.5 !w-2.5 !rounded-full !border-[1.5px] !bg-white !shadow-sm transition-all duration-150 hover:!h-3.5 hover:!w-3.5';
```

## 适配指南

- 任何节点图 / 卡片需要「类型色彩锚点但不显廉价」就用整卡微染（hue 50/40）而非左色条 / 左色块 —— 消除拼接缝
- 类型信号靠三件套承载：彩色图标块（bg 50）+ 类型副标题色（700）+ 极淡卡底（50/40）
- 运行态用边框语义染色（running pulse / success 绿 / failed 红 / errorHandled 橙），叠在静态卡底上
- 出口 handle 按语义 tone 上色（true 绿 / false 红 / 分类 lime / case 琥珀 / fail 红）
- handle 默认克制（10px 白底细灰边），hover 才放大高亮 —— 不抢卡片视觉

## 反模式

- ❌ 用左色条 / 左色边块 —— 产生「白卡旁一块彩色」的可见边界、隔阂感（整卡微染替代）
- ❌ 卡底用饱和色 —— 是极淡 `50/40` 色温，不是实色块
- ❌ handle 默认就大就彩 —— 默认 10px 白底细灰，hover 才放大高亮
- ❌ 多出口不分语义色 —— true/false/分类/case/fail 各有 tone
- ❌ 状态边框换整卡背景 —— 只改 border 颜色，卡底保持类型微染
