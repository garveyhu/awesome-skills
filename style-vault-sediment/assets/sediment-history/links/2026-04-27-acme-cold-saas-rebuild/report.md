# 沉淀报告 · acme-cold-saas Tier 2 重构

日期：2026-04-27
模式：modify + create（混合）
起点：用户指定 product（重构第一版 demo product）
档位：Tier 2 · 基础级（目标 12-18 · 实际 14 个文件变更）
作者：links

## 改了什么

### 新增 11 条（按拓扑序）
1. `tokens/motion/acme/instant-snap` · 工业冷感零浪漫动效
2. `components/buttons/acme/cyan-cta` · 主 CTA（cyan 实色）
3. `components/inputs/acme/mono-input` · 等宽数字输入
4. `components/indicators/acme/status-pulse` · 四态脉冲点
5. `blocks/nav/acme/saas-cold-topbar` · 56px 全局顶栏
6. `blocks/display/acme/saas-metric-grid` · KPI 4 列网格
7. `blocks/display/acme/saas-data-table` · 高密度紧凑表格
8. `blocks/feedback/acme/saas-status-banner` · 32px 三态告警条
9. `pages/auth/acme/auth-cold-split` · 60/40 双栏登录
10. `pages/dashboard/acme/saas-monitor-overview` · 监控主页
11. `pages/list-table/acme/saas-incident-list` · 事件列表
12. `pages/pricing/acme/saas-cold-pricing` · 定价页

### 重构 1 条
- `styles/saas-tool/cold-industrial-saas`
  - README "视觉特征" 段从 5 行扩到 ~20 行；新增"设计哲学" / "设计原则" / "Tokens 注入" 三段
  - uses 数组从 4 条 → 16 条
  - preview tsx 顶部加 status banner（neutral 态），ServicesTable 中 healthy 状态点改为带呼吸光晕

### 修改 product 1 条
- `products/acme-cold-saas`
  - description: "为量化团队打造的效率驾驶舱" → "冷感工业型监控 SaaS——把注意力留给数据本身"
  - refs.pages: 1 → 5
  - refs.blocks: 2 unlink + 4 新（不含 toolbar-bar/table，它们仍在 SkillHub 下保留）
  - refs.components: 1 → 4
  - 设计叙事段重写

## 元信息来源

- AI 自动填（用户授权 Y）：第 1-12 条全部新增
- 用户决策驱动 + AI 起草：第 13、14 条

## 命名规则（本次首次应用）

所有新条目按 Phase 1 引入的 namespace 规则：`<bucket>/acme/<slug>`
（详见 [`style-vault/references/README.md` · Namespace 子目录](../../../../../style-vault/references/README.md#namespace-子目录强制)）

## Unlink（不删 / 不挪）

- `blocks/layout/skillhub/toolbar-bar` —— 仍属 SkillHub
- `blocks/display/skillhub/table` —— 仍属 SkillHub

它们当时被 acme 错引用，本次从 acme.refs.blocks 移除。

## 校验结果

- `yarn sync` · 56 entries · 0 error 0 warning ✅
- `yarn build` · 0 error ✅
- 档位区间 14 ∈ [12, 18] ✅
- 所有 ref 目标存在 ✅

## Commit

- skill 仓：`feat(style-vault): rebuild acme-cold-saas Tier 2 (12 new + 1 style refactor + 1 product update)`
- 网站仓：`feat(preview): add acme-cold-saas Tier 2 previews (12 new + 1 style refactor) + tweak ProductListPage spacing`
- **均未 push**

## 顺手改动

ProductListPage 顶部间距从 `pt-10` → `pt-4`（用户截图反馈），同时进 vault 仓 commit。

## 下一步

1. `cd $VAULT/frontend && yarn dev` 肉眼过：
   - `/products/acme-cold-saas` 5 段是否完整、配色统一
   - 各 preview 单独打开 `/item/<id>` 查看密度与等宽数字效果
   - 顶部间距是否合适
2. OK 后 `git push` 两仓
3. 发现问题 `git reset --soft HEAD~1` 回到工作区

---
*由 style-vault-sediment skill 生成 · 模式：create+modify · Phase 2 of 2-phase rebuild*
