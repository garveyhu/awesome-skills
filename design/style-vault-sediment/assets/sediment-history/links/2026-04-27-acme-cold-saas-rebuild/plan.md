# 沉淀计划 · acme-cold-saas Tier 2 重构

日期：2026-04-27
作者：links
模式：modify + create（混合：1 product 改 refs + 1 style 重构 + 11 新增条目 + unlink 2）
起点：用户指定 product（重构第一版 demo product，从单薄扩到 Tier 2 体量）
档位：Tier 2 · 基础级（目标 12–18 条 · 实际 14 个文件变更）

## 目标

把 `products/acme-cold-saas` 从"单薄一页 demo"扩成完整冷感工业型监控 SaaS 产品的 Tier 2 设计系统聚合视图：5 段（风格/页面/模块/组件/原语）全部丰富，定位锐化为 DevOps 可观测性 SaaS。

## 涉及条目（依赖拓扑序，14 个文件变更）

### 新增（11 条）
1. `tokens/motion/acme/instant-snap`
2. `components/buttons/acme/cyan-cta`
3. `components/inputs/acme/mono-input`
4. `components/indicators/acme/status-pulse`
5. `blocks/nav/acme/saas-cold-topbar`
6. `blocks/display/acme/saas-metric-grid`
7. `blocks/display/acme/saas-data-table`
8. `blocks/feedback/acme/saas-status-banner`
9. `pages/auth/acme/auth-cold-split`
10. `pages/dashboard/acme/saas-monitor-overview`
11. `pages/list-table/acme/saas-incident-list`
12. `pages/pricing/acme/saas-cold-pricing`

### 重构（1 条）
13. `styles/saas-tool/cold-industrial-saas` · README 视觉特征段从 5 行扩到 ~15 行；preview tsx 增密；uses 数组扩展

### 修改 product（1 条）
14. `products/acme-cold-saas` · description 锐化为"冷感工业型监控 SaaS"；refs.pages 从 1 → 4；refs.blocks 从 2(unlink) → 4(新)；refs.components 从 1 → 4

### Unlink（不删 / 不挪）
- `blocks/layout/skillhub/toolbar-bar` —— 仍在 SkillHub 下保留
- `blocks/display/skillhub/table` —— 仍在 SkillHub 下保留

## 依赖关系

```
products/acme-cold-saas
  → styles/saas-tool/cold-industrial-saas
      → tokens/palettes/acme/slate-cyan-ice
      → tokens/typography/pairs/acme/ibm-plex-duo
      → tokens/motion/acme/instant-snap (新)
      → components/buttons/acme/{ghost-button, cyan-cta(新)}
      → components/inputs/acme/mono-input (新)
      → components/indicators/acme/status-pulse (新)
      → blocks/nav/acme/saas-cold-topbar (新)
      → blocks/display/acme/{saas-metric-grid, saas-data-table} (新)
      → blocks/feedback/acme/saas-status-banner (新)
      → pages/landing/acme/saas-landing
      → pages/auth/acme/auth-cold-split (新)
      → pages/dashboard/acme/saas-monitor-overview (新)
      → pages/list-table/acme/saas-incident-list (新)
      → pages/pricing/acme/saas-cold-pricing (新)
```

## 元信息填写方式

- AI 自动填（用户授权 Y）：全部 11 条新增
- 用户指令驱动：第 13、14 条（style 重构 + product 修改）

## 校验

- 档位区间：14 ∈ [12, 18] ✅
- 命名空间：所有新增按 `<bucket>/acme/<slug>` ✅
- tag/category：全部在 taxonomy.json
- 所有 refs 目标在写入完成后存在

## 执行状态

☑ 用户已确认 · 待写入

## Phase 1 前置（已完成）

- 网站仓 commit 32c5b14
- skill 仓 commit 5b6d919（+ 139194f cleanup）
- 整套 vault 已迁到 namespace 规则下，sync + build 全绿
