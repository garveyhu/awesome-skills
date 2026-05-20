# 沉淀计划 · Mission Ops & Tactical HUD

日期：2026-05-20
作者：links
模式：create
起点：from-project（两份本地 mockup HTML）
档位：Tier 1 · 精髓档（目标 5–8 条 / style，× 2 = 10–16 条总）

## 目标

把 aura 监控大屏 v3 系列的两套视觉调子沉淀成可复用资产：
- **A · Mission Ops**：NASA MOCR / Bloomberg Terminal 工程 nerd 风（极致信息密度 + 4 字母代号 + 工程图纹）
- **C · Tactical HUD**：钢铁侠贾维斯 / 银翼杀手 2049 战术屏风（圆环刻度 + 玻璃透视 + 雷达扫描）

下次开发后台 / 监控 / 工程类项目时能直接取 token + 原子组件 + 整页样板复用。

## 来源溯源

- `/Users/links/Documents/company/ikt-docs/数据同步/docs/plans/2026-05-20-aura-redesign-mockups/mockup-v3-A-nasa.html`
- `/Users/links/Documents/company/ikt-docs/数据同步/docs/plans/2026-05-20-aura-redesign-mockups/mockup-v3-C-hud.html`

## 涉及条目（依赖拓扑序 · 共 12 条）

### A · Mission Ops（6 条）
1. tokens/palettes/mission-ops/deep-space-amber
2. tokens/typography/pairs/mission-ops/plex-mono-inter-duo
3. components/indicators/mission-ops/coded-kpi-card
4. blocks/display/mission-ops/coded-panel-header
5. pages/dashboard/mission-ops/realtime-deck
6. styles/admin-console/mission-ops-flight-deck

### C · Tactical HUD（6 条）
7. tokens/palettes/tactical-hud/hud-cyan-glass
8. tokens/typography/pairs/tactical-hud/orbitron-rajdhani-trio
9. components/indicators/tactical-hud/arc-ring-kpi
10. blocks/display/tactical-hud/radar-sweep-panel
11. pages/dashboard/tactical-hud/realtime-deck
12. styles/admin-console/tactical-hud-jarvis

## 依赖关系

```
mission-ops-flight-deck  (style)
  ├─ tokens/palettes/mission-ops/deep-space-amber
  ├─ tokens/typography/pairs/mission-ops/plex-mono-inter-duo
  ├─ components/indicators/mission-ops/coded-kpi-card
  ├─ blocks/display/mission-ops/coded-panel-header
  └─ pages/dashboard/mission-ops/realtime-deck

tactical-hud-jarvis  (style)
  ├─ tokens/palettes/tactical-hud/hud-cyan-glass
  ├─ tokens/typography/pairs/tactical-hud/orbitron-rajdhani-trio
  ├─ components/indicators/tactical-hud/arc-ring-kpi
  ├─ blocks/display/tactical-hud/radar-sweep-panel
  └─ pages/dashboard/tactical-hud/realtime-deck
```

## 元信息填写方式

- AI 自动填：全部 12 条（用户批准 Y 模式）

## 不出 product 的决策

用户原话："它不是一个产品呀。只是两种风格"——按 Tier 1 必出原本含 1 个 product，本次根据用户实际意图破例不出 products/*。

## 执行状态

☑ 用户已确认（含调整：删 products / 加 pages 文件夹形态 / 双仓写入）· 待写入
