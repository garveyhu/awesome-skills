---
id: pages/landing/studio-board/channel-board-home
type: page
name: 频道 Board 首页
description: 奶油纸底 + 细网格上的频道主页——sticky 顶栏(logo+频道+搜索+平台pills) + banner + 头像左下叠 + 关注/粉丝/获赞 + 投稿 tabs + 2~6 列作品网格
platforms: [web]
theme: light
tags:
  aesthetic: [editorial, minimal]
  mood: [warm, calm]
  stack: [react-tailwind]
uses:
  - components/toggles/studio-board/platform-pills
  - blocks/media/studio-board/work-card
  - tokens/palettes/studio-board/warm-sand-ink
  - tokens/typography/pairs/studio-board/grotesk-han-plex
  - tokens/texture/studio-board/warm-paper-grain
preview: /preview/pages/landing/studio-board/channel-board-home
---

# 频道 Board 首页

> 奶油纸底 + 48px 细网格 + 冷蓝径向高光上，仿各平台个人空间的频道主页：头图 → 头像左下叠 → 数据 → 投稿网格。四平台各自主页组件（B 站/YT/抖音/小红书按各自版式）。

## 页面骨架

- **底**：`body` 奶油渐变 `#fbf8f0→#f6f2e8` + 48px 细网格（横竖 1px `ink 4%`）+ 右上冷蓝径向高光（[[warm-paper-grain]] 的 board 变体）；页面容器 `bg-surface/40`
- **① sticky 顶栏**（`sticky top-0 z-30 bg-paper/85 backdrop-blur px-6 py-2.5`）：左 = logo + `·` + 频道名 pill(`rounded-full border px-2.5 py-1 text-xs font-bold` + `▾`)；右 = 搜片(收纳图标·展开筛选) + [[platform-pills]] 四平台切换
- **② 频道头**（以 B 站版为例）：
  - banner `h-32 w-full`（bannerStyle 渐变）
  - **头像左下叠**：`Avatar h-24 w-24 border-4 border-paper shadow-lg`，`-mt-10` 压在 banner 下沿
  - 频道名 `font-display text-2xl font-black` + bio/slogan `text-[13px] text-ink-soft`
  - **数据行**：关注 / 粉丝 / 获赞（ProfileStats，`mt-3`）
  - **投稿 tabs**：主页/投稿/合集/动态/收藏（ProfileTabs，`mt-4 border-b border-ink-soft/15`，激活项蓝下划线）
- **③ 作品网格**：`grid grid-cols-2 sm:3 lg:4 xl:5 2xl:6 · gap-x-4 gap-y-6 py-6`，单元 = [[work-card]]
- **空态**：`mx-auto mt-16 max-w-md rounded-xl border border-dashed border-ink-soft/30 px-4 py-12 text-center text-sm text-ink-soft`（还没有作品 / 没有符合筛选的片）
- **视觉要点**：多平台一套数据、各出各的主页版式；顶栏平台激活态染品牌色；整体比详情页密度更高、圆角更收（board 圆角阶）

## 适配指南

- 首页走奶油亮底 + 细网格（工程台秩序），比详情页更亮更暖；焦点用冷蓝做链接/激活高光（区别于详情页的暖近黑主操作）
- 头像 `border-4 border-paper` 压 banner 下沿是「个人空间」范式的招牌，别改成居中
- 作品网格响应式列数 2→6，`gap-y` 比 `gap-x` 大（纵向留呼吸）

## 反模式

- 不要首页也上白玻璃 + 颗粒（那是详情页脸；首页走奶油 + 细网格）
- 不要 banner 头像居中堆叠（要头像左下叠的个人空间范式）
- 不要网格卡加重投影/描边（纸感封面靠图本身）

## 引用关系

- uses：platform-pills · work-card · warm-sand-ink · grotesk-han-plex · warm-paper-grain
- used by：`styles/content-media/warm-sand-workbench` · `products/studio-board`
