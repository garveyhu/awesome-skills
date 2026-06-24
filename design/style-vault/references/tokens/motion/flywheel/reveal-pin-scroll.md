---
id: tokens/motion/flywheel/reveal-pin-scroll
type: token
name: 进场揭示 + 钉滚动效体系
description: framer-motion 一套 —— whileInView 进场揭示 + 钉滚脊梁穿行 + scroll-spy + 顶部进度，克制不堆
platforms: [web]
theme: light
tags:
  aesthetic: [brutalist, editorial]
  mood: [energetic, confident]
  stack: [react-tailwind]
preview: /preview/tokens/motion/flywheel/reveal-pin-scroll
---

# 进场揭示 + 钉滚动效体系

> 一次高质量的滚动编排 > 到处撒微交互。四件套：进场揭示 / 钉滚脊梁 / scroll-spy / 进度条

## 视觉特征

- **进场揭示（reveal）**：`initial={{opacity:0, y:28}} whileInView={{opacity:1, y:0}} viewport={{once:true, margin:'-80px'}} transition={{duration:0.6, ease:[0.22,1,0.36,1]}}` —— 每节/每卡入视淡入上移，`once` 只放一次。卡片列表按 `delay:i*0.06~0.1` 错峰
- **钉滚脊梁（pinned scroll）**：外层 `~520vh` 高容器 + 内层 `sticky top-0 h-screen`；`useScroll({target, offset:['start start','end end']})` → `useTransform(progress,[0,1],['0%','100%'])` 驱动进度填充 + 令牌横移；`useMotionValueEvent` 把 progress 离散成"当前阶段"切详情卡
- **scroll-spy 导航**：`IntersectionObserver`，`rootMargin:'-48% 0px -48% 0px'`（视口中线窄带）——任一时刻只有一个 section 跨中线 = 高亮当前
- **顶部进度条**：`useScroll().scrollYProgress` + `useSpring(…,{stiffness:120,damping:30})` → `scaleX` origin-left
- **漂浮（float）**：IP 图标 `animate={{y:[0,-10,0]}} transition={{duration:4, repeat:Infinity}}`
- 全局 `prefers-reduced-motion` 关动画

## Tokens

```json
{
  "reveal": "opacity 0→1, y 28→0 · 0.6s · cubic-bezier(0.22,1,0.36,1) · whileInView once",
  "stagger": "delay i*0.06–0.1",
  "pin-track-vh": 520,
  "spy-rootmargin": "-48% 0px -48% 0px",
  "progress-spring": "stiffness 120 · damping 30 · mass 0.4",
  "float": "y [0,-10,0] · 4s loop infinite",
  "ease": "[0.22, 1, 0.36, 1]"
}
```

依赖 framer-motion（`useScroll/useTransform/useMotionValueEvent/useSpring/whileInView`）。

## 适配指南

- **signature moment 只一个**：整页只造一处钉滚脊梁交互，其余只用低调的 reveal，给它让路
- 进场用 `once:true`——回滚不重放，避免廉价感
- 钉滚容器高度按"每阶段约 50–60vh × 阶段数"算；阶段切换详情卡用 keyed `motion.div` 重渲（不用 `AnimatePresence mode=wait`，长跳会留空白）
- scroll-spy 用中线窄带 rootMargin，对超高钉滚 section 也成立
- 缺 framer-motion 的环境降级：reveal 用 CSS `@keyframes` + IntersectionObserver

## 反模式

- ❌ 满屏微交互无重点（违反"一个 signature moment"）
- ❌ 进场不设 `once`，来回滚反复抖
- ❌ `AnimatePresence mode="wait"` 做 scroll 步进卡（快跳会空帧）
- ❌ 忽略 `prefers-reduced-motion`
- ❌ 用过长的平滑 `scroll-behavior:smooth` 跳超远距离（扫屏眩晕）
