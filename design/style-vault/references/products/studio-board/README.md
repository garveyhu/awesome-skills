---
id: products/studio-board
type: product
name: Media Studio · 暖砂工作台看板
description: 自媒体创作流水线的可视化工作台——首页频道 board(多平台作品流) + 详情页工作台(生产管线/主台/发布备料)，两屏一体的暖砂白玻璃产品
platforms: [web]
theme: both
category: productivity
tags:
  aesthetic: [editorial, glass]
  mood: [warm, calm]
  stack: [react-tailwind]
refs:
  style: styles/content-media/warm-sand-workbench
  pages:
    - pages/dashboard/studio-board/workstation-detail
    - pages/landing/studio-board/channel-board-home
  blocks:
    - blocks/nav/studio-board/pipeline-rail
    - blocks/display/studio-board/publish-hero
    - blocks/media/studio-board/work-card
  components:
    - components/display/studio-board/warm-glass-card
    - components/buttons/studio-board/ink-cta
    - components/tags-badges/studio-board/status-badge
    - components/indicators/studio-board/pipeline-status-light
    - components/toggles/studio-board/platform-pills
  tokens:
    palette: tokens/palettes/studio-board/warm-sand-ink
    typography: tokens/typography/pairs/studio-board/grotesk-han-plex
    texture: tokens/texture/studio-board/warm-paper-grain
    motion: tokens/motion/studio-board/liquid-ease
    radius: tokens/radius/studio-board/soft-sand-scale
preview: /preview/pages/dashboard/studio-board/workstation-detail
---

# Media Studio · 暖砂工作台看板

> media-studio 生态的**可视化工作台**（本地网页看板 + MCP·与对话里的 Claude 共享同一份状态）：把自媒体创作流水线做成「一眼看清、可编辑」的暖砂白玻璃产品。

## 是什么

- **首页 = 频道 board**（[[channel-board-home]]）：奶油纸底 + 细网格，仿各平台个人空间，多平台切换看同一批作品的投稿流。
- **详情页 = 生产工作台**（[[workstation-detail]]）：暖砂颗粒底上四块白玻璃——左「生产管线」轨（选题→脚本→分镜→…→发布，苔绿判成）、中主工作台（步头 + 发布 Hero + 编辑区）、右「发布备料」（四平台核对 + 一键预填 + 回填链接）。
- **视觉脸** = [[warm-sand-workbench]]：暖纸 editorial × 产品级白玻璃 × 苔绿判成 × 暖近黑 CTA × 颗粒去塑料 × 大软圆角 × Grotesk×苹方 × liquid easeOut，亮暖砂 / 暗冷 slate 双态。

## 技术栈

React 18 + Vite + TypeScript + Tailwind 3.4 + react-router v6（无组件库·纯自研 UI + CSS 变量驱动 token）。

## 定位区分

- 这是媒体生产的**工具壳**（生产看板 UI），不是频道对外**内容脸**（后者见 `flywheel` 命名空间：memphis 撞色/scrolly landing）。
- 暖纸工具邻居 `waveflow-warm-engineer` 是平底 soft-card + 蓝 CTA + shadcn；本产品是白玻璃 + 苔绿/暖近黑 + react-tailwind + 双主题。
