---
id: blocks/feedback/chameleon/flair-glow-empty-state
type: block
name: 辉光呼吸空态
description: 图标 + 标题 + 描述 + action 四件套；flair 模式给图标加 primary-300 radial 辉光呼吸 + 上下漂浮 + primary-500 着色，compact 模式则朴素无动效供表格内用
platforms:
- web
theme: light
tags:
  aesthetic:
  - minimal
  mood:
  - calm
  - playful
  stack:
  - shadcn-radix
uses:
- tokens/motion/waveflow/keyframes-suite
- tokens/palettes/waveflow/warm-paper-ink-blue
preview: /preview/blocks/feedback/chameleon/flair-glow-empty-state
---

# 辉光呼吸空态

> Chameleon 的 `EmptyState`（`core/components/common/empty-state.tsx`）——图标 + 标题 + 描述 + 可选 action 居中四件套。三种形态：默认朴素、`flair` 惊喜感（图标辉光呼吸 + 漂浮 + 主色，用于知识库无文档 / 评测无运行等长留页）、`compact` 紧凑（表格内空态，无动效、尺寸缩小）。

## 视觉特征

- **外容器**：`flex flex-col items-center justify-center text-center`
  - compact：`gap-1.5 py-2`（6px gap / 8px 纵向）
  - 否则：`gap-3 py-10`（12px gap / 40px 纵向）
- **flair 图标**（`flair && !compact`）：`relative grid place-items-center` 包裹，图标自身 `[&>svg]:h-12 [&>svg]:w-12`（48px）
  - **辉光 span**：`aria-hidden` + `anim-halo absolute h-20 w-20 rounded-full`（80px），`background: radial-gradient(circle, color-mix(in srgb, var(--color-primary-300) 28%, transparent), transparent 65%)`——默认主题 `--color-primary-300 = #93c5fd`
  - **漂浮图标层**：`anim-float relative text-primary-500`（默认 `#3b82f6`）
  - `anim-halo` = `halo-pulse 3s ease-in-out infinite`（scale 1→1.12，opacity 0.6→1）；`anim-float` = `float-soft 3.4s ease-in-out infinite`（translateY 0→-7px→0）
- **普通图标**：`text-stone-300`（#d6d3d1）
  - compact：`[&>svg]:h-7 [&>svg]:w-7`（28px）
  - 否则：`[&>svg]:h-12 [&>svg]:w-12`（48px）
- **title**：`font-medium text-stone-600`（#57534e）
  - compact：`text-[12.5px]`，否则 `text-[14px]`
- **description**：`max-w-sm leading-relaxed text-stone-400`（#a8a29e）
  - compact：`text-[11.5px]`，否则 `text-[12.5px]`
- **action**：compact `mt-1`（4px），否则 `mt-2`（8px）

## 核心代码

```tsx
const useFlair = flair && !compact;
<div className={cn('flex flex-col items-center justify-center text-center',
  compact ? 'gap-1.5 py-2' : 'gap-3 py-10', className)}>
  {icon && (useFlair ? (
    <div className="relative grid place-items-center [&>svg]:h-12 [&>svg]:w-12">
      <span aria-hidden className="anim-halo absolute h-20 w-20 rounded-full"
        style={{ background: 'radial-gradient(circle, color-mix(in srgb, var(--color-primary-300) 28%, transparent), transparent 65%)' }} />
      <div className="anim-float relative text-primary-500">{icon}</div>
    </div>
  ) : (
    <div className={cn('text-stone-300', compact ? '[&>svg]:h-7 [&>svg]:w-7' : '[&>svg]:h-12 [&>svg]:w-12')}>{icon}</div>
  ))}
  {title && <div className={cn('font-medium text-stone-600', compact ? 'text-[12.5px]' : 'text-[14px]')}>{title}</div>}
  {description && <div className={cn('max-w-sm leading-relaxed text-stone-400', compact ? 'text-[11.5px]' : 'text-[12.5px]')}>{description}</div>}
  {action && <div className={compact ? 'mt-1' : 'mt-2'}>{action}</div>}
</div>
```

## 与 waveflow/empty-dashed-state 区分

供 AI 消费时选对：

| 维度 | waveflow/empty-dashed-state | chameleon/flair-glow-empty-state |
|------|------|------|
| **外框** | `rounded-lg border-2 border-dashed border-stone-200 px-6 py-10` 虚线圆框 | **无 dashed 框**，纯居中 `flex flex-col` + `gap-3 py-10` |
| **图标容器** | `h-12 w-12 rounded-full bg-stone-100`，内置 16-20px 小图标 | flair：`h-12 w-12`（48px）svg + 80px radial 辉光环；普通：48px svg 裸放 stone-300 |
| **动效** | 无 | **独有 flair**：`anim-halo` 辉光呼吸 + `anim-float` 上下漂浮 + primary-500 着色 |
| **title** | `text-[14px] font-semibold text-stone-700` | `text-[14px] font-medium text-stone-600`（更轻字重、更浅） |
| **description** | `text-[12px] text-stone-500` | `text-[12.5px] text-stone-400`（更浅） |
| **compact 模式** | 无（表格内空态用 DataTable 自带 emptyText） | **独有**：`gap-1.5 py-2` + 28px 图标 + 12.5px title，专供表格 / 抽屉内 |

选型：要「未选择 / 暂无数据」的强空区分隔 → waveflow 虚线框版；要长留页面的惊喜感（KB 无文档、评测无运行）→ flair 版；表格内的轻量占位 → compact 版。

## 适配指南

- flair 仅用于「长留」的全屏 / 大区块空态——动效有持续生命力但不喧宾夺主
- flair 的主色随主题色板切换（`--color-primary-*`）；紫主题辉光是 `#d8b4fe`、绿主题是 `#6ee7b7`，跟主题走
- compact 给 DataTable 内嵌空态 / 抽屉内 / 小卡片用——无动效避免分散注意力
- icon 用 lucide，flair 模式 svg 自动放大到 48px，无须手动指定尺寸

## 反模式

- ❌ flair 与 compact 同开——`useFlair = flair && !compact`，compact 永远压制 flair
- ❌ 给 flair 图标手动写 `h-X w-X`——容器的 `[&>svg]` 选择器已统一控制到 48px
- ❌ 辉光环写死 hex——必须走 `var(--color-primary-300)` + `color-mix`，才能跟主题
- ❌ 表格内空态用 flair 版——动效在密集表格里制造噪音，用 compact
