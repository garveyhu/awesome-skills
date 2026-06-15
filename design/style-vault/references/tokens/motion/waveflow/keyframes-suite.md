---
id: tokens/motion/waveflow/keyframes-suite
type: token
name: Waveflow 七 keyframe 动效套件
description: accordion-down/up + decor-drift-1/2/3 + ping-soft + global-progress + boot-dot + shimmer + Tailwind animate-* 的全套 CSS keyframes
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, industrial]
  mood: [calm]
  stack: [shadcn-radix]
uses: []
preview: /preview/tokens/motion/waveflow/keyframes-suite
---

# Waveflow Keyframes Suite

> waveflow 全部自定义 CSS 动画的总集——9 个 keyframe，覆盖：手风琴展开、登录浮件漂浮 ×3、状态点呼吸、全局顶部进度条、启动 loading 点、骨架 shimmer。所有声明在 `src/styles/global.css`，整站走 Tailwind `animate-*` 语义触发。

## Tokens

```json
{
  "accordion-down": {
    "duration": "0.2s ease-out",
    "css": "from { height: 0 } to { height: var(--radix-accordion-content-height) }",
    "用法": "Radix Accordion data-state=open 时（@theme: --animate-accordion-down）"
  },
  "accordion-up": {
    "duration": "0.2s ease-out",
    "css": "from { height: var(--radix-accordion-content-height) } to { height: 0 }"
  },
  "decor-drift-1": {
    "duration": "6-7s ease-in-out infinite",
    "css": "0,100% { translate: 0 0 } 50% { translate: 0 -12px }",
    "用法": "登录左侧装饰圆点 / 同心圆（用 CSS Level 4 独立 translate 属性，避免被 JS transform 视差覆盖）"
  },
  "decor-drift-2": {
    "duration": "8s ease-in-out infinite",
    "css": "0,100% { translate: 0 0; rotate: 0deg } 50% { translate: 0 -8px; rotate: 8deg }",
    "用法": "登录左侧圆角方"
  },
  "decor-drift-3": {
    "duration": "9s ease-in-out infinite",
    "css": "0,100% { translate: 0 0; rotate: 45deg } 50% { translate: 0 -14px; rotate: 50deg }",
    "用法": "登录左侧三角"
  },
  "ping-soft": {
    "duration": "2s ease-in-out infinite",
    "css": "0,100% { opacity: 1 } 50% { opacity: 0.6 }",
    "用法": "状态点呼吸（.pulse-soft）"
  },
  "global-progress": {
    "duration": "1.1s ease-in-out infinite",
    "css": "0% { transform: translateX(-100%) } 100% { transform: translateX(100%) }",
    "用法": "顶部 2px indeterminate progress bar"
  },
  "boot-dot": {
    "duration": "1s infinite (3 dot 0/-0.16s/-0.32s delay)",
    "css": "0,80,100% { opacity:0.4; transform: scale(0.5) } 40% { opacity:1; transform:scale(1) }",
    "用法": "全屏启动 loading 三点 ·· ·· ·"
  },
  "shimmer": {
    "duration": "1.6s ease-in-out infinite",
    "css": "0% { background-position: -200px 0 } 100% { background-position: 200px 0 }",
    "用法": ".skeleton 类 · DataTable 8 行延迟 200ms shimmer 骨架"
  },
  "tailwind-animate": {
    "animate-pulse": "Radix Dialog/Select/Popover/Tooltip 配合 data-state",
    "animate-spin":  "Loader2 / RefreshCw spinning",
    "animate-ping":  "Topbar 在线 dot 外层涟漪"
  }
}
```

## 视觉特征

- **decor-drift 用 CSS L4 `translate` / `rotate` 独立属性**：和 transform 解耦，所以 React refs 在 JS 里设 transform 不会冲突——这是 LeftDecor.tsx 浮件能漂的关键技术
- **global-progress 单层渐变带**：transparent → blue-500 (40%) → blue-600 (60%) → transparent，1.1s 全幅穿过，**不是循环 push 多带**——只用一条带子穿来穿去
- **shimmer 不是改 opacity**：是改 `background-position` 让暖灰渐变 `linear-gradient(90deg, #ebe9e3, #f5f4ee 50%, #ebe9e3)` 移动 —— 比 `animate-pulse` 更"高级"
- **ping-soft 比 animate-pulse 慢**：2s 而非默认 1s——更"安静"的呼吸

## 适配指南

- 应用 keyframe：`className="animate-pulse"` 走 Tailwind；自定义 keyframe 用 `style={{ animation: 'decor-drift-1 7s ease-in-out infinite' }}`
- Tailwind v4 注入：`@theme { --animate-accordion-down: accordion-down 0.2s ease-out }`
- shimmer 用法：把元素加 `.skeleton` 类，自带渐变 + 动画

## 反模式

- ❌ 用 `transform: translate(...)` 而不是 CSS L4 `translate:` —— LeftDecor 视差会冲突
- ❌ 给登录浮件加快漂浮（< 5s）——会让用户分神
- ❌ 给 admin 主体加 decor-drift 系列——这是登录专属语言
