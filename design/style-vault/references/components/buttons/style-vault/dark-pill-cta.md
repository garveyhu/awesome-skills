---
id: components/buttons/style-vault/dark-pill-cta
type: component
name: 深色胶囊主 CTA
description: rounded-full bg-slate-900 + 深柔投影 + ArrowRight 位移的主操作按钮
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind, html-tailwind]
uses:
  - tokens/palettes/style-vault/slate-cyan-cool
  - tokens/motion/style-vault/editorial-flow
preview: /preview/components/buttons/style-vault/dark-pill-cta
---

# Dark Pill CTA

> Style Vault 的主操作按钮：slate-900 实色 + rounded-full 全圆角 + 深向投影 + 末尾箭头位移

## 视觉特征

- 底色 `bg-slate-900` (#0f172a)；hover `bg-slate-700` (#334155)；**绝不**走 cyan 实色（cyan 是装饰色，不是 action 色）
- 字色 `text-white`，字重 500，正文 13-15px（normal/large 双档）
- 形状 `rounded-full` 全胶囊——和 ghost-bordered-cta 的 `rounded-lg` 形成"主圆 / 次方"对比
- 深向投影 `shadow-[0_20px_48px_-20px_rgba(15,23,42,0.6)]`——大尺寸 normal 档；small 档无投影
- 末尾 `ArrowRightOutlined` group-hover 时 `translate-x-1`——CTA 招手感来自这个 1px 微动
- 高度三档：sm `h-9 px-5`（TopBar 登录用）· md `h-10 px-5`（ProductDetail 用）· lg `h-14 px-9`（HomePage hero 用，附深投影）

## 与同 bucket 区分

- **vs `components/buttons/acme/cyan-cta`**（cyan-400 实色 + 4px 圆角）：那条是冷工业 dark theme 主 CTA；本条是 light theme 浅底站的对应位
- **vs `components/buttons/skillhub/dark-primary-cta`**（slate-900 + active scale-95）：那条带回弹（社区暖调）；本条**绝不 scale**——只切背景色

## 核心代码

```tsx
import clsx from 'clsx';
import { ArrowRightOutlined } from '@ant-design/icons';

type Size = 'sm' | 'md' | 'lg';

interface DarkPillCtaProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  size?: Size;
  withArrow?: boolean;
}

const sizeCls: Record<Size, string> = {
  sm: 'h-9 px-5 text-[13px]',
  md: 'h-10 px-5 text-[13px]',
  lg: 'h-14 px-9 text-[15px] shadow-[0_20px_48px_-20px_rgba(15,23,42,0.6)]',
};

export function DarkPillCta({
  className,
  size = 'md',
  withArrow = true,
  children,
  ...rest
}: DarkPillCtaProps) {
  return (
    <button
      {...rest}
      className={clsx(
        'group inline-flex items-center justify-center gap-2 rounded-full',
        'bg-slate-900 text-white font-medium',
        'transition-colors duration-200 hover:bg-slate-700',
        sizeCls[size],
        className,
      )}
    >
      {children}
      {withArrow && (
        <ArrowRightOutlined className="transition group-hover:translate-x-1" />
      )}
    </button>
  );
}
```

## 适配指南

- 全站同屏 1 个 dark-pill-cta + N 个 ghost-bordered-cta —— 不要并列两个 dark
- hero 用 lg 档（大投影），常规 toolbar 用 md，TopBar / 紧凑场景用 sm
- 暗底面板上要切到反相版（`bg-white text-slate-900` 同样 rounded-full），保对比

## 反模式

- 不要圆角降到 `rounded-lg`/`rounded-md`——破坏"胶囊主圆"形态
- 不要加 transform: scale 或 active:scale —— editorial-flow motion 系统不允许
- 不要把 hover 切成 cyan—— cyan 是装饰色，不是 action 色
- 不要在 hero 用 sm 档——失重
