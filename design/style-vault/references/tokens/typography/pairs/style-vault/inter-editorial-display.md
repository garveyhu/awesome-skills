---
id: tokens/typography/pairs/style-vault/inter-editorial-display
type: token
name: Inter Editorial Display
description: 单字族 Inter，靠字距 + ss01/cv 数字 features + uppercase tracking caption + mono 索引数字拉出编辑感层级
platforms: [any]
theme: both
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind, html-tailwind]
preview: /preview/tokens/typography/pairs/style-vault/inter-editorial-display
---

# Inter Editorial Display

> 一种字（Inter），靠 letter-spacing / OpenType features / uppercase tracking 拉出编辑感节奏

## 视觉特征

- **不引第二种 sans 字族**——整站 Inter 包揽 UI / display / body
- display 标题靠 `letter-spacing: -0.035em` 收紧 + `font-feature-settings: "cv02","cv03","cv04","cv11","ss01"` 启用更"印刷感"的字形（数字 1 带衬、a/g 改字形）
- caption 一律 **uppercase + tracking-[0.18em–0.28em]**——这是编辑感的视觉底层
- mono **不切到第二种字族**——直接用系统 monospace fallback（`font-mono` Tailwind 默认），用在索引数字 `01 / 02 / 03` 和元信息 ID
- 字号梯队跨度大：caption 11px → body 14-17px → h2 22-26px → h1 32-44px → display 64-88px——**靠尺寸跳挡而非字重堆**

## Tokens

```json
{
  "fonts": {
    "sans": "'Inter', -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Microsoft YaHei', 'Segoe UI', sans-serif",
    "display": "'Inter', -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Microsoft YaHei', 'Segoe UI', sans-serif",
    "mono": "ui-monospace, 'SF Mono', Menlo, Consolas, monospace"
  },
  "features": {
    "body":    "'cv02','cv03','cv04','cv11'",
    "display": "'cv02','cv03','cv04','cv11','ss01'"
  },
  "scale": {
    "display":  { "size": "88px", "lineHeight": "1.08", "weight": 600, "letterSpacing": "-0.035em" },
    "h1":       { "size": "44px", "lineHeight": "1.08", "weight": 600, "letterSpacing": "-0.025em" },
    "h2":       { "size": "26px", "lineHeight": "1.2",  "weight": 600, "letterSpacing": "-0.015em" },
    "h3":       { "size": "20px", "lineHeight": "1.3",  "weight": 600 },
    "body-lg":  { "size": "17px", "lineHeight": "1.8",  "weight": 400 },
    "body":     { "size": "14px", "lineHeight": "1.6",  "weight": 400 },
    "caption":  { "size": "11px", "lineHeight": "1.4",  "weight": 500, "letterSpacing": "0.22em", "textTransform": "uppercase" },
    "mono-idx": { "size": "13px", "lineHeight": "1",    "weight": 400, "letterSpacing": "0.05em" }
  }
}
```

## 适配指南

- 全局 `body { font-family: var(--font-sans); }`，display 标题 `class="font-display"` 套上 `letter-spacing: -0.035em`
- caption 用法：所有 kicker / section eyebrow / type 标识——`text-[11px] font-medium uppercase tracking-[0.22em] text-slate-400/500`
- mono 用法：page index `01 02 03` / item ID 字串 / 数字徽标——**不**用于普通正文
- 渐变标题 `bg-clip-text` 时只渐变末尾词，前缀仍 slate-900（参考 HomePage hero "为 AI 编码而造的 / 设计风格库"）

## 反模式

- 不要引第二种 sans（衬线 / 装饰字）——Inter 一种字到底是这套 typography 的核心约定
- 不要把 caption 写成 sentence-case——uppercase + tracking 是身份特征
- 不要为正文加 letter-spacing 收紧（只 display 收紧）
- 不要用 font-weight 800/900——600 是上限
