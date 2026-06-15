---
id: blocks/display/waveflow/set-card-segmented
type: block
name: 任务集 button-card
description: jobSet sidebar 内单卡 - preset icon + 名称 + 计数 + SegmentedBlocks 状态条 + active blue-50/70 / hover stone-50
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, industrial]
  mood: [serious]
  stack: [shadcn-radix]
uses:
  - components/indicators/waveflow/segmented-blocks
preview: /preview/blocks/display/waveflow/set-card-segmented
---

# Waveflow Set Card Segmented

> jobSet 主从视图左侧 aside 内每个任务集是一个 button card —— `block w-full rounded-lg border p-2.5 text-left`。**头部**: 14px preset icon (用户配置 themed color) + 任务集名（12.5px font-semibold stone-900）+ 末尾成员数（10px mono tnum stone-500）。**底部**: SegmentedBlocks 状态条（每个方块 = 一个任务的状态）。active 时 `border-blue-200/50 bg-blue-50/70`。

## 视觉特征

- **基础类**：`block w-full rounded-lg border p-2.5 text-left transition`
- **active**：`border-blue-200/50 bg-blue-50/70`（蓝半透 + 蓝边）
- **default**：`border-transparent hover:bg-stone-50`（无边框 + hover 浅暖）
- **header row**: `mb-2 flex items-center gap-2`
  - preset icon 14×14 + `style={{ color: theme.fg }}`（用户配置）
  - name: `flex-1 truncate text-[12.5px] font-semibold text-stone-900`
  - count: `font-mono text-[10px] tnum text-stone-500`
- **status 行**: SegmentedBlocks（构造 statuses 数组：running × n + error × n + stopped × n + pending × n）
- **新建集合按钮**（card 列表末）：`flex w-full items-center justify-center gap-1.5 rounded-lg border border-dashed border-stone-300 px-2.5 py-1.5 text-[12px] text-stone-600 hover:bg-stone-50`

## 适配指南

- preset 系统：图标 + 主题色由后端字段 `iconName` / `themeName` 驱动，通过 `getPresetIcon()` / `getPresetTheme()` 解析；同时支持 user 自定义新 preset
- 极小 status 条（每方块 14×6px）—— 只对< 20 任务的小型集合直观；大集合用 ThreeSegmentBar 百分比
- 卡片间距：`space-y-1.5` —— 紧凑

## 反模式

- ❌ active 用蓝实色—— 失去暖底气质
- ❌ icon 大于 16px—— 抢任务集名
- ❌ 把 count 用 16px font-bold—— 跟主名抢戏
