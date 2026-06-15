---
id: components/inputs/sage/icon-prefix-input
type: component
name: 前缀图标输入框
description: pl-10 + 绝对定位 lucide 图标的表单输入，sage 登录页 / 注册码 / 部分 admin 表单的标准款
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm]
  stack: [react-antd-tailwind]
uses: []
preview: /preview/components/inputs/sage/icon-prefix-input
---

# Icon Prefix Input

> 登录页风格的输入框——左侧 lucide 图标（绝对定位 `left-3 top-2.5 text-slate-400`）+ 文本输入 + 可选右侧 toggle 按钮（密码可见性切换）。无主题色侵染（登录前没主题）。

## 视觉特征

- 容器：`relative` 用作图标定位锚点
- icon：`absolute left-3 top-2.5 text-slate-400`，size 20
- input：`w-full pl-10 pr-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none`
- 右侧 toggle：`absolute right-3 top-2.5 text-slate-400 hover:text-slate-600 transition-colors` + `<Eye/EyeOff/>`，`tabIndex={-1}` 防止 tab 焦点
- label：`block text-sm font-medium text-slate-700 mb-1`（出现 15 处）

## 核心代码

```tsx
import { Lock, Eye, EyeOff } from 'lucide-react';

<div>
  <label className="block text-sm font-medium text-slate-700 mb-1">Password</label>
  <div className="relative">
    <Lock className="absolute left-3 top-2.5 text-slate-400" size={20} />
    <input
      type={showPassword ? 'text' : 'password'}
      value={password}
      onChange={e => setPassword(e.target.value)}
      className="w-full pl-10 pr-10 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
      required
    />
    <button
      type="button"
      onClick={() => setShowPassword(v => !v)}
      className="absolute right-3 top-2.5 text-slate-400 hover:text-slate-600 transition-colors"
      tabIndex={-1}
    >
      {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
    </button>
  </div>
</div>
```

## 适配指南

- 登录 / 注册场景固定 `focus:ring-green-500`（emerald 是 sage 登录页的"品牌色"，固定不变）
- admin 表单内的 input 走 ManagementLayout 注入的 ConfigProvider 主题——和这条不一样，那时候用 antd Input
- toggle 按钮永远 `tabIndex={-1}`：让 tab 顺序保持 input → 下一字段，跳过装饰按钮

## 反模式

- ❌ icon size 用默认 24 —— 视觉太重；20 / 18 更协调
- ❌ 把 `focus:ring-green-500` 改成主题色 —— 登录前用户没主题，也没必要为登录页一个表单写多色
