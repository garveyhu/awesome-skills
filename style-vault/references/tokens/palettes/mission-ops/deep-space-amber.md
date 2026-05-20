---
id: tokens/palettes/mission-ops/deep-space-amber
type: token
name: 深空琥珀
description: 4 层深蓝黑背景递进 + 全息绿 / 琥珀 / 玫瑰红状态色 + 4 级中性文本，NASA MOCR / Bloomberg Terminal 工程屏调色板
platforms: [web]
theme: dark
tags:
  aesthetic: [industrial, editorial]
  mood: [cold, serious]
  stack: [html-tailwind, react-tailwind]
preview: /preview/tokens/palettes/mission-ops/deep-space-amber
---

# Deep Space Amber

> 4 层深蓝黑递进底 + 全息绿主色 + 琥珀警告 + 玫瑰红 fail，工程控制屏标准配色

## 视觉特征

- **底色 4 层递进**：从 `#070a12`（页面底）到 `#121a2c`（panel 高亮），1px 一档，靠层次而非边框分隔
- **4 级中性文本**：96% / 62% / 38% / 22% rgba 白，给信息密度让路
- **状态色严格语义化**：每色绑死含义，不混用
  - `ok #34d399` 健康（兼 secondary `ok2 #00ff9d` 给极亮态）
  - `info #22d3ee` 中性数据 / 提示
  - `warn #fbbf24` 警告（兼 `warn2 #fb923c` 偏橙）
  - `fail #fb7185` 玫瑰红，告警
  - `purple #a78bfa` 特殊业务 / CDC 等非同步源
  - `mute #94a3b8` 已禁用 / 离线
- **加重色** `amber #f59e0b` / `green #22c55e` / `crit #ef4444` 用于强调态（如告警 banner / 关键 KPI delta）
- **极淡 grid 线** `rgba(120,180,255,0.04-0.075)`，给"工程图纸"感而不抢内容

## Tokens

```json
{
  "bg": {
    "page":    "#070a12",
    "panel-1": "#0a0e1a",
    "panel-2": "#0d1320",
    "panel-3": "#121a2c"
  },
  "text": {
    "1": "rgba(255,255,255,0.96)",
    "2": "rgba(255,255,255,0.62)",
    "3": "rgba(255,255,255,0.38)",
    "4": "rgba(255,255,255,0.22)"
  },
  "line": {
    "1": "rgba(255,255,255,0.07)",
    "2": "rgba(255,255,255,0.12)",
    "3": "rgba(255,255,255,0.22)"
  },
  "grid": {
    "1": "rgba(120,180,255,0.04)",
    "2": "rgba(120,180,255,0.075)"
  },
  "state": {
    "ok":    "#34d399",
    "ok2":   "#00ff9d",
    "info":  "#22d3ee",
    "warn":  "#fbbf24",
    "warn2": "#fb923c",
    "fail":  "#fb7185",
    "purple":"#a78bfa",
    "mute":  "#94a3b8"
  },
  "accent": {
    "amber": "#f59e0b",
    "green": "#22c55e",
    "crit":  "#ef4444"
  }
}
```

## 适配指南

- 如果是 React + Tailwind，用 `tailwind.config` 的 `theme.extend.colors` 把上面 token 落到 `bg.page` / `text.1` 等命名空间
- 单文件 HTML 用 CSS 变量定义在 `:root`
- **底色 4 层不能省**——少一层信息层次会塌；少了就退化成普通暗色 admin

## 反模式

- 不要把状态色泛用做装饰色（fail 红不能拿来做"重要"emphasis）
- 不要加第 5 种 accent 颜色——本调色板的"工程感"靠的是颜色克制
- 不要把 fail/warn 的明度提到主文本级别（96%），那是中性文本专属
