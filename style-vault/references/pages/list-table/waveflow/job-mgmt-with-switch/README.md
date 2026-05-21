---
id: pages/list-table/waveflow/job-mgmt-with-switch
type: page
name: 任务管理列表（带行 Switch + LeftBar）
description: jobInfo / jobTemplate 共用 - TableToolbar 三 filter (类型/执行状态/开关状态) + MultiSelect 项目 + DataTable 含 LeftBar (emerald/red/stone) + Switch + GlueTypeBadge + 最近触发 mono + MoreHorizontal dropdown
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, industrial]
  mood: [serious]
  stack: [shadcn-radix]
uses:
  - blocks/display/waveflow/canonical-table-shell
  - blocks/display/waveflow/data-table-leftbar-shimmer
  - components/toggles/waveflow/emerald-switch
  - components/tags-badges/waveflow/glue-type-badge-duo
  - components/selects/waveflow/multi-select-popover
preview: /preview/pages/list-table/waveflow/job-mgmt-with-switch
---

# Waveflow Job Management with Switch

> waveflow 任务列表的完整形态 (`/job/jobInfo` 和 `/job/jobTemplate`)——比 canonical-section-list 多 4 个东西：**3 个 filter dropdown**（类型 / 执行状态 / 开关状态）+ **MultiSelect 项目筛选**（带 search + count chip）+ **DataTable LeftBar**（任务派生状态：error red / running emerald / stopped stone）+ **行内 Switch**（运行 / 暂停 + 乐观更新）+ **MoreHorizontal dropdown**（终止 / 删除 / 跳日志列表）。

## 适用场景

| 路由 | 实际名称 | 差异 |
|---|---|---|
| `/job/jobInfo` | 任务管理 | 完整 - 含 cron / 触发时间 / 执行码列 |
| `/job/jobTemplate` | 任务模板 | 简化 - 不显示 cron 列；额外"NextTriggerPopover" 和 "RegisterNodePopover" 内嵌 |

## 页面骨架

```tsx
<div className="h-full px-6 py-4">
  <section className="rounded-xl border border-stone-200/40 bg-[var(--color-paper)] p-5 shadow-[var(--shadow-soft)]">
    <TableToolbar
      title="任务管理"
      search={{ value, onChange, onSubmit, onRefresh, placeholder: '搜索任务' }}
      filters={[
        { value: glueType,    onChange, placeholder: '任务类型', options: TYPE_OPTIONS    },  // FETCH/TRANS/PUSH/COMPLEX/BEAN/Shell/Python
        { value: runFilter,   onChange, placeholder: '执行状态', options: RUN_STATUS_OPTIONS },  // success/fail/running/never
        { value: switchFilter, onChange, placeholder: '开关状态', options: SWITCH_OPTIONS  },  // running/stopped
      ]}
      extra={
        <>
          <MultiSelect value={projectIds} onChange={setProjectIds} options={...} placeholder="所属项目" triggerWidth={130} contentWidth={240} size="sm" searchable showCountTag />
          <Button variant="primary" size="sm" onClick={onCreate}><Plus /> 添加任务</Button>
        </>
      }
    />

    <DataTable
      columns={[
        { key: 'id',          header: 'ID',     width: 56,  cellClassName: 'font-mono text-stone-500 tnum' },
        { key: 'jobDesc',     header: '任务名称', render: r => <TruncatedText text={r.jobDesc} className="font-medium text-stone-900" /> },
        { key: 'project',     header: '所属项目', width: 130 },
        { key: 'glueType',    header: '类型',   width: 70, render: r => <GlueTypeBadge type={r.glueType} /> },
        { key: 'jobCron',     header: 'Cron',   width: 132, cellClassName: 'font-mono text-[11.5px] text-stone-600 tnum' },
        { key: 'runStatus',   header: '执行',   width: 70, render: r => <span className={cn('text-[11.5px]', RUN_STATUS_COLOR[rs])}>{RUN_STATUS_LABEL[rs]}</span> },
        { key: 'triggerStatus', header: '开关', width: 70, render: r => <Switch checked={r.triggerStatus === 1} onCheckedChange={c => handleToggleRunning(r, c)} /> },
        { key: 'triggerNextTime', header: '下次触发', width: 116, cellClassName: 'truncate font-mono text-[11.5px] text-stone-600 tnum' },
        { key: 'actions',     header: '操作', width: 96, align: 'right', render: r => <ActionDropdown ... /> },
      ]}
      leftBar={r => {
        const status = deriveJobStatus(r.triggerStatus, r.lastHandleCode, r.lastTriggerCode, ...);
        return status === 'error' ? 'bg-red-500' : status === 'running' ? 'bg-emerald-500' : 'bg-stone-300';
      }}
      rows={rows}
      rowKey="id"
      loading={loading}
      emptyText={noFilterApplied ? '还没有任务' : '没有匹配的任务'}
      emptyExtra={noFilterApplied ? <Button variant="link" size="sm">+ 添加任务</Button> : null}
    />

    <TablePagination ... />
  </section>

  <JobInfoDetailDialog open={editDialogOpen} ... />
  <TriggerJobDialog open={triggerOpen} ... />
  <LogViewerDialog open={logOpen} ... />
  {confirmDialog}
</div>
```

## 视觉要点

1. **LeftBar 4px 状态条**：error red-500 / running emerald-500 / stopped stone-300 / transparent—— 让"哪一行有问题"一眼可读
2. **Switch 列宽 70px / align left**：紧贴左边，给"运行/暂停"语义最大可见性
3. **乐观更新**：onCheckedChange 立即更新 rows + onSuccess 拉接口 / onError revert—— 用户感觉"切换"瞬间响应
4. **3 filter 顺序**：类型 → 执行状态 → 开关状态（从分类到状态到运行），最常切的放后
5. **MultiSelect 项目 130px trigger / 240px content**：项目名通常较长，content 宽度比 trigger 大
6. **deriveRunStatus 派生**：把后端 4 个 code 字段 (lastHandleCode/lastTriggerCode/triggerLastTime/recentTriggerTime) 派生成 success/fail/running/never 4 态
7. **Action 列默认 3 个 icon button** + MoreHorizontal: Play (触发一次) + ScrollText (查看日志) + More (编辑/列表跳/终止/删除)
8. **删除走 useConfirm**：danger 模式 + 描述高亮任务名

## 适配指南

- jobTemplate 页减少 Cron / 下次触发列，但加 NextTriggerPopover + RegisterNodePopover —— 复用本骨架
- 切 set / project 时记得 `setPage(1)` —— 否则跳到不存在的分页
- 终止任务：拉最近一条 jobLog → killJob(log) → 刷新表格
- "终止任务" 仅在 runStatus === 'running' 时显示

## 反模式

- ❌ Switch 不做乐观更新——每次切换要等接口
- ❌ leftBar 用饱和色 (bg-red-700)—— 4px 窄条用 500 就够
- ❌ filter 排序乱（开关 → 类型）—— 用户切换习惯不符
