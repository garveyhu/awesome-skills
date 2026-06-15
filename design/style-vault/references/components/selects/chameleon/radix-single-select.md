---
id: components/selects/chameleon/radix-single-select
type: component
name: Radix 单选下拉
description: Radix Select 单选原语封装——Trigger 复用蓝聚焦输入态 + Item pl-8 左对勾 + ChevronDown 触发图标 + shadow-pop 浮层
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
preview: /preview/components/selects/chameleon/radix-single-select
---

# Radix 单选下拉

> Chameleon 的 Radix Select 单选原语封装（Trigger / Content / Item + Check 指示器）。Trigger 与 blue-focus-input 同款蓝聚焦输入态（h-8 + focus:border-blue-500 + ring-2 ring-blue-100），末尾 `ChevronDown opacity-50`；下拉浮层走 `shadow-pop`，Item `pl-8` 左侧绝对定位 `Check` 对勾。waveflow 只有 multi-select-popover 通用多选，无单选 Select 原语，故 new。

## 视觉特征

### SelectTrigger
- `flex h-8 w-full items-center justify-between rounded-md border border-stone-300 bg-white px-3 text-[13px] outline-none transition placeholder:text-stone-400`
- focus `focus:border-blue-500 focus:ring-2 focus:ring-blue-100`（同 blue-focus-input）
- disabled `disabled:cursor-not-allowed disabled:bg-stone-100 disabled:text-stone-500`
- 末尾 `<ChevronDown className="h-4 w-4 opacity-50" />`

### SelectContent
- `relative z-50 max-h-96 min-w-[8rem] overflow-hidden rounded-md border border-stone-200 bg-[var(--color-paper)] text-stone-900 shadow-pop`（shadow-pop = `0 8px 24px rgb(0 0 0/0.08), 0 2px 8px rgb(0 0 0/0.04)`）
- popper 模式 `translate-y-1`，Viewport `p-1`

### SelectItem
- `relative flex w-full cursor-pointer select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-[13px] outline-none`
- `hover:bg-stone-100 focus:bg-stone-100 data-[disabled]:pointer-events-none data-[disabled]:opacity-50`
- 左侧 `absolute left-2 flex h-3.5 w-3.5 items-center justify-center` 内 `ItemIndicator` → `Check h-4 w-4`（pl-8 为对勾留位）

## 核心代码

```tsx
<SelectTrigger className="...h-8...focus:border-blue-500 focus:ring-2 focus:ring-blue-100">
  {children}
  <SelectPrimitive.Icon asChild><ChevronDown className="h-4 w-4 opacity-50" /></SelectPrimitive.Icon>
</SelectTrigger>

<SelectContent className="...rounded-md border border-stone-200 bg-[var(--color-paper)] shadow-pop translate-y-1">
  <SelectPrimitive.Viewport className="p-1">{children}</SelectPrimitive.Viewport>
</SelectContent>

<SelectItem className="relative flex w-full cursor-pointer items-center rounded-sm py-1.5 pl-8 pr-2 text-[13px] hover:bg-stone-100 focus:bg-stone-100">
  <span className="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
    <SelectPrimitive.ItemIndicator><Check className="h-4 w-4" /></SelectPrimitive.ItemIndicator>
  </span>
  <SelectPrimitive.ItemText>{children}</SelectPrimitive.ItemText>
</SelectItem>
```

## 适配指南
- 普通单选枚举（kind / status / 语言…）一律走它，与 Input/Textarea 视觉一致（同 h-8 + 蓝 ring）
- 紧凑场景（画布节点 / 创建表单）覆写 Trigger `h-7 text-[12px]`（见 ImageModelSelect）
- Item 内可塞 mono code + 灰 provider 副标（自由组合子节点），pl-8 已为对勾留位
- 浮层背景走 `var(--color-paper)` 主题变量，不硬编码白

## 反模式
- ❌ Trigger 用 stone-400 边 / 2px black —— 与 stone-300/1px + 蓝 ring 体系不一致
- ❌ Item 对勾放右侧 —— Radix Select 惯例是左侧 pl-8 对勾（选中项左缘对齐），右侧留给附标
- ❌ Content 用 shadow-card / shadow-soft —— 浮层用 shadow-pop（更强的悬浮层次），card/soft 是贴地卡片
- ❌ Item 不写 `cursor-pointer` —— Radix 默认无指针，要显式加
