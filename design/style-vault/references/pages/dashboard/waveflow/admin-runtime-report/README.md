---
id: pages/dashboard/waveflow/admin-runtime-report
type: page
name: 运行报表 Dashboard
description: 6 KPI row + 12-col 主图(line)+状态分布(pie) + executor health table + recent failures + 时长 bar + 调度 TOP 5 + 失败 TOP 5
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, industrial]
  mood: [serious, confident]
  stack: [shadcn-radix]
uses:
  - blocks/display/waveflow/dashboard-kpi-six-row
  - tokens/layout/waveflow/data-console-shell
preview: /preview/pages/dashboard/waveflow/admin-runtime-report
---

# Waveflow Admin Runtime Report

> waveflow 主 dashboard 页 (`/dashboard`) ——管理员一眼看到调度系统全局健康。**6 区块**自上而下：**Header**（页标题 + "实时·30s 刷新" 状态指示 + 1h/24h/7d/30d 时间范围切换）→ **KPI Row 6 卡**（dispatch+sparkline / success%+gradient bar / avg time / online executor / active jobs / 24h failed）→ **8/4 grid 主图区**（调度趋势 line chart + 任务状态 pie chart）→ **7/5 grid**（执行器健康 table + 最近失败 list）→ **5/3/4 grid**（执行时长分布 bar + 调度 TOP 5 + 失败 TOP 5）。

## 页面骨架

```tsx
<div className="space-y-3 px-6 py-5">

  {/* Header */}
  <header className="mb-2 flex items-center justify-between">
    <div>
      <h1 className="text-[20px] font-semibold tracking-tight text-stone-900">仪表盘</h1>
      <p className="mt-0.5 text-[12.5px] text-stone-500">实时调度状态 · 跨网数据同步</p>
    </div>
    <div className="flex items-center gap-4">
      {/* 实时刷新 pulse */}
      <div className="flex items-center gap-1.5 font-mono text-[11.5px] tnum text-stone-500">
        <span className="inline-block h-1.5 w-1.5 animate-pulse rounded-full bg-emerald-500"
          style={{ boxShadow: '0 0 6px #10b981' }} />
        实时 · 30s 刷新
      </div>
      {/* 时间范围 segment control */}
      <div className="flex items-center gap-1 rounded-lg bg-stone-100 p-1">
        {(['1h', '24h', '7d', '30d']).map(r => (
          <button key={r} onClick={() => setRange(r)}
            className={cn('rounded px-2.5 py-1 font-mono text-[11.5px] tnum transition',
              range === r ? 'bg-stone-900 text-white' : 'text-stone-500 hover:bg-stone-200/60')}>
            {r}
          </button>
        ))}
      </div>
    </div>
  </header>

  {/* KPI Row 6 */}
  {info ? <KPIRow info={info} /> : <div className="h-[120px]" />}

  {/* 主图 8/4 */}
  <div className="grid grid-cols-12 gap-3">
    <div className="rounded-2xl border border-stone-200/70 bg-white p-4 col-span-12 lg:col-span-8">
      <div className="mb-2 flex items-center justify-between">
        <div>
          <div className="text-[13px] font-semibold text-stone-800">调度趋势 · {RANGE_LABEL[range]}</div>
          <div className="mt-0.5 text-[11px] text-stone-500">成功 / 失败 / 执行中</div>
        </div>
        <div className="flex items-center gap-3 text-[11.5px]">
          <span className="flex items-center gap-1"><span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />成功</span>
          <span className="flex items-center gap-1"><span className="h-1.5 w-1.5 rounded-full bg-red-500" />失败</span>
          <span className="flex items-center gap-1"><span className="h-1.5 w-1.5 rounded-full bg-amber-500" />执行中</span>
        </div>
      </div>
      <LineChart chartData={lineChartData} height={280} />
    </div>

    <div className="rounded-2xl border border-stone-200/70 bg-white p-4 col-span-12 lg:col-span-4">
      <div className="mb-2 text-[13px] font-semibold text-stone-800">任务状态分布</div>
      <StatusPieChart data={info?.statusDistribution ?? {}} height={280} />
    </div>
  </div>

  {/* 7/5 grid */}
  <div className="grid grid-cols-12 gap-3">
    <div className="col-span-12 lg:col-span-7"><ExecutorHealthTable /></div>
    <div className="col-span-12 lg:col-span-5"><RecentFailures /></div>
  </div>

  {/* 5/3/4 grid */}
  <div className="grid grid-cols-12 gap-3">
    <div className="col-span-12 md:col-span-5"><DurationBarChart /></div>
    <div className="col-span-12 md:col-span-3"><TopList title="调度 TOP 5" mode="execution" /></div>
    <div className="col-span-12 md:col-span-4"><TopList title="失败 TOP 5" mode="failure" /></div>
  </div>

</div>
```

## 视觉要点

1. **`space-y-3` 行间距 12px**：所有区块之间—— 比 admin 卡片密集，但避免挤
2. **`px-6 py-5`**：dashboard 用 py-5 (而非列表页 py-4) —— 给"信息密集页面"多一档纵向呼吸
3. **header 时间范围 = stone-100 background segment control**：active stone-900 黑底白字（命令面板同款语言）、inactive stone-500 hover stone-200/60—— 不用 RadioGroup，直接 button 组
4. **实时 pulse 用 `animate-pulse + box-shadow glow #10b981`**：和 topbar 在线 dot 同款语言
5. **图表卡用 `bg-white + rounded-2xl + border-stone-200/70`**：dashboard 故意用 **白底** 而非 paper—— 让数据可视化"独立"更明显
6. **所有图表 ECharts**：line / pie / bar / gauge —— 单一可视化技术栈
7. **30s polling**：useEffect setInterval(fetchChartInfo(range), 30_000)
8. **range 改变后立即重拉**：useEffect [range] 依赖

## 适配指南

- 30s 是默认 polling 周期；如果服务端有 SSE 接口，可以改成 push（实际 waveflow 选了 polling 简单稳）
- 主图卡 `lg:col-span-8/4` —— 1024+ 才双列，小屏垂直堆叠
- 图表卡用 ReactECharts；动画必关 (`animation: false`) —— 避免每 30s 重渲染动一遍
- 时间范围切换不重置 polling 时钟—— `setInterval` 监听 range，自动用最新值

## 反模式

- ❌ dashboard 卡片用 hover 升浮—— display only，不交互
- ❌ KPI 卡用 paper 底—— dashboard 故意白底让 KPI"显赫"
- ❌ 不防 fetch 失败—— toast.error 提示 + 保留旧数据
- ❌ range 默认 1h—— 用 7d 更有视觉冲击
