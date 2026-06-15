---
id: blocks/display/acme/saas-metric-grid
type: block
name: SaaS 指标网格
description: 4 列 KPI 卡 · uppercase caption + Plex Mono 大数字 + delta arrow + sparkline
platforms: [web]
theme: dark
tags:
  aesthetic: [minimal, industrial]
  mood: [cold, serious]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/acme/slate-cyan-ice
  - tokens/typography/pairs/acme/ibm-plex-duo
preview: /preview/blocks/display/acme/saas-metric-grid
---

# SaaS Metric Grid

> 监控 dashboard 顶部的 KPI 一览：4 列等宽，**信息密度即美学**。

## 视觉特征

- 4 列 grid（lg）/ 2 列（md）/ 1 列（sm），间距 `gap-px`（仅 1px 切割线，不是 gap-4）
- 每 cell：
  - **caption**（11px Plex Sans uppercase tracking-[0.18em] color slate-500）
  - **display number**（Plex Mono 36px，font-weight 500，color slate-100）
  - **delta**（13px Plex Mono；emerald-400 上 / rose-400 下；绝对值小尽量压平不抢眼）
  - **sparkline**（高 28px 的 SVG 折线，subtle slate-700 stroke）
- 整体高度 ~140px；背景 `slate-900`（比页面 slate-950 浅一档）
- 不要任何边框圆角；cell 之间用 1px slate-800 分割

## 核心代码

```tsx
interface Metric {
  label: string;
  value: string;
  delta?: { dir: 'up' | 'down'; value: string };
  sparkline?: number[]; // 0..1 normalized
}

export function SaasMetricGrid({ metrics }: { metrics: Metric[] }) {
  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-px bg-slate-800">
      {metrics.map((m) => (
        <div key={m.label} className="bg-slate-900 px-6 py-5">
          <div className="text-[11px] uppercase tracking-[0.18em] text-slate-500">
            {m.label}
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="font-mono text-[36px] font-medium text-slate-100 leading-none">
              {m.value}
            </span>
            {m.delta && (
              <span
                className={`font-mono text-[13px] ${
                  m.delta.dir === 'up' ? 'text-emerald-400' : 'text-rose-400'
                }`}
              >
                {m.delta.dir === 'up' ? '↑' : '↓'} {m.delta.value}
              </span>
            )}
          </div>
          {m.sparkline && <Sparkline values={m.sparkline} />}
        </div>
      ))}
    </div>
  );
}

function Sparkline({ values }: { values: number[] }) {
  const w = 200;
  const h = 28;
  const step = w / (values.length - 1);
  const path = values
    .map((v, i) => `${i === 0 ? 'M' : 'L'} ${i * step} ${h - v * h}`)
    .join(' ');
  return (
    <svg width="100%" height={h} viewBox={`0 0 ${w} ${h}`} className="mt-3 text-slate-600">
      <path d={path} fill="none" stroke="currentColor" strokeWidth="1.2" />
    </svg>
  );
}
```

## 适配指南

- caption 必 uppercase + tracking-wider —— 这是冷感工业的标识
- delta 上下分别用 emerald / rose（不要 green / red）
- sparkline 中性灰色 stroke—**不要**配 cell 主题色，避免视觉过载
- 跨 4 cell 的 metric 顺序通常按"健康度 → 流量 → 性能 → 错误"

## 反模式

- 不要给 cell 加背景色区分类型（如 critical 整 cell 飙红）—— 用 delta 颜色就够
- 不要圆角 cell
- 不要 gap > 1px（破坏"信息密度即美学"）
