---
id: pages/list-table/waveflow/canonical-section-list
type: page
name: 单 Section 列表页（项目 / 执行器 / 用户 / 数据源）
description: 单一 paper section 套壳 + TableToolbar (title + search + extra) + DataTable (无 leftBar) + Pagination + FormDialog - waveflow 4 个最简列表页共用形态
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm]
  stack: [shadcn-radix]
uses:
  - blocks/display/waveflow/canonical-table-shell
  - blocks/form/waveflow/dialog-vertical-form
preview: /preview/pages/list-table/waveflow/canonical-section-list
---

# Waveflow Canonical Section List

> waveflow 4 个最简列表页共用形态：**项目管理 / 数据源管理 / 执行器管理 / 用户管理**。`canonical-table-shell` 套壳：标题 + 搜索 + 添加按钮 + 表格（无 leftBar，ID / 名称 / 描述 / 创建者 / 创建时间 / 操作）+ 分页 + 增删改 FormDialog + ConfirmDialog。

## 适用场景

| 路由 | 实际名称 | 字段差异 |
|---|---|---|
| `/project` | 项目管理 | ID + 名称 + 描述 + 所属用户 + 创建时间 + 操作 |
| `/datasource` | 数据源管理 | ID + 名称 + JDBC URL + 用户名 + 测试连接 + 操作 |
| `/executor` | 执行器管理 | 名称 + AppName + 注册方式 + OnlineMachine + 排序 + 操作 |
| `/user` | 用户管理 | 用户名 + 角色 + 权限 + 创建时间 + 操作 |

## 页面骨架

```tsx
<div className="h-full px-6 py-4">
  <section className="rounded-xl border border-stone-200/40 bg-[var(--color-paper)] p-5 shadow-[var(--shadow-soft)]">
    <TableToolbar
      title="项目管理"
      search={{ value: searchInput, onChange: setSearchInput, onSubmit: v => { setKeyword(v); setPage(1); }, onRefresh: () => setRefreshTick(t => t+1), placeholder: '搜索项目名称' }}
      extra={
        <Button variant="primary" size="sm" onClick={handleCreate}>
          <Plus className="h-3.5 w-3.5" /> 添加项目
        </Button>
      }
    />
    <DataTable
      columns={columns}        {/* ID (mono tnum) + 名称 (font-medium) + 描述 + 创建者 + 创建时间 (mono tnum) + 操作 */}
      rows={projects}
      rowKey="id"
      loading={loading}
      emptyText={keyword ? '没有匹配的项目' : '还没有项目'}
      emptyExtra={!keyword ? <Button variant="link" size="sm" onClick={handleCreate}>+ 添加项目</Button> : null}
    />
    <TablePagination page={page} pageSize={pageSize} total={total} onPageChange={setPage} onPageSizeChange={s => { setPageSize(s); setPage(1) }} />
  </section>

  <ProjectFormDialog open={dialogOpen} mode={dialogMode} project={currentProject} onClose={...} onSave={() => { setDialogOpen(false); fetchProjects() }} />
  {confirmDialog}
</div>
```

## 视觉要点

1. **整页 `h-full px-6 py-4`** + **内 section `rounded-xl border-stone-200/40 paper shadow-soft p-5`** —— 双层 padding 节奏
2. **行内操作按钮**：编辑（Pencil）+ 删除（Trash2 hover red-100 + red-600）—— rounded p-1 + hover bg-stone-200
3. **删除走 useConfirm**：`const ok = await confirm({ title: '确认删除', description: 「项目」, confirmText: '删除', danger: true })`
4. **URL 同步搜索词**：`useSearchParams()` hydrate `initialKeyword`，让 ⌘K 跳转能携带 `?searchVal=xxx`
5. **searchInput vs keyword 解耦**：输入框 local state，回车/点搜索 icon 才同步到 keyword
6. **refreshTick**：值不变时也能强制 effect 重跑（点搜索图标但 query 没变）

## 适配指南

- 字段差异控制在 columns 数组里——其它结构 100% 共享
- FormDialog 走 dialog-vertical-form block，每页一个表单 component（ProjectFormDialog / UserFormDialog / ExecutorFormDialog / DatasourceFormDialog）
- 操作权限：用户管理用 `meta.roles: ['ROLE_ADMIN']` 路由控制可见性

## 反模式

- ❌ 4 个页面各自重写 ToolBar / Pagination—— 失去一致性
- ❌ 不用 useConfirm 直接 `window.confirm`—— 破坏 admin 视觉
- ❌ 搜索 input 跟 fetch 同步触发—— 每字符一次请求
