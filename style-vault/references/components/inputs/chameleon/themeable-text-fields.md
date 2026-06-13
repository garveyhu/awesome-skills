---
id: components/inputs/chameleon/themeable-text-fields
type: component
name: 紧凑文本域与标签
description: blue-focus-input 的多行兄弟件——min-h-72px textarea + Radix Label（12px medium stone-600 + peer-disabled）
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
- components/inputs/waveflow/blue-focus-input
preview: /preview/components/inputs/chameleon/themeable-text-fields
---

# 紧凑文本域与标签

> blue-focus-input 同款蓝聚焦表单原语的两个补全件：多行 `Textarea`（min-h-72px + 同款蓝 ring）和 Radix `Label`（12px / medium / stone-600 / peer-disabled 态）。配色与 input.tsx 逐字对齐——`focus:border-blue-500 + ring-2 ring-blue-100`，用的是字面 blue-500/blue-100（非 themeable primary）。waveflow 无独立 textarea / label 条目，故 new；其 input 本体直接 cross-namespace 复用 waveflow/blue-focus-input。

## 视觉特征

### Textarea
- `w-full min-h-[72px] rounded-md border border-stone-300 bg-white px-3 py-1.5 text-[13px] outline-none transition placeholder:text-stone-400`
- focus `focus:border-blue-500 focus:ring-2 focus:ring-blue-100`（边 stone-300→blue-500 #3b82f6，外加 2px blue-100 #dbeafe ring）
- disabled `disabled:cursor-not-allowed disabled:bg-stone-100 disabled:text-stone-500`
- 与 input 唯一差异：`min-h-[72px] py-1.5`（多行起始高度），无 `h-8`

### Label（LabelPrimitive.Root）
- `text-[12px] font-medium leading-none text-stone-600 peer-disabled:cursor-not-allowed peer-disabled:opacity-70`
- 比 input 内的 placeholder 略深（stone-600 vs stone-400），是表单字段标签的基线

## 核心代码

```tsx
// Textarea
<textarea
  className={cn(
    'w-full min-h-[72px] rounded-md border border-stone-300 bg-white px-3 py-1.5 text-[13px] outline-none transition placeholder:text-stone-400',
    'focus:border-blue-500 focus:ring-2 focus:ring-blue-100',
    'disabled:cursor-not-allowed disabled:bg-stone-100 disabled:text-stone-500',
    className,
  )}
/>

// Label
<LabelPrimitive.Root
  className={cn('text-[12px] font-medium leading-none text-stone-600 peer-disabled:cursor-not-allowed peer-disabled:opacity-70', className)}
/>
```

## 适配指南
- 多行输入一律走 `<Textarea>`，单行走 `<Input>`（waveflow/blue-focus-input）——两者 focus ring 视觉一致
- 字段标签走 `<Label>`（Radix，支持 `htmlFor` 联动 + peer-disabled），不要散写 `<label className="...">`
- textarea 要更高起始高度时用 `className="min-h-[120px]"` 覆写，不改原 min-h-[72px]

## 反模式
- ❌ textarea 不写 `py-1.5` —— input 是 `h-8` 定高所以无垂直 padding，textarea 必须靠 py 撑出可读上下边距
- ❌ Label 用 stone-700/stone-900 —— 标签是 stone-600（中性、不抢输入内容），ControlField 内的画布字段标签才是 stone-700

## 与 waveflow/blue-focus-input 区分
- **同源**：focus 态、disabled 态、border-stone-300、rounded-md、text-[13px] 与 blue-focus-input **逐字一致**——本条是它的多行 + 标签补全件，不是另一套配色
- **结构差异**：blue-focus-input 是 `h-8` 单行 input（带 `error` / `mono` prop）；本条的 Textarea 是 `min-h-[72px]` 多行（无 error/mono prop，但有 `py-1.5`）
- **Label 不属于 blue-focus-input**：它是 Radix LabelPrimitive 封装，配 input 用，blue-focus-input 条目里没有
- **选择**：单行输入 → 用 waveflow/blue-focus-input；多行 → 用本条 Textarea；字段标签 → 用本条 Label
