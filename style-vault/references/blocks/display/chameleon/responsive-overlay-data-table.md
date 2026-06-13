---
id: blocks/display/chameleon/responsive-overlay-data-table
type: block
name: 自适应横滚 + 蓝渐变 overlay 数据表
description: DataTable 泛型主体 - 4px 左状态条 + 8 行双阈值延迟 shimmer 骨架 + 顶部蓝渐变 refreshing overlay(已有数据静默换页) + scrollX/minWidth 大小屏自适应横滚 + ArrowUpDown 排序 + hover ? 列提示原子
platforms:
- web
theme: light
tags:
  aesthetic:
  - industrial
  - minimal
  mood:
  - calm
  - serious
  stack:
  - shadcn-radix
uses:
- tokens/border/waveflow/translucent-stone-system
- tokens/iconography/waveflow/engineer-detail-classes
- tokens/motion/waveflow/keyframes-suite
- tokens/palettes/waveflow/warm-paper-ink-blue
preview: /preview/blocks/display/chameleon/responsive-overlay-data-table
---

# 自适应横滚 + 蓝渐变 overlay 数据表

> Chameleon 的 DataTable 泛型主体（`core/components/table/data-table.tsx`）：**4px 左状态条** + **8 行双阈值延迟 shimmer 骨架** + **顶部蓝渐变 refreshing overlay**（已有数据时翻页/改筛选静默换页，不替换为骨架）+ **scrollX/minWidth 大小屏自适应横滚** + ArrowUpDown 可点排序。与 `waveflow/data-table-leftbar-shimmer` 同源，但**表头样式 + 刷新机制明显分叉**。附带 `ColumnHeader` 表头 hover ? 提示原子。

## 视觉特征

- **wrapper**：`relative rounded-lg(8) border border-stone-200/60`；overflowX 时 `overflow-x-auto` 否则 `overflow-hidden`
- **table**：`table-fixed`；`scrollX && !minWidth` → `min-w-max`，否则 `w-full`；设 minWidth 时 `style.minWidth`
- **colgroup**：hasLeftBar 时首列 `<col style={{ width: 4 }} />`，其余按 `col.width`
- **thead**：`border-b border-stone-200/70`
  - tr：`text-[11px] font-medium text-stone-400`（**无暖底、无大写、无字距** —— 与 waveflow 分叉点）
  - th：`px-3 py-2.5 font-medium` + 对齐可配
  - sortable header：`<button className="inline-flex items-center gap-1 hover:text-stone-900">` + SortIndicator（ArrowUpDown/ArrowUp/ArrowDown `h-3 w-3`，未排序 `text-stone-300`）
- **tbody**：`divide-y divide-stone-100 text-[12.5px] transition-opacity duration-200`；showOverlay 时叠 `pointer-events-none opacity-50`
- **refreshing overlay**（核心特色）：`pointer-events-none absolute inset-x-0 top-0 z-10 h-[2px] overflow-hidden bg-stone-200/30`，内层 `h-full` + `background: linear-gradient(90deg, transparent 0%, #3b82f6 40%, #2563eb 60%, transparent 100%)` + `animation: global-progress 1.1s ease-in-out infinite`
- **skeleton 行**（8 条）：每行 `transition-opacity duration-150`，showSkeleton 时 `opacity-100` 否则 `opacity-0`（透明占位防闪）；cell `px-3 py-3`，内 `div.skeleton h-2 rounded-full` `style.width = `${40 + ((i*7 + c.key.length) % 50)}%``
- **leftBar 列**：td `relative p-0`，内 `span absolute inset-y-0 left-0 w-1`（4px）+ `bg-emerald/red/stone-*` 或 `bg-transparent`（与 waveflow 的 `h-10 w-1` 块式不同，本表用绝对定位铺满行高）
- **数据行**：`group transition-colors hover:bg-stone-50`；onRowClick 时叠 `cursor-pointer`
- **数据 cell**：`px-3 py-3`
- **empty 态**：colSpan 全列 `py-8 text-center text-stone-400`，内 `flex flex-col items-center gap-2` emptyText + emptyExtra
- **双阈值延迟**：`useDelayedFlag(isPlaceholder, 200, 400)` 控骨架；`useDelayedFlag(busy && !isPlaceholder && rows>0, 250, 400)` 控 overlay（消除"翻页闪一下"）
- **ColumnHeader（hover ? 原子）**：`span inline-flex items-center gap-1` + title + 可选 Tooltip 包 `HelpCircle h-3 w-3 cursor-help text-stone-300 hover:text-stone-500 strokeWidth={1.75}`

