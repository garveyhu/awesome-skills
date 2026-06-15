---
id: blocks/form/waveflow/cron-builder-modal
type: block
name: Cron 可视化构建器
description: 5 mode radio (每 N 分 / 每小时 / 每天 / 每周 / 每月) + 对应数字输入 + 实时反馈 cron 字符串 + 内置 next trigger time popover
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, industrial]
  mood: [serious]
  stack: [shadcn-radix]
uses:
  - components/inputs/waveflow/blue-focus-input
  - blocks/form/waveflow/dialog-vertical-form
preview: /preview/blocks/form/waveflow/cron-builder-modal
---

# Waveflow Cron Builder

> waveflow 任务调度的可视化 cron 构建器 (`components/CronBuilder.tsx`) —— 5 种模式（每 N 分钟 / 每小时 / 每天 / 每周 / 每月）通过 RadioGroup 切换，每模式提供对应数字字段（时 / 分 / 日 / 周天）。所有 NumberField 默认 mono——用户输入数字时是工程师的"参数表"感。

## 视觉特征

- **5 mode**：EVERY_MINUTES / HOURLY / DAILY / WEEKLY / MONTHLY
- **mode 切换**：`<RadioGroup>` 行内（不堆 dropdown）—— 一眼看完
- **NumberField 通用组件**:
  - label `text-[11px] text-stone-500`
  - `<Input type="number" mono min max />`（默认走 `mono tnum` font）
  - width 默认 w-24（96px）—— 装得下 5-6 位数
- **DAY of WEEK 7 项**：MON-SUN 中文标签
- **value 同步**：watch mode + 各 state，构造 cron 字符串 `seconds minutes hour day month dayOfWeek year` (xxljob 6/7-part 格式)
- **反向解析**：组件接收 `value` prop 时尝试解析回 mode + 各字段

## 适配指南

- 配合 `next trigger time popover`（jobTemplate 列表 / 任务编辑器用）即时看下 5-10 个触发时间
- 嵌入 Dialog 表单：套 `dialog-vertical-form` block 即可
- 字段 keyboard arrow up/down 自动 +1 —— 走原生 `<input type="number">`
- 不支持的复杂 cron（如 0/15 9-17 * * MON-FRI 工作时间内 15 分钟）回退到"自定义" mode 让用户写 raw 字符串

## 反模式

- ❌ 不分 mode 直接 6 输入框 ——用户得想"哪个位是什么"，本来是想避免这个才做可视化
- ❌ 内置 next time 计算逻辑 —— 应该走后端解析（避免前后端时区偏差）
