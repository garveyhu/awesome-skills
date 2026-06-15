---
id: blocks/nav/waveflow/icon-collapsed-sidebar
type: block
name: 56px 折叠态侧栏
description: w-14 折叠态 - logo (40×40) + 展开按钮 + icon-only 菜单 (9×9 button + 17px icon) + tooltip
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm]
  stack: [shadcn-radix]
uses: []
preview: /preview/blocks/nav/waveflow/icon-collapsed-sidebar
---

# Waveflow Icon Collapsed Sidebar

> 侧栏折叠态——w-14 (56px) icon-only，顶部 logo 大缩小框 + 展开按钮，下面是平铺所有顶级菜单（无分组、无 group / leaf 区分，子菜单合并到 "任务列表" 单项）。每个 icon button 配 title 属性给原生 tooltip。

## 页面骨架

1. **aside**: `flex h-full w-14 flex-shrink-0 flex-col items-center border-r border-stone-200/70 bg-[var(--color-warm-2)] py-2`
2. **logo 按钮**（也作为展开入口）: `mb-1 flex h-10 w-10 items-center justify-center rounded-lg hover:bg-[var(--color-paper)] hover:shadow-[var(--shadow-soft)]` 包 `<img className="h-9 w-9 object-contain" />`
3. **展开按钮**: `mb-1 flex h-7 w-9 items-center justify-center rounded-md text-stone-500 hover:bg-stone-200/60 hover:text-stone-800` 包 PanelLeftOpen 15px
4. **nav**: `flex-1 space-y-1 overflow-y-auto overflow-x-hidden`
   - 每项: `<Link className="group flex h-9 w-9 items-center justify-center rounded-lg ..." title={label}>` + `<Icon className="h-[17px] w-[17px]" />`
   - active: `bg-[var(--color-paper)] text-blue-600 shadow-[var(--shadow-soft)]`
   - default: `text-stone-600 hover:bg-[var(--color-paper)] hover:shadow-[var(--shadow-soft)]`

## 视觉特征

- **logo 9×9（=36px）放在 10×10 button 框里**：上下左右各 2px 缝，hover 时框升起
- **菜单按钮 9×9 = 36×36px**：和 logo 框等宽，垂直对齐
- **icon 17px**：和展开态一致——折叠不缩 icon
- **active 改 paper bg + blue-600 icon**：和展开态同款语义，但少了文字
- **不显示 count / dot**：折叠态视觉极简，把任务数等信息隐藏

## 适配指南

- `useState(collapsed)` 在 Layout 组件维护，sidebar 接 props
- 折叠展开切换平滑：用 `width transition` 不需要，**直接换 component**——这是 waveflow 的实做，两态完全不同
- icon 项不要太密——10+ 项要分两段（一段 nav 一段底部）

## 反模式

- ❌ 折叠后 icon 缩到 12px—— 失去识别度
- ❌ 折叠态 active 用 ring 而非 bg + shadow——和展开态语言不一致
- ❌ 折叠状态保存到 localStorage —— waveflow 不做（每次新 session 默认展开）
