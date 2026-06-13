---
id: blocks/display/chameleon/kb-chunking-3pane-preview
type: block
name: 切块策略三栏实时预览
description: 左原文 textarea / 中 chunks 卡片列表(seq + 字数·token + 选中高亮) / 右 strategy 表单(mode 七按钮网格 + amber range 滑块 + 清洗开关) - 300ms 防抖即时预览不写库的 amber 调试面
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
- components/toggles/waveflow/emerald-switch
- tokens/palettes/waveflow/warm-paper-ink-blue
preview: /preview/blocks/display/chameleon/kb-chunking-3pane-preview
---

# 切块策略三栏实时预览

> `/kbs/:id/chunking-preview` 的三栏调试面：**左**原文 textarea（粘贴/默认示例）、**中** chunks 卡片列表（按 seq 渲染 + 字数·token + 选中高亮）、**右** strategy 表单（mode 七按钮网格 + amber range 滑块 + 文本清洗开关）。改动 300ms 防抖即时预览、**不写库**。amber 是这个调试面的强调色（区别于全站蓝主色）。waveflow 无 chunking，全新。

## 视觉特征

- **外壳**：`SectionCard !p-0`（去内边距，子区自管 padding）
- **header**：`flex items-center justify-between border-b border-stone-200/70 px-3 py-2`
  - 左：ghost「返回」(ChevronLeft h-3.5) + 标题 `text-[14px] font-medium text-stone-900「切块策略预览」` + 副标 `text-[11px] text-stone-500「KB「名」· 不写库；调试用」`
  - 右 `text-[11.5px] text-stone-500`：`N chunks`（数字 font-medium text-stone-700）+ `·` + `mode=xxx` + ghost「重跑」(RotateCw h-3，pending `animate-spin`)
- **三栏网格**：`grid h-[calc(100vh-180px)] min-h-[480px] grid-cols-[1fr_1.2fr_320px]`（左:中:右 = 1 : 1.2 : 320px 固定）
- **栏头**（统一）：`bg-warm-2/40 border-b border-stone-200/70 px-3 py-1.5 text-[10.5px] tracking-wider text-stone-500 uppercase`
- **左栏（原文）**：`flex flex-col border-r border-stone-200/70`，Textarea `min-h-0 flex-1 resize-none rounded-none border-0 font-mono text-[12px] leading-relaxed`
- **中栏（chunks）**：`bg-warm-2/20 flex flex-col border-r`，内容区 `flex-1 overflow-y-auto p-3 space-y-2`
  - ChunkCard：`w-full rounded-md border bg-white px-3 py-2 text-left transition`，选中 `border-amber-400 ring-2 ring-amber-100` / 未选 `border-stone-200 hover:border-stone-300 hover:bg-stone-50`
    - 头 `flex items-center justify-between text-[10px] tracking-wider text-stone-500 uppercase`：`#{seq}`（font-mono）+ `N 字 · ~M tok`（tnum font-mono）
    - 正文 `mt-1 text-[12px] break-words whitespace-pre-wrap text-stone-800`
- **右栏（策略）**：`bg-warm-2/40 flex flex-col`，内容 `space-y-3 overflow-y-auto p-3`
  - Field label：`mb-1 block text-[11.5px] text-stone-700`
  - **mode 七按钮**：`grid grid-cols-2 gap-1.5`，每个 `rounded-md border px-2 py-1.5 text-[11.5px] transition`，选中 `border-amber-400 bg-amber-50/60 text-amber-800` / 未选 `border-stone-200 bg-white text-stone-600 hover:border-stone-300`（固定字数/按段落/按句子/自定义正则/按 Token/父子分层/QA 问答）
  - **range 滑块**：`w-full accent-amber-600`，label 动态显当前值「chunk_size = N 字符」「overlap = N 字符」
  - 条件字段：regex→separator_regex Input `h-7 font-mono text-[11.5px]`；token→模型编码器 Input；parent_child→parent_size 滑块；qa→提示框 `rounded-md border border-amber-200 bg-amber-50/50 px-2.5 py-2 text-[10.5px]`
  - **CleanRow**（文本清洗）：`flex cursor-pointer items-center justify-between rounded-md border border-stone-200 bg-white px-2.5 py-1.5 text-[11.5px] text-stone-600` + 右侧 Switch
  - **底部提示**：`border-t border-stone-200 pt-2 text-[10.5px] text-stone-500` + `Sparkles h-3 w-3 text-amber-500`「修改即时预览（300ms 防抖）…」

## 核心代码

```tsx
// 切策略 / 文本变化 300ms 防抖自动跑预览（不写库）
useEffect(() => {
  const tid = setTimeout(() => { if (text.trim()) previewMut.mutate(); }, 300);
  return () => clearTimeout(tid);
}, [text, JSON.stringify(strategy)]);

// mode 七按钮：选中 amber，未选 stone hover
className={cn('rounded-md border px-2 py-1.5 text-[11.5px] transition',
  strategy.mode === m.value
    ? 'border-amber-400 bg-amber-50/60 text-amber-800'
    : 'border-stone-200 bg-white text-stone-600 hover:border-stone-300')}

// ChunkCard 选中环
selected ? 'border-amber-400 ring-2 ring-amber-100'
         : 'border-stone-200 hover:border-stone-300 hover:bg-stone-50'
```

## 适配指南

- amber 是 KB「调试 / 试探」场景的统一强调色（chunk-card-wall、hit-test 同源），不要换成全站蓝主色
- 预览态 mutate **绝不写库**，只调 `chunkingPreview()` 拿结果；保存策略要到「配置」tab
- 滑块 min/max/step 随 mode 切换（token 模式走 token 单位，其它走字符），label 实时显当前值
- range 用 `accent-amber-600` 直接染原生滑块，不自造 slider 组件

## 反模式

- ❌ 改一下就立即请求——必须 300ms 防抖，避免拖滑块时狂发
- ❌ 预览写库——这是调试面，改动只在 preview 内部 state
- ❌ mode 选中用蓝色——KB 调试域专用 amber 区分主域
- ❌ 三栏等宽——中栏（chunks 结果）最需要空间，用 `1fr_1.2fr_320px` 让结果区更宽、参数区固定窄
