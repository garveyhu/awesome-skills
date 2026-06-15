---
id: pages/list-table/waveflow/job-log-batch-select
type: page
name: 日志列表（批量选择 + 清理）
description: heavy filter + 自定义 toolbar (任务ID/描述 search + 执行器 select + 状态 select + datetime-range + 批量删 + 清理日志 dialog) + 表格首列 checkbox + indeterminate
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, industrial]
  mood: [serious]
  stack: [shadcn-radix]
uses:
  - blocks/display/waveflow/canonical-table-shell
  - components/inputs/waveflow/datetime-range-presets
  - components/tags-badges/waveflow/code-status-badge
preview: /preview/pages/list-table/waveflow/job-log-batch-select
---

# Waveflow Job Log Batch-Select

> waveflow 日志列表 (`/log`)——最复杂的列表页：**4 个 input/select filter**（任务 ID + 任务描述 input + 执行器 select + 状态 select + DateTimeRange）+ **首列 checkbox**（含 indeterminate 半选态）+ **批量删按钮**（仅选中后显示）+ **清理日志独立 dialog**（按"清理类型"枚举批量物理删）+ 每行 **执行码 CodeBadge**（200/0/500/null）+ **跳日志详情 / 终止任务** 操作。

## 视觉要点

1. **5 个 filter 走自定义 toolbar 而非 TableToolbar 默认槽**：因为有 DateTimeRangePicker + 批量删按钮等非标准控件，TableToolbar 装不下
2. **首列 checkbox 40px / center**：表头 checkbox 支持 `indeterminate`（已选少于全部 = 半选）
3. **CodeBadge 嵌入 "执行码" 列**：200 emerald / 0 blue / 500+ red / null stone
4. **批量选 → 批量删按钮 ymeijiang**：未选中时按钮不显示；选中后显示 + count `已选 N`
5. **清理日志 dialog 独立**：Header "清理日志" + 锁定"执行器"/"任务"= 全部（disabled input）+ "清理类型" Select（保留 7 / 30 / 90 天 / 全部）+ danger 确认
6. **URL `?jobId=xxx` hydration**：用户从其它页跳转过来携带的 jobId 自动填进搜索 + 重查
7. **批量选 reset on filter 改变**：任何 filter 修改都 `setSelectedLogs([])` —— 避免跨页选错

## 关键代码片段

```tsx
// header checkbox 含 indeterminate
{
  key: 'select',
  header: <Checkbox checked={allChecked ? true : someChecked ? 'indeterminate' : false} onCheckedChange={v => toggleSelectAll(v === true)} />,
  width: 40, align: 'center',
  render: r => <Checkbox checked={selectedLogs.includes(r.id)} onCheckedChange={v => toggleSelect(r.id, v === true)} />,
}

// CodeBadge 列
{
  key: 'handleCode',
  header: '执行码',
  width: 90,
  render: r => <CodeBadge code={r.handleCode} />,
}

// 批量删按钮
{selectedLogs.length > 0 && (
  <Button variant="danger-outline" size="sm" onClick={onBatchDelete}>
    <Trash2 className="h-3.5 w-3.5" /> 删除选中（{selectedLogs.length}）
  </Button>
)}
```

## 适配指南

- 富文本日志备注用 DOMParser 净化 + 限定 allowedTags（DIV/BR/SPAN/P/B/STRONG/I/EM/U/CODE/PRE/SMALL）+ allowedStyles（color/font-weight/font-style/text-decoration/background-color/font-size），防 XSS
- 跨页保留选中：通常**不**保留（用户切页大概率是要改查 query）
- DateTimeRangePicker 配 6 个预设：今天 / 昨天 / 近 7 天 / 近 30 天 / 本月 / 上月
- 清理日志 dialog 是物理删除——必须 danger 确认 + 描述明确"不可恢复"

## 反模式

- ❌ 删按钮永远显示—— 用户没选时按钮 disabled 也容易误点
- ❌ checkbox 不支持 indeterminate—— "已选 N 条但不是全部" 视觉不明显
- ❌ 富文本备注不净化—— XSS 漏洞
