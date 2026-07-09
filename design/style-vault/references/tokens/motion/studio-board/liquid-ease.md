---
id: tokens/motion/studio-board/liquid-ease
type: token
name: Liquid easeOut 动效栈
description: cubic-bezier(0.16,1,0.3,1) 阻尼缓动 + 140/240ms 双时长 + 进场/抽屉/运行灯/卡片悬浮 keyframes —— 有物理阻尼的产品级动效
platforms: [web]
theme: both
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-tailwind]
---

# Liquid easeOut 动效栈

> 一条「液体」阻尼缓动统治全站 + 两档时长 + 一组克制 keyframes。产品级：进场编排有节奏、微交互有反馈、绝不 linear。

## 视觉特征

- **主缓动 `cubic-bezier(0.16, 1, 0.3, 1)`**（workstation·强 easeOut·尾部长缓冲=液体感）统一进场/揭示/位移；board 用略缓的 `cubic-bezier(0.2, 0.8, 0.2, 1)`。**绝不用 `linear`/默认 `ease`**
- **两档时长**：`fast 140ms`（hover/点击反馈）、`medium 240ms`（进场/抽屉/转场）
- **进场 `studio-enter`**：`opacity 0→1 + translateY(8px→0)`，medium。首屏卡片错峰入场
- **抽屉 `studio-drawer`**：`opacity 0→1 + translateX(12px→0)`，medium（右侧滑入）
- **运行灯 `studio-running-light`**（进行中态·唯一循环动画）：`opacity .72↔1 + box-shadow 0→5px 扩散环`，1.35s 无限，标出「正在跑」的黄态节点
- **卡片悬浮 `studio-card-motion`**：hover `translateY(-2px)` + 描边转强，fast——1–2px 微上浮，不是整块放大
- **当前步静态环 `studio-node-current`**：`0 5px 16px -4px rgba(acc,.5) + 0 0 0 4px rgba(acc,.1)`——静态高亮不循环，标当前步不抢注意力
- 只动 `transform`/`opacity`（GPU 友好）；尊重 `prefers-reduced-motion`（命中则退化即时态、hover 不位移）

## Tokens

```json
{
  "ease-standard-workstation": "cubic-bezier(0.16, 1, 0.3, 1)",
  "ease-standard-board": "cubic-bezier(0.2, 0.8, 0.2, 1)",
  "duration-fast": "140ms",
  "duration-medium": "240ms",
  "enter": "opacity 0->1 + translateY(8px->0) @ medium",
  "drawer": "opacity 0->1 + translateX(12px->0) @ medium",
  "running-light": "opacity .72<->1 + ring 0->5px @ 1.35s infinite",
  "card-hover": "translateY(-2px) @ fast",
  "node-current": "static glow: 0 5px 16px -4px rgba(acc,.5), 0 0 0 4px rgba(acc,.1)"
}
```

## 适配指南

- 一站只认一条主缓动，写成 CSS 变量 `--ease-standard` 全局复用，别每处手抖一个值
- 循环动画只留「进行中」一处（运行灯）；完成/当前用**静态**高亮环，不循环——多个循环动画一起会抢注意力、显廉价
- 进场用错峰 stagger（IntersectionObserver / 延迟），不是所有元素同时 fade

## 反模式

- 不要 `linear`/默认 `ease`（没有阻尼=模板味）
- 不要 hover 只换背景色（要 1–3px 位移 + 描边/柔光反馈）
- 不要给「当前/完成」态加常驻脉冲（只有「进行中」配循环，其余静态）
- 不要动 `width`/`top`/`left`（掉帧；只动 transform/opacity）
