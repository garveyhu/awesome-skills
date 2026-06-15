# 沉淀计划 · SkillHub

日期：2026-04-24
作者：links
模式：create
起点：from-project (`/Users/links/Coding/A-complex/ikt/skills/skillhub`)

## 目标

将 SkillHub（AI Agent 技能社区平台）的视觉风格全量沉淀到 style-vault，覆盖六层资产。
SkillHub 视觉 DNA：浅色为底 + teal 主色 + 玻璃 pill 导航 + 彩虹流动渐变 + 12 色柔和头像 + framer-motion 微动效。

## 涉及条目（依赖拓扑序 · 14 新增 + 2 复用）

### Tokens（4 新增）

1. `tokens/palettes/skillhub-teal-mist`
2. `tokens/typography/pairs/inter-jetbrains-duo`
3. `tokens/motion/gentle-flow`
4. `tokens/shadow/ambient-float`

### Components（3 新增）

5. `components/tags-badges/teal-pill`
6. `components/avatars-icons/letter-avatar`
7. `components/buttons/border-trace-cta`

### Blocks（4 新增 + 2 复用）

- `blocks/display/table`（已存在 · 复用）
- `blocks/layout/toolbar-bar`（已存在 · 复用）

8. `blocks/nav/glass-pill-navbar`
9. `blocks/marketing/gradient-hero`
10. `blocks/display/skill-card`
11. `blocks/display/leaderboard-row`

### Pages（2 新增）

12. `pages/landing/skill-community-home`
13. `pages/list-table/admin-console`

### Style（1 新增）

14. `styles/community-social/skillhub-soft-modernist`

### Product（1 新增）

15. `products/skillhub`

## 依赖关系

```
products/skillhub
  └─ refs.style → styles/community-social/skillhub-soft-modernist
       └─ uses:
            tokens/palettes/skillhub-teal-mist
            tokens/typography/pairs/inter-jetbrains-duo
            tokens/motion/gentle-flow
            tokens/shadow/ambient-float
            components/tags-badges/teal-pill
            components/avatars-icons/letter-avatar
            components/buttons/border-trace-cta
            blocks/nav/glass-pill-navbar
            blocks/marketing/gradient-hero
            blocks/display/skill-card
            blocks/display/leaderboard-row
            blocks/display/table          (复用)
            blocks/layout/toolbar-bar     (复用)
            pages/landing/skill-community-home
            pages/list-table/admin-console
```

## 元信息填写方式

- AI 自动填（用户已授权 Y）：全部 15 条新增
- 用户手填：无

## 用户在 review 阶段的定制

- product category：`productivity`
- block #11 名字：`ranking-list-row` → `leaderboard-row`

## 视觉定位（全部新条目共用的元信息底盘）

- theme: `light`
- platforms: `[web]`
- tags.aesthetic: `[minimal, editorial]`
- tags.mood: `[calm, confident]`
- tags.stack: `[react-antd-tailwind]`

## 执行状态

☑ 用户已确认 · VAULT_OK=true（双仓同步）· 已上锁 · 待写入
