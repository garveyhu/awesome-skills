---
id: tokens/typography/pairs/acme/ibm-plex-duo
type: token
name: IBM Plex 双字体
description: IBM Plex Sans + IBM Plex Mono，技术感与中性感兼具的字体搭配
platforms: [any]
theme: both
tags:
  aesthetic: [minimal, industrial]
  mood: [serious, calm]
  stack: [react-antd-tailwind, html-tailwind]
preview: /preview/tokens/typography/pairs/acme/ibm-plex-duo
---

# IBM Plex Duo

> Plex Sans 正文 + Plex Mono 代码/数据，统一来自 IBM Plex 家族，风格高度一致

## 视觉特征

- Plex Sans 做 UI 文字：中性、现代、字重从 300 到 700 都可用
- Plex Mono 做 code / number / label：等宽，与 Sans 风格吻合
- 整体偏"工程/文档"观感，与工具型 SaaS 调性契合

## Tokens

```json
{
  "fonts": {
    "sans": "'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif",
    "mono": "'IBM Plex Mono', 'SF Mono', Menlo, monospace"
  },
  "scale": {
    "display": { "size": "56px", "lineHeight": "1.1", "weight": 600, "letterSpacing": "-0.02em" },
    "h1":      { "size": "40px", "lineHeight": "1.2", "weight": 600, "letterSpacing": "-0.01em" },
    "h2":      { "size": "28px", "lineHeight": "1.3", "weight": 600 },
    "h3":      { "size": "20px", "lineHeight": "1.4", "weight": 600 },
    "body":    { "size": "16px", "lineHeight": "1.6", "weight": 400 },
    "caption": { "size": "13px", "lineHeight": "1.5", "weight": 400 }
  },
  "load": "https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap"
}
```

## 适配指南

- 在 HTML `<head>` 里 `<link rel="stylesheet" href="{load}">` 预载
- CSS 变量 `--font-sans` / `--font-mono` 指向 tokens.fonts.sans/mono
- 层级遵循 scale；不要随意改 display/h1 的 letterSpacing
- 中文 fallback：Plex 没有中文字形，Mac 自动掉 PingFang，Windows 掉 Microsoft YaHei

## 反模式

- 别混入第三种字体家族
- 别用 weight < 300 或 > 700
- 别给正文开斜体（Plex 的斜体偏工程气，不贴合正文）
