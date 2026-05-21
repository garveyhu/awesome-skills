---
id: blocks/display/waveflow/dashboard-kpi-six-row
type: block
name: 6 KPI 卡片大数字行
description: 调度+sparkline / 成功率+渐变 bar / 平均耗时 + min-max / 在线执行器 + 健康 dot / 活跃任务 + glue chips / 24h 失败 - 6 张差异化 KPI 卡
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, industrial]
  mood: [serious, confident]
  stack: [shadcn-radix]
uses:
  - components/tags-badges/waveflow/glue-type-badge-duo
  - components/indicators/waveflow/pulse-ping-dot
  - components/typography-atoms/waveflow/meta-caps-mono-pair
preview: /preview/blocks/display/waveflow/dashboard-kpi-six-row
---

# Waveflow Dashboard KPI Six Row

> dashboard 顶部 6 KPI 大数字卡 (`KPIRow.tsx`)——`grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3`。每张 Card 都是 `rounded-2xl border border-stone-200/70 bg-white p-4`，自上而下三段：**Label**（10.5/11px uppercase tracking-wider）/ **Num**（28px mono bold tnum letter-spacing -0.02em）/ **辅助行**（Delta 趋势 / sparkline / mini progress / health dots / chips）。

## 6 张卡的差异化设计

### 1. 今日调度（DispatchCard）

- Num: 总调度次数 toLocaleString()
- Delta: `+12.5% vs ytd` (今 vs 昨) emerald/red 上下箭头
- **底部 32px 高 ECharts sparkline**：smooth line `#6366f1` 1.8px + 下方 `linear gradient(rgba 99,102,241 0.3 → 0)` 面积填充

### 2. 成功率（SuccessRateCard）

- Num: emerald-600 `99.4%` (1 位小数)
- Delta: `+0.3pp`
- **mini progress bar**: `h-1 rounded-full bg-stone-100` 内 `width=rate% + linear-gradient(90deg, #10b981, #06b6d4)` 渐变填充
- 底部 mono 10.5px stone-500: "12,345 成功 / 67 失败"

### 3. 平均耗时（AvgTimeCard）

- Num: `2.3` + 单位 `s` (14px stone-500)（自动 ms→s→m 切换）
- Delta: `-12% vs ytd` invert (减小是好事)
- 底部两栏: `min 0.4s     max 1m`（10.5px mono stone-500 justify-between）

### 4. 在线执行器（ExecutorOnlineCard）

- Num: `8` + `/ 10` 总数（14px stone-400）
- 健康标记: emerald `全部健康` + glow dot / amber `2 异常`
- **底部 8 段 health dots**：`flex gap-1` × 8 个 `h-1.5 flex-1 rounded-sm bg-emerald-500/stone-300/stone-100`

### 5. 活跃任务（ActiveJobsCard）

- Num: 运行中 + `/ N` 总数
- 中间行：`{paused} 停用 · {failOrError} 异常` mono 11px stone-500
- **底部 GlueType solid chips 横排**：`FETCH 12` `TRANS 8` `PUSH 5` ...（按 chipOrder 排序）

### 6. 24h 失败（FailedCountCard）

- Num: red-600 `7`
- Delta: invert (上升是坏事)
- 底部 mono 10.5px stone-500: "最近 14:32 · 上海"

## 视觉特征

- **6 卡用同一 Card 外框**：`rounded-2xl border border-stone-200/70 bg-white p-4` —— 唯一**白底**而非 paper 的卡片（dashboard 故意用 white 让 KPI 更"显赫"）
- **Num 28px font-bold + letter-spacing -0.02em**：紧凑数字感
- **Delta 11.5px tnum + 上下箭头 3×3**：good=emerald-600 / bad=red-600，`invert` prop 让某些指标反向（失败次数）
- **6 张卡的"辅助行"故意每张不同**：sparkline / progress / range / dots / chips / time——避免视觉同质化

## 适配指南

- 极简卡片 + 大数字 = 让"数据本身"是视觉主体——不要加任何卡片装饰
- 6 张是上限，再多就用第二行
- ECharts sparkline 选项必关 animation（`animation: false`）——避免 30s 刷新时跳

## 反模式

- ❌ KPI 卡加 hover 升浮——dashboard 是 display only，不交互
- ❌ Num 加 thousands separator 同时用 mono ——`12,345` 在 mono 字体里逗号位置怪，用 `toLocaleString()` + tnum 配合
- ❌ Delta 用大字号（> 12px）——会跟主 Num 抢戏
