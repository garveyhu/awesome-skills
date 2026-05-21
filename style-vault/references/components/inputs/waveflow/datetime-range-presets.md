---
id: components/inputs/waveflow/datetime-range-presets
type: component
name: 日期时间范围 + 预设
description: 触发器 + Popover 双 datetime-local input + 今天 / 昨天 / 7 天 / 30 天 等预设快捷条
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm]
  stack: [shadcn-radix]
uses: []
preview: /preview/components/inputs/waveflow/datetime-range-presets
---

# Waveflow Datetime Range Presets

> 日志页 / 任务列表用的日期时间范围选择器 (`components/ui/datetime-range-picker.tsx`)。Trigger 显示"`start ~ end`"或 placeholder + Calendar icon；点开后 Popover 里左侧一列预设按钮（今天 / 昨天 / 近 7 天 / 近 30 天 / 本月 / 上月），右侧两个原生 `<input type="datetime-local">` 让用户精确改 start / end。

## 视觉特征

- **Trigger**：
  - `flex h-8 items-center gap-2 rounded-md border border-stone-300 bg-white px-3 text-[13px] outline-none transition hover:border-stone-400`
  - Calendar icon 14px + 时间 mono 显示 + 末尾 X 清空按钮（已选时显示）
  - 时间格式：`YYYY-MM-DD HH:mm` mono tnum
- **Popover Content**：
  - 宽度 ~ 480px，`grid-cols-[160px_1fr]` 左预设列 + 右编辑区
  - **预设按钮**：`block w-full rounded px-2.5 py-1.5 text-left text-[12px] text-stone-700 hover:bg-stone-100`
  - **datetime-local input**：原生 `<input>` 但套 `<Input>` 同款 className（保持视觉一致）
  - 底部 `<Button variant="ghost" size="sm">取消</Button><Button variant="primary" size="sm">应用</Button>`
- **时间格式转换**：内部维护两份格式
  - 对外（API）：`'YYYY-MM-DD HH:mm:ss'`
  - 对 `input[datetime-local]`（浏览器原生）：`'YYYY-MM-DDTHH:mm:ss'`
  - 用 `toLocal` / `fromLocal` 双向转换

## 适配指南

- 预设列表至少 5 条：今天 / 昨天 / 近 7 天 / 近 30 天 / 本月 — 是 admin 日志场景最常需的范围
- 默认 close 行为：选择预设后**立刻 apply 并关 popover**；手动改 input 后**等用户点"应用"**
- value 接口：`{ start?: string; end?: string }`，空字符串视为未选——配合 X 清空按钮使用
- 不依赖 dayjs / date-fns，用原生 Date + 字符串解析：保持 bundle 小

## 反模式

- ❌ 用 react-day-picker 全替——原生 datetime-local 已经够用，加包浪费 30KB
- ❌ 预设按钮太多（> 8 个）——选择困难
- ❌ 不验证 start ≤ end—— 用户能搞出"反向"区间导致空查询
