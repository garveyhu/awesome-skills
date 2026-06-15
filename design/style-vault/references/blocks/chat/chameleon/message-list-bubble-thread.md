---
id: blocks/chat/chameleon/message-list-bubble-thread
type: block
name: 气泡式对话流（虚拟滚动）
description: Playground/widget 共用对话流：bot 渐变头像 + 白底左上 tail 气泡，user blue-600 右上 tail，VirtualList stickToBottom，footer 常显 token 用量 + hover 浮现 trace/存样本/改写动作
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
- blocks/display/waveflow/data-table-leftbar-shimmer
- components/avatars-icons/chameleon/provider-bot-avatar
- components/feedback/chameleon/neon-loader
- components/feedback/chameleon/loading-skeleton-kit
- tokens/palettes/waveflow/warm-paper-ink-blue
preview: /preview/blocks/chat/chameleon/message-list-bubble-thread
---

# Chameleon Message List Bubble Thread · 气泡式对话流

> Playground / widget 共用的对话流：assistant 左侧带**紫蓝渐变 Bot 头像**气泡（左上直角 tail）、user 右侧 **blue-600 实色**气泡（右上直角 tail）；走 `VirtualList` 虚拟滚动 + `stickToBottom` 黏底。流式空内容显示 `NeonLoader「思考中…」` 或 `ImageGenLoading` 骨架；含附件预览（图/音频/文件 chip）、failed 红气泡、pinned 琥珀 ring、footer **常显 token 用量（↑↓）**、hover 浮现 **trace / 存样本 / 改写提示词** 三个调试入口。这是 Chameleon「可调试对话」的旗舰表面，waveflow 无对话。

源码：`system/playground/components/message-thread.tsx`（整文件，重点 `:37-349`）。

## 视觉特征

### 行外层

- `group flex gap-2(8)`，user `flex-row-reverse` / bot `flex-row`，`msg.stale` → `opacity-50`
- VirtualList `estimateSize={72} stickToBottom`，外层 `flex-1 px-4 pt-4`，itemClassName `pb-4`

### Bot 渐变头像

- `mt-0.5 h-6 w-6(24) shrink-0 rounded-full bg-gradient-to-br from-violet-500(#8b5cf6) to-blue-500(#3b82f6) text-white`，内 `Bot h-3.5 w-3.5(14)`

### 气泡

- 容器 `flex min-w-0 max-w-[88%] flex-col gap-1(4)`，user `items-end` / bot `items-start`
- 本体 `min-w-0 rounded-2xl(16) px-3(12) py-2(8) text-[13px] leading-relaxed`
  - user → `rounded-tr-sm(2) bg-blue-600(#2563eb) text-white`
  - bot → `rounded-tl-sm(2) border border-stone-200 bg-white text-stone-800 shadow-[0_1px_2px_rgba(0,0,0,0.04)]`
  - failed → `!border-rose-200 !bg-rose-50 !text-rose-700`
  - pinned → `ring-1 ring-amber-300`
- 错误副行 `mt-1 text-[12px] text-rose-600`

### 流式 / 暂停态（气泡内空内容时）

- mediaKind 有值 → `ImageGenLoading className="w-60"`（骨架 + 计时）
- 否则 → `NeonLoader size="sm" label="思考中…"`（霓虹旋转环 + 流光字）
- paused → `text-amber-600`「⏸ 等待人工输入…」
- 空回复 → `text-stone-400`「（空回复）」

### footer（常显 + hover 动作）

