---
id: components/avatars-icons/chameleon/provider-bot-avatar
type: component
name: 品牌单字头像 + 渐变 Bot 头像
description: 两个 AI 身份头像 - (A)按 provider code 给品牌色+短标(DS/通/AI/⇄/Di/FG/Cz)的方头像 (B)violet→blue 圆形渐变 + 白色 Bot 图标
platforms:
- web
theme: light
tags:
  aesthetic:
  - minimal
  - industrial
  mood:
  - calm
  - serious
  stack:
  - shadcn-radix
uses:
- tokens/palettes/waveflow/warm-paper-ink-blue
preview: /preview/components/avatars-icons/chameleon/provider-bot-avatar
---

# Chameleon 品牌单字头像 + 渐变 Bot 头像

> 两个互补的 AI 身份头像。**(A) ProviderAvatar 品牌单字方头像**：按 provider code 给品牌色对（bg/text/ring）+ 短标（DS/通/AI/⇄/Di/FG/Cz），替代千篇一律的灰云图标提升可扫性；未知 code 回退首两字母 + 中性色，孤儿（`__deleted_*`）剥后缀。**(B) 渐变 Bot 头像**：`h-6 w-6 rounded-full bg-gradient-to-br from-violet-500 to-blue-500` + 白色 `Bot` 图标，playground AI 消息气泡 / widget bot 头像共用；对比列头变体降为 `h-4 w-4 rounded` 同渐变色块（无图标）。

## 视觉特征 · (A) ProviderAvatar 品牌单字方头像

- **外层**：`flex shrink-0 items-center justify-center rounded-lg(8px) font-semibold ring-1 ring-inset`
- **2 档尺寸**：`sm = h-8 w-8(32px) text-[11px]` / `md = h-10 w-10(40px) text-[13px]`
- **品牌色对（bg / text / ring，全 50/600/100 系）+ 短标**：
  - deepseek `'DS'` → `bg-blue-50 text-blue-600 ring-blue-100`
  - qwen `'通'` → `bg-violet-50 text-violet-600 ring-violet-100`
  - openai `'AI'` → `bg-emerald-50 text-emerald-600 ring-emerald-100`
  - new-api / oneapi `'⇄'` → `bg-primary-50 text-primary-600 ring-primary-100`（随 --color-primary 切换，默认 blue）
  - dify `'Di'` → `bg-indigo-50 text-indigo-600 ring-indigo-100`
  - fastgpt `'FG'` → `bg-cyan-50 text-cyan-600 ring-cyan-100`
  - coze `'Cz'` → `bg-amber-50 text-amber-600 ring-amber-100`
- **fallback**：`{ label: '?', cls: 'bg-stone-100 text-stone-500 ring-stone-200' }`；有 code 但未匹配则取首两字母大写（`key.slice(0,2).toUpperCase()`）+ fallback 色
- **孤儿剥后缀**：`code.toLowerCase().replace(/__deleted.*/, '')`

## 视觉特征 · (B) 渐变 Bot 头像

- **AI 消息头像**：`mt-0.5 flex h-6 w-6(24px) shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-violet-500(#8b5cf6) to-blue-500(#3b82f6) text-white`，内含 `Bot h-3.5 w-3.5(14px)`
- **对比列头变体**：`h-4 w-4(16px) shrink-0 rounded(4px) bg-gradient-to-br from-violet-500 to-blue-500` —— 同渐变作小色块（无 Bot 图标）

## 核心代码

```tsx
const BRAND: Record<string, { label: string; cls: string }> = {
  deepseek: { label: 'DS', cls: 'bg-blue-50 text-blue-600 ring-blue-100' },
  qwen:     { label: '通', cls: 'bg-violet-50 text-violet-600 ring-violet-100' },
  openai:   { label: 'AI', cls: 'bg-emerald-50 text-emerald-600 ring-emerald-100' },
  'new-api':{ label: '⇄', cls: 'bg-primary-50 text-primary-600 ring-primary-100' },
  dify:     { label: 'Di', cls: 'bg-indigo-50 text-indigo-600 ring-indigo-100' },
  fastgpt:  { label: 'FG', cls: 'bg-cyan-50 text-cyan-600 ring-cyan-100' },
  coze:     { label: 'Cz', cls: 'bg-amber-50 text-amber-600 ring-amber-100' },
};
const SIZE = { sm: 'h-8 w-8 text-[11px]', md: 'h-10 w-10 text-[13px]' };

export const ProviderAvatar = ({ code, size = 'sm' }) => {
  const key = (code || '').toLowerCase().replace(/__deleted.*/, '');
  const brand = BRAND[key] ?? (key ? { label: key.slice(0,2).toUpperCase(), cls: FALLBACK.cls } : FALLBACK);
  return (
    <div className={cn('flex shrink-0 items-center justify-center rounded-lg font-semibold ring-1 ring-inset', SIZE[size], brand.cls)}>
      {brand.label}
    </div>
  );
};

// 渐变 Bot 头像（playground AI 消息）
<div className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-violet-500 to-blue-500 text-white">
  <Bot className="h-3.5 w-3.5" />
</div>
```

lucide：Bot。

## 适配指南

- provider 头像用真实 provider code 选品牌色——`new-api`/`oneapi` 走 `⇄`（中转网关语义），不要给具体厂商图标
- 未知 code 务必回退首两字母 + 中性色，**不要**裸字符串溢出
- AI bot 渐变头像在消息气泡用 `h-6 w-6` 圆形 + Bot 图标；对比列头空间紧用 `h-4 w-4` 圆角小色块（去掉图标）
- 品牌 ring 用 `ring-1 ring-inset` 100 系——浅描边而非粗框

## 反模式

- ❌ 所有 provider 共用一个灰云图标——失去可扫性（这是本条存在的理由）
- ❌ 渐变方向乱写——固定 `bg-gradient-to-br from-violet-500 to-blue-500`（左上→右下 violet→blue）
- ❌ Bot 图标用 emoji 🤖——用 lucide Bot
- ❌ 品牌头像用饱和实心底（bg-blue-600）——用 50 系浅底 + 600 字 + 100 ring，工程克制
