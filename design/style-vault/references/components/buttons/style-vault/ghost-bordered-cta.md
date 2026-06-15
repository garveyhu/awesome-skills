---
id: components/buttons/style-vault/ghost-bordered-cta
type: component
name: 描边幽灵 CTA
description: border-[1.5px] border-slate-300 + rounded-lg + hover 收紧到 slate-900 的次操作按钮
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind, html-tailwind]
uses:
  - tokens/palettes/style-vault/slate-cyan-cool
  - tokens/motion/style-vault/editorial-flow
preview: /preview/components/buttons/style-vault/ghost-bordered-cta
---

# Ghost Bordered CTA

> Style Vault 的次要 CTA：白底 + 1.5px 描边 + rounded-lg + hover 收紧描边和字色到 slate-900

## 视觉特征

- 底色 `bg-white`，描边 `border-[1.5px] border-slate-300` —— 1.5px 比 1px 厚一档，避免在白底上消失
- 字色 `text-slate-700`（默认）→ `text-slate-900`（hover）
- hover 状态 **同时切两件事**：描边色 `border-slate-300 → border-slate-900` + 字色 `text-slate-700 → text-slate-900` —— 实现"线条收紧"的视觉
- 形状 `rounded-lg`（8px）—— 跟 dark-pill-cta 的 `rounded-full` 形成"主圆 / 次方"区分
- icon 走 `text-[13px]`，常配 `CopyOutlined` / `EditOutlined` 这种描线图标

## 与同 bucket 区分

- **vs `components/buttons/style-vault/dark-pill-cta`**：dark 是主 action（rounded-full 胶囊 + 实色填充）；ghost 是次要 action（rounded-lg + 描边）。同屏配对：1 dark + N ghost
- **vs `components/buttons/acme/ghost-button`**（slate-700 描边 + 暗底）：那条用在暗色面板；本条专为 light 浅底站

## 核心代码

```tsx
import clsx from 'clsx';

interface GhostBorderedCtaProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  fullWidth?: boolean;
  icon?: React.ReactNode;
}

export function GhostBorderedCta({
  className,
  fullWidth,
  icon,
  children,
  ...rest
}: GhostBorderedCtaProps) {
  return (
    <button
      {...rest}
      className={clsx(
        'inline-flex items-center justify-center gap-2 rounded-lg',
        'border-[1.5px] border-slate-300 bg-white px-4 py-2',
        'text-[13px] font-medium text-slate-700',
        'transition-colors duration-200 hover:border-slate-900 hover:text-slate-900',
        'disabled:cursor-not-allowed disabled:opacity-50',
        fullWidth && 'w-full',
        className,
      )}
    >
      {icon && <span className="text-[13px]">{icon}</span>}
      {children}
    </button>
  );
}
```

## 适配指南

- 经典场景：复制 / 编辑 / 取消 / 浏览跳转 —— 这些**没有"提交"语义**的次要操作
- 用 `fullWidth` 撑满列宽（如 DetailPage 左列"复制 Prompt"按钮）
- 在 toolbar 里跟其它 ghost 并排时按 8px gap 排列；不要混入 dark-pill

## 反模式

- 不要把描边换成 1px——会被白底吞掉
- 不要 hover 时 fill 颜色（变成 dark-pill 同款会破坏分级）
- 不要圆角到 rounded-full（变成第二种主 CTA）
- 不要给 disabled 用灰底——保持白底 + 半透明描边
