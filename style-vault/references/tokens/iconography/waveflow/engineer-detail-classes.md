---
id: tokens/iconography/waveflow/engineer-detail-classes
type: token
name: 工程师细节类合集
description: .tnum / .kbd / .status-dot[-running/-stopped/-error] / .tree-line / .tree-item / .skeleton / .pulse-soft 全局工程师感细节类
platforms: [web]
theme: light
tags:
  aesthetic: [industrial, minimal]
  mood: [serious, calm]
  stack: [shadcn-radix]
uses:
  - tokens/motion/waveflow/keyframes-suite
preview: /preview/tokens/iconography/waveflow/engineer-detail-classes
---

# Waveflow Engineer Detail Classes

> waveflow 全局 CSS 里**不走 Tailwind** 的工程师小细节类合集——直接在 global.css 声明，整站文件随处用。每个都是 1-3 行 CSS，但加起来构成了 waveflow"工程师感"的底色。

## Tokens

```json
{
  ".tnum": {
    "font-variant-numeric": "tabular-nums",
    "用途": "所有数字必加：表格 ID 列 / cron / 时间 / KPI 大数字 / kbd / count chip"
  },
  ".kbd": {
    "padding": "1px 5px",
    "font-family": "var(--font-mono)",
    "font-size": "10px",
    "color": "#78716c",
    "background": "#fff",
    "border": "1px solid #e7e5e0",
    "border-radius": "4px",
    "box-shadow": "0 1px 0 #e7e5e0",
    "用途": "Topbar ⌘K / SearchPanel 底部 ↑↓↵ 提示"
  },
  ".status-dot": {
    "display": "inline-block",
    "width": "7px",
    "height": "7px",
    "border-radius": "50%"
  },
  ".status-dot-running": {
    "background": "#10b981",
    "box-shadow": "0 0 0 2px rgb(16 185 129 / 15%)"
  },
  ".status-dot-stopped": {
    "background": "#d6d3d1",
    "(没有 ring，因 stopped 是默认态)": null
  },
  ".status-dot-error": {
    "background": "#ef4444",
    "box-shadow": "0 0 0 2px rgb(239 68 68 / 18%)"
  },
  ".pulse-soft": {
    "animation": "ping-soft 2s ease-in-out infinite"
  },
  ".skeleton": {
    "background": "linear-gradient(90deg, #ebe9e3 0%, #f5f4ee 50%, #ebe9e3 100%)",
    "background-size": "400px 100%",
    "animation": "shimmer 1.6s ease-in-out infinite"
  },
  ".tree-line": {
    "position": "relative",
    "::before": "absolute top 0 bottom 0 left 14px width 1px background #d6d3d1"
  },
  ".tree-item": {
    "position": "relative",
    "::before": "absolute top 50% left 14px width 10px height 1px background #d6d3d1"
  }
}
```

## 视觉特征

- **`.status-dot` 7px + 2px ring 15% alpha**：是 waveflow 状态语言的根。running 有 ring（在跑→有"动感"）、stopped 无 ring（静止→"沉默"）、error 有 ring 红 18%
- **`.tree-line + .tree-item` 是 sidebar 的招牌**：左 14px 竖线 + 右 10px 横线小钩——L 形 connector 让"父 → 子"层级一眼可读。比 indent + bullet 更"工程师"
- **`.kbd` 1px bottom shadow**：模拟键帽的轻微立体感，但没 box-shadow 那么 cartoon
- **`.skeleton` 暖灰渐变**：用 #ebe9e3 → #f5f4ee → #ebe9e3 三段，对应暖底色系——比 Tailwind `animate-pulse` 的灰色更和谐

## 适配指南

- 应用：`<span className="status-dot status-dot-running" />` 或者 `<span className="kbd">⌘K</span>`
- 数字一律：`<span className="font-mono tnum">{id}</span>`
- tree-line 嵌套：`<div className="tree-line">{children.map(c => <Link className="tree-item">...</Link>)}</div>`
- skeleton：直接给元素加 `.skeleton` 类，不需要额外 keyframe 引用

## 反模式

- ❌ 把 status-dot 做大到 10px+——会跟实心 Badge 抢主视觉
- ❌ tree-line 不配 tree-item——只有竖线没有钩子，看不出层级
- ❌ 数字不加 .tnum——表格列对齐塌
