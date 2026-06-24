---
id: pages/landing/flywheel/scrolly-explainer-doc
type: page
name: 滚动叙事单页文档站
description: 一页到底的图文并茂讲解站 —— Memphis hero + N 个序号 section + 钉滚 signature + 右侧 TOC + 进度条，docsify 的替代
platforms: [web]
theme: light
tags:
  aesthetic: [brutalist, editorial]
  mood: [confident, energetic, playful]
  stack: [react-tailwind]
uses:
  - tokens/palettes/flywheel/memphis-collision
  - tokens/typography/pairs/flywheel/han-black-grotesk
  - tokens/shadow/flywheel/hard-offset-stack
  - tokens/motion/flywheel/reveal-pin-scroll
  - components/indicators/flywheel/scroll-progress-bar
  - blocks/layout/flywheel/numbered-section-shell
  - blocks/nav/flywheel/toc-scroll-rail
  - blocks/marketing/flywheel/scroll-pinned-spine
  - blocks/display/flywheel/layered-atlas-grid
preview: /preview/pages/landing/flywheel/scrolly-explainer-doc
---

# 滚动叙事单页文档站

> 把一份图文并茂的讲解做成"一页滚到底"的叙事站——不用 docsify，用 React 把流程/数据流动/闭环讲成可交互体验。整页 = Memphis hero + N 个序号 section + 一处钉滚 signature + 右侧 TOC + 顶部进度

## 页面骨架（从上到下）

1. **顶部进度条**（`scroll-progress-bar`）：薄荷青 scaleX，全程钉顶
2. **右侧 TOC 导航**（`toc-scroll-rail`）：悬浮硬阴影卡，首页隐藏、滚进正文淡入，scroll-spy 高亮
3. **Hero（`id="top"`）**：满屏撞色底（常用活力黄）+ 点阵 + 散落孟菲斯几何（旋转方块/圆/菱形带硬阴影）；左列超粗大标题（`一句话 → 一条结论`，mark 点睛）+ kicker 徽标 + 引言 + 硬阴影 CTA；右列 IP 角色漂浮 + 标签牌；底部"向下滚动 ↓"提示
4. **若干静态 section**（`numbered-section-shell`）：背景 paper / paper-2 / graph 交替；内容多用 `layered-atlas-grid`（分层信息）、双列对比卡、骨架/spotlight 卡
5. **一处钉滚 signature**（`scroll-pinned-spine`）：暗场，滚动演一条流程，整页唯一记忆点
6. **页脚**：暗场 `bg-ink` + IP + 大号 slogan + 来源说明 + 标签

## 视觉要点

- **背景节奏**：相邻 section 背景在 paper / paper-2 / graph(方格) 间交替，暗场（pipeline / footer）插在中间，避免一片米白
- **一个 signature moment**：只有钉滚脊梁那节是交互重头，其余克制留白，给它让路
- **进场编排**：每节头区 + 卡片 whileInView 淡入上移（`once`），错峰 `delay i*0.06`
- **超粗黑大字**主导，撞色块点睛，硬阴影卡承载——signature 三件套一刷就认出
- 全宽出血背景 + `max-w-6xl` 居中内容
- 技术栈 Vite + React + TS + Tailwind v4 + framer-motion；`base:'./'` 相对路径，可丢 CDN 子目录托管

## 与同 bucket 区分

- **vs docsify / 传统文档主题**：那是 markdown 阅读器（侧栏 + 正文）；本条是**滚动叙事 + 交互 signature**的单页，讲流程/数据流动/闭环这类"动态"内容
- **vs 普通 landing page**：本条是"用 landing 技法做文档/讲解"——有 hero/scrollytelling 的能量，但内容是教学/拆解，章节序号化、有 TOC

## 数据驱动

讲解文案收在一处 `data/*.ts`（section 列表、各 section 数据），组件零散写；section 锚点表（`{id,num,label}`）喂 TOC 导航，与各 section `id` 一一对应。换内容改数据、组件不动。

## 适配指南

- 章节数建议 6–11；超过加分组，TOC 才不太长
- signature 节放中段（读者已进入），不放首屏（首屏是 hero）
- 大图/媒体走静态资源相对路径（`./...`），配合 `base:'./'` 上 CDN
- 暗场节（signature / footer）用同套 token 反相，浮层（TOC）务必带背板

## 反模式

- ❌ 多个 signature moment（散，记不住）
- ❌ 背景全 paper 不交替（单调）
- ❌ 首屏就堆交互（hero 该是强排版 + 一个 CTA）
- ❌ 文案散写进组件（应收 data 层，便于改/复用）
- ❌ 命中 frontend-aesthetic 自检：紫靛渐变 / 满屏毛玻璃 / emoji 当图标 / Inter 系统字 / 居中三等卡 / 配色均分
