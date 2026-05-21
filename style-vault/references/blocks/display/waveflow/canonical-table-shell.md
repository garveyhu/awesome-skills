---
id: blocks/display/waveflow/canonical-table-shell
type: block
name: 列表页规范外壳
description: 页面 `h-full px-6 py-4` + rounded-xl border/40 paper bg shadow-soft section + 内部 TableToolbar + DataTable + TablePagination 三件套
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, industrial]
  mood: [calm, serious]
  stack: [shadcn-radix]
uses:
  - tokens/palettes/waveflow/warm-paper-ink-blue
  - tokens/shadow/waveflow/soft-card-pop-trio
  - blocks/filters/waveflow/table-toolbar-tri
  - blocks/display/waveflow/data-table-leftbar-shimmer
preview: /preview/blocks/display/waveflow/canonical-table-shell
---

# Waveflow Canonical Table Shell

> waveflow 所有列表页（项目 / 数据源 / 任务 / 执行器 / 用户 / 日志 / 任务模板）共用的页面外壳——`h-full px-6 py-4` 外框 + 内部一个 `rounded-xl border border-stone-200/40 bg-[var(--color-paper)] shadow-[var(--shadow-soft)] p-5` 大 section，section 内**自上而下三件套**：TableToolbar / DataTable / TablePagination。

## 页面骨架

```tsx
<div className="h-full px-6 py-4">
  <section className="rounded-xl border border-stone-200/40 bg-[var(--color-paper)] shadow-[var(--shadow-soft)] p-5">
    <TableToolbar
      title="项目管理"
      search={{ value, onChange, onSubmit, onRefresh, placeholder: '搜索项目名称' }}
      filters={[...]}                  // 可选
      extra={<Button variant="primary" size="sm"><Plus /> 添加项目</Button>}
    />
    <DataTable
      columns={columns}
      rows={rows}
      rowKey="id"
      loading={loading}
      leftBar={r => ...}              // 可选：返回 bg-* class
      emptyText={keyword ? '没有匹配的' : '还没有'}
      emptyExtra={!keyword ? <Button variant="link" size="sm">+ 添加</Button> : null}
    />
    <TablePagination
      page={page} pageSize={pageSize} total={total}
      onPageChange={setPage}
      onPageSizeChange={s => { setPageSize(s); setPage(1) }}
    />
  </section>

  {/* 各类 Dialog: FormDialog / ConfirmDialog 平铺在 section 外 */}
  <ProjectFormDialog open={...} ... />
  {confirmDialog}
</div>
```

## 视觉特征

- **`px-6 py-4` 外框**：24px 横、16px 纵——比页面默认更紧凑
- **section 用 `border-stone-200/40 + paper + soft shadow`**：3 件套的代表性组合，是整站卡片的"基础形态"
- **section 内 padding `p-5` (20px)**：toolbar 与 section 边距统一
- **三件套垂直无 gap**：TableToolbar 自带 `mb-2.5`、DataTable 包外框、TablePagination 自带 `mt-3`——节奏自然
- **filter / extra 跟随 toolbar 右对齐**——title 顶左，filter+extra 顶右

## 适配指南

- 复用于所有"单表 + 工具栏"列表页（**项目 / 数据源 / 执行器 / 用户**完全套用）
- 复杂场景（**jobInfo / jobLog**）也用同款外壳，多加几个 filter 即可
- master/detail 场景（**jobSet**）则不用本 shell，换 `master-detail-list-aside` block
- Dialog 永远在 section 外平铺（避免 portal 层级混乱）

## 反模式

- ❌ section 嵌套 section—— 视觉重负
- ❌ 把 toolbar / table / pagination 拆三个独立 section—— 失去"一张卡 = 一个数据集"的语义
- ❌ 给 section 加 max-width—— admin 必须用满宽度
