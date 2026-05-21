---
id: components/indicators/waveflow/segmented-blocks
type: component
name: 任务集分段方块进度
description: N 个 14×6px 方块平铺，每个对应一个任务状态 (running emerald / error red / stopped stone / pending stone-200)，配套 3-segment percentage bar
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, industrial]
  mood: [serious, calm]
  stack: [shadcn-radix]
uses:
  - components/indicators/waveflow/status-dot-ring
preview: /preview/components/indicators/waveflow/segmented-blocks
---

# Waveflow Segmented Blocks

> waveflow 任务集 sidebar 的招牌视觉——一行**14×6px 方块**，每个方块对应集合内**一个任务**的状态。把 N 个任务的整体健康状况一眼可读。同文件还导出 `ThreeSegmentBar`（横向 emerald/stone/red 三段填充进度条）配合 sidebar 卡片用。

## 视觉特征

- **SegmentedBlocks**：
  - 容器：`flex flex-wrap` + `gap: 2px` (style)
  - 单方块：`inline-block rounded-[1px]` + `width: 14px; height: 6px` (style)
  - 4 态颜色：`running bg-emerald-500 / error bg-red-400 / stopped bg-stone-300 / pending bg-stone-200`
  - 默认尺寸可调：`blockSize=14, blockHeight=6, gap=2`
- **ThreeSegmentBar**（横向条）：
  - 外框：`flex h-1.5 overflow-hidden rounded-full bg-stone-100`
  - 三段：`bg-emerald-500 (running %) → bg-stone-300 (stopped %) → bg-red-400 (error %)`
  - 计算：`pct(n) = total > 0 ? (n / total) * 100 : 0`
- **任务集 sidebar 卡片用法**：构造 statuses 数组 `[...Array(okRunning).fill('running'), ...Array(errors).fill('error'), ...Array(stopped).fill('stopped'), ...Array(pending).fill('pending')]`，按这个顺序填到 SegmentedBlocks

## 核心代码

```tsx
export const SegmentedBlocks = ({ statuses, blockSize = 14, blockHeight = 6, gap = 2, className }) => (
  <div className={cn('flex flex-wrap', className)} style={{ gap }}>
    {statuses.map((s, i) => (
      <span
        key={i}
        className={cn('inline-block rounded-[1px]', segColor[s])}
        style={{ width: blockSize, height: blockHeight }}
      />
    ))}
  </div>
);

export const ThreeSegmentBar = ({ running, stopped = 0, error = 0 }) => {
  const total = running + stopped + error;
  const pct = n => total > 0 ? (n / total) * 100 : 0;
  return (
    <div className="flex h-1.5 overflow-hidden rounded-full bg-stone-100">
      <div className="bg-emerald-500" style={{ width: `${pct(running)}%` }} />
      <div className="bg-stone-300" style={{ width: `${pct(stopped)}%` }} />
      <div className="bg-red-400" style={{ width: `${pct(error)}%` }} />
    </div>
  );
};
```

## 适配指南

- 任务集场景：N 个任务 → N 个方块，让用户一眼看到"哪个任务有问题"
- 任务多（> 20）→ 把 blockSize 缩到 10×4，gap 1
- 任务巨多（> 50）→ 改用 ThreeSegmentBar 表达百分比聚合，不再"按个数"展示
- 状态填充顺序：running → error → stopped → pending（让"危险"和"正常"集中显示而不是穿插）

## 反模式

- ❌ 方块改大到 24×12—— 失去"密度感"
- ❌ 方块用圆形—— 失去"块状=任务"的直观映射
- ❌ 状态散乱排（按 jobId 排）—— 看不清整体健康
