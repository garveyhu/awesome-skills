---
id: blocks/display/studio-board/publish-hero
type: block
name: 发布成片 Hero
description: 详情页 signature 带——成片封面 16:9 + 封面自身色泼光晕 + kicker + 大标题 + 三交付统计(tabular-nums)；一屏一个记忆点
platforms: [web]
theme: both
tags:
  aesthetic: [editorial, glass]
  mood: [warm, confident]
  stack: [react-tailwind]
uses:
  - tokens/palettes/studio-board/warm-sand-ink
  - tokens/typography/pairs/studio-board/grotesk-han-plex
  - tokens/radius/studio-board/soft-sand-scale
preview: /preview/blocks/display/studio-board/publish-hero
---

# 发布成片 Hero

> 详情页主工作台顶部的整宽 signature 带（发布步）：左封面右文案，封面自身色泼一圈柔光晕到卡面，是全页**唯一强记忆点**，其余区域克制退让。

## 视觉特征

- **布局**：`relative px-7 pb-7 pt-6 · flex-col md:flex-row md:items-center md:gap-7`
- **封面 hero（左·300px）**：
  - 封面图 `aspect-video w-full rounded-xl border object-cover` + `shadow-[var(--shadow-lg)]`（柔暖大投影）
  - **泼色光晕**：封面自身作背景 `absolute -inset-6 rounded-[36px] bg-cover bg-center opacity-20 blur-[42px] saturate-150 scale-1.04`——把封面主色泼一圈到卡面，静态、低透明、无脉冲。signature 的「氛围」来源
  - 封面左下角浮 mono 标 `成片封面 · 16:9`（`bg-ink text-bg rounded-full px-2.5 py-1 text-[9.5px]` + 柔投影）
- **文案 + 统计（右）**：
  - **kicker**：`font-display text-[11px] font-semibold uppercase tracking-[0.16em] text-warning`（如「已完成 · 全矩阵同步」/「待发布 · 全矩阵同步」）
  - **大标题**：`font-display font-bold text-[clamp(20px,2.4vw,28px)] leading-[1.15] tracking-tight`
  - 一句母版说明 `text-[13px] leading-relaxed text-muted-strong max-w-[52ch]`，内嵌 mono `master.mp4`
  - **三交付统计**：`flex gap-x-8 gap-y-3`，每个 = 大数 `font-display text-[22px] font-bold tabular-nums` + 小单位 `text-[13px] text-muted`（如 `74.6MB` / `4/4` / `9/9`）+ 下方 label `text-[10.5px] text-muted`（母版大小 / 平台就绪 / 管线完成）
- 配色全走 workstation token，亮/暗自动跟

## 核心代码

```tsx
<section className="relative px-7 pb-7 pt-6">
  <div className="flex flex-col gap-6 md:flex-row md:items-center md:gap-7">
    <div className="relative w-full shrink-0 md:w-[300px]">
      <div aria-hidden className="pointer-events-none absolute -inset-6 z-0 rounded-[36px] bg-cover bg-center opacity-20 blur-[42px] saturate-150"
           style={{ backgroundImage:`url(${coverUrl})`, transform:'scale(1.04)' }} />
      <img src={coverUrl} className="relative z-[1] block aspect-video w-full rounded-xl border border-border object-cover shadow-[var(--shadow-lg)]" />
      <span className="absolute -bottom-2.5 left-3 z-[2] rounded-full bg-ink px-2.5 py-1 font-mono text-[9.5px] text-bg">成片封面 · 16:9</span>
    </div>
    <div className="relative z-[1] flex min-w-0 flex-col gap-3">
      <span className="font-display text-[11px] font-semibold uppercase tracking-[0.16em] text-warning">已完成 · 全矩阵同步</span>
      <h2 className="font-display text-[clamp(20px,2.4vw,28px)] font-bold leading-[1.15] tracking-tight text-ink">{title}</h2>
      <div className="flex flex-wrap gap-x-8 gap-y-3">{stats.map(Stat)}</div>
    </div>
  </div>
</section>
```

## 适配指南

- 泼色光晕的「氛围」来自封面本身色——无封面时退化为 `bg-surface/60` 占位，别硬造假光斑
- 统计数字必 `tabular-nums`（等宽对齐才「交付看板」）
- 一页只放这一个 hero 当 signature，其余区块保持信息密度但不抢戏

## 反模式

- 不要给泼色光晕加脉冲/循环（静态低透明才高级）
- 不要标题堆 900 超粗（clamp + bold 700 即够，克制）
- 不要多个 hero 并列抢 signature（一屏一个记忆点）
