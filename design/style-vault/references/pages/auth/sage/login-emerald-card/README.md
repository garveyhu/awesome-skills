---
id: pages/auth/sage/login-emerald-card
type: page
name: 登录页
description: slate-50 全屏背景 + 居中卡片 + emerald CTA + 注册码可选 + 右上语言切换
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - blocks/marketing/sage/auth-emerald-card
  - components/inputs/sage/icon-prefix-input
preview: /preview/pages/auth/sage/login-emerald-card
---

# Sage 登录页

> sage 登录路由 `/login`。整页 `bg-slate-50` + 居中 `max-w-md` 卡片 + 右上角语言选择器。卡片内 logo 12×12 居中 + 标题 + Username + Password (+ 注册码可选) + emerald submit + 切换链接。**关键**：登录前用户没主题色，所有强调色固定 emerald-600。

## 页面骨架（自上而下）

1. **绝对定位语言选择器**：`absolute top-4 right-4` + 地球图标 + 当前语言名
2. **居中容器**：`min-h-screen flex items-center justify-center bg-slate-50`
3. **卡片**：`bg-white p-8 rounded-2xl shadow-xl w-full max-w-md`
   - **Header 区** `text-center mb-8`：logo 48×48 + h1 24px bold slate-800 "{APP_NAME}" + 副标题 slate-500 mt-2（"AI 数据分析平台" / "注册新账号"）
   - **Error banner**（如有）：`mb-4 p-3 bg-red-50 text-red-600 text-sm rounded-lg`
   - **Form** `space-y-4`：
     - Username（lucide UserIcon 前缀）
     - Password（Lock 前缀 + Eye/EyeOff toggle）
     - Registration Code（注册时显示 · Key 前缀 + Eye toggle）
   - **Submit** `mt-6` `bg-emerald-600 hover:bg-emerald-700 text-white py-2 rounded-lg + ArrowRight 后缀`
   - **切换** `mt-6 text-center text-sm text-slate-600` + emerald 链接

## 视觉要点

1. **3 处独有视觉结构**：
   - logo 12×12 + APP_NAME 大字标题（远比 sidebar 的 7×7 logo 突出）
   - 注册码字段 type="password" + Eye toggle —— 防偷看（注册码当一次性凭证）
   - submit 按钮固定 `<ArrowRight size={18} />` 后缀 —— 视觉推动用户进入
2. error banner 用 `bg-red-50 text-red-600` 浅红 —— 不刺眼但能看到
3. emerald 系（不走 themeClasses）的所有色阶：`bg-emerald-600 hover:bg-emerald-700 text-emerald-600 focus:ring-green-500`
4. 卡片角圆 16 + xl shadow 比 admin overlay 的 2xl shadow 略弱 —— "邀请进入"的轻盈感

## 跳转逻辑

- 成功 + 有空间 → `localStorage.setItem(USER_INFO_KEY, JSON.stringify(user))` + `localStorage.setItem('currentSpaceId', String(spaceId))` + 应用 user.language → `navigate('/', { replace: true })`
- 成功 + 无空间 → 显示"请联系管理员分配空间"错误 + 清 token
- 注册成功 → 自动登录（不让用户再输一次密码）

## 反模式

- ❌ 用 themeClasses 着色 —— 登录前 themeColor=blue fallback，跟 emerald 品牌不一致
- ❌ 把 logo 放在 form 顶部内（不居中显示） —— 登录页是品牌时刻
