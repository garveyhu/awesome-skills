---
id: components/indicators/studio-board/pipeline-status-light
type: component
name: 管线节点状态灯
description: 圆形状态节点——完成=实心苔绿+白勾+柔光·进行=琥珀软圈脉冲·需处理=柔红·未开始=中性空·跳过=虚线；语义清晰不刺
platforms: [web]
theme: both
tags:
  aesthetic: [minimal]
  mood: [calm, confident]
  stack: [react-tailwind]
uses:
  - tokens/palettes/studio-board/warm-sand-ink
  - tokens/motion/studio-board/liquid-ease
preview: /preview/components/indicators/studio-board/pipeline-status-light
---

# 管线节点状态灯

> 生产管线每一步的圆形状态灯，五种语义各一副长相。完成态是**实心苔绿 + 白勾 + 柔光外扩**，是首页/详情页判「成」的视觉主音。

## 视觉特征

- **圆形节点**：`rounded-full · inline-flex 居中 · font-mono font-semibold`；两档尺寸 `compact h-7 w-7 text-[11px]` / 常规 `h-9 w-9 text-[13px]`
- **五态**：
  - `green`（完成）：`bg-success text-white border-transparent` + 柔光 `shadow-[0_4px_12px_-4px_rgba(var(--ok-rgb),0.5)]`，内嵌**白勾** SVG（`strokeWidth 3.4` 圆头）——苔绿实心 + 白勾 + 绿柔光
  - `yellow`（进行中）：`border-warning bg-warning/10 text-warning` + `studio-running-light`（循环脉冲环）——琥珀软圈、唯一循环态
  - `red`（需处理）：`border-risk bg-risk/10 text-risk`——柔红软圈
  - `gray`/`waiting`（未开始/待确认）：`border-border bg-surface text-muted`——中性空心
  - `skipped`（跳过）：`border-dashed border-border bg-surface/60 text-muted-strong/50`——虚线中性，一眼区别于「还没做」
- 完成态显白勾（不显字形），其余态显灯语义 glyph
- **只有「进行中」配循环动画**，完成/未开始/跳过全静态——避免多个循环抢注意力

## 核心代码

```tsx
const VARIANT = {
  green:   'border border-transparent bg-success text-white shadow-[0_4px_12px_-4px_rgba(var(--ok-rgb),0.5)]',
  yellow:  'border border-warning bg-warning/10 text-warning studio-running-light',
  red:     'border border-risk bg-risk/10 text-risk',
  gray:    'border border-border bg-surface text-muted',
  waiting: 'border border-border bg-surface text-muted',
};
// skipped: 'border border-dashed border-border bg-surface/60 text-muted-strong/50'
// green 内嵌白勾：<path d="M20 6 9 17l-5-5" strokeWidth={3.4} />
```

`--ok-rgb: 91, 140, 90`（苔绿的 rgb，供柔光 rgba 用）。

## 适配指南

- 完成态的苔绿柔光是「判成」的情绪锚——换赛道时随 `success` 色一起换 `--ok-rgb`
- 「进行中」才用脉冲；别给完成/当前也加循环（静态柔光即可）
- compact 尺寸用于密集列表（管线步骤行），常规尺寸用于独立状态展示

## 反模式

- 不要完成态用描边空心（要实心 + 白勾，判成要「实」）
- 不要多态都加循环动画（只进行中循环）
- 不要荧光绿/科技绿（要低饱和苔橄榄）
