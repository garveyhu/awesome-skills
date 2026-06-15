---
id: pages/dashboard/sage/agent-chat-stream
type: page
name: 智能体问答主页
description: ChatPage 主舞台——header (model select + title + more) + 消息流 + ChatInput + QuestionNavSidebar
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - blocks/nav/sage/themed-sidebar-shell
  - blocks/form/sage/chat-composer
  - blocks/feedback/sage/delete-confirm-modal
  - blocks/feedback/sage/spin-fullscreen-loader
  - components/avatars-icons/sage/themed-circle-avatar
preview: /preview/pages/dashboard/sage/agent-chat-stream
---

# Agent Chat Stream

> sage 主路由 `/chat` + `/chat/:sessionId` 的整页布局。MainLayout 已注入侧栏，ChatPage 自己包裹一层 `flex-1 flex flex-col h-full p-1 + 内容白盒 rounded-2xl border-t border-x border-slate-100/50`。三段：header / 消息流 / ChatInput；右侧浮动 QuestionNavSidebar。

## 页面骨架

1. **外层** `flex-1 flex flex-col h-full w-full relative p-1`
2. **内层白盒** `flex-1 flex flex-col h-full w-full bg-white rounded-2xl border-t border-x border-slate-100/50 overflow-hidden relative`
3. **Header** `bg-white border-b border-slate-200/50 h-14 flex items-center justify-between px-3 md:px-6 flex-shrink-0`：
   - **左**：折叠侧栏时的 logo/PanelLeftOpen 双图标按钮 + Antd Select（model 切换，`variant="borderless" font-semibold`，注入 `sage-dropdown-scroll sage-select-dropdown` 类）
   - **中（绝对定位）**：`absolute left-1/2 -translate-x-1/2 font-medium text-slate-800` 显示 sessionTitle 或 "新对话"
   - **右**：AgentHeaderActionSlot（agent 自定义注入区）+ 当 sessionId 时显 MoreVertical 圆形 ghost button + 下拉菜单 `mt-1 w-45 bg-white border border-slate-200 rounded-lg shadow-lg py-1 z-20 + animate-in fade-in zoom-in-95 duration-100`
4. **消息流** `flex-1 overflow-y-scroll py-4 md:py-8 space-y-6 bg-white relative` + `style={{ scrollbarGutter: 'stable both-edges' }}`
   - 空态：`absolute inset-0 flex flex-col items-center justify-center text-slate-400 pointer-events-none` + logo 16×16 + `text-lg font-medium text-slate-500` + 副标题
   - 消息：`<ChatMessage>` （AI 头像 + 气泡 + thinking process + actions）
   - 末尾 `<QuestionNavSidebar>` 右侧 sticky 浮标——点击跳到对应用户提问
5. **ChatInput** 见 `blocks/form/sage/chat-composer`
6. **删除确认 Modal** 见 `blocks/feedback/sage/delete-confirm-modal`
7. **AgentSelectorModal**（条件渲染）/ **isSessionLoading overlay**：`absolute inset-0 bg-white flex items-center justify-center z-50 + Loading large`

## 视觉要点

1. **内层白盒只有 border-t / border-x，无 border-b**：让 ChatInput 区"挂"在底部，融入背景
2. **scrollbarGutter: 'stable both-edges'** —— 消息流即使无内容也保留滚动条空间，避免内容跳动
3. **QuestionNavSidebar 是 sage 专属**：长对话时右侧浮一列圆点，点击跳到对应消息（cf framer-motion `whileHover: y:-4`）
4. **Header model select 用 `variant="borderless"`** —— 像普通文字，靠 popup 才暗示这是切换器
5. **消息间距 `space-y-6`**（24px）—— sage 选用比 chat 4-5（16px）大一档的呼吸感
6. **AI 头像在桌面绝对定位** `md:absolute md:-left-12 md:mt-1` —— 让消息体居中，头像浮在左侧外侧

## 状态机

- `isSessionLoading: true` → 全屏 `<Loading />` 盖在内层白盒上
- `isLoading: true`（流式响应中）→ ChatInput 切到 stop 按钮 + textarea opacity-60
- `displayedMessages.length === 0 && !isSessionLoading` → 显空态（logo + 标题）

## 反模式

- ❌ 把侧栏放在 ChatPage 内 —— 侧栏由 MainLayout 提供
- ❌ 给消息流加 background —— 必须保持白色
- ❌ 隐藏 scrollbarGutter —— 流式追加内容时会跳动
