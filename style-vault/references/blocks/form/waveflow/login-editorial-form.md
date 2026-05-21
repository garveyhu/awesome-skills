---
id: blocks/form/waveflow/login-editorial-form
type: block
name: Editorial 登录左半表单
description: 14vh padding-top + hero (56px logo + 28px Waveflow. period + tagline) + 10mt 表单 (underline inputs + checkbox + dark-pill CTA) + footer year © sticky 底
platforms: [web]
theme: light
tags:
  aesthetic: [editorial, minimal]
  mood: [calm, confident]
  stack: [shadcn-radix]
uses:
  - components/inputs/waveflow/underline-bare-input
  - components/buttons/waveflow/dark-pill-arrow-cta
preview: /preview/blocks/form/waveflow/login-editorial-form
---

# Waveflow Login Editorial Form (Left Half)

> 登录页左半页内容——editorial editorial split design：**顶部 14vh 留白** → **hero 块**（56×56 圆角 logo + "Waveflow." + 灰 period + 13.5px tagline）→ **mt-10 表单**（underline username + underline password with Eye toggle + 记住我 checkbox + dark-pill "继续" CTA）→ **flex-1 弹性占位** → **footer 12px stone-400 年份 ©**。`max-w-[440px]` 限制内容宽度，整体在父 container 内 sticky 偏上。

## 页面骨架

```tsx
<div className="relative flex w-full flex-col overflow-hidden px-8 sm:px-16 lg:w-1/2">
  <LeftDecor />   {/* 点阵 + 浮件 + 柔光 + 连线（z-0~3） */}

  <div className="relative z-10 pt-[14vh]">
    <div className="max-w-[440px]">
      <img src={waveflowIcon} alt="waveflow" className="mb-5 h-14 w-14 rounded-2xl shadow-[var(--shadow-soft)]" />
      <div className="text-[28px] font-medium tracking-tight text-stone-900" style={{ letterSpacing: '-0.02em' }}>
        Waveflow<span className="text-stone-400">.</span>
      </div>
      <div className="mt-1.5 text-[13.5px] text-stone-500">数据同步与任务调度平台</div>
    </div>

    <div className="mt-10 max-w-[440px]">
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="mb-1 block text-[12px] font-medium text-stone-500">用户名</label>
          <UnderlineInput type="text" name="username" autoFocus value={...} placeholder="请输入用户名" />
          {errors.username && <div className="mt-1 text-[11.5px] text-red-600">{errors.username}</div>}
        </div>

        <div>
          <label className="mb-1 block text-[12px] font-medium text-stone-500">密码</label>
          <div className="relative">
            <UnderlineInput type={showPassword ? 'text' : 'password'} className="pr-8" placeholder="请输入密码" />
            <button type="button" onClick={() => setShowPassword(s => !s)}
              className="absolute right-0 top-1/2 -translate-y-1/2 rounded p-1 text-stone-400 hover:bg-stone-100 hover:text-stone-700">
              {showPassword ? <EyeOff className="h-3.5 w-3.5" /> : <Eye className="h-3.5 w-3.5" />}
            </button>
          </div>
          {errors.password && <div className="mt-1 text-[11.5px] text-red-600">{errors.password}</div>}
        </div>

        <div className="pt-1">
          <label className="flex cursor-pointer items-center gap-2 text-[13px] text-stone-600">
            <Checkbox checked={rememberMe} onCheckedChange={...} className="data-[state=checked]:!border-stone-900 data-[state=checked]:!bg-stone-900 focus-visible:!ring-stone-300" />
            记住我
          </label>
        </div>

        <Button type="submit" variant="dark" disabled={loading}
          className="group !h-11 !min-w-[140px] !rounded-full !px-6 !text-[13.5px] !tracking-wide">
          继续
          {loading ? <Loader2 spin /> : <ArrowRight className="h-3.5 w-3.5 transition group-hover:translate-x-1" />}
        </Button>
      </form>
    </div>
  </div>

  <div className="flex-1 min-h-10" />
  <footer className="relative z-10 pb-10 text-[12px] text-stone-400">
    © {new Date().getFullYear()} Waveflow
  </footer>
</div>
```

## 视觉特征

- **`px-8 sm:px-16 lg:w-1/2`**：移动全宽 / sm 边距加 / lg 占一半（让右半 Three.js 出现）
- **`pt-[14vh]`**：上留白巨大——editorial 气质
- **logo 14×14 (56px) rounded-2xl + shadow-soft**：比 admin sidebar logo (28px) 大 4 倍，浮在背景上
- **"Waveflow." period 配色**：标题 stone-900 + period stone-400—— 视觉切节奏的小细节
- **letter-spacing -0.02em**：紧凑标题感
- **form `space-y-6` (24px)**：字段间距比 dialog 表单（3.5 = 14px）大近 2x —— editorial 给字段呼吸
- **Checkbox 覆写 stone-900**：记住我用 stone-900 而非 blue —— 配合 dark-pill CTA 视觉系
- **footer `flex-1 min-h-10` 弹性占位**：表单和 footer 之间留白自适应屏高

## 适配指南

- "Waveflow." 加 period 是签名风格——可以复用到品牌登录页
- form 容错：input 状态错误时输入立刻清错
- 错误信息走 `text-[11.5px] text-red-600` —— 比 admin (`text-[11px]`) 略大半档（登录的字号整体大）
- 提交后 100ms 延迟 navigate，给 toast 时间显示

## 反模式

- ❌ form 紧凑 `space-y-3.5` —— 失去 editorial 气质
- ❌ form 宽度全宽 —— 视觉散
- ❌ 用 primary blue 替 dark CTA —— 失去签名感
- ❌ logo 改小到 sidebar 同款 —— 失去"主入口"仪式感
