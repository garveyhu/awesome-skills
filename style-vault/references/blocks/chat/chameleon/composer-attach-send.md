---
id: blocks/chat/chameleon/composer-attach-send
type: block
name: 多模态输入框 + 运行参数栏
description: Playground 圆角白卡输入框（无边内嵌 Textarea + 琥珀附件按钮 + 发送/停止切换）与右栏运行参数面板（模型/系统提示词/模板变量/数字调参/琥珀 KB chip/紫色生成态）
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
- components/inputs/waveflow/blue-focus-input
- tokens/palettes/waveflow/warm-paper-ink-blue
preview: /preview/blocks/chat/chameleon/composer-attach-send
---

# Chameleon Composer + Param Panel · 输入框 + 调参栏

> Playground 双件套：左侧底部「圆角白卡输入框」（`rounded-xl border-stone-200 bg-white p-2.5`，内嵌**完全无边**的两行 Textarea，底栏左附件按钮右发送/停止）+ 右栏「运行参数面板」（模型 Select / System Prompt / 模板变量填值 / Temperature·TopP·MaxTokens 数字行 / 琥珀色 KB chip / 绑生成应用时整面板切紫色提示条 + GenerationPanel）。

源码：`system/playground/components/composer.tsx` · `file-attach-button.tsx` · `param-panel.tsx` · `template-vars-panel.tsx`。

## 视觉特征

### 输入框卡（composer）

- **外卡** `rounded-xl(12) border border-stone-200(#e7e5e0) bg-white p-2.5(10) shadow-[0_1px_2px_rgba(0,0,0,.03)]`——比卡片默认 shadow 更轻
- **Textarea 完全消形**：`!border-0 !p-0 text-[12.5px] !shadow-none focus-visible:!ring-0`，`rows={2}`——视觉上「文字直接漂在卡里」，无第二层框
- **底栏** `mt-1.5(6) flex items-center gap-2(8)`，发送/停止用 `ml-auto` 推到最右
- **发送按钮** `Button size=sm`（蓝主色），内 `Send` icon `mr-1 h-3 w-3(12)` + 文字「发送」，`disabled={!input.trim() && attachments.length===0}`
- **停止按钮**（流式态切换）`Button variant=ghost size=sm`，内 `Square mr-1 h-3 w-3` + 「停止」
- **交互**：Enter 发送、Shift+Enter 换行、`nativeEvent.isComposing` 中文组词回车不拦截

### 附件按钮 + chip（file-attach-button）

- **按钮** `h-7 w-7(28) rounded-md(6) border border-stone-200/70 bg-white text-stone-500(#78716c)`；hover→`border-amber-300 bg-amber-50/40 text-amber-700(#b45309)`；disabled→`opacity-50 cursor-not-allowed`
- icon：闲时 `Paperclip h-3.5 w-3.5(14)`，上传中 `Loader2 h-3.5 w-3.5 animate-spin`
- 上传契约：`accept="image/*,audio/*,application/pdf" multiple`，三步走 presign→PUT→finalize，单文件 max 20MB
- **AttachmentChip** `rounded-md border border-stone-200/70 bg-stone-50/60 px-1.5 py-0.5 text-[11px]`；图缩略 `h-5 w-5(20) rounded object-cover`；文件名 `max-w-[80px] truncate text-stone-700`；移除 X `rounded p-0.5 text-stone-400 hover:bg-rose-100 hover:text-rose-600`，icon `h-3 w-3`

### 运行参数面板（param-panel）

- **容器** `space-y-3(12) text-[12.5px]`；每个 label `mb-1 block text-stone-600(#57534e)`
- **辅助提示文案** `mt-1 text-[10.5px] leading-tight text-stone-400`
- **生成应用模式提示条**（绑 comfyui 应用时显示）`rounded-md border border-violet-200 bg-violet-50 px-2.5 py-2 text-[11px] leading-snug text-violet-700`——整面板换成 GenerationPanel
- **模型 / KB Select 触发** `h-8`；KB 触发占位「已选 N 个」/「未关联」
- **NumberField** `flex items-center justify-between gap-2`，左 label `text-stone-600`，右 `Input type=number !h-7 !w-20 text-right text-[12px] tnum`；`allowEmpty` 时 value=0 渲染空 + placeholder `∞`
- **KB 已选 chip** `inline-flex items-center gap-1 rounded-full bg-amber-50 px-2 py-0.5 text-[10.5px] text-amber-700` + `×` 移除按钮，`mt-1 flex flex-wrap gap-1` 排布
- **模板变量行** `flex items-center gap-2`：变量名 chip `shrink-0 rounded bg-stone-100 px-1.5 py-0.5 font-mono text-[10.5px] text-stone-600`「{{name}}」+ `Input !h-7 flex-1 text-[12px]` placeholder「未填，将原样发送」

## 核心代码

```tsx
// composer.tsx —— 圆角白卡内无边 Textarea + 底栏切换
<div className="rounded-xl border border-stone-200 bg-white p-2.5 shadow-[0_1px_2px_rgba(0,0,0,.03)]">
  <Textarea
    rows={2}
    onKeyDown={e => {
      if (e.key === 'Enter' && !e.shiftKey && !e.nativeEvent.isComposing) {
        e.preventDefault(); void doSend();
      }
    }}
    className="!border-0 !p-0 text-[12.5px] !shadow-none focus-visible:!ring-0"
  />
  <div className="mt-1.5 flex items-center gap-2">
    <FileAttachButton ... />
    <div className="ml-auto">
      {streaming
        ? <Button size="sm" variant="ghost" onClick={onStop}><Square className="mr-1 h-3 w-3" />停止</Button>
        : <Button size="sm" onClick={doSend} disabled={!input.trim() && attachments.length === 0}><Send className="mr-1 h-3 w-3" />发送</Button>}
    </div>
  </div>
</div>
```

```tsx
// file-attach-button.tsx —— 琥珀 hover 附件按钮
<button className={cn(
  'inline-flex h-7 w-7 items-center justify-center rounded-md border border-stone-200/70 bg-white text-stone-500 transition',
  'hover:border-amber-300 hover:bg-amber-50/40 hover:text-amber-700',
  'disabled:cursor-not-allowed disabled:opacity-50',
)}>
  {uploading ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Paperclip className="h-3.5 w-3.5" />}
</button>
```

## 适配指南

- 输入框父级只给 `onSend(text, attachments)`——对比模式可一次广播多列，组件本身不绑列
- 附件 chip 受控：父级持 `attachments[]`，按钮回调 `onAttached/onRemove` 增删
- 参数面板按应用 `source` 分流：`comfyui`→生成面板 + 紫提示条 / `local`→运行真实应用（模型 KB 仅信息展示）/ 普通→预填模型·提示词·KB
- 琥珀色（amber）是本块的「附件/知识」语义专用色，蓝（blue-600）留给发送主操作，紫（violet）留给生成态——三色各司其职，别混

## 反模式

- ❌ 给 Textarea 加 border / shadow / ring——它必须完全消形融进白卡，否则出现「框中框」
- ❌ 附件按钮用蓝色 hover——琥珀是附件专属语义，蓝是发送主操作
- ❌ MaxTokens 不给 `∞` 占位——用户分不清 0 是「无限」还是「禁用」
- ❌ KB chip 用方角 rounded-md——已选 KB 用 `rounded-full` pill 形与模板变量方角 chip 区分语义
