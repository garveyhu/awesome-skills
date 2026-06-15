---
id: components/selects/waveflow/multi-select-popover
type: component
name: 多选 Popover
description: trigger + popover + 可搜索 + 选项 checkbox + 已选 count chip + 清空按钮的多选下拉
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm]
  stack: [shadcn-radix]
uses:
  - components/inputs/waveflow/blue-focus-input
preview: /preview/components/selects/waveflow/multi-select-popover
---

# Waveflow Multi-Select Popover

> waveflow 多选下拉（`components/ui/multi-select.tsx`）—— Radix Popover 包 Trigger + Checkbox 列表 + Search 输入。Trigger 显示 placeholder + 末尾 count chip（"已选 3"）。专给 jobInfo / jobSet 等"按项目多选"场景用。

## 视觉特征

- **Trigger**：
  - 复用 `<SelectTrigger>` 同款 className（`flex h-8 items-center justify-between border-stone-300 px-3 text-[13px]` + `hover:border-stone-400 focus:border-blue-500 focus:ring-2 focus:ring-blue-100`）
  - 内容区：placeholder text-stone-400 + 末尾 `<span className="rounded bg-stone-100 px-1.5 py-0.5 text-[10.5px] font-mono tnum text-stone-600">已选 {n}</span>`
  - 右侧 ChevronDown 14px 灰
- **size sm/md**：`h-7 text-[12px]` / `h-8 text-[13px]`
- **Popover Content**：
  - `bg-[var(--color-paper)] border-stone-200/60 rounded-lg shadow-[var(--shadow-pop)] p-1`
  - 搜索框：`<Input className="!h-7 pl-6 text-[12px]" />` + search icon 绝对定位
  - 选项行：`flex items-center gap-2 rounded px-2 py-1.5 cursor-pointer hover:bg-stone-100` + Checkbox + 文本
  - 高度限制：`max-h-[280px] overflow-y-auto`
- **showCountTag prop**：trigger 显示 count chip
- **searchable prop**：选项数 > 8 推荐开启

## 适配指南

- 用法：`<MultiSelect value={ids} onChange={setIds} options={[{value, label}]} searchable showCountTag triggerWidth={130} />`
- options 通常从接口数据 map：`projects.map(p => ({ value: p.id!, label: p.name }))`
- 切换选项后立即调 `setPage(1)`——避免老分页号超出新结果范围
- 关闭 popover 时不清空 search query 也行——下次打开还在原 query（用户大概率想接着筛）

## 反模式

- ❌ 把多选改成 modal——杀鸡用牛刀
- ❌ 不给 max-h——选项 50+ 直接撑出屏幕
- ❌ Trigger 不显示 count——用户不知道选了几个
