---
id: components/buttons/waveflow/dark-pill-arrow-cta
type: component
name: 深色胶囊箭头 CTA
description: 登录页"继续"按钮 - stone-900 底 + rounded-full + 箭头 hover translate-x-1 + loading 切 Loader2
platforms: [web]
theme: light
tags:
  aesthetic: [editorial, minimal]
  mood: [confident, serious]
  stack: [shadcn-radix]
uses:
  - components/buttons/waveflow/cva-engineer-button
preview: /preview/components/buttons/waveflow/dark-pill-arrow-cta
---

# Waveflow Dark Pill Arrow CTA

> 登录页"继续"按钮——基于 cva-engineer-button 的 `variant="dark"`，加 `rounded-full + min-w + group hover` 包装实现：右侧 `ArrowRight` icon `group-hover:translate-x-1` 缓动 200ms。loading 时 ArrowRight 切 Loader2 spin。它是 waveflow 登录页"editorial 性格"的视觉句号。

## 视觉特征

- **核心 className**：`group !h-11 !min-w-[140px] !rounded-full !px-6 !text-[13.5px] !tracking-wide`
- **底层 variant**：`dark` (`bg-stone-900 text-white hover:bg-stone-800 active:bg-stone-700`)
- **高度 h-11 (44px)**：比 Button 的 lg=h-9 高 8px——登录是大动作 CTA
- **rounded-full**：完全圆角胶囊形——和 admin 主体的 `rounded-md` 形成断层
- **min-w-[140px]**：保证"继续 →" 不会窄到只一个字 + 一个箭头
- **tracking-wide (0.025em)**：字距加宽，让"继续"4 个字距撑开
- **箭头位移动画**：`<ArrowRight className="h-3.5 w-3.5 transition group-hover:translate-x-1" />` —— 200ms 默认 transition + translateX 4px
- **loading 替换**：`{loading ? <Loader2 spin /> : <ArrowRight ... />}` —— **不**在 loading 时还做位移

## 核心代码

```tsx
<Button
  type="submit"
  variant="dark"
  disabled={loading}
  className="group !h-11 !min-w-[140px] !rounded-full !px-6 !text-[13.5px] !tracking-wide"
>
  继续
  {loading ? (
    <Loader2 className="h-3.5 w-3.5 animate-spin" />
  ) : (
    <ArrowRight className="h-3.5 w-3.5 transition group-hover:translate-x-1" />
  )}
</Button>
```

## 适配指南

- 登录页提交按钮的**唯一**形态——其它表单 CTA 用 `variant="primary"`（blue-600 + rounded-md）
- 复用到 onboarding 第一屏 / 注册成功页"下一步"也合适，**不要**用到 admin 主体内部
- 必须 type="submit" 配合 `<form onSubmit={...}>`，按 Enter 也能触发

## 反模式

- ❌ 用在 admin 表格内—— editorial 胶囊在工业风列表里显违和
- ❌ 把箭头改成右上 `↗` —— 那是"打开新窗口"语义
- ❌ 高度改 h-9—— 失去登录页"大动作"的仪式感
- ❌ tracking-wide 改 tracking-tight—— 紧凑字距失去 editorial 气质
