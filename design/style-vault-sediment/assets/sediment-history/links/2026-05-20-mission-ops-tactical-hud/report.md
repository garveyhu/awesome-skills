# 沉淀报告 · Mission Ops & Tactical HUD

日期：2026-05-20
模式：create
起点：from-project（两份本地 HTML mockup）
档位：Tier 1 · 精髓档（目标 5–8 / style · 实际 6 + 6 = 12 条）
作者：links

## 涉及条目（12 条）

| # | 操作 | 类型 | ID | 名称 |
|---|---|---|---|---|
| 1 | 新增 | token | tokens/palettes/mission-ops/deep-space-amber | 深空琥珀 |
| 2 | 新增 | token | tokens/typography/pairs/mission-ops/plex-mono-inter-duo | Plex Mono 主导 + Inter |
| 3 | 新增 | component | components/indicators/mission-ops/coded-kpi-card | 代号 KPI 卡 |
| 4 | 新增 | block | blocks/display/mission-ops/coded-panel-header | 4 字母代号工程面板 |
| 5 | 新增 | page | pages/dashboard/mission-ops/realtime-deck | Mission Ops 实时大屏 |
| 6 | 新增 | style | styles/admin-console/mission-ops-flight-deck | Mission Ops 飞控台 |
| 7 | 新增 | token | tokens/palettes/tactical-hud/hud-cyan-glass | HUD 青光玻璃 |
| 8 | 新增 | token | tokens/typography/pairs/tactical-hud/orbitron-rajdhani-trio | Orbitron 三件套 |
| 9 | 新增 | component | components/indicators/tactical-hud/arc-ring-kpi | 270° 圆环 KPI |
| 10 | 新增 | block | blocks/display/tactical-hud/radar-sweep-panel | 雷达扫描全息面板 |
| 11 | 新增 | page | pages/dashboard/tactical-hud/realtime-deck | Tactical HUD 实时大屏 |
| 12 | 新增 | style | styles/admin-console/tactical-hud-jarvis | Tactical HUD Jarvis |

## 元信息来源

- AI 自动填（用户授权 Y 模式）：全部 12 条
- 用户手改：无（review 时整批 OK）
- 纯手填：无

## 分类决策说明

- **theme**: 两条都标 `dark`（mockup 本身就是 dark），typography token 标 `both`（字体本身两个主题都能用）
- **stack**: `html-tailwind`（mockup 源自 HTML + Tailwind CDN），typography token 加 `react-tailwind`（字体跨栈通用）
- **aesthetic**: 两条都打 `industrial`（工程屏 / 工业仪表），A 加 `editorial`（信息密度排版感），C 加 `glass`（玻璃透视）
- **mood**: A 走 `cold + serious`（NASA 工程屏严肃感），C 走 `cold + confident`（HUD 战术屏的"自信感"）
- **不出 product**：用户原话"不是一个产品呀。只是两种风格"——破例 Tier 1 必出 1 个 product 的硬规矩
- **加 pages**：用户希望直接预览整页效果，pages 文件夹形态 + React preview 满足这个诉求

## Namespace 决策

- `mission-ops`（NASA 任务运维）—— A 系列 4 个 tokens/components/blocks 资产的归属
- `tactical-hud`（战术 HUD）—— C 系列 4 个 tokens/components/blocks 资产的归属

两个 namespace 都是**首次启用**（vault 现有 namespace：acme / sage / skillhub / style-vault / _shared）。不绑特定 product —— 用户明确希望以后能复用到 aura 之外的项目。

## styles/admin-console/ bucket 首批

之前 `styles/admin-console/` 是空 bucket（vault 现有 styles 都在 saas-tool / community-social / portfolio-studio 等下）。本次沉淀让 admin-console 启用，专门承载"后台 / 监控 / 工程类"的整套调子。

## 重名 grep 结果

- `tokens/typography/pairs/acme/ibm-plex-duo` 与 mission-ops 的 plex-mono-inter-duo 存在字体重叠（都用 IBM Plex Mono），但用法不同：acme 用 Plex Sans 主、Plex Mono 副，mission-ops 反过来。已在新条目 README 加"与 ibm-plex-duo 的区分"章节明确差异。
- 其他无近义条目冲突。

## 视觉锚点确认

| 系列 | 必须传神的元素 | preview 落实 |
|------|--------------|-------------|
| **A · mission-ops** | 4 层深蓝黑底 / 4 字母代号 / σ/max/min 微统计 / IBM Plex Mono 主导 / 底部 14 段遥测条 | ✓ 都在 6 个 tsx 内完整呈现 |
| **C · tactical-hud** | 径向深空蓝 / HUD 蓝 / 270° 圆环 / backdrop-blur 玻璃 / 4 角 HUD 角标 / 雷达 sweep / PING 脉冲 / 十字光标 | ✓ 都用真实 SVG / CSS keyframes 实现，未用 emoji 替代 |

## Commit

- 网站仓：`~/Coding/Archer/style-vault/` · `feat(preview): add mission-ops + tactical-hud preview (12 条)` · 13 files / 4711 insertions
- skill 仓：（步骤 8 末尾）`feat(style-vault): add mission-ops + tactical-hud (12 条 · 4 tokens + 2 components + 2 blocks + 2 pages + 2 styles)`
- **两仓均未 push**，保留给用户

## 校验通过

- `yarn sync`：✓ synced 145 items，0 error
- `tsc --noEmit`：静默通过，无类型错误

## 下一步

1. `cd ~/Coding/Archer/style-vault/frontend && yarn dev`
   浏览器打开 vault 网站，左侧导航选 styles → admin-console → 两条 style 看实际效果
2. 肉眼过 12 条 preview，对比 mockup 原版（`~/Documents/company/ikt-docs/数据同步/docs/plans/2026-05-20-aura-redesign-mockups/mockup-v3-A-nasa.html` 和 `mockup-v3-C-hud.html`）
3. 若 OK：两仓各自 `git push`
4. 若发现细节问题：用 modify-workflow 改对应条目，不要重新走 sediment 全流程

## 教训回写

本次沉淀过程中，用户两次纠正方向：
1. "不是产品呀" —— Tier 1 必出 1 product 的硬规矩在 from-project 用户起点是"风格样本"时不适用
2. "前端代码也要沉淀啊。除了 skill 不是有个前端仓库项目吗" —— 我中途差点只在 skill 仓写 .md 漏了网站仓 tsx

**判定**：第 1 个是"用户具体诉求 vs Tier 1 标准"的张力，**属一次小错**，不回写。第 2 个是 AI 对双仓机制不熟悉导致差点漏写网站仓，**属模式错的边缘**——但 SKILL.md / shared-workflow.md 步骤 6 已有明确双仓写入说明，是 AI 读得不够仔细而非 workflow 缺口。**不回写**，但作为以后沉淀的自检点：进 step 6 前必读步骤 6 "写入位置" 段确认双仓路径。

---

*由 style-vault-sediment skill 生成 · 来源：from-project*
