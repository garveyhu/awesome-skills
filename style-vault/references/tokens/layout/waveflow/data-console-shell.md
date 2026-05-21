---
id: tokens/layout/waveflow/data-console-shell
type: token
name: 数据控制台外壳布局
description: 240px sidebar (折叠态 56px) + 48px topbar + main grid 三段式 admin 控制台布局
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, industrial]
  mood: [calm, serious]
  stack: [shadcn-radix]
uses: []
preview: /preview/tokens/layout/waveflow/data-console-shell
---

# Waveflow Data Console Shell

> waveflow 整站结构骨架：**左 sidebar (240px / 折叠 56px)** + **右上 topbar (48px)** + **右下 main (剩余 + 自动滚)**。Layout 组件不 unmount，切菜单只切 Outlet，避免整屏闪烁。整页底色 `bg-[var(--color-warm)]`，sidebar 底色 `bg-[var(--color-warm-2)]`，main 卡片底色 `bg-[var(--color-paper)]`——三档暖白对应三档视觉层级。

## Tokens

```json
{
  "viewport": "h-screen overflow-hidden flex",
  "sidebar": {
    "expanded": "w-60 (240px) flex-shrink-0 flex-col",
    "collapsed": "w-14 (56px) flex-shrink-0 flex-col items-center",
    "background": "bg-[var(--color-warm-2)]",
    "right-border": "border-r border-stone-200/70"
  },
  "topbar": {
    "height": "h-12 (48px)",
    "padding": "px-6",
    "background": "bg-[var(--color-warm)] (= 页面底色，无对比)",
    "bottom-border": "border-b border-stone-200/70",
    "flex": "flex items-center gap-3 flex-shrink-0"
  },
  "main": {
    "flex": "flex-1 flex-col overflow-hidden",
    "outlet-wrap": "flex-1 overflow-auto [scrollbar-gutter:stable]",
    "page-padding": "px-6 py-4 (列表页) / px-6 py-5 (dashboard)"
  },
  "floating-children": [
    "<Toaster />            // 全局 sonner",
    "<SearchPanel />        // CMD+K modal portal",
    "<GlobalProgress />     // 顶部 2px progress bar"
  ],
  "page-content-shell": "rounded-xl border border-stone-200/40 bg-[var(--color-paper)] shadow-[var(--shadow-soft)] p-5"
}
```

## 视觉特征

- **整页 `h-screen overflow-hidden`**：sidebar + main 各自管自己的滚，主区滚动条不会顶掉 layout
- **`[scrollbar-gutter:stable]`**：内容区滚动条预留位，避免内容宽度随滚动闪
- **页面外框 `px-6 py-4` + 内卡片 `rounded-xl + paper + soft shadow + p-5`**：是所有 list 页的固定双层模式
- **三档暖白做层级**：warm → warm-2 → paper，越往内越亮——给"卡片浮在底上"的感觉
- **Layout 不 unmount**：sidebar 永远 mount，切菜单只切 `<Outlet />`——避免侧栏闪一下

## 适配指南

- 用 React Router v6 `<Outlet />` 嵌套，**不要把 Layout 放到每个 page 里**
- `<React.Suspense fallback={null}>` 配合顶部 GlobalProgress 做切页指示，**不要让 Suspense 闪 spinner**
- 内 page 一律：`<div className="h-full px-6 py-4"><section className="rounded-xl border border-stone-200/40 bg-[var(--color-paper)] shadow-[var(--shadow-soft)] p-5">...</section></div>`

## 反模式

- ❌ 给 sidebar 加固定阴影——让侧栏"飘起来"破坏暖底统一感
- ❌ 给主区滚动条隐藏（`scrollbar-width:none`）——管理后台必须看见滚动位置
- ❌ topbar 高度不固定——会被内容推走
