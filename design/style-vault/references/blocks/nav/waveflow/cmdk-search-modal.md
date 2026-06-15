---
id: blocks/nav/waveflow/cmdk-search-modal
type: block
name: ⌘K 命令面板
description: 12vh-from-top 720×560 modal · 类型 sidebar(136px) + 搜索输入 + 最近 chips + 列表 + amber 高亮 + footer Kbd 提示
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [shadcn-radix]
uses:
  - components/typography-atoms/waveflow/kbd-key-cap
  - tokens/shadow/waveflow/soft-card-pop-trio
preview: /preview/blocks/nav/waveflow/cmdk-search-modal
---

# Waveflow CMDK Search Modal

> waveflow 全站搜索 panel (`components/search/SearchPanel.tsx`) ——按 ⌘K 触发，从顶部 12vh 落下 720×560px 圆角面板。**左侧 136px 类型 sidebar**（任务 / 任务集 / 项目，带 count）+ **右侧主区**（搜索输入 + 最近搜索 chips + 高亮匹配的行列表）+ **底部 footer**（↑↓导航 / ↵打开 / ⌘↵新窗口）。entry 动画 translate-y -3 + scale 0.97 → 0 + 100% 300ms ease-out。

## 页面骨架

1. **全屏遮罩 wrapper**: `fixed inset-0 z-[200] flex justify-center pt-[12vh] transition-opacity duration-200`
2. **遮罩层**: `absolute inset-0 bg-stone-900/30 backdrop-blur-[1px]`
3. **modal container**:
   - 尺寸：`h-[min(560px,calc(100vh-12vh-32px))] w-[min(720px,calc(100vw-48px))]`
   - 样式：`overflow-hidden rounded-2xl border border-stone-200/70 bg-[var(--color-paper)] shadow-[var(--shadow-pop)]`
   - entry 动画：`mounted ? 'translate-y-0 scale-100 opacity-100' : '-translate-y-3 scale-[0.97] opacity-0'` + 300ms ease-out
4. **toolbar**: `flex items-center gap-2 border-b border-stone-100 px-4 py-3`
   - Search icon 4×4 stone-400
   - input: `flex-1 bg-transparent text-[15px] tracking-tight text-stone-900 outline-none placeholder:text-stone-400`
   - 清空按钮 X 14px（q 非空时显示）
   - `<Kbd>ESC</Kbd>`
5. **最近搜索 chips**（空 query 时显示）:
   - `flex items-center gap-2 border-b border-stone-100 px-4 py-2.5`
   - 标签：`font-mono text-[10px] uppercase tracking-[0.18em] text-stone-400` "最近"
   - chips：`rounded-full border border-stone-200 px-2.5 py-0.5 text-[11.5px] text-stone-600 hover:border-stone-300`
   - 末尾 "清除" 链接
6. **body**: `flex min-h-0 flex-1`
   - **类型 sidebar (136px)**：4 个按钮（全部 / 任务 / 任务集 / 项目）每个左 label 右 count mono
     - active: `bg-stone-900 text-white`
     - default: `text-stone-600 hover:bg-stone-100`
   - **content list (flex-1 overflow-y-auto p-2)**：
     - **空态**：垂直居中 ListChecks 5x5 + "暂无数据" / "没有匹配项"
     - **行**：`group flex w-full items-center gap-3 rounded-lg px-3 py-2 text-left transition` + `active ? 'bg-stone-100' : 'hover:bg-stone-100/70'`
     - 行内：7x7 type icon 圆角方 + 标题 + 副文 highlight + 右侧操作按钮（鼠标 hover 出来）
7. **footer**: `flex items-center gap-4 border-t border-stone-100 px-4 py-2 text-[11px] text-stone-400`
   - 三段：`<Kbd>↑</Kbd><Kbd>↓</Kbd> 导航` / `<Kbd>↵</Kbd> 打开` / `<Kbd>⌘</Kbd><Kbd>↵</Kbd> 新窗口`

## 视觉特征

- **匹配高亮**：`<mark className="rounded bg-amber-100 px-0.5 text-stone-900">{matched}</mark>` —— 整站唯一使用 amber-100 的地方
- **类型 sidebar active 反显**：stone-900 黑底 + 白字 + 灰 count——比 blue 更"键盘党"
- **类型 icon 配色**：job FileText text-blue-500 / jobSet Layers text-violet-500 / jobProject FolderKanban text-amber-500
- **入场动画 -3px 上移 + 0.97 缩放**：极轻——给"从顶部落下"的物理感
- **遮罩 stone-900/30 + backdrop-blur-[1px]**：1px 模糊 + 30% 黑——既"穿透"又"分层"
- **keyboard nav**：↑↓ 控制 kbIdx、↵ openItem、⌘↵ 新窗口、ESC 关闭

## 适配指南

- 全站热键 hook (useSearchHotkey)：监听 `metaKey + K` 和 `/`（input 之外）；ESC 关闭由 panel 自己处理
- 最近搜索存 localStorage `waveflow-search-recent`，最多 5 条，FIFO
- POP navigation 复活：用户后退到上一页时如果之前 panel 是开的，自动 reopen
- 搜索 registry 异步加载：第一次按 ⌘K 才 import + fetch

## 反模式

- ❌ 类型 sidebar active 用 blue 而非 stone-900——失去"命令面板"键盘感
- ❌ 高亮用其它颜色（如 yellow-300）—— amber-100 是 waveflow 唯一指定的高亮色
- ❌ entry 动画过大（translate -8px+）—— 让人晕
- ❌ 不带最近搜索—— 用户重复同 query 时摩擦大
