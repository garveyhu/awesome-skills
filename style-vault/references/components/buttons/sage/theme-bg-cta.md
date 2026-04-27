---
id: components/buttons/sage/theme-bg-cta
type: component
name: 主题色主按钮
description: 用 ${themeClasses.bg} ${themeClasses.bgHover} 动态着色的圆/方角主按钮，整站发送 / 提交 / 主操作
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/sage/twelve-theme-spectrum
preview: /preview/components/buttons/sage/theme-bg-cta
---

# Theme Bg CTA

> sage 整站的主操作按钮——用户当前主题色作底，hover 加深一档。圆形（chat 发送）和方形（form 提交）两种形态。

## 视觉特征

- 圆形：`w-8 h-8 ${themeClasses.bg} ${themeClasses.bgHover} text-white rounded-full disabled:opacity-40 disabled:cursor-not-allowed transition-colors`
- 方形：`px-4 py-2 ${themeClasses.bg} ${themeClasses.bgHover} text-white rounded-lg font-medium transition-colors`
- 大尺寸（登录页 submit）：`w-full bg-emerald-600 text-white py-2 rounded-lg hover:bg-emerald-700 ... flex items-center justify-center gap-2`（注：登录页特意用 emerald 固定色而非 themeClasses，因为登录前还没主题）
- icon-leading：`<Icon size={16-18} className="-ml-0.5 mt-0.5" />` + 文字
- disabled 态用 `disabled:opacity-40 disabled:cursor-not-allowed`，不变色不变形

## 核心代码

```tsx
import { THEME_CLASSES, type ThemeColor } from '@/core/utils/themeUtils';
import { Send } from 'lucide-react';

export function ThemeBgCta({
  themeColor = 'gray',
  shape = 'circle',
  disabled,
  children,
  onClick,
}: {
  themeColor?: ThemeColor;
  shape?: 'circle' | 'rect';
  disabled?: boolean;
  children?: React.ReactNode;
  onClick?: () => void;
}) {
  const tc = THEME_CLASSES[themeColor];
  if (shape === 'circle') {
    return (
      <button
        onClick={onClick}
        disabled={disabled}
        className={`w-8 h-8 flex items-center justify-center ${tc.bg} ${tc.bgHover} text-white rounded-full disabled:opacity-40 disabled:cursor-not-allowed transition-colors`}
      >
        <Send size={16} className="-ml-0.5 mt-0.5" />
      </button>
    );
  }
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`px-4 py-2 ${tc.bg} ${tc.bgHover} text-white rounded-lg font-medium transition-colors disabled:opacity-40`}
    >
      {children}
    </button>
  );
}
```

## 适配指南

- 切换主题不需要改组件——`themeColor` 从 `useOutletContext()` 取
- 登录前的 submit 按钮坚持 emerald 硬编码（`bg-emerald-600 hover:bg-emerald-700`），因为用户尚未登录无 themeColor
- 删除按钮例外：用 `bg-red-600 hover:bg-red-700`，永远红色不走主题

## 反模式

- ❌ 写 `bg-${color}-500` 动态拼接 —— Tailwind JIT 不识别，必须查表
- ❌ 给 disabled 加 grayscale —— sage 用 opacity-40 保留主题感
