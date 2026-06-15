---
id: blocks/display/chameleon/app-card-gallery-grid
type: block
name: 应用卡片画廊网格（Dify 风）
description: responsive 卡片网格——图标块(hover 旋转放大) + 名称 + key(mono) + 描述 + 类型徽标 + 状态 + 更新时间 + hover 顶部渐变高光线 + 悬浮三点菜单 + 虚线「新建」卡；agents/kbs 共用
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
- blocks/feedback/waveflow/action-dropdown-more
- tokens/palettes/waveflow/warm-paper-ink-blue
preview: /preview/blocks/display/chameleon/app-card-gallery-grid
---

# Chameleon App Card Gallery Grid · 应用卡片画廊网格

> Dify 风 responsive 卡片网格：`grid-cols-1 sm:2 lg:3 xl:4 gap-3`。每张卡含**图标块（hover -rotate-6 + scale-105）+ 名称 + key（mono）+ 两行描述 + 类型徽标 + 状态（已发布/草稿/已嵌入）+ 更新时间**，hover 时顶部浮现一道**渐变高光线**、右上角浮现三点菜单。起手一张虚线「新建」卡。agents（应用）/ kbs（知识库）共用同一卡族（高度 148 / 132）。waveflow 是表格 shell，这套网格全新。

源码：`system/agents/components/app-card.tsx` · `agents/pages/agents-page.tsx:259-290` · `kbs/pages/kbs-page.tsx:83-130`。

## 视觉特征

### 网格

- `grid grid-cols-1 gap-3(12) sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4`

### 卡片

- `group relative flex h-[148px](kb 132px) cursor-pointer flex-col rounded-xl(12) border border-stone-200/80 bg-white p-4(16) shadow-sm`
- 过渡 `transition-[box-shadow,border-color] duration-300`，hover `border-primary-200(#bfdbfe) shadow-md`
- **hover 顶部高光线**：`pointer-events-none absolute inset-x-4 top-0 h-0.5(2) rounded-full bg-gradient-to-r from-transparent via-primary-500(#3b82f6) to-transparent opacity-0 group-hover:opacity-100 duration-300`
- **图标块** `h-9 w-9(36) shrink-0 overflow-hidden rounded-lg(8) transition-transform duration-300 group-hover:-rotate-6 group-hover:scale-105`，按 kind 着色 tile（无自定义图标时）
  - code `bg-indigo-50 text-indigo-600`（icon `Code2`）
  - chatflow `bg-sky-50 text-sky-600`（`MessageSquare`）
  - workflow `bg-violet-50 text-violet-600`（`Workflow`）
  - external `bg-amber-50 text-amber-600`（`Globe`）
  - icon `h-5 w-5 strokeWidth={1.75}`；有自定义图标则 `bg-stone-100` + img `object-cover`
- **名称** `truncate text-[13.5px] font-medium text-stone-900` + **key** `truncate font-mono text-[10.5px] text-stone-400`，文字区 `pr-7` 让位三点
- **描述** `mt-2 line-clamp-2 flex-1 text-[11.5px] leading-relaxed text-stone-500`「暂无描述」兜底

### 底部一行徽标 + 时间

- `mt-auto flex items-center gap-2`，徽标组 `flex min-w-0 flex-wrap items-center gap-1.5`
- 类型徽标 `inline-flex shrink-0 rounded px-1.5 py-0.5 text-[10px] font-medium`（kind 配色）
  - code `bg-indigo-50 text-indigo-700` / chatflow `bg-sky-50 text-sky-700` / workflow `bg-violet-50 text-violet-700` / external `bg-amber-50 text-amber-700`
- 已发布 `bg-emerald-50 text-emerald-700`「已发布 v{n}」/ 草稿 `bg-stone-100 text-stone-500`「草稿」
- 已嵌入 `bg-blue-50 text-blue-700`「已嵌入」
- 更新时间 `ml-auto shrink-0 truncate text-[11px] text-stone-400`「更新于 …」

