---
id: tokens/border/waveflow/translucent-stone-system
type: token
name: 半透明 Stone 分层边框系统
description: 5 档 stone-200/40 · /60 · /70 · stone-100 · stone-300，按层级用"透明度"区分边框，让暖底色透出来
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm]
  stack: [shadcn-radix]
uses: []
preview: /preview/tokens/border/waveflow/translucent-stone-system
---

# Waveflow Translucent Stone Borders

> waveflow 边框系统的核心招式：**不用 stone-200 实色，用 stone-200/40~70 半透明**——让底色（warm-2 / paper）透过边框淡淡浮现，比纯线条更柔和、更"工程师"。5 档透明度对应不同层级。

## Tokens

```json
{
  "border-stone-200/40": "rgba(231,229,224,0.4)  - 19 文件 · 外框 Section / Article / Dialog（最淡，几乎只是结构提示）",
  "border-stone-200/60": "rgba(231,229,224,0.6)  - 10 文件 · DataTable 外框 / Card 外框（中淡，主结构感）",
  "border-stone-200/70": "rgba(231,229,224,0.7)  - 13 文件 · sidebar 右边 / topbar 下边 / cmdk modal 外框（强结构线）",
  "border-stone-100":    "rgba(245,244,238,1)    - 36 文件 · 章节/卡片内部分割（DialogHeader 下 / DataTable thead 下 / tbody divide-y / KPI card 内）",
  "border-stone-300":    "rgba(214,211,209,1)    - 输入框默认边 / 选项卡未选中 / Stepper 未激活圆圈",
  "border-stone-400":    "(hover 输入框升级边)",
  "border-dashed":       "用于空态 EmptyState + 新建集合按钮（border-2 border-dashed border-stone-200）"
}
```

## 视觉特征

- **/40 vs /60 vs /70 不是装饰**：是层级语义——/40 是"无关紧要的外壳"、/60 是"主内容卡边"、/70 是"骨架边线（sidebar/topbar/modal）"
- **stone-100 实色作分割**：内部横线必须用 stone-100，不能用 /40 半透——半透在白底上看不见
- **dashed 只给"空态/新建"用**：1.5x 粗细 + dashed → 一眼读懂"这里要加东西"
- 跟 shadow 软配合："淡 border + 软 shadow" 是 waveflow 卡片的双轮——少了任一都飘

## 适配指南

- Section 外壳：`rounded-xl border border-stone-200/40 bg-[var(--color-paper)] shadow-[var(--shadow-soft)]`
- Dialog 外壳：`rounded-2xl border border-stone-200/60 bg-[var(--color-paper)] shadow-[var(--shadow-pop)]`
- 横向分割：`border-b border-stone-100`
- 输入框：`border-stone-300 hover:border-stone-400 focus:border-blue-500`

## 反模式

- ❌ 用 zinc/slate/neutral 系列——和暖底色温不和
- ❌ 用纯实色 stone-200 大量铺——会和暖底"硬碰硬"显廉价
- ❌ 内部分割也用半透明 stone-200/40——在白底上几乎看不见
