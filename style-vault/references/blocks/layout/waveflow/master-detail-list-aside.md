---
id: blocks/layout/waveflow/master-detail-list-aside
type: block
name: 256px 左 aside + 右详情面板主从
description: jobSet 招牌布局 - 左 256px 任务集列表 aside (折叠态隐藏 + 弹出展开按钮) + 右详情面板 HERO + 4 MetricCard + 内嵌 DataTable
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, industrial]
  mood: [calm, serious]
  stack: [shadcn-radix]
uses:
  - blocks/display/waveflow/set-card-segmented
  - blocks/display/waveflow/metric-card-quartet
  - blocks/display/waveflow/data-table-leftbar-shimmer
preview: /preview/blocks/layout/waveflow/master-detail-list-aside
---

# Waveflow Master-Detail List Aside

> jobSet 页招牌布局——主从视图。**左侧 256px aside**：`flex w-64 flex-shrink-0 flex-col rounded-xl border border-stone-200/40 bg-[var(--color-paper)] shadow-[var(--shadow-soft)]`，自上而下 header（标题 + count + 折叠）+ 任务集列表 + "新建集合"虚线按钮。**右侧 flex-1 详情面板**：`flex-1 overflow-auto rounded-xl border ... bg-paper shadow-soft + scrollbar-gutter:stable`，内含 HERO（icon + breadcrumb meta + 名称 + 描述 + 按钮组）+ 4 MetricCard 度量行 + MembersTable。

## 页面骨架

```tsx
<div className="relative flex h-full gap-4 px-6 py-4">

  {asideCollapsed && (
    <Tooltip content="展开任务集列表">
      <button onClick={...} className="absolute left-1 top-4 z-10 rounded-md p-1 text-stone-400 hover:bg-stone-100">
        <ChevronsRight className="h-4 w-4" />
      </button>
    </Tooltip>
  )}

  {!asideCollapsed && (
    <aside className="flex w-64 flex-shrink-0 flex-col rounded-xl border border-stone-200/40 bg-[var(--color-paper)] shadow-[var(--shadow-soft)]">
      <div className="flex items-center justify-between border-b border-stone-100 px-3.5 py-3">
        <h2 className="text-[13px] font-semibold text-stone-700">任务集 · 状态总览</h2>
        <div className="flex items-center gap-1.5">
          <CountTag value={sets.length} />
          <button onClick={() => setAsideCollapsed(true)} className="rounded p-1 text-stone-400 hover:bg-stone-100">
            <PanelLeftClose className="h-3.5 w-3.5" />
          </button>
        </div>
      </div>
      <div className="flex-1 space-y-1.5 overflow-auto p-2.5 [scrollbar-gutter:stable]">
        {sets.map(s => <SetCard set={s} isActive={s.id === activeId} onClick={...} />)}
        <button className="...border-dashed border-stone-300">+ 新建集合</button>
      </div>
    </aside>
  )}

  <section className="flex-1 overflow-auto rounded-xl border border-stone-200/40 bg-[var(--color-paper)] shadow-[var(--shadow-soft)] [scrollbar-gutter:stable]">
    {!activeSet
      ? <EmptyState icon={<ListChecks />} title="请选择一个任务集" description="左侧选中后查看详情，或新建一个" />
      : <DetailView set={activeSet}>
          <Hero />          {/* icon 44×44 themed bg + breadcrumb meta + 20px name + desc + 按钮组 */}
          <MetricCardQuartet />  {/* 总/运行/暂停/异常 */}
          <MembersTable />  {/* 内嵌完整 toolbar+table+pagination 三件套 */}
        </DetailView>
    }
  </section>

</div>
```

## 视觉特征

- **整体外框 `flex h-full gap-4 px-6 py-4`**：左右两个 section 之间 16px 间隙
- **aside 256px 固定宽**：再窄装不下任务集名 + count + segmented
- **aside header `border-b border-stone-100 px-3.5 py-3`**：13px font-semibold stone-700 + CountTag 末尾
- **aside body 卡片密集排**：`space-y-1.5 p-2.5` —— 上下 1.5 间距，最大密度
- **新建集合按钮**：虚线 dashed + Plus 12px + "新建集合" 12px
- **折叠按钮在 absolute left-1 top-4**：折叠时浮在面板左上方，避免占任何宽度
- **HERO** 内 breadcrumb：`text-[10.5px] uppercase tracking-wider text-stone-500` "任务集 ·" + ProjectTag + "·" + 最近触发时间
- **HERO 名称 h1**：`text-[20px] font-semibold leading-tight tracking-tight text-stone-900`
- **HERO icon**: `flex h-11 w-11 items-center justify-center rounded-xl` + `style={{ background: theme.bg, color: theme.fg }}`
- **HERO 操作按钮组**: 编辑 (variant outline) + 添加任务 (variant primary) + MoreHorizontal DropdownMenu

## 适配指南

- 折叠态把 aside 整个 unmount —— 不做 width transition（实际 waveflow 选择）
- aside `[scrollbar-gutter:stable]` 防内容多少切换时宽度跳
- 空态 EmptyState 在 detail 区中心居中

## 反模式

- ❌ aside 改 width 切换—— 主区会跟着抖
- ❌ aside 不可折叠—— 移动端 / 小屏炸
- ❌ 用 sticky 把 HERO 钉顶—— 滚动时被 4 MetricCard 顶撞视觉
