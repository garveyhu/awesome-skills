---
id: blocks/marketing/sage/auth-emerald-card
type: block
name: 登录卡片
description: max-w-md 居中卡片 + emerald CTA + 图标前缀输入 + 注册码切换，sage 登录页核心模块
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - components/inputs/sage/icon-prefix-input
preview: /preview/blocks/marketing/sage/auth-emerald-card
---

# Auth Emerald Card

> sage 登录页核心卡片——`max-w-md bg-white p-8 rounded-2xl shadow-xl`，slate-50 背景中央。Logo + 大标题 + 副标题 + Username + Password (+ 注册码可选) + Submit + 登录/注册切换链接。emerald 为登录前唯一固定主题色（用户尚未登录无 themeColor）。

## 视觉特征

- 整页背景：`min-h-screen flex items-center justify-center bg-slate-50`
- 右上语言切换：`absolute top-4 right-4` + LoginLanguageSelector
- 卡片：`bg-white p-8 rounded-2xl shadow-xl w-full max-w-md`
- Header：`text-center mb-8`
- Logo：`flex justify-center mb-4` + `h-12 w-12`
- Title：`text-2xl font-bold text-slate-800`
- Subtitle：`text-slate-500 mt-2`
- Error banner：`mb-4 p-3 bg-red-50 text-red-600 text-sm rounded-lg`
- Form：`space-y-4`
- Field label：`block text-sm font-medium text-slate-700 mb-1`
- Field input：`w-full pl-10 pr-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none`
- Submit：`mt-6` + `w-full bg-emerald-600 text-white py-2 rounded-lg hover:bg-emerald-700 transition-colors flex items-center justify-center gap-2`，结尾 `<ArrowRight size={18} />`
- 注册切换：`mt-6 text-center text-sm text-slate-600` + `<button className="text-emerald-600 font-medium hover:underline">`

## 核心代码

```tsx
<div className="min-h-screen flex items-center justify-center bg-slate-50">
  <div className="absolute top-4 right-4"><LoginLanguageSelector /></div>

  <div className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md">
    <div className="text-center mb-8">
      <div className="flex justify-center mb-4"><img src={logo} className="h-12 w-12" /></div>
      <h1 className="text-2xl font-bold text-slate-800">{APP_NAME}</h1>
      <p className="text-slate-500 mt-2">{isRegistering ? '注册新账号' : 'AI 数据分析平台'}</p>
    </div>

    {error && <div className="mb-4 p-3 bg-red-50 text-red-600 text-sm rounded-lg">{error}</div>}

    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Username */}
      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">Username</label>
        <div className="relative">
          <UserIcon className="absolute left-3 top-2.5 text-slate-400" size={20} />
          <input className="w-full pl-10 pr-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none" required />
        </div>
      </div>

      {/* Password ... + 可见性切换 */}

      {isRegistering && /* 注册码 with Key icon */}

      <button type="submit" className="w-full bg-emerald-600 text-white py-2 rounded-lg hover:bg-emerald-700 transition-colors flex items-center justify-center gap-2">
        {isRegistering ? '注册' : '登录'}<ArrowRight size={18} />
      </button>
    </form>

    <div className="mt-6 text-center text-sm text-slate-600">
      {isRegistering ? '已有账号？' : '还没账号？'}{' '}
      <button onClick={() => setIsRegistering(v => !v)} className="text-emerald-600 font-medium hover:underline">
        {isRegistering ? '登录' : '注册'}
      </button>
    </div>
  </div>
</div>
```

## 视觉要点

1. emerald-600 不走 `themeClasses` —— 固定色因为 "登录前没主题"
2. `rounded-2xl shadow-xl` —— 比 admin overlay 的 shadow-2xl 略弱，给"轻、邀请进入"的感觉
3. Logo 12×12 比 sidebar 的 7×7 大近一倍 —— 登录页是品牌时刻，要把 logo 放大
4. 注册码字段是 `password` 类型 + Eye/EyeOff toggle —— 防偷看（有些组织把注册码当一次性凭证）
5. Submit 按钮固定 `<ArrowRight />` 后缀 —— 视觉上"推动用户进入"

## 适配指南

- 错误处理走 `setError(message)` + 红色 banner
- 登录成功有两个分支：有 space → navigate '/'，无 space → 显示 "请联系管理员分配空间" 错误并清 token
- 注册成功后**自动登录**（不让用户再输一次密码）

## 反模式

- ❌ 把整张卡铺满屏 —— 失去"邀请进入"的感觉
- ❌ submit 用主题色 —— 登录前 themeColor 是 "blue" fallback，但视觉跟 emerald 品牌不一致
