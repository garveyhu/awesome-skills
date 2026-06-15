---
id: components/inputs/waveflow/underline-bare-input
type: component
name: 极简下划线输入
description: 登录表单专属 - bg 透明 + border-b only + py-2.5 + 15px Inter + 失焦深 stone-300 / 聚焦 stone-900 / error red-400→600
platforms: [web]
theme: light
tags:
  aesthetic: [editorial, minimal]
  mood: [calm, confident]
  stack: [shadcn-radix]
uses: []
preview: /preview/components/inputs/waveflow/underline-bare-input
---

# Waveflow Underline Bare Input

> 登录页"用户名 / 密码"输入框的极简形态——**没有 box border**、**没有 background**、**只有底部一根 1px stone-300 横线**。失焦 stone-300 / 聚焦 stone-900 / error red。15px font-size 让字大、py-2.5 让点击区域宽。这是 waveflow 登录页 editorial 气质的最直接载体。

## 视觉特征

- **基础类**：`w-full border-b bg-transparent py-2.5 text-[15px] text-stone-900 outline-none transition placeholder:text-stone-400`
- **失焦边色**：`border-stone-300`（淡灰）
- **聚焦边色**：`focus:border-stone-900`（变墨黑——和文字同色）
- **error 边色**：`border-red-400 focus:border-red-600`
- **font-size 15px**：比标准 input 的 13px 大 2px——登录表单要"大"
- **py-2.5 (10px)**：上下 padding 加大，整高约 38px
- **bg-transparent**：让登录页背景（点阵 / 浮件）透过来——是 editorial 气质的根
- **label 在 input 上**：`<label className="mb-1 block text-[12px] font-medium text-stone-500">用户名</label>` —— 标签和 input 不挤在一行

## 核心代码

```tsx
<input
  type="text"
  name="username"
  autoComplete="username"
  value={username}
  onChange={...}
  placeholder="请输入用户名"
  className={cn(
    'w-full border-b bg-transparent py-2.5 text-[15px] text-stone-900 outline-none transition placeholder:text-stone-400',
    errors.username
      ? 'border-red-400 focus:border-red-600'
      : 'border-stone-300 focus:border-stone-900',
  )}
/>
```

## 适配指南

- 仅用在**全屏白底/暖底**的入口表单：登录、忘记密码、注册三屏。**绝不**用在 Dialog 表单或 admin 内部
- 密码输入框右侧 Eye/EyeOff toggle：`<button className="absolute right-0 top-1/2 -translate-y-1/2 rounded p-1 text-stone-400 hover:bg-stone-100 hover:text-stone-700">`
- 错误提示：`<div className="mt-1 text-[11.5px] text-red-600">{errors.username}</div>`
- 输入变化清错：`onChange` 里检测到 errors[field] 存在时立即清空 → 不让用户重输报错"卡住"

## 反模式

- ❌ 加 background-color——失去 editorial 透明感
- ❌ 加 box border / rounded——立刻变成普通 Input
- ❌ 用 13px font-size——和登录页的"大动作"气质不符
- ❌ 跟 admin Input 共用同一 component—— 两套视觉语言不该混
