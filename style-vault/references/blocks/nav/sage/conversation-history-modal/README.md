---
id: blocks/nav/sage/conversation-history-modal
type: block
name: 历史对话弹窗
description: 680px 居中 Modal · h-[70vh] 浅 mask + backdrop blur · 时间分组（今天/昨天/近 7 天/近 30 天/去年/更早）+ 批量管理 + inline 重命名 + 滚动加载
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm]
  stack: [react-antd-tailwind]
preview: /preview/blocks/nav/sage/conversation-history-modal
---

# Conversation History Modal

> sage 历史对话浏览。Modal 居中 + 浅紫黑 backdrop。顶部 header（标题+计数+管理/关闭）+ 搜索 + 时间分组列表（懒加载）+ 双确认弹窗（单条 / 批量删除）。inline 重命名带 Esc/Enter 键盘控制。

## Modal 容器

```jsx
<Modal
  open={open} onCancel={onClose}
  footer={null} centered closable={false}
  width={680}
  className="conversation-manager-modal"
  styles={{
    body: { padding: 0 },
    mask: { background: 'rgba(15, 23, 42, 0.3)', backdropFilter: 'blur(2px)' },
  }}
>
  <div className="flex flex-col h-[70vh] bg-white rounded-2xl overflow-hidden">
```

## Header

`flex items-center justify-between px-6 py-4 border-b border-neutral-100`

- **左**：`flex items-center gap-3`
  - Title `text-lg font-semibold text-neutral-800` "对话历史"
  - 计数 `text-sm text-neutral-400` "(共 N 条)"
- **右**：分两态
  - 普通：管理按钮 `px-3 py-1.5 text-sm ${themeClasses.text} rounded-lg` "批量管理" + `<X />` 关闭
  - 批量态：`text-red-600 hover:bg-red-50` "全选 / 删除({count}) / 取消"

## 搜索

`px-6 py-3 border-b border-neutral-100`：`<Input prefix={<Search size={14} />} allowClear className="rounded-lg" />`

## 列表

容器：`flex-1 overflow-y-auto px-4 py-2`，ref={scrollContainerRef}，onScroll 触发底部 100px 时 loadMore

### 时间分组
每个分组 `mb-4`：
- 标题（sticky）：`px-2 py-1.5 text-xs font-medium text-neutral-400 uppercase tracking-wider sticky top-0 bg-white z-10`
- 列表 `space-y-1`

### 单行 session
`group flex items-center gap-3 px-3 py-2.5 rounded-xl cursor-pointer transition-all`
- 当前选中：`bg-neutral-100 ${themeClasses.text}`
- 批量勾选：`bg-neutral-100`
- hover：`hover:bg-neutral-50`

行内：
- `<Checkbox>`（仅批量态）
- `<MessageSquare size={16} className="text-neutral-400 flex-shrink-0" />`
- 标题区 `flex-1 min-w-0`：
  - 标题 `text-sm text-neutral-700 truncate font-medium`
  - 时间 `text-xs text-neutral-400 mt-0.5`（formatDate）
- 操作按钮 `flex items-center gap-1 opacity-0 group-hover:opacity-100`
  - `<Edit2 />` 重命名 + `<Trash2 />` 删除

### inline 重命名
切换为：`flex-1 flex items-center gap-2`（onClick stopPropagation）
- `<Input size="small" autoFocus maxLength={INPUT_LIMITS.CONVERSATION_TITLE} />`
- `<Check />` 确认（`p-1 ${themeClasses.text} hover:bg-neutral-100`）
- `<X />` 取消（`p-1 text-neutral-400 hover:bg-neutral-100`）
- 键盘：Esc 取消 / Enter 确认

### 加载状态
- loading：`flex justify-center py-4` + `<Spin size="small" />`
- 全部加载完：`text-center py-4 text-sm text-neutral-400` "已加载全部"

### 空态
`<Empty image={Empty.PRESENTED_IMAGE_SIMPLE} className="mt-12" />`

## 删除确认弹窗

两个独立 Modal：
- 单条：`<Modal width={360} title="确认删除" okType="danger" />`
- 批量：同上但 title 含数量

## 视觉要点

1. **mask 0.30 alpha + backdrop-blur(2px)**：温柔的玻璃模糊，不像传统 modal 那种黑屏 50% alpha 死板
2. **rounded-2xl（16px）**：比常规 modal 圆角大一档，配合 70vh 高度营造"半屏卡片"感
3. **时间分组 sticky**：滚动时分组标题钉在顶部，方便用户在长对话历史里定位时间段
4. **opacity-0 group-hover:opacity-100**：操作按钮默认隐藏，hover 整行才显 —— 列表保持视觉简洁
5. **inline 重命名替换原行**：不弹新窗、不抖动 —— 同一位置 Input 替换 div

## 反模式

- ❌ 不要把单条删除做成 Popconfirm —— 与批量删除走两个流程，统一用 Modal 更清晰
- ❌ 不要把搜索框塞到 header 同行 —— sage 故意拆成两行：header（标题/动作）+ search（独立行）

## 使用上游
- `system/chat/pages/ChatPage` （sidebar 顶部"全部对话"按钮触发）
