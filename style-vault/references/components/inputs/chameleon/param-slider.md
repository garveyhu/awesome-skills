---
id: components/inputs/chameleon/param-slider
type: component
name: 参数滑块
description: LLM 运行参数统一滑块——标签 + 当前值 mono 徽章 + min/max 刻度 + 可选 ∞@0 + hint，原生 range accent-amber-600 暖色手柄
platforms:
- web
theme: light
tags:
  aesthetic:
  - industrial
  - minimal
  mood:
  - serious
  stack:
  - shadcn-radix
preview: /preview/components/inputs/chameleon/param-slider
---

# 参数滑块

> Chameleon 给 LLM 运行参数（temperature / top_p / max_tokens）统一的滑块控件，取代各处散落的裸 `range`。标签行右侧一枚 mono 值徽章，下方原生 range（`accent-amber-600` 暖色手柄，刻意区别于全站蓝），轨道两端标 min/max 刻度，可选「∞@0」（如 max_tokens=0 表示不限）与底部 hint。waveflow 无滑块条目，故 new。

## 视觉特征

- 容器 `space-y-1.5`（6px 纵向间距）
- 头行 `flex items-center justify-between`：
  - label `text-[12px] font-medium text-stone-700`
  - 值徽章 `rounded bg-stone-100 px-1.5 py-0.5 font-mono text-[11.5px] tabular-nums text-stone-700`（`infinityAtZero && value===0` 时显 `∞`）
- range `w-full cursor-pointer accent-amber-600`（#d97706 暖橙手柄——signature，区别于全站 primary 蓝）
- 刻度行 `flex justify-between text-[10px] tabular-nums text-stone-400`：min（∞ 模式且 min===0 显 `0`） / max（∞ 模式显 `∞`）
- hint `text-[10.5px] leading-snug text-stone-500`

## 核心代码

```tsx
<div className="space-y-1.5">
  <div className="flex items-center justify-between">
    <label className="text-[12px] font-medium text-stone-700">{label}</label>
    <span className="rounded bg-stone-100 px-1.5 py-0.5 font-mono text-[11.5px] tabular-nums text-stone-700">
      {infinityAtZero && value === 0 ? '∞' : value}
    </span>
  </div>
  <input type="range" min={min} max={max} step={step} value={value}
    className="w-full cursor-pointer accent-amber-600" />
  <div className="flex justify-between text-[10px] tabular-nums text-stone-400">
    <span>{infinityAtZero && min === 0 ? '0' : min}</span>
    <span>{infinityAtZero ? '∞' : max}</span>
  </div>
  {hint && <p className="text-[10.5px] leading-snug text-stone-500">{hint}</p>}
</div>
```

## 适配指南
- 全站 LLM 参数面板（应用设置 / playground）统一走它；max_tokens 这类「0=不限」参数传 `infinityAtZero`
- 值徽章必须 `font-mono tabular-nums`，否则拖动时数字宽度跳动
- 画布节点 inspector 内的滑块用 `graph-config-field-kit` 的 SliderField（accent-blue-600）——两者按场景分色：节点配置蓝、运行参数暖橙

## 反模式
- ❌ 滑块用 accent-blue-600 —— param-slider 的 signature 就是暖橙 accent-amber-600，与节点配置滑块刻意分色
- ❌ 值徽章用普通 sans 字体 —— 必须 mono + tabular-nums，拖动时数字不跳
- ❌ hint 用 stone-400 —— hint 是 stone-500，比刻度的 stone-400 略深（hint 是要读的，刻度是参考）
