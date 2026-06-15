---
id: components/indicators/waveflow/pulse-ping-dot
type: component
name: Ping 双层在线点
description: 1.5×1.5px 实心 emerald-500 + 外层同色 animate-ping opacity-60 涟漪扩散；topbar / dashboard "实时" 标记
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm, confident]
  stack: [shadcn-radix]
uses: []
preview: /preview/components/indicators/waveflow/pulse-ping-dot
---

# Waveflow Pulse Ping Dot

> waveflow"实时"语义的视觉标记——`relative` 容器内 absolute 一层 `animate-ping` 涟漪 + relative 一层实心圆。两者尺寸相同 1.5×1.5px (`h-1.5 w-1.5`)，差距用 opacity 控制。`emerald-500` 表示活动，配合右侧 "N 在线" 数字（mono tnum）。Topbar 和 Dashboard 的"30s 刷新"实时标记都用它。

## 视觉特征

- **基础结构**：`<span className="relative flex h-1.5 w-1.5">` 内含两层：
  - 涟漪：`<span className="absolute inset-0 animate-ping rounded-full bg-emerald-400 opacity-60" />`
  - 实心：`<span className="relative h-1.5 w-1.5 rounded-full bg-emerald-500" />`
- **尺寸 h-1.5 w-1.5 = 6×6px**：极小——只是个"印章"
- **涟漪用 emerald-400 + opacity-60**：比实心淡 + 半透——`animate-ping` 扩散时不会刺眼
- **实心 emerald-500**：跟 `.status-dot-running` 同色，保持视觉语义统一
- **配套 dashboard 实时标记加 box-shadow**：`<span style={{ boxShadow: '0 0 6px #10b981' }} />` 6px glow，更"发光"
- 紧接右侧用 `font-mono tnum text-stone-500` 显示在线数

## 核心代码

```tsx
// Topbar 在线状态
<span className="relative flex h-1.5 w-1.5">
  <span className="absolute inset-0 animate-ping rounded-full bg-emerald-400 opacity-60" />
  <span className="relative h-1.5 w-1.5 rounded-full bg-emerald-500" />
</span>
<span className="text-[11.5px] tnum">
  <span className="font-medium text-stone-800">{online}</span>
  <span className="ml-1 text-stone-500">在线</span>
</span>

// Dashboard 实时刷新（带 glow）
<span
  className="inline-block h-1.5 w-1.5 animate-pulse rounded-full bg-emerald-500"
  style={{ boxShadow: '0 0 6px #10b981' }}
/>
实时 · 30s 刷新
```

## 适配指南

- "live" 语义专属——心跳、在线、流式接收
- 离线态：去掉 animate-ping 那层，单层 `bg-stone-400` 6px 即可
- 不要叠 `animate-pulse` + `animate-ping`——双动会"抖"，选一个
- 数字后必带 `tnum` —— 跳数时数字不晃

## 反模式

- ❌ 用 box-shadow blur > 10px ——成"光圈"而不是"标记"
- ❌ 涟漪和实心同 opacity——分不出层
- ❌ 蓝 / amber 替 emerald—— 失去"running/live"语义
