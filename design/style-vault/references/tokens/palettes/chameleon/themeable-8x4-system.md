---
id: tokens/palettes/chameleon/themeable-8x4-system
type: token
name: 可切换 8×4 主题系统
description: 运行时 data-attribute 切换的 8 primary × 4 neutral 调色系统；默认 = waveflow 暖纸墨蓝，叠 :root[data-primary]/[data-neutral] 属性切换重写全套 CSS 变量
platforms:
- web
theme: light
tags:
  aesthetic:
  - industrial
  - minimal
  mood:
  - calm
  - confident
  - serious
  stack:
  - shadcn-radix
uses: []
preview: /preview/tokens/palettes/chameleon/themeable-8x4-system
---

# Chameleon Themeable 8×4 System

> 运行时 `data-attribute` 切换的多主题调色系统：**8 个 primary 调色板**（blue 默认 + purple/green/orange/rose/cyan/amber/teal）× **4 个 neutral 基底**（stone 默认 + slate/zinc/gray）。默认值就是 waveflow 暖纸墨蓝，但叠加了 `:root[data-primary]` / `:root[data-neutral]` 属性层——整套 `--color-primary-50..900` 与 `--color-warm/warm-2/paper/ink` 在运行时重写，无需重新加载。

## Tokens

```json
{
  "default-@theme": {
    "primary": {
      "50": "#eff6ff", "100": "#dbeafe", "200": "#bfdbfe", "300": "#93c5fd", "400": "#60a5fa",
      "500": "#3b82f6", "600": "#2563eb", "700": "#1d4ed8", "800": "#1e40af", "900": "#1e3a8a"
    },
    "neutral-base": {
      "--color-warm": "#fafaf7  (页面底)",
      "--color-warm-2": "#f4f3ee  (侧栏 + 表头)",
      "--color-paper": "#fffefb  (卡片 / dialog)",
      "--color-ink": "#1c1917  (body 文字)"
    },
    "semantic": {
      "--color-success": "#10b981",
      "--color-warning": "#f59e0b",
      "--color-danger": "#ef4444",
      "--color-info": "#06b6d4"
    },
    "body": "background var(--color-warm); color var(--color-ink); font-family var(--font-sans); font-size 14px; line-height 1.5; -webkit-font-smoothing antialiased"
  },
  "primary-palettes (各 50..900，锚 500/600)": {
    "blue":   "默认（@theme 已写，不覆盖）· 500 #3b82f6 / 600 #2563eb",
    "purple": "500 #a855f7 / 600 #9333ea",
    "green":  "500 #10b981 / 600 #059669",
    "orange": "500 #f97316 / 600 #ea580c",
    "rose":   "500 #f43f5e / 600 #e11d48",
    "cyan":   "500 #06b6d4 / 600 #0891b2",
    "amber":  "500 #f59e0b / 600 #d97706",
    "teal":   "500 #14b8a6 / 600 #0d9488"
  },
  "neutral-bases (覆盖 warm / warm-2 / paper / ink)": {
    "stone":  "默认（@theme 已写）· #fafaf7 / #f4f3ee / #fffefb / #1c1917",
    "slate":  "#f8fafc / #f1f5f9 / #ffffff / #0f172a",
    "zinc":   "#fafafa / #f4f4f5 / #ffffff / #18181b",
    "gray":   "#f9fafb / #f3f4f6 / #ffffff / #111827"
  },
  "anchor": "调色板基于 Tailwind v4 默认色板的 500/600/700 阶为锚",
  "switch": "document.documentElement.dataset.primary = 'purple'; dataset.neutral = 'slate'  → 立即重写，无需重载"
}
```

## 视觉特征

- **两轴独立切换**：`primary`（动作色：CTA / 链接 / active / focus）与 `neutral`（基底色温：页面 / 卡片 / 文字）互不耦合——8 × 4 = 32 组合
- **primary 只重写 `--color-primary-*`**：50..900 全套覆盖，锚在 Tailwind v4 默认色板的 500/600/700 阶（如 purple 600 = `#9333ea`、teal 600 = `#0d9488`）；blue 是默认值在 `@theme` 已写，不进切换层
- **neutral 只重写 4 个基底变量**：`--color-warm` / `--color-warm-2` / `--color-paper` / `--color-ink`——stone（暖灰、默认）vs slate/zinc/gray（三档不同色温的冷灰）；切冷灰系时 paper 变纯 `#ffffff`、ink 变更深的冷黑
- **stone 默认不写覆盖**：暖白 `#fafaf7`（warm 永远比 paper `#fffefb` 暗一点点，让卡片浮出来）；slate/zinc/gray 把 paper 都改成纯 `#ffffff`，气质转向冷工程
- **语义 4 色固定不进切换**：success emerald / warning amber / danger red / info cyan 在任何主题下恒定，保证状态语义跨主题一致
- **score 色阶（评测复用）**：≥0.8 emerald-600/emerald-50 · 0.5–0.8 amber-600/amber-50 · <0.5 red-600/red-50 · 空 stone-400/stone-100
- **body 基础锚定**：14px / line-height 1.5 / antialiased，无论换什么主题都不动

## 适配指南

- 写主题：`document.documentElement.dataset.primary = 'teal'`、`dataset.neutral = 'zinc'`；移除 attr 回默认 blue + stone
- 取色：组件一律走 `bg-primary-600` / `text-primary-700` / `bg-[var(--color-paper)]` / `text-[var(--color-ink)]`，**不硬编码 hex**——这样切主题才生效
- 卡片底用 `var(--color-paper)`、页面底 `var(--color-warm)`、章节头 `var(--color-warm-2)`，保留 warm < paper 的微对比
- 新增 primary 调色板：在 theme.css 写 `:root[data-primary="<name>"] { --color-primary-50..900 }` 全 10 阶，以 Tailwind 同名色板对齐

## 反模式

- ❌ 硬编码 `#2563eb` / `#fafaf7`——切主题失效，必须走 CSS var / `primary-*` 语义
- ❌ 让 primary 切换影响语义 4 色——状态色跨主题恒定
- ❌ neutral 只改 warm 不改 paper/ink——基底色温会割裂
- ❌ 新增 primary 只写 500/600——下拉 / 浅底 / hover 会缺阶，必须 50..900 齐全

## 与 waveflow/warm-paper-ink-blue 区分

同源——默认态完全等同 waveflow 暖纸墨蓝（primary blue `#2563eb` + stone 暖白 `#fafaf7 / #fffefb / #1c1917` + 语义 4 色 emerald/amber/red/cyan）。差异只在「可切换层」：

| 维度 | waveflow/warm-paper-ink-blue | chameleon/themeable-8x4-system |
|------|------------------------------|--------------------------------|
| **结构** | 单套硬冻结色板 | 默认板 + `:root[data-primary]` / `:root[data-neutral]` 两轴运行时切换 |
| **primary** | 只有 blue（`#2563eb`），别处避开蓝色 | blue 默认 + 7 个可切（purple/green/orange/rose/cyan/amber/teal），全 50..900 |
| **neutral** | 只有 stone 暖白（`#fafaf7` 系） | stone 默认 + slate/zinc/gray（切冷灰时 paper → 纯白） |
| **切换** | 无——色板是常量 | `dataset.primary/neutral` 即时重写，无需重载 |
| **气质** | 单一冻结暖工业 | 暖工业可调成冷工程 / 多 accent 的主题工厂 |

需要"就一套确定的暖纸墨蓝、不给用户调"→ 选 waveflow；需要"允许用户切 accent 色 + 基底色温的可换肤系统"→ 选 chameleon（默认态视觉与 waveflow 像素一致）。
