---
id: components/buttons/acme/ghost-button
type: component
name: 幽灵按钮
description: 幽灵按钮——透明底 + 1px 描边，只在 hover 时显色
platforms: [web]
theme: both
tags:
  aesthetic: [minimal, industrial]
  mood: [calm, serious]
  stack: [react-antd-tailwind, html-tailwind]
uses:
  - tokens/palettes/acme/slate-cyan-ice
preview: /preview/components/buttons/acme/ghost-button
---

# Ghost Button

> 低饱和强克制的次要操作按钮

## 视觉特征

透明背景、1px 描边、hover 填色但保持低饱和。和 solid primary 成对使用——
primary 承载主 CTA，ghost 承载次要/取消/探索型操作。

## 核心代码

```tsx
import clsx from 'clsx';

type Props = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  size?: 'sm' | 'md' | 'lg';
};

export function GhostButton({ className, size = 'md', ...rest }: Props) {
  return (
    <button
      className={clsx(
        'border transition-colors duration-150',
        'border-slate-600 text-slate-200',
        'hover:bg-slate-800 hover:border-slate-400',
        'active:bg-slate-700',
        'disabled:opacity-40 disabled:cursor-not-allowed',
        {
          'px-3 py-1 text-sm rounded': size === 'sm',
          'px-4 py-2 text-base rounded': size === 'md',
          'px-6 py-3 text-lg rounded': size === 'lg',
        },
        className,
      )}
      {...rest}
    />
  );
}
```

## 适配指南

- 颜色从 `uses` 的 slate-cyan-ice 取值；若改其他 palette，对应替换 border/text hover 色
- 动效 150ms 冷感（与 slate-cyan-ice 的低饱和一致）
- focus ring：hover/active 已覆盖；如需 a11y focus ring，自加 `focus:ring-2 focus:ring-cyan-400`

## 反模式

- 别填实色（即使 hover 也不要全填），破坏 ghost 语义
- 别加圆角 > 4px（破坏冷感）
- 别做阴影 hover
