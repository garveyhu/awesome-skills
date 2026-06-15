---
id: components/feedback/chameleon/radix-overlay-primitives
type: component
name: Radix 浮层四件套
description: Dialog（居中卡片）/ Popover（w-72）/ DropdownMenu（全套菜单）/ Tooltip（暗底）—— paper 底 + shadow-pop 统一壳
platforms:
- web
theme: light
tags:
  aesthetic:
  - minimal
  mood:
  - calm
  stack:
  - shadcn-radix
uses:
- tokens/shadow/waveflow/soft-card-pop-trio
preview: /preview/components/feedback/chameleon/radix-overlay-primitives
---

# Chameleon Radix 浮层四件套

> 全站浮层的基础原语，都基于 Radix + 统一 `bg-[var(--color-paper)]` + `shadow-pop`。`Dialog`（居中卡片，max-w-lg + p-6 + 右上 X）/ `Popover`（w-72 浮层壳，datetime/multi-select 用）/ `DropdownMenu`（Content/Item/Label/Sub/Separator 全套，hover stone-100）/ `Tooltip`（stone-900 暗底白字 11px + 便利包装组件）。`shadow-pop = 0 8px 24px rgb(0 0 0/8%), 0 2px 8px rgb(0 0 0/4%)`。

## 视觉特征

### Dialog（居中卡片）

- **Overlay**：`fixed inset-0 z-50 bg-stone-950/20 data-[state=open]:animate-in data-[state=closed]:animate-out`
- **Content**：`fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg(512px) translate-x-[-50%] translate-y-[-50%] gap-4(16px) bg-[var(--color-paper)](#fffefb) p-6(24px) shadow-pop rounded-lg(8px) border border-stone-200`
- **Close**：`absolute right-4(16px) top-4 rounded-sm opacity-70 hover:opacity-100` 内 `<X className="h-4 w-4"/>`
- **Header** `flex flex-col space-y-1.5(6px) text-left`；**Footer** `flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2(8px)`
- **Title** `text-lg(18px) font-semibold leading-none tracking-tight`；**Description** `text-sm(14px) text-stone-500`

### Popover（w-72 浮层壳）

- **Content**：`shadow-pop z-50 w-72(288px) rounded-lg(8px) border border-stone-200 bg-[var(--color-paper)] p-3(12px) text-stone-900 outline-none`
- 默认 `align="center"` `sideOffset={6}`

### DropdownMenu（菜单全套）

- **Content / SubContent**：`z-50 min-w-[8rem](128px) overflow-hidden rounded-md(6px) border border-stone-200 bg-[var(--color-paper)] p-1(4px) text-stone-900 shadow-pop`，默认 `sideOffset={4}`
- **Item / SubTrigger**：`relative flex cursor-pointer select-none items-center rounded-sm px-2(8px) py-1.5(6px) text-sm(14px) outline-none transition-colors hover:bg-stone-100 focus:bg-stone-100 data-[disabled]:opacity-50`，`inset` 时 `pl-8(32px)`，SubTrigger 加 `data-[state=open]:bg-stone-100`
- **Label**：`px-2 py-1.5 text-xs(12px) font-semibold text-stone-500`
- **Separator**：`-mx-1 my-1 h-px bg-stone-200`

### Tooltip（暗底浮层）

- **Content**：`z-50 overflow-hidden rounded-md(6px) bg-stone-900(#1c1917) px-2(8px) py-1(4px) text-[11px] font-medium leading-tight text-stone-50 shadow-md data-[state=delayed-open]:animate-in data-[state=closed]:animate-out`，默认 `sideOffset={6}`
- **便利包装** `<Tooltip content side='top' align='center' delayDuration={250} disabled>`：`disabled || !content` 时直透 children

## 核心代码

```tsx
// Dialog
<DialogContent className="... w-full max-w-lg gap-4 bg-[var(--color-paper)] p-6 shadow-pop rounded-lg border border-stone-200" />

// Popover
<PopoverContent className="shadow-pop z-50 w-72 rounded-lg border border-stone-200 bg-[var(--color-paper)] p-3" />

// DropdownMenu Item
<DropdownMenuItem className="relative flex cursor-pointer items-center rounded-sm px-2 py-1.5 text-sm hover:bg-stone-100 focus:bg-stone-100" />

// Tooltip 便利包装：disabled 直透
export const Tooltip = ({ content, children, side='top', delayDuration=250, disabled }) => {
  if (disabled || !content) return children;
  return <TooltipRoot delayDuration={delayDuration}>
    <TooltipTrigger asChild>{children}</TooltipTrigger>
    <TooltipPortal><TooltipContent side={side}>{content}</TooltipContent></TooltipPortal>
  </TooltipRoot>;
};
```

## 适配指南

- 短交互（确认 / 简单表单）用 `Dialog`；复杂分档表单用 `Modal`（见 modal-sheet-confirm）
- 行内浮层（日期 / 多选 / 颜色）用 `Popover`，宽度可 `className="!w-[280px]"` 覆盖默认 w-72
- 行操作菜单用 `DropdownMenu`，分组用 `Label` + `Separator`
- icon-only 按钮必套 `Tooltip` 给 label；`disabled` prop 让条件 tooltip 不破坏 DOM 结构

## 反模式

- ❌ Tooltip 用浅底——这里刻意 stone-900 暗底，浅色背景上不够对比
- ❌ Popover/Dropdown 自写阴影——统一 `shadow-pop`，别散落自定义 box-shadow
- ❌ DropdownMenu Item hover 用蓝底——统一 `hover:bg-stone-100` 中性灰，蓝色留给选中态
- ❌ Tooltip content 为空仍渲染 TooltipRoot——用 `disabled || !content` 直透，省去空浮层
