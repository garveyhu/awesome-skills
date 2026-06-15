---
id: components/buttons/sage/icon-circle-ghost
type: component
name: 圆形透明图标按钮
description: 透明底圆形按钮，hover 时显灰底，sage 整站工具栏 / header / 会话项右侧操作的标配
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/sage/neutral-rgb-ladder
preview: /preview/components/buttons/sage/icon-circle-ghost
---

# Icon Circle Ghost

> sage 整站"次要图标按钮"的形态——透明底，hover 时变灰底，一个 lucide 图标，色阶用 slate-400/500 / slate-600/700。Chat header 的 MoreVertical / Logo 切换 / Sidebar 折叠按钮全是这个形态。

## 视觉特征

- 默认：`p-2 text-slate-400 hover:text-slate-600 transition-colors rounded-full hover:bg-slate-100` 或 `hover:bg-[rgb(242,242,242)]`
- 8x8 / 24x24 / 32x32 三档大小：`w-8 h-8 flex items-center justify-center rounded-full`
- 危险态变体：`hover:bg-red-100 hover:text-red-600` 用于关闭 admin overlay
- group hover 显示：搭配 `opacity-0 group-hover:opacity-100`，平时不可见，悬停时浮现
- 双图标切换（如 logo/PanelLeftOpen）：用 `absolute inset-0` 叠加 + `group-hover:opacity-0` / `group-hover:opacity-100` 互斥

## 核心代码

```tsx
import { MoreVertical } from 'lucide-react';

// 默认
<button className="p-2 text-slate-400 hover:text-slate-600 hover:bg-[rgb(242,242,242)] rounded-full transition-colors">
  <MoreVertical size={20} />
</button>

// 双图标切换（侧栏折叠时的 logo + open）
<button className="group relative w-8 h-8 flex items-center justify-center rounded-full hover:bg-slate-100 transition-all">
  <div className="absolute inset-0 flex items-center justify-center transition-opacity duration-200 group-hover:opacity-0">
    <img src={logo} className="w-6 h-6" />
  </div>
  <div className="absolute inset-0 flex items-center justify-center opacity-0 transition-opacity duration-200 group-hover:opacity-100 text-slate-600">
    <PanelLeftOpen size={20} />
  </div>
</button>

// 危险态（关闭 admin overlay）
<button className="p-2 rounded-full bg-slate-100 hover:bg-red-100 text-slate-500 hover:text-red-600 transition-colors shadow-sm">
  <X size={20} />
</button>
```

## 适配指南

- 图标只用 lucide-react，size 16/18/20，stroke 默认（不显式调）
- hover 底色：常规用 `bg-slate-100`，"主交互区"（chat header / 会话操作）用 RGB 灰阶 `bg-[rgb(242,242,242)]`
- 不传任何 themeColor —— 这个按钮永远是中性色，不参与主题着色

## 反模式

- ❌ 改成主题色 hover —— 这是"次要"按钮，主题色留给主操作
- ❌ 加 border / shadow —— 破坏 ghost 感
