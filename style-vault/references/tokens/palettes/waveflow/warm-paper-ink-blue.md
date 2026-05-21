---
id: tokens/palettes/waveflow/warm-paper-ink-blue
type: token
name: 暖纸墨蓝调色板
description: 暖白基底 (#fafaf7 / #f4f3ee / #fffefb) + 墨黑 (#1c1917) + blue-600 主色 + stone/emerald/red/amber/violet 工程师调色
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, industrial]
  mood: [calm, serious]
  stack: [shadcn-radix]
uses: []
preview: /preview/tokens/palettes/waveflow/warm-paper-ink-blue
---

# Waveflow Warm Paper Ink Blue

> waveflow 整站的色彩骨架：**3 档暖白**做底色（页面、卡片、章节头）、**stone 墨色**做主文字、**blue-600** 做唯一动作色、**emerald/red/amber/violet** 仅在状态语义场景出现。低饱和、不冲突、紧凑工程师感的根原语。

## Tokens

```json
{
  "warm": {
    "warm":    "#fafaf7  (页面底)",
    "warm-2":  "#f4f3ee  (侧栏 + 表头 + footer)",
    "paper":   "#fffefb  (卡片 / dialog / popover)"
  },
  "ink": {
    "primary":   "#1c1917  (body 文字)",
    "stone-900": "#1c1917",
    "stone-800": "#292524",
    "stone-700": "#44403c",
    "stone-600": "#57534e",
    "stone-500": "#78716c  (副文 / placeholder)",
    "stone-400": "#a8a29e  (meta caps label)",
    "stone-300": "#d6d3d1  (border)",
    "stone-200": "#e7e5e0  (.kbd shadow / disabled)",
    "stone-100": "#f5f4ee  (skeleton 渐变中点 / divider)"
  },
  "primary": {
    "blue-600":  "#2563eb  (Button primary / 链接 / active icon)",
    "blue-500":  "#3b82f6  (focus border / progress bar)",
    "blue-100":  "#dbeafe  (focus ring / 选中行底色)",
    "blue-50":   "#eff6ff  (子项 active 浅底)",
    "blue-700":  "#1d4ed8  (Button primary hover)"
  },
  "semantic": {
    "emerald-500": "#10b981  (running / 在线 / 成功)",
    "emerald-50":  "#ecfdf5",
    "red-500":     "#ef4444  (error)",
    "red-600":     "#dc2626  (danger Button)",
    "red-50":      "#fef2f2",
    "amber-500":   "#f59e0b  (warning / 执行中)",
    "violet-500":  "#8b5cf6  (任务集 type)",
    "pink-500":    "#ec4899  (清洗类型 / login decor)",
    "cyan-500":    "#06b6d4  (Python 类型 / login decor)",
    "indigo-500":  "#6366f1  (DataX / Three.js mesh)"
  },
  "css-vars": {
    "--color-warm":   "#fafaf7",
    "--color-warm-2": "#f4f3ee",
    "--color-paper":  "#fffefb",
    "--color-ink":    "#1c1917"
  }
}
```

## 视觉特征

- **暖白三档**是整站气质的根：`warm` 做底永远比 `paper` 暗一点点，让卡片"浮出来"——没有这层对比整页变扁平
- **stone 而非 gray**：暖灰 stone 系列让中性色不冷，呼应暖底
- **唯一 CTA 蓝**：blue-600 只用在 primary Button / 链接 / active 图标 / focus border 5 处，其它一律避开蓝色
- **状态语义 5 色**：emerald running / red error / amber 执行中 / blue 进行中 / stone 灰停
- 不出 indigo / violet / cyan / pink 等冷亮色到正常 UI——它们只在登录页装饰（Three.js icosahedron）和 GlueType chip 类型徽标里出现

## 适配指南

- 整站底色：`bg-[var(--color-warm)]`；卡片：`bg-[var(--color-paper)]`；章节头/footer 底：`bg-[var(--color-warm-2)]/40`
- 文字层级：标题 stone-900 → 正文 stone-700/600 → 副文 stone-500 → 占位 stone-400
- border 透明度：外框 `border-stone-200/40`；横分割 `border-stone-100`；输入 `border-stone-300`
- 千万**不要硬编码** `#fafaf7` —— 走 CSS var `var(--color-warm)`

## 反模式

- ❌ 加 indigo/violet/pink 到正常组件——破坏暖工业风
- ❌ 用纯 #fff 做卡片底——会和暖底色"撞色"显廉价
- ❌ 文字用 zinc-* / gray-* 系列（冷灰）—— 与暖底色温不和
