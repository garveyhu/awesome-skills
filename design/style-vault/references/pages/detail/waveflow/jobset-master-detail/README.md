---
id: pages/detail/waveflow/jobset-master-detail
type: page
name: 任务集主从详情
description: 左 256px aside (status overview list + segmented blocks) + 右详情 (HERO icon+breadcrumb+name+desc+actions + 4 MetricCard + members 二级 toolbar+table+pagination) + 7 dialogs
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, industrial]
  mood: [serious, calm]
  stack: [shadcn-radix]
uses:
  - blocks/layout/waveflow/master-detail-list-aside
  - blocks/display/waveflow/set-card-segmented
  - blocks/display/waveflow/metric-card-quartet
  - blocks/display/waveflow/data-table-leftbar-shimmer
  - blocks/feedback/waveflow/danger-confirm-modal
preview: /preview/pages/detail/waveflow/jobset-master-detail
---

# Waveflow JobSet Master-Detail

> waveflow 任务集页 (`/jobSet`)——主从布局的招牌实践。左侧 256px aside 列所有集合（每个 set-card-segmented：preset icon + 名称 + 计数 + SegmentedBlocks）+ 右侧 detail panel（HERO + 4 MetricCard + 内嵌 MembersTable + 7 个 dialog）。**URL `?id=N` 双向同步**：sidebar 选中或 URL 变化都互相驱动。**乐观更新**：行级开关或触发任务后立即更新 sidebar stats，1.5s 后再 fetch 真实状态。

## 页面要点

### 左 aside

- header（"任务集 · 状态总览" 13px font-semibold + CountTag + 折叠按钮）
- 卡片列表 `space-y-1.5 p-2.5`，每个 `set-card-segmented`
- 末尾"+ 新建集合" border-dashed button

### 右 detail HERO

```tsx
<div className="mb-4 flex items-start gap-3.5 border-b border-stone-100 pb-4">
  <span className="flex h-11 w-11 flex-shrink-0 items-center justify-center rounded-xl" style={{ background: theme.bg, color: theme.fg }}>
    <Icon size={22} />
  </span>
  <div className="flex-1">
    <div className="mb-0.5 flex items-center gap-1.5">
      <span className="text-[10.5px] font-medium uppercase tracking-wider text-stone-500">任务集</span>
      <span className="text-stone-300">·</span>
      <ProjectTag name={set.projectName} />
      <span className="text-stone-300">·</span>
      <span className="text-[10.5px] text-stone-500">最近触发 <span className="font-mono tnum text-stone-700">{lastTrigger}</span></span>
    </div>
    <h1 className="text-[20px] font-semibold leading-tight tracking-tight text-stone-900">{set.name}</h1>
    <p className="mt-0.5 text-[13px] text-stone-600">{set.description || '—'}</p>
  </div>
  <div className="flex items-center gap-1.5">
    <Button variant="outline" size="md" onClick={onEdit}><Pencil /> 编辑</Button>
    <Button variant="primary" size="md" onClick={onAddMembers}><Plus /> 添加任务</Button>
    <DropdownMenu>...</DropdownMenu>
  </div>
</div>
```

### MetricCard Quartet

`grid grid-cols-4 gap-3 mb-5`：总任务 (default) / 运行中 (success) / 已暂停 (default) / 异常 (danger)

### MembersTable 二级

`data-table-leftbar-shimmer` 完整体 + 完整三件套 toolbar/table/pagination + 二级 dialog 集成（Trigger/LogViewer/JobDetail/RemoveMember）

### 7 个 Dialog

1. `JobSetFormDialog` - 编辑集合本身
2. `AddMembersDialog` - 批量添加任务
3. `RemoveMembersDialog` - 批量移除
4. `JobInfoDetailDialog` - 编辑/查看单任务
5. `TriggerJobDialog` - 触发一次（带参数）
6. `LogViewerDialog` - 快速看最近日志
7. ConfirmDialog - 删除集合 / 移除成员 / 终止任务

## 视觉要点

1. **HERO 不用 rounded section 包**：HERO + Metrics + Table 都在外 detail section 内的不同节，用 `border-b border-stone-100 pb-4 / mb-4 / mb-5` 做内部分割
2. **HERO breadcrumb 4 段** "任务集 · {project} · 最近触发 N 分钟前"：用 stone-300 "·" 做分隔
3. **preset icon 系统**：themed bg+fg，由 `getPresetIcon(iconName)` + `getPresetTheme(themeName)` 解析—— 用户可在 FormDialog 里选 N 个 preset
4. **触发任务乐观 stamp**：用 `triggeredStamp = { jobId, t }`，让 MembersTable 把对应行立即显示"执行中"，1.5s 后才 fetchSets（等后端写 jobLog 落库）
5. **URL 双向**：`useSearchParams() ?id=N` 和 `activeId` state 互相驱动；点 sidebar 重置 URL（`replace: true`）
6. **空态**：activeSet 为 null 时整个 detail 显 EmptyState 居中

## 适配指南

- 256px aside 是上限——再宽挤主区
- 集合数 > 20 时 aside 加内部 search（waveflow 当前没做，因实际场景集合 < 10）
- HERO 操作按钮组：变 outline(辅) + primary(主) + ghost icon-sm(更多) —— 同款适用所有 detail 页

## 反模式

- ❌ aside 不可折叠—— 移动端炸
- ❌ 触发任务不做乐观 stamp—— 用户感觉"按了没反应"
- ❌ URL 不同步 activeId—— 刷新丢状态
