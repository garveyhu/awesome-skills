---
id: blocks/nav/waveflow/topbar-search-ping
type: block
name: 48px 顶部栏 + ⌘K 搜索 + 在线状态
description: h-12 极简顶部栏 - 260px 搜索按钮 (⌘K Kbd) + ping 双层在线 dot + N 在线计数
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm, serious]
  stack: [shadcn-radix]
uses:
  - components/indicators/waveflow/pulse-ping-dot
  - components/typography-atoms/waveflow/kbd-key-cap
preview: /preview/blocks/nav/waveflow/topbar-search-ping
---

# Waveflow Topbar Search + Ping

> waveflow 极简顶部栏——48px 高、暖底无独立背景（和页面同色），只放两个元素：**260px 宽的"搜索任务、集合、项目"按钮**（占据视觉重心）和**ping 双层在线状态**（emerald-500 实心 + 涟漪 + N 在线 mono）。没有头像、通知、面包屑——它们都在侧栏处理了。

## 页面骨架

1. **header**: `flex h-12 flex-shrink-0 items-center gap-3 border-b border-stone-200/70 bg-[var(--color-warm)] px-6`
2. **搜索按钮**（点击触发 SearchPanel 全屏 modal）:
   - `flex w-[260px] items-center gap-2 rounded-md border border-stone-200/40 bg-[var(--color-paper)] px-3 py-1 text-[12.5px] text-stone-400 shadow-[var(--shadow-soft)] hover:border-stone-300 hover:text-stone-500`
   - Search icon 14px text-stone-400
   - 占位文字 "搜索任务、集合、项目"
   - 末尾 `<Kbd className="ml-auto">⌘K</Kbd>`
3. **在线状态**（条件渲染：online > 0 vs = 0）:
   - **在线时**：emerald ping + 计数（见 pulse-ping-dot 组件）
   - **离线时**：单层 stone-400 1.5px dot + "离线"
4. **title 属性**：搜索按钮 `title="全站搜索 ⌘K / /"`、在线状态 `title="N 个执行器在线"`

## 视觉特征

- **背景同页面 warm 底**：topbar 不"突出"——只是个不抢戏的功能条
- **下边 stone-200/70 1px**：让 main 区有"上方边界"
- **搜索按钮宽度固定 260px**：再窄会挤、再宽会"占太多"
- **paper bg + soft shadow**：搜索按钮"浮"在 warm 底上——和 sidebar item active 同款悬浮语
- **完全没有 padding-top/bottom**：靠 h-12 + items-center 撑

## 关键代码

```tsx
<header className="flex h-12 flex-shrink-0 items-center gap-3 border-b border-stone-200/70 bg-[var(--color-warm)] px-6">
  <button
    onClick={() => searchPanel.open()}
    className="flex w-[260px] items-center gap-2 rounded-md border border-stone-200/40 bg-[var(--color-paper)] px-3 py-1 text-[12.5px] text-stone-400 shadow-[var(--shadow-soft)] hover:border-stone-300 hover:text-stone-500"
    title="全站搜索 ⌘K / /"
  >
    <Search className="h-3.5 w-3.5 text-stone-400" />
    <span>搜索任务、集合、项目</span>
    <Kbd className="ml-auto">⌘K</Kbd>
  </button>
  {online > 0 ? <OnlineIndicator count={online} /> : <OfflineIndicator />}
</header>
```

## 适配指南

- 搜索按钮触发 SearchPanel modal（独立条目）
- 全局热键 hook：useSearchHotkey() 在 Layout 顶层调用，监听 ⌘K / `/`
- 不要在 topbar 加面包屑——waveflow 用 page header 处理路径

## 反模式

- ❌ 加用户头像 / 通知 / 主题切换到 topbar—— sidebar bottom user 已有
- ❌ 给 topbar 加 bg-white 高对比——破坏暖底统一感
- ❌ 搜索按钮宽度全宽—— 视觉太重
