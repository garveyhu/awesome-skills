---
id: blocks/nav/chameleon/cmdk-grouped-palette
type: block
name: 600px cmdk 四分组命令面板
description: 基于 cmdk 库的 600px 命令面板 - 12vh 落下 + Search 输入(Esc kbd) + 四分组(搜索结果/跳转/动作/最近访问) + 蓝选中 + footer 快捷键提示
platforms:
- web
theme: light
tags:
  aesthetic:
  - editorial
  - minimal
  mood:
  - calm
  - confident
  stack:
  - shadcn-radix
uses:
- components/typography-atoms/waveflow/kbd-key-cap
- tokens/palettes/waveflow/warm-paper-ink-blue
- tokens/shadow/waveflow/soft-card-pop-trio
preview: /preview/blocks/nav/chameleon/cmdk-grouped-palette
---

# Chameleon cmdk 四分组命令面板

> 全站 ⌘K 命令面板，基于 `cmdk` 库。遮罩 `bg-stone-950/40 backdrop-blur-sm`，面板从顶部 10vh 落下，600px 宽。顶部 Search 输入行（h-12 + 末尾 Esc kbd）+ 四语义分组列表（**搜索结果 / 跳转 / 动作 / 最近访问**）+ footer 快捷键提示。选中态走蓝色（`blue-50` 底 + `blue-700` 字），防抖 200ms 调 searchApi，最近访问存 localStorage（`chameleon.recent_pages`，max 8）。

## 视觉特征

- **遮罩 `fixed inset-0 z-[100] flex items-start justify-center bg-stone-950/40 backdrop-blur-sm`**：半透深底 + 轻磨砂
- **Command 容器 `relative mt-[10vh] w-[600px] max-w-[90vw] overflow-hidden rounded-xl(12px) border border-stone-200 bg-paper(#fffefb) shadow-pop`** + `flex flex-col max-h-[70vh]`
- **输入行 `flex items-center gap-2 border-b border-stone-100 px-4(16px)`**：
  - `Search` icon `h-4 w-4 text-stone-400 strokeWidth={1.75}`
  - `Command.Input` `flex h-12(48px) w-full bg-transparent text-[13.5px] text-stone-800 placeholder:text-stone-400 outline-none`
  - Esc kbd：`rounded border border-stone-200 px-1.5 py-0.5 text-[10px] font-mono text-stone-400`（sm 以上 inline-block）
- **List `flex-1 overflow-y-auto px-2 py-2`**
- **`.cmdk-group`**：`padding: 4px 0`
- **group-heading**：`padding: 6px 10px 4px; font-size: 10.5px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; color: rgb(120 113 108)`(stone-500)
- **`.cmdk-item`**：`display: flex; align-items: center; gap: 10px; padding: 7px 10px; border-radius: 6px; font-size: 12.5px; transition: background 0.12s`
  - `[data-selected=true]`：`background: rgb(239 246 255)`(blue-50) + `color: rgb(29 78 216)`(blue-700)
  - `:hover`：`background: rgb(245 244 238)`(warm-2)
- **四组结构**：
  - **搜索结果**（仅 query 时）：icon ICON_MAP（bot/cpu/cloud/library/key/users/puzzle）`h-3.5 w-3.5 text-stone-400` + title `font-medium text-stone-800` + snippet `ml-2 font-mono text-[10.5px] text-stone-400` + 右侧类型 chip `rounded bg-stone-100 px-1.5 py-0.5 text-[10px] font-medium text-stone-500`
  - **跳转**（NAV_ITEMS）：icon + label `text-stone-700` + 右侧 path `font-mono text-[10.5px] text-stone-400`
  - **动作**（ACTIONS：Plus/Download/KeyRound/LogOut）：icon + label
  - **最近访问**（仅无 query 时）：`History` icon + label + path
- **footer `flex items-center gap-3 border-t border-stone-100 bg-warm-2/30 px-3 py-2 text-[10.5px] text-stone-400`**：↑↓ 导航 / ⏎ 选择 / `ml-auto` 处 Code2 `h-3 w-3` + ⌘K kbd；footer kbd 风格 `rounded border border-stone-200 bg-paper px-1 py-0.5 font-mono`

## 核心代码

```tsx
<Command loop label="命令面板" shouldFilter
  className="relative mt-[10vh] w-[600px] max-w-[90vw] overflow-hidden rounded-xl border border-stone-200 bg-paper shadow-pop flex flex-col max-h-[70vh]">
  <div className="flex items-center gap-2 border-b border-stone-100 px-4">
    <Search className="h-4 w-4 text-stone-400" strokeWidth={1.75} />
    <Command.Input className="flex h-12 w-full bg-transparent text-[13.5px] ... outline-none" />
    <kbd className="... text-[10px] font-mono text-stone-400">Esc</kbd>
  </div>
  <Command.List className="flex-1 overflow-y-auto px-2 py-2">
    <Command.Group heading="搜索结果" className="cmdk-group">…</Command.Group>
    <Command.Group heading="跳转" className="cmdk-group">…</Command.Group>
    <Command.Group heading="动作" className="cmdk-group">…</Command.Group>
    <Command.Group heading="最近访问" className="cmdk-group">…</Command.Group>
  </Command.List>
  <div className="flex items-center gap-3 border-t border-stone-100 bg-warm-2/30 px-3 py-2 ...">…</div>
</Command>
```

lucide: Search / Bot / Cloud / Code2 / Cpu / Download / History / Key / KeyRound / LayoutDashboard / Library / LogOut / Plus / Puzzle / Settings / Shield / Users。

## 适配指南

- 用真 `cmdk` 库（`shouldFilter` + `loop`），别手写键盘导航
- 搜索结果仅 `debouncedQ` 非空时渲染；最近访问仅 query 为空时渲染——两者互斥占位
- 选中态用 `[data-selected='true']` 不是 `:hover`——cmdk 键盘高亮走 data 属性
- 防抖 200ms 才请求；`staleTime 30s` 缓存

## 与 waveflow/cmdk-search-modal 区分

| 维度 | waveflow cmdk-search-modal | 本条 cmdk-grouped-palette |
|------|----------------------------|---------------------------|
| 尺寸 | 720×560 | 600px（max-h-70vh） |
| 结构 | 左 136px **类型 sidebar** + 右结果区 | 纯 cmdk 库、**无类型 sidebar**，靠 4 个语义分组组织 |
| 高亮 | `amber-100` 高亮匹配 + `stone-900` 黑底 active（键盘风） | **`blue-50`/`blue-700` 蓝选中**（克制） |
| 分组 | 按类型 sidebar 切 | **搜索结果 / 跳转 / 动作 / 最近访问** 四语义组 |
| 数据 | 静态结果 | 防抖 200ms 调 searchApi + localStorage 最近访问（max 8） |

选条原则：要「左类型 sidebar + amber/黑底键盘风」用 waveflow；要「纯 cmdk 四分组 + 蓝选中 + 实时搜索 + 最近访问」用本条。

## 反模式

- ❌ 手写 keydown 上下导航——用 cmdk 的 `loop`，省掉边界处理
- ❌ active 用 stone-900 黑底——那是 waveflow 键盘风，本条走蓝克制选中
- ❌ 搜索结果 + 最近访问同屏都显示——按 query 互斥
- ❌ footer kbd 不用 `bg-paper`——会与 warm-2/30 footer 底融在一起看不清
