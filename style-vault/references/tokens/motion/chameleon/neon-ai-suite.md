---
id: tokens/motion/chameleon/neon-ai-suite
type: token
name: 霓虹 AI loading 三件套
description: 长耗时 AI 任务专属 signature 动效——锥形渐变霓虹旋转环 + 流光渐变文字 + 容器呼吸辉光；violet→fuchsia→cyan 冷亮霓虹
platforms:
- web
theme: light
tags:
  aesthetic:
  - industrial
  mood:
  - confident
  - energetic
  stack:
  - shadcn-radix
uses: []
preview: /preview/tokens/motion/chameleon/neon-ai-suite
---

# Chameleon Neon AI Loading Suite

> 长耗时 AI 任务（评测 / 分析 / 扩样 / 优化 / 生图）专属的 **signature 动效三件套**：锥形渐变霓虹**旋转环** + 流光渐变**文字** + 容器**呼吸辉光底**。`violet #8b5cf6 → fuchsia #d946ef → cyan #22d3ee` 是 Chameleon 唯一一处冷亮霓虹语言，与暖工业风全站形成强对比——专门用来告诉用户"AI 正在算"。

## Tokens

```json
{
  "neon-colors": {
    "violet": "#8b5cf6  (环渐变 35%)",
    "violet-deep": "#7c3aed  (文字渐变端点)",
    "fuchsia": "#d946ef  (环渐变 55% / 文字中点)",
    "cyan": "#22d3ee  (环渐变 75% / 文字 / drop-shadow)"
  },
  "neon-loader__ring": {
    "background": "conic-gradient(from 90deg, transparent 0%, #8b5cf6 35%, #d946ef 55%, #22d3ee 75%, transparent 100%)",
    "mask": "radial-gradient(farthest-side, transparent calc(100% - var(--neon-t, 2.5px)), #000 0)  ← 中空成环",
    "border-radius": "9999px",
    "filter": "drop-shadow(0 0 3px rgba(139,92,246,.85)) drop-shadow(0 0 7px rgba(34,211,238,.5))",
    "animation": "neon-spin 0.85s linear infinite  → @keyframes neon-spin { to { transform: rotate(360deg) } }"
  },
  "neon-loader__text": {
    "background": "linear-gradient(90deg, #7c3aed, #d946ef, #22d3ee, #7c3aed)",
    "background-size": "200% auto",
    "background-clip": "text  → color: transparent",
    "animation": "neon-shimmer 2.6s linear infinite  → @keyframes neon-shimmer { to { background-position: 200% center } }"
  },
  "neon-loader--glow": {
    "background": "rgba(139,92,246,.05)",
    "box-shadow": "0 0 0 1px rgba(139,92,246,.22), 0 0 16px rgba(139,92,246,.14)",
    "animation": "neon-breathe 2.4s ease-in-out infinite",
    "breathe": "0,100% { 0 0 0 1px rgba(139,92,246,.22), 0 0 12px rgba(139,92,246,.12) }  50% { 0 0 0 1px rgba(217,70,239,.3), 0 0 20px rgba(34,211,238,.2) }",
    "padding": "px-3 py-1.5 (12px / 6px)"
  },
  "sizes": {
    "xs": "d 12px / t 2px    / text-[11px]    (内联按钮)",
    "sm": "d 14px / t 2.25px / text-[11.5px]  (紧凑)",
    "md": "d 16px / t 2.5px  / text-[12px]    (默认)",
    "lg": "d 24px / t 3.25px / text-[13.5px]  (大面板)"
  }
}
```

## 视觉特征

- **环 = conic-gradient + radial mask**：`conic-gradient(from 90deg, transparent→violet 35%→fuchsia 55%→cyan 75%→transparent)` 渲实心圆盘，再用 `radial-gradient` mask 把中间挖空成 `var(--neon-t)` 厚的环——不是 `border` 描边，渐变能沿环周连续过渡
- **双层 drop-shadow 霓虹辉光**：`drop-shadow(0 0 3px violet .85) drop-shadow(0 0 7px cyan .5)`——近处紫强、外圈青弱，霓虹灯管的辉散
- **旋转极快**：`neon-spin 0.85s linear`，比常规 spinner（1s+）快，传达"高速运算"
- **文字 background-clip 流光**：`linear-gradient(90deg, violet-deep, fuchsia, cyan, violet-deep)` 撑 `200% auto`，`neon-shimmer 2.6s` 推 `background-position` 让色带横向流过文字
- **容器呼吸切换 hue**：`neon-breathe 2.4s` 在 violet（0/100%）↔ fuchsia+cyan（50%）之间换 ring 色与辉光半径（12px→20px），底色固定 `rgba(139,92,246,.05)` 极淡紫
- **尺寸自洽**：环直径 `--neon-d` 与环厚 `--neon-t` 同步缩放（12/2 → 24/3.25），文字字号随之 11→13.5px

## 适配指南

- 组件用法：`<NeonLoader label="评测进行中…" size="lg" glow />`；省 `label` 只显环；`glow` 给容器加呼吸辉光底（独立成块更有氛围，内联可不开）
- 环尺寸经 CSS 变量注入：`style={{ '--neon-d': '24px', '--neon-t': '3.25px' }}`，缺省 md（16/2.5）
- 只用在长耗时 AI 任务的等待态——评测 / 分析 / 扩样 / 优化 / 生图；常规 loading 仍用普通 spinner
- 三色锚点固定 `violet #8b5cf6 / #7c3aed · fuchsia #d946ef · cyan #22d3ee`，不要换成主题色——这是跨主题恒定的 AI 签名

## 反模式

- ❌ 用 `border` 画环代替 conic + mask——丢掉渐变沿环连续过渡
- ❌ 把霓虹三色用到非 AI 等待的常规 UI——破坏暖工业风的克制
- ❌ 去掉双层 drop-shadow——环变扁平，没有霓虹辉散
- ❌ 旋转放慢到 1s+ ——失去"高速运算"的张力
- ❌ 文字换纯色——丢掉 background-clip 流光，这是文字部分的灵魂
