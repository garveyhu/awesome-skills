---
id: styles/experimental/quiver-night-studio
type: style
name: Quiver 夜色像素工作室
description: 用治愈的等距像素游戏世界皮肤化一个严肃 AI agent 监管台——夜色 + 单一暖强调 + 磨砂玻璃 chrome 的设计语言
platforms: [web]
theme: dark
tags:
  aesthetic: [pixel, retro, glass]
  mood: [calm, playful, nostalgic]
  stack: [vanilla-css]
uses:
  - blocks/layout/quiver/iso-office-world
  - blocks/nav/quiver/glass-topbar-hud
  - blocks/search/quiver/command-palette
  - blocks/feedback/quiver/world-ambience
  - blocks/display/quiver/glass-panel-modal
  - components/avatars-icons/quiver/pixel-worker-sprite
  - components/buttons/quiver/lime-go-button
  - components/buttons/quiver/glass-chrome-button
  - components/indicators/quiver/autonomy-pill-badge
  - tokens/palettes/quiver/night-studio
  - tokens/typography/pairs/quiver/sf-system-duo
  - tokens/motion/quiver/pixel-steps
  - tokens/layout/quiver/iso-grid
preview: /preview/styles/experimental/quiver-night-studio
---

# Quiver 夜色像素工作室

> 把「监管一群无头编码 agent」这件严肃的事，皮肤化成一间整夜亮灯的等距像素办公室——功能没削，但你是在「看公司」而不是「读 dashboard」

## 视觉特征（风格主张）

- **夜色 + 唯一暖强调**：深夜蓝径向舞台（不是平涂暗底），全局冷文字 + 状态色，**只留琥珀 `#ffd27a` 一处暖**当温度锚点（台灯/选中/聚焦/王冠）；行动/成功另用「青柠绿」
- **世界即界面**：核心是一间 13×9 等距像素办公室（纯 DOM 体素，非 canvas/引擎），房间靠地板 tint + 灯光冷暖分区，「楼」就是功能入口——点运维楼开预算、点质检台开追溯
- **像素角色承载状态**：一任务 = 一工位像素小人（CSS 手搓、变量换肤），敲键/走位/思考/庆祝全用 `steps()` 跳帧；经理戴王冠、审计戴护目镜
- **玻璃 chrome 浮在世界上**：HUD / 命令面板 / 模态全是磨砂玻璃（`blur(13px) saturate(1.25)` + 白色低 alpha 发丝边 + 顶部高光），悬浮但不夺戏
- **氛围即反馈**：夜色整夜呼吸、预算逼近上限全场转冷转暗临界亮红边、交付时刻边缘泛绿/泛红——抽象状态翻成体感
- **signature moment**：那间**活着的等距像素办公室**——小人在工位敲键、灯随机明灭、窗外月光斜射、猫蜷在地上。其余 chrome 全部克制退让给这一个世界
- **性能即设计**：失焦冻结全动画、LED 由 JS 低频随机驱动、颗粒静态缓存——「活」与「不烧电」同时成立

## Tokens（聚合）

- 调色板：[`tokens/palettes/quiver/night-studio`](../../../tokens/palettes/quiver/night-studio.md)
- 字体对：[`tokens/typography/pairs/quiver/sf-system-duo`](../../../tokens/typography/pairs/quiver/sf-system-duo.md)
- 动效：[`tokens/motion/quiver/pixel-steps`](../../../tokens/motion/quiver/pixel-steps.md)
- 等距网格：[`tokens/layout/quiver/iso-grid`](../../../tokens/layout/quiver/iso-grid.md)

## 适配指南

- 想复用这套风格做别的「监管/编排类」工具：保留「世界即界面 + 单一暖强调 + 玻璃 chrome + 像素角色承载状态」四件套，换房间语义即可
- 严守颜色分工：琥珀=氛围/焦点，青柠绿=行动/运转，状态色只做语义；不引第三种暖色
- 一屏只造一个 signature（那个世界），chrome 一律退让

## 反模式

- 不要加传统侧栏/tab 导航——破坏「这是世界不是后台」的核心错觉
- 不要把像素世界做成静态贴图——它的魅力在「活着」（小人、灯、光、猫），但活要走低开销路径
- 不要把暖强调铺开——琥珀是点睛的唯一暖，泛用即廉价
