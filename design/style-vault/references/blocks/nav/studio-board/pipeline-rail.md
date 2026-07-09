---
id: blocks/nav/studio-board/pipeline-rail
type: block
name: 生产管线脊柱轨
description: 左栏白玻璃管线导航——创意/制作分组 + 串珠竖线轨 + 步骤行(当前步近黑竖条+序号圆+柔光环·完成绿灯) + done/total 计数
platforms: [web]
theme: both
tags:
  aesthetic: [glass, minimal]
  mood: [calm, serious]
  stack: [react-tailwind]
uses:
  - components/display/studio-board/warm-glass-card
  - components/indicators/studio-board/pipeline-status-light
  - tokens/palettes/studio-board/warm-sand-ink
  - tokens/motion/studio-board/liquid-ease
preview: /preview/blocks/nav/studio-board/pipeline-rail
---

# 生产管线脊柱轨

> 详情页左栏（260px 白玻璃卡）：把一条内容的生产步骤竖排成「串珠脊柱」，分创意/制作两组，当前步近黑高亮、完成步苔绿打勾。

## 视觉特征

- **外壳**：`studio-glass rounded-lg p-4 · flex-col gap-4`，`sb-thin-scroll` 块内滚、满高
- **脊柱头**：`生产管线` 标题（`font-display text-sm font-semibold`）+ 右侧 `done/total` 计数胶囊——**全部完成才染苔绿**（`border-success/30 bg-success/10 text-success`），否则中性
- **两分组（LaneGroup）**：`创意 · 需你定稿` / `制作 · 自动执行`，组标是 `font-mono text-[10px] uppercase tracking-[0.14em] text-muted opacity-60`——极克制的 mono 小标
- **串珠竖线轨**：每组内 `relative`，一条 `absolute inset-y-4 left-5 w-px bg-border` 竖线穿过各节点圆心、被实心节点盖住 → 串珠脊柱效果
- **步骤行（StepNode）**：`rounded-lg py-2 pl-1.5 pr-2.5`，含状态灯圆 + 步名(`font-display text-sm`) + 副行(`font-mono text-[10px]` 状态/进度) + 毛病计数徽标
  - **当前步**：`studio-step-current`（`linear-gradient(90deg, rgba(acc,.07), transparent 72%)` 横向渐隐底）+ 左侧近黑竖条(`h-5 w-[3px] bg-focus`) + 节点变**实心近黑序号圆**(`h-8 w-8 bg-focus text-white`) + `studio-node-current` 柔光环
  - **hover**：左侧指示条竖向展开(`scale-y 0→1`)、节点 `scale-105`——比整行右移克制
  - **进行中步**：行内嵌细进度条(`h-1.5 rounded-full`，可数=金色定宽、不可数=脉冲、卡住=转灰)
- 缓动统一 `cubic-bezier(0.16,1,0.3,1)`

## 核心代码

```tsx
<aside className="studio-glass sb-thin-scroll flex flex-col gap-4 overflow-y-auto rounded-lg p-4 lg:h-full">
  <div className="flex items-baseline justify-between px-1">
    <span className="font-display text-sm font-semibold text-ink">生产管线</span>
    <span className={`rounded-full border px-2 py-0.5 font-mono text-[11px] ${allDone ? 'border-success/30 bg-success/10 text-success' : 'border-border text-muted'}`}>{done} / {total}</span>
  </div>
  <LaneGroup title="创意 · 需你定稿">{creative.map(StepNode)}</LaneGroup>
  <LaneGroup title="制作 · 自动执行">{mechanical.map(StepNode)}</LaneGroup>
</aside>
// LaneGroup 串珠线：<span className="absolute inset-y-4 left-5 w-px bg-border" />
// 当前步节点：<span className="studio-node-current h-8 w-8 rounded-full bg-focus text-white">{index}</span>
```

## 适配指南

- 分组小标用 mono uppercase + `opacity-60`——克制到几乎退隐，不与步名抢
- 当前步靠「近黑序号圆 + 左竖条 + 横向渐隐底」三重标记，别只换背景色
- 计数「全绿才染绿」——中间态保持中性，避免过早庆祝

## 反模式

- 不要用重色块标当前步（近黑 + 柔光即够，克制）
- 不要给每步都加脉冲（只进行中步的进度条脉冲）
- 不要丢掉串珠竖线（它是「脊柱」隐喻的关键，去掉就散成列表）
