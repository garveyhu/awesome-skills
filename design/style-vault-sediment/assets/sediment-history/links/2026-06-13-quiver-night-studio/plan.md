# 沉淀计划 · Quiver 夜色像素工作室

日期：2026-06-13
作者：links
模式：create
起点：from-project（~/Coding/Archer/quiver · feat/game-first 分支）
档位：Tier 2 · 基础级（目标 12–18 · 本计划 16 条）
技术栈指纹：React 18 + TypeScript + Vite + Tauri v2 · 纯手写 CSS（无 Tailwind）· DOM 等距渲染器（clip-path 体素 + 画家算法 z-index）
namespace：quiver

## 目标

把 Quiver「夜色 + 等距像素办公室」这套高度自洽的游戏化监管台风格沉淀为可复用的设计资产：
深夜蓝径向舞台 + 冷文字三阶 + 单一琥珀暖强调 + 磨砂玻璃 HUD + 64×32 菱形瓦片 + 纯 CSS 像素工人精灵。

## 涉及条目（依赖拓扑序 · 16 条）

### tokens (4)
1. tokens/palettes/quiver/night-studio
2. tokens/typography/pairs/quiver/sf-system-duo
3. tokens/motion/quiver/pixel-steps
4. tokens/layout/quiver/iso-grid

### components (4)
5. components/avatars-icons/quiver/pixel-worker-sprite
6. components/buttons/quiver/lime-go-button
7. components/buttons/quiver/glass-chrome-button
8. components/indicators/quiver/autonomy-pill-badge

### blocks (5)
9.  blocks/layout/quiver/iso-office-world
10. blocks/nav/quiver/glass-topbar-hud
11. blocks/search/quiver/command-palette
12. blocks/feedback/quiver/world-ambience
13. blocks/display/quiver/glass-panel-modal

### page (1)
14. pages/dashboard/quiver/office-command-deck

### style (1) + product (1)
15. styles/experimental/quiver-night-studio
16. products/quiver

## 依赖关系

products/quiver → style: styles/experimental/quiver-night-studio
products/quiver → pages: [office-command-deck]
products/quiver → blocks: [iso-office-world, glass-topbar-hud, command-palette, world-ambience, glass-panel-modal]
products/quiver → components: [pixel-worker-sprite, lime-go-button, glass-chrome-button, autonomy-pill-badge]
products/quiver → tokens: {palette: night-studio, typography: sf-system-duo, motion: pixel-steps, layout: iso-grid}

styles/experimental/quiver-night-studio → uses [9,10,11,12,13,5,6,7,8] · refs.tokens {palette[1], typography[2]}
pages/dashboard/quiver/office-command-deck → uses [9,10,11,12,13]
blocks/layout/quiver/iso-office-world → uses [1,3,4,5]
blocks/nav/quiver/glass-topbar-hud → uses [1,2,6,7,8]
blocks/search/quiver/command-palette → uses [1,2]
blocks/feedback/quiver/world-ambience → uses [1,3]
blocks/display/quiver/glass-panel-modal → uses [1,2]
components/* → uses {tokens 1,3}

## 元信息填写方式

- AI 自动填：全部 16 条（用户授权 Y）
- 用户手填：无
- stack 统一：vanilla-css（React + 纯 CSS、无 Tailwind）
- 新增字典：aesthetic.pixel（zh=像素），已写入 style-vault/assets/taxonomy.json
- 决策：category=ai · style bucket=experimental

## 防重名 / 差异化（必写「与 X 区分」章节）

- night-studio palette ↔ mission-ops/deep-space-amber（深空琥珀·工程终端）+ tactical-hud/hud-cyan-glass（战术 HUD）
- glass-chrome-button ↔ components/buttons/.../ghost-button
- autonomy-pill-badge ↔ components/indicators/.../pulse-dot（点状家族）

## 双仓

VAULT_OK=true（~/Coding/Archer/style-vault · style-vault-site marker 校验通过）
preview tsx：12 个（4 token 中仅 palette 给 preview；typography/motion/layout token 按可选省略）

## 执行状态

☑ 用户已确认 · 待写入
