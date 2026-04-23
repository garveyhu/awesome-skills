---
id: vibes/saas-tool/cold-industrial-saas
type: vibe
name: Cold Industrial SaaS
description: 冷感留白 + IBM Plex 双字体 + 几何切割，工具型 SaaS 的整站调性
tags:
  aesthetic: [minimal, industrial]
  mood: [cold, serious]
  theme: [dark, light]
  stack: [react-antd-tailwind]
uses:
  - primitives/palettes/slate-cyan-ice
  - primitives/typography/pairs/ibm-plex-duo
  - atoms/buttons/ghost-button
  - archetypes/landing/saas-landing
preview: /preview/vibes/saas-tool/cold-industrial-saas
---

# Cold Industrial SaaS

> 冷感留白、几何切割、无圆角的工具型 SaaS 基调

## 视觉特征

- 全站暗色（slate-950 底）
- IBM Plex Sans 正文 + Plex Mono 数据
- 圆角 ≤ 4px；无阴影；1px slate-800 描边
- 只一个 cyan-400 高亮色
- 动效 150ms ease-out，无 bounce

## 适配指南

- 把 uses 里的 primitive tokens 注入 CSS 变量：
  - `--font-sans` / `--font-mono` ← ibm-plex-duo
  - `--color-bg` / `--color-fg` / `--color-accent` ← slate-cyan-ice
- archetypes/landing/saas-landing 直接套用后只需覆盖变量
- ghost-button 作为次要 CTA；primary CTA 用 slate-cyan-ice 的 accent 作填色

## 反模式

- 不要用 > 4px 圆角
- 不要加暖色 accent / 渐变 / 柔光
- 不要混入第三种字体
