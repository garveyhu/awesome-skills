---
id: tokens/shadow/waveflow/soft-card-pop-trio
type: token
name: 软卡浮三档阴影
description: 3 档极淡阴影 (soft / card / pop)，4-8% alpha 双层叠加；CSS var 引用 28 处
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm, serious]
  stack: [shadcn-radix]
uses: []
preview: /preview/tokens/shadow/waveflow/soft-card-pop-trio
---

# Waveflow Soft / Card / Pop 三档阴影

> waveflow 阴影哲学：**软到只有 4-8% alpha**，双层叠加做"近+远"光线感。3 档分别用在：**hover/选中悬浮**（soft · 28 处）、**Section/Article 卡片底**（card · 兜底）、**Dialog/Popover 弹层**（pop · 8 处）。

## Tokens

```json
{
  "soft": "0 1px 2px rgb(0 0 0 / 4%), 0 4px 12px rgb(0 0 0 / 3%)",
  "card": "0 1px 3px rgb(0 0 0 / 5%), 0 2px 8px rgb(0 0 0 / 3%)",
  "pop":  "0 8px 24px rgb(0 0 0 / 8%), 0 2px 8px rgb(0 0 0 / 4%)",
  "css-vars": {
    "--shadow-soft": "(soft 值)",
    "--shadow-card": "(card 值)",
    "--shadow-pop":  "(pop 值)"
  },
  "usage": {
    "shadow-[var(--shadow-soft)]": "28 处 · sidebar item active + hover / brand logo / 表格 section / topbar 搜索按钮 / sidebar collapsed icon active",
    "shadow-[var(--shadow-card)]": "卡片兜底（与 paper 底色配合，存在感最低）",
    "shadow-[var(--shadow-pop)]":  "8 处 · Dialog / Popover / Tooltip / Toast / SearchPanel / DropdownMenu"
  }
}
```

## 视觉特征

- **没有 5–10% alpha 中档**：3 档之间跳跃，但每档差距小（4 / 5 / 8%）
- **双层模糊**：近层 1-2px 模糊定边、远层 8-24px 模糊给"浮起来"感——单层 shadow 会像贴片
- **soft 是"悬浮"语义**：默认 transparent，hover/active 时切到 `shadow-soft + bg-paper`——让按钮"升起来"而不是变色
- **pop 是"穿层"语义**：只用在真正脱离主流的 z-50+ 弹层

## 适配指南

- inline 引用：`className="shadow-[var(--shadow-soft)]"`（Tailwind v4 任意值）
- hover 升浮范式：`hover:bg-[var(--color-paper)] hover:shadow-[var(--shadow-soft)]`
- 弹层一律 `shadow-[var(--shadow-pop)]`

## 反模式

- ❌ 用 Tailwind 默认 `shadow-md` / `shadow-lg`——alpha 太重显廉价
- ❌ 卡片堆 `shadow-2xl`——破坏暖白页气质
