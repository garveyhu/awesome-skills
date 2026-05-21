---
id: blocks/filters/waveflow/table-toolbar-tri
type: block
name: 表格三段工具栏
description: title (左) + 右侧 search icon-prefix + N 个 h-7 select filter + extra slot (按钮 / MultiSelect)
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm]
  stack: [shadcn-radix]
uses:
  - components/inputs/waveflow/blue-focus-input
preview: /preview/blocks/filters/waveflow/table-toolbar-tri
---

# Waveflow Table Toolbar (TableToolbar)

> waveflow 通用表格工具栏 (`components/table/TableToolbar.tsx`) ——三段式：**title 左** / **search 中** / **N filters + extra 右**。所有控件 h-7 紧凑型，title 13.5px font-semibold。`onRefresh` 配合 React effect 重跑（值不变时也能强制刷新）。

## 页面骨架

```tsx
<div className="mb-2.5 flex items-center gap-2">
  {title && <h3 className="text-[13.5px] font-semibold text-stone-900">{title}</h3>}
  <div className="ml-auto flex flex-wrap items-center gap-1.5">

    {search && (
      <div className="relative">
        <button onClick={() => { search.onSubmit(search.value); search.onRefresh?.(); }}
          className="absolute left-1.5 top-1/2 z-10 -translate-y-1/2 rounded p-0.5 text-stone-400 hover:bg-stone-100 hover:text-stone-700">
          <Search className="h-3 w-3" />
        </button>
        <Input
          className="!h-7 pl-6 text-[12px]"
          style={{ maxWidth: search.width ?? 180 }}
          placeholder={search.placeholder}
          value={search.value}
          onChange={e => search.onChange(e.target.value)}
          onKeyDown={e => { if (e.key === 'Enter') search.onSubmit(search.value); }}
        />
      </div>
    )}

    {filters?.map(f => (
      <Select value={f.value} onValueChange={f.onChange}>
        <SelectTrigger className="!h-7 whitespace-nowrap !text-[12px]" style={{ width: f.width ?? 110 }}>
          <span className="truncate">{f.value === 'all' ? f.placeholder : optLabel}</span>
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">全部</SelectItem>
          {f.options.map(o => <SelectItem value={o.value}>{o.label}</SelectItem>)}
        </SelectContent>
      </Select>
    ))}

    {extra}
  </div>
</div>
```

## 视觉特征

- **gap-1.5 (6px)**：filter 之间紧凑
- **`!h-7`** 覆写 Input / Select 默认 h-8——更紧凑
- **search 默认 width 180px**：可压窄到 130-200 范围
- **filter trigger default width 110px**：装得下"任务类型" / "执行状态" 等 4 字
- **search "submit on icon click" + "submit on Enter"**：双触发；input 失焦不 submit（避免误提交）
- **onRefresh 自增计数器**：搜索词没变时也能重新拉接口（点搜索图标 = 强制 refresh）

## 适配指南

- 复杂场景额外 filter（如项目 MultiSelect）走 extra：`extra={<><MultiSelect /><Button variant="primary" size="sm">+ 添加</Button></>}`
- 搜索是受控：输入框 local state 与提交 keyword 解耦，避免输入逐字触发请求
- filter 改变后必跟 `setPage(1)` —— 否则跳到不存在的分页

## 反模式

- ❌ 工具栏靠左排（filter / search 在 title 后）—— 视觉重心混乱
- ❌ filter trigger 宽度不固定—— 切换 placeholder 时跳
- ❌ search 不带 icon 前缀—— 失去"这是搜索"的视觉
