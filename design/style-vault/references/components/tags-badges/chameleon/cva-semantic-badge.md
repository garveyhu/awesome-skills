---
id: components/tags-badges/chameleon/cva-semantic-badge
type: component
name: CVA 语义标签
description: 通用 CVA 标签 6 variant (default/primary/success/warning/danger/outline) · 浅底深字 + rounded-md(6px) + px-2 紧凑 chip
platforms:
- web
theme: light
tags:
  aesthetic:
  - minimal
  mood:
  - serious
  stack:
  - shadcn-radix
uses:
- tokens/palettes/chameleon/themeable-8x4-system
preview: /preview/components/tags-badges/chameleon/cva-semantic-badge
---

# Chameleon CVA Semantic Badge

> chameleon 全站通用语义标签——用 CVA 实现 6 个泛化语义 variant（default / primary / success / warning / danger / outline），统一浅底深字 + `rounded-md`。与 waveflow code-status-badge 同属"浅底深字 chip"语言，但它是**泛化的语义变体集**（按业务调 `<Badge variant="success">` 用），不是按执行码映射；primary variant 走 themeable `primary-100/800` 随主题切换。

## 视觉特征

- **基础类**：`inline-flex items-center rounded-md(6px) border px-2(8px) py-0.5(2px) text-xs(12px) font-medium transition-colors`
- **6 variant**（border / bg / text）：
  - `default`（**默认**）：`border-transparent bg-stone-100(#f5f5f4) text-stone-700(#44403c)`
  - `primary`：`border-transparent bg-primary-100 text-primary-800`（随 `data-primary` 主题切换，默认蓝 `#dbeafe` / `#1e40af`）
  - `success`：`border-transparent bg-emerald-100(#d1fae5) text-emerald-800(#065f46)`
  - `warning`：`border-transparent bg-amber-100(#fef3c7) text-amber-800(#92400e)`
  - `danger`：`border-transparent bg-red-100(#fee2e2) text-red-800(#991b1b)`
  - `outline`：`border-stone-300(#d6d3d1) text-stone-700(#44403c)`（透明底 + 实边）
- **统一规则**：实底 5 个 variant 都 `border-transparent`（边框不可见、靠浅底分块），仅 `outline` 留可见边；圆角 `rounded-md`（6px）非 `rounded-full pill`，工程克制
- 渲染为 `<div>` 而非 `<span>`（接 `React.HTMLAttributes<HTMLDivElement>`）

## 核心代码

```tsx
const badgeVariants = cva(
  'inline-flex items-center rounded-md border px-2 py-0.5 text-xs font-medium transition-colors',
  {
    variants: {
      variant: {
        default: 'border-transparent bg-stone-100 text-stone-700',
        primary: 'border-transparent bg-primary-100 text-primary-800',
        success: 'border-transparent bg-emerald-100 text-emerald-800',
        warning: 'border-transparent bg-amber-100 text-amber-800',
        danger:  'border-transparent bg-red-100 text-red-800',
        outline: 'border-stone-300 text-stone-700',
      },
    },
    defaultVariants: { variant: 'default' },
  },
);

export const Badge = ({ className, variant, ...props }: BadgeProps) => (
  <div className={cn(badgeVariants({ variant }), className)} {...props} />
);
```

## 适配指南

- 通用语义标签优先用本组件 `<Badge variant="success">已发布</Badge>`——状态/类别/计数都走它
- `primary` variant 用于跟随站点主题色的强调标记（如"当前主题色"），不写死蓝
- 需要更小更密的纯类别 chip（10/10.5px）走 `orchestration-kind-badge` 那套软色阶，别把本组件改小

## 反模式

- ❌ 圆角改 `rounded-full` —— 失去 chameleon 工业网格感（waveflow 同纪律）
- ❌ 实底 variant 加可见边框——5 个实底全 `border-transparent`，只有 outline 留边
- ❌ 把 `success/danger` 渲染成 emoji ✓ ✗ —— 失去 chip 形态

## 与 waveflow/code-status-badge 区分

| 维度 | chameleon cva-semantic-badge | waveflow code-status-badge |
|------|------------------------------|----------------------------|
| 圆角 | `rounded-md`（6px） | `rounded`（4px） |
| 横向内边距 | `px-2`（8px） | `px-1.5`（6px） |
| 字号 | `text-xs`（12px） | `text-[11px]`（11px） |
| 模型 | 泛化 6 语义 variant（CVA，业务自选） | 按执行码 200/0/500/null 映射 4 态 |
| 边框 | 实底 variant `border-transparent`，仅 outline 留边 | 4 态全带可见浅色边（emerald-300 等） |
| 底色档位 | `-100`（更深，深字 `-800`） | `-50`（更浅，深字 `-700`） |
| primary | themeable `primary-100/800`（随主题切换） | 无 primary，固定执行码色 |

选择：要"语义状态自由组合 + 跟主题色"用 chameleon；要"日志列里按后端 code 自动出状态"用 waveflow。
