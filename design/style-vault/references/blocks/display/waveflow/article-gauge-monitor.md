---
id: blocks/display/waveflow/article-gauge-monitor
type: block
name: 资源监控 Article + 3-Gauge
description: 资源监控页 article 卡 - header（执行器 + 注册地址 + 更新时间）+ 3-column gauge 网格（CPU / 内存 / Load Average）
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, industrial]
  mood: [serious]
  stack: [shadcn-radix]
uses:
  - tokens/palettes/waveflow/warm-paper-ink-blue
  - components/typography-atoms/waveflow/meta-caps-mono-pair
preview: /preview/blocks/display/waveflow/article-gauge-monitor
---

# Waveflow Article Gauge Monitor

> 资源监控页（`/registry`）每个执行器一张 article 卡——`rounded-xl border border-stone-200/40 bg-[var(--color-paper)] shadow-[var(--shadow-soft)] p-4`。**Header**: 执行器名（stone-900 medium） + 注册地址（mono blue-600 tnum）+ 右上更新时间（mono stone-600 11.5px）。**Body**: `grid grid-cols-1 md:grid-cols-3 gap-3` 三 gauge：CPU `#2563eb` / 内存 `#dc2626` / Load Average。

## 页面骨架

```tsx
<article className="rounded-xl border border-stone-200/40 bg-[var(--color-paper)] shadow-[var(--shadow-soft)] p-4">
  <header className="mb-4 flex flex-wrap items-center justify-between gap-3 border-b border-stone-100 pb-3">
    <div className="flex flex-wrap items-center gap-6 text-[12.5px]">
      <div>
        <span className="text-stone-500">执行器：</span>
        <span className="font-medium text-stone-900">{registryKey}</span>
      </div>
      <div>
        <span className="text-stone-500">注册地址：</span>
        <span className="font-mono text-blue-600 tnum">{registryValue}</span>
      </div>
    </div>
    <div className="text-[11.5px] text-stone-500">
      更新时间：<span className="font-mono text-stone-600 tnum">{updateTime}</span>
    </div>
  </header>

  <div className="grid grid-cols-1 gap-3 md:grid-cols-3">
    <GaugeChart title="CPU 使用率" value={cpuUsage} unit="%" color="#2563eb" />
    <GaugeChart title="内存使用率" value={memoryUsage} unit="%" color="#dc2626" />
    <LoadAverage value={loadAverage} />
  </div>
</article>
```

## 视觉特征

- **多 article 间 `space-y-4`**：每个执行器是独立 article（不共用 section）—— `<div className="space-y-4">{registryList.map(item => <article key={item.id}>...)}</div>`
- **header 内 label/value 用色阶差表达**：label stone-500 / value stone-900 / 关键 value mono blue-600（注册地址）
- **gauge 三色对应负载语义**：CPU 蓝 / 内存红 / Load 自定—— 颜色不滥用，每色专管一指标
- **header 下 `border-b border-stone-100 pb-3 mb-4`**：分割 header 和 gauge 区
- **响应式**：1 col mobile → 3 col md+

## 适配指南

- 多机房 / 多执行器场景天然适配——article 平铺，scrollable
- `GaugeChart` 用 ECharts gauge type，dataset 单值 + 圆环
- 加搜索筛选时，把 `<section>` 搜索栏放在 article list 上方（独立 card）

## 反模式

- ❌ 把所有执行器塞一个 table 里—— 失去"每台机器一张卡"的直观
- ❌ gauge 改用进度条—— 圆环比线性更能表达"满负载"语义
- ❌ 更新时间靠 polling 一直刷数字闪—— 用 30s 间隔，gauge 内部不做动画
