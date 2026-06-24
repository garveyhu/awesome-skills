---
id: styles/marketing-brand/memphis-scrolly-doc
type: style
name: 孟菲斯滚动叙事文档站
description: 把图文并茂的讲解做成滚动叙事单页的 brutalist/Memphis 风格 —— 撞色硬卡 + 超粗黑大字 + 一个钉滚 signature，docsify 替代
platforms: [web]
theme: light
tags:
  aesthetic: [brutalist, editorial]
  mood: [confident, energetic, playful]
  stack: [react-tailwind]
uses:
  - blocks/layout/flywheel/numbered-section-shell
  - blocks/nav/flywheel/toc-scroll-rail
  - blocks/marketing/flywheel/scroll-pinned-spine
  - blocks/display/flywheel/layered-atlas-grid
  - components/display/flywheel/hard-shadow-card
  - components/typography-atoms/flywheel/kicker-collision-mark
  - components/indicators/flywheel/scroll-progress-bar
refs:
  tokens:
    palette: tokens/palettes/flywheel/memphis-collision
    typography: tokens/typography/pairs/flywheel/han-black-grotesk
    shadow: tokens/shadow/flywheel/hard-offset-stack
    motion: tokens/motion/flywheel/reveal-pin-scroll
preview: /preview/styles/marketing-brand/memphis-scrolly-doc
---

# 孟菲斯滚动叙事文档站

> 一张"脸"：用滚动叙事 + 交互把图文讲解做成体验，而非 markdown 阅读器。孟菲斯撞色 + 新粗野硬卡 + 超粗黑大字 + 一个钉滚 signature。**想写讲解型文档站、又不想用 docsify 时复用它**

## 这张脸是什么

- **气质**：鲜艳孟菲斯撞色 + 新粗野（brutalist）——有冲击、有活力、有专业骨；不是暗场冷淡、也不是 markdown 性冷淡
- **signature 三件套**：薄荷青锐利强调（IP 眼睛色）+ 黑粗大字 + 撞色背景，一刷就认出
- **核心信条**：① 冻结 design token（5 色板 / 字体 / 硬阴影），组件零硬编码、换 token 换脸 ② 整页只造**一个 signature moment**（钉滚脊梁穿行），其余克制留白让路 ③ 一次高质量进场编排 > 满屏微交互 ④ 超粗黑大字主导 + 撞色点睛 + 硬阴影卡承载

## 组成（uses / refs）

- **底层 token**：`memphis-collision`（撞色板）+ `han-black-grotesk`（思源黑 900 字栈）+ `hard-offset-stack`（硬阴影 + 粗边）+ `reveal-pin-scroll`（进场 + 钉滚 + scroll-spy + 进度）
- **原子/件**：`hard-shadow-card`（砖块）+ `kicker-collision-mark`（节标签 + 撞色高亮）+ `scroll-progress-bar`（顶部进度）
- **块**：`numbered-section-shell`（章节模具）+ `toc-scroll-rail`（右侧目录）+ `scroll-pinned-spine`（★signature）+ `layered-atlas-grid`（分层信息网格）
- **页**：`pages/landing/flywheel/scrolly-explainer-doc`（一页到底的编排）

## 适用 / 不适用

- **适用**：讲解流程 / 数据流动 / 架构 / 闭环 / 方法论这类"动态、有分支、有脊梁穿行"的图文内容；想要图文并茂 + 交互 + 强品牌、又不想用 docsify
- **不适用**：纯参考手册（改一行 md 就更新 → 用 docsify/wiki）；海量多路由文档库（这套是单页叙事）；性冷淡极简产品文档

## 换脸指南

- 换 `memphis-collision` 的 5 主色 = 换风格基调；换 `han-black-grotesk` 的 display 字体（保持 ≥900 字重）= 换性格；结构/排版/交互范式不动
- IP 角色可替换（任意吉祥物/插画），但要冻结、跨内容一致

## 反模式（过 frontend-aesthetic 自检）

- ❌ 紫→靛渐变兜底 / 满屏毛玻璃 / emoji 当图标 / Inter·系统字兜底
- ❌ 多个 signature moment / 配色均分无主撞色 / 背景纯色无氛围
- ❌ 软阴影卡 / 标题非 900 黑体 / 文案散写不进数据层
