---
id: pages/dashboard/mission-ops/realtime-deck
type: page
name: Mission Ops 实时大屏
description: NASA MOCR / Bloomberg Terminal 风的实时监控大屏 —— 左侧目录树 + 主区域 12-col 致密网格（4 KPI + 11×N 动态业务矩阵 + 实时事件流 + 失败 Top + 24h 趋势 + 系统遥测） + 底部 14 段状态栏
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
preview: /preview/pages/dashboard/mission-ops/realtime-deck
---

# Mission Ops Realtime Deck

> NASA 任务控制中心 / Bloomberg Terminal 风的实时监控大屏。一屏塞满数据，但靠 4 字母代号 + σ/max/min 微统计 + 双层网格 + 工程图纹拉出清晰层次。

## 页面结构

自左至右、自上至下：

### 左侧 240px 目录树

- 顶部：Aura logo + 站名 + `v0.5` + `⌘K 搜索` 输入
- 6 个分组（▾ 可折叠）：总览 / 区域观测（11 区，带健康度数字） / 数据源 / 反查 / 告警 / 系统
- 当前选中项左侧 2-3px 高亮条
- 底部：`admin@aura · ⚙`

### 主区（剩余宽度，12-col 网格）

1. **Topbar**：面包屑 `总览 / 实时大屏` + 时钟 + LIVE 徽章 + 刷新间隔下拉
2. **4 KPI 卡**（[`coded-kpi-card`](../../../../components/indicators/mission-ops/coded-kpi-card.md)）：今日总事件 / 成功率 / P95 / 数据源在线
3. **OVRV-MTRX**（8/12）：region × **动态** 业务矩阵
   - 11 行区域，每行业务列数不同（拱墅 5 / syzh 4 / 嘉善 2 / 北仑 6 等）
   - 每业务格：cell 顶部业务名 + 状态符号 + microbar 阵列 + 健康 %
   - 奉化离线状态（hp `—` / skip cells）
4. **RTM-FEED**（4/12）：右侧实时事件流，12-15 条 slide-in 进入
5. **FAIL-TOP**（4/12）：失败 Top 5 + 百分比条
6. **FLOW-24H**（5/12）：24h 双线吞吐 + 网格底纹 + dashed reference lines + 扫描线
7. **SYS-INFO**（3/12）：18 行遥测表格

### 底部 28px 遥测条

横跨全屏，14 段分隔：
`CTL OPERATIONAL · REGIONS 10/11 · FEED rate · P95 · QUEUE · MEM · CPU · DB · REDIS · ALERTS 3 OPEN · BUILD hash · UPTIME · MODE · UTC+8`

关键段（OPERATIONAL / ALERTS）带脉冲点。

## 节奏

- 4 KPI 卡间距 12px（gap-3）
- panel 之间间距 16px（gap-4）
- panel header 高 36-40px，content 紧贴内边距 16-20px

## 完整 HTML 来源

完整可运行 HTML mockup 留在项目仓的 `docs/plans/2026-05-20-aura-redesign-mockups/mockup-v3-A-nasa.html`，作为本 page 的"完整渲染参考"。网站仓的 preview tsx 是 React 化的可交互版本。

## 反模式

- 不要把每个区域行做成"齐整列数"——业务动态化是这个 page 的关键卖点
- 不要省 4 字母代号系统——它是 panel 头部的视觉锚
- 不要给整屏加 padding > 24px 的呼吸——信息密度是这套风格的灵魂
- 不要在 12-col 网格里搞 12 等分——主从应该明显（OVRV-MTRX 8 vs RTM-FEED 4）
