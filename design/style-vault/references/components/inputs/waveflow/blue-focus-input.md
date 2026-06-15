---
id: components/inputs/waveflow/blue-focus-input
type: component
name: 蓝聚焦输入框
description: h-8 默认 input + focus:border-blue-500 + ring-2 ring-blue-100 + error 红 + mono 模式
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm]
  stack: [shadcn-radix]
uses:
  - tokens/palettes/waveflow/warm-paper-ink-blue
preview: /preview/components/inputs/waveflow/blue-focus-input
---

# Waveflow Blue Focus Input

> waveflow 全站标准输入框 (`components/ui/input.tsx`)——h-8 紧凑 + 蓝 focus ring + `mono` prop 切 JetBrains Mono + `error` prop 切红边。是 Dialog 表单和 TableToolbar 搜索的基础原语。

## 视觉特征

- **基础类**：`h-8 w-full rounded-md border border-stone-300 bg-white px-3 text-[13px] outline-none transition placeholder:text-stone-400`
- **focus 态**：`focus:border-blue-500 focus:ring-2 focus:ring-blue-100`
  - 边色从 stone-300 → blue-500
  - 外加 2px blue-100 (#dbeafe) ring
  - 共 4 行 9 处文件复用此组合
- **disabled 态**：`disabled:cursor-not-allowed disabled:bg-stone-100 disabled:text-stone-500`
- **error prop**：`border-red-500 focus:border-red-500 focus:ring-red-100`
- **mono prop**：加 `font-mono tnum` —— 给 cron / 数字 / 路径输入用
- **placeholder**：stone-400 灰
- **TableToolbar 紧凑变体**：覆写 `!h-7 pl-6 text-[12px]`（左 padding 留给 search icon）

## 核心代码

```tsx
export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type = 'text', error, mono, ...props }, ref) => (
    <input
      ref={ref}
      type={type}
      className={cn(
        'h-8 w-full rounded-md border border-stone-300 bg-white px-3 text-[13px] outline-none transition placeholder:text-stone-400',
        'focus:border-blue-500 focus:ring-2 focus:ring-blue-100',
        'disabled:cursor-not-allowed disabled:bg-stone-100 disabled:text-stone-500',
        error && 'border-red-500 focus:border-red-500 focus:ring-red-100',
        mono && 'font-mono tnum',
        className,
      )}
      {...props}
    />
  ),
);
```

## 适配指南

- 一律走 `<Input>`，不要直接写 `<input>`——focus ring 是 waveflow 表单的视觉一致性根
- 错误显示：`<Input error={!!errors.name} />` + 下一行 `<div className="mt-1 text-[11px] text-red-600">{errors.name}</div>`
- 数字/cron 输入：`<Input mono type="number" />` 自动套 mono + tnum
- TableToolbar 搜索：`className="!h-7 pl-6 text-[12px]"` + 绝对定位的 search icon button

## 反模式

- ❌ 用 `outline` border 配色（black/2px）——和 stone-300/1px 不和谐
- ❌ focus 加 box-shadow 而非 ring-2——shadow 会被 transition-colors 跳过
- ❌ disabled 不加 bg-stone-100—— 看起来仍可输入
