---
id: pages/dashboard/chameleon/observability-overview-tabs
type: page
name: 可观测总览多 Tab 仪表盘
description: 单页多 tab（概览/成本）可观测总览 · 4 StatTile KPI（带环比 delta）+ 调用趋势双轴折线 + 渠道/错误分布卡 + Top 应用/智能体 DataTable（rank + 占比条）
platforms:
- web
theme: light
tags:
  aesthetic:
  - minimal
  - industrial
  mood:
  - calm
  - serious
  stack:
  - shadcn-radix
uses:
- components/display/chameleon/distribution-score-bars
- components/display/chameleon/stat-tile-delta
preview: /preview/pages/dashboard/chameleon/observability-overview-tabs
---

# Chameleon Observability Overview Tabs

> chameleon 可观测域的总览页——单页多 tab（概览 / 成本，路由 `/dashboard` + `/dashboard/cost` 切同一壳，nav 只 1 个入口、tab 按权限显隐保高亮）。无大标题，顶栏只有 SegmentedControl tab + DateRangePicker 一行。概览 tab：4 个 StatTile KPI（调用量 / 成功率 / Token / 活跃终端用户，带环比 delta + 图标 chip）→ 调用趋势双轴折线（总调用 primary / 错误 red）→ 渠道 + 错误分布卡（横向占比条）→ Top 应用 + Top 智能体 DataTable（RankBadge + 名称 + 占比条 + count）。

## 视觉特征

- **整页**：`space-y-4(16px)`（无大标题；顶栏 `mb-4 flex items-center justify-between gap-3`：左 SegmentedControl，右 DateRangePicker）
- **KPI grid**：`grid grid-cols-2 gap-4 lg:grid-cols-4`，每格 StatTile：
  - 卡：`flex items-start justify-between rounded-xl(16px) border border-stone-200(#e7e5e0) bg-paper p-5(20px)`
  - 左侧：label `text-xs(12px) text-stone-500` → value `mt-2 truncate font-mono text-2xl(24px) tracking-tight text-stone-900`（loading 显 `—`）→ hint 行 `mt-1 text-[11px]`：hint `text-stone-400` + delta `inline-flex gap-0.5 font-medium`（`TrendingUp/Down h-3 w-3`，good→`text-emerald-600` / bad→`text-red-600` / 0→`text-stone-400`，`(delta*100).toFixed(1)%`）
  - 右侧 icon chip：`h-10 w-10 rounded-lg(8px)` + tone 色（primary `bg-primary-50 text-primary-600` / success `bg-emerald-50 text-emerald-600` / warning `bg-amber-50 text-amber-600` / danger `bg-red-50 text-red-600`），内 `Icon h-5 w-5`（Activity / Sparkles / Bot / Users）
  - 成功率 tone 分档：`>0.95 success` / `>0.8 warning` / else `danger`
- **趋势卡**：`Card(rounded-lg(8px) border-stone-200 bg-paper shadow-card) > CardContent pt-5`：header `mb-3 flex items-center justify-between`（h3 `text-sm font-medium text-stone-900「调用趋势」` + 粒度 `text-[11px] text-stone-400「按天/小时」`）+ TimeSeriesChart `height 240` 双 series（total `var(--color-primary-600)` / errors `var(--color-red-500)`）
- **分布行**：`grid grid-cols-1 gap-4 lg:grid-cols-2` → 2 个 DistributionCard（渠道分布 / 错误类型）：
  - `Card > CardContent pt-5`，h3 同上 → `ul space-y-2.5`，每行：label/count 行 `mb-1 flex justify-between text-[12px]`（label `truncate text-stone-700` + count `tnum text-stone-500` + `%` `ml-1 text-stone-400`）+ 占比条 `relative h-1.5 w-full overflow-hidden rounded bg-stone-100` 内 `bg-primary-400 absolute inset-y-0 left-0 rounded`（width = count/total %）
- **Top 行**：`grid grid-cols-1 gap-4 lg:grid-cols-2` → 2 个 Card（Top 应用 / Top 智能体），`CardContent pt-5` + h3 + DataTable：
  - 名称列：`flex items-center gap-2`——RankBadge（`h-5 w-5 rounded-full text-[10px] font-semibold tabular-nums ring-1 ring-inset`，前三金 `bg-amber-100 text-amber-700 ring-amber-200` / 银 `bg-slate-200 text-slate-600 ring-slate-300` / 铜 `bg-orange-100 text-orange-700 ring-orange-200`，其余 `bg-stone-100 text-stone-400 ring-stone-200`）+ 名称 `truncate text-stone-700`
  - 调用列（`align right` width 160）：占比条 `h-1.5 w-16 overflow-hidden rounded-full bg-stone-100` 内 `from-primary-300 to-primary-500 h-full rounded-full bg-gradient-to-r`（width = count/max %）+ count `tnum w-10 text-right text-stone-600`

## 核心代码

```tsx
// 顶栏：tab + 区间，无大标题
<div className="mb-4 flex items-center justify-between gap-3">
  {visibleTabs.length > 1 ? <SegmentedControl value={active} onChange={switchTab} options={...} /> : <div />}
  <DateRangePicker value={range} onChange={setRange} />
</div>
<RequirePermission perm={activePerm}>{active === 'cost' ? <CostTab .../> : <OverviewTab .../>}</RequirePermission>

// KPI tone 分档
const successTone: StatTone =
  (o?.success_rate ?? 1) > 0.95 ? 'success' : (o?.success_rate ?? 1) > 0.8 ? 'warning' : 'danger';

// Top 列：rank + 占比条
{
  key: 'count', header: '调用', align: 'right', width: 160,
  render: r => (
    <div className="flex items-center justify-end gap-2">
      <div className="h-1.5 w-16 overflow-hidden rounded-full bg-stone-100">
        <div className="from-primary-300 to-primary-500 h-full rounded-full bg-gradient-to-r" style={{ width: `${(r.count/max)*100}%` }} />
      </div>
      <span className="tnum w-10 text-right text-stone-600">{formatNumber(r.count)}</span>
    </div>
  ),
}
```

## 适配指南

- 多 tab 切换走 SegmentedControl（弹性滑块），路由切换保 `location.search`（区间联动），nav 只 1 个 dashboard 入口、cost tab 在页内按 `call_logs:read` 显隐
- 大数字 KPI 一律 `font-mono text-2xl tracking-tight`（tnum 对齐），label 小灰、delta 用 TrendingUp/Down + emerald/red 双色
- 占比条两种：分布卡用纯色 `bg-primary-400` 横满宽，Top 表用窄条 `w-16` + `from-primary-300 to-primary-500` 渐变
- 所有图表色用 CSS 变量（`var(--color-primary-600)`）随主题，不写死

## 反模式

- ❌ 给页面加大标题——这页靠 tab 栏 + 区间一行起头，无 h1
- ❌ KPI 数字用普通字体——大数字一律 `font-mono tnum` 才对齐扫读
- ❌ delta 永远一个色——上升/下降必须 emerald/red 分色（成本类 deltaInverse 反转）
- ❌ 图表色写死 hex——用 `var(--color-primary-600)` 随主题
- ❌ Top 占比条用满宽纯色——Top 表用 `w-16` 渐变窄条，和分布卡满宽条区分
