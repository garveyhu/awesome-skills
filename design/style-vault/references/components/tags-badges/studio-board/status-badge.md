---
id: components/tags-badges/studio-board/status-badge
type: component
name: 语义状态徽标
description: 描边 + surface 底 + 同色 mono 字的胶囊徽标(已完成/已发布=苔绿·待发布=金·错误=陶土·中性)；克制不喧宾
platforms: [web]
theme: both
tags:
  aesthetic: [minimal]
  mood: [calm, serious]
  stack: [react-tailwind]
uses:
  - tokens/palettes/studio-board/warm-sand-ink
preview: /preview/components/tags-badges/studio-board/status-badge
---

# 语义状态徽标

> 状态一眼可辨的胶囊徽标：**描边 + surface 底 + 同色 mono 字**，不用实底色块（克制、不抢）。苔绿判成、金待发布、陶土错误、中性默认。

## 视觉特征

- **结构**：`rounded-full · border · px-2 py-0.5 · font-mono · text-[11px] · font-bold · leading-5`——胶囊 + 等宽小字
- **四态（描边 + surface 底 + 同色字）**：
  - `success`（已完成/已发布）：`border-success bg-surface text-success`——**苔橄榄绿**
  - `warning`（待发布/进行中）：`border-warning bg-surface text-warning`——金
  - `risk`（错误/冲突）：`border-risk bg-surface text-risk`——陶土
  - `neutral`（默认）：`border-border bg-surface text-muted-strong`
- **软填变体**（如状态胶囊/计数）：`border-{tone}/40 bg-{tone}/10 text-{tone}`——极淡同色填充 + 描边，更柔（用于步头状态胶囊、进度计数 `9/9`）
- **关键**：底永远是 `surface`（暖白）或极淡同色，**不用饱和实底**——徽标是标记不是按钮，克制才产品感

## 核心代码

```tsx
const BASE = 'inline-flex items-center rounded-full border px-2 py-0.5 font-mono text-[11px] font-bold leading-5';
const TONE = {
  neutral: 'border-border bg-surface text-muted-strong',
  warning: 'border-warning bg-surface text-warning',
  risk:    'border-risk bg-surface text-risk',
  success: 'border-success bg-surface text-success',
};
// 软填变体（步头/计数）：
// success 'border-success/30 bg-success/10 text-success'
```

## 适配指南

- 判「成/发布」永远 `success`（苔绿），与管线完成节点同一语义色，全站一致
- 描边式（`bg-surface`）用于独立徽标；软填式（`bg-{tone}/10`）用于紧贴内容的状态胶囊/计数
- 徽标字用 mono，与元信息体系统一

## 反模式

- 不要饱和实底徽标（那像小按钮，抢主操作）
- 不要用黄底黑字这种高对比警示色（本套走描边同色、克制）
- 不要正文字体做徽标（要 mono）
