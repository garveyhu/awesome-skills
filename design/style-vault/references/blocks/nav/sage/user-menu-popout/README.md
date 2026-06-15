---
id: blocks/nav/sage/user-menu-popout
type: block
name: 用户菜单浮层
description: 左下角用户头像点击展开 · 头像选择 5 列网格 + 主题色横向 chip 滑条 + 语言切换 + 登出 · 浮层 fixed bottom-full + zoom-in-95 动效
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm]
  stack: [react-antd-tailwind]
preview: /preview/blocks/nav/sage/user-menu-popout
---

# User Menu Popout

> sage MainLayout 左下角用户区。点击用户行展开向上浮的菜单，包含 4 个区块：头像选择网格 / 主题色滑条 / 语言切换 / 登出。语言切换需点开嵌套，走 `createPortal` 浮到右侧（避开浮层堆叠）。

## 用户行（触发器）

容器：`pt-2 border-t border-slate-200 mt-auto relative`

按钮：`flex items-center gap-3 px-2 cursor-pointer hover:bg-[rgb(237,237,237)] py-1.5 rounded-lg transition-all duration-200 group`

- 头像圆：`w-8 h-8 rounded-full bg-white border border-slate-200 flex items-center justify-center font-bold transition-transform duration-300 group-hover:rotate-12`
  - 内含 `<UserAvatarIcon size={18} className={themeClasses.text} />`
- 用户名：`p-flex-1 overflow-hidden` + `text-sm font-medium text-slate-700 truncate group-hover:text-slate-900 transition-colors`

## 浮层主体（向上展开）

容器（条件 `isUserMenuOpen`）：
```
absolute bottom-full left-0 w-full mb-2
bg-white border border-slate-200 rounded-xl shadow-xl p-1.5 z-20
animate-in fade-in slide-in-from-bottom-4 zoom-in-95 duration-300 ease-out origin-bottom
```

### 1. 头像选择区
- `px-2 py-2 border-b border-slate-100 mb-1`
- 标题：`text-xs font-medium text-slate-500 mb-2` "头像"
- 网格：`grid grid-cols-5 gap-1.5 mb-3 max-h-32 overflow-y-auto no-scrollbar p-0.5`
- 每个头像：`w-8 h-8 rounded-full flex items-center justify-center transition-all`
  - 选中：`{themeClasses.bg} text-white scale-110 shadow-sm`
  - 未选：`bg-slate-100 text-slate-500 hover:bg-slate-200 hover:scale-105`

### 2. 主题色滑条
- `text-xs font-medium text-slate-500 mb-2` "主题色"
- 容器：`flex items-center justify-between -mx-1.5 group/themes`（`group/themes` named group 控制 chevron 显隐）
- 左 ChevronLeft：`opacity-0 group-hover/themes:opacity-100`
- 中：`flex gap-1.5 overflow-x-auto scroll-smooth py-1 px-1 no-scrollbar flex-1`
  - 内联 style：`{ scrollbarWidth: 'none', msOverflowStyle: 'none', WebkitOverflowScrolling: 'touch' }`
- 右 ChevronRight：同左
- 每个色块：`flex-shrink-0 w-6 h-6 rounded-full border-2 transition-all`
  - 选中：`border-slate-600 scale-110 shadow-sm`
  - 未选：`border-transparent hover:scale-110`

### 3. 语言切换
- `flex items-center gap-2 text-slate-600 hover:text-slate-900 w-full px-3 py-2 rounded-lg hover:bg-slate-50 transition-colors text-sm`
- 内：`<Globe size={16} />` + 当前语言原生名

### 4. 登出
- 同上的 button 类，但 `hover:text-red-600`
- `<LogOut size={16} />` + "退出登录"

## 语言子菜单（Portal）

`createPortal` 到 `document.body`：
- `fixed z-[9999] bg-white border border-slate-200 rounded-xl shadow-lg p-2 min-w-[160px]`
- `animate-in fade-in slide-in-from-left-2 duration-150`
- inline style: `left: '15.5rem', bottom: '6rem'`（精确定位到 sidebar 右边缘 + 用户行垂直对齐）

### 三角箭头（双层做白边）
- 外层（slate 边）：`absolute right-full top-1/2 -translate-y-1/2 border-t-[7px] border-b-[7px] border-r-[7px] border-r-slate-200`
- 内层（白填充，盖在外层上 1px）：`right-full top-1/2 -translate-y-1/2 border-t-[6px] border-b-[6px] border-r-[6px] border-r-white mr-[-1px]`

## 视觉要点

1. **group-hover/themes/ named group**：主题滑条左右 chevron 默认透明，hover 整个滑条时才显 —— 不喧宾夺主
2. **createPortal 给语言菜单**：避免 user menu 内部 z-index 不够导致被 sidebar 遮挡；同时让箭头能穿出
3. **双层 border 三角箭头**：CSS border trick 做出白底 + slate 描边的"漂浮感"
4. **animate-in / slide-in-from-bottom-4 / zoom-in-95 / origin-bottom**：浮层从下往上"弹出"，origin-bottom 保证缩放从底部开始
5. **头像 hover rotate-12**：触发器头像 hover 时 12° 旋转，告诉用户它是个可点击的 trigger 而不是装饰

## 反模式

- ❌ 不要用 antd Dropdown —— 头像/主题双滑动 + Portal 子菜单是 antd Dropdown 难以实现的复合交互
- ❌ 不要用 `transform: scale` 动效 —— 浮层动用 tailwind animate-in（Radix style），更自然
- ❌ 主题色滑条不要无限滚 —— 用 Chevron 控制 200ms scroll-smooth 移动，避免 swipe 卡

## 使用上游
- `core/components/layout/MainLayout` （sidebar 固定底部位置）
