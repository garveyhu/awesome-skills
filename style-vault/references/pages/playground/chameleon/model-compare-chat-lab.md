---
id: pages/playground/chameleon/model-compare-chat-lab
type: page
name: 模型对比聊天实验室（单聊三栏 / 对比多列双模式）
description: 旗舰对话调试台——单聊三栏(左历史会话 + 中消息流+预设 + 右运行设置)；对比多列(左对比历史 + N 列广播同输入 + 共享 Composer)；顶栏 segmented 切换 + 溯源 KeyPicker；每条 assistant 可开 trace
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
- blocks/chat/chameleon/composer-attach-send
- blocks/chat/chameleon/message-list-bubble-thread
- components/avatars-icons/chameleon/provider-bot-avatar
- tokens/layout/waveflow/data-console-shell
- tokens/palettes/waveflow/warm-paper-ink-blue
preview: /preview/pages/playground/chameleon/model-compare-chat-lab
---

# Chameleon Model Compare Chat Lab

> Chameleon 旗舰对话调试台（`/playground`）。整页 `SectionCard !p-0` 内：**顶栏**（「Playground」标题 + 单聊/对比 segmented 切换 + `ml-auto` 溯源 KeyPicker + 对比模式额外的 新对比/加列）+ 两态主体（高 `h-[calc(100vh-150px)]`）。**单聊** = 左 历史会话侧栏(w-56) + 中 对话流(顶 bar 预设 Popover + 清空 / MessageThread 气泡 / 底 Composer) + 右 运行设置 ParamPanel(w-72)。**对比** = 左 对比历史侧栏(w-56) + 中 N 列并排（列头 渐变方块 + 模型名 + 列号 + 提升单聊/齿轮/清空/移除）+ 底部共享 Composer 广播到全部列。每条 assistant 气泡可开 TraceDrawer 溯源。

## 视觉特征

- 顶栏 `flex items-center gap-3 border-b border-stone-200/70 px-4 py-2.5`：h2 `text-[14px] font-medium text-stone-900`「Playground」；segmented `flex overflow-hidden rounded-lg border border-stone-200 text-[12px]`，每段 `px-3 py-1`，active `bg-blue-50 font-medium text-blue-700`、idle `text-stone-500`；`ml-auto` 后接 KeyPicker；对比模式追加 新对比(Sparkles)/加列(Plus)
- **KeyPicker**：SelectTrigger `!h-7 !w-[200px] gap-1.5 text-[12px]` + KeyRound `h-3.5 w-3.5 text-stone-400` + 名称 truncate；下拉项右侧 key_prefix `font-mono text-[10px] text-stone-400`；理念=模型随便用、流量必须挂一个 key 溯源记账
- **历史会话侧栏**（单聊）`aside w-56 shrink-0 border-r border-stone-200/70 bg-[var(--color-warm-2)]/30`：顶部新对话按钮 `rounded-md border border-stone-200 bg-white py-1.5 text-[12px] font-medium text-stone-700`（Plus h-3.5）；分组标签 `px-1.5 py-1 text-[10.5px] tracking-wide text-stone-400`「历史会话」；会话项 `rounded-md`，active `bg-white shadow-sm ring-1 ring-stone-200`、idle `hover:bg-white/70`；标题 `text-[12px] text-stone-700 truncate pr-10` + 副 `text-[10px] text-stone-400`「时间 · N 轮」；hover 动作 加入对比(Columns2 hover:bg-violet-50/text-violet-600)/删除(Trash2 hover:bg-rose-50/text-rose-600)
- **中主区**（单聊）`main flex min-w-0 flex-1 flex-col`：顶 bar `flex items-center justify-between border-b px-3 py-1.5`——预设 Popover 触发 `rounded px-1.5 py-1 text-[12px] text-stone-500`（Sparkles h-3.5「预设」）+ 清空 Trash2 `hover:bg-rose-50 hover:text-rose-600`；PopoverContent `!w-56 !p-1`，项 `rounded-md px-2 py-1.5 text-[12px] hover:bg-stone-100`；MessageThread 气泡流；底 Composer `border-t p-3`
- **右栏**（单聊）`aside w-72 shrink-0 overflow-auto border-l border-stone-200/70 p-4`：标题 `mb-3 text-[10.5px] tracking-wide text-stone-400`「运行设置」+ ParamPanel
- **对比历史侧栏** `aside w-56 bg-[var(--color-warm-2)]/30`：分组标签 `flex items-center gap-1`（History h-3 + 「对比历史」）；组项同会话项外观（标题 `pr-5` + 副「N 列 · 模型 · 模型」）
- **对比列**（CompareColumn）`flex min-w-0 flex-1 flex-col border-r border-stone-200/70 last:border-r-0`：header `flex items-center gap-1.5 border-b bg-[var(--color-warm-2)]/30 px-3 py-2`——渐变方块 `h-4 w-4 shrink-0 rounded bg-gradient-to-br from-violet-500 to-blue-500` + 模型名 `text-[12px] font-medium text-stone-800`（含列号 `ml-1 text-[10.5px] text-stone-400`「列 N」）+ 提升单聊(MessageSquare hover:text-blue-600) + 参数(Settings2 hover:bg-stone-100) + 清空(Trash2 hover:text-rose-600) + 移除(X hover:text-rose-600)；下方 MessageThread；底部共享 Composer 广播
- **消息气泡**（MessageThread）：bot 头像 `h-6 w-6 rounded-full bg-gradient-to-br from-violet-500 to-blue-500 text-white`（Bot h-3.5）；气泡 `rounded-2xl px-3 py-2 text-[13px] leading-relaxed`，user `rounded-tr-sm bg-blue-600 text-white`、bot `rounded-tl-sm border border-stone-200 bg-white text-stone-800 shadow-[0_1px_2px_rgba(0,0,0,0.04)]`，max-w-[88%]；footer `text-[10px] text-stone-400` 用量 `tnum font-mono ↑N ↓N` + hover 浮现 trace(ListTree hover:violet)/存样本(BookmarkPlus hover:emerald)/改写提示词(Wand2 hover:violet)

