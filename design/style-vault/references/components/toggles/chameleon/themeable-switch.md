---
id: components/toggles/chameleon/themeable-switch
type: component
name: 主题色开关
description: h-5 w-9 Radix Switch · checked themeable primary-600 / unchecked stone-300 · thumb h-4 w-4 white shadow-soft + translate-x-4
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
preview: /preview/components/toggles/chameleon/themeable-switch
---

# Chameleon Themeable Switch

> chameleon 全站开/关切换——和 waveflow emerald-switch 同尺寸结构（h-5 w-9 轨道 + h-4 w-4 白 thumb），但 checked 态走 **themeable `primary-600`**（跟随站点主题色，默认蓝 `#2563eb` 而非固定 emerald），focus ring 用 `primary-400`、thumb 用 `shadow-soft`。`@radix-ui/react-switch` 实现，`forwardRef` 透传所有 Root props。

## 视觉特征

- **Root 轨道**：`peer inline-flex h-5(20px) w-9(36px) shrink-0 cursor-pointer items-center rounded-full border-2 border-transparent transition-colors`
- **state 切换**：
  - `data-[state=checked]:bg-primary-600`（随主题，默认 `#2563eb`）
  - `data-[state=unchecked]:bg-stone-300(#d6d3d1)`
- **focus ring**：`focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-400`（随主题，默认 `#60a5fa`）
- **disabled**：`disabled:opacity-50`
- **Thumb**：`pointer-events-none block h-4(16px) w-4 rounded-full bg-white shadow-soft transition-transform`
  - `data-[state=checked]:translate-x-4`（向右 16px）/ `data-[state=unchecked]:translate-x-0`
- `shadow-soft` = `0 1px 2px rgb(0 0 0/4%), 0 4px 12px rgb(0 0 0/3%)`（比 emerald-switch 的 `shadow-sm` 更柔）
- 轨道高 20px + thumb 16px → 上下各 2px 缝隙，"刚好包住"

## 核心代码

```tsx
<SwitchPrimitive.Root
  className={cn(
    'peer inline-flex h-5 w-9 shrink-0 cursor-pointer items-center rounded-full border-2 border-transparent transition-colors',
    'data-[state=checked]:bg-primary-600 data-[state=unchecked]:bg-stone-300',
    'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-400 disabled:opacity-50',
  )}
>
  <SwitchPrimitive.Thumb className="pointer-events-none block h-4 w-4 rounded-full bg-white shadow-soft transition-transform data-[state=checked]:translate-x-4 data-[state=unchecked]:translate-x-0" />
</SwitchPrimitive.Root>
```

## 适配指南

- 配置开关、行内启停一律用它——checked 跟站点主题色，不写死
- 乐观更新：`onCheckedChange={c => { setLocal(c); api()... }}`，失败 revert
- icon-only 语义补 `<Tooltip>`（启用/停用）

## 反模式

- ❌ checked 写死某个色（emerald / blue）——破坏 themeable 主题切换，必须 `primary-600`
- ❌ thumb 大小 = 轨道高度——失去"动起来"的视觉感
- ❌ 在大表格里改 `w-12`——破坏全站一致

## 与 waveflow/emerald-switch 区分

| 维度 | chameleon themeable-switch | waveflow emerald-switch |
|------|----------------------------|-------------------------|
| checked 色 | `bg-primary-600`（随主题，默认 `#2563eb`） | `bg-emerald-500`（固定 `#10b981`，语义=任务在跑=绿） |
| focus ring | `ring-primary-400`（随主题） | `ring-blue-200`（固定 `#bfdbfe`） |
| thumb 阴影 | `shadow-soft`（双层柔阴影） | `shadow-sm`（单层硬阴影） |
| transition | `transition-colors`（轨道）+ `transition-transform`（thumb） | `transition`（轨道全属性）+ `transition-transform` |
| 尺寸/结构 | **完全相同**（h-5 w-9 / thumb h-4 w-4 / translate-x-4） | 同左 |

选择：要"开关跟站点主题色变"用 chameleon；要"绿色表达任务运行中"语义用 waveflow emerald。
