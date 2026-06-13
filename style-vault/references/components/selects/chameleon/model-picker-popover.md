---
id: components/selects/chameleon/model-picker-popover
type: component
name: 模型选择器双件
description: provider 类别栏双栏 popover（chat 模型，Cpu 图标 + mono code + provider 副行）+ 紧凑内联生图模型 Select
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
preview: /preview/components/selects/chameleon/model-picker-popover
---

# 模型选择器双件

> Chameleon 选模型的两件套：A·`ModelPicker` 照抄 agent-picker 交互的 chat 模型双栏 popover（左侧 provider 类别栏从数据派生去重，右侧搜索 + 列表，行带 `Cpu` 图标 + mono model code + provider 灰 mono 副行 + 选中 `Check`，一次性返列表前端过滤，非无限滚动）；B·`ImageModelSelect` 选一个 image 模型的紧凑内联 Radix Select（值=model.id 字符串避雪花丢精度，选项 mono code + 灰 provider 副标，空态引导去模型页加 image 模型）。

## 视觉特征

### A·ModelPicker 双栏 popover
- 结构与 agent-picker 一致：触发 `h-7 rounded-md border border-stone-200 bg-white px-2 text-[12px] text-stone-700 hover:border-stone-300`（value='' 时 `text-stone-400`）+ `ChevronDown h-3.5 w-3.5 text-stone-400`，width 默认 168
- `PopoverContent !w-[420px] !p-0`，内 `flex h-[340px]`
- 左 provider 栏 `w-24 shrink-0 space-y-0.5 border-r border-stone-100 p-1.5`，含「全部」+ 派生 providers，active `bg-blue-50 font-medium text-blue-700`，idle `text-stone-600 hover:bg-stone-100`（provider 项加 `truncate`）
- 右搜索 `Search h-3.5 w-3.5 absolute left-3.5 text-stone-400` + Input `!h-7 pl-7 text-[12px]`
- Row `flex w-full items-center gap-2 rounded px-2 py-1.5 hover:bg-stone-100`，active `bg-blue-50`
  - 图标 `Cpu h-3.5 w-3.5 text-stone-400`（固定，非 img）
  - 标题（model code）`block truncate text-[12px] text-stone-800`
  - provider 副行 `block truncate font-mono text-[10px] text-stone-400`
  - active `Check h-3.5 w-3.5 text-blue-600`
- 「不指定（用默认模型）」可配空值行；空态 `py-6 text-center text-[12px] text-stone-400`「无匹配模型」
- 值为 **model_code**（非 id）

### B·ImageModelSelect 内联 Select
- `SelectTrigger` 覆写 `h-7 text-[12px]`，placeholder 加载中→「加载中…」否则「选择生图模型」
- `SelectItem text-[12px]`：`<span className="font-mono">{code}</span>` + provider `<span className="ml-1.5 text-[10px] text-stone-400">`
- 空态 `px-2 py-1.5 text-[11px] text-stone-400`「暂无生图模型，请先在「模型」页添加 image 模型」
- 值为 **model.id 字符串**（避免雪花 id 过 Number 丢精度）

## 核心代码

```tsx
// A·ModelPicker Row（Cpu 图标 + code + provider 副行）
<button className={cn('flex w-full items-center gap-2 rounded px-2 py-1.5 hover:bg-stone-100', active && 'bg-blue-50')}>
  <span className="shrink-0"><Cpu className="h-3.5 w-3.5 text-stone-400" /></span>
  <span className="min-w-0 flex-1">
    <span className="block truncate text-[12px] text-stone-800">{m.code}</span>
    {sub && <span className="block truncate font-mono text-[10px] text-stone-400">{sub}</span>}
  </span>
  {active && <Check className="h-3.5 w-3.5 shrink-0 text-blue-600" />}
</button>

// B·ImageModelSelect 选项
<SelectItem value={String(m.id)} className="text-[12px]">
  <span className="font-mono">{m.code}</span>
  {m.provider_code && <span className="ml-1.5 text-[10px] text-stone-400">{m.provider_code}</span>}
</SelectItem>
```

## 适配指南
- chat 模型筛选（多选 / 列表大）走 ModelPicker 双栏 popover；单选绑定一个 image 模型走 ImageModelSelect 内联 Select
- ModelPicker 的 provider 栏从 `models` 按 `provider_code` 去重派生，无需写死类别表
- ImageModelSelect 值类型必须是 **string**（`String(m.id)`），雪花 id 走 Number 会丢精度
- 空态文案带「去模型页添加」引导，不要只显空白

## 反模式
- ❌ ModelPicker 行图标用 Bot —— chat 模型用 `Cpu`（区别于 agent-picker 的 Bot/img）
- ❌ ImageModelSelect 值传 number —— 雪花 id 必须字符串
- ❌ model code 不用 mono —— code 是 `font-mono`，provider 副标也是 mono，名称才是常规对比层级
- ❌ ImageModelSelect 用 `h-8` 默认 Trigger —— 这里覆写 `h-7 text-[12px]` 紧凑款，配画布节点 / 创建表单的密度
