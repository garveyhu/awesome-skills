---
id: blocks/display/chameleon/eval-spreadsheet-airtable
type: block
name: 评测样本电子表格（Airtable 化）
description: 动态 {{var}} 输入列 + 固定「理想回答/元数据/备注/操作」列的行内可编辑表格 - 单格失焦保存 / 长值省略 hover Tooltip / 复杂值 JSON Popover 双视图 / 系统列默认隐藏可勾回 / 脱敏行 Lock 只读 / 底部「+新增行」
platforms:
- web
theme: light
tags:
  aesthetic:
  - minimal
  - industrial
  mood:
  - calm
  - serious
  stack:
  - shadcn-radix
uses:
- components/inputs/waveflow/blue-focus-input
- tokens/palettes/waveflow/warm-paper-ink-blue
preview: /preview/blocks/display/chameleon/eval-spreadsheet-airtable
---

# 评测样本电子表格（Airtable 化）

> 按 DataTable 视觉语言自建的 **editable variant**：动态 `{{var}}` 输入列（来自 `input_payload` 顶层 key 并集，走 `getColumnLabel` 中文映射）+ 固定尾列「理想回答 / 元数据 / 备注 / 操作」。单格失焦乐观保存、长值省略 hover Tooltip 看全、复杂值点开 JSON Popover「查看 ↔ 编辑」双视图、系统列（hash/length/token_count）默认隐藏可勾回（localStorage 按数据集隔离）、采样脱敏行 Lock 只读、底部「+新增行」。waveflow 无电子表格，全新。

## 视觉特征

- **外层**：`relative overflow-x-auto rounded-lg(8) border border-stone-200/60` —— 横向自适应滚，列窄系统列/列宽业务文本列
- **table**：`w-full table-fixed`，`style.minWidth` = 动态列宽和 + EXPECTED + META + NOTE + 48（操作列）+ 可选 36（多选列）
- **colgroup 列宽**：可选 36 多选列 / 动态列各 `getColumnWidth(k)` / EXPECTED_COL_WIDTH / META_COL_WIDTH / NOTE_COL_WIDTH / 48 操作列
- **thead**：`border-b border-stone-200/70 bg-[var(--color-warm-2)]/40`（warm-2 #f4f3ee 透 40%）
  - tr：`text-[11px] font-medium text-stone-500`
  - th：`sticky top-0 px-3 py-2.5 text-left font-medium`，列名走 `getColumnLabel`（user_input→用户输入），与原 key 不同时 hover Tooltip 显原 key
- **tbody**：`divide-y divide-stone-100 text-[12.5px]`
  - 行：`group hover:bg-stone-50`
  - td：`px-3 py-2 align-top`
- **EditableText（标量/空格）**：
  - 非编辑：`block w-full truncate text-left text-stone-700 hover:text-stone-900`，空值占位 `text-stone-300`；有值时 hover Tooltip（`block max-w-xs break-words`）看全文
  - 编辑：`textarea autoFocus` `w-full resize-none rounded border border-blue-300 bg-white px-1.5 py-1 text-[12.5px] leading-snug ring-2 ring-blue-100 outline-none`，rows = clamp(1,6, 换行数)；**Enter 提交 / Shift+Enter 换行 / Esc 还原**
- **JsonCellPopover（对象/数组/meta）**：
  - 触发：`block w-full truncate text-left font-mono text-[11.5px] text-stone-500 hover:text-stone-800`，显 `text.replace(/\s+/g,' ').slice(0,60)` 或 `{ }`
  - PopoverContent：`w-[28rem]`，头部 label `text-[11.5px] font-medium text-stone-600` + 右侧「查看 ↔ 编辑」切换 `text-[11px] text-stone-500 hover:text-stone-800`
  - 查看态：`JsonViewer` 语法高亮（`maxHeight="20rem"`）；编辑态：`JsonEditor` + 底部 ghost「取消」+ primary「保存」（非法 JSON toast.error）
- **redacted（采样脱敏）**：`flex items-center gap-1 truncate text-stone-400` + `Lock h-3 w-3 shrink-0`，hover Tooltip「采样脱敏，不可直接编辑：…」
- **NoteCell（备注）**：`textarea rows={1}` `w-full resize-none rounded border border-transparent bg-transparent px-1 py-0.5 text-[12px] leading-snug text-stone-600 outline-none transition placeholder:text-stone-300 hover:border-stone-200 focus:border-blue-300 focus:bg-white`；下方 `metaSummary` `text-[10.5px] text-stone-400`
- **删除**：`rounded p-1 text-stone-300 opacity-0 transition group-hover:opacity-100 hover:bg-rose-50 hover:text-rose-600` + `Trash2 h-3.5 w-3.5`（默认隐形，行 hover 才露）
- **ColumnMenu**：DropdownMenu 触发 ghost Button + `Columns3 mr-1 h-3.5 w-3.5` +「列」；隐藏数 > 0 时 chip `ml-1 rounded bg-stone-200/70 px-1 text-[10px] text-stone-500「隐 N」`；菜单项 `text-[12.5px] text-stone-700 hover:bg-stone-100`，显示态 `Eye text-stone-500` / 隐藏态 `EyeOff text-stone-300`
- **新增行**：`Button size="sm" variant="secondary"` + `Plus mr-1 h-3.5 w-3.5`，pending 显「新增中…」

## 核心代码

```tsx
// 编辑态 textarea：Enter 提交 / Shift+Enter 换行 / Esc 还原
<textarea
  autoFocus
  rows={Math.min(6, Math.max(1, draft.split('\n').length))}
  onKeyDown={e => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); (e.target as HTMLTextAreaElement).blur(); }
    if (e.key === 'Escape') { setDraft(initial); setEditing(false); }
  }}
  className="w-full resize-none rounded border border-blue-300 bg-white px-1.5 py-1 text-[12.5px] leading-snug ring-2 ring-blue-100 outline-none"
/>

// Cell 分派：脱敏 Lock 只读 / json Popover / scalar 行内文本（key 含值，确保换值 remount）
if (cell.kind === 'redacted') return <LockedCell />;
if (cell.kind === 'json') return <JsonCellPopover .../>;
return <EditableText key={`${item.id}:${initial}`} initial={initial} placeholder="—" onCommit={onScalar} />;

// 隐藏列偏好按数据集隔离存 localStorage（A 集偏好不污染 B 集默认视图）
const hiddenColsStorageKey = (id) => `chm:dataset-sheet:hidden-cols:${id}`;
```

## 适配指南

- 行内编辑单格 **失焦/Enter 才发请求**（值真变了才发），乐观更新；外部值变化由父级 `key={`${item.id}:${value}`}` 重挂同步
- 系统列默认隐藏靠 `defaultHiddenColumns(columnKeys)`，用户勾回后写 localStorage；不同数据集列结构不同，storage key 必须带 datasetId
- 与「全字段抽屉 / 批量导入」并存，互补不替代——电子表格只管高频单格快编
- 空 dataset 给默认占位列 `['user_input']`，让「+新增行」有处落值

## 反模式

- ❌ 每次 onChange 就发请求——必须失焦/Enter 提交，且值未变不发
- ❌ 隐藏列偏好用全局 localStorage key——A 集偏好会污染 B 集默认视图
- ❌ 复杂值（对象/数组）也用 textarea 直编——用 JsonCellPopover 双视图，避免在窄格里改坏结构
- ❌ 删除按钮常驻可见——靠 `opacity-0 group-hover:opacity-100` 行 hover 才露，保持密度感
