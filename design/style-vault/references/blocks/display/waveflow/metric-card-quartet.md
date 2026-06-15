---
id: blocks/display/waveflow/metric-card-quartet
type: block
name: 4 tone 度量卡四件
description: default warm-2 / success emerald-50 / warning orange-50 / danger red-50 - rounded-lg border + icon + 11px label + 24px mono 大数字
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [serious, calm]
  stack: [shadcn-radix]
uses: []
preview: /preview/blocks/display/waveflow/metric-card-quartet
---

# Waveflow MetricCard Quartet

> waveflow 数据卡片小型号（`components/common/MetricCard.tsx`）—— jobSet detail 顶部 4-grid 用：**总任务 (default)** / **运行中 (success)** / **已暂停 (default)** / **异常 (danger)**。比 KPI Card 小一档：`rounded-lg border p-3` + icon 12px + 11px label + 24px mono num。

## 视觉特征

- **基础类**：`rounded-lg border p-3` + 不同 tone 切 wrap/label/num 颜色
- **4 tone**：
  - **default**: `bg-[var(--color-warm-2)]/60 border-stone-200/40` · label text-stone-500 · num text-stone-900
  - **success**: `bg-emerald-50/60 border-emerald-200/40` · label text-emerald-700 · num text-emerald-700
  - **warning**: `bg-orange-50/60 border-orange-200/40` · label text-orange-700 · num text-orange-700
  - **danger**:  `bg-red-50/60 border-red-200/40` · label text-red-700 · num text-red-700
- **label**：`flex items-center gap-1.5 text-[11px] mb-0.5` + 11px label
- **icon**：12×12 (`h-3 w-3`) —— 比标签字略大半档
- **num**：`text-[24px] font-semibold leading-none font-mono tnum`
- **4-grid layout**：`grid grid-cols-4 gap-3` 平铺

## 核心代码

```tsx
export const MetricCard = ({ icon, label, value, tone = 'default', className }) => {
  const c = toneClass[tone];
  return (
    <div className={cn('rounded-lg border p-3', c.wrap, className)}>
      <div className={cn('flex items-center gap-1.5 text-[11px] mb-0.5', c.label)}>
        {icon}{label}
      </div>
      <div className={cn('text-[24px] font-semibold leading-none font-mono tnum', c.num)}>
        {value}
      </div>
    </div>
  );
};

// 用法
<div className="mb-5 grid grid-cols-4 gap-3">
  <MetricCard icon={<ListChecks className="h-3 w-3" />} label="总任务" value={memberCount} />
  <MetricCard icon={<CheckCircle2 className="h-3 w-3" />} label="运行中" value={runningCount} tone="success" />
  <MetricCard icon={<PauseCircle className="h-3 w-3" />} label="已暂停" value={stoppedCount} />
  <MetricCard icon={<AlertCircle className="h-3 w-3" />} label="异常" value={errorCount} tone="danger" />
</div>
```

## 适配指南

- 4 张是上限——更多用 6-KPI row 风格（28px num + 行数据辅助）
- tone 选 default/success/danger 三档够 —— warning 用于"已暂停"是 amber 视觉抢戏，故 waveflow 实际把"已暂停"也用 default（去抢眼）
- 数字直接显数字，不要 `toLocaleString()` —— 小数据 1-3 位不需要千分位

## 反模式

- ❌ tone 配色 alpha 提到 100%—— 失去"淡淡的色彩区分"
- ❌ num 不加 mono tnum—— 表格列对齐塌
- ❌ icon size 8px 太小—— 看不清
