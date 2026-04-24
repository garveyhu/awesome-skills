# 沉淀报告 · SkillHub

日期：2026-04-24
模式：create
起点：from-project (`/Users/links/Coding/A-complex/ikt/skills/skillhub`)
作者：links

## 涉及条目（15 新增 + 2 复用）

| 操作 | 类型 | ID | 名称 | 分类 / 标签 |
|---|---|---|---|---|
| 新增 | token | `tokens/palettes/skillhub-teal-mist` | SkillHub 柔雾 Teal 调色板 | aesthetic:[minimal,editorial] · mood:[calm,confident] |
| 新增 | token | `tokens/typography/pairs/inter-jetbrains-duo` | Inter × JetBrains Mono 字体对 | 同上 |
| 新增 | token | `tokens/motion/gentle-flow` | 温和流动动效系统 | 同上 |
| 新增 | token | `tokens/shadow/ambient-float` | 环境悬浮阴影 | 同上 |
| 新增 | component | `components/tags-badges/teal-pill` | Teal 胶囊标签 | stack:[react-antd-tailwind] |
| 新增 | component | `components/avatars-icons/letter-avatar` | 12 色柔和字母头像 | 同上 |
| 新增 | component | `components/buttons/border-trace-cta` | 追光边框 CTA | 同上 |
| 新增 | block | `blocks/nav/glass-pill-navbar` | 玻璃 Pill 导航栏 | 同上 |
| 新增 | block | `blocks/marketing/gradient-hero` | 流光渐变 Hero | 同上 |
| 新增 | block | `blocks/display/skill-card` | Skill 卡片 | 同上 |
| 新增 | block | `blocks/display/leaderboard-row` | 榜单行 | 同上 |
| **复用** | block | `blocks/display/table` | 管理后台表格 | — |
| **复用** | block | `blocks/layout/toolbar-bar` | 管理后台工具栏 | — |
| 新增 | page | `pages/landing/skill-community-home` | 技能社区首页 | 同上 |
| 新增 | page | `pages/list-table/admin-console` | 多域管理后台 | 同上 |
| 新增 | style | `styles/community-social/skillhub-soft-modernist` | SkillHub 柔雾现代风 | 同上 · theme:light |
| 新增 | product | `products/skillhub` | SkillHub · AI 技能社区平台 | category:productivity |

## 元信息来源

- **AI 自动填（Y 模式授权）**：全部 15 条
- **用户在 review 阶段手改**：
  - block 命名 `ranking-list-row` → `leaderboard-row`
  - product category 锁定 `productivity`
- 纯手填：无

## 分类决策说明

### aesthetic / mood 选择
- `minimal` —— 浅色、克制、内容优先
- `editorial` —— 强排版、大号 extrabold + uppercase tracking-wider 的 meta 字、prose 样式精修
- `mood: calm` —— 主色 teal 偏绿松、非燥动；动效缓慢（14s flow，300ms 入场）
- `mood: confident` —— Hero 大字 `text-6xl extrabold`、rank 色块、玻璃 pill 浮感；不怯场

### product category：productivity
SkillHub 在功能上兼社区与工具——但**主导价值是"发现 + 使用 AI 技能"**（工具型），
社区面（实践广场 / 私信 / 关注）是围绕技能展开的二级功能。

### 非选项说明
- 没挂 `social` category：social 更适合纯关系链驱动的产品（微博式动态流）
- 没挂 `theme: both`：skillhub 几乎没有 dark 主题实现；硬挂 both 是对不上实情

## 关键视觉决策

1. **teal 主色 vs slate-900 CTA 并存**：两条色线分工——teal 给交互强调（搜索 / 分类 / 分页激活），slate-900/#1a1a1a 给 CTA 与 nav 激活。分工清晰、不内耗
2. **流光只保留 1 处**：Hero 强调词 14s 循环 + border-trace 按钮 3s 追光 = 两处装饰动效，分属"文字流"与"边缘流"不重叠
3. **头像 12 色独立 palette**：没有并入主调色板，因为 12 色是"辨识而非主色"的工具，混进主色会稀释
4. **蓝 / 青 / 紫 / 粉 四色流光**：包含暖粉是为了打破纯冷调，给社区感加一点人味；但止步于此，不扩到正文配色

## Commit

- **Skill 仓 (`~/.agents/skills`)**：待提交（本报告写入后聚合 commit）
- **网站仓 (`~/Coding/Archer/style-vault`)**：`4d0fb79` · `feat(preview): add skillhub sediment preview (14 items)`
- **均未 push**

## 下一步

1. `cd ~/Coding/Archer/style-vault/frontend && yarn dev` 肉眼 review 所有 preview
2. OK 后分别 `git push origin main` 两仓
3. 发现问题用 `git reset --soft HEAD~1` 回到工作区再调

## 与既有 `products/acme-cold-saas` 的关系

这次沉淀**完全独立**。skillhub 用的 style 是新建的 `styles/community-social/skillhub-soft-modernist`，与 `styles/saas-tool/cold-industrial-saas` 是两个平行风格谱系：

- cold-industrial-saas：暗底、冷蓝、IBM Plex、无阴影、150ms 简过渡 —— 给 quant 驾驶舱
- skillhub-soft-modernist：浅底、teal + 彩虹流光、Inter、超轻阴影、framer-motion 微动 —— 给社区工具

复用的只有 `blocks/display/table` + `blocks/layout/toolbar-bar`（两者都适合"管理后台"骨架，不挑上层风格）。

---
*由 style-vault-sediment skill 生成 · 来源：from-project*
