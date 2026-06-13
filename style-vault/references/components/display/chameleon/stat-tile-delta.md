---
id: components/display/chameleon/stat-tile-delta
type: component
name: KPI 指标卡四态
description: KPI 大数字卡四种形态 — StatTile(delta+tone chip) / MiniStat(7 色紧凑横排) / StatBar(无框发丝分隔指标条)，mono 大数字 + 环比趋势 + deltaInverse
platforms:
- web
theme: both
tags:
  aesthetic:
  - industrial
  - minimal
  mood:
  - calm
  - confident
  - serious
  stack:
  - shadcn-radix
uses:
- tokens/iconography/waveflow/engineer-detail-classes
- tokens/palettes/chameleon/themeable-8x4-system
- tokens/palettes/waveflow/warm-paper-ink-blue
- tokens/typography/pairs/waveflow/inter-jetbrains-instrument-trio
preview: /preview/components/display/chameleon/stat-tile-delta
---

# KPI 指标卡四态

> Chameleon dashboard / cost / eval / trace / 会话详情共用的 KPI 展示族，四种形态共享「mono 大数字 + tone 色块/语义色」基因：① **StatTile**——主指标大卡（label + mono text-2xl 值 + hint + 环比 delta 箭头 + 右侧 5 tone 图标 chip），`deltaInverse` 给「越低越好」的成本类指标反转红绿；② **MiniStat**——紧凑横排卡（左 7 色圆角图标块 + 右 mono 数字 + 小灰标签）；③ **StatBar / StatItem**——无框无卡的指标平铺横条（极淡竖发丝分隔，trace/会话详情用）。

## 视觉特征

### StatTile（主指标大卡 · signature）

- 容器：`flex items-start justify-between rounded-xl border border-stone-200 bg-[var(--color-paper)] p-5`（radius xl=12px，p-5=20px）
- 左侧（min-w-0）：
  - label：`text-xs text-stone-500`（12px）
  - value：`mt-2 truncate font-mono text-2xl tracking-tight text-stone-900`（**mono 24px 大数字**，loading 显 `—`）
  - hint + delta 行：`mt-1 flex items-center gap-2 text-[11px]`
    - hint：`truncate text-stone-400`
    - delta：`inline-flex shrink-0 items-center gap-0.5 font-medium` + 颜色（good=`text-emerald-600` #059669 / bad=`text-red-600` #dc2626 / 零或无=`text-stone-400`）+ `TrendingUp`/`TrendingDown h-3 w-3` + `{up?'+':''}{(delta*100).toFixed(1)}%`
- 右侧图标 chip（5 tone TONE_CHIP）：`flex h-10 w-10 shrink-0 items-center justify-center rounded-lg`（40px / radius 8px）+ tone 类：`primary bg-primary-50 text-primary-600`（**随主题**）/ `success bg-emerald-50 text-emerald-600` / `warning bg-amber-50 text-amber-600` / `danger bg-red-50 text-red-600` / `neutral bg-stone-100 text-stone-500`，内 `Icon h-5 w-5`（20px）
- **good 逻辑**：`deltaInverse ? down : up`——成本上升显红、下降显绿

### MiniStat（紧凑横排 · 7 tone）

- 卡：`flex items-center gap-3 rounded-xl border border-stone-200 bg-[var(--color-paper)] px-4 py-3`（radius 12px，px-4=16 / py-3=12）
- 左图标块：`flex h-9 w-9 shrink-0 items-center justify-center rounded-lg`（36px / radius 8px）+ tone 类，内 `Icon h-[18px] w-[18px]`（18px）
- 右（min-w-0）：数字 `tnum font-mono text-[19px] leading-none font-semibold text-stone-900`（19px）+ 标签 `mt-1 truncate text-[11px] text-stone-500`
- **7 tone**：primary `bg-primary-50 text-primary-600` / success emerald / warning amber / danger red / violet `bg-violet-50 text-violet-600` / sky `bg-sky-50 text-sky-600` / neutral `bg-stone-100 text-stone-500`（浅底深字）

### StatBar / StatItem（无框发丝指标条）

