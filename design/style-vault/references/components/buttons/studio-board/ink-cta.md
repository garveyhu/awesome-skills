---
id: components/buttons/studio-board/ink-cta
type: component
name: 暖墨主操作按钮
description: 暖近黑实底 + 暖奶白字的主 CTA(打开成片/自动填充) + 描边次级 + 陶土危险三态；焦点环走暖近黑
platforms: [web]
theme: both
tags:
  aesthetic: [minimal, editorial]
  mood: [confident, serious]
  stack: [react-tailwind]
uses:
  - tokens/palettes/studio-board/warm-sand-ink
  - tokens/radius/studio-board/soft-sand-scale
preview: /preview/components/buttons/studio-board/ink-cta
---

# 暖墨主操作按钮

> 主操作 = 暖近黑实底 + 暖奶白字（`打开成片` / `自动填充`）。焦点色不是蓝、是暖墨本身，克制而权威。三态：primary(暖墨实底) / secondary(描边) / danger(陶土)。

## 视觉特征

- **primary（主 CTA）**：`bg-text text-bg border-text`——暖近黑 `#2a2620` 实底、暖奶白 `#fffdfa` 字、同色描边；hover 转 `bg-muted-strong`（略提亮）。这是详情页顶栏「打开成片」、发布区「自动填充（停在发布键）」那颗黑按钮
- **secondary（次级）**：`border-border bg-surface text-text`，hover `border-border-strong bg-surface-elevated`——暖白描边按钮
- **danger（危险）**：`border-risk bg-risk text-text`（陶土实底）
- **形**：`rounded-md · border · font-display · font-bold`；两档尺寸 `sm: h-8 px-3 text-xs` / `md: h-10 px-4 text-sm`
- **焦点环**：`focus-visible:ring-2 ring-focus ring-offset-2 ring-offset-bg`——环是暖近黑，不是蓝
- **编号 CTA 变体**：主按钮可带前置序号圆（发布流程「①自动填充 → ②去点发布 → ③回填链接」），圆 `bg-bg/20 text-bg`
- `disabled:opacity-50 cursor-not-allowed`

## 核心代码

```tsx
const BASE = 'inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md border font-display font-bold transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-focus focus-visible:ring-offset-2 focus-visible:ring-offset-bg disabled:opacity-50 disabled:cursor-not-allowed';
const TONE = {
  primary:   'border-text bg-text text-bg hover:bg-muted-strong',
  secondary: 'border-border bg-surface text-text hover:border-border-strong hover:bg-surface-elevated',
  danger:    'border-risk bg-risk text-text hover:border-text',
};
const SIZE = { sm: 'h-8 px-3 text-xs', md: 'h-10 px-4 text-sm' };
```

## 适配指南

- 一屏**只有一颗** primary 暖墨实底（signature 主操作）；其余动作用 secondary 描边，别满屏黑按钮
- 主操作用「暖墨实底」而非彩色，靠形色克制传达权威——彩色实底大按钮反而廉价
- 焦点环、hover 都用 token（`ring-focus`/`bg-muted-strong`），换赛道零改

## 反模式

- 不要主按钮用品牌彩色实底（要暖近黑）
- 不要一屏多颗 primary（主操作唯一）
- 不要纯色平填无 hover 反馈（至少 `hover:bg-muted-strong` 提亮）
