---
id: components/toggles/waveflow/emerald-switch
type: component
name: Emerald 开关
description: h-5 w-9 Radix Switch + checked emerald-500 / unchecked stone-300 + thumb h-4 w-4 white + translate-x-4 切换
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm]
  stack: [shadcn-radix]
uses: []
preview: /preview/components/toggles/waveflow/emerald-switch
---

# Waveflow Emerald Switch

> waveflow 任务"开/关"切换的视觉标识——开 emerald-500、关 stone-300，比 shadcn 默认 (`bg-input`) 更"语义化"——任务在跑 = 绿。h-5 w-9 (20×36px) 紧凑、thumb 4px 内边距。整站任务列表 / 任务集 / 配置 dialog 全用它。

## 视觉特征

- **Root 尺寸**：`peer inline-flex h-5 w-9 shrink-0 cursor-pointer items-center rounded-full border-2 border-transparent transition`
- **focus ring**：`focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-200`（**蓝**而非 emerald——避免双绿）
- **disabled**：`disabled:cursor-not-allowed disabled:opacity-50`
- **state 切换**：
  - `data-[state=checked]:bg-emerald-500`
  - `data-[state=unchecked]:bg-stone-300`
- **Thumb 尺寸**：`pointer-events-none block h-4 w-4 rounded-full bg-white shadow-sm ring-0 transition-transform`
- **Thumb 平移**：
  - `data-[state=checked]:translate-x-4`（向右 16px）
  - `data-[state=unchecked]:translate-x-0`
- 整体高 20px + thumb 16px → 上下各 2px 缝隙（看起来"刚好包住"）

## 核心代码

```tsx
<SwitchPrimitive.Root
  className={cn(
    'peer inline-flex h-5 w-9 shrink-0 cursor-pointer items-center rounded-full border-2 border-transparent transition',
    'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-200',
    'disabled:cursor-not-allowed disabled:opacity-50',
    'data-[state=checked]:bg-emerald-500 data-[state=unchecked]:bg-stone-300',
  )}
>
  <SwitchPrimitive.Thumb className="pointer-events-none block h-4 w-4 rounded-full bg-white shadow-sm ring-0 transition-transform data-[state=checked]:translate-x-4 data-[state=unchecked]:translate-x-0" />
</SwitchPrimitive.Root>
```

## 适配指南

- 用 emerald-500 (running 同色) 表达"this is ON"——比 blue 更准确
- 表格行内开关一律 `width: 70px` 列、`align: left`，Switch 自然紧贴左边
- 乐观更新：`onCheckedChange={c => handleToggle(row, c)}` 内先 `setRows(... triggerStatus: c)`，再 await API，失败 revert
- 配合 `<Tooltip>` 给"启动/暂停"语义

## 反模式

- ❌ 用 blue 做 checked——和 primary CTA 撞色
- ❌ thumb 大小 = root 高度——失去"动起来"的视觉感
- ❌ Switch 在 lg 表格里改 w-12—— 破坏全站一致性
