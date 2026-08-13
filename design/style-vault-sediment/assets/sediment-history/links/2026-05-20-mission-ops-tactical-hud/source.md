# 素材溯源 · Mission Ops & Tactical HUD

## 来源类型

from-project（本地 HTML mockup 反向提取）

## 项目路径

`~/Documents/company/ikt-docs/数据同步/docs/plans/2026-05-20-aura-redesign-mockups/`

属于 aura 监控大屏重构 brainstorming 期间产出的视觉探索 mockup。**不是真实生产代码**，是 4 个并行 agent 跑出的 4 套调子（A NASA / B 赛博朋克 / C HUD / D NOC），其中 A 和 C 被用户选中沉淀。

## 关键文件

- `mockup-v3-A-nasa.html`（51 KB · 826 行）—— NASA / Bloomberg Terminal 风
- `mockup-v3-C-hud.html`（43 KB · 453 行）—— 钢铁侠 / 银翼杀手 HUD 风

均为单文件 HTML + Tailwind CDN + 内联 SVG，能浏览器双击直接渲染。

## 视觉锚点提取

### A · NASA / Mission Ops

- 4 层深蓝黑底（#070a12 / #0a0e1a / #0d1320 / #121a2c）
- IBM Plex Mono 主导 + Inter 中文副
- 4 字母代号系统（OVRV-MTRX / RTM-FEED / FAIL-TOP / FLOW-24H / SYS-INFO）
- σ/max/min 三段微统计
- 14 段底部遥测条
- 双层 grid 底纹（24px + 120px）+ radial mask
- 状态色严格 6 种

### C · HUD / Tactical HUD

- 径向深空蓝（#040816 → #0a1228）
- HUD 蓝双色 #38bdf8 / #22d3ee
- backdrop-blur 玻璃面板 + 1px HUD 蓝边
- 270° 圆环 KPI + 8 cardinal ticks
- 4 角 HUD 角标（⌐⌐ ⌐⌐）
- 雷达扫描扇形（conic-gradient + 5s 旋转）
- PING 脉冲圆（1.5s ease-out）
- 十字光标常驻
- Orbitron + Rajdhani + JetBrains Mono 三件套

## 对话摘录

用户原话（关键决策点）：

> "把 A 和 C 两种风格沉淀到 style-vault 中"
>
> "它不是一个产品呀。只是两种风格，以及简单的一些页面，以及从 HTML 拆出一些原子化组件出来"
>
> "前端代码也要沉淀啊。"
>
> "除了 skill 不是有个前端仓库项目吗，要在那里把 html 拆分沉淀进去"

这三句话直接决定了：
1. **不出 product 层**（破例 Tier 1 必出之一）
2. **加 pages 层做完整页面预览**
3. **必须双仓写入**（skill .md + 网站仓 .tsx React 预览）

## 起点

aura 监控平台的视觉重构 brainstorming 议题 —— 用户希望在确定 aura 主视觉前，把两套已经成型的"高级感"调子沉淀成可复用资产，为以后 aura 之外的后台 / 监控 / 工程类项目提供风格选择。
