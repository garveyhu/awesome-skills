---
id: components/display/chameleon/json-viewer-cell
type: component
name: JSON 折叠单元格 + 零依赖 JSON 树
description: 表格 cell 级 JSON 折叠（短文本直显/长文本单行摘要点击展开 mono pre）+ 零依赖 JSON 树查看器（缩进折叠/类型着色/搜索高亮/逐节点复制）
platforms:
- web
theme: light
tags:
  aesthetic:
  - industrial
  - minimal
  mood:
  - serious
  stack:
  - shadcn-radix
uses:
- tokens/iconography/waveflow/engineer-detail-classes
- tokens/palettes/waveflow/warm-paper-ink-blue
preview: /preview/components/display/chameleon/json-viewer-cell
---

# JSON 折叠单元格 + 零依赖 JSON 树

> Chameleon 两个层级的只读结构数据展示件：① **JsonCell**——表格 cell 级，短文本直显、长文本/对象折叠为单行 mono 摘要（80 字），点击展开缩进 pre，脱敏字段 `{hash,length,preview}` 优先显 preview；② **JsonViewer**——整面板级，自实现零依赖 JSON 树，缩进折叠 + 类型着色（string 翠绿 / number 天蓝 / boolean 紫 / null 灰）+ 搜索过滤（命中 amber 高亮 + 隐藏不匹配子树 + 命中自动展开）+ 整体/逐节点复制 + maxHeight 滚动。

## 视觉特征

### JsonCell（表格单元格折叠）

- null：`<span className="text-stone-400">—</span>`
- 短 string（≤80）：`text-stone-700`（直显，不折叠）
- 折叠触发按钮：`block max-w-full truncate text-left font-mono text-[11px] text-stone-600 hover:text-stone-900`
  - open 时显 `▾ 收起`（preview 中用 `ChevronDown` lucide 替代 ▾）；else 显 summary（`pickPreview` 取对象 `.preview` 截 100 字，否则 oneLine 截 80 + `…`）
- 展开 pre：`mt-1 max-h-64 overflow-auto rounded-md bg-stone-50 p-2 font-mono text-[11px] leading-relaxed text-stone-700`（max-h-64=256px，radius md=6px，p-2=8px）

### JsonViewer（零依赖树）

- 外框：`flex flex-col overflow-hidden rounded-md border border-stone-200 bg-white`（radius 6px）
- 搜索条（searchable）：`flex items-center gap-2 border-b border-stone-200 bg-stone-50/60 px-2 py-1.5`
  - `Search` 图标 `h-3.5 w-3.5 text-stone-400`（14px）
  - input：`flex-1 bg-transparent text-[12.5px] outline-none placeholder:text-stone-400`
  - 复制按钮：`inline-flex items-center gap-1 rounded px-1.5 py-1 text-[11.5px] text-stone-600 hover:bg-stone-200 hover:text-stone-900`；成功显 `Check h-3 w-3 text-emerald-600` + 「已复制」，否则 `Copy h-3 w-3` + 「复制」
- 内容区：`overflow-auto p-2 font-mono text-[12px] leading-snug`，`style.maxHeight` 默认 `'70vh'`
- 节点缩进：`paddingLeft = depth * 12`（每层 12px）
- 值着色（关键签名）：
  - string `text-emerald-700`（值用 `JSON.stringify` 带引号）
  - number `text-sky-700`
  - boolean `text-purple-700`
  - null / undefined `text-stone-400`
  - key `text-stone-700`（带引号）
  - 括号 `{ } [ ]` `text-stone-500`
  - 折叠摘要 `text-stone-400`（`N items` / `N keys`）
- 展开/折叠按钮：`mr-1 text-stone-400 hover:text-stone-600`，open `ChevronDown h-3 w-3` / closed `ChevronRight h-3 w-3`（12px）
- 逐节点复制 CopyButton：`ml-2 hidden rounded p-0.5 text-stone-400 hover:bg-stone-100 hover:text-stone-700 group-hover:inline-flex`（**hover 行才出现**），`Check`/`Copy h-3 w-3`
- 搜索高亮：`<mark className="rounded bg-amber-100 px-0.5 text-stone-900">`
- 默认展开规则：`forceExpand || (defaultExpanded && depth < 3) || (query && hasMatch)`——顶层默认展开前 3 层；搜索时命中子树强制展开
- lucide：`Check / ChevronDown / ChevronRight / Copy / Search`

## 核心代码

```tsx
// JsonCell：长文本折叠
const summary = preview ?? (oneLine.length <= 80 ? oneLine : oneLine.slice(0, 80) + '…');
<button onClick={() => setOpen(o => !o)}
  className="block max-w-full truncate text-left font-mono text-[11px] text-stone-600 hover:text-stone-900">
  {open ? '▾ 收起' : summary}
</button>
{open && (
  <pre className="mt-1 max-h-64 overflow-auto rounded-md bg-stone-50 p-2 font-mono text-[11px] leading-relaxed text-stone-700">
    {full}
  </pre>
)}

// JsonViewer：类型着色
if (typeof value === 'string')  return <span className="text-emerald-700">{highlight(JSON.stringify(value), query)}</span>;
if (typeof value === 'number')  return <span className="text-sky-700">{value}</span>;
if (typeof value === 'boolean') return <span className="text-purple-700">{String(value)}</span>;
if (value === null)             return <span className="text-stone-400">null</span>;

// 缩进 + 折叠摘要
<div style={{ paddingLeft: depth * 12 }}>
  <span className="text-stone-500">{openBr}</span>
  {!expanded && <span className="ml-1 text-stone-400">{isArr ? `${n} items` : `${n} keys`}</span>}
</div>
```

## 适配指南

- 表格里塞 JSON / 长文本用 `JsonCell`（cell 级折叠，max-h-64 限高）；详情面板/抽屉里展示完整 trace input/output 用 `JsonViewer`（树 + 搜索）
- 脱敏字段约定 `{hash,length,preview}`——`pickPreview` 自动取 `preview` 字段截 100 字作摘要，避免在表格里展开敏感原文
- JsonViewer 搜索是「过滤 + 高亮」双效——不匹配子树直接 `return null` 隐藏，命中节点 `forceExpand` 自动展开内层
- 全部 `font-mono` + `text-[11px]`/`text-[12px]`——结构数据用等宽字体对齐，比正文小一档不抢戏

## 反模式

- ❌ 引第三方 JSON 树库（react-json-view 等）——Chameleon 故意零依赖自实现，体积小且类型着色可控
- ❌ JsonCell 展开 pre 不限高——长 JSON 撑爆表格行；必须 `max-h-64 overflow-auto`
- ❌ 类型色乱配——string=emerald / number=sky / boolean=purple / null=stone 是固定语义，复用别改
- ❌ 逐节点复制按钮常驻显示——用 `group-hover:inline-flex` 仅 hover 行才出现，否则每行一堆图标很吵
