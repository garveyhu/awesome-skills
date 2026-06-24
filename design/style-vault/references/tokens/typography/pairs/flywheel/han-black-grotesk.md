---
id: tokens/typography/pairs/flywheel/han-black-grotesk
type: token
name: 思源黑 Black × Grotesk 字体栈
description: 中文思源黑 900 超粗大字 + 西文 Space Grotesk + 等宽 JetBrains Mono —— 黑大字主导的冲击型排版
platforms: [web]
theme: light
tags:
  aesthetic: [brutalist, editorial]
  mood: [confident, energetic]
  stack: [react-tailwind]
preview: /preview/tokens/typography/pairs/flywheel/han-black-grotesk
---

# 思源黑 Black × Grotesk 字体栈

> 中文超粗黑大字（思源黑 Black/Heavy）当 signature 主角 + 西文数字 Space Grotesk + 等宽 JetBrains Mono

## 视觉特征

- **display（标题）**：`'Noto Sans SC'(900), 'PingFang SC', 'Space Grotesk', system-ui` —— Noto Sans SC 是思源黑 web 版，**真·900 黑体**，是整套的冲击主角。`font-weight:900 · line-height:0.98 · letter-spacing:-0.02em`，桌面端 text-6xl/7xl
- **body（正文）**：`'PingFang SC', 'Source Han Sans', system-ui` —— 苹方原生、不拉网络字体省加载；行高 1.6+
- **mono（等宽）**：`'JetBrains Mono', ui-monospace` —— kicker 标签 / 时间戳 / 代码 / 编号
- **kicker 范式**：`mono · 0.72rem · letter-spacing:0.18em · uppercase · ink-soft` —— 每节小标签靠它
- 数字走 `font-feature-settings:'tnum'` 等宽对齐
- 不用 emoji 当图标，用纯几何符号 `▸ → ↓ ⚡` 或 lucide

## Tokens

```json
{
  "font-display": "'Noto Sans SC', 'PingFang SC', 'Space Grotesk', system-ui, sans-serif",
  "font-body":    "'PingFang SC', 'Source Han Sans SC', system-ui, sans-serif",
  "font-mono":    "'JetBrains Mono', ui-monospace, monospace",
  "display-weight": 900,
  "display-leading": 0.98,
  "display-tracking": "-0.02em",
  "kicker": "mono · 0.72rem · 0.18em tracking · uppercase"
}
```

Google Fonts 只拉 `Noto Sans SC:900` + `Space Grotesk` + `JetBrains Mono`；中文正文用系统苹方不拉网络字体（思源黑全字重太重）。

## 适配指南

- 标题**必须**上到 900 黑体才有冲击——若只有 PingFang（无 900）会"软"，务必网络字体兜 `Noto Sans SC:900`
- 三档字族分工死守：大标题 display / 正文 body / 标签代码 mono，不混用
- 换脸时 display 可换任意"超粗 grotesk / 黑体"，但**字重不能降**（signature 是"够黑够粗"）

## 反模式

- ❌ Inter / Roboto / 系统字兜底当主字体（AI 味）
- ❌ 标题用 400/500 常规字重（失去冲击）
- ❌ emoji 当 kicker / 图标符号
- ❌ 中文正文也拉思源黑全字重网络字体（加载爆炸）
