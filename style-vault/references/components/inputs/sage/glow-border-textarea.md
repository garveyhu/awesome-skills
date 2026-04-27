---
id: components/inputs/sage/glow-border-textarea
type: component
name: 霓虹光晕输入框
description: rounded-[24px] textarea + 双层 box-shadow 主题色 focus 光晕，sage Chat 主输入框的灵魂
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm, dreamy]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/sage/twelve-theme-spectrum
preview: /preview/components/inputs/sage/glow-border-textarea
---

# Glow Border Textarea

> ChatInput 主输入框——`rounded-[24px]` 大圆角 + `bg-white shadow-sm` 衬底 + focus 时双层 box-shadow（4px 内层 + 15px 外层）打出主题色霓虹光晕。这种光不是 ring 也不是 border-color，而是从内向外的氛围光，是 sage 输入框的辨识符号。

## 视觉特征

- **形状**：`rounded-[24px] p-2.5 bg-white border` 自定义圆角，比 `rounded-3xl`(24px) 更精确控制
- **idle 边框**：`borderColor: '#e2e8f0'` (slate-200)
- **focus 边框**：`borderColor: '${THEME_HEX_COLORS[themeColor]}50'` (50% alpha · 半透明)
- **idle 光晕**：`boxShadow: '0 0 4px rgba(148,163,184,0.15), 0 0 15px rgba(148,163,184,0.08)'` （slate 灰晕，极淡）
- **focus 光晕**：`boxShadow: '0 0 4px ${themeHex}40, 0 0 15px ${themeHex}30'`（主题色 + 双层叠加 = 模糊光环）
- **textarea 本身**：`bg-transparent border-none focus:ring-0 outline-none px-1 py-1 text-base text-gray-800 placeholder:text-gray-400 resize-none min-h-[35px] max-h-[200px]`
- 内含 textarea 自动 resize（scroll height ≤ 200）+ overflow-y auto/hidden 切换

## 核心代码

```tsx
import { THEME_HEX_COLORS } from '@/core/utils/themeUtils';

const [isFocused, setIsFocused] = useState(false);
const themeHex = THEME_HEX_COLORS[themeColor];

<form
  onFocus={() => setIsFocused(true)}
  onBlur={() => setIsFocused(false)}
  className="relative flex flex-col gap-0 bg-white border rounded-[24px] shadow-sm transition-all p-2.5"
  style={{
    borderColor: isFocused ? `${themeHex}50` : '#e2e8f0',
    boxShadow: isFocused
      ? `0 0 4px ${themeHex}40, 0 0 15px ${themeHex}30`
      : `0 0 4px rgba(148, 163, 184, 0.15), 0 0 15px rgba(148, 163, 184, 0.08)`,
  }}
>
  <textarea
    className="w-full bg-transparent border-none focus:ring-0 outline-none px-1 py-1 text-base text-gray-800 placeholder:text-gray-400 resize-none overflow-hidden min-h-[35px] max-h-[200px]"
    placeholder="问点什么吧?"
  />
</form>
```

## 适配指南

- 注入 themeHex 用 inline style（不能走 Tailwind）—— `${color}50` / `${color}40` 这种 hex+alpha 字符串拼接 JIT 不支持
- 配合 textarea 的 auto-resize：`scrollHeight` 监听变化，撑高同时撑高 form 容器
- 双层 box-shadow 的 4px + 15px 是经验值：4px 给"边缘清晰", 15px 给"氛围晕染"

## 反模式

- ❌ 改用 `focus:ring-2 focus:ring-blue-300` Tailwind ring —— 那是硬边光，不是氛围光
- ❌ 把光晕 alpha 调到 60+ —— 显得"刺眼"，破坏氛围感
