---
id: components/buttons/acme/cyan-cta
type: component
name: 青蓝主 CTA
description: cyan-400 实色填充 + 黑字的主操作按钮，与 acme/ghost-button 配对成 primary/secondary
platforms: [web]
theme: dark
tags:
  aesthetic: [minimal, industrial]
  mood: [cold, serious]
  stack: [react-antd-tailwind, html-tailwind]
uses:
  - tokens/palettes/acme/slate-cyan-ice
  - tokens/motion/acme/instant-snap
preview: /preview/components/buttons/acme/cyan-cta
---

# Cyan CTA

> 冷感工业风格的主 CTA：cyan-400 实色 + 黑字 + 4px 圆角 + 150ms ease-out。

## 视觉特征

- 底色 `#22d3ee`（slate-cyan-ice 的 accent.base）；hover `#06b6d4`；active `#0891b2`
- 字色 `#0f172a` slate-950（黑字反白）；字重 500
- 圆角 4px，**绝不**圆角化更大
- padding 三档：sm `px-3 py-1.5` · md `px-4 py-2` · lg `px-6 py-2.5`
- transition 150ms ease-out，仅 background-color，**不做 transform**
- focus ring `outline: 2px solid #22d3ee; outline-offset: 2px`

**与 components/buttons/acme/ghost-button 配对**：cyan-cta 承载 primary action（确认 / 提交 / 启动），ghost-button 承载 secondary（取消 / 探索）。**与 components/buttons/skillhub/dark-primary-cta 区分**：那条是黑底 + scale-95 回弹（社区暖调），本条是 cyan 实色 + 无 scale（冷感工业）。

## 核心代码

```tsx
import clsx from 'clsx';

type Size = 'sm' | 'md' | 'lg';

interface CyanCtaProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  size?: Size;
}

const sizeCls: Record<Size, string> = {
  sm: 'px-3 py-1.5 text-xs',
  md: 'px-4 py-2 text-sm',
  lg: 'px-6 py-2.5 text-base',
};

export function CyanCta({ className, size = 'md', children, ...rest }: CyanCtaProps) {
  return (
    <button
      {...rest}
      className={clsx(
        'inline-flex items-center justify-center gap-1.5 rounded font-medium',
        'bg-cyan-400 text-slate-950',
        'hover:bg-cyan-300 active:bg-cyan-500',
        'transition-colors duration-150 ease-out',
        'focus:outline focus:outline-2 focus:outline-cyan-400 focus:outline-offset-2',
        'disabled:bg-slate-700 disabled:text-slate-500 disabled:cursor-not-allowed',
        sizeCls[size],
        className,
      )}
    >
      {children}
    </button>
  );
}
```

## 适配指南

- 全站同屏 1 个 cyan-cta + N 个 ghost-button —— 不要并列两个 cyan
- 不要给 cyan-cta 加 icon-only 形态——`status-pulse` / 状态指示已经承担"图标 + 颜色"的语义
- 字体走 IBM Plex Sans（继承全局 `--font-sans`）；**不要**为 CTA 单独切到 mono
- 暗底面板上直接放；浅底（罕见）上要求外加 1px slate-700 描边以保对比

## 反模式

- 不要圆角 > 4px
- 不要加 scale / shadow / glow
- 不要做 gradient 填充——破坏冷感单色逻辑
- 不要 hover 变化字色——只切背景饱和度
