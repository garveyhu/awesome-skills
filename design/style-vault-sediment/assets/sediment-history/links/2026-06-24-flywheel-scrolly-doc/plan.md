# 沉淀计划 · 飞轮的内部 · 孟菲斯滚动叙事文档站

日期：2026-06-24
作者：links
模式：create
起点：from-project（~/Documents/wiki/media-studio · 已公开发布 cdn.archeruuu.com/pages/media-studio/）
档位：Tier 2 · 基础级（目标 12–18 · 实际 14 条）

## 目标
把「滚动叙事单页文档站」的结构 + 视觉体系沉淀成可复用模板——下次写图文并茂讲解型文档站、不想用 docsify 时直接复用。孟菲斯撞色脸可换，结构/排版/交互范式是骨架。

## 技术栈指纹
react-tailwind（Vite + React 18 + TS + Tailwind v4 + framer-motion）· base 相对路径

## 涉及条目（依赖拓扑序 · namespace=flywheel）
1. tokens/palettes/flywheel/memphis-collision
2. tokens/typography/pairs/flywheel/han-black-grotesk
3. tokens/shadow/flywheel/hard-offset-stack
4. tokens/motion/flywheel/reveal-pin-scroll
5. components/display/flywheel/hard-shadow-card
6. components/typography-atoms/flywheel/kicker-collision-mark
7. components/indicators/flywheel/scroll-progress-bar
8. blocks/layout/flywheel/numbered-section-shell
9. blocks/nav/flywheel/toc-scroll-rail
10. blocks/marketing/flywheel/scroll-pinned-spine
11. blocks/display/flywheel/layered-atlas-grid
12. pages/landing/flywheel/scrolly-explainer-doc
13. styles/marketing-brand/memphis-scrolly-doc
14. products/flywheel-inside

## 依赖关系
flywheel-inside → memphis-scrolly-doc → [8,9,10,11,5,6,7] → refs tokens[1,2,3,4]

## 元信息填写方式
- AI 自动填（Y 授权）：全部 14 条
- 用户手填：无

## 执行状态
☑ 用户已确认 · 待写入
