---
id: blocks/nav/sage/themed-sidebar-shell
type: block
name: 主题色侧栏壳体
description: sage 整站主侧栏整体——logo + space switcher + 入口按钮 + 会话列表 + 用户菜单
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
  - components/avatars-icons/sage/themed-circle-avatar
preview: /preview/blocks/nav/sage/themed-sidebar-shell
---

# Themed Sidebar Shell

> 264px 宽（`w-64`） · `bg-[rgb(249,249,249)]` 底 · 自上而下分 7 段：
> ① logo + 折叠按钮  ② 空间切换器  ③ "新对话"按钮  ④ "我的收藏"  ⑤（管理员）"Agent Store"  ⑥ 会话列表（标题 caps + 滚动）  ⑦ 底部用户菜单（avatar + theme picker + 语言 + 登出）

## 视觉特征

- 容器：`fixed inset-y-0 left-0 z-50 bg-[rgb(249,249,249)] text-slate-600 transition-all duration-300 ease-in-out overflow-hidden w-64`
- 折叠：`-translate-x-full` + `md:translate-x-0 md:w-0` 响应式
- 内部：`px-3 pt-4 pb-2 flex flex-col h-full`
- logo 行：`mb-6 gap-2 flex items-center justify-between`，logo 28x28，标题 `font-semibold text-base tracking-tight cursor-pointer hover:opacity-80`
- 入口按钮：`flex items-center gap-2 px-3 py-2 rounded-lg transition-all border-none text-slate-500 hover:bg-[rgb(237,237,237)] ${themeClasses.textHover}`
- 会话区标题：`px-3 py-2 sticky top-0 bg-[rgb(249,249,249)] z-10 + text-xs font-semibold text-slate-400 uppercase tracking-wider`
- 用户菜单容器：`pt-2 border-t border-slate-200 mt-auto relative`
- 用户头像：`w-8 h-8 rounded-full bg-white border border-slate-200 + group-hover:rotate-12`
- 用户菜单 popup：`absolute bottom-full mb-2 bg-white border border-slate-200 rounded-xl shadow-xl p-1.5 + animate-in fade-in slide-in-from-bottom-4 zoom-in-95 duration-300 origin-bottom`

## 核心代码

见 `core/components/layout/MainLayout.tsx` 第 357-635 行。骨架：

```tsx
<div className="fixed inset-y-0 left-0 z-50 bg-[rgb(249,249,249)] w-64 ...">
  <div className="w-64 h-full flex flex-col px-3 pt-4 pb-2">
    {/* ① logo */}
    <div className="flex items-center justify-between mb-6">
      <img src={logo} className="h-7 w-7" />
      <span>{APP_NAME}</span>
      <button onClick={() => setIsSidebarOpen(false)}><PanelLeftClose size={20} /></button>
    </div>
    {/* ② 空间切换器 */}
    <SpaceSwitcher user={user} />
    {/* ③ ④ ⑤ 入口按钮 */}
    <button className="flex ... text-slate-500 hover:bg-[rgb(237,237,237)] ${themeClasses.textHover}">
      <Plus size={20} />新对话
    </button>
    {/* ⑥ 会话列表（参见 sidebar-session-row block） */}
    <div className="flex-1 overflow-y-auto no-scrollbar">
      <div className="px-3 py-2 sticky top-0 ...">
        <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">CHATS</span>
      </div>
      {sessions.map(s => <SessionRow ... />)}
    </div>
    {/* ⑦ 用户菜单 */}
    <div className="pt-2 border-t border-slate-200 mt-auto relative">
      <div className="group flex items-center gap-3 cursor-pointer hover:bg-[rgb(237,237,237)]">
        <Avatar />
        <span>{user.username}</span>
      </div>
    </div>
  </div>
</div>
```

## 视觉要点（page README 必查）

1. logo 28×28，**hover 时 logo 80% 透明度**（`hover:opacity-80`）—— 不是缩放
2. 入口按钮上 lucide icon size 永远 20，文字永远 `font-medium`（500）
3. 会话列表标题用 `uppercase tracking-wider text-slate-400`——是 sage 的"分组印章"
4. 用户菜单展开是 `slide-in-from-bottom-4 + origin-bottom + duration-300`，比一般 100ms 弹层更慢，强调"从用户位置升起"
5. 头像菜单里有 12 主题色横向 dot 选择器 + 左右箭头 hover 才显（`opacity-0 group-hover/themes:opacity-100`）
6. 整个侧栏有自定义 `::selection` 样式注入 `THEME_SELECTION_COLORS[themeColor]`

## 适配指南

- 父级父级容器必须是 `flex h-screen overflow-hidden`，否则 `mt-auto` 不生效
- 768px 以下自动收回（`window.innerWidth < 768 setIsSidebarOpen(false)` 在每个 nav 后触发）
- 主题切换通过 `usersApi.updateUser(id, { themeColor: color })` 持久化 + dispatch `user-info-updated` event 通知 App.tsx 同步重渲染

## 反模式

- ❌ 把 logo 放在折叠后的 ChatPage header（已经在那有了 PanelLeftOpen 切换）
- ❌ 用 sticky session header 不带 `bg-[rgb(249,249,249)]` —— 滚动时下面内容会透出来
