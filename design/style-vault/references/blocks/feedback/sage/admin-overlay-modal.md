---
id: blocks/feedback/sage/admin-overlay-modal
type: block
name: 管理后台浮层
description: bg-white/95 backdrop-blur-md rounded-2xl shadow-2xl 全屏管理面板 + 右上角关闭，sage 所有 admin 模块的统一外壳
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, glass]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses: []
preview: /preview/blocks/feedback/sage/admin-overlay-modal
---

# Admin Overlay Modal

> sage 大量 admin 功能（用户管理 / 角色管理 / 规则集 / 模型配置 / 数据源 / 空间管理 / 用量分析 / 反馈分析 / 知识库）都不走独立 route，而是从 RevolverMenu 或 CommandPalette 调用 `setActiveAdminModule(module)`，弹出这个全屏 overlay。`max-w-7xl h-[85vh]` 几乎占满屏幕但留四周缝隙，让用户感知到"还在 chat 上下文里"。

## 视觉特征

- 蒙层：`fixed inset-0 z-[110] flex items-center justify-center bg-slate-900/30 backdrop-blur-sm animate-in fade-in duration-200`
- 卡片：`bg-white/95 backdrop-blur-md rounded-2xl shadow-2xl w-full max-w-7xl h-[85vh] mx-4 flex flex-col overflow-hidden relative border border-white/20`
- 关闭按钮：`absolute top-0 right-0 p-2 z-50` + `<button className="p-2 rounded-full bg-slate-100 hover:bg-red-100 text-slate-500 hover:text-red-600 transition-colors shadow-sm"><X size={20}/></button>`
- 内容容器：`flex-1 overflow-auto custom-scrollbar p-2 pt-10`（pt-10 留给关闭按钮）
- Suspense fallback：`h-full flex items-center justify-center` + `<Loading themeColor large />`
- 子内容用 `<PermissionGuard requiredPermission="..."><Component themeColor={themeColor} /></PermissionGuard>` 包裹

## 核心代码

```tsx
{activeAdminModule && (
  <div
    className="fixed inset-0 z-[110] flex items-center justify-center bg-slate-900/30 backdrop-blur-sm animate-in fade-in duration-200"
    onClick={handleClose}
  >
    <div
      className="bg-white/95 backdrop-blur-md rounded-2xl shadow-2xl w-full max-w-7xl h-[85vh] mx-4 flex flex-col overflow-hidden relative border border-white/20"
      onClick={e => e.stopPropagation()}
    >
      <div className="absolute top-0 right-0 p-2 z-50">
        <button
          onClick={handleClose}
          className="p-2 rounded-full bg-slate-100 hover:bg-red-100 text-slate-500 hover:text-red-600 transition-colors shadow-sm"
        >
          <X size={20} />
        </button>
      </div>
      <div className="flex-1 overflow-auto custom-scrollbar p-2 pt-10">
        <Suspense fallback={<div className="h-full flex items-center justify-center"><Loading themeColor={themeColor} size="large" /></div>}>
          {activeAdminModule === 'admin/users' && <PermissionGuard requiredPermission="user:read"><UserManagement themeColor={themeColor} /></PermissionGuard>}
          {/* ... 其它 module ... */}
        </Suspense>
      </div>
    </div>
  </div>
)}
```

## 视觉要点

1. **z-[110]** 很高 —— 因为 RevolverMenu z-100，CommandPalette Modal antd 默认 z-1000，此 overlay 要在它们之上
2. `bg-white/95 + backdrop-blur-md` —— 95% 白底 + md 模糊，让蒙层"几乎实心但能透出 chat 上下文一点点"
3. `border border-white/20` —— 几乎不可见的高光边，让卡片看起来"贴在玻璃上"
4. 关闭按钮 hover 红色 —— sage 用 `bg-slate-100 → bg-red-100` + `text-slate-500 → text-red-600`，是唯一一个"非删除场景里允许 hover 红"的按钮
5. 整层入场只用 `fade-in 200ms`，不缩放——配合 backdrop-blur 给"窗户起雾"的感觉

## 适配指南

- 父级管理 `activeAdminModule` state，子模块卸载时调 `handleCloseOverlay` 清理（特别注意清 `localStorage.removeItem('tempAdminSpaceId')`）
- 子模块得知道自己在 overlay 里：通过 `themeColor` prop 注入主题，通过 `onNavigate` callback 让模块间跳转（不直接 `useNavigate`，免得 overlay 关错）
- `e.stopPropagation()` 是关键 —— 否则点卡片内部会冒泡到蒙层 onClick 关闭

## 反模式

- ❌ 用 `bg-white` 满底 + 不模糊 —— 失去"叠在 chat 之上"的感觉
- ❌ 给关闭按钮加 `bg-red-600` —— 红色 hover 已经够暗示，平时不需要
