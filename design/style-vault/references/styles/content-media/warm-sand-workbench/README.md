---
id: styles/content-media/warm-sand-workbench
type: style
name: 暖砂白玻璃工作台
description: 暖纸 editorial 底 × 产品级白玻璃 × 苔绿判成 × 暖近黑 CTA × 金陶土点睛 × feTurbulence 颗粒 × 大软圆角 × Grotesk×苹方 × liquid easeOut —— 亮暖砂 / 暗冷 slate 双态
platforms: [web]
theme: both
tags:
  aesthetic: [editorial, glass, minimal]
  mood: [warm, calm, confident]
  stack: [react-tailwind]
uses:
  - tokens/palettes/studio-board/warm-sand-ink
  - tokens/typography/pairs/studio-board/grotesk-han-plex
  - tokens/texture/studio-board/warm-paper-grain
  - tokens/motion/studio-board/liquid-ease
  - tokens/radius/studio-board/soft-sand-scale
  - components/display/studio-board/warm-glass-card
  - components/buttons/studio-board/ink-cta
  - components/tags-badges/studio-board/status-badge
  - components/indicators/studio-board/pipeline-status-light
  - components/toggles/studio-board/platform-pills
  - blocks/nav/studio-board/pipeline-rail
  - blocks/display/studio-board/publish-hero
  - blocks/media/studio-board/work-card
  - pages/dashboard/studio-board/workstation-detail
  - pages/landing/studio-board/channel-board-home
preview: /preview/styles/content-media/warm-sand-workbench
---

# 暖砂白玻璃工作台

> 「暖纸感编辑 × 克制产品 UI」的杂交脸：editorial 暖纸打底（呼吸、纸感、颗粒），产品级白玻璃 + 克制色阶做前景（精密、有层次）。既暖又稳，是媒体生产工具的一张自研实战脸。

## 视觉语言（signature 一览）

1. **暖砂/暖纸底 + 三层氛围**：暖砂 `#f0eeea`（详情）/ 奶油 `#f6f2e8`（首页）+ feTurbulence 细颗粒(.05·去塑料) + 金光弥散 + 细网格（[[warm-paper-grain]]）
2. **白磨砂玻璃卡**：真半透 + blur(30)saturate(140) + 亮边 + 顶 light-leak 高光 + 玻璃内高光 + **暖棕柔投影**（[[warm-glass-card]]）——signature 承载件
3. **苔橄榄绿判「成/已发布」**（`#5b8c5a`）+ **暖近黑主操作 CTA**（`#2a2620`·focus 不是蓝）+ 金/陶土副色 ≤5% 点睛（[[warm-sand-ink]] / [[ink-cta]] / [[status-badge]]）
4. **大软圆角**（详情 16–22·[[soft-sand-scale]]）+ **Grotesk×苹方×mono** 排版（mono 承重·[[grotesk-han-plex]]）
5. **liquid easeOut** `cubic-bezier(0.16,1,0.3,1)` 阻尼动效 + 克制微交互（[[liquid-ease]]）
6. **亮暖砂 / 暗冷 slate 双主题**——暗场不跟暖走、改冷中性
7. **两屏一体**：首页 board（奶油+细网格+作品流）+ 详情工作台（暖砂+四玻璃块），同源两温度档

## 与近邻区分

- **与 `styles/admin-console/waveflow-warm-engineer`（暖纸数据控制台）区分**：同是「暖纸 + 墨 + editorial」的暖底工具，但 waveflow = **平底 soft-card** + `blue-600` 单一 CTA + shadcn-radix + **仅亮**；本脸 = **白磨砂玻璃 + feTurbulence 颗粒** + **苔绿判成/暖近黑 CTA**（不是蓝）+ react-tailwind + **双主题**。一句话：waveflow 是「暖纸平面控制台」，本脸是「暖砂玻璃工作台」。
- **与 `flywheel`（飞轮日记频道内容品牌·memphis 撞色/纸板硬投影/scrolly landing）区分**：flywheel 是同一 media-studio 生态里的**内容脸**（对外发布物/落地页·孟菲斯撞色·900 黑大字·硬位移阴影），本脸是**工具壳**（生产看板 UI·暖砂玻璃·600 克制标题·柔暖投影）。**内容脸 vs 工具壳，两套系统别混用**。

## 适配指南

- 起同风格新产品：先冻结 5 token（palette/typography/texture/motion/radius），再取 warm-glass-card 当承载件、ink-cta 当主操作、status-badge/status-light 表状态
- 「工作/操作台」型页面用暖砂玻璃 + 大圆角 + 暖近黑 CTA；「内容/浏览」型页面（如首页）可切奶油亮底 + 细网格 + 冷蓝焦点
- 一屏一个 signature（如详情页的发布 Hero），其余克制退让
- 过 frontend-aesthetic AI 味自检：暖砂玻璃 + 真颗粒 + 苔绿 + 暖近黑，天然规避「紫靛渐变 / 满屏弥散光 / 科技霓虹」

## 反模式

- 不要纯白平底（要暖砂/奶油 + 颗粒）· 不要冷黑投影（要暖棕）
- 不要主 CTA 上品牌彩色（要暖近黑）· 不要苔绿铺底（判成语义点睛）
- 不要满屏玻璃叠玻璃（四大区块各一块）· 不要暗态沿用暖砂（改冷 slate）
