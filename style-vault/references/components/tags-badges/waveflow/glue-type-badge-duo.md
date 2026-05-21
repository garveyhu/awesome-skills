---
id: components/tags-badges/waveflow/glue-type-badge-duo
type: component
name: 任务类型徽章双变体
description: 11 种业务类型 chip · light 浅底深字带边 / solid 反显实心白字 · emerald/pink/blue/amber/indigo/cyan/stone 7 色映射
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, industrial]
  mood: [serious, playful]
  stack: [shadcn-radix]
uses: []
preview: /preview/components/tags-badges/waveflow/glue-type-badge-duo
---

# Waveflow GlueType Badge Duo

> waveflow 业务类型 chip——11 种任务类型 (FETCH/TRANS/PUSH/COMPLEX/BEAN/GLUE_SHELL/GLUE_PYTHON/...) 每种映射一个色彩，**双变体**：`light` 浅底深字带边（表格密集场景，不抢戏）+ `solid` 反显实心白字（dashboard 突出位置，高对比）。额外配套 `GlueTypeCountChip`（solid + 数字）和 `ProjectTag` (mono) / `CountTag` (小数字)。

## 视觉特征

- **GlueTypeBadge light 变体**（**默认**）：
  - 形状：`inline-block shrink-0 whitespace-nowrap rounded border px-1.5 py-0.5 text-[10.5px] leading-none`
  - 配色（部分）：
    - FETCH `bg-emerald-50 text-emerald-700 border-emerald-200`
    - TRANS `bg-pink-50 text-pink-700 border-pink-200`
    - PUSH `bg-blue-50 text-blue-700 border-blue-200`
    - COMPLEX `bg-amber-50 text-amber-700 border-amber-200`
    - BEAN `bg-indigo-50 text-indigo-700 border-indigo-200`
    - GLUE_PYTHON `bg-cyan-50 text-cyan-700 border-cyan-200`
    - GLUE_SHELL / GROOVY / PHP / NODEJS / POWERSHELL `bg-stone-100 text-stone-700 border-stone-200`
- **GlueTypeBadge solid 变体**：
  - 形状：`inline-block shrink-0 whitespace-nowrap rounded px-1.5 py-0.5 text-[10.5px] font-semibold tracking-wide leading-none`
  - 配色：同 light 的 hue 但走 600 + text-white（如 `bg-emerald-600 text-white`）
- **GlueTypeCountChip**（dashboard "活跃任务" 用）：solid 色 + label + 空格 + count（数字 mono bold tnum）
- **ProjectTag**（mono 项目名）：`inline-block rounded px-1.5 py-0.5 text-[10.5px] font-mono tnum + bg-stone-100 text-stone-700` (default) 或 `bg-red-100 text-red-700 font-medium` (danger)
- **CountTag**（小数字 chip）：`inline-block rounded bg-stone-100 px-1.5 py-0.5 text-[10px] font-mono tnum text-stone-500`
- **统一规则**：所有 chip 都是 `text-[10.5px] / [10px]` + `px-1.5 py-0.5` + 圆角 `rounded` —— 不出 `rounded-full pill`，保持工业感

## 适配指南

- 表格类型列优先 `variant="light"`——和行 hover bg-stone-50/60 不冲突
- dashboard 突出位置 `variant="solid"`——和 KPI 大数字配合
- 用 `GLUE_TYPE_LABEL` / `GLUE_TYPE_SOLID_CLASS` / `GLUE_TYPE_LIGHT_CLASS` 三个导出常量给业务代码 share 配色

## 反模式

- ❌ chip 圆角改 rounded-full —— 失去工业网格感
- ❌ 配色随机分配新业务类型 —— 必须在 GLUE 字典里登记
- ❌ light 变体用饱和 hue（如 emerald-300）—— 抢戏
