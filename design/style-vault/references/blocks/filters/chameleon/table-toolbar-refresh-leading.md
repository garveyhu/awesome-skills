---
id: blocks/filters/chameleon/table-toolbar-refresh-leading
type: block
name: 带刷新前导槽工具栏
description: waveflow 三段工具栏基础上新增独立 RotateCw 刷新 icon 按钮（最左）+ leadingExtra 槽（DateRangePicker / AgentPicker，排在下拉前），其余 search + N filter + extra 同源
platforms:
- web
theme: light
tags:
  aesthetic:
  - minimal
  mood:
  - calm
  stack:
  - shadcn-radix
uses:
- tokens/palettes/waveflow/warm-paper-ink-blue
preview: /preview/blocks/filters/chameleon/table-toolbar-refresh-leading
---

# 带刷新前导槽工具栏

> Chameleon 的 `TableToolbar`（`core/components/table/table-toolbar.tsx`）——在 waveflow 三段式（title 左 / search / N filter + extra 右）基础上多两个结构槽：右区最左的独立 `RotateCw` 刷新 icon 按钮，以及紧随其后的 `leadingExtra` 槽（放 DateRangePicker / AgentPicker 等宽控件，排在下拉 filter 之前）。

## 视觉特征

- **容器**：`mb-2.5 flex items-center gap-2`（下边距 10px / 横向 gap 8px）
- **title**：`h3.text-[13.5px] font-semibold text-stone-900`（#1c1917）
- **右区**：`ml-auto flex flex-wrap items-center gap-1.5`（gap 6px）
- **刷新按钮**（`onRefresh` 传入时，**右区最左**）：`flex h-7 w-7 shrink-0 items-center justify-center rounded-md text-stone-400 transition hover:bg-stone-100 hover:text-stone-700`，内 `RotateCw h-3.5 w-3.5`（14px）
- **leadingExtra 槽**：紧跟刷新按钮之后、search 之前——放日期区间 / AgentPicker
- **search**：`relative` 包裹
  - 前缀搜索按钮：`absolute left-1.5 top-1/2 z-10 -translate-y-1/2 rounded p-0.5 text-stone-400 hover:bg-stone-100 hover:text-stone-700`，内 `Search h-3 w-3`（12px）
  - Input：`!h-7 pl-6 text-[12px]`（高 28px / 左 padding 24px / 字 12px），`maxWidth = search.width ?? 180`，Enter 提交
- **filter**（每个 Select）：SelectTrigger `!h-7 whitespace-nowrap !text-[12px]`，`width = f.width ?? 110`，内 `span.truncate`；SelectContent 首项 `SelectItem value="all"`（allLabel 默认「全部」）
- **extra 槽**：收尾（按钮 / 菜单）
- **lucide**：`RotateCw` / `Search`

## 核心代码

```tsx
<div className="mb-2.5 flex items-center gap-2">
  {title && <h3 className="text-[13.5px] font-semibold text-stone-900">{title}</h3>}
  <div className="ml-auto flex flex-wrap items-center gap-1.5">
    {onRefresh && (
      <button title="刷新" onClick={onRefresh}
        className="flex h-7 w-7 shrink-0 items-center justify-center rounded-md text-stone-400 transition hover:bg-stone-100 hover:text-stone-700">
        <RotateCw className="h-3.5 w-3.5" />
      </button>
    )}
    {leadingExtra}
    {search && (
      <div className="relative">
        <button className="absolute left-1.5 top-1/2 z-10 -translate-y-1/2 rounded p-0.5 text-stone-400 hover:bg-stone-100 hover:text-stone-700"
          onClick={() => { search.onSubmit(search.value); search.onRefresh?.(); }}>
          <Search className="h-3 w-3" />
        </button>
        <Input className="!h-7 pl-6 text-[12px]" style={{ maxWidth: search.width ?? 180 }}
          value={search.value} onChange={e => search.onChange(e.target.value)}
          onKeyDown={e => { if (e.key === 'Enter') search.onSubmit(search.value); }} />
      </div>
    )}
    {filters?.map(f => (
      <Select value={f.value} onValueChange={f.onChange}>
        <SelectTrigger className="!h-7 whitespace-nowrap !text-[12px]" style={{ width: f.width ?? 110 }}>
          <span className="truncate">{f.value === 'all' ? f.placeholder : optLabel}</span>
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">{f.allLabel ?? '全部'}</SelectItem>
          {f.options.map(o => <SelectItem value={o.value}>{o.label}</SelectItem>)}
        </SelectContent>
      </Select>
    ))}
    {extra}
  </div>
</div>
```

## 与 waveflow/table-toolbar-tri 区分

供 AI 消费时选对：

| 维度 | waveflow/table-toolbar-tri | chameleon/table-toolbar-refresh-leading |
|------|------|------|
| **刷新触发** | 只藏在 search 图标 click（`search.onRefresh?.()`），无独立按钮 | **独立 `RotateCw` h-7 w-7 icon 按钮**，排右区最左，无须先搜索即可刷新 |
| **前导槽** | 无 | **`leadingExtra` 槽**：刷新按钮后、search 前——专放 DateRangePicker / AgentPicker 等宽控件 |
| **三段主体** | title / search / N filter + extra | 完全同源（数值、h-7、gap-1.5、110px filter、180px search 全一致） |

选型：单纯列表筛选 → waveflow 版；需要显眼刷新按钮、或有日期区间 / Agent 选择器要排在下拉前 → 本变体。

## 适配指南

- `onRefresh` 与 search 内的 `onRefresh` 是两套：前者是独立按钮的强制刷新，后者是搜索图标点击附带刷新
- leadingExtra 放宽控件（DateRangePicker），filter 放窄下拉——视觉从左到右由宽到窄收敛
- filter 改变后必跟 `setPage(1)`，避免跳到不存在的分页
- 所有控件统一 `h-7`（28px）紧凑型，与 DataTable 卡片节奏对齐

## 反模式

- ❌ 把刷新按钮做成有文字的 button——破坏右区紧凑节奏，icon 即可
- ❌ leadingExtra 放窄下拉——宽控件靠前、窄下拉靠后才是收敛布局
- ❌ filter trigger 宽度不固定——切 placeholder 时跳动
