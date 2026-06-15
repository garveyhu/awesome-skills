---
id: tokens/palettes/style-vault/slate-cyan-cool
type: token
name: Slate × Cyan Cool
description: 浅底冷感设计目录站配色 —— slate 全阶 + cyan 单点 accent + #fafafa 页面底
platforms: [any]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, cold, confident]
  stack: [react-antd-tailwind, html-tailwind]
preview: /preview/tokens/palettes/style-vault/slate-cyan-cool
---

# Slate × Cyan Cool

> 浅底冷感设计目录站配色，#fafafa 页面底 + slate 文字阶 + cyan 单点高亮

## 视觉特征

- 页面底色 `#fafafa`，panel/card 白色——**整站白上叠白靠 `border-slate-100/200` 1px 切割**而非阴影
- slate 7 阶完整使用：900（标题/CTA）→ 700（hover）→ 500（正文）→ 400（caption）→ 300（icon idle）→ 200（border）→ 100（separator）→ 50（subtle bg）
- cyan **作为唯一品牌色**——只用在：meta 圆点 / blob 装饰 / 标题 bg-clip 渐变末端 / manifesto italic 强调
- type 圆点 6 色（purple/rose/indigo/cyan/emerald/amber）做层级标识，**不参与品牌主视觉**——仅用于 type 标记

## Tokens

```json
{
  "bg": {
    "page":   "#fafafa",
    "panel":  "#ffffff",
    "subtle": "#f8fafc",
    "dark":   "#0f172a"
  },
  "fg": {
    "heading": "#0f172a",
    "strong":  "#334155",
    "body":    "#64748b",
    "muted":   "#94a3b8",
    "subtle":  "#cbd5e1"
  },
  "border": {
    "soft":  "#f1f5f9",
    "base":  "#e2e8f0",
    "strong":"#cbd5e1"
  },
  "accent": {
    "blob":     "#cffafe",
    "meta-dot": "#06b6d4",
    "italic":   "#67e8f9",
    "deep":     "#0891b2"
  },
  "type-dot": {
    "product":   "#a855f7",
    "style":     "#f43f5e",
    "page":      "#6366f1",
    "block":     "#06b6d4",
    "component": "#10b981",
    "token":     "#f59e0b"
  }
}
```

## 适配指南

- 整页底色一律 `#fafafa`，panel 白；**切割** 全部走 `border-slate-100` (separator) 或 `border-slate-200/80` (card)，不要堆 shadow
- cyan **同屏 ≤ 3 处**：通常 1 个 meta dot + 1 个 blob + 1 处文字强调（manifesto italic / 标题渐变末端）。超过就糊
- dark panel（`#0f172a`）只用于 manifesto / 主 CTA 填充——不要做大面积 dark hero
- type-dot 是数据可视化用色，**不**参与品牌——做 type / category 区分时才出现，1.5×1.5px 小圆点形态

## 反模式

- 不要把 cyan 当大面积背景（`bg-cyan-500` 整段）
- 不要把 slate-900 当 hero 全填底（除 manifesto 外）
- 不要给白卡叠重投影（违反"白上叠白靠 hairline"原则）
- 不要用 emerald / rose / amber 做大面积——它们只是 type-dot 区分器
