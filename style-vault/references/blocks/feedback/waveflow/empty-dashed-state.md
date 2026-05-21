---
id: blocks/feedback/waveflow/empty-dashed-state
type: block
name: 虚线圆框空态
description: 2px dashed border + 12x12 圆 stone-100 icon + 14px font-semibold title + 12px stone-500 desc + 可选 action 槽
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm]
  stack: [shadcn-radix]
uses: []
preview: /preview/blocks/feedback/waveflow/empty-dashed-state
---

# Waveflow EmptyState Dashed

> waveflow 空态组件 (`components/common/EmptyState.tsx`) ——dashed 圆角框 + 圆形 icon 容器 + title + desc + action slot 四件套。适用于"未选择任何项目"、"暂无数据"、"未搜到结果"等场景。

## 视觉特征

- **外框**：`rounded-lg border-2 border-dashed border-stone-200 px-6 py-10 text-center`
- **icon 容器**：`mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-full bg-stone-100 text-stone-400`
  - 内置 icon 16-20px（lucide ListChecks / Box / Search 等）
- **title**：`text-[14px] font-semibold text-stone-700`
- **description**（可选）：`mt-1 mb-4 text-[12px] text-stone-500`
- **action**：button 或 link 槽

## 核心代码

```tsx
export const EmptyState = ({ icon, title, description, action, className }) => (
  <div className={cn('rounded-lg border-2 border-dashed border-stone-200 px-6 py-10 text-center', className)}>
    {icon && (
      <div className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-full bg-stone-100 text-stone-400">
        {icon}
      </div>
    )}
    <div className="text-[14px] font-semibold text-stone-700">{title}</div>
    {description && <div className="mt-1 mb-4 text-[12px] text-stone-500">{description}</div>}
    {action}
  </div>
);

// 用法
<EmptyState
  icon={<ListChecks className="h-5 w-5" />}
  title="请选择一个任务集"
  description="左侧选中后查看详情，或新建一个"
  action={<Button variant="primary" size="sm">+ 新建任务集</Button>}
/>
```

## 适配指南

- 表格内空态用 DataTable 的 `emptyText + emptyExtra`（不用本组件，避免双层 border）
- 大区块空态用本组件—— jobSet 未选时全屏居中显示
- icon 别太大（< 24px）—— 12×12 容器装得下 16-20px 是甜区

## 反模式

- ❌ dashed border-1—— 视觉太弱
- ❌ icon 容器用 paper bg—— 失去"空态"的中性灰感
- ❌ title 用 12px—— 失去层级
