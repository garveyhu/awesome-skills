---
id: blocks/chat/chameleon/message-actions-bar
type: block
name: 消息动作工具条（玻璃质感）
description: 单条消息 hover 浮现的玻璃质感动作条（半透明白底 + backdrop-blur），主操作内联、次操作收进 ⋯ DropdownMenu；纯函数 resolveActions 按 role+status 分组
platforms:
- web
theme: light
tags:
  aesthetic:
  - minimal
  - industrial
  mood:
  - calm
  - serious
  stack:
  - shadcn-radix
uses:
- tokens/palettes/waveflow/warm-paper-ink-blue
preview: /preview/blocks/chat/chameleon/message-actions-bar
---

# Chameleon Message Actions Bar · 消息动作工具条

> 单条消息 hover 浮现的**玻璃质感动作条**：`bg-white/90 + backdrop-blur`，主操作（copy/edit/regenerate/👍/👎）内联 12px 微图标，次操作（continueGen/translate/tts/branching/pin/export/share/delete）收进 `⋯` DropdownMenu。translate 配语言列表时渲染为子菜单；copy/tts/export/share 自带默认实现。纯函数 `resolveActions` 按 role+status 决定哪些可用、各落主条还是菜单（流式 / HITL 暂停只留 copy）。跨 playground / conversations / widget 复用。

源码：`core/components/chat/message-actions.tsx:99-359` · `resolve-actions.ts:1-110`。

## 视觉特征

### 工具条容器

- `pointer-events-auto flex items-center gap-0.5(2) rounded-md(6) border border-stone-200/70 bg-white/90 p-0.5(2) shadow-sm backdrop-blur`
- 浮现：`opacity-0 group-hover:opacity-100 focus-within:opacity-100 transition`——默认隐藏，hover 消息组 / 聚焦时显
- 玻璃感来自 `bg-white/90 + backdrop-blur`（半透明白 + 背景模糊）

### ActionBtn（主条按钮）

- `rounded px-1 py-1 text-stone-500`，icon 统一 `h-3 w-3(12)`
- hover（普通）`bg-stone-100 text-stone-800`；hover（danger）`bg-rose-50 text-rose-600`
- active（普通）`bg-amber-100 text-amber-800`；active（danger）`bg-rose-100 text-rose-700`
- disabled `cursor-not-allowed opacity-40`
- copied 态：图标换 `Check h-3 w-3 text-emerald-600`
- tts 朗读中：图标换 `VolumeX`；pin 已置顶：图标换 `PinOff`

### ⋯ 下拉

- 触发 `rounded px-1 py-1 text-stone-500 hover:bg-stone-100 hover:text-stone-800`，icon `MoreHorizontal h-3 w-3`
- `DropdownMenuContent align=end min-w-[9rem]`
- **MenuRow** `flex items-center gap-2`：icon `text-stone-500` + label `text-[12.5px]`
- delete 菜单项前置 `DropdownMenuSeparator`，`text-rose-600 hover:bg-rose-50 hover:text-rose-700`
- active 菜单项（pin/tts 等）`text-amber-700`
- translate 配语言列表 → `DropdownMenuSub`（子菜单列语言）

### 图标集（lucide）

`Copy / Pencil / RefreshCw / Trash2 / ThumbsUp / ThumbsDown / Split / Languages / ArrowDownFromLine / Volume2 / VolumeX / Download / Share2 / Pin / PinOff / Check / MoreHorizontal`

## 核心代码

```ts
// resolve-actions.ts —— 纯函数分组
const PRIMARY_ORDER = ['copy', 'edit', 'regenerate', 'thumbsUp', 'thumbsDown'];
const MORE_ORDER = ['continueGen', 'translate', 'tts', 'branching', 'pin', 'export', 'share', 'delete'];
const BUILT_IN = new Set(['copy', 'tts', 'export', 'share']);  // 无 handler 也可渲染

export function resolveActions(msg, handlers, hidden): { primary; more } {
  // 流式中 / HITL 暂停中只留 copy（重发会丢 pending）
  if (msg.status === 'streaming' || msg.status === 'paused') return { primary: ['copy'], more: [] };
  const pick = order => order.filter(k => isAvailable(k, msg, handlers, hidden));
  return { primary: pick(PRIMARY_ORDER), more: pick(MORE_ORDER) };
}
```

```tsx
// message-actions.tsx —— 玻璃条 + active 配色
<div className={cn(
  'pointer-events-auto flex items-center gap-0.5 rounded-md border border-stone-200/70 bg-white/90 p-0.5 shadow-sm backdrop-blur transition',
  'opacity-0 group-hover:opacity-100 focus-within:opacity-100',
)}>
  {/* ActionBtn active 态 */}
  className={cn('rounded px-1 py-1 text-stone-500 transition',
    danger ? 'hover:bg-rose-50 hover:text-rose-600' : 'hover:bg-stone-100 hover:text-stone-800',
    active && (danger ? 'bg-rose-100 text-rose-700' : 'bg-amber-100 text-amber-800'))}
</div>
```

## 适配指南

- 消费方把自己的消息映射成 `ChatActionMessage`（id/role/content/status/feedback/pinned），handlers 各注入
- 主条 / 菜单分组完全由 `resolveActions` 纯函数决定——不在组件里写 if-else 判断 role
- BUILT_IN（copy/tts/export/share）即使无 handler 也渲染（自带默认实现）
- active 用琥珀（amber-100/800）统一标记「已选 / 已置顶 / 朗读中」；danger（delete）用玫瑰（rose）
- 工具条必须配在 `group` 父容器里才能 `group-hover` 浮现

## 反模式

- ❌ 全部 action 平铺主条——一排 13 个图标视觉爆炸，主 5 次 8 必须分组
- ❌ 工具条用实色白底——`bg-white/90 + backdrop-blur` 的半透明玻璃感是它的辨识点
- ❌ delete 和普通项混在一起——必须 Separator 隔开 + rose 色警示
- ❌ 流式 / 暂停态还显全部动作——会误操作丢 pending，只留 copy
- ❌ active 态用蓝色——蓝留给主操作，选中 / 置顶用琥珀
