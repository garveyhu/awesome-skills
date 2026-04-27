---
id: blocks/nav/sage/sidebar-session-row
type: block
name: 侧栏会话行
description: 单条会话项 + 选中态 + group hover MoreHorizontal 按钮 + 三气泡操作菜单
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/sage/twelve-theme-spectrum
  - tokens/palettes/sage/neutral-rgb-ladder
  - components/buttons/sage/icon-circle-ghost
preview: /preview/blocks/nav/sage/sidebar-session-row
---

# Sidebar Session Row

> 侧栏会话列表里的单条——选中态用 `bg-[rgb(239,239,239)] ${themeClasses.text}` 双层（背景 + 主题色文字）；hover 时右侧浮出 `MoreHorizontal` 按钮，再点出 rename / duplicate / delete 三按钮气泡。还支持双击进入 inline 编辑标题。

## 视觉特征

- 容器：`group w-full text-left px-3 py-1.5 flex items-center gap-3 transition-all cursor-pointer relative mb-0.5 rounded-lg border-none`
- 选中：`bg-[rgb(239,239,239)] ${themeClasses.text} hover:bg-[rgb(231,231,231)]`
- 未选：`hover:bg-[rgb(231,231,231)] text-slate-600 hover:text-slate-900`
- 标题：`truncate text-sm flex-1 font-medium`，超过 20 字符 hover 显 Tooltip
- 操作按钮：`opacity-0 group-hover:opacity-100 + p-1 rounded-md text-slate-400 hover:text-slate-600 hover:bg-slate-200/50`
- 操作打开后：`bg-slate-200 text-slate-800` 高亮自身
- 气泡菜单：`absolute right-0 top-full mt-1 w-32 bg-white border border-slate-200 rounded-lg shadow-lg py-1 z-20 + animate-in fade-in zoom-in-95 duration-100`
- 菜单按钮：`w-full text-left px-3 py-2 text-sm text-slate-600 hover:bg-slate-50 ${themeClasses.textHover} flex items-center gap-2` + lucide icon size 14
- 删除按钮特殊：`hover:bg-red-50 hover:text-red-600`
- inline 编辑：`bg-white text-slate-800 text-sm px-1 py-0.5 rounded w-full outline-none border ${themeClasses.borderFocus}` + Enter 提交 / Esc 取消

## 核心代码

```tsx
<div
  className={`group w-full text-left px-3 py-1.5 flex items-center gap-3 transition-all cursor-pointer relative mb-0.5 rounded-lg border-none ${
    sessionId === s.id
      ? `bg-[rgb(239,239,239)] ${tc.text} hover:bg-[rgb(231,231,231)]`
      : 'hover:bg-[rgb(231,231,231)] text-slate-600 hover:text-slate-900'
  }`}
  onClick={() => navigate(`/chat/${s.id}`)}
>
  {editingId === s.id ? (
    <input
      autoFocus
      value={editTitle}
      className={`bg-white text-slate-800 text-sm px-1 py-0.5 rounded w-full outline-none border ${tc.borderFocus}`}
      onKeyDown={e => { if (e.key === 'Enter') save(); if (e.key === 'Escape') cancel(); }}
    />
  ) : (
    <>
      <Tooltip title={s.title.length > 20 ? s.title : ''} placement="right" mouseEnterDelay={0.5}>
        <span className="truncate text-sm flex-1 font-medium">{s.title || 'Untitled'}</span>
      </Tooltip>
      <div className="relative">
        <button
          className={`p-1 rounded-md transition-colors ${
            menuOpen
              ? 'bg-slate-200 text-slate-800'
              : 'text-slate-400 hover:text-slate-600 hover:bg-slate-200/50 opacity-0 group-hover:opacity-100'
          }`}
          onClick={e => { e.stopPropagation(); toggleMenu(); }}
        >
          <MoreHorizontal size={16} />
        </button>
        {menuOpen && (
          <div className="absolute right-0 top-full mt-1 w-32 bg-white border border-slate-200 rounded-lg shadow-lg py-1 z-20 animate-in fade-in zoom-in-95 duration-100">
            <MenuButton icon={<Edit2 size={14} />} label="重命名" onClick={startEdit} />
            <MenuButton icon={<Copy size={14} />} label="复制对话" onClick={duplicate} />
            <MenuButton icon={<Trash2 size={14} />} label="删除" danger onClick={confirmDelete} />
          </div>
        )}
      </div>
    </>
  )}
</div>
```

## 适配指南

- 父级 sessions 列表：`flex-1 overflow-y-auto no-scrollbar group/sessions relative` —— 用 `group/sessions` 标记可让顶部"管理"按钮 hover 显
- inline 编辑要 `e.stopPropagation()` 阻止点击穿透到 onClick navigate
- 删除前必弹 `<DeleteConfirmModal>`（block: `feedback/sage/delete-confirm-modal`），不直接执行

## 反模式

- ❌ 选中态加 border —— 视觉过重
- ❌ 操作按钮平时显示（不用 group-hover）—— 列表会变得拥挤
