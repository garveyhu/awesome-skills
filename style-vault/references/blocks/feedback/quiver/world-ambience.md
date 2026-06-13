---
id: blocks/feedback/quiver/world-ambience
type: block
name: 世界氛围后期
description: 夜色呼吸天空 + 预算染色红边告警 + 交付绿红闪 + 暗角颗粒浮尘，整屏氛围与状态反馈后期层
platforms: [web]
theme: dark
tags:
  aesthetic: [pixel, glass]
  mood: [dreamy, calm]
  stack: [vanilla-css]
uses:
  - tokens/palettes/quiver/night-studio
  - tokens/motion/quiver/pixel-steps
preview: /preview/blocks/feedback/quiver/world-ambience
---

# 世界氛围后期

> 叠在世界之上的整屏后期层：夜色整夜缓慢呼吸、预算逼近上限全场转冷转暗、交付时刻边缘泛光——氛围即状态反馈

## 视觉特征

- **夜色呼吸天空 `#sky`**：JS `nightTick`（650ms）整夜三段循环——黄昏 `[42,34,58]` → 深夜 `[8,14,34]` → 黎明 `[20,34,64]`，地平线暖冷过渡（HOT `[120,72,46]` ↔ COLD `[36,58,96]`），写成竖向三档 `linear-gradient`，用 ref 改 style 不触发重渲染
- **预算 = 能量染色 `#budgetTint`**：`budgetTick`（800ms）按 `花费/上限` 开方驱动 opacity（`e*0.55`），`mix-blend-mode: multiply` 的蓝紫径向——花费越逼近上限，全场越冷越暗
- **临界红边 `#rededge`**：花费 > 78% 时浮现径向红边并 `redpulse 2.4s` 脉动——「快烧光了」的体感告警
- **交付脉冲 `#flashfx`**：验收通过 = 绿径向边 `rgba(108,196,122,.42)`、打回 = 红径向边，`flashfx 1.2s` 一闪即散
- **暗角 `#vignette`**：静态径向 `rgba(0,0,0,0)→.6`，把视线收向中心舞台
- **颗粒 `#grain`**：`opacity: .05` + `mix-blend-mode: overlay` 的双层 repeating-radial 噪点，**静态缓存不平移**（平移动画曾让脏矩形撑满整窗→掉帧）
- **浮尘**：22 粒，暖灯附近偏暖 `#ffe2b0`、余处冷白，`floaty` 上浮淡出，时长 4–9s 错相位
- **失焦不刷新**：nightTick/budgetTick 都 `if (!document.hasFocus()) return`——失焦时不动全屏层，避免空占合成器

## 核心代码

```tsx
<Atmosphere spentUsd={spent} budgetCapUsd={cap} />  // #sky / #budgetTint / #rededge
<div id="flashfx" className={fx ?? ''} />            // ok | bad 一闪
<div id="vignette" /><div id="grain" />              // 静态后期
```

## 适配指南

- 全屏氛围层一律用 ref 改 style + setInterval 驱动，**别进 React 重渲染**；且失焦时 early-return 停刷
- 「预算→冷暗」「交付→泛光」把抽象状态翻成体感——数字之外多一层「能感觉到」的反馈
- 颗粒/扫描线只栅格化一次缓存，绝不挂平移动画

## 反模式

- 不要让任何全屏层挂持续平移/无限动画——脏矩形 = 整窗，每帧重栅格化，整机掉帧
- 不要用 `filter: blur` + `mix-blend` 做大面积柔光——macOS WebView 合成极耗 GPU，用 radial-gradient 模拟
- 不要把氛围层做成纯装饰——绑定预算/交付真实状态，氛围才有信息量