- StatBar 容器：`flex flex-wrap gap-y-3 py-1`
- StatItem：`mr-4 border-r border-stone-100 pr-4 last:mr-0 last:border-r-0 last:pr-0`（**右侧极淡竖发丝分隔，最后一项去掉**）
  - label：`text-[10.5px] tracking-wide text-stone-400`
  - value 行：`mt-1 flex items-baseline gap-1.5`，span `tnum text-[15px] font-semibold`，tone=ok `text-emerald-600` / err `text-rose-600` / 默认 `text-stone-800`，mono 时 `font-mono text-[13px]`
  - sub 副值：`tnum text-[11px] font-normal text-stone-400`

## Tokens

```json
{
  "tile": { "radius": "12px", "padding": "20px", "value": { "font": "mono", "size": "24px" }, "iconChip": "40px" },
  "mini": { "radius": "12px", "padding": "12px 16px", "iconBlock": "36px", "icon": "18px", "value": "19px" },
  "statBar": { "divider": "1px solid #f5f5f4", "label": "10.5px", "value": "15px", "valueMono": "13px" },
  "tone": {
    "primary": { "bg": "var(--color-primary-50)", "fg": "var(--color-primary-600)" },
    "success": { "bg": "#ecfdf5", "fg": "#059669" },
    "warning": { "bg": "#fffbeb", "fg": "#d97706" },
    "danger": { "bg": "#fef2f2", "fg": "#dc2626" },
    "violet": { "bg": "#f5f3ff", "fg": "#7c3aed" },
    "sky": { "bg": "#f0f9ff", "fg": "#0284c7" },
    "neutral": { "bg": "#f5f5f4", "fg": "#78716c" }
  },
  "delta": { "good": "#059669", "bad": "#dc2626", "zero": "#a8a29e" }
}
```

## 核心代码

```tsx
// StatTile good 逻辑 + delta 色
const good = deltaInverse ? down : up;
const deltaColor = !hasDelta || delta === 0 ? 'text-stone-400' : good ? 'text-emerald-600' : 'text-red-600';

<div className="flex items-start justify-between rounded-xl border border-stone-200 bg-[var(--color-paper)] p-5">
  <div className="min-w-0">
    <div className="text-xs text-stone-500">{label}</div>
    <div className="mt-2 truncate font-mono text-2xl tracking-tight text-stone-900">{loading ? '—' : value}</div>
    <div className="mt-1 flex items-center gap-2 text-[11px]">
      {hint && <span className="truncate text-stone-400">{hint}</span>}
      {hasDelta && (
        <span className={cn('inline-flex shrink-0 items-center gap-0.5 font-medium', deltaColor)}>
          {up ? <TrendingUp className="h-3 w-3" /> : down ? <TrendingDown className="h-3 w-3" /> : null}
          {up ? '+' : ''}{(delta * 100).toFixed(1)}%
        </span>
      )}
    </div>
  </div>
  {Icon && <div className={cn('flex h-10 w-10 shrink-0 items-center justify-center rounded-lg', TONE_CHIP[tone])}><Icon className="h-5 w-5" /></div>}
</div>
```

## 适配指南

- 成本 / 延迟 / 错误率等「越低越好」的指标传 `deltaInverse`——下降才显绿
- StatTile 用于页面顶部主 KPI（成排 3–4 个）；MiniStat 用于列表页顶部轻量概览（不抢主体卡风头）；StatBar 用于详情页/抽屉里横排指标（无框最省空间）
- 图标 chip 的 `primary` tone 走 `bg-primary-50/text-primary-600` 随主题色——其余 tone 是固定语义色
- 大数字一律 `font-mono` + `tnum`（tabular-nums）——数字等宽对齐，刷新时不抖动

## 反模式

- ❌ 大数字用正文字体——必须 `font-mono`，是 KPI 卡的识别基因
- ❌ delta 不区分 deltaInverse——成本上升显绿是误导
- ❌ StatBar 用实色竖线分隔——必须 `border-stone-100`（极淡发丝），重了像表格
- ❌ MiniStat 图标块用深底白字——它是「浅底深字」（bg-X-50 + text-X-600），跟 StatTile chip 一致
