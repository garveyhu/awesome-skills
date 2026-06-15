---
id: components/typography-atoms/waveflow/kbd-key-cap
type: component
name: 键帽 Kbd
description: padding 1px 5px + 10px mono + 1px stone-200 border + 1px shadow 模拟物理键帽
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, industrial]
  mood: [serious]
  stack: [shadcn-radix]
uses:
  - tokens/iconography/waveflow/engineer-detail-classes
preview: /preview/components/typography-atoms/waveflow/kbd-key-cap
---

# Waveflow Kbd Key Cap

> 键盘按键的视觉标记——padding 1px 5px、10px mono、stone-200 1px border + 底部 1px shadow 模拟键帽轻微立体感。整站只在 4 处出现：Topbar ⌘K / SearchPanel footer ↑ ↓ ↵ ⌘↵ ESC 提示。

## 视觉特征

- **底层走 `.kbd` 全局 CSS 类**（global.css 声明）：
  ```css
  padding: 1px 5px;
  font-family: var(--font-mono);
  font-size: 10px;
  color: #78716c;
  background: #fff;
  border: 1px solid #e7e5e0;
  border-radius: 4px;
  box-shadow: 0 1px 0 #e7e5e0;
  ```
- **React wrapper**：`<Kbd className={cn('kbd', className)}>{children}</Kbd>`——只是一个 span 套 `.kbd`
- **font-size 10px**：极小，但 mono 字形保证可读
- **底部 1px shadow** = 同色 stone-200 —— 模拟键帽下沿，**不**做 box-shadow blur

## 核心代码

```tsx
export const Kbd = ({ className, children }: { className?: string; children: React.ReactNode }) => (
  <span className={cn('kbd', className)}>{children}</span>
);

// 用法
<Kbd>⌘K</Kbd>
<Kbd>↑</Kbd> <Kbd>↓</Kbd> 导航
<Kbd>ESC</Kbd>
```

## 适配指南

- 永远成对出现（"⌘ K" 通常是 `<Kbd>⌘</Kbd><Kbd>K</Kbd>` 两片）—— 不要合一个 `⌘K` 让符号挤
- 多键 + 文字说明：`<span className="flex items-center gap-1.5"><Kbd>↑</Kbd><Kbd>↓</Kbd> 导航</span>` —— gap-1.5 与文字呼吸
- 不依赖 lucide icon——直接用 unicode ⌘ ↑ ↓ ↵ ESC ⌃ ⇧ ⌥

## 反模式

- ❌ 用 `<code>` 替代——失去键帽立体感
- ❌ font-size 14px+ —— 看起来像标签而不是键
- ❌ 加 box-shadow blur 大于 1px —— 显廉价
