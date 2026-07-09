---
id: tokens/texture/studio-board/warm-paper-grain
type: token
name: 暖纸颗粒 + 弥散氛围底
description: 全幅 feTurbulence 细颗粒(opacity .05·overlay 混合)去塑料 + 金光弥散 ambient + 48px 细网格 —— 让暖砂白玻璃有纸感纵深
platforms: [web]
theme: both
tags:
  aesthetic: [editorial, organic]
  mood: [warm, calm]
  stack: [react-tailwind]
---

# 暖纸颗粒 + 弥散氛围底

> 三层氛围底：底噪颗粒（去塑料）+ 金光弥散（暖意）+ 细网格（工程台秩序）。让纯色暖砂底有纵深、白玻璃卡浮起来。

## 视觉特征

- **全幅 feTurbulence 颗粒**（详情页 signature）：`fractalNoise · baseFrequency 0.85 · numOctaves 2`，内联 SVG data-URI 平铺；`position:fixed · inset:0 · opacity 0.05 · mix-blend-mode:overlay`，`z-index:0` 只染氛围底、内容层 `z-index:1` 在其上保持锐利。**去「塑料白玻璃」的关键一层**，静态不呼吸
- **金光弥散 ambient**（暖而不黄）：两团低透明径向渐变，`radial-gradient(72vw 60vh at 84% -14%, rgba(200,137,31,0.03), transparent 60%)` + `radial-gradient(60vw 50vh at 8% 4%, rgba(178,152,116,0.03), transparent 55%)`，叠在 `linear-gradient(168deg,#f0eeea,#e9e5df 70%)` 之上；`background-attachment:fixed`。金光收到 .03（demo 的 .20→.10 再半）——**有暖意、不发黄**
- **48px 细网格**（首页 board）：横竖 `linear-gradient` 各 1px、`color-mix(ink 4%)`，`background-size:48px 48px`，叠奶油渐变 + 冷蓝径向高光——工程台秩序感的底纹
- 暗态：关颗粒（`grain:0`）、ambient 改冷顶光 `radial(90vw 62vh at 50% -22%, rgba(120,140,190,.1))`、底改纯 `#14161b`——暗场不要暖颗粒

## Tokens

```json
{
  "grain-opacity-light": 0.05,
  "grain-opacity-dark": 0,
  "grain-svg": "feTurbulence fractalNoise baseFrequency=0.85 numOctaves=2, tile 140x140",
  "grain-blend": "overlay",
  "ambient-gold": "radial-gradient(72vw 60vh at 84% -14%, rgba(200,137,31,0.03), transparent 60%)",
  "ambient-sand": "radial-gradient(60vw 50vh at 8% 4%, rgba(178,152,116,0.03), transparent 55%)",
  "bg-grad": "linear-gradient(168deg, #f0eeea, #e9e5df 70%)",
  "grid-line": "color-mix(in srgb, var(--color-text) 4%, transparent)",
  "grid-size": "48px 48px"
}
```

核心实现（`body::after` 颗粒层）：

```css
:root[data-page='workstation'] body::after {
  content: ''; position: fixed; inset: 0; z-index: 0; pointer-events: none;
  opacity: 0.05; mix-blend-mode: overlay;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}
```

## 适配指南

- 颗粒 `opacity` 0.04–0.06 之间调；超过 0.08 会脏。`mix-blend:overlay` 让它只压暗/提亮不改色
- ambient 弥散只作氛围底、**永远低透明（≤.04）**，不当 signature focal（满屏弥散光=AI 味）
- 内容层务必 `z-index:1` 提到颗粒之上，否则正文被颗粒糊

## 反模式

- 不要把颗粒开太重（>0.08 变噪点脏底）
- 不要暗态还挂暖颗粒 + 金光（暗场发糊，改冷顶光 + 关颗粒）
- 不要拿弥散光/mesh 当满屏兜底——只作暖砂底的氛围补充