### 三点菜单（悬浮）

- `absolute right-2 top-2 opacity-0 group-hover:opacity-100`，触发 `h-7 w-7 rounded-md text-stone-400 hover:bg-stone-100 hover:text-stone-700`，icon `MoreVertical h-4 w-4`
- `DropdownMenuContent align=end sideOffset=6 w-36 rounded-xl border-stone-200/70 p-1 shadow-lg`
- 菜单项 `gap-2 rounded-lg px-2.5 py-1.5 text-[12.5px] text-stone-700`，icon `h-3.5 w-3.5 text-stone-400`；删除项 `text-rose-600 focus:bg-rose-50 focus:text-rose-700`

### 新建卡（虚线）

- `group flex h-[148px] flex-col items-center justify-center gap-2 rounded-xl border border-dashed border-stone-300 bg-white/60 text-stone-500`
- hover `border-blue-400 bg-blue-50/40 text-blue-600`
- 内圆 `h-9 w-9 rounded-full bg-stone-100 group-hover:bg-blue-100`，`Plus h-5 w-5 strokeWidth={1.75}`，标题 `text-[13px] font-medium`，副 `text-[11px] text-stone-400`

### 骨架

- `.skeleton h-[148px] rounded-xl opacity-60`（4 个占位）

## 核心代码

```tsx
// hover 顶部渐变高光线（signature）
<span aria-hidden className="pointer-events-none absolute inset-x-4 top-0 h-0.5 rounded-full bg-gradient-to-r from-transparent via-primary-500 to-transparent opacity-0 transition-opacity duration-300 group-hover:opacity-100" />

// 图标块 hover 旋转放大
<div className={`flex h-9 w-9 shrink-0 items-center justify-center overflow-hidden rounded-lg transition-transform duration-300 group-hover:-rotate-6 group-hover:scale-105 ${card.icon ? 'bg-stone-100' : meta.tile}`}>
  {card.icon ? <img src={card.icon} className="h-full w-full object-cover" /> : <Icon className="h-5 w-5" strokeWidth={1.75} />}
</div>
```

```tsx
// kind 配色映射
const KIND_META = {
  code:     { Icon: Code2,         badge: 'bg-indigo-50 text-indigo-700', tile: 'bg-indigo-50 text-indigo-600' },
  chatflow: { Icon: MessageSquare, badge: 'bg-sky-50 text-sky-700',       tile: 'bg-sky-50 text-sky-600' },
  workflow: { Icon: Workflow,      badge: 'bg-violet-50 text-violet-700', tile: 'bg-violet-50 text-violet-600' },
  external: { Icon: Globe,         badge: 'bg-amber-50 text-amber-700',   tile: 'bg-amber-50 text-amber-600' },
};
```

## 适配指南

- 卡片纯展示：接 props 出 UI，open/edit/embed/delete 动作由父页面回调注入
- `primary-*` 是 themeable 主题色（默认 blue：primary-200 #bfdbfe / 500 #3b82f6 / 600 #2563eb），hover 高光走 `via-primary-500`
- kind 配色用「浅底深字」对（50/600·50/700），图标块和徽标同色系不同深度
- 新建卡固定第一格虚线引导，骨架同高度占位避免布局抖动
- agents 卡 148 高、kbs 卡 132 高——内容密度不同，结构同款

## 反模式

- ❌ 卡片用纯 #fff 底——破坏暖白基底，应配 `bg-white`(=#fff) 在 `bg-warm` 页面底上自然浮出
- ❌ hover 只换 border 不上高光线——顶部渐变高光线是这套卡的 signature
- ❌ 图标块 hover 无旋转——`-rotate-6 + scale-105` 的微动是「product-shelf inviting」气质来源
- ❌ 类型徽标硬编码单色——必须按 kind 分色（indigo/sky/violet/amber）
- ❌ 三点菜单常显——必须 hover 浮现（opacity-0 group-hover:opacity-100）保持网格干净
