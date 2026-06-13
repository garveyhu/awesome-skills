---
id: styles/admin-console/chameleon-ai-orchestration
type: style
name: Chameleon · 暖白工程师 AI 编排台
description: 在 waveflow 暖纸墨蓝工程师语言之上叠加「霓虹 AI 强调 + 可切换主题 + 画布节点配色」三件套——暖白基底 (#fafaf7/#f4f3ee/#fffefb) + ink#1c1917 + blue-600 单一 CTA + Inter/JetBrains Mono/Instrument Serif，长耗时 AI 任务用紫→品红→青锥形霓虹环点睛，工作流画布按节点类型微染色温
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, industrial]
  mood: [calm, serious, confident]
  stack: [shadcn-radix]
uses:
  - tokens/palettes/chameleon/themeable-8x4-system
  - tokens/motion/chameleon/neon-ai-suite
  - tokens/motion/chameleon/keyframes-anim-modes
  - tokens/palettes/chameleon/node-type-hue-system
  - tokens/motion/chameleon/canvas-edge-dash-flow
  - tokens/palettes/waveflow/warm-paper-ink-blue
  - tokens/typography/pairs/waveflow/inter-jetbrains-instrument-trio
  - tokens/shadow/waveflow/soft-card-pop-trio
  - tokens/border/waveflow/translucent-stone-system
  - tokens/iconography/waveflow/engineer-detail-classes
  - tokens/layout/waveflow/data-console-shell
  - components/feedback/chameleon/neon-loader
  - components/buttons/chameleon/themeable-cva-button
  - components/inputs/chameleon/codemirror-json-editor
  - components/inputs/chameleon/graph-config-field-kit
  - components/toggles/chameleon/sliding-thumb-segmented
  - components/display/chameleon/recharts-time-series
  - blocks/canvas/chameleon/node-palette
  - blocks/canvas/chameleon/graph-node-card
  - blocks/canvas/chameleon/config-panel-inspector
  - blocks/display/chameleon/trace-observation-tree-gantt
  - blocks/display/chameleon/eval-spreadsheet-airtable
  - blocks/chat/chameleon/message-list-bubble-thread
  - blocks/layout/chameleon/domain-tab-app-shell
  - blocks/nav/chameleon/borderless-bookmark-rail
preview: /preview/styles/admin-console/chameleon-ai-orchestration
---

# Chameleon · 暖白工程师 AI 编排台

> 与 [[styles/admin-console/waveflow-warm-engineer]] 同根（暖白纸墨 + blue-600 + 三字体 + tabular-nums 工程师感），但 Chameleon 是 **LLM 编排平台**，在工程师底座上叠了三层 AI 专属语言：**① 霓虹 AI 流**（长耗时任务的紫→品红→青锥形旋转环 + 流光文字 + 呼吸辉光）、**② 可切换主题**（8 primary × 4 neutral × 3 anim，data-attribute 运行时切换）、**③ 工作流画布**（xyflow 节点按 9 类语义微染色温 + 流动虚线连线）。

## 视觉特征

- **基底**：页面 `--color-warm #fafaf7`，侧栏/表头 `--color-warm-2 #f4f3ee`，卡片/dialog/popover `--color-paper #fffefb`，正文 `--color-ink #1c1917`。`* { border-color: rgb(0 0 0/8%) }` 极淡描边。base 14px / line-height 1.5。
- **唯一动作色**：`blue-600 #2563eb`（Button primary / 链接 / active），focus 走 `blue-500 #3b82f6` 边 + `blue-100 #dbeafe` ring；选中行/子项浅底 `blue-50 #eff6ff`。语义色仅状态用：emerald #10b981 / red #ef4444 / amber #f59e0b / cyan #06b6d4。
- **三字体**：Inter 正文 UI、JetBrains Mono 跑 ID/cron/token/路径/日志（`.tnum` tabular-nums）、Instrument Serif italic 做 editorial 出口。
- **signature moment（与 waveflow 的关键分野）**：长耗时 AI 任务（评测/分析/扩样/生图）用 `NeonLoader`——`conic-gradient(from 90deg, transparent, #8b5cf6 35%, #d946ef 55%, #22d3ee 75%, transparent)` + radial mask 中空成环 + `drop-shadow` 双层霓虹辉光 + 流光渐变文字。这是整套冷静工程感里**唯一允许的「奇观」**，其余一律克制。
- **可切换主题**：`:root[data-primary]`（8 色）/`[data-neutral]`（4 中性）/`[data-anim]`（disabled/agile/smooth）运行时重写 CSS 变量，无需重载。默认 blue + stone + smooth。
- **工作流画布**：节点卡 `rounded-[14px]` 按类型整卡微染色温（hue-50/40 无拼接缝），连线贝塞尔 curvature 0.2 四态（normal stone-300 / active 蓝流动虚线 / fail rose 虚线 / dimmed 0.35）。

## Tokens

```json
{
  "warm":   "#fafaf7", "warm-2": "#f4f3ee", "paper": "#fffefb", "ink": "#1c1917",
  "primary-600": "#2563eb", "primary-500": "#3b82f6", "primary-100": "#dbeafe", "primary-50": "#eff6ff",
  "semantic": { "success": "#10b981", "warning": "#f59e0b", "danger": "#ef4444", "info": "#06b6d4" },
  "neon": { "violet": "#8b5cf6", "violet-deep": "#7c3aed", "fuchsia": "#d946ef", "cyan": "#22d3ee" },
  "font": { "sans": "Inter", "mono": "JetBrains Mono", "serif": "Instrument Serif" },
  "shadow": { "soft": "0 1px 2px rgb(0 0 0/4%),0 4px 12px rgb(0 0 0/3%)", "card": "0 1px 3px rgb(0 0 0/5%),0 2px 8px rgb(0 0 0/3%)", "pop": "0 8px 24px rgb(0 0 0/8%),0 2px 8px rgb(0 0 0/4%)" }
}
```

## 适配指南

- 起一个同风格 AI 编排 / Agent 平台：先冻结 `themeable-8x4-system` 的 blue+stone 默认 + `inter-jetbrains-instrument-trio` 字体，再按域铺 `domain-tab-app-shell`（顶部域 Tab + 左侧 `borderless-bookmark-rail` 书签竖条）。
- AI 长任务 loading **必须**用 `neon-loader`（不要用普通 spinner）——这是品牌识别点。普通数据 loading 用 waveflow 的 shimmer skeleton。
- 有工作流/编排画布才引 `node-type-hue-system` + `canvas-edge-dash-flow` + canvas blocks；纯表单后台不需要。
- 复用 waveflow 地基：通用按钮/输入/开关/表格/cron/状态点直接 ref `waveflow/*`，不要重造。

## 反模式

- ❌ 霓虹色用在非 AI 场景（普通按钮/边框/背景）——霓虹只属于「AI 正在干活」这一个语境。
- ❌ 同屏多处 signature moment——neon 一屏最多一处，其余留白。
- ❌ 把可切换主题的非默认色（purple/rose 等）硬编码进组件——必须走 `--color-primary-*` 变量才能跟随切换。
- ❌ 节点配色用满饱和——画布节点是「微染色温」（hue-50/40 浅底），不是高饱和色块。