## 核心代码

```tsx
// 双阈值：骨架延 200ms 显形/至少留 400ms；overlay 延 250ms/至少 400ms
const isPlaceholder = !!loading && rows.length === 0;
const showSkeleton = useDelayedFlag(isPlaceholder, 200, 400);
const busy = !!refreshing || !!loading;
const showOverlay = useDelayedFlag(busy && !isPlaceholder && rows.length > 0, 250, 400);
const overflowX = scrollX || minWidth != null;

// 顶部蓝渐变 refreshing 进度条（已有数据静默换页用）
{showOverlay && (
  <div className="pointer-events-none absolute inset-x-0 top-0 z-10 h-[2px] overflow-hidden bg-stone-200/30">
    <div className="h-full" style={{
      background: 'linear-gradient(90deg, transparent 0%, #3b82f6 40%, #2563eb 60%, transparent 100%)',
      animation: 'global-progress 1.1s ease-in-out infinite',
    }} />
  </div>
)}

<table className={cn('table-fixed', scrollX && minWidth == null ? 'min-w-max' : 'w-full')}
       style={minWidth != null ? { minWidth } : undefined}>
```

## 与 waveflow/data-table-leftbar-shimmer 区分

同源（都是 leftBar + 8 行延迟 shimmer + ArrowUpDown 排序），但 chameleon 版有四处分叉，**AI 选型时按需求挑**：

| 维度 | waveflow/data-table-leftbar-shimmer | chameleon/responsive-overlay-data-table |
|------|------|------|
| **表头样式** | `bg-warm-2/40` 暖底 + `text-[10.5px] uppercase tracking-wider text-stone-500` | **无暖底** + `text-[11px] font-medium text-stone-400`（无大写、无字距） |
| **刷新机制** | 仅 loading→8 行 shimmer 骨架 | 多一路 **refreshing overlay**：已有数据时翻页/改筛选不替骨架，顶部蓝渐变进度条 + body `opacity-50` 静默换页 |
| **延迟阈值** | 单阈值 `useDelayedFlag(isPlaceholder, 200)` | **双阈值**（min-show）：骨架 200/400、overlay 250/400，消除快查询闪烁 + 慢查询瞬灭 |
| **leftBar 实现** | `<div className="h-10 w-1 bg-emerald-500" />` 块式（固定行高 40） | `span absolute inset-y-0 left-0 w-1` 绝对定位铺满**任意行高** |
| **大小屏** | 固定 `w-full table-fixed` | `scrollX`/`minWidth` 自适应：大屏撑满、小屏横滚不压缩列宽 |

- 简单列表（行高固定、不需静默换页）→ 用 waveflow 版
- 业务表（翻页频繁要无闪、行高不定、宽表小屏要横滚）→ 用 chameleon 版

## 适配指南

- 已有数据的重查传 `refreshing`（react-query 接 `isFetching` + `placeholderData: keepPreviousData`），不要清空 rows 走骨架——会闪空表
- 宽表只传 `minWidth` 即自动开横滚（无需再传 scrollX）；大屏列吃余量等分扩展
- 列含义不直观时表头用 `<ColumnHeader title="..." hint="..." />`，hover ? 出 Tooltip

## 反模式

- ❌ loading 时清空 rows——保留上一页避免闪空；用 refreshing overlay 静默换页
- ❌ 表头照搬 waveflow 暖底大写——chameleon 表头是无底色 stone-400，套错会破坏本站表头气质
- ❌ 单阈值延迟——必须双阈值（延迟显形 + 最小展示时长），否则快查询闪、慢查询瞬灭
- ❌ leftBar 用固定高 `h-10`——本表行高不定，用 `absolute inset-y-0` 铺满
- ❌ 小屏压缩列宽——用 `minWidth` + 横滚保列宽
