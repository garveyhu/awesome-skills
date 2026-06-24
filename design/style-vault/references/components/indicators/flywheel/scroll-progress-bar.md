---
id: components/indicators/flywheel/scroll-progress-bar
type: component
name: 顶部滚动进度条
description: 固定顶栏的薄荷青 scaleX 阅读进度条，useScroll + useSpring 平滑跟随
platforms: [web]
theme: light
tags:
  aesthetic: [brutalist, minimal]
  mood: [confident]
  stack: [react-tailwind]
uses:
  - tokens/palettes/flywheel/memphis-collision
  - tokens/motion/flywheel/reveal-pin-scroll
preview: /preview/components/indicators/flywheel/scroll-progress-bar
---

# 顶部滚动进度条

> 钉在视口顶部的一条薄荷青进度条，随全页滚动进度从左生长——长文/滚动叙事的阅读锚

## 视觉特征

- `fixed left-0 top-0 z-50 h-1.5 w-full`，`bg-mint`（#16C79A · signature 色）
- `transform-origin: left`，用 `scaleX` 从 0→1 生长（**不是改 width**，性能好）
- 进度值 `useScroll().scrollYProgress` 经 `useSpring(…,{stiffness:120, damping:30, mass:0.4})` 平滑——直接绑 raw 会"跳"，spring 后丝滑
- 高度 6px（`h-1.5`），细而醒目；色就是品牌 signature 色，不另选

## 与同 bucket 区分

- **vs 钉滚脊梁里的"阶段进度填充"**（`blocks/marketing/flywheel/scroll-pinned-spine`）：那条是**单个 section 内**的局部进度（脊梁线填充）；本条是**全页**阅读进度，钉在最顶

## 核心代码

```tsx
import { motion, useScroll, useSpring } from 'framer-motion';

export function ScrollProgress() {
  const { scrollYProgress } = useScroll();
  const scaleX = useSpring(scrollYProgress, { stiffness: 120, damping: 30, mass: 0.4 });
  return (
    <motion.div
      style={{ scaleX }}
      className="fixed left-0 top-0 z-50 h-1.5 w-full origin-left bg-mint"
    />
  );
}
```

## 适配指南

- 进度色用 signature accent（mint），让"读到哪了"和品牌色绑定
- `z-50` 压在内容上、但低于模态；和右侧 TOC 导航不冲突
- 缺 framer-motion 时降级：监听 `scroll` 事件算 `scrollTop/scrollHeight` 直接设 `scaleX`（无 spring，略生硬）

## 反模式

- ❌ 改 `width` 而非 `scaleX`（触发 layout，卡）
- ❌ 不加 spring（进度跳变、廉价）
- ❌ 进度条太粗（> 8px 抢视觉）或用非品牌色
