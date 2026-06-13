---
id: blocks/chat/chameleon/hitl-human-input-prompt
type: block
name: 人工输入回填卡（HITL）
description: durable agent ctx.ask_human 暂停 run 时挂在 assistant 气泡下方的琥珀色回填卡：prompt + Textarea + 「提交并续跑」按钮，Cmd/Ctrl+Enter 提交
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
preview: /preview/blocks/chat/chameleon/hitl-human-input-prompt
---

# Chameleon HITL Human Input Prompt · 人工输入回填卡

> 当 durable agent 经 `ctx.ask_human` 暂停 run 时，在该条 assistant 气泡下方渲染的**琥珀色回填卡**：标题「等待人工输入」+ prompt 文案 + 两行 Textarea + 右下「提交并续跑」按钮。Cmd/Ctrl+Enter 提交，回填后续跑暂停的 run。气泡本体在 `paused` 态显示「等待人工输入…」占位。Chameleon 独有（durable agent HITL），waveflow 无人机协作。

源码：`system/playground/components/message-thread.tsx:383-419`（`HumanInputPending`）+ `:234-238`（气泡 paused 占位）。

## 视觉特征

- **卡片** `mt-1.5(6) w-full max-w-[420px] rounded-xl(12) border border-amber-200(#fde68a) bg-amber-50/60 p-3(12)`——挂在气泡下方，琥珀边 + 半透明琥珀底
- **标题行** `mb-2(8) flex items-center gap-1.5(6) text-[12px] font-medium text-amber-700(#b45309)`「⏸ 等待人工输入」（preview 用 `Pause` lucide icon 替 ⏸ emoji）
- **prompt** `mb-2 whitespace-pre-wrap break-words text-[13px] text-stone-700(#44403c)`——展示 `ctx.ask_human` 问句
- **Textarea** `rows={2} mb-2 text-[13px]`，placeholder「填写答案后提交，续跑该智能体…」
- **底部** `flex justify-end`，`Button size=sm disabled={!val.trim()}`「提交并续跑」（蓝主色）
- **气泡内 paused 占位** `text-amber-600(#d97706)`「⏸ 等待人工输入…」——在 prompt 卡之上、气泡本体里显示
- **交互**：`onKeyDown` 中 `Enter && (metaKey || ctrlKey)` 才提交（区别于普通输入框 Enter 直发）

## 核心代码

```tsx
const HumanInputPending = ({ prompt, onSubmit }: { prompt: string; onSubmit: (answer: string) => void }) => {
  const [val, setVal] = useState('');
  const submit = () => { const a = val.trim(); if (a) onSubmit(a); };
  return (
    <div className="mt-1.5 w-full max-w-[420px] rounded-xl border border-amber-200 bg-amber-50/60 p-3">
      <div className="mb-2 flex items-center gap-1.5 text-[12px] font-medium text-amber-700">
        ⏸ 等待人工输入
      </div>
      <div className="mb-2 whitespace-pre-wrap break-words text-[13px] text-stone-700">{prompt}</div>
      <Textarea value={val} onChange={e => setVal(e.target.value)}
        placeholder="填写答案后提交，续跑该智能体…" rows={2} className="mb-2 text-[13px]"
        onKeyDown={e => { if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) submit(); }} />
      <div className="flex justify-end">
        <Button size="sm" disabled={!val.trim()} onClick={submit}>提交并续跑</Button>
      </div>
    </div>
  );
};
```

## 适配指南

- 仅在 `!isUser && msg.status === 'paused' && msg.pending` 时渲染——挂在该条 assistant 气泡的 `items-start` 列里
- 琥珀色（amber-200/50/600/700）是「等待人工」的语义专色：暂停态用它统一标记（气泡占位 + 回填卡 + footer 一致）
- `max-w-[420px]` 限宽，比气泡 88% 更可控，避免回填框过宽
- Cmd/Ctrl+Enter 提交而非裸 Enter——多行答案场景下避免误发

## 反模式

- ❌ 用蓝色/红色做暂停卡——暂停是「等待 + 提醒」语义，琥珀（amber）专用，蓝留给主操作、红留给失败
- ❌ 回填卡塞进气泡内部——它是气泡的兄弟节点（气泡下方独立卡），结构上不嵌套
- ❌ Textarea 裸 Enter 提交——多行人工答案需 Cmd/Ctrl+Enter
- ❌ 按钮在空答案时仍可点——必须 `disabled={!val.trim()}`