- `flex items-center gap-2(8) px-1 text-[10px] text-stone-400`，user 反向
- pinned `text-amber-600`「📌」；streaming `text-blue-600`「生成中…」；stale「已替换」
- 用量 `tnum font-mono`「↑{in} ↓{out}」常显
- hover 动作组 `flex items-center gap-1 opacity-0 transition group-hover:opacity-100`：
  - trace（需 requestId）`hover:bg-violet-50 hover:text-violet-600`，`ListTree h-3 w-3` + 「trace」
  - 存样本 `hover:bg-emerald-50 hover:text-emerald-600`，`BookmarkPlus h-3 w-3` + 「存样本」
  - 改写提示词 `hover:bg-violet-50 hover:text-violet-600`，`Wand2 h-3 w-3` + 「改写提示词」
  - 三个动作按钮 `flex items-center gap-0.5 rounded px-1 py-0.5 text-stone-400`
  - 末尾接 `MessageActions`（玻璃质感动作条）

### 附件预览（AttachmentPreview）

- 图 → `block overflow-hidden rounded-lg border border-stone-200/70 hover:border-blue-300`，img `h-28 w-28(112) object-cover`
- 音频 → `audio controls h-8 max-w-[280px] rounded-md`
- 文件 → `inline-flex items-center gap-1 rounded-full border border-stone-200/70 bg-stone-50/60 px-2.5 py-1 text-[11px] text-stone-700`「📎 文件名」hover `border-blue-300 bg-blue-50/40`

### 编辑态（user 消息编辑）

- 整条换 `flex flex-col gap-1.5 rounded-xl border border-stone-200 bg-white p-2`，内 `Textarea rows=3 text-[13px]` + 右下「取消」(ghost) / 「提交并重发」(primary, disabled 空)

### 空态

- `flex flex-1 items-center justify-center text-[12px] text-stone-400`「输入消息开始对话」

## 核心代码

```tsx
// 渐变 bot 头像
{!isUser && (
  <div className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-violet-500 to-blue-500 text-white">
    <Bot className="h-3.5 w-3.5" />
  </div>
)}

// 气泡本体（tail 直角 + 状态叠加）
<div className={cn(
  'min-w-0 rounded-2xl px-3 py-2 text-[13px] leading-relaxed',
  isUser ? 'rounded-tr-sm bg-blue-600 text-white'
         : 'rounded-tl-sm border border-stone-200 bg-white text-stone-800 shadow-[0_1px_2px_rgba(0,0,0,0.04)]',
  msg.status === 'failed' && '!border-rose-200 !bg-rose-50 !text-rose-700',
  msg.pinned && 'ring-1 ring-amber-300',
)}>

// footer 用量常显 + hover trace
{msg.usage && <span className="tnum font-mono">↑{msg.usage.input_tokens} ↓{msg.usage.output_tokens}</span>}
<button className="flex items-center gap-0.5 rounded px-1 py-0.5 text-stone-400 transition hover:bg-violet-50 hover:text-violet-600">
  <ListTree className="h-3 w-3" /> trace
</button>
```

## 适配指南

- 走 VirtualList（`estimateSize=72 stickToBottom`）支撑长对话——不要裸 map 渲染
- bot 头像渐变 `from-violet-500 to-blue-500` 是 AI 的霓虹强调，与气泡的暖白克制形成对比（signature）
- tail 直角放贴头像侧：bot 左上 `rounded-tl-sm`、user 右上 `rounded-tr-sm`，2px 直角
- token 用量常显（不 hover 才出）——「可调试」语义：随时看消耗
- trace / 改写走紫（violet）、存样本走绿（emerald）——三个调试动作各自语义色
- 流式态分流：媒体生成用骨架计时（耗时长），文本用霓虹「思考中…」

## 反模式

- ❌ 气泡四角全圆——贴头像那角必须 2px 直角做指向
- ❌ user 气泡用渐变 / bot 头像用实色——头像渐变 + 气泡克制的对比是 signature，别反过来
- ❌ footer 把用量也藏进 hover——用量要常显（可调试）
- ❌ 流式空内容显「生成中」纯文字——用 NeonLoader 霓虹环 / ImageGenLoading 骨架，给高级观感
- ❌ 长对话裸渲染——必须虚拟滚动 + stickToBottom
- ❌ 把 trace/存样本/改写糊成一个「更多」——三个调试入口要直接可见（hover 即出）
