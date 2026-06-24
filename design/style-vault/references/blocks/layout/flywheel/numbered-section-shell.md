---
id: blocks/layout/flywheel/numbered-section-shell
type: block
name: 序号 Section 外壳
description: 全宽背景层 + 居中内容 + 序号 kicker + 超粗大标题 + 进场揭示的章节外壳，整页由它复用拼成
platforms: [web]
theme: light
tags:
  aesthetic: [brutalist, editorial]
  mood: [confident, energetic]
  stack: [react-tailwind]
uses:
  - tokens/palettes/flywheel/memphis-collision
  - tokens/typography/pairs/flywheel/han-black-grotesk
  - tokens/motion/flywheel/reveal-pin-scroll
  - components/typography-atoms/flywheel/kicker-collision-mark
preview: /preview/blocks/layout/flywheel/numbered-section-shell
---

# 序号 Section 外壳

> 滚动叙事文档站的"章节模具"：全宽背景层 + 居中内容 + 序号 kicker + 超粗大标题 + 进场揭示。整页就是 N 个它

## 视觉特征

- **两层结构**：外层 `<section>` 全宽承背景（`bg-paper` / `bg-paper-2` / `bg-graph` 点阵），内层 `mx-auto max-w-6xl px-6 py-24 md:py-32` 居中内容——背景全宽出血、内容收窄
- **背景层次**交替：相邻 section 用 paper / paper-2 / graph(方格纸) 错开，避免一片米白单调；signature 暗场用 `bg-ink`
- **头区**（whileInView 揭示）：序号圆（`h-9 w-9 rounded-full border-[2.5px] border-ink bg-ink text-mint`）+ mono kicker，下面 `heading-xl text-4xl md:text-6xl`（思源黑 900），再下 `max-w-2xl text-lg text-ink-soft` 引言
- 标题里用 `mark-mint` / `mark-yellow` 点关键词
- 进场：头区 `initial opacity:0 y:28 → whileInView · 0.6s · once`

## 与同 bucket 区分

- **vs 任意通用 Section 容器**：本条把"全宽背景 + 居中内容 + 序号 kicker + 超粗标题 + 进场揭示"**固化成一个模具**，传 `index/kicker/title/intro/bg` 即出一节；不是裸 `<section>`
- **vs `blocks/marketing/flywheel/scroll-pinned-spine`**：那条是带钉滚交互的 signature 节；本条是**静态承载节**（90% 的节用它），signature 节是特例

## 核心代码

```tsx
import { type ReactNode } from 'react';
import { motion } from 'framer-motion';

type Bg = 'paper' | 'paper-2' | 'graph';
const BG: Record<Bg, string> = {
  paper: 'bg-paper',
  'paper-2': 'bg-paper-2',
  graph: 'bg-paper bg-graph',
};

export function Section({ id, index, kicker, title, intro, children, bg = 'paper' }: {
  id: string; index: string; kicker: string;
  title: ReactNode; intro?: ReactNode; children: ReactNode; bg?: Bg;
}) {
  return (
    <section id={id} className={`relative w-full ${BG[bg]}`}>
      <div className="mx-auto w-full max-w-6xl px-6 py-24 md:py-32">
        <motion.div
          initial={{ opacity: 0, y: 28 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-80px' }}
          transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
        >
          <div className="mb-3 flex items-center gap-3">
            <span className="flex h-9 w-9 items-center justify-center rounded-full border-[2.5px] border-ink bg-ink font-mono text-sm font-bold text-mint">{index}</span>
            <span className="font-mono text-[0.72rem] uppercase tracking-[0.18em] text-ink-soft">{kicker}</span>
          </div>
          <h2 className="mb-6 text-4xl font-black leading-[0.98] tracking-[-0.02em] text-ink md:text-6xl">{title}</h2>
          {intro && <div className="mb-12 max-w-2xl text-lg leading-relaxed text-ink-soft md:text-xl">{intro}</div>}
        </motion.div>
        {children}
      </div>
    </section>
  );
}
```

`.bg-graph` = 双向 `linear-gradient` 方格纸（32px）；`.bg-dotgrid` = `radial-gradient` 点阵（22px）。

## 适配指南

- 背景交替排：常用 paper → graph → paper-2 → paper… 让滚动有节奏
- 序号用两位（`01`…`10`）+ kicker 英文大写副中文，全站统一
- 内容宽度 `max-w-6xl`（1152px）居中；引言 `max-w-2xl` 更窄好读
- 暗场节单独 `bg-ink` + 文字反相（见 signature 节），但仍套这个头区范式

## 反模式

- ❌ 背景色只盖居中列不出血（必须外层全宽承背景、内层收窄）
- ❌ 相邻节全用纯 paper（单调，要交替）
- ❌ 标题不上 900 字重 / 不用 mark 点睛（失去冲击）
- ❌ 进场不设 `once`（回滚重放廉价）
