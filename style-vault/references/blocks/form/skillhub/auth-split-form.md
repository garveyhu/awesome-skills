---
id: blocks/form/skillhub/auth-split-form
type: block
name: 分屏登录注册表单
description: 两屏切换（密码 / 注册）+ slate 渐变方块 logo + soft-form-input 字段 + dark CTA
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/skillhub/skillhub-teal-mist
  - tokens/typography/pairs/skillhub/inter-jetbrains-duo
  - components/inputs/skillhub/soft-form-input
  - components/buttons/skillhub/dark-primary-cta
preview: /preview/blocks/form/skillhub/auth-split-form
---

# Auth Split Form

> 登录 / 注册共用一个 form block。顶部是 10×10 的 slate 渐变方块 logo + 站名 + mode 切换胶囊（密码登录 / 创建账号），下面是 soft-form-input 字段组 + dark CTA 结尾。

## 视觉特征

### 顶栏
- 2 列 flex gap-4：左方块 + 右标题
- 方块：`w-10 h-10 rounded-xl bg-gradient-to-br from-slate-800 to-slate-950 text-white font-bold shadow-md`
- 标题：`text-2xl font-extrabold text-slate-900 tracking-tight`

### Mode 切换
- 横向两按钮 pill：`flex gap-2 p-1 bg-slate-100 rounded-xl border border-slate-200/60`
- active：`bg-white text-slate-900 shadow-sm`
- default：`text-slate-500 hover:text-slate-700`

### Feedback 条
- 成功：`bg-emerald-50 text-emerald-700 border-emerald-200`
- 错误：`bg-red-50 text-red-700 border-red-200`
- 样式：`p-4 rounded-xl text-sm font-medium border`

### 字段组
- `space-y-5`
- 每个 field：label `text-sm font-bold text-slate-900 mb-1.5` + SoftFormInput
- 子 hint：`text-xs text-slate-500`

### 提交
- 全宽 DarkPrimaryCta size=lg，放在表单末

## 核心代码

```tsx
type Mode = 'login' | 'register';

export const AuthSplitForm = () => {
  const [mode, setMode] = useState<Mode>('login');
  const [feedback, setFeedback] = useState<string | null>(null);
  // ... form state

  return (
    <div className="mx-auto w-full max-w-sm lg:w-96">
      {/* Logo + 标题 */}
      <div className="flex gap-4 items-center mb-8">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-slate-800 to-slate-950
                        flex items-center justify-center text-white font-bold shadow-md">
          S
        </div>
        <h2 className="text-2xl font-extrabold text-slate-900 tracking-tight">
          {mode === 'login' ? '登录 SkillHub' : '加入 SkillHub'}
        </h2>
      </div>

      {/* Mode 切换 */}
      <div className="flex gap-2 p-1 bg-slate-100 rounded-xl mb-8 border border-slate-200/60">
        <button
          onClick={() => setMode('login')}
          className={`flex-1 py-2 text-sm font-semibold rounded-lg transition-all ${
            mode === 'login' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-700'
          }`}
        >
          密码登录
        </button>
        <button
          onClick={() => setMode('register')}
          className={`flex-1 py-2 text-sm font-semibold rounded-lg transition-all ${
            mode === 'register' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-700'
          }`}
        >
          创建账号
        </button>
      </div>

      {/* Feedback */}
      {feedback && (
        <div className={`p-4 rounded-xl mb-6 text-sm font-medium border ${
          feedback.includes('成功')
            ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
            : 'bg-red-50 text-red-700 border-red-200'
        }`}>
          {feedback}
        </div>
      )}

      {/* 字段组 */}
      {mode === 'login' ? (
        <form className="space-y-5" onSubmit={handleSubmit}>
          <SoftFormInput label="邮箱地址" type="email" placeholder="admin@example.com" />
          <SoftFormInput label="密码" type="password" placeholder="至少 8 位" />
          <DarkPrimaryCta size="lg" className="w-full justify-center" type="submit">
            登录
          </DarkPrimaryCta>
        </form>
      ) : (
        <form className="space-y-5" onSubmit={handleSubmit}>
          <SoftFormInput label="昵称" placeholder="展示用名" />
          <SoftFormInput label="邮箱地址" type="email" placeholder="admin@example.com" />
          <SoftFormInput label="密码" type="password" placeholder="至少 8 位" />
          <SoftFormInput label="确认密码" type="password" />
          <DarkPrimaryCta size="lg" className="w-full justify-center" type="submit">
            创建账号
          </DarkPrimaryCta>
        </form>
      )}

      {/* 第三方登录 */}
      <div className="mt-6 pt-6 border-t border-slate-200">
        <GoogleLoginButton />
      </div>
    </div>
  );
};
```

## 布局（在 page 里用）

```tsx
<div className="min-h-screen bg-slate-50 flex font-sans">
  {/* 左：form */}
  <div className="flex-1 flex flex-col justify-center py-12 px-4 sm:px-6 lg:flex-none lg:px-20 xl:px-24 w-full lg:w-1/2">
    <AuthSplitForm />
  </div>

  {/* 右：visual panel（仅 lg+） */}
  <div className="hidden lg:block lg:flex-1 bg-gradient-to-br from-slate-900 to-slate-950 relative overflow-hidden">
    {/* 可选装饰：流光、渐变、Slogan */}
  </div>
</div>
```

## 适配指南

- logo 方块单字母（"S"），需要换品牌时直接换字符，gradient 色可以换（但继续保持 deep-dark 系以压住浅底）
- mode toggle 两个按钮的 active 色是 `bg-white` 不是 `bg-slate-900`——和 dark CTA 区分：toggle 是"当前模式"而不是"提交动作"
- 验证错误用 rose 不要用 orange——orange 留给通知
- CTA 必须 `w-full` + `justify-center`（dark-primary-cta 默认 inline-flex 不满宽）
- 表单提交后等待态建议在 CTA 上加 `loading` + `disabled` + `opacity-60 cursor-not-allowed`，不必改版式

## 反模式

- 不要用 Antd `<Form>`——自制表单更贴近品牌字体 + 间距；Antd 的 Form.Item 默认标签和间距不合本系
- 不要让 mode toggle 消失（比如点 "密码登录" 后藏注册）——保留 toggle 让用户能回切
- 不要在 register 里加 terms checkbox 作为主提交条件——如必须，放在 CTA 下方独立文字链式同意，不把它做得视觉等重
