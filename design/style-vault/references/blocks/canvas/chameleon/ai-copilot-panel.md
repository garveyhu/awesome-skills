---
id: blocks/canvas/chameleon/ai-copilot-panel
type: block
name: 右侧 AI 编排助手对话面板
description: Gamma 式右侧滑入 AI 助手 - 对话气泡流（用户蓝 600 / 助手 slate-100 / 错误 rose）+ 进行中阶段进度气泡（调模型 / 生成 N 字 / 校验 / 重试）+ 每轮 trace 链接 + 底部多行输入 + 蓝色发送圆钮
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
- tokens/motion/chameleon/canvas-edge-dash-flow
- tokens/palettes/chameleon/node-type-hue-system
preview: /preview/blocks/canvas/chameleon/ai-copilot-panel
---

# 右侧 AI 编排助手对话面板

> 工作流编辑器画布右侧常驻的 Gamma 式 AI 助手：把「当前画布 spec + 本轮指令」发给后端流式生成修改后的图，对话气泡流呈现，进行中用阶段进度气泡（调模型 / 生成 N 字 / 校验 / 修正重试）实时投影 SSE 事件，每轮 assistant 消息附 trace 链接。

源码：`src/system/graphs/components/ai-copilot-panel.tsx`（`AiCopilotPanel` 外层加载会话 + `CopilotChat` 内层）。

## 视觉特征

- **外壳**：`aside` `w-96`（384px）`flex h-full flex-col bg-white`，入场 `animate-in fade-in slide-in-from-right-2 duration-200`（淡入 + 从右 8px 滑入，200ms）
- **头部** `border-b border-slate-200/80 px-4 py-3 flex items-center gap-2`：
  - 图标块 `h-7 w-7 rounded-lg bg-blue-50 text-blue-600`（28px，bg `#eff6ff` / 字 `#2563eb`），内 `Sparkles h-3.5 w-3.5`（14px）
  - 标题 `text-[13px] font-semibold text-stone-900`「AI 编排助手」
  - 副标题 `text-[10.5px] text-stone-400`
  - 清空按钮 `rounded-lg p-1.5 text-stone-400 hover:bg-rose-50 hover:text-rose-600` + `Trash2 h-[14px]`（仅有消息时）
  - 关闭按钮 `rounded-lg p-1.5 text-stone-400 hover:bg-stone-100 hover:text-stone-700` + `X h-[15px]`
- **消息流** `min-h-0 flex-1 space-y-2.5 overflow-y-auto px-4 py-3`：
  - 气泡 `max-w-[85%] rounded-xl px-3 py-2 text-[12px] leading-relaxed whitespace-pre-wrap`
  - user：`bg-blue-600 text-white`（`#2563eb` / 白），靠右 `justify-end`
  - assistant：`bg-slate-100 text-stone-700`（`#f1f5f9` / `#44403c`），靠左
  - error：`bg-rose-50 text-rose-700 ring-1 ring-rose-200`（`#fff1f2` / `#be123c`，内描边 `#fecdd3`）
  - trace 链接：气泡内 `mt-1 flex items-center gap-1 text-[10.5px] text-blue-500 hover:text-blue-600 hover:underline` + `ExternalLink h-3`
- **进度气泡**（生成中）：`min-w-[200px] space-y-1.5 rounded-xl bg-slate-100 px-3 py-2 text-[12px] text-stone-600`
  - 蓝点 `h-1.5 w-1.5 animate-pulse rounded-full bg-blue-500` + 阶段文案（调用模型中 / 生成中·已产出 N 字 / 校验图结构中 / 第 N 轮校验未过修正重试中）
  - 重试小字块 `rounded-md bg-amber-50 px-2 py-1 text-[10.5px] leading-snug text-amber-700`「上轮问题：…」
- **空态**：`pt-6 text-center space-y-2` —— `Sparkles mx-auto h-6 w-6 text-blue-300` + `text-[12px] font-medium text-stone-600`「让 AI 帮你编排」+ `max-w-[260px] text-[11px] leading-relaxed text-stone-400` 引导文案
- **输入区** `border-t border-slate-200/80 p-3`，`flex items-end gap-2`：
  - Textarea `max-h-32 min-h-[3rem] flex-1 resize-none text-[12px]`（最小 48px、最大 128px）
  - 发送钮 `h-9 w-9 shrink-0 rounded-xl bg-blue-600 text-white shadow-sm hover:bg-blue-700 disabled:opacity-40` + `Send h-4 w-4`（36px 蓝圆角方钮）

## 核心代码

```tsx
// 气泡按角色三态
<div className={cn(
  'max-w-[85%] rounded-xl px-3 py-2 text-[12px] leading-relaxed whitespace-pre-wrap',
  m.role === 'user' ? 'bg-blue-600 text-white'
    : m.error ? 'bg-rose-50 text-rose-700 ring-1 ring-rose-200'
      : 'bg-slate-100 text-stone-700',
)}>

// 进度气泡阶段文案（SSE 事件投影）
{progress?.stage === 'validating' ? '校验图结构中…'
  : progress?.stage === 'retry' ? `第 ${progress.attempt} 轮校验未过，修正重试中…`
    : progress && progress.chars > 0 ? `生成中 · 已产出 ${progress.chars} 字`
      : '调用模型中…'}
```

## 适配指南

- 任何「画布 / 文档 + 右侧 AI 持续对话改稿」场景套用（Gamma / Dify AI workflow generator 套路）
- 进度气泡是关键质感：流式生成时不要只放 spinner，要把后端阶段事件（开始 / 生成字数 / 校验 / 重试）翻译成人话实时刷新
- 每轮 assistant 结果附 trace 链接是「可溯源」信号，新标签打开
- 面板宽度固定 `w-96`，与右侧 inspector 互斥共存（z 竞争 + 失焦错位露角）

## 反模式

- ❌ 进度只放转圈 spinner —— 丢掉「生成 N 字 / 第几轮重试」的过程反馈
- ❌ 气泡用满屏毛玻璃 / 渐变 —— 这里是克制的纯色气泡（蓝 / slate / rose）
- ❌ 发送钮做成文字按钮 —— 是 36px 蓝色圆角方钮 + Send 图标
- ❌ 错误气泡只改文字色不加 ring —— rose 气泡靠 `ring-1 ring-rose-200` 描边强调
