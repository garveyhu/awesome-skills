---
id: tokens/typography/pairs/tactical-hud/orbitron-rajdhani-trio
type: token
name: Orbitron · Rajdhani · JetBrains Mono 三件套
description: HUD / 战术屏风格的三层字体——Orbitron 做品牌与大数字（未来感）、Rajdhani 做正文与中文（紧凑现代）、JetBrains Mono 做数据与代码（等宽工程）
platforms: [any]
theme: both
tags:
  aesthetic: [industrial]
  mood: [confident, cold]
  stack: [html-tailwind, react-tailwind]
preview: /preview/tokens/typography/pairs/tactical-hud/orbitron-rajdhani-trio
---

# Orbitron · Rajdhani · JetBrains Mono Trio

> 三层字体协奏：Orbitron 出未来感、Rajdhani 出紧凑现代感、JetBrains Mono 出工程感

## 三层职责

| 层 | 字体 | 用途 |
|---|------|------|
| **brand / display** | `Orbitron` 600-700 | 站名 wordmark / KPI 大数字 / `LIVE` 徽章 / 小标题 |
| **body / 中文** | `Rajdhani` 400-600 | 正文 / 中文 label / 区域名 |
| **mono / 数据** | `JetBrains Mono` 400-500 | 代码 / 数字 / 时间戳 / 搜索快捷键 |

Orbitron 是关键——它有强烈的"科幻 / 战术屏"基因，但只能用在小范围（10% 内）的"品牌点"和"大数字"上，泛用会让整个 UI 变成"游戏 UI"。

## Tokens

```css
:root {
  --font-orbi: 'Orbitron', 'Rajdhani', sans-serif;
  --font-sans: 'Rajdhani', 'PingFang SC', 'Microsoft YaHei', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', ui-monospace, Menlo, monospace;
  font-feature-settings: 'tnum' 1;
}
.orbi { font-family: var(--font-orbi); letter-spacing: 1px; }
.sans { font-family: var(--font-sans); }
.mono { font-family: var(--font-mono); font-variant-numeric: tabular-nums; }
```

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link
  href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700&family=Rajdhani:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500;600&display=swap"
  rel="stylesheet"
/>
```

## 字号 scale

| token | size | weight | font | letter-spacing | 用途 |
|---|---|---|---|---|---|
| `brand` | 15-18px | 700 | orbi | 1.5px | 站名 wordmark |
| `eyebrow` | 10-11px uppercase | 500 | orbi | 2px | 分组标题（▾ 总览 / ▾ 区域观测） |
| `kpi-num` | 32-48px | 500-700 | orbi | 0-0.5px | KPI 中央数字 |
| `data` | 13-14px | 400-500 | mono | 0.5px | 表格 / 列表数据 |
| `label` | 12-13px | 400-500 | sans | 0 | 中文标签 / body |
| `caption` | 10-11px | 400 | mono | 0.5px | 时间戳 / 副 caption |

## 适配指南

- **Orbitron 占用比例必须低**（< 10%）——它太强势，泛用会让 UI 卡通化
- 中文必须有 fallback `PingFang SC` / `Microsoft YaHei`，Rajdhani 不含中文字形
- JetBrains Mono 数字必加 `font-variant-numeric: tabular-nums`，否则位数不对齐
- `LIVE` / `OFFLINE` / `STREAMING` 这种 system 徽章用 orbi + uppercase + letter-spacing 1.5-2px

## 反模式

- 不要把正文全用 Orbitron——它的字形太宽，正文阅读吃力
- 不要给 mono 字加 italic
- 不要给 sans 上 weight 700+（Rajdhani 700 已偏粗，800 会失去"紧凑现代"感）
- 不要混入第 4 种字体（serif 一律禁止）
