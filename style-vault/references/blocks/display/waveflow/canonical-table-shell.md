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

## TablePagination 子模式（必看）

分页条**两段**：左 range + pageSize select；右 4-button 翻页器 + **「跳至 N 页」跳转输入**。

### 跳转输入（参考 aura-form-style 方案 B · Linear 风极简）

- **不是框型 input**——而是**虚线下划线** 风格：
  - `background: transparent`
  - `border: none` (无 left/right/top)
  - `border-bottom: 1px dashed stone-300` —— 默认虚线
  - `focus:border-solid focus:border-blue-500` —— 聚焦时虚线变实线 + 蓝色
- **尺寸**：`h-[22px] w-8` (22 × 32px) · text-center · `font-mono text-[11.5px] tnum font-medium text-stone-800`
- **行为**：
  - 未聚焦显示**当前页码**（不要 placeholder "页码"）
  - 聚焦清空让用户输入
  - `onChange` 用 `replace(/[^\d]/g, '')` 仅允许数字
  - `onBlur` / `Enter` 提交，越界自动夹到 `[1, totalPages]`
  - 与当前页相同不触发回调（避免无效跳转）
- **标签**：`<span>跳至</span> <input/> <span>页</span>` 三段，标签 stone-500
- **仅 `totalPages > 1` 时显示**——单页隐藏避免没意义
- **margin-left 18px**：与左侧"末页"按钮拉开距离

### 跳转输入核心代码

```tsx
const JumpInput: React.FC<{ current: number; totalPages: number; onJump: (p: number) => void }> = ({ current, totalPages, onJump }) => {
  const [val, setVal] = React.useState('');
  const [editing, setEditing] = React.useState(false);

  const commit = () => {
    setEditing(false);
    if (val === '') return;
    const n = parseInt(val, 10);
    setVal('');
    if (!Number.isFinite(n)) return;
    const clamped = Math.min(Math.max(1, n), totalPages);
    if (clamped !== current) onJump(clamped);
  };

  return (
    <span className="ml-3 flex items-center gap-1.5 text-stone-500">
      <span>跳至</span>
      <input
        type="text" inputMode="numeric"
        value={editing ? val : String(current)}
        onFocus={() => { setEditing(true); setVal(''); }}
        onChange={e => setVal(e.target.value.replace(/[^\d]/g, ''))}
        onBlur={commit}
        onKeyDown={e => { if (e.key === 'Enter') (e.target as HTMLInputElement).blur(); }}
        className="h-[22px] w-8 border-0 border-b border-dashed border-stone-300 bg-transparent p-0 text-center font-mono text-[11.5px] tnum font-medium text-stone-800 outline-none transition focus:border-solid focus:border-blue-500"
      />
      <span>页</span>
    </span>
  );
};
```

### 反模式

- ❌ 用框型 input（h-7 rounded-md border-stone-300）—— 在 4 翻页 button 旁边显得"重"，破坏极简
- ❌ 永远显示 placeholder "页码"—— 用户没看到当前页号，仍要去左边数字处确认
- ❌ 输入框 width > 40px—— 通常 1-3 位数字就够，宽了空荡
- ❌ 提交后保留输入值—— 跳页后应回到"显示当前页"状态

## 适配指南

- 复用于所有"单表 + 工具栏"列表页（**项目 / 数据源 / 执行器 / 用户**完全套用）
- 复杂场景（**jobInfo / jobLog**）也用同款外壳，多加几个 filter 即可
- master/detail 场景（**jobSet**）则不用本 shell，换 `master-detail-list-aside` block
- Dialog 永远在 section 外平铺（避免 portal 层级混乱）

## 反模式

- ❌ section 嵌套 section—— 视觉重负
- ❌ 把 toolbar / table / pagination 拆三个独立 section—— 失去"一张卡 = 一个数据集"的语义
- ❌ 给 section 加 max-width—— admin 必须用满宽度
