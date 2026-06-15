---
id: blocks/canvas/chameleon/node-palette
type: block
name: 左侧常驻节点面板（双列 + 顶部 Tab）
description: 对齐 Dify block-selector / FastGPT NodeTemplates 的左侧常驻节点面板 - 顶部 4 大类 Tab（全部/生成/逻辑/数据）+ 搜索 + 最近使用置顶 + 双列网格节点卡（图标块 group-hover 放大）；展开常驻 / 收起只留「+」小按钮带滑入动画
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
preview: /preview/blocks/canvas/chameleon/node-palette
---

# 左侧常驻节点面板（双列 + 顶部 Tab）

> 工作流编辑器左上常驻的节点面板。顶部 4 大类 Tab（全部 / 生成 / 逻辑 / 数据）+ 搜索 + 最近使用置顶 + 双列网格节点卡（图标块 group-hover 放大）。展开常驻 / 收起只留「+」小按钮（带滑入动画）。拖拽 + 点击放置双保留。

源码：`src/system/graphs/components/node-palette.tsx`（`NodePalette`）；节点目录 `lib/node-catalog.ts`。

## 视觉特征

- **面板**：`absolute top-3 left-3 z-20 w-[21rem]`（336px）`max-h-[calc(100%-1.5rem)] flex flex-col overflow-hidden rounded-2xl border border-stone-200/80 bg-white shadow-xl ring-1 ring-stone-900/5`
- **入场**：`animate-in fade-in slide-in-from-left-2 duration-200`（从左 8px 滑入）
- **Tab 行** `flex items-center gap-1 px-2 pt-2`：
  - Tab 按钮 `flex items-center gap-1 rounded-lg px-2 py-1.5 text-[11.5px] font-medium`，active `bg-blue-50 text-blue-600`，非 `text-stone-500 hover:bg-stone-100 hover:text-stone-700`，icon `h-3.5`（`LayoutGrid` 全部 / `Sparkles` 生成 / `GitBranch` 逻辑 / `Boxes` 数据）
  - 收起钮 `h-6 w-6 rounded-md text-stone-400 hover:bg-stone-100` + `ChevronsLeft h-3.5`
- **搜索** `px-2.5 pt-2 pb-2`：`h-8 rounded-lg border border-stone-200 bg-stone-50 pl-8 pr-7 text-[12px] focus:border-blue-300 focus:bg-white focus:ring-1 focus:ring-blue-200` + `Search h-3.5 text-stone-400`（左），清除 `X h-3.5`（右，有值时）
- **分组** `mb-3`：标题 `px-1.5 pb-1.5 text-[10px] font-semibold tracking-wide text-stone-400`，网格 `grid grid-cols-2 gap-1`
- **节点卡**：`group flex items-center gap-2 rounded-xl border border-transparent px-2 py-2 text-left hover:border-stone-200 hover:bg-stone-50 hover:shadow-sm active:bg-stone-100`
  - 图标块 `h-7 w-7 rounded-lg ring-1 ring-stone-900/5 group-hover:scale-105` + `it.bg`，图标 `h-4 w-4` + `it.color`
  - 名 `truncate text-[12px] font-medium text-stone-700`
- **收起态「+」按钮**：`absolute top-3 left-3 z-20 h-8 w-8 rounded-lg border border-stone-200/70 bg-white/95 text-stone-500 shadow-md backdrop-blur hover:bg-blue-50 hover:text-blue-600` + `Plus h-4`
- **分组顺序**：生成 / 检索 & 工具 / 逻辑 / 编排 / 变量 & 输出
- **空态**：`Search h-5 text-stone-300` + `text-[11.5px] text-stone-400`

## 核心代码

```tsx
// Tab 按钮 active 态
className={cn('flex items-center gap-1 rounded-lg px-2 py-1.5 text-[11.5px] font-medium',
  isActive ? 'bg-blue-50 text-blue-600' : 'text-stone-500 hover:bg-stone-100 hover:text-stone-700')}

// 双列网格节点卡 + 图标块 group-hover 放大
<div className="grid grid-cols-2 gap-1">
  <button className="group flex items-center gap-2 rounded-xl border border-transparent px-2 py-2 hover:border-stone-200 hover:bg-stone-50 hover:shadow-sm">
    <span className={cn('flex h-7 w-7 rounded-lg ring-1 ring-stone-900/5 group-hover:scale-105', it.bg)}>
      <it.icon className={cn('h-4 w-4', it.color)} />
    </span>
    <span className="truncate text-[12px] font-medium text-stone-700">{it.label}</span>
  </button>
</div>
```

## 适配指南

- 任何「画布 + 可添加元素」场景套用（Dify block-selector / FastGPT 套路）
- 顶部 Tab 把细分组归并成可扫读的大类（4 个），细分组在每 Tab 内仍按 group 标题列
- 「最近使用」只在「全部」Tab、无搜索时置顶 —— 避免细 Tab 里出现跨类条目
- 节点卡图标块 group-hover 微放大（scale-105）是低调的「可点」反馈
- 展开常驻 / 收起只留「+」小钮，状态落 localStorage；拖拽 + 点击放置双保留

## 反模式

- ❌ 单列长列表 —— 双列网格更省空间、可扫读
- ❌ 节点卡 hover 大动效 —— 图标块仅微放大（scale-105）
- ❌ Tab 用按钮组实心填充 —— active 用浅 `bg-blue-50 text-blue-600`，克制
- ❌ 收起后完全消失无入口 —— 留 `h-8 w-8` 的「+」小钮带滑入动画
- ❌ 搜索框用大圆角白底 —— 是 `h-8 rounded-lg bg-stone-50`，focus 才转白 + 蓝环
