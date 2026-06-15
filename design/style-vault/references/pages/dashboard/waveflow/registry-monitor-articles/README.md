---
id: pages/dashboard/waveflow/registry-monitor-articles
type: page
name: 资源监控（Article 堆叠 + 3-Gauge）
description: 顶部独立 search section + 多 article 堆叠 (每个执行器一卡 - header 信息 + 3-col gauge grid (CPU 蓝 / 内存 红 / Load 自定))
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, industrial]
  mood: [serious]
  stack: [shadcn-radix]
uses:
  - blocks/display/waveflow/article-gauge-monitor
preview: /preview/pages/dashboard/waveflow/registry-monitor-articles
---

# Waveflow Registry Monitor Articles

> waveflow 资源监控页 (`/registry`)——独立的 article 堆叠 dashboard。**顶部** 一个简化的 search section（仅 200px 搜索 input + icon prefix）+ **下方** `space-y-4` 多个 article 卡，每个对应一个执行器：header 显示执行器名 + 注册地址 + 更新时间，下方 `grid grid-cols-1 md:grid-cols-3` 三个 gauge（CPU `#2563eb` / 内存 `#dc2626` / Load Average 自定 color）。

## 页面骨架

```tsx
<div className="h-full px-6 py-4">

  {/* 顶部 search section */}
  <section className="mb-3 rounded-xl border border-stone-200/40 bg-[var(--color-paper)] p-3.5 shadow-[var(--shadow-soft)]">
    <div className="flex items-center gap-2">
      <h3 className="text-[13.5px] font-semibold text-stone-900">资源监控</h3>
      <div className="ml-auto flex items-center gap-1.5">
        <div className="relative">
          <button onClick={submit} className="absolute left-1.5 top-1/2 z-10 -translate-y-1/2 rounded p-0.5 text-stone-400 hover:bg-stone-100 hover:text-stone-700">
            <Search className="h-3 w-3" />
          </button>
          <Input className="!h-7 w-[200px] pl-6 text-[12px]" placeholder="搜索执行器" value={searchInput} onChange={...} onBlur={submit} onKeyDown={e => e.key === 'Enter' && submit()} />
        </div>
      </div>
    </div>
  </section>

  {/* article 列表 */}
  {loading && registryList.length === 0 ? (
    <div className="flex justify-center py-12 text-stone-400"><Loader2 className="h-5 w-5 animate-spin" /></div>
  ) : registryList.length === 0 ? (
    <div className="flex items-center justify-center py-16 text-[13px] text-stone-400">暂无监控数据</div>
  ) : (
    <div className="space-y-4">
      {registryList.map(item => (
        <article key={item.id} className="rounded-xl border border-stone-200/40 bg-[var(--color-paper)] p-4 shadow-[var(--shadow-soft)]">
          <header className="mb-4 flex flex-wrap items-center justify-between gap-3 border-b border-stone-100 pb-3">
            <div className="flex flex-wrap items-center gap-6 text-[12.5px]">
              <div><span className="text-stone-500">执行器：</span><span className="font-medium text-stone-900">{item.registryKey}</span></div>
              <div><span className="text-stone-500">注册地址：</span><span className="font-mono text-blue-600 tnum">{item.registryValue}</span></div>
            </div>
            <div className="text-[11.5px] text-stone-500">更新时间：<span className="font-mono text-stone-600 tnum">{item.updateTime}</span></div>
          </header>
          <div className="grid grid-cols-1 gap-3 md:grid-cols-3">
            <GaugeChart title="CPU 使用率" value={item.cpuUsage} unit="%" color="#2563eb" />
            <GaugeChart title="内存使用率" value={item.memoryUsage} unit="%" color="#dc2626" />
            <LoadAverage value={item.loadAverage} />
          </div>
        </article>
      ))}
    </div>
  )}
</div>
```

## 视觉要点

1. **search section 比正常 list section 矮**：`p-3.5` 而非 `p-5`—— 因没有 table 内容
2. **article 列表 `space-y-4`**：每个执行器一张独立卡片
3. **article header 双行布局**：左侧执行器名 + 注册地址（gap-6 横向） / 右侧更新时间
4. **gauge 三色专属**：CPU 蓝 / 内存红 / Load 自定—— 不复用，避免色彩混乱
5. **空态分两层**：loading + empty list → centered Loader2 ; empty data → "暂无监控数据" 居中文本
6. **搜索 input blur+enter+icon click 三触发**：用户多种习惯都覆盖

## 适配指南

- 多机房 / 多节点场景：article 自然堆叠
- GaugeChart 用 ECharts gauge type，dataset 单值；动画必关
- 实时更新：page 内 setInterval 30s 拉一次（waveflow 选 polling）

## 反模式

- ❌ 用 table 显示监控数据—— 失去"每台机一卡"直观
- ❌ gauge 用进度条—— 圆环更"满负载"感
- ❌ article 间无 gap—— 视觉粘连
