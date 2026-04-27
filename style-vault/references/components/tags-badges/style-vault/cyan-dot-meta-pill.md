---
id: components/tags-badges/style-vault/cyan-dot-meta-pill
type: component
name: Cyan Dot Meta Pill
description: 圆角胶囊 + cyan 小圆点 + uppercase tracking caption 的元信息标签
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind, html-tailwind]
uses:
  - tokens/palettes/style-vault/slate-cyan-cool
  - tokens/typography/pairs/style-vault/inter-editorial-display
preview: /preview/components/tags-badges/style-vault/cyan-dot-meta-pill
---

# Cyan Dot Meta Pill

> 编辑感的元信息胶囊：白底 + 1.5×1.5px cyan 圆点 + 11px uppercase tracking-[0.22em] 文字

## 视觉特征

- 形态 `rounded-full border border-slate-200 bg-white/85 backdrop-blur-sm` —— 玻璃感淡描边胶囊
- 内容三段：`cyan-500` 小圆点 + 文本 + 可选 separator
  - 圆点 `h-1.5 w-1.5 bg-cyan-500 rounded-full`
  - 文字 `text-[11px] font-medium uppercase tracking-[0.22em] text-slate-500`
- padding `px-3 py-1`，整体高度紧凑（≈26px）
- 通常出现在 **section kicker 位置**：HomePage hero "STYLE VAULT · 风格库"、ProductDetail hero "产品 · 设计"
- 在产品列表场景里，cyan 圆点会被 **category-dot 替换**（productivity=purple / design=indigo / ...）—— 圆点颜色随 category 切，胶囊壳不变

## 与同 bucket 区分

- **vs `components/tags-badges/skillhub/teal-pill`**（teal 实色填充胶囊 + 白字）：那条是醒目分类标签；本条是低调元信息 kicker，几乎不抢戏

## 核心代码

```tsx
import clsx from 'clsx';

interface CyanDotMetaPillProps {
  dotColor?: string; // 默认 cyan-500，category 场景会传 categoryDot()
  children: React.ReactNode;
  className?: string;
}

export function CyanDotMetaPill({
  dotColor = '#06b6d4',
  children,
  className,
}: CyanDotMetaPillProps) {
  return (
    <span
      className={clsx(
        'inline-flex items-center gap-2 rounded-full',
        'border border-slate-200 bg-white/85 backdrop-blur-sm',
        'px-3 py-1',
        'text-[11px] font-medium uppercase tracking-[0.22em] text-slate-500',
        className,
      )}
    >
      <span
        className="h-1.5 w-1.5 rounded-full"
        style={{ background: dotColor }}
      />
      {children}
    </span>
  );
}
```

## 适配指南

- 用作 hero kicker、section eyebrow，**不要**用于按钮 / 链接（无交互态）
- 文字一律 uppercase + tracking-[0.22em]，配 `font-medium` 保稳重；**不要**改成 sentence-case
- 在 dark panel 上用时把胶囊改成 `bg-white/10 border-white/20 text-slate-300`
- 圆点颜色按场景：默认 cyan / 在 category 列表场景传 category dot / 在 type 列表场景传 type dot

## 反模式

- 不要把 `bg-white/85` 改成 `bg-white` 实白—— blur 玻璃感来自半透
- 不要去掉 `backdrop-blur-sm`——hero 上叠 blob 时玻璃感是定身份的
- 不要把字号撑到 13px+——会跟 caption 体系打架
- 不要把圆点撑到 ≥ 6px——会变成 type-dot 风格抢视觉
