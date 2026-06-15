---
id: tokens/palettes/sage/twelve-theme-spectrum
type: token
name: 十二主题色谱
description: 12 个用户可切换主题色 × 3 档明度（hex / light / selection），驱动整站 119 处动态着色
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses: []
preview: /preview/tokens/palettes/sage/twelve-theme-spectrum
---

# Sage Twelve-Theme Spectrum

> 12 个 Tailwind 色阶映射的主题色，用户在头像菜单里点击切换；整站每一处带颜色的元素（CTA / 选中态 / focus ring / 头像 icon / 进度条 / 主按钮）都通过 `THEME_CLASSES[themeColor]` 动态查表着色——主题切换是 sage 视觉系统的根原语。

## Tokens

```json
{
  "themes": {
    "blue":   { "tw": "blue",    "hex": "#60a5fa", "light": "#93c5fd", "selection": "#bfdbfe" },
    "green":  { "tw": "emerald", "hex": "#10b981", "light": "#34d399", "selection": "#a7f3d0" },
    "yellow": { "tw": "amber",   "hex": "#fbbf24", "light": "#fcd34d", "selection": "#fde68a" },
    "pink":   { "tw": "pink",    "hex": "#f472b6", "light": "#f9a8d4", "selection": "#fbcfe8" },
    "orange": { "tw": "orange",  "hex": "#fb923c", "light": "#fdba74", "selection": "#fed7aa" },
    "gray":   { "tw": "slate",   "hex": "#64748b", "light": "#94a3b8", "selection": "#e2e8f0" },
    "purple": { "tw": "violet",  "hex": "#a78bfa", "light": "#c4b5fd", "selection": "#ddd6fe" },
    "red":    { "tw": "red",     "hex": "#f87171", "light": "#fca5a5", "selection": "#fecaca" },
    "indigo": { "tw": "indigo",  "hex": "#818cf8", "light": "#a5b4fc", "selection": "#c7d2fe" },
    "teal":   { "tw": "teal",    "hex": "#2dd4bf", "light": "#5eead4", "selection": "#99f6e4" },
    "cyan":   { "tw": "cyan",    "hex": "#22d3ee", "light": "#67e8f9", "selection": "#a5f3fc" },
    "rose":   { "tw": "rose",    "hex": "#fb7185", "light": "#fda4af", "selection": "#fecdd3" }
  },
  "axes": {
    "text":         "text-{tw}-400|500",
    "textHover":    "hover:text-{tw}-400|500",
    "textDark":     "text-{tw}-500|600",
    "bg":           "bg-{tw}-400|500",
    "bgHover":      "hover:bg-{tw}-500|600",
    "bgLight":      "bg-{tw}-50",
    "bgLightActive": "bg-{tw}-100",
    "border":       "border-{tw}-100",
    "borderFocus":  "focus:border-{tw}-300",
    "ring":         "focus:ring-{tw}-300",
    "shadow":       "shadow-{tw}-100"
  }
}
```

## 视觉特征

- 12 色覆盖暖（pink / orange / amber / rose）+ 中（blue / teal / cyan / indigo）+ 冷（emerald / slate / violet / red）三象限，足够让每个用户找到"自己的颜色"
- 每色三档明度有明确语义：`hex`（默认 CTA / icon）/ `light`（侧栏会话选中、Suspense fallback、Loading）/ `selection`（::selection 文本选中）
- `gray` 是唯一映射到 `slate` 的项——表示"无主题"但仍然走主题系统的 fallback
- `green` / `teal` / `gray` / `blue` 四档主色 500 而非 400，因为它们偏冷需要更高饱和度才能"读出来"

## 适配指南

- 任何带颜色的元素：从 `import { THEME_CLASSES } from '@/core/utils/themeUtils'` 查表，**绝不**硬编码 `bg-blue-500`
- 取 raw hex（用于 styled-components / inline style）：`THEME_HEX_COLORS[themeColor]`
- ::selection 全局变色：`THEME_SELECTION_COLORS[themeColor]`，配合一段 `<style>` 注入

## 反模式

- ❌ 硬编码 Tailwind 色类（`bg-blue-500`）—— 主题切换时不会变
- ❌ 把 `themeColor` 直接当 Tailwind 词（`bg-${themeColor}-500`）—— 用户主题词 ≠ Tailwind 词（"green" → "emerald"），且 JIT 不识别动态拼接
