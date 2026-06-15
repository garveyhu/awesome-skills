---
id: components/buttons/waveflow/cva-engineer-button
type: component
name: CVA 工程师按钮
description: 7 variant × 5 size CVA 按钮 (primary/outline/ghost/link/danger/danger-outline/dark) + loading 自动 Loader2 + Slot 多态
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, industrial]
  mood: [serious, confident]
  stack: [shadcn-radix]
uses:
  - tokens/palettes/waveflow/warm-paper-ink-blue
preview: /preview/components/buttons/waveflow/cva-engineer-button
---

# Waveflow CVA Engineer Button

> waveflow 全站按钮——用 CVA 实现 7 variant × 5 size，比 shadcn 默认 button **更紧凑**（最大 lg=h-9 而非 h-10）、**更暗**（primary 走 blue-600 而非 blue-500）、**带 dark variant**（专给登录 CTA 用）。`loading=true` 自动前置 `Loader2` 旋转图标，Radix `Slot` 支持 polymorphic (asChild)。

## 视觉特征

- **基础类**：`inline-flex shrink-0 items-center justify-center gap-1.5 whitespace-nowrap rounded-md font-medium transition-colors disabled:pointer-events-none disabled:opacity-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-200`
- **7 variant**：
  - `primary`: `bg-blue-600 text-white hover:bg-blue-700 active:bg-blue-800` (全站主 CTA)
  - `outline`（**默认**）: `border border-stone-300 bg-white text-stone-700 hover:bg-stone-50 active:bg-stone-100`
  - `ghost`: `text-stone-700 hover:bg-stone-100 active:bg-stone-200`
  - `link`: `text-blue-600 hover:underline underline-offset-2`
  - `danger`: `bg-red-600 text-white hover:bg-red-700 active:bg-red-800`
  - `danger-outline`: `border border-red-300 text-red-600 hover:bg-red-50 active:bg-red-100`
  - `dark`: `bg-stone-900 text-white hover:bg-stone-800 active:bg-stone-700` (登录 CTA 专属)
- **5 size**：
  - `sm`: `h-7 px-2.5 text-[11.5px]` (table action / TableToolbar)
  - `md`（**默认**）: `h-8 px-3 text-[12.5px]` (Dialog footer / 一般行动)
  - `lg`: `h-9 px-4 text-[14px]` (主要 CTA)
  - `icon`: `h-8 w-8 p-0`
  - `icon-sm`: `h-7 w-7 p-0`
- **loading 自动注入**：`{loading ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : null}{children}` —— 加 disabled
- **gap-1.5 + h-3.5 icon**：icon 与文字间距 6px，icon 14px——比文字略小一档，不抢戏
- **focus-visible-only ring**：键盘 tab 才有 ring，鼠标点不显——避免点击后残留 ring

## 核心代码

```tsx
const buttonVariants = cva(
  'inline-flex shrink-0 items-center justify-center gap-1.5 whitespace-nowrap rounded-md font-medium transition-colors disabled:pointer-events-none disabled:opacity-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-200',
  {
    variants: {
      variant: { primary, outline, ghost, link, danger, 'danger-outline', dark },
      size:    { sm, md, lg, icon, 'icon-sm' },
    },
    defaultVariants: { variant: 'outline', size: 'md' },
  },
);

<Button variant="primary" size="sm" onClick={...} loading={loading}>
  <Plus className="h-3.5 w-3.5" /> 添加任务
</Button>
```

## 适配指南

- 表格行内 action 用 `<button className="rounded p-1 hover:bg-stone-200 hover:text-stone-900">`，**不**用 Button 组件（避免 h-7 太占空间）—— 单独抽到 `icon-ghost-square` 模式
- danger 操作用 `danger`（实心红）做最终确认 CTA；用 `danger-outline` 做未确认的"打开删除菜单"按钮
- 登录页 CTA 用 `dark`（stone-900），不要用 primary 蓝——蓝色在彩色背景上不够强势
- icon-only 按钮必须套 `<Tooltip>` 给 label

## 反模式

- ❌ 用 `secondary` variant —— waveflow 没这个 variant，用 `outline` 或 `ghost` 代替
- ❌ lg size 用在 dialog footer——h-9 太大顶到 footer 边
- ❌ `dark` variant 用在 admin 主体——只属于登录页
- ❌ loading 时不 disabled——多次点击重发请求
