---
id: products/flywheel-inside
type: product
name: 飞轮的内部
description: media-studio 制片流水线的可视化讲解站 —— 一页滚到底讲清「一句灵感→一条成片」，孟菲斯滚动叙事脸
platforms: [web]
theme: light
category: content
tags:
  aesthetic: [brutalist, editorial]
  mood: [confident, energetic, playful]
  stack: [react-tailwind]
refs:
  style: styles/marketing-brand/memphis-scrolly-doc
preview: /preview/products/flywheel-inside
---

# 飞轮的内部

> 把一套自媒体制片流水线（media-studio）拆开摊给人看的单页讲解站——一页滚到底，讲清「一句灵感如何变成一条四平台成片」。已公开发布。

## 是什么

- **品类**：图文并茂的**讲解 / 文档站**（content），不是产品官网、不是后台
- **内容**：一条内容创作流水线的可视化拆解——五区生命周期、九阶段流水线（钉滚 signature）、完整 skill 地图、「剪视频→写文字」核心架构、品牌脸、飞轮闭环、真片案例
- **形态**：滚动叙事单页（11 节）+ 右侧 TOC + 顶部进度 + 一处钉滚交互
- **托管**：Vite build（`base:'./'` 相对路径）→ 个人 CDN 子目录 → `cdn.archeruuu.com/pages/media-studio/`

## 用什么脸

`refs.style` → [`styles/marketing-brand/memphis-scrolly-doc`](../../styles/marketing-brand/memphis-scrolly-doc/README.md)：孟菲斯撞色 + 新粗野硬卡 + 超粗黑大字 + 一个钉滚 signature。

signature 三件套 = 薄荷青眼 IP（黑猫）+ 黑粗大字 + 撞色背景。

## 复用价值

这个产品是"滚动叙事文档站"模板的**首个落地实例**。下次想写类似的图文讲解站、又不想用 docsify 时，直接复用它的 style + 底层 tokens/components/blocks，换 5 色板和 IP 即换脸、结构不动。

## 技术栈

Vite + React 18 + TypeScript（strict）+ Tailwind v4 + framer-motion。`@/` 别名；设计 token 在 `styles/index.css` 的 `@theme`，事实源 DTCG `tokens.dtcg.json`。
