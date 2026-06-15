---
id: components/typography-atoms/waveflow/meta-caps-mono-pair
type: component
name: 元信息 caps + mono 数字对
description: 两个最常用的工程师印章 - `text-[10.5px] uppercase tracking-wider text-stone-500` 元标签 / `font-mono text-[11.5px] tnum text-stone-600` 数字段
platforms: [web]
theme: light
tags:
  aesthetic: [industrial, minimal]
  mood: [serious]
  stack: [shadcn-radix]
uses: []
preview: /preview/components/typography-atoms/waveflow/meta-caps-mono-pair
---

# Waveflow Meta Caps + Mono Pair

> waveflow 信息分组的"印章"，两个 className 模式整站共享：
> - **元信息 caps**：`text-[10.5px] uppercase tracking-wider text-stone-500` —— 9 处共用（sidebar group label / Section header meta / Dialog 副标 / Table 表头）
> - **数字段 mono**：`font-mono text-[11.5px] tnum text-stone-600` —— 7 文件共用（cron / 时间戳 / ID / 注册地址）

## 视觉特征

### 元信息 Caps

- **`text-[10.5px]` 而非 `text-xs` (12px)**：故意比标准 xs 小 1.5px——让"小标题"小到几乎是装饰，但又能读
- **`uppercase tracking-wider (0.05em)`**：大写 + 字距加宽——印章感
- **`text-stone-500`**：中灰，不抢主标题
- 衍生：sidebar 分组用 `text-[11px] font-medium uppercase tracking-wider text-stone-400`（暗一档）
- 衍生：DataTable thead 用 `text-[10.5px] uppercase tracking-wider text-stone-500 font-medium`

### 数字段 Mono

- **`font-mono`** = JetBrains Mono
- **`text-[11.5px]`**：比 12px 略小，给"密集数据列"用
- **`tnum`** = `font-variant-numeric: tabular-nums` —— 数字对齐
- **`text-stone-600`**：比 stone-500 略深半档——数字本身是核心信息
- 衍生：table ID 列用 `font-mono text-stone-500 tnum`（淡一档，因 ID 是辅助信息）
- 衍生：dashboard 大数字 `font-mono text-[28px] font-bold tnum text-stone-900 letter-spacing -0.02em`

## 核心代码

```tsx
// 1. 元信息 caps
<span className="text-[10.5px] uppercase tracking-wider text-stone-500">
  任务集 · 状态总览
</span>

// 2. sidebar 分组（暗变体）
<div className="px-3 pb-1 pt-3 text-[11px] font-medium uppercase tracking-wider text-stone-400">
  调度
</div>

// 3. 数字段 mono
<span className="font-mono text-[11.5px] tnum text-stone-600">
  {cron || '—'}
</span>

// 4. KPI 大数字
<div
  className="font-mono text-[28px] font-bold leading-none tnum text-stone-900"
  style={{ letterSpacing: '-0.02em' }}
>
  {value.toLocaleString()}
</div>
```

## 适配指南

- 任何"小标题 / meta label" 一律走 caps：sidebar 分组、breadcrumb 副标、Card meta、Dialog body 小标题
- 任何数字 / 时间戳 / cron / ID / 地址 一律 `font-mono ... tnum` ——表格列对齐才稳
- **不要把这两个模式写到 className 里**——只看到一次说明你在 reinvent

## 反模式

- ❌ 元信息用 `text-xs`（12px）—— 比 10.5 大太多，盖过主标题
- ❌ 数字段不加 tnum—— 表格列里 0 和 1 宽度不一样，丑
- ❌ 给中文段加 mono—— mono 中文显得"代码化"
