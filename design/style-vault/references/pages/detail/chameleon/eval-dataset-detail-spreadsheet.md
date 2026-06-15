---
id: pages/detail/chameleon/eval-dataset-detail-spreadsheet
type: page
name: 评测数据集详情 / Airtable 电子表格
description: 评测数据集详情整页（样本/运行/配置 tab + 双 SegmentedControl 视图切换）· 样本走 Airtable 化电子表格（动态{{var}}列 + 行内编辑 + 列显隐菜单 + JSON Popover + 多选批量）
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
- blocks/display/chameleon/eval-spreadsheet-airtable
- components/feedback/chameleon/neon-loader
preview: /preview/pages/detail/chameleon/eval-dataset-detail-spreadsheet
---

# Chameleon Eval Dataset Detail / Airtable Spreadsheet

> 评测域核心页——数据集详情整页。`?tab=` 切「样本 / 运行」两 tab（items 默认不写 query 保地址干净）。顶部 header = 面包屑 + 按 tab 区分的右对齐操作组（样本 tab：导出 / 手工导入 / AI 扩样 / AI 归类 / 从日志采样；运行 tab：导出运行 / 新建评估）。tab 栏用**双 SegmentedControl**（左主 tab + 右视图切换/对比工具）。样本 tab 可在「表格 DataTable / 电子表格 Airtable」两视图切换——**signature = Airtable 化电子表格**：动态 `{{var}}` 输入列（来自 input_payload key 并集）+ 固定「理想回答 / 元数据 / 备注 / 操作」尾列，行内单格失焦保存（乐观更新），系统列默认隐藏 + 「列」菜单勾回（存 localStorage）。

## 视觉特征

- **整页**：`space-y-4(16px)`
- **header**（`flex items-center gap-3`）：返回 Link `inline-flex gap-1 rounded-md px-2 py-1 text-[12.5px] text-stone-500 hover:bg-stone-100` (`ArrowLeft h-3.5 w-3.5` + 「数据集」) → `/` 灰 → 数据集名 `text-[15px] font-medium text-stone-900` + `· N 样本 text-[11.5px] text-stone-500` → `ml-auto` 推开 → 操作 Button 组（`size sm`，导出 ghost / 其余 secondary / 新建评估 primary，icon `mr-1 h-3.5 w-3.5`）
- **tab 栏**（`flex items-center justify-between`）：左 SegmentedControl（样本/运行）；样本 tab 右侧再一个 SegmentedControl（表格/电子表格）；运行 tab 右侧是对比工具栏（提示 `text-[11.5px] text-stone-400` + 「对比所选」secondary + 「清空」ghost）
- **样本来源徽标**（DataTable 视图）：`rounded px-1.5 py-0.5 text-[10.5px]`——AI 扩样 `bg-violet-50 text-violet-700` / 日志采样 `bg-emerald-50 text-emerald-700` / 手工导入 `bg-indigo-50 text-indigo-700` / 手动新增 `bg-stone-100 text-stone-600`

