---
id: blocks/display/mission-ops/coded-panel-header
type: block
name: 4 字母代号工程面板
description: 工程屏 panel 标志性头部模式——左侧 4 字母大写代号（OVRV-MTRX / RTM-FEED 等）+ 中文副标题 + 右侧 σ/max/min 三微统计 + 状态点 + 1px hairline 分隔
platforms: [web]
theme: dark
tags:
  aesthetic: [industrial, editorial]
  mood: [cold, serious]
  stack: [html-tailwind, react-tailwind]
uses:
  - tokens/palettes/mission-ops/deep-space-amber
  - tokens/typography/pairs/mission-ops/plex-mono-inter-duo
preview: /preview/blocks/display/mission-ops/coded-panel-header
---

# Coded Panel Header

> 模块化工程面板的"标识系统"：每个 panel 都有自己的 4 字母代号 + 副标题 + 微统计 + 状态点。Bloomberg Terminal / NASA MOCR / 量化交易桌的核心视觉语言。

## 视觉锚点

- **4 字母大写代号**：`OVRV-MTRX` / `RTM-FEED` / `FAIL-TOP` / `FLOW-24H` / `SYS-INFO` 等
  - mono 大写 + `letter-spacing: 0.12em` + 11-12px + accent 色（如 ok 绿 / info 青）
  - 永远在 panel 头部最左
- **中文副标题**：`sans` 字体 / 12px / `text-2` 灰，跟在代号后用 1px 竖线分隔
- **σ/max/min 微统计**：mono / 10.5px / `text-3` 灰，右上角横排，每段独立
- **状态点**：4px 实心圆 + 1px ring，靠 panel 头部最右，对应 panel 健康度
- **底部 1px hairline** `rgba(255,255,255,.07)` 切开 panel header 与 content

## 用到的 tokens

- color：`ok #34d399` / `info #22d3ee` / `warn #fbbf24` / `fail #fb7185` / text 4 级
- font：mono（代号 + 微统计）+ sans（中文副标题）

## 核心代码

```html
<div class="panel border border-white/10 bg-[#0a0e1a]">
  <div class="panel-hd flex items-center gap-3 px-3.5 py-2.5"
       style="border-bottom:1px solid rgba(255,255,255,.07)">
    <span class="mono"
          style="font-size:11px;letter-spacing:.12em;color:#34d399;text-transform:uppercase;font-weight:500">
      OVRV-MTRX
    </span>
    <span style="width:1px;height:11px;background:rgba(255,255,255,.18)"></span>
    <span class="sans" style="font-size:12px;color:rgba(255,255,255,.62)">总览矩阵</span>

    <div class="ml-auto mono flex items-center gap-3"
         style="font-size:10.5px;color:rgba(255,255,255,.38)">
      <span>σ <span style="color:rgba(255,255,255,.62)">0.42</span></span>
      <span>max <span style="color:rgba(255,255,255,.62)">16.0M</span></span>
      <span>min <span style="color:rgba(255,255,255,.62)">8.2M</span></span>
    </div>

    <span class="ml-2 relative" style="width:4px;height:4px;background:#34d399;border-radius:50%;
          box-shadow:0 0 0 1px rgba(52,211,153,.4),0 0 8px rgba(52,211,153,.4)"></span>
  </div>

  <div class="panel-body p-4">
    <!-- 这里塞 panel 内容（矩阵 / 列表 / 图表等） -->
  </div>
</div>
```

## 代号命名约定

- 4 字符 + dash + 4 字符（如 `OVRV-MTRX`）或 4 字符 + dash + 3 字符（如 `SYS-INFO`）
- 大写、无 underscore、纯 ASCII
- 语义：前段是"业务域"（OVRV=overview / RTM=realtime / FAIL=failure 等），后段是"内容形态"（MTRX=matrix / FEED=stream / TOP=ranking / 24H=time-series 等）
- **一致性**：同 dashboard 内的 panel 代号要"成体系"——如果 OVRV-MTRX 用了，就别再有 OVERVIEW-MATRIX 或 OV-M

## 适配指南

- 状态点的颜色 = panel 整体健康度：全部正常 ok 绿 / 有 fail warn 琥珀 / 大面积 fail crit 红
- 状态点常驻不脉冲（除非 panel 本身处于异常态）
- σ/max/min 三段最少出 1 段（如果数据本身没有方差/极值，至少出 max 或 last）

## 反模式

- 不要在代号里加 emoji 或颜色 icon——纯文字才有工程感
- 不要让中文副标题超过 8 字——长了挤掉微统计
- 不要把代号字号做大成"标题"——它是 caption，11-12px 上限
- 不要在 panel 边框用 > 1px 的 stroke
