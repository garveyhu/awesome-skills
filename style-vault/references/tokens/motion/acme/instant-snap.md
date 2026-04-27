---
id: tokens/motion/acme/instant-snap
type: token
name: 即时切动效
description: 工业冷感的零浪漫动效——100/150/200ms ease-out，无 bounce、无回弹、无 scale
platforms: [any]
theme: both
tags:
  aesthetic: [minimal, industrial]
  mood: [cold, serious]
  stack: [react-antd-tailwind, html-tailwind]
preview: /preview/tokens/motion/acme/instant-snap
---

# Instant Snap

> 工业冷感的"零浪漫"动效系统：直接切，不浪漫。

## 视觉特征

- 三档 duration：fast 100ms · base 150ms · slow 200ms
- easing 一律 `ease-out`，**绝不**用 `ease-in-out` / `cubic-bezier` spring 曲线
- transform 只允许 `opacity` + `translateY` 1-2px——**不允许** `scale` / `rotate` / `skew`
- 状态切换无动画（`status: healthy → critical` 立即切色，不淡入淡出）
- 唯一例外：`status-pulse` 的 healthy 态有循环呼吸光晕（属"持续状态"而非"切换"）

## Tokens

```json
{
  "duration": { "fast": "100ms", "base": "150ms", "slow": "200ms" },
  "easing":   { "out": "cubic-bezier(0, 0, 0.2, 1)" },
  "transform": {
    "rest":  "translateY(0) opacity(1)",
    "hover": "translateY(-1px)",
    "press": "translateY(0)"
  },
  "css": "transition: background-color 150ms cubic-bezier(0,0,0.2,1), border-color 150ms cubic-bezier(0,0,0.2,1), color 150ms cubic-bezier(0,0,0.2,1), opacity 150ms cubic-bezier(0,0,0.2,1), transform 100ms cubic-bezier(0,0,0.2,1);"
}
```

## 适配指南

- Tailwind 表达：`transition-colors duration-150 ease-out` 是标准基线
- hover 抬起仅在 `cursor-pointer` 元素上用，1px 即可（不超过 2px）
- 配合 `slate-cyan-ice` palette：focus / accent 切换不加渐变
- 与 `gentle-flow`（skillhub）相反——那条偏温柔波动；本条偏机械直接

## 反模式

- 不要 `transition-all`——污染过多属性，常被 layout 抖动击穿
- 不要 `ease-in` / `ease-in-out`——出尾过缓，与"工业"反
- 不要 `scale` / `rotate`——任何放大缩小都偏玩具感
- 不要 spring / bounce / cubic-bezier 带 overshoot——绝对禁止
