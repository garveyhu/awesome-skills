---
id: tokens/motion/sage/animate-in-suite
type: token
name: 动效入场套件
description: tailwindcss-animate 提供的 fade-in / zoom-in / slide-in 标准过渡集合，sage 整站弹层入场基线
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm]
  stack: [react-antd-tailwind]
uses: []
preview: /preview/tokens/motion/sage/animate-in-suite
---

# Sage Animate-In Suite

> sage 弹层入场不写 framer-motion——直接用 `tailwindcss-animate` 的 `animate-in` 工具类。简单、零运行时成本、和 Tailwind 系统对齐。整站出现 10 处。

## Tokens

```json
{
  "presets": {
    "menuPop": {
      "classes": "animate-in fade-in zoom-in-95 duration-100",
      "use": "会话 hover 操作菜单 / chat header more menu"
    },
    "userMenuRise": {
      "classes": "animate-in fade-in slide-in-from-bottom-4 zoom-in-95 duration-300 ease-out origin-bottom",
      "use": "侧栏底部用户菜单展开"
    },
    "languagePop": {
      "classes": "animate-in fade-in slide-in-from-left-2 duration-150",
      "use": "语言选择 portal"
    },
    "modalFade": {
      "classes": "animate-in fade-in duration-200",
      "use": "全屏 backdrop overlay 入场"
    }
  },
  "primitives": {
    "spin":  "animate-spin (1s linear infinite · 通用 RefreshCw / Spin)",
    "pulse": "animate-pulse (2s · 停止生成按钮外发光)",
    "ping":  "animate-ping (1s · 停止生成按钮 ring)"
  },
  "duration": {
    "fast":      100,
    "interactive": 150,
    "default":   200,
    "stately":   300
  },
  "easing": {
    "default": "cubic-bezier(0.4, 0, 0.2, 1)",
    "out":     "cubic-bezier(0, 0, 0.2, 1)"
  }
}
```

## 视觉特征

- 入场以 100ms / 200ms / 300ms 三档递进——越大的弹层用越慢的 duration
- `zoom-in-95`（从 0.95 缩放到 1）+ `fade-in` 是 sage 弹层标配组合，比纯 fade 更"立体"
- 用户菜单 300ms + `slide-in-from-bottom-4 origin-bottom`——让菜单看起来"从用户头像底部弹出来"
- 没有 bounce / 没有 spring——气质偏克制理性

## 适配指南

- 直接拼 className：`<div className="animate-in fade-in zoom-in-95 duration-100">`
- 配合条件渲染：`{isOpen && <div className="animate-in ...">...</div>}`，卸载时不动画（acceptable）
- 复杂 keyframes（雪花 / 流光 / 雪人）改走 `tokens/motion/sage/styled-keyframes`

## 反模式

- ❌ 入场超过 300ms —— sage 整体节奏要快
- ❌ 用 `animate-bounce` —— 气质不符
