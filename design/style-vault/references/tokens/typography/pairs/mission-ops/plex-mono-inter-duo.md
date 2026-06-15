---
id: tokens/typography/pairs/mission-ops/plex-mono-inter-duo
type: token
name: Plex Mono 主导 + Inter 双字体
description: IBM Plex Mono 主导 80%（数据 / 标签 / 编号） + Inter 副（中文与人名标签），与 ibm-plex-duo 的差异是 mono first 且用 Inter 替代 Plex Sans
platforms: [any]
theme: both
tags:
  aesthetic: [industrial, editorial]
  mood: [serious, cold]
  stack: [html-tailwind, react-tailwind]
preview: /preview/tokens/typography/pairs/mission-ops/plex-mono-inter-duo
---

# Plex Mono First + Inter

> **Mono 主导**的工程屏字体对：IBM Plex Mono 跑 80% 数据 / 标签 / 编号，Inter 仅做中文与必要的人话文本

## 与 `ibm-plex-duo` 的区分

- `ibm-plex-duo`：Plex Sans 主 + Plex Mono 副，**Sans 跑 UI 主体**
- 本条：**Mono 主、Inter 副**——专门给 NASA MOCR / Bloomberg / 工程屏这类"以数据为王"的场景，UI 主体也是 mono，体现"机器在跟你说话"的工程感

## Tokens

```css
:root {
  --font-mono: 'IBM Plex Mono', 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-feature-settings: 'tnum' 1;
}

.mono { font-family: var(--font-mono); font-variant-numeric: tabular-nums; }
.sans { font-family: var(--font-sans); }
```

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link
  href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600;700&family=Inter:wght@400;500;600;700&display=swap"
  rel="stylesheet"
/>
```

## 字号 scale（紧凑工程档）

| token | size | weight | 用途 |
|---|---|---|---|
| `eyebrow` | 10-11px / uppercase / letter-spacing 0.08em | 500 | 标签 / 代号 / 微统计 caption |
| `label` | 11-12px | 400 | 区域名 / 列头 |
| `data` | 13-14px | 400-500 | 表格 / 事件流 / 字典数据 |
| `kpi-num` | 28-40px | 500 | KPI 数字（mono + tabular-nums） |
| `big` | 48-60px | 500 | 极少数大数字场景 |

## 适配指南

- **数字一定要 `font-variant-numeric: tabular-nums`** 不然位数不对齐，工程感塌
- 中文 fallback 用 `PingFang SC` / `Microsoft YaHei`，不要 noto sans cjk（与 Plex 风格不搭）
- weight 别上 700/800，Plex Mono 重字重失去工程感；500 已是上限

## 反模式

- 不要把正文也用 Inter——这会让"工程感"对半折，整体退化成普通 admin
- 不要混入第三种字体（serif 完全不要）
- 不要用 Plex Mono 的 italic 体（设计上几乎没用过的字重）
