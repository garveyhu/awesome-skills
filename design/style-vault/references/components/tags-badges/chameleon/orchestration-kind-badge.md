---
id: components/tags-badges/chameleon/orchestration-kind-badge
type: component
name: 编排方式徽标
description: 由 agent source + graph kind 推导的 4-kind 编排方式 chip (代码/对话编排/流程编排/外部) · 10px 软色阶 + 无值灰破折号
platforms:
- web
theme: light
tags:
  aesthetic:
  - industrial
  - minimal
  mood:
  - serious
  stack:
  - shadcn-radix
uses:
- tokens/palettes/waveflow/warm-paper-ink-blue
preview: /preview/components/tags-badges/chameleon/orchestration-kind-badge
---

# Chameleon Orchestration Kind Badge

> 应用列表 / 详情里"这个应用是怎么编排出来的"徽标——由 agent 的 `source` + 关联 graph 的 `kind` 推导成 4 种编排域（代码 / 对话编排 / 流程编排 / 外部），每域一个软色阶 chip。纯展示组件（接 props 出 UI），推导逻辑下沉到 `@/core/lib/orchestration`。沿用 waveflow glue-type-badge-duo 的 light 浅底深字 chip 体系，但映射的是 4 个编排域而非 11 种业务类型。

## 视觉特征

- **chip 形状**：`inline-flex shrink-0 rounded(4px) px-1.5(6px) py-0.5(2px) text-[10px] font-medium`
- **4 域配色**（bg / text，全走 `-50 / -700` 软色阶）：
  - `code` 代码：`bg-indigo-50(#eef2ff) text-indigo-700(#4338ca)`
  - `chatflow` 对话编排：`bg-sky-50(#f0f9ff) text-sky-700(#0369a1)`
  - `workflow` 流程编排：`bg-violet-50(#f5f3ff) text-violet-700(#6d28d9)`
  - `external` 外部：`bg-amber-50(#fffbeb) text-amber-700(#b45309)`
- **无值态**：`<span class="text-[10.5px] text-stone-300(#d6d3d1)">—</span>`（不渲染 chip，留破折号占位保高度）
- 圆角 `rounded`（4px）+ 10px 字号——比通用 Badge 更小更密，专给"次要类别标记"

## 核心代码

```tsx
const KIND_DEFS: Record<OrchestrationKind, { label: string; cls: string }> = {
  code:     { label: '代码',     cls: 'bg-indigo-50 text-indigo-700' },
  chatflow: { label: '对话编排', cls: 'bg-sky-50 text-sky-700' },
  workflow: { label: '流程编排', cls: 'bg-violet-50 text-violet-700' },
  external: { label: '外部',     cls: 'bg-amber-50 text-amber-700' },
};

export const OrchestrationBadge = ({ source, graphKind }: Props) => {
  const kind = resolveOrchestrationKind(source, graphKind);
  if (!kind) return <span className="text-[10.5px] text-stone-300">—</span>;
  const def = KIND_DEFS[kind];
  return (
    <span className={`inline-flex shrink-0 rounded px-1.5 py-0.5 text-[10px] font-medium ${def.cls}`}>
      {def.label}
    </span>
  );
};
```

## 适配指南

- 推导逻辑（source → kind）一律在 `resolveOrchestrationKind`，组件只接 `source` / `graphKind` 出 UI，不在组件里写判断
- 4 个域色固定，新增编排方式先在 `OrchestrationKind` + `KIND_DEFS` 字典登记，不随手挑色
- 无推导结果显灰破折号 `—`，不要渲染空 chip 或隐藏（保住列高对齐）

## 反模式

- ❌ chip 圆角改 `rounded-full` —— 失去工业网格感
- ❌ 把推导逻辑写进组件——下沉到 `lib/orchestration`
- ❌ 无值时返回 `null` 或空串——用 `—` 灰破折号占位

## 与 waveflow/glue-type-badge-duo 区分

| 维度 | chameleon orchestration-kind-badge | waveflow glue-type-badge-duo |
|------|-----------------------------------|------------------------------|
| 域数量 | 4 个编排方式（code/chatflow/workflow/external） | 11 种业务类型（FETCH/TRANS/PUSH/...） |
| 变体 | 单一 light 软色阶 | 双变体 light（浅底深字带边）+ solid（实心白字） |
| 边框 | 无边（纯浅底，`-50` 色） | light 带可见边（`-200`），solid 无边 |
| 字号 | `text-[10px]`（无值 `[10.5px]`） | `text-[10.5px]` / CountTag `[10px]` |
| 无值态 | 灰破折号 `—`（text-stone-300） | 无专门无值态 |
| 附带 | 仅单组件 + 推导 | 配套 CountChip / ProjectTag / CountTag |

选择：要"应用编排方式的 4 域标记"用 chameleon；要"任务类型 11 色映射 + dashboard solid 反显"用 waveflow。
