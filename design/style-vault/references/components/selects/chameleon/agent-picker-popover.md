---
id: components/selects/chameleon/agent-picker-popover
type: component
name: 分页类别智能体选择器
description: 左类别竖栏 + 右搜索 + 无限滚动分页列表的双栏 popover 单选器，行带图标/名称/mono key 副行/选中 Check
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
- components/inputs/waveflow/blue-focus-input
- tokens/palettes/waveflow/warm-paper-ink-blue
preview: /preview/components/selects/chameleon/agent-picker-popover
---

# 分页类别智能体选择器

> Chameleon 全站智能体筛选下拉——一个 `!w-[420px]` 双栏 popover：左侧 `w-24` 应用类别竖栏（全部 / 代码 / 对话编排 / 流程编排 / 外部），右侧搜索框 + 无限滚动分页列表（向下触底 -48px 加载下一页）。每行图标（自定义 img 或 `Bot` 兜底）+ 名称 + mono key 副行 + 选中 `Check`。触发器 `h-7` 紧凑按钮显选中名 / 「全部应用」。waveflow multi-select-popover 是通用多选，本件是带类别栏 + 分页 + 搜索的单选应用选择器，故 new。

## 视觉特征

### 触发器
- `flex h-7 items-center justify-between gap-1 rounded-md border border-stone-200 bg-white px-2 text-[12px] text-stone-700 hover:border-stone-300`，`style={{ width: 168 }}`
- `span.truncate` 标签 + `ChevronDown h-3.5 w-3.5 shrink-0 text-stone-400`

### Popover 容器
- `PopoverContent align="start"` 覆写 `!w-[420px] !p-0`，内 `flex h-[340px]`

### 左·类别竖栏
- `w-24 shrink-0 space-y-0.5 overflow-y-auto border-r border-stone-100 p-1.5`
- 每项 `w-full rounded px-2 py-1.5 text-left text-[12px]`，active `bg-blue-50 font-medium text-blue-700`，idle `text-stone-600 hover:bg-stone-100`

### 右·搜索 + 列表
- 搜索 `relative shrink-0 p-1.5`：`Search` 绝对 `left-3.5 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-stone-400` + Input 覆写 `!h-7 pl-7 text-[12px]`
- 列表 `min-h-0 flex-1 overflow-y-auto p-1.5 pt-0`，`onScroll` 触底 -48px 加载
- Row `flex w-full items-center gap-2 rounded px-2 py-1.5 text-left hover:bg-stone-100`，active 加 `bg-blue-50`
  - 图标 `span.shrink-0`：`img h-4 w-4 rounded object-cover` 或 `Bot h-3.5 w-3.5 text-stone-400`
  - 标题 `block truncate text-[12px] text-stone-800`，key 副行 `block truncate font-mono text-[10px] text-stone-400`
  - active `Check h-3.5 w-3.5 shrink-0 text-blue-600`
- 加载态 `flex items-center justify-center gap-1.5 py-2 text-[11px] text-stone-400` + `Loader2 h-3 w-3 animate-spin`「加载中…」
- 空态 `py-6 text-center text-[12px] text-stone-400`「无匹配应用」
- 到底 `py-2 text-center text-[10.5px] text-stone-300`「没有更多了」

## 核心代码

```tsx
<PopoverContent align="start" className="!w-[420px] !p-0">
  <div className="flex h-[340px]">
    {/* 左：类别栏 */}
    <div className="w-24 shrink-0 space-y-0.5 overflow-y-auto border-r border-stone-100 p-1.5">
      {CATEGORIES.map(c => (
        <button className={category === c.value
          ? 'w-full rounded px-2 py-1.5 text-left text-[12px] bg-blue-50 font-medium text-blue-700'
          : 'w-full rounded px-2 py-1.5 text-left text-[12px] text-stone-600 hover:bg-stone-100'}>
          {c.label}
        </button>
      ))}
    </div>
    {/* 右：搜索 + 列表 */}
    <div className="flex min-w-0 flex-1 flex-col">
      <div className="relative shrink-0 p-1.5">
        <Search className="absolute top-1/2 left-3.5 h-3.5 w-3.5 -translate-y-1/2 text-stone-400" />
        <Input className="!h-7 pl-7 text-[12px]" placeholder="搜索名称 / key" />
      </div>
      <div ref={listRef} onScroll={onScroll} className="min-h-0 flex-1 overflow-y-auto p-1.5 pt-0">
        {/* Row: icon + name + mono key 副行 + Check */}
      </div>
    </div>
  </div>
</PopoverContent>
```

## 适配指南
- 触底加载阈值 `scrollTop + clientHeight >= scrollHeight - 48`，配 `useInfiniteQuery`（page_size 20）
- 空值「全部应用 / 不关联」行用 `Bot` 图标、`allLabel` 文案可配（筛选场景「全部应用」/ 绑定场景「不关联」）
- 触发器记下点选项的展示名（picked state），外部仅给 agent_key 时回退显示 key
- 类别栏选中只缩当前列表，不重置搜索词

## 反模式
- ❌ 类别栏选中态用边框 / 加粗灰 —— 是 `bg-blue-50 + text-blue-700 + font-medium` 蓝底
- ❌ Row 选中只换底不给 Check —— `bg-blue-50` + 右侧 `Check text-blue-600` 双重指示
- ❌ key 副行用普通 sans —— 必须 `font-mono text-[10px] text-stone-400`，与名称（sans 12px）拉开层级
- ❌ Popover 用默认宽 —— 必须 `!w-[420px] !p-0`（覆盖 PopoverContent 默认 padding），否则双栏挤不开
