---
id: styles/admin-console/mission-ops-flight-deck
type: style
name: Mission Ops 飞控台
description: NASA MOCR / Bloomberg Terminal / 量化交易桌的工程 nerd 风。极致信息密度 + 4 字母代号系统 + 工程图纹 + Mono 主导字体，专为监控大屏 / 运维台 / 数据工程后台设计
platforms: [web]
theme: dark
tags:
  aesthetic: [industrial, editorial]
  mood: [cold, serious]
  stack: [html-tailwind]
uses:
  - tokens/palettes/mission-ops/deep-space-amber
  - tokens/typography/pairs/mission-ops/plex-mono-inter-duo
  - components/indicators/mission-ops/coded-kpi-card
  - blocks/display/mission-ops/coded-panel-header
  - pages/dashboard/mission-ops/realtime-deck
preview: /preview/styles/admin-console/mission-ops-flight-deck
---

# Mission Ops Flight Deck

> 把 NASA 任务控制室（MOCR）+ Bloomberg Terminal + 量化交易终端的视觉语言抽象出来——给现代工程屏一套统一的"工业仪表盘"调子。

## 设计哲学

**信息密度优先**——所有视觉决策让位于"一屏看完更多"。
**机器在跟你说话**——UI 主体用 mono 字体（80% 数据 / 标签 / 编号），让画面有"控制台"而不是"网站"的感觉。
**模块化标识**——每个 panel 是独立的"工位"，有自己的 4 字母代号（OVRV-MTRX / RTM-FEED 等）+ σ/max/min 微统计，模仿真实 NASA 屏上每块面板的"模块编号"。

## 视觉特征

- **全站暗色**：4 层深蓝黑 `#070a12 → #121a2c` 递进，靠层次而非边框
- **Mono 主导**：IBM Plex Mono 占 80%（数据 / 编号 / 标签），Inter 仅做中文与人话标签
- **4 字母代号系统**：所有 panel 头部带 `OVRV-MTRX` 这种"4+4"或"4+3"代号
- **σ/max/min 三段微统计**：panel 头部右侧常驻，让每块数据自带"统计上下文"
- **双层网格底纹**：24px + 120px 两层 grid + radial mask 渐隐，工程图纸感
- **状态色严格语义化**：6 色（ok/info/warn/fail/purple/mute）+ 3 加重色（amber/green/crit），每色绑死含义
- **14 段底部遥测条**：横跨全屏，模拟飞控台的"舱底信息条"，OPERATIONAL / ALERTS / BUILD / UPTIME 等关键段带脉冲点
- **极小动效**：仅 feed slide-in（45ms stagger）+ chart end-point pulse + 状态点脉冲；**无持续呼吸 / 粒子 / 扫描线**

## 设计原则

1. **零浪漫动效**：spring / bounce / overshoot 一律禁止；feed 进入用 ease-out 200ms 即可
2. **一色一职**：状态色 6 个职责绑死（ok=健康 / warn=警告 / fail=告警 / info=数据 / purple=特殊源 / mute=离线）
3. **数字优先**：数字一律 mono + tabular-nums，右对齐
4. **角落讲价值**：每个 panel 右上角 σ/max/min，底部一定有 1px hairline，左下角可加坐标刻度
5. **告警不打扰**：异常态用静态颜色 + 状态点常亮（不闪烁），ALERTS 段在底部遥测条用脉冲点
6. **业务列数动态**：region 维度的网格不强求"齐整"——每区业务列数不同是这套风格的卖点之一

## 字号 stack

| level | size | weight | usage |
|---|---|---|---|
| eyebrow | 10-11px uppercase | 500 | 代号 / caption |
| label | 11-12px | 400 | 中文标签 / 列头 |
| data | 13-14px mono | 400-500 | 表格 / 数据 |
| kpi | 28-40px mono | 500 | KPI 大数字 |
| big | 48-60px | 500 | 极少数场景 |

## 适配指南

**适合用本风格的产品**：
- 同步链路监控 / 实时大屏（如 aura 监控本身）
- 运维 NOC / SRE 监控台
- 量化交易 / 金融行情桌
- 数据工程 ETL 任务调度后台
- 飞控 / 卫星地面站 / 工业 SCADA

**不适合**：
- 消费级 SaaS / 营销页
- 内容站 / 文档站
- 任何讲求"留白美学"或"温暖人性化"的产品

## 反模式

- 不要在本风格里加渐变色装饰（破坏工程感）
- 不要把卡片圆角 > 4px
- 不要做 box-shadow（层次靠 1px hairline）
- 不要让 panel 头部"成为标题"——它是 caption + 代号 + 微统计的组合，永远 36-40px 高
- 不要给数字加颜色装饰（除了 delta 涨跌）
- 不要在 panel 网格里搞 12 等分——主从必须明显
