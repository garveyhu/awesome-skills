---
id: components/indicators/waveflow/status-dot-ring
type: component
name: 7px 状态点 + 2px ring
description: 任务状态点（运行 emerald / 停 stone / 异常 red），7×7px + 2px 半透色 ring + 派生 deriveJobStatus / deriveRunStatus 函数
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, industrial]
  mood: [serious]
  stack: [shadcn-radix]
uses:
  - tokens/iconography/waveflow/engineer-detail-classes
preview: /preview/components/indicators/waveflow/status-dot-ring
---

# Waveflow Status Dot Ring

> waveflow 任务状态的最小可见单位——7×7px 圆 + 2px 半透色 ring（15-18% alpha）。3 态：running emerald / stopped stone / error red。配套 `deriveJobStatus()` 和 `deriveRunStatus()` 派生函数把 xxljob 后端的 4 个 code (200/0/500/null) 映射成可读语义。

## 视觉特征

- **核心 className**：`.status-dot` (`display:inline-block; width:7px; height:7px; border-radius:50%`)
- **3 态**：
  - `.status-dot-running` (`bg-emerald-500 (#10b981) + box-shadow: 0 0 0 2px rgb(16 185 129 / 15%)`)
  - `.status-dot-stopped` (`bg-stone-300 (#d6d3d1)` · 无 ring · "沉默"语义)
  - `.status-dot-error` (`bg-red-500 (#ef4444) + box-shadow: 0 0 0 2px rgb(239 68 68 / 18%)`)
- **StatusBadge wrapper**：dot + 中文 label
  - running emerald-600 文 / stopped stone-500 文 / error red-600 文 / pending stone-500 文 "待运行"
- **派生函数**：
  - `deriveJobStatus(triggerStatus, lastHandleCode, lastTriggerCode, triggerLastTime?, recentTriggerTime?) → JobStatus`
    - triggerStatus !== 1 → stopped
    - 调度失败 (lastTriggerCode != 200) → error
    - 执行失败 (lastHandleCode != 0/200) → error
    - 否则 → running
  - `deriveRunStatus(...)` → success / fail / running / never（综合派生最近执行结果）

## 核心代码

```tsx
export const StatusDot = ({ status, className }: { status: JobStatus; className?: string }) => (
  <span className={cn(dotClass[status], className)} />
);

export const StatusBadge = ({ status, label }) => (
  <span className={cn('inline-flex items-center gap-1.5 text-[12px]', colorMap[status])}>
    <StatusDot status={status} />
    {label ?? labelMap[status]}
  </span>
);
```

## 适配指南

- 用法极简：`<StatusDot status="running" />` 或 `<StatusBadge status="error" />`
- 嵌入文字行内：`<span className="inline-flex items-center gap-1.5"><StatusDot status="running" /><span>{name}</span></span>`
- 派生函数是核心：直接把后端 code 字段喂进去，不要业务层自己 if-else——保证全站一致
- 表格 leftBar 用同套色：`bg-emerald-500` / `bg-red-500` / `bg-stone-300`
- sidebar 子项 dot：用同款 dotFor 函数返回一个 `<Dot />` 子组件，把 ring 包在 inline-flex 容器内

## 反模式

- ❌ stopped 也加 ring—— "停止"是默认/沉默语义，加 ring 会显得"活跃"
- ❌ 改 dot 大小到 10px+——会跟 chip 抢主视觉
- ❌ 自己写 `triggerStatus === 1 ? 'running' : 'stopped'`——逻辑会和 deriveJobStatus 分叉
