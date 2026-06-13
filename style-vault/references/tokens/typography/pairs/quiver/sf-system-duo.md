---
id: tokens/typography/pairs/quiver/sf-system-duo
type: token
name: 系统无衬线 + Mono 数字
description: 系统 UI 字（SF Pro / PingFang）配 SF Mono / JetBrains，所有数字走 tabular-nums 等宽对齐
platforms: [web]
theme: dark
tags:
  aesthetic: [minimal]
  mood: [calm, serious]
  stack: [vanilla-css]
---

# 系统无衬线 + Mono 数字

> 界面用系统无衬线、数字一律切等宽 Mono，桌面应用「原生感 + 工程感」的字体分工

## 视觉特征

- **正文/界面 = 系统无衬线栈**：`-apple-system, "SF Pro Text", "Inter", "PingFang SC", "Microsoft YaHei", sans-serif`——优先吃 macOS 原生 SF Pro，桌面 app 一眼「原生」，中文落 PingFang
- **数字/快捷键/代码 = Mono 栈**：`"SF Mono", "JetBrains Mono", ui-monospace, SFMono-Regular, monospace`
- **所有数字强制等宽对齐**：`.num` 用 `font-variant-numeric: tabular-nums; font-feature-settings: "tnum" 1, "ss01" 1; letter-spacing: 0`——HUD 的经理/运行/通过/花费数字跳动时不抖位
- **字重靠 500–660 区间分层**，不堆超粗：界面 500、强调 600、卡头 `font-weight: 650`、面板标题 `font-weight: 660`
- **基础字号偏小、letter-spacing 极克制**：界面 11–13px、`letter-spacing: .1px`；分组小标题走 `10.5px / letter-spacing 1.2px / uppercase` 当眉头
- **DPR=1 子像素优化**：非 retina 屏 body 切 `subpixel-antialiased`、磨砂面退实底，专治「字糊」（见 global.css 注释）

## Tokens

```json
{
  "family": {
    "ui": "-apple-system, \"SF Pro Text\", \"Inter\", \"PingFang SC\", \"Microsoft YaHei\", sans-serif",
    "mono": "\"SF Mono\", \"JetBrains Mono\", ui-monospace, SFMono-Regular, monospace"
  },
  "numeric": {
    "font-variant-numeric": "tabular-nums",
    "font-feature-settings": "\"tnum\" 1, \"ss01\" 1",
    "letter-spacing": "0"
  },
  "weight": { "ui": 500, "emphasis": 600, "card-head": 650, "panel-title": 660 },
  "size": {
    "micro": "10.5px", "meta": "11px", "ui": "12.5px",
    "field": "14px", "cmdk-input": "15px", "panel-h2": "16px"
  },
  "tracking": { "base": ".1px", "eyebrow": "1.2px" }
}
```

## 适配指南

- 不装任何 web font——全走系统字栈，桌面 app 零网络依赖、原生质感是卖点
- **数字位必须挂等宽类**：凡是会实时跳动的统计（花费 `$x.xx`、计数、时长）一律 `.num` / tabular-nums，否则 HUD 抖动
- 中文环境把 PingFang 留在栈里；纯英文场景可省

## 反模式

- 不要为「设计感」换展示衬线/手写字——这套是工具型桌面 app，字体职责是退让与对齐，不是表演
- 不要给跳动数字用比例字（proportional）——宽度抖动比字体本身更廉价
- 不要堆 700+ 超粗字重——层级靠 500/600/650 三档 + 颜色明度，不靠字重轰炸