## 核心代码

```tsx
<SectionCard className="!p-0">
  <div className="flex items-center gap-3 border-b border-stone-200/70 px-4 py-2.5">
    <h2 className="text-[14px] font-medium text-stone-900">Playground</h2>
    <div className="flex overflow-hidden rounded-lg border border-stone-200 text-[12px]">
      <button className={cn('px-3 py-1', mode === 'single' ? 'bg-blue-50 font-medium text-blue-700' : 'text-stone-500')}>单聊</button>
      <button className={cn('px-3 py-1', mode === 'compare' ? 'bg-blue-50 font-medium text-blue-700' : 'text-stone-500')}>对比</button>
    </div>
    <span className="ml-auto" />
    <KeyPicker />
  </div>
  {mode === 'single' ? <SinglePane … /> : <ComparePane … />}
</SectionCard>

{/* 对比列头 */}
<header className="flex items-center gap-1.5 border-b border-stone-200/70 bg-[var(--color-warm-2)]/30 px-3 py-2">
  <span className="h-4 w-4 shrink-0 rounded bg-gradient-to-br from-violet-500 to-blue-500" />
  <span className="min-w-0 flex-1 truncate text-[12px] font-medium text-stone-800">
    {modelLabel}<span className="ml-1 text-[10.5px] font-normal text-stone-400">列 {index + 1}</span>
  </span>
  <button title="在单聊打开此列"><MessageSquare className="h-3.5 w-3.5" /></button>
  <Popover>…<Settings2 className="h-3.5 w-3.5" />…</Popover>
  <button title="清空"><Trash2 className="h-3.5 w-3.5" /></button>
  {onRemove && <button title="移除此列"><X className="h-3.5 w-3.5" /></button>}
</header>
```

## 适配指南

- 列头渐变方块 `from-violet-500 to-blue-500` 是「模型槽」的视觉锚点——每列一个，紫→蓝渐变是整页唯一的 signature 渐变（其余克制暖白）
- bot 头像同款 violet→blue 渐变小圆，呼应列头方块——「这是 AI」的统一标识
- 对比模式底部一个共享 Composer 广播到全部列（`columns.forEach(c => send(c.id, t, a))`）；单聊每列独立 Composer
- 侧栏（历史会话 / 对比历史）用 `bg-[var(--color-warm-2)]/30` 浅暖底，active 项 `bg-white shadow-sm ring-1 ring-stone-200` 浮出
- KeyPicker 自渲染 trigger 内容（不用 SelectValue 镜像）——避免长 key 名 + 前缀溢出边界
- config 跟会话走（meta.config）；model_id / kb_ids 一律 string（雪花精度），禁 Number() 转
- 每条 assistant 气泡 footer 的 trace 入口（ListTree）开 TraceDrawer，与本目录 trace-detail 页同一份链路树

## 反模式

- ❌ 列头不用渐变方块——这是对比模式唯一的「模型槽」标识，紫蓝渐变不可省
- ❌ 满屏堆渐变——除了列头方块 + bot 头像，其余一律暖白克制，渐变是 signature moment 不是底色
- ❌ 用 Number(v) 转 model_id / session_id——雪花超 MAX_SAFE_INTEGER 丢精度，全 string
- ❌ 对比模式每列各一 Composer——必须底部一个共享 Composer 广播，才叫「一次输入对照多模型」
- ❌ user 气泡用边框白底——user 实色 blue-600 + 右上 tail，bot 才是白底边框 + 左上 tail
- ❌ 历史 / 对比侧栏用纯白底——用 warm-2/30 浅暖底，active 项才靠白底 + ring 浮出
