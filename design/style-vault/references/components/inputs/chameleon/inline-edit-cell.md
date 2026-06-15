---
id: components/inputs/chameleon/inline-edit-cell
type: component
name: 表格内联编辑单元
description: 表格内 hover 露铅笔 / 双击进编辑——蓝边输入 + 勾叉确认 + saving spinner，Enter 提交 Escape 取消
platforms:
- web
theme: light
tags:
  aesthetic:
  - industrial
  - minimal
  mood:
  - serious
  stack:
  - shadcn-radix
uses:
- components/inputs/waveflow/blue-focus-input
- tokens/palettes/waveflow/warm-paper-ink-blue
preview: /preview/components/inputs/chameleon/inline-edit-cell
---

# 表格内联编辑单元

> Chameleon 表格单元的就地编辑控件——平时只是一段文字，hover 时尾部淡入一支铅笔，双击进入编辑态：蓝边小输入框 + 绿勾 / 灰叉确认取消，保存中转 spinner。`onSave` 返回 promise，throw 时 toast 回滚。readonly 与「值未变更」短路。waveflow 表格无内联编辑能力，故 new。

## 视觉特征

### 显示态
- 容器 `span group/inline inline-flex items-center gap-1 cursor-pointer`，双击进编辑（`title="双击编辑"`）
- 空值占位 `<span className="text-stone-400">—</span>`
- 铅笔按钮 `rounded p-0.5 opacity-0 group-hover/inline:opacity-100 hover:bg-stone-100`，内 `Pencil h-3 w-3 text-stone-400`（hover 行时整支铅笔淡入）

### 编辑态
- 容器 `span inline-flex items-center gap-1`
- 输入框 `h-6 w-full max-w-[140px] rounded border border-blue-300 bg-white px-1.5 text-[12px] outline-none ring-2 ring-blue-100`（注意是 `rounded`=4px + `border-blue-300` + 常驻 `ring-2 ring-blue-100`，非 input.tsx 的 focus-only ring）
- saving 时只显 `Loader2 h-3 w-3 animate-spin text-stone-400`，否则显勾叉两个按钮：
  - 确认 `rounded p-0.5 text-emerald-600 hover:bg-emerald-50`，内 `Check h-3 w-3`
  - 取消 `rounded p-0.5 text-stone-400 hover:bg-stone-100`，内 `X h-3 w-3`
- 键盘：Enter 提交，Escape 退出

## 核心代码

```tsx
// 编辑态
<span className="inline-flex items-center gap-1">
  <input
    type={type}
    onKeyDown={e => { if (e.key === 'Enter') submit(); if (e.key === 'Escape') exitEdit(); }}
    className="h-6 w-full max-w-[140px] rounded border border-blue-300 bg-white px-1.5 text-[12px] outline-none ring-2 ring-blue-100"
  />
  {saving ? (
    <Loader2 className="h-3 w-3 animate-spin text-stone-400" />
  ) : (
    <>
      <button className="rounded p-0.5 text-emerald-600 hover:bg-emerald-50"><Check className="h-3 w-3" /></button>
      <button className="rounded p-0.5 text-stone-400 hover:bg-stone-100"><X className="h-3 w-3" /></button>
    </>
  )}
</span>

// 显示态
<span className="group/inline inline-flex items-center gap-1 cursor-pointer" onDoubleClick={...}>
  <span>{value ?? <span className="text-stone-400">—</span>}</span>
  <button className="rounded p-0.5 opacity-0 transition group-hover/inline:opacity-100 hover:bg-stone-100">
    <Pencil className="h-3 w-3 text-stone-400" />
  </button>
</span>
```

## 适配指南
- `onSave` 必须返 promise；throw 时上层 toast `e.message`，组件自动留在编辑态（不清 draft）
- number 类型解析 `Number(draft)`，NaN → toast「请输入数字」不提交
- 「值未变更」短路：`String(parsed) === String(value)` 直接退出，不发请求
- 编辑框 max-w-[140px] 防窜行宽；放表格紧凑单元里刚好

## 反模式
- ❌ 编辑框用 input.tsx 的 h-8 + focus-only ring —— 这里是 h-6 + 常驻 ring-2 ring-blue-100（编辑态本就该高亮，不等 focus）
- ❌ 铅笔常显 —— 必须 `opacity-0 group-hover:opacity-100`，否则每行尾巴一支铅笔太吵
- ❌ saving 时还显勾叉 —— 只显 spinner，避免重复提交
- ❌ 确认用蓝色 —— 确认是 emerald-600 绿，取消是 stone-400 灰，语义分色
