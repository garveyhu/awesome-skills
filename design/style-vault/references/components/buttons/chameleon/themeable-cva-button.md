---
id: components/buttons/chameleon/themeable-cva-button
type: component
name: 可切主色 CVA 按钮（9 variant × 6 size）
description: CVA 按钮 - 9 variant × 6 size，primary 走可切换的 --color-primary-*(8 套主题色)而非硬编码 blue；新增 secondary + default 别名 + loading 自动 Loader2 + asChild 多态
platforms:
- web
theme: light
tags:
  aesthetic:
  - industrial
  - minimal
  mood:
  - confident
  - serious
  stack:
  - shadcn-radix
uses:
- tokens/palettes/chameleon/themeable-8x4-system
preview: /preview/components/buttons/chameleon/themeable-cva-button
---

# Chameleon 可切主色 CVA 按钮

> waveflow CVA 按钮的可换肤变体——同样紧凑（最大 lg=h-9）、同样 `loading` 自动 `Loader2` + Radix `Slot` 多态，但 **primary 走可切换的 `--color-primary-*` CSS 变量而非硬编码 blue**：通过 `<html data-primary="...">` 在 8 套主题色间切（blue #2563eb 默认 / purple #9333ea / green #059669 / orange #ea580c / rose / cyan / amber / teal），整站 primary 按钮 / link / focus ring 跟着变。相比 waveflow：**9 variant**（多 `secondary`）× **6 size**（多 `default`/`md` 别名），`primary` 为默认 variant（不是 outline），`default` 别名等于 primary（兼容旧代码免改名）。

## 视觉特征

- **base**：`inline-flex shrink-0 items-center justify-center gap-1.5(6px) whitespace-nowrap rounded-md(6px) font-medium transition-colors disabled:pointer-events-none disabled:opacity-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-200`（focus ring 也跟主题色）
- **9 variant**：
  - `primary`（默认）/ `default`（别名）：`bg-primary-600 text-white hover:bg-primary-700 active:bg-primary-800` —— **primary-600 随 data-primary 切换**（默认 #2563eb）
  - `outline`：`border border-stone-300 bg-white text-stone-700 hover:bg-stone-50 active:bg-stone-100`
  - `secondary`（waveflow 无此 variant）：`bg-stone-100 text-stone-900 hover:bg-stone-200`
  - `ghost`：`text-stone-700 hover:bg-stone-100 active:bg-stone-200`
  - `link`：`text-primary-600 hover:underline underline-offset-2`
  - `danger`：`bg-red-600(#dc2626) text-white hover:bg-red-700 active:bg-red-800`
  - `danger-outline`：`border border-red-300 text-red-600 hover:bg-red-50 active:bg-red-100`
  - `dark`：`bg-stone-900 text-white hover:bg-stone-800 active:bg-stone-700`
- **6 size**：
  - `sm`：`h-7(28px) px-2.5(10px) text-[11.5px]`
  - `md`（默认）/ `default`（别名）：`h-8(32px) px-3(12px) text-[12.5px]`
  - `lg`：`h-9(36px) px-4(16px) text-[14px]`
  - `icon`：`h-8 w-8 p-0`
  - `icon-sm`：`h-7 w-7 p-0`
- **defaultVariants**：`{ variant: 'primary', size: 'md' }`
- **loading**：前置 `<Loader2 className="h-3.5 w-3.5(14px) animate-spin" />` 并 `disabled={disabled || loading}`；asChild 模式不支持 loading（Slot 要求唯一 child）

## 核心代码

```tsx
const buttonVariants = cva(
  'inline-flex shrink-0 items-center justify-center gap-1.5 whitespace-nowrap rounded-md font-medium transition-colors disabled:pointer-events-none disabled:opacity-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-200',
  {
    variants: {
      variant: {
        primary: 'bg-primary-600 text-white hover:bg-primary-700 active:bg-primary-800',
        default: 'bg-primary-600 text-white hover:bg-primary-700 active:bg-primary-800',
        outline: 'border border-stone-300 bg-white text-stone-700 hover:bg-stone-50 active:bg-stone-100',
        secondary: 'bg-stone-100 text-stone-900 hover:bg-stone-200',
        ghost: 'text-stone-700 hover:bg-stone-100 active:bg-stone-200',
        link: 'text-primary-600 hover:underline underline-offset-2',
        danger: 'bg-red-600 text-white hover:bg-red-700 active:bg-red-800',
        'danger-outline': 'border border-red-300 text-red-600 hover:bg-red-50 active:bg-red-100',
        dark: 'bg-stone-900 text-white hover:bg-stone-800 active:bg-stone-700',
      },
      size: {
        sm: 'h-7 px-2.5 text-[11.5px]', md: 'h-8 px-3 text-[12.5px]', default: 'h-8 px-3 text-[12.5px]',
        lg: 'h-9 px-4 text-[14px]', icon: 'h-8 w-8 p-0', 'icon-sm': 'h-7 w-7 p-0',
      },
    },
    defaultVariants: { variant: 'primary', size: 'md' },
  },
);

// asChild → Radix Slot（不支持 loading）；否则 button 前置 Loader2
{loading ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : null}{children}
```

lucide：Loader2。

## 适配指南

- primary 系不硬编码 blue——用 `bg-primary-600` 等 Tailwind token，主色靠 `<html data-primary>` 全站切换（见 themeable-primary-warm-paper token）
- 默认就是 primary（不像 waveflow 默认 outline）——大多数 CTA 直接 `<Button>` 即可
- `default` / `md` 别名只为兼容旧代码免大改名，新代码统一写 `primary` / `md`
- asChild（包 Link / 外链）不传 loading——Slot 要求唯一 child
- focus ring 用 `ring-primary-200` 跟主题色，不写死蓝

## 与 waveflow/cva-engineer-button 区分

| 维度 | waveflow cva-engineer-button | 本条 themeable-cva-button |
|------|------------------------------|---------------------------|
| primary 色 | 硬编码 `bg-blue-600/700/800` | **`bg-primary-600/700/800`**（8 套 data-primary 主题色，blue/purple/green/orange/rose/cyan/amber/teal） |
| variant 数 | 7（primary/outline/ghost/link/danger/danger-outline/dark） | **9**（多 `secondary` + `default` 别名） |
| size 数 | 5（sm/md/lg/icon/icon-sm） | **6**（多 `default` 别名 = md） |
| 默认 variant | `outline` | `primary` |
| focus ring | `ring-blue-200` | `ring-primary-200`（跟主题色） |

选条原则：要「固定蓝、默认 outline 的工程按钮」用 waveflow；要「可换肤主色 + 默认 primary + secondary variant」用本条。

## 反模式

- ❌ primary 写死 `bg-blue-600`——破坏换肤，必须 `bg-primary-600`
- ❌ focus ring 写死 `ring-blue-200`——主色切了 ring 不跟，违和
- ❌ 新代码用 `default` 别名——别名只为兼容旧 import，新写 `primary`
- ❌ asChild 同时传 loading——Slot 会因两个 child 报错
- ❌ loading 时不 disabled——多次点击重发请求
