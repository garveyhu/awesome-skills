---
id: tokens/palettes/acme/slate-cyan-ice
type: token
name: Slate × Cyan Ice
description: 冷感留白、深 slate 底 + cyan 高亮的工具型界面基础色
platforms: [any]
theme: both
tags:
  aesthetic: [minimal, industrial]
  mood: [cold, serious]
  stack: [react-antd-tailwind, html-tailwind]
preview: /preview/tokens/palettes/acme/slate-cyan-ice
---

# Slate × Cyan Ice

> 冷感留白工具型配色

## 视觉特征

深 slate 底（接近 midnight）、冷灰中间色阶、cyan 高亮作唯一品牌色。无暖色。
阴影低，边界靠 1px 描边而非阴影。

## Tokens

```json
{
  "bg":     { "base": "#0f172a", "subtle": "#1e293b", "panel": "#0b1220" },
  "fg":     { "base": "#e2e8f0", "muted": "#94a3b8", "subtle": "#64748b" },
  "accent": { "base": "#22d3ee", "hover": "#06b6d4", "active": "#0891b2" },
  "border": { "base": "#1e293b", "strong": "#334155" },
  "status": { "success": "#10b981", "warning": "#f59e0b", "danger": "#ef4444" }
}
```

## 适配指南

- `bg.base` 用于整页；`bg.panel` 用于 card / dialog 比页面略深一挡
- `accent.base` 只用在 CTA / 强调字 / focus ring；不用于大面积背景
- 暗色优先；换 light 模式时把 `bg` 组翻转（base=#fff / subtle=#f8fafc / panel=#f1f5f9），`fg` 同理翻转
- 请勿与 `warning` / `danger` 饱和红橙并用大面积——会破坏冷感

## 反模式

- 不要加暖色 accent（打破冷感）
- 不要用 `accent` 做大面积背景
- 不要加渐变或柔光（和无阴影低对比的语言冲突）
