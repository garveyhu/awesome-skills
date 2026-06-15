---
id: blocks/display/waveflow/data-table-leftbar-shimmer
type: block
name: 左状态条 + 延迟 shimmer 表格
description: DataTable 完整体 - 4px 左状态条 + 8 行延迟 200ms shimmer 骨架 + warm-2 sticky 表头 + ArrowUpDown 排序 + zebra-free hover + divide stone-100
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, industrial]
  mood: [calm, serious]
  stack: [shadcn-radix]
uses:
  - tokens/iconography/waveflow/engineer-detail-classes
  - tokens/border/waveflow/translucent-stone-system
  - components/typography-atoms/waveflow/meta-caps-mono-pair
preview: /preview/blocks/display/waveflow/data-table-leftbar-shimmer
---

# Waveflow DataTable LeftBar + Shimmer

> waveflow 表格组件（`components/table/DataTable.tsx`）——通用泛型 + 4 个 waveflow 特色：**4px 左边状态条**（leftBar callback 返 `bg-emerald/red/stone`）/ **8 行延迟 200ms shimmer 骨架**（200ms 内回数据全程透明不闪）/ **sticky warm-2 thead**（10.5px UPPERCASE tracking-wider）/ **ArrowUpDown sortable headers**。

## 视觉特征

- **外框**：`overflow-hidden rounded-lg border border-stone-200/60`
- **table**: `w-full table-fixed`（固定列宽，靠 colgroup 控）
- **thead**：`bg-[var(--color-warm-2)]/40`
  - tr: `text-[10.5px] uppercase tracking-wider text-stone-500`
  - th: `px-3 py-2 font-medium` + 左中右对齐可配
  - sortable header: `<button className="inline-flex items-center gap-1 hover:text-stone-900">` + ArrowUpDown/Up/Down 12px
- **tbody**：`divide-y divide-stone-100 text-[12.5px]`
- **leftBar 列**（可选，4px 宽）：
  - colgroup 第一列 `style={{ width: 4 }}`
  - 每行 td 内 `<div className="h-10 w-1 bg-emerald-500" />` (running) / `bg-red-500` (error) / `bg-stone-300` (stopped) / `bg-transparent` (无状态)
- **row hover**: `hover:bg-stone-50/60` + `group` 类（给 hover 内行内按钮露出来用）
- **cell padding**: `px-3 py-2.5`
- **shimmer 骨架行**：
  - 表格 200ms 内透明渲染 8 占位行；超 200ms 才显形 `opacity-100`
  - 每个 cell 内：`<div className="skeleton h-2 rounded-full" style={{ width: `${40 + ((i*7 + c.key.length) % 50)}%` }} />`
  - **rounded-full pill 形态 + 暖灰横向 shimmer 波**（不是 animate-pulse opacity）—— 走全局 `.skeleton` 类：`linear-gradient(90deg, #ebe9e3 0%, #f5f4ee 50%, #ebe9e3 100%) + background-size 400px + animation: shimmer 1.6s ease-in-out infinite`，让"波"从左划到右更优雅
  - height **8px (h-2)**：比之前 h-3 (12px) 更细 pill，配合 rounded-full 视觉是"会动的占位线"
  - 列宽伪随机（40-90%）
- **empty 态**：colSpan 全列 + `py-8 text-center text-stone-400` + `flex-col items-center gap-2 emptyText + emptyExtra`

## 关键代码

```tsx
const showSkeleton = useDelayedFlag(isPlaceholder, 200);

<div className="overflow-hidden rounded-lg border border-stone-200/60">
  <table className="w-full table-fixed">
    <colgroup>{hasLeftBar ? <col style={{ width: 4 }} /> : null}{columns.map(c => <col key={c.key} style={c.width ? { width: c.width } : undefined} />)}</colgroup>
    <thead className="bg-[var(--color-warm-2)]/40">
      <tr className="text-[10.5px] uppercase tracking-wider text-stone-500">
        {hasLeftBar ? <th className="p-0" /> : null}
        {columns.map(c => <th className="px-3 py-2 font-medium">{sortable ? <button>{c.header} <SortIndicator /></button> : c.header}</th>)}
      </tr>
    </thead>
    <tbody className="divide-y divide-stone-100 text-[12.5px]">
      {isPlaceholder
        ? Array.from({ length: 8 }).map((_, i) => <SkeletonRow showSkeleton={showSkeleton} />)
        : empty
          ? <EmptyRow />
          : rows.map(row => <DataRow row={row} bar={leftBar?.(row)} />)
      }
    </tbody>
  </table>
</div>
```

## 适配指南

- 不要为 loading 单独清空 rows——保留原数据避免闪烁；200ms 内回数据全程透明骨架（用户感觉"瞬间响应"）
- leftBar 仅用于"任务/集合"语义场景；普通数据表（项目 / 用户）省略
- DataTableColumn 必填 `key + header + render`；`width` 不传则自适应
- ID 列用 `cellClassName: 'font-mono text-stone-500 tnum'`，cron / 时间用 `'font-mono text-[11.5px] text-stone-600 tnum'`

## 反模式

- ❌ loading 时直接清空 rows——会闪空表
- ❌ shimmer 用 `animate-pulse + bg-stone-100`——只闪 opacity 不优雅，要用 `.skeleton` 横向 gradient wave
- ❌ shimmer 占位用矩形 (`rounded` / `rounded-md`)——必须 `rounded-full` pill 形态
- ❌ shimmer 占位高度 ≥ 12px—— 太"实"像数据条；用 `h-2` (8px) 才像"占位线"
- ❌ shimmer 用 `bg-gray-200` 渐变——和暖底色温不和谐（用 #ebe9e3 → #f5f4ee → #ebe9e3 三段）
- ❌ 表头加深色 bg—— 破坏全站轻量感
- ❌ row 加 zebra (`even:bg-stone-50`)—— waveflow 故意不做斑马纹（密度感够，斑马反而碎）
- ❌ leftBar 用饱和色 (`bg-red-600`)——4px 窄条用 500 就够，600 太重
