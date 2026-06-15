---
id: blocks/feedback/waveflow/danger-confirm-modal
type: block
name: Danger 确认弹窗
description: title 内嵌 28x28 red-50 圆 + AlertTriangle red-600 icon + 命令式 useConfirm() await 返 bool
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [serious]
  stack: [shadcn-radix]
uses:
  - blocks/form/waveflow/dialog-vertical-form
  - components/buttons/waveflow/cva-engineer-button
preview: /preview/blocks/feedback/waveflow/danger-confirm-modal
---

# Waveflow Danger Confirm Modal

> 替代浏览器原生 `window.confirm` 的视觉版——基于 Dialog，**Title 内嵌一个 28×28 red-50 圆 + AlertTriangle red-600 icon**（danger 模式时显示），Body 描述富文本，Footer ghost 取消 + danger 实心红"删除/确定"。配套 `useConfirm()` hook 提供命令式 `const ok = await confirm({ title, description, danger: true, confirmText: '删除' })`。

## 视觉特征

- **Dialog max-w-md**：标准短确认
- **DialogTitle 行内 icon 容器**（仅 danger 模式）：
  ```tsx
  <span className="flex h-7 w-7 items-center justify-center rounded-full bg-red-50">
    <AlertTriangle className="h-4 w-4 text-red-600" />
  </span>
  ```
  + title 文本：`flex items-center gap-2`
- **DialogBody**：
  - 文本：`text-[13px] text-stone-600`（一行简短描述）
  - 富文本：传 `<>...</>` jsx，可含 `<span className="font-medium text-stone-900">{name}</span>` 高亮 + `<br />` + `<span className="text-stone-500">（补充说明）</span>`
- **DialogFooter**：
  - 左：`<Button variant="ghost">取消</Button>`
  - 右：`<Button variant={danger ? 'danger' : 'primary'}>{confirmText}</Button>`

## 核心代码

```tsx
// useConfirm hook
const { confirm, dialog } = useConfirm();

// 命令式调用
const ok = await confirm({
  title: '确认删除',
  description: <>将删除任务 <span className="font-medium text-stone-900">「{name}」</span>，此操作不可恢复，确认继续？</>,
  confirmText: '删除',
  danger: true,
});
if (!ok) return;
// 真正执行删除
```

## 适配指南

- 命令式 hook：在组件顶部 `const { confirm, dialog: confirmDialog } = useConfirm()` + 末尾 render `{confirmDialog}`，事件回调里 `await confirm(...)` 拿 bool
- danger 用红圆 icon + danger 红按钮；非 danger（如警告但可继续）用 primary 蓝按钮、省略 icon
- description 富文本里高亮 entity 名："将删除任务 「**XX**」" 让用户看清要删的是什么

## 反模式

- ❌ 用浏览器 `window.confirm`——不可定制 / 不响应主题
- ❌ danger 按钮放左 / 取消放右 —— 反人类（confirmtext 始终右）
- ❌ icon 过大（> 32px）—— 抢主标题字
- ❌ 没 description 直接 yes/no—— 用户不知道按"删除"会发生啥
