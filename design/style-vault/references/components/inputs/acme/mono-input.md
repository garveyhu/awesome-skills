---
id: components/inputs/acme/mono-input
type: component
name: 等宽数字输入框
description: Plex Mono 字体、右对齐、cyan focus ring 的数字输入控件，用于金额 / 阈值 / 端口号
platforms: [web]
theme: dark
tags:
  aesthetic: [minimal, industrial]
  mood: [cold, serious]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/acme/slate-cyan-ice
  - tokens/typography/pairs/acme/ibm-plex-duo
preview: /preview/components/inputs/acme/mono-input
---

# Mono Input

> 数字 / 时间 / 阈值类输入字段：Plex Mono 等宽 + 右对齐 + cyan focus ring。

## 视觉特征

- 字体 IBM Plex Mono，文本右对齐（数字必须右对齐）
- 暗底面板上：底色 `#0b1220` slate-950 略深一档；border `#334155` slate-700
- focus 时 border → `#22d3ee` cyan-400，`box-shadow: 0 0 0 1px #22d3ee` 仿 ring（不要 ring-blur）
- placeholder 用 `#475569` slate-600，与正文足够对比
- 支持前缀 / 后缀（uppercase 11px caption 风）：`ms` / `req/s` / `MB` 等单位标注
- 高度 32px（紧凑）或 36px（标准）；padding `8px 12px`

## 核心代码

```tsx
import clsx from 'clsx';

interface MonoInputProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'size'> {
  size?: 'sm' | 'md';
  suffix?: string;
  prefix?: string;
}

export function MonoInput({
  className,
  size = 'md',
  suffix,
  prefix,
  ...rest
}: MonoInputProps) {
  return (
    <div
      className={clsx(
        'inline-flex items-center font-mono text-slate-100',
        'bg-slate-950 border border-slate-700 rounded',
        'focus-within:border-cyan-400 focus-within:shadow-[0_0_0_1px_#22d3ee]',
        'transition-colors duration-150 ease-out',
        size === 'sm' ? 'h-8 px-2.5' : 'h-9 px-3',
        className,
      )}
    >
      {prefix && (
        <span className="text-[11px] uppercase tracking-wider text-slate-500 mr-2">
          {prefix}
        </span>
      )}
      <input
        {...rest}
        className="flex-1 bg-transparent text-right outline-none placeholder:text-slate-600"
      />
      {suffix && (
        <span className="text-[11px] uppercase tracking-wider text-slate-500 ml-2">
          {suffix}
        </span>
      )}
    </div>
  );
}
```

## 适配指南

- 数字输入必右对齐——这是工业 SaaS 的可读性硬规则
- suffix 单位用 uppercase + tracking-wider，与 KPI grid 的 caption 同种排版语言
- 浅底（罕见）切到 `bg-white border-slate-300`，focus 仍是 cyan
- 不要给输入框加 prefix icon（如放大镜）——搜索请用专门的 `SearchInput`，那是另一个组件，不是 mono-input

## 反模式

- 不要左对齐数字——视觉错位
- 不要用 Plex Sans 替换字体——失去等宽语义
- 不要圆角 > 4px
- 不要 focus 时加 ring blur（破坏锐利感）；只用 1px 实色 box-shadow 模拟 ring
