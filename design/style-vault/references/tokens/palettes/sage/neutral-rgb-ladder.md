---
id: tokens/palettes/sage/neutral-rgb-ladder
type: token
name: 九阶手调灰阶
description: bg-[rgb(231..252)] 9 个手调灰阶 + slate 体系，承载 sage 整站背景与 hover/selected 微差
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm]
  stack: [react-antd-tailwind]
uses: []
preview: /preview/tokens/palettes/sage/neutral-rgb-ladder
---

# Sage Neutral RGB Ladder

> sage 在 Tailwind `slate` / `gray` 之间手调了一组 9 阶 RGB 灰，专门解决"侧栏 idle / hover / selected / active"微差视觉。Tailwind 默认 slate 阶之间跨度太大（slate-100 #f1f5f9 → slate-50 #f8fafc），手调 RGB 让每两阶之间只差 2-3 个点位，实现"可感知但不刺眼"的细腻状态切换。

## Tokens

```json
{
  "rgbLadder": [
    { "name": "page-bg",        "value": "rgb(249, 249, 249)", "use": "整站 body 背景 / 侧栏底色" },
    { "name": "session-active", "value": "rgb(239, 239, 239)", "use": "选中会话项底色" },
    { "name": "session-hover",  "value": "rgb(237, 237, 237)", "use": "侧栏按钮 hover" },
    { "name": "session-deephover","value": "rgb(231, 231, 231)", "use": "选中会话项 hover" },
    { "name": "icon-btn-hover", "value": "rgb(242, 242, 242)", "use": "圆形图标按钮 hover / 思考过程头部" },
    { "name": "neutral-244",    "value": "rgb(244, 244, 244)" },
    { "name": "neutral-246",    "value": "rgb(246, 246, 246)" },
    { "name": "neutral-251",    "value": "rgb(251, 251, 251)" },
    { "name": "neutral-252",    "value": "rgb(252, 252, 252)" }
  ],
  "slate": {
    "fg-strong":  "#1e293b (slate-800)",
    "fg-base":    "#334155 (slate-700)",
    "fg-body":    "#475569 (slate-600)",
    "fg-muted":   "#64748b (slate-500)",
    "fg-subtle":  "#94a3b8 (slate-400)",
    "fg-ghost":   "#cbd5e1 (slate-300)",
    "border":     "#e2e8f0 (slate-200)",
    "border-soft":"#f1f5f9 (slate-100)",
    "bg-soft":    "#f8fafc (slate-50)"
  },
  "scrollbar": {
    "default-thumb":      "rgb(215, 215, 215)",
    "default-thumb-hover":"rgb(185, 185, 185)",
    "dropdown-thumb":     "rgba(0, 0, 0, 0.02)",
    "dropdown-thumb-hover":"rgba(0, 0, 0, 0.10)"
  }
}
```

## 视觉特征

- 整站底是 `rgb(249,249,249)`——比 `slate-50` (#f8fafc) 暖一丁点，比白纸柔；这一阶决定 sage 不像 Linear 那么冷
- 侧栏交互三档：idle 透明 → hover `rgb(237,237,237)` → selected `rgb(239,239,239)`，差只有 2 个点位但视觉很清晰
- 选中态再 hover 下沉到 `rgb(231,231,231)`——告诉用户"再点一次也是它"
- slate 系负责文字和边框，绝不和 RGB 灰混用作背景

## 适配指南

- 直接 className：`bg-[rgb(249,249,249)]` / `hover:bg-[rgb(237,237,237)]`（Tailwind v4 任意值语法）
- 动态切换可结合 `${themeColor === 'foo' ? 'bg-[rgb(231,231,231)]' : 'bg-[rgb(237,237,237)]'}`
- 滚动条统一定义在 `core/assets/styles/index.less`（默认 7px 灰），下拉用 `.sage-dropdown-scroll` 类（3px 透明黑）

## 反模式

- ❌ 用 `bg-gray-100/200` 替代——色温不一致，整片掉档
- ❌ slate-50 当 page bg——会偏冷
