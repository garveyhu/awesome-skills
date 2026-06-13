---
id: products/quiver
type: product
name: Quiver · 像素办公室 agent 监管台
description: 监管无头编码 agent 的 CEO 甲板——一任务 = 一 git worktree = 一个工位像素小人，整夜自治跑、管预算、每次合并都过验证门
platforms: [web]
theme: dark
category: ai
tags:
  aesthetic: [pixel, glass]
  mood: [calm, playful]
  stack: [vanilla-css]
refs:
  style: styles/experimental/quiver-night-studio
  pages:
    - pages/dashboard/quiver/office-command-deck
  blocks:
    - blocks/layout/quiver/iso-office-world
    - blocks/nav/quiver/glass-topbar-hud
    - blocks/search/quiver/command-palette
    - blocks/feedback/quiver/world-ambience
    - blocks/display/quiver/glass-panel-modal
  components:
    - components/avatars-icons/quiver/pixel-worker-sprite
    - components/buttons/quiver/lime-go-button
    - components/buttons/quiver/glass-chrome-button
    - components/indicators/quiver/autonomy-pill-badge
  tokens:
    palette: tokens/palettes/quiver/night-studio
    typography: tokens/typography/pairs/quiver/sf-system-duo
    motion: tokens/motion/quiver/pixel-steps
    layout: tokens/layout/quiver/iso-grid
---

# Quiver · 像素办公室 agent 监管台

> 一个开源 macOS 桌面应用：把「监管一群无头编码 agent」做成一间整夜亮灯的等距像素办公室。你是 CEO，下个目标，公司自己跑。

## 定位

- **它是什么**：headless 编码 agent 的 supervisor，套了一层治愈像素办公室皮肤。一任务 = 一 git worktree = 一个 detached agent 进程 = 一个工位像素小人。整夜运行、管美元预算、每次合并都过验证门。
- **技术栈**：Tauri v2（Rust 核）+ React/TypeScript + 纯手写 CSS 的 DOM 等距渲染器（已从 Phaser 迁回）+ SQLite。
- **category = ai**：核心价值是编排/监管 AI 编码 agent；视觉上是 `experimental` 的像素游戏皮肤。

## 风格

绑定 [`styles/experimental/quiver-night-studio`](../../styles/experimental/quiver-night-studio/README.md)：夜色 + 唯一琥珀暖强调 + 世界即界面 + 玻璃 chrome + 像素角色承载状态。

## 资产构成

- **页面**：办公室指挥甲板（单屏，世界 + 浮层 chrome + 叠层 + 氛围后期）
- **场景块**：等距像素办公室世界 · 玻璃顶栏 HUD · ⌘K 命令面板 · 世界氛围后期 · 玻璃模态面板
- **组件**：像素工人精灵 · 青柠出发按钮 · 玻璃 chrome 按钮 · 自治状态药丸
- **tokens**：夜色工作室调色板 · 系统无衬线+Mono · 像素步进动效 · 等距像素网格

## signature moment

那间**活着的等距像素办公室**：小人在工位敲键、机房 LED 随机明灭、窗外月光斜射、猫蜷在地上、经理戴着王冠在领导区思考。整个 chrome（HUD/面板/命令栏）全部克制退让，把舞台让给这一个世界。
