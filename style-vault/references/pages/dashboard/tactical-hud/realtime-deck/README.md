---
id: pages/dashboard/tactical-hud/realtime-deck
type: page
name: Tactical HUD 实时大屏
description: 钢铁侠贾维斯 / 银翼杀手 2049 战术屏风的实时监控大屏 —— 左侧目录树 + 主区域玻璃面板拼接（4 圆环 KPI + 11×N 区域 HUD 卡 + 实时事件流 + 失败 Top + 雷达扫描趋势图 + 浙江 mini-map）
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
preview: /preview/pages/dashboard/tactical-hud/realtime-deck
---

# Tactical HUD Realtime Deck

> 全息控制台 / 战术 HUD 风的实时监控大屏。玻璃透视 + 圆环刻度 + 雷达扫描 + 全息蓝光，模拟"贾维斯界面"。

## 页面结构

### 左侧 240px 目录树

- 顶部：AURA logo（concentric ring SVG）+ Orbitron wordmark + `v0.5` chip + `⌐ ⌐` HUD 角标 + `⌘K 搜索`
- 6 个分组（Orbitron uppercase 标题：总览 / 区域观测 / 数据源 / 反查 / 告警 / 系统）
- 11 区域名带健康度数字（98% 绿 / 97% 琥珀 / 95% 红脉冲 / `—` 灰）
- 当前选中项有渐变发光左侧条 + 极淡 glitch
- 底部：admin@aura 用户胶囊

### 主区（玻璃面板拼接）

每个面板都是 [`radar-sweep-panel`](../../../../blocks/display/tactical-hud/radar-sweep-panel.md) 风格：

1. **Topbar**：HUD 4 角角标 + 面包屑 + 时钟（mono）+ LIVE 脉冲徽章 + 刷新下拉
2. **4 圆环 KPI**：[`arc-ring-kpi`](../../../../components/indicators/tactical-hud/arc-ring-kpi.md) × 4，每个 120×120 圆环 + 中心 Orbitron 数字
3. **区域 HUD 矩阵**：11 区 × 动态业务列
   - 每行区域名（Rajdhani）+ 健康度 mini-ring + lat/ev 元数据
   - 每业务 HUD 节点：状态点（绿/琥/红/紫）+ 业务名 + 极小数字
   - 每行有微微发光的左侧 hud 蓝条
4. **实时事件流**：PING 脉冲圆作 header 装饰 + 12-15 条 slide-in 事件（带极淡 RGB 偏移过渡）
5. **失败 Top 5**：带 hud 蓝 hover 边的列表
6. **24h 吞吐图**：3 层 area chart + 多 stroke neon 折线 + 旋转 radar sweep + 末端十字准星

### 固定 overlay

- 左下角：**浙江 mini-map SVG**（极简轮廓 + 11 个发光点 + 中心 ping 圆扩散）
- 右下角：**HUD 遥测块**——4 行 mono 数字（SIGNAL / LAT / SEQ / SYS），每秒 JS tick 更新
- 整页背景：**十字光标**（垂直 + 水平虚线 + 中心点）常驻

## 全屏装饰层

- 底层：48px 网格 overlay（HUD 蓝 5% 透明度）+ scanline 1px 横线 5s 一次扫过
- 背景径向：`#0a1228` → `#040816` 深空蓝纵深感

## 节奏

- panel 间距 16px
- 玻璃面板 padding 18-24px
- 4 KPI 圆环间距 16-24px

## 完整 HTML 来源

完整可运行 HTML mockup 留在项目仓的 `docs/plans/2026-05-20-aura-redesign-mockups/mockup-v3-C-hud.html`。网站仓的 preview tsx 是 React 化版本。

## 反模式

- 不要省 4 角 HUD 角标——整屏的"全息感"靠它们建立
- 不要把雷达 sweep 放 > 2 处（视觉竞争）
- 不要把状态色升级到 hud 蓝级别的"发光强度"（保持 hud 蓝是主调）
- 不要让 KPI 圆环用 360° 闭环——270° 缺口才是 HUD 仪表语言
- 不要省十字光标——它表达"系统在观测中"
