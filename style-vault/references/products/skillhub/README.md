---
id: products/skillhub
type: product
name: SkillHub · AI 技能社区平台
description: 聚合 Git 仓库扫描 SKILL.md 的技能发现、投稿、实践与管理平台
platforms: [web]
theme: light
category: productivity
refs:
  style: styles/community-social/skillhub-soft-modernist
  pages:
    - pages/landing/skillhub/skill-community-home
    - pages/detail/skillhub/skill-article-detail
    - pages/form-flow/skillhub/skill-publish-wizard
    - pages/list-table/skillhub/practice-plaza
    - pages/detail/skillhub/practice-post-detail
    - pages/form-flow/skillhub/practice-compose
    - pages/content-reader/skillhub/im-conversation
    - pages/dashboard/skillhub/user-home
    - pages/form-flow/skillhub/profile-edit
    - pages/detail/skillhub/user-public-profile
    - pages/auth/skillhub/auth-split
    - pages/list-table/skillhub/admin-console
    - pages/dashboard/skillhub/admin-overview
  blocks:
    - blocks/nav/skillhub/glass-pill-navbar
    - blocks/marketing/skillhub/gradient-hero
    - blocks/display/skillhub/skill-card
    - blocks/display/skillhub/leaderboard-row
    - blocks/display/skillhub/gradient-stat-card
    - blocks/display/skillhub/table
    - blocks/layout/skillhub/toolbar-bar
    - blocks/form/skillhub/auth-split-form
    - blocks/form/skillhub/profile-edit-form
    - blocks/feedback/skillhub/skeleton-card
    - blocks/feedback/skillhub/empty-state
  components:
    - components/buttons/skillhub/dark-primary-cta
    - components/buttons/skillhub/border-trace-cta
    - components/inputs/skillhub/soft-form-input
    - components/tags-badges/skillhub/teal-pill
    - components/avatars-icons/skillhub/letter-avatar
    - components/indicators/skillhub/pulse-dot
  tokens:
    palette: tokens/palettes/skillhub/skillhub-teal-mist
    typography: tokens/typography/pairs/skillhub/inter-jetbrains-duo
    motion: tokens/motion/skillhub/gentle-flow
    shadow: tokens/shadow/skillhub/ambient-float
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses: []
---

## 设计叙事

SkillHub 的视觉是"社区 × 工具"双重身份的平衡：

- **社区身份**：首页用流光 hero 字 + 12 色柔和头像 + 玻璃 pill 导航带来轻快感——第一眼不像冷冰冰的 SaaS
- **工具身份**：往下一滚立刻切到榜单、表格、分类网格——信息密度高、排版严谨、meta 字 uppercase tracking-wider

整站用 teal-500 做唯一交互强调色（搜索、分页激活、分类 pill），品牌/动作 CTA 统一 `#1a1a1a` / slate-900 黑底 + `active:scale-95` 回弹（这是跨 9 个文件 19 处的"负空间一致性"骨架），品牌发布按钮用追光黑；三条色线分工清晰、不打架。

运营概览是整站**唯一**的多彩表达——indigo / blue / purple / emerald 四色 stat card 配色阴影，来承载"运营仪表盘"的信息密度；正常业务面保持 teal + slate 单色调。

动效是"温和流动"——卡片 hover `y:-4` 浮起、按钮 tap `scale:0.95` 回弹、hero 强调词 14s 四色流光循环、"发布 Skill"按钮外缘 3s 追光；没有 bounce、没有大段过渡，节奏偏克制。

## 组成（Tier 3 全量覆盖）

### Style
- `styles/community-social/skillhub-soft-modernist` · 整站调性锚点

### Pages · 13 条主路由全覆盖

| 路由 | Page 条目 | 用途 |
|---|---|---|
| `/` → `/discover` | `pages/landing/skillhub/skill-community-home` | 发现首页（hero + 榜单 + 网格）|
| `/skills/:slug` | `pages/detail/skillhub/skill-article-detail` | 技能详情（markdown + sidebar）|
| `/skills/submit` | `pages/form-flow/skillhub/skill-publish-wizard` | 发布技能向导 |
| `/practice` | `pages/list-table/skillhub/practice-plaza` | 实践广场 |
| `/practice/:id` | `pages/detail/skillhub/practice-post-detail` | 实践详情（单栏长文）|
| `/practice/create` | `pages/form-flow/skillhub/practice-compose` | 发布实践编辑器 |
| `/messages` | `pages/content-reader/skillhub/im-conversation` | 消息会话 |
| `/me` | `pages/dashboard/skillhub/user-home` | 用户中心 |
| `/me/edit` | `pages/form-flow/skillhub/profile-edit` | 编辑资料 |
| `/users/:id` | `pages/detail/skillhub/user-public-profile` | 他人主页 |
| `/login` + `/register` | `pages/auth/skillhub/auth-split` | 登录分屏 |
| `/admin` | `pages/list-table/skillhub/admin-console` | 管理后台（Tabs 骨架）|
| `/admin` overview tab | `pages/dashboard/skillhub/admin-overview` | 运营概览（渐变 stat card）|

### Blocks
- Nav：`blocks/nav/skillhub/glass-pill-navbar` · 全站玻璃 pill 导航
- Marketing：`blocks/marketing/skillhub/gradient-hero` · 流光 hero
- Display：`skill-card` · `leaderboard-row` · `gradient-stat-card` · `table`（复用）
- Form：`auth-split-form` · `profile-edit-form`
- Layout：`toolbar-bar`（复用）
- Feedback：`skeleton-card` · `empty-state`

### Components
- Buttons：`dark-primary-cta`（全站统一黑白骨架）· `border-trace-cta`（品牌追光 CTA）
- Inputs：`soft-form-input`（表单字段统一）
- Tags：`teal-pill`
- Avatars：`letter-avatar`
- Indicators：`pulse-dot`

### Tokens
- Palette：`skillhub-teal-mist` · 5-group（primary teal / slate / avatar 12色 / rank 3色 / gradient 4色）
- Typography：`inter-jetbrains-duo` · Inter + JetBrains Mono + cv02/03/04/11
- Motion：`gentle-flow` · framer-motion + CSS flow-right + SVG 追光
- Shadow：`ambient-float` · 超轻 ambient + hover md + pulse 辉光
