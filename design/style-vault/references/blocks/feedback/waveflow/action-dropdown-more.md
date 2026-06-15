---
id: blocks/feedback/waveflow/action-dropdown-more
type: block
name: 表格行 MoreHorizontal 操作菜单
description: 行内 MoreHorizontal trigger 按钮 + Radix DropdownMenu 内容（编辑 / 列表跳转 / 终止 / Separator / 危险删除）+ danger 项 red 文
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [serious]
  stack: [shadcn-radix]
uses: []
preview: /preview/blocks/feedback/waveflow/action-dropdown-more
---

# Waveflow Action Dropdown More

> 表格行内"更多操作"下拉——`<button className="rounded p-1 hover:bg-stone-200"><MoreHorizontal className="h-3.5 w-3.5 text-stone-500" /></button>` 作为 trigger，点开后 Radix DropdownMenu 内容（paper bg + pop shadow + rounded-lg）：N 个常规 item + Separator + danger items（red 文 + 红 hover 底）。

## 视觉特征

- **Trigger 按钮**：`rounded p-1 hover:bg-stone-200` —— 和左侧 inline action button 同款
- **DropdownMenuContent**：`min-w-[8rem] rounded-lg border-stone-200/60 bg-[var(--color-paper)] shadow-[var(--shadow-pop)] p-1`
- **DropdownMenuItem**：
  - 基础：`flex items-center gap-2 rounded px-2 py-1.5 text-[12.5px] text-stone-700 cursor-pointer outline-none focus:bg-stone-100`
  - icon: lucide 12px (`h-3 w-3`) text-stone-500
  - `danger` prop: text-red-600 + `focus:bg-red-50` + icon text-red-500
- **DropdownMenuSeparator**: `my-1 h-px bg-stone-100`
- **align="end"**：在表格右侧操作列里用 end，让 menu 出在 trigger 左下方
- **常规打开行为**：先非危险（编辑 / 查看 / 跳转），Separator 后才是危险（终止 / 删除 / 移除）

## 关键代码

```tsx
<DropdownMenu>
  <DropdownMenuTrigger asChild>
    <button className="rounded p-1 hover:bg-stone-200">
      <MoreHorizontal className="h-3.5 w-3.5 text-stone-500" />
    </button>
  </DropdownMenuTrigger>
  <DropdownMenuContent align="end">
    <DropdownMenuItem onClick={onEdit}>
      <Pencil className="h-3 w-3 text-stone-500" /> 编辑任务
    </DropdownMenuItem>
    <DropdownMenuItem onClick={onOpenLogList}>
      <List className="h-3 w-3 text-stone-500" /> 日志列表
    </DropdownMenuItem>
    {isRunning && (
      <DropdownMenuItem danger onClick={onKill}>
        <Square className="h-3 w-3" /> 终止任务
      </DropdownMenuItem>
    )}
    <DropdownMenuSeparator />
    <DropdownMenuItem danger onClick={onDelete}>
      <Trash2 className="h-3 w-3" /> 删除任务
    </DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>
```

## 适配指南

- 表格列宽 `width: 96` 通常装得下"触发一次 / 查看日志 / 更多" 3 个 icon button
- 条件 menu item：动态根据行状态显示（`rs === 'running' && <DropdownMenuItem danger>终止</>`）
- 危险操作前必跑 `useConfirm()` await
- "查看日志" 类跳转：用 `window.open(href, '_blank')` 新窗口

## 反模式

- ❌ 不用 Separator 直接堆所有项 —— 用户区分不出"安全 vs 危险"
- ❌ trigger 按钮太大（h-7+）—— 和左侧 icon button 不齐
- ❌ danger 项不变色—— "删除"和"编辑"视觉等价，容易误点