### Airtable 电子表格（signature，`space-y-3`）
- **「列」菜单行**：`flex justify-end` → 「列」ghost 按钮（`Columns3 mr-1 h-3.5 w-3.5` + 隐藏计数 chip `rounded bg-stone-200/70 px-1 text-[10px] text-stone-500「隐 N」`）
- **表格容器**：`relative overflow-x-auto rounded-lg(8px) border border-stone-200/60`，内 `table w-full table-fixed`（minWidth 按列宽算）
- **thead**：`border-b border-stone-200/70 bg-warm-2/40(40% #f4f3ee)`，行 `text-[11px] font-medium text-stone-500`，单元格 `sticky top-0 px-3(12px) py-2.5(10px) text-left font-medium`——选择列（checkbox `h-3.5 w-3.5 accent-stone-700`）+ 动态 `{{var}}` 列（中文映射标签 truncate）+ 固定「理想回答 / 元数据 / 备注」+ 空操作列
- **tbody**：`divide-y divide-stone-100 text-[12.5px]`，行 `group hover:bg-stone-50`，单元格 `px-3 py-2(8px) align-top`
  - 文本单元格（EditableText）：非编辑态 `block w-full truncate text-stone-700 hover:text-stone-900`（空显 `text-stone-300` placeholder）；编辑态 textarea `rounded border border-blue-300 bg-white px-1.5 py-1 text-[12.5px] ring-2 ring-blue-100`
  - JSON 单元格（JsonCellPopover）：`block w-full truncate font-mono text-[11.5px] text-stone-500 hover:text-stone-800`（空显 `{ }`），点开 Popover `w-[28rem]`（查看/编辑双视图）
  - 脱敏单元格：`flex gap-1 truncate text-stone-400`（`Lock h-3 w-3` + preview）
  - 备注（NoteCell）：透明 textarea `rounded border border-transparent px-1 py-0.5 text-[12px] text-stone-600 hover:border-stone-200 focus:border-blue-300 focus:bg-white`
  - 元数据下 summary `mt-0.5 block truncate text-[10.5px] text-stone-400`
  - 删除按钮：`rounded p-1 text-stone-300 opacity-0 group-hover:opacity-100 hover:bg-rose-50 hover:text-rose-600`（`Trash2 h-3.5 w-3.5`）
- **底部**：「新增行」`Button size sm variant secondary`（`Plus mr-1 h-3.5 w-3.5`）
- **AI 扩样**走 ai-generate-studio（候选卡 + NeonLoader），AI 归类 pending 时按钮内嵌 `NeonLoader size xs`

## 核心代码

```tsx
// 双 SegmentedControl：主 tab + 视图
<div className="flex items-center justify-between">
  <SegmentedControl value={tab} onChange={setTab} options={[{value:'items',label:'样本'},{value:'runs',label:'运行'}]} />
  {tab === 'items' && <SegmentedControl value={itemsView} onChange={setItemsView}
    options={[{value:'table',label:'表格'},{value:'sheet',label:'电子表格'}]} />}
</div>

// Airtable thead + 行内编辑单元格
<thead className="border-b border-stone-200/70 bg-[var(--color-warm-2)]/40">
  <tr className="text-[11px] font-medium text-stone-500">
    {visibleKeys.map(k => <th className="sticky top-0 px-3 py-2.5 text-left font-medium">{getColumnLabel(k)}</th>)}
    <th>理想回答</th><th>元数据</th><th>备注</th><th />
  </tr>
</thead>

// 编辑态 textarea：蓝边 + 蓝 ring
className="w-full resize-none rounded border border-blue-300 bg-white px-1.5 py-1 text-[12.5px] ring-2 ring-blue-100 outline-none"
```

## 适配指南

- dsId 全程保 string——snowflake 64-bit 超 MAX_SAFE_INTEGER，`Number()` 会精度丢失
- tab 同步 URL（`?tab=runs`），items 默认不写 query；view 切换走本地 state（表格密集场景看 DataTable，逐格编辑看 Airtable）
- 电子表格动态列来自 `input_payload` 顶层 key 并集（`inferVarKeys`），系统列（hash/length/token_count）默认隐藏存 localStorage（按数据集隔离 key，避免 A 集偏好污染 B 集）
- 行内编辑乐观更新：单格失焦/Enter 提交（值变才发请求），key 用 `item.id + 当前值` 确保换行/换值 remount
- 多选 checkbox 用 `accent-stone-700`（不染主题色，保持工具感）

## 反模式

- ❌ dsId 转 Number——雪花 ID 精度丢失（全站铁律）
- ❌ 电子表格表头硬编码列名——走 `getColumnLabel` 中文映射 + 未知 key 兜底
- ❌ 全字段编辑只给一种入口——Airtable 行内编辑 + 全字段抽屉 + 批量导入三者互补不替代
- ❌ 多选 checkbox 染主题色——用 `accent-stone-700` 中性工具色
- ❌ 把样本来源徽标做大/染满——`text-[10.5px]` 软色阶 `-50/-700`，不抢样本内容
