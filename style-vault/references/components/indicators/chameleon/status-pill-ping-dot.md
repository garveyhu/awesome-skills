---
id: components/indicators/chameleon/status-pill-ping-dot
type: component
name: 药丸状态徽标 + ping 点
description: 浅底药丸 + 1.5px 状态点 + 可选 animate-ping 双层脉冲，6 态语义集（含 running/info sky）
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
preview: /preview/components/indicators/chameleon/status-pill-ping-dot
---

# Chameleon 药丸状态徽标 + ping 点

> 语义状态徽标——浅底药丸 + 1.5px(6px) 状态点 + 可选 `animate-ping` 双层脉冲（运行/排队态用）。6 态语义集：success / error / warning / info / running / neutral。用于日志、任务、健康度等场景，强调「状态」语义（与纯文字 Badge 互补）。

## 视觉特征

- **外层 pill**：`inline-flex items-center gap-1.5(6px) whitespace-nowrap rounded-md(6px) px-2(8px) py-0.5(2px) text-[11px] font-medium` + tone.pill
- **点容器**：`relative flex h-1.5(6px) w-1.5`；`pulse` 时叠一层 `absolute inline-flex h-full w-full animate-ping rounded-full opacity-75` + dot 色，再实点 `relative inline-flex h-1.5 w-1.5 rounded-full` + dot 色
- **6 tone（dot 色 / pill 底字色）**：
  - `success` — dot `bg-emerald-500(#10b981)`，pill `bg-emerald-50 text-emerald-700`
  - `error` — dot `bg-red-500(#ef4444)`，pill `bg-red-50 text-red-700`
  - `warning` — dot `bg-amber-500(#f59e0b)`，pill `bg-amber-50 text-amber-700`
  - `info` — dot `bg-sky-500(#0ea5e9)`，pill `bg-sky-50 text-sky-700`
  - `running` — dot `bg-sky-500(#0ea5e9)`，pill `bg-sky-50 text-sky-700`（同 info 色，语义不同）
  - `neutral` — dot `bg-stone-400(#a8a29e)`，pill `bg-stone-100 text-stone-600`

## 核心代码

```tsx
const TONE = {
  success: { dot:'bg-emerald-500', pill:'bg-emerald-50 text-emerald-700' },
  error:   { dot:'bg-red-500',     pill:'bg-red-50 text-red-700' },
  warning: { dot:'bg-amber-500',   pill:'bg-amber-50 text-amber-700' },
  info:    { dot:'bg-sky-500',     pill:'bg-sky-50 text-sky-700' },
  running: { dot:'bg-sky-500',     pill:'bg-sky-50 text-sky-700' },
  neutral: { dot:'bg-stone-400',   pill:'bg-stone-100 text-stone-600' },
};

<span className={cn('inline-flex items-center gap-1.5 whitespace-nowrap rounded-md px-2 py-0.5 text-[11px] font-medium', c.pill)}>
  <span className="relative flex h-1.5 w-1.5">
    {pulse && <span className={cn('absolute inline-flex h-full w-full animate-ping rounded-full opacity-75', c.dot)} />}
    <span className={cn('relative inline-flex h-1.5 w-1.5 rounded-full', c.dot)} />
  </span>
  {children}
</span>
```

## 适配指南

- 运行中 / 排队中用 `tone="running"` + `pulse`——双层 ping 暗示「活着、在动」
- 终态（成功/失败）不开 pulse——已结束的状态不该闪动
- 文字放在 children，不内置 label——同 tone 在不同场景文案不同（「成功」「已完成」「200」）
- 药丸 `text-[11px]` 偏小是刻意的——状态徽标是辅助信息，不抢行内主文字

## 与 waveflow/status-dot-ring 区分

| 维度 | waveflow status-dot-ring | chameleon status-pill-ping-dot |
|------|--------------------------|-------------------------------|
| 容器 | 仅 dot + inline label，**无药丸底** | **浅底药丸** `rounded-md px-2 py-0.5` + tone 浅底 |
| 点尺寸 | **7×7px** | **6px**（h-1.5 w-1.5） |
| 点动效 | 静态 + `box-shadow` 半透色 ring（15-18% alpha） | **`animate-ping` 双层脉冲**（运行态），无 box-shadow ring |
| 态数 | **3 态** running emerald / stopped stone / error red | **6 态**（含 running/info sky 色、warning amber） |
| 派生 | 配套 `deriveJobStatus()` / `deriveRunStatus()` 把后端 code 映射成语义 | 无派生，直接传 tone |

选型：纯状态点嵌行内文字（任务列表 leftBar）用 waveflow；需要带底色徽标 + 运行态脉冲（日志/健康度 chip）用 chameleon。

## 反模式

- ❌ 终态加 pulse——成功/失败已结束，闪动误导用户以为还在进行
- ❌ 6 态全开 pulse——只有 running/排队这类「进行中」语义才脉冲
- ❌ dot 放大到 10px+——会跟药丸文字抢主视觉
- ❌ 内置写死 label——同 tone 多场景文案不同，交给 children
