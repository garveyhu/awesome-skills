---
id: pages/auth/waveflow/login-editorial-three
type: page
name: Editorial Split 登录（含 Three.js）
description: 左半 editorial 表单 (14vh hero + underline inputs + dark-pill CTA) + 右半 Three.js dark scene (三 icosahedron + 200 stars + 双 radial glow + serif italic 诗句) + LeftDecor 4 SVG 浮件 + 动态连线
platforms: [web]
theme: light
tags:
  aesthetic: [editorial, minimal]
  mood: [calm, dreamy, confident]
  stack: [shadcn-radix]
uses:
  - blocks/form/waveflow/login-editorial-form
  - blocks/form/waveflow/login-three-decor-right
  - tokens/texture/waveflow/login-floating-geom-quartet
  - tokens/texture/waveflow/login-dot-grid-mask
  - tokens/motion/waveflow/three-icosahedron-bg
preview: /preview/pages/auth/waveflow/login-editorial-three
---

# Waveflow Login Editorial + Three.js

> waveflow 登录页 (`/login`) ——editorial split design 的完整实现。**整页 `flex min-h-screen`**：左 50% editorial 表单（14vh padding + hero "Waveflow." + underline 表单 + dark-pill "继续" CTA + 4 SVG 浮件 + 动态连线 + dot grid mask + 鼠标 multiply 柔光 + footer 年份）/ 右 50%（仅 `lg+` 显示） dark gradient + Three.js 三 icosahedron + serif italic 诗句"让数据，自如流转。"

## 页面骨架

```tsx
<div className="flex min-h-screen">
  {/* 左半 editorial 表单 */}
  <div className="relative flex w-full flex-col overflow-hidden px-8 sm:px-16 lg:w-1/2">
    <LeftDecor />     {/* 点阵 + 4 SVG 浮件 + 鼠标柔光 + 动态连线 */}
    <div className="relative z-10 pt-[14vh]">
      <HeroLogo />    {/* 14×14 logo + "Waveflow." + tagline */}
      <Form className="mt-10" />   {/* underline inputs + Eye toggle + 记住我 + dark-pill CTA */}
    </div>
    <div className="flex-1 min-h-10" />
    <footer className="relative z-10 pb-10 text-[12px] text-stone-400">© {year} Waveflow</footer>
  </div>

  {/* 右半 Three.js（lg+ only） */}
  <div className="relative hidden w-1/2 overflow-hidden lg:block">
    <div className="absolute inset-0" style={{ background: 'linear-gradient(135deg, #0a0e1a 0%, #1a1530 50%, #0a1822 100%)' }} />
    <div className="pointer-events-none absolute inset-0" style={{ background: 'radial-gradient(circle at 30% 40%, rgba(99,102,241,0.3), transparent 60%), radial-gradient(circle at 70% 70%, rgba(6,182,212,0.2), transparent 60%)' }} />
    <ThreeBackground />
    <div className="pointer-events-none absolute inset-x-0 bottom-0 z-10 flex flex-col p-10 text-white">
      <p className="mb-2 text-[11px] tracking-[0.4em] text-white/40">实时编排 · 数据中枢</p>
      <h2 className="text-[30px] font-light leading-tight tracking-tight" style={{ letterSpacing: '-0.01em' }}>
        让数据，
        <span className="text-white/85" style={{ fontFamily: 'var(--font-serif)', fontStyle: 'italic', fontWeight: 400 }}>
          自如流转。
        </span>
      </h2>
    </div>
  </div>
</div>
```

## 视觉要点

1. **左半 5 层 z-index**：底 dot grid (0) → SVG 动态连线 (1) → 柔光 (2) → 浮件 (3) → 内容 (10) → footer (10)
2. **"Waveflow." 配色 trick**：标题 stone-900 + period stone-400 —— 视觉签名
3. **14vh top padding**：editorial 气质的根
4. **响应式**：lg- 只显示左半（Three.js 隐）；< sm 收紧 padding 到 px-8
5. **登录态防回登录**：`forbidRepeatLogin` route meta + `isAuthenticated()` 检查重定向到 /
6. **URL `?redirect=xxx`**：登录后跳到原目标页（带 query 参数也保留）
7. **toast.success("登录成功")** 后 100ms 延迟 navigate（给 toast 时间显示）
8. **Three.js cleanup**：useEffect return 必须 dispose 所有 geometry/material + cancelAnimationFrame + removeChild
9. **LeftDecor cleanup**：mousemove/mouseleave listener 解除 + cancelAnimationFrame

## 适配指南

- API 失败 toast.error，不 navigate；保留 form 输入让用户重试
- "记住我" 切换 `rememberMe: 1 / 0` 字段传给后端，决定 token 存 localStorage vs sessionStorage
- Three.js 加载首屏白屏：waveflow 选择直接加载（首屏即登录）
- 移动端体验：右半隐藏后左半铺满，editorial 气质保留

## 反模式

- ❌ 没 LeftDecor 整页太空—— editorial 失败
- ❌ Three.js 不 dispose—— 每次进登录 +50MB 内存
- ❌ "Waveflow." 不带 period—— 失去签名
- ❌ form padding 改紧凑（space-y-3.5）—— 失去 editorial 节奏
