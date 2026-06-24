---
id: components/display/flywheel/hard-shadow-card
type: component
name: 硬阴影卡
description: 2.5px 粗黑描边 + 6px/3px 硬位移阴影 + 米白底的孟菲斯基础卡，全站最常复用的承载件
platforms: [web]
theme: light
tags:
  aesthetic: [brutalist]
  mood: [confident, playful]
  stack: [react-tailwind]
uses:
  - tokens/palettes/flywheel/memphis-collision
  - tokens/shadow/flywheel/hard-offset-stack
preview: /preview/components/display/flywheel/hard-shadow-card
---

# 硬阴影卡

> 2.5px 粗黑描边 + 6px 硬位移阴影 + 米白底——这套脸的"砖块"，几乎每个区块都由它垒成

## 视觉特征

- 大号 `.card-hard`：`border-[2.5px] border-ink` + `shadow-[6px_6px_0_#1A1A1A]` + `bg-paper`（#FFF8EC）
- 小号 `.card-hard-sm`：同描边 + `shadow-[3px_3px_0_#1A1A1A]`（次级 / 内嵌）
- signature 强调卡：阴影换 `shadow-[6px_6px_0_#16C79A]`（薄荷青）——一屏只给一个
- 撞色头卡：卡内顶部加一条撞色 bar（`bg-yellow/blue/mint` + 黑字），下半 `bg-paper`
- 内距 `p-4 ~ p-6`；卡内小标签用 `border-[1.5px] border-ink/30 bg-paper-2` 等宽小字
- hover（可点卡）：`transition-transform hover:-translate-y-0.5`，阴影显"变厚"，**不改模糊**

## 与同 bucket 区分

- **vs 任意 `shadow-md` 软卡**：本条**只用硬位移阴影 + 粗描边**，立体来自硬边；软阴影卡是另一种视觉语言，不混用
- **vs `blocks/display/flywheel/layered-atlas-grid`**：那条是"多张硬卡 + 撞色头"的网格布局块；本条是单张卡原子，被它复用

## 核心代码

```tsx
import { type ReactNode } from 'react';

interface HardCardProps {
  children: ReactNode;
  size?: 'lg' | 'sm';
  /** 薄荷青 signature 阴影（一屏一个） */
  signature?: boolean;
  className?: string;
}

export function HardCard({ children, size = 'lg', signature, className }: HardCardProps) {
  const shadow = signature
    ? 'shadow-[6px_6px_0_#16C79A]'
    : size === 'lg'
      ? 'shadow-[6px_6px_0_#1A1A1A]'
      : 'shadow-[3px_3px_0_#1A1A1A]';
  return (
    <div className={`border-[2.5px] border-ink bg-paper ${shadow} ${className ?? ''}`}>
      {children}
    </div>
  );
}
```

或纯 CSS（`@layer components`）：

```css
.card-hard    { border: 2.5px solid var(--color-ink); box-shadow: 6px 6px 0 var(--color-ink); background: var(--color-paper); }
.card-hard-sm { border: 2.5px solid var(--color-ink); box-shadow: 3px 3px 0 var(--color-ink); background: var(--color-paper); }
```

## 适配指南

- 嵌套时外卡 6px、内卡 3px，避免阴影互相打架
- 撞色头卡：`<div class="bg-yellow border-b-[2.5px] border-ink p-5">头</div><div class="bg-paper p-5">体</div>`
- signature 卡同屏 ≤ 1
- 卡之间留够间距（阴影占 6px，gap ≥ 16px 不然阴影压到邻卡）

## 反模式

- ❌ 用 `rounded-2xl shadow-md`（软卡，破坏 brutalist）
- ❌ 描边低于 2px 或非实心（变软）
- ❌ 满屏 signature 薄荷青阴影（强调失效）
- ❌ 卡底用纯白（要 paper 米白）
