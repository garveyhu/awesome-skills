---
id: pages/empty-error/waveflow/minimal-text-401
type: page
name: 极简文本 401
description: 居中容器 - "401" 大数字 + 主消息 + 副描述 + 返回 / 回首页 双按钮 - 纯样式 CSS 类不走 Tailwind
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm, serious]
  stack: [shadcn-radix]
uses: []
preview: /preview/pages/empty-error/waveflow/minimal-text-401
---

# Waveflow Minimal 401

> waveflow 401 未授权页（`/401`）—— 极简文本，不复用 retro TV 404 的拟物风。**居中容器** + **"401" 大数字** + **"抱歉，您没有权限访问该页面"** 主消息 + **"请联系管理员获取相应的权限"** 副描述 + **"返回上一页 / 回到首页"** 双按钮。**用全局 CSS 类**（`.error-page-container` / `.error-code` 等）而非 Tailwind className——和 404 styled-components 同一套"错误页归全局样式管"的思路。

## 页面骨架

```tsx
const Unauthorized: React.FC = () => (
  <div className="error-page-container">
    <div className="error-content">
      <div className="error-code">401</div>
      <div className="error-message">抱歉，您没有权限访问该页面</div>
      <div className="error-description">请联系管理员获取相应的权限</div>
      <div className="error-actions">
        <button onClick={() => window.history.back()}>返回上一页</button>
        <button onClick={() => (window.location.href = '/')}>回到首页</button>
      </div>
    </div>
  </div>
);
```

## 视觉要点

1. **极简字号金字塔**：401 大字（建议 6em+ stone-200/300）→ 主消息（18-20px stone-700）→ 副描述（14px stone-500）
2. **双按钮平铺**：返回上一页（ghost）+ 回到首页（primary blue-600）—— 给用户两种"逃生"方向
3. **整页居中**：flex center min-h-screen
4. **不走 Layout**：401 直接渲染整页，不嵌 sidebar/topbar
5. **CSS 类全局声明**：让所有错误页（401/404 等）共享同一套 `error-page-*` class，方便统一调整

## 适配指南

- 401 = 已登录但无权限；403 同语义可复用
- 配合 axios 401 拦截器：捕到 401 → navigate('/401') 或者直接显示这页
- 推荐主消息提供"请联系 admin"的"接下来怎么做"指引，避免用户卡死
- 错误页路由必须 `meta.auth: false`，否则未登录访问会循环重定向

## 反模式

- ❌ 把 401 也做成 retro TV 风—— 失去"权限错误"的严肃性（应该和 404 visual 区分）
- ❌ 只放"回到首页"按钮—— 大概率用户想"返回"看刚看的页
- ❌ 用复杂插画—— 错误页应该 < 1KB，加载失败也能看
