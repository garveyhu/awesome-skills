---
id: styles/admin-console/tactical-hud-jarvis
type: style
name: Tactical HUD Jarvis
description: 钢铁侠贾维斯 / 银翼杀手 2049 / Halo 战术屏风。圆环刻度 + 玻璃透视 + 雷达扫描 + 全息蓝，专为科技感运维台 / 实时控制系统 / 安防 / 战术展示设计
platforms: [web]
theme: dark
tags:
  aesthetic: [industrial, glass]
  mood: [confident, cold]
  stack: [html-tailwind]
uses:
  - tokens/palettes/tactical-hud/hud-cyan-glass
  - tokens/typography/pairs/tactical-hud/orbitron-rajdhani-trio
  - components/indicators/tactical-hud/arc-ring-kpi
  - blocks/display/tactical-hud/radar-sweep-panel
  - pages/dashboard/tactical-hud/realtime-deck
preview: /preview/styles/admin-console/tactical-hud-jarvis
---

# Tactical HUD Jarvis

> 把钢铁侠贾维斯 / 银翼杀手 2049 / Halo 战术屏的视觉语言抽象成一套设计系统——给现代实时控制台一种"全息投影 / 科幻仪表"的强力调子。

## 设计哲学

**仪表 > 平面**——所有 KPI 都是"仪表"（270° 圆环 + cardinal ticks），不是纯文字数据。
**全息 > 实体**——所有 panel 都用 backdrop-blur + 半透明玻璃 + 1px 蓝边，模拟"浮在空中的数据层"。
**持续观测**——雷达 sweep + PING 脉冲 + 十字光标，让画面永远在"动"，传达"系统在工作"。
**HUD 蓝是灵魂**——所有 accent 都用 `#38bdf8` / `#22d3ee` 这两个 HUD 蓝，状态色仅 4 种，色系极克制。

## 视觉特征

- **径向深空蓝底**：`radial-gradient(#0a1228, #040816)`，纵深感取代平面
- **三层字体协奏**：Orbitron（品牌+大数字）+ Rajdhani（中文+正文）+ JetBrains Mono（数据+代码）
- **玻璃面板基底**：所有卡片 `backdrop-filter: blur(20px)` + `bg: rgba(56,189,248,0.05)` + 1px HUD 蓝边
- **270° 圆环 KPI**：所有 KPI 都用 `arc-ring-kpi` 形态，不用平面卡
- **4 角 HUD 角标**：所有 panel 都带 `⌐⌐⌐⌐` 角标
- **雷达 sweep 动效**：核心 panel 有缓慢旋转的 5s 扇形
- **PING 脉冲**：状态点用 `box-shadow: 0 0 0 X` 扩散圆，1.5s 周期
- **十字光标常驻**：背景永远有水平 + 垂直 + 中心点的"准星"
- **mini-map 角落**：右下角 / 左下角放区域 / 拓扑 mini-map，11 个发光点

## 设计原则

1. **HUD 蓝克制**：所有发光元素都走 `#38bdf8` / `#22d3ee`，不要替换或添加第三种 accent 蓝
2. **状态色仅 4 种**：ok 绿 / warn 琥珀 / bad 红 / info 紫，每色绑死含义
3. **Orbitron 不泛用**：只用在 brand wordmark + KPI 大数字 + system 徽章（LIVE / OFFLINE），其它一律 Rajdhani / mono
4. **持续动效 ≤ 3 处**：sweep + PING + 数字 counter，再多就视觉过载
5. **玻璃 + blur 不可省**：blur < 16px 失去"全息感"
6. **270° 不闭合圆**：所有圆环 KPI 都留 90° 缺口，那个缺口是"工程仪表"语言的标识
7. **业务列数动态**：region 矩阵每行业务列数不齐整——HUD 风承认数据源的不齐整性

## 适配指南

**适合用本风格的产品**：
- 科技感强的运维 / 监控 / 控制台
- 实时观测系统（安防 / 调度中心 / 物流大屏）
- 战术展示 / 军工 / 航海航天界面
- 想"震撼领导"或"对外宣传"的项目

**不适合**：
- 内容站 / 文档站
- 主张"克制美学 / 性冷淡"的产品
- 移动端 / 小屏（圆环 + 玻璃在小尺寸下吃力）
- 需要可访问性极强的合规项目（玻璃低对比度可能影响 a11y）

## 反模式

- 不要把 HUD 蓝替换为绿 / 紫 / 粉——这是这套风格的灵魂色
- 不要在 HUD 风内加渐变色卡片装饰（粉紫渐变会破坏全息感）
- 不要用 360° 闭合圆做 KPI（必须 270° 缺口）
- 不要堆 emoji
- 不要给中文用 noto sans cjk（与 Rajdhani 风格不搭，要用 PingFang SC）
- 不要在持续动效上加速度（保持 1.5-5s 慢节奏，快了变廉价游戏 UI）
- 不要使 panel 完全不透明（背景纯色 = 失去玻璃感 = 退化成普通暗色 admin）
