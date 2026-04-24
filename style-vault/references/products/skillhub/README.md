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
    - pages/landing/skill-community-home
    - pages/list-table/admin-console
  blocks:
    - blocks/nav/glass-pill-navbar
    - blocks/marketing/gradient-hero
    - blocks/display/skill-card
    - blocks/display/leaderboard-row
    - blocks/display/table
    - blocks/layout/toolbar-bar
  components:
    - components/tags-badges/teal-pill
    - components/avatars-icons/letter-avatar
    - components/buttons/border-trace-cta
  tokens:
    palette: tokens/palettes/skillhub-teal-mist
    typography: tokens/typography/pairs/inter-jetbrains-duo
    motion: tokens/motion/gentle-flow
    shadow: tokens/shadow/ambient-float
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

整站用 teal-500 做唯一交互强调色（搜索、分页激活、分类 pill），nav 激活用 slate-900 黑胶囊，品牌 CTA 用追光黑按钮——三条色线分工清晰、不打架。

动效是"温和流动"——卡片 hover `y:-4` 浮起、按钮 tap `scale:0.95` 回弹、hero 强调词 14s 四色流光循环、"发布 Skill"按钮外缘 3s 追光；没有 bounce、没有大段过渡，节奏偏克制。

## 组成

- **Style**：`styles/community-social/skillhub-soft-modernist` · 整站调性锚点
- **Pages**：
  - `pages/landing/skill-community-home` · 发现 / 首页（hero + 榜单 + 分类 + 搜索 + 网格）
  - `pages/list-table/admin-console` · 多域管理后台（Tabs + toolbar + table）
- **Blocks**：
  - `blocks/nav/glass-pill-navbar` · 全站 navbar
  - `blocks/marketing/gradient-hero` · 流光 hero
  - `blocks/display/skill-card` · 发现页卡片
  - `blocks/display/leaderboard-row` · Top Skills 榜单行
  - `blocks/display/table`（复用）· 管理后台表格
  - `blocks/layout/toolbar-bar`（复用）· 表格顶部工具栏
- **Components**：
  - `components/tags-badges/teal-pill` · 分类 / 标签胶囊
  - `components/avatars-icons/letter-avatar` · 字母头像（真实头像降级）
  - `components/buttons/border-trace-cta` · 发布 Skill 追光按钮
- **Tokens**：
  - `tokens/palettes/skillhub-teal-mist` · Teal 主色 + Slate 中性 + 12 色头像 + 流光 4 色
  - `tokens/typography/pairs/inter-jetbrains-duo` · Inter + JetBrains Mono
  - `tokens/motion/gentle-flow` · framer-motion + CSS flow-right + SVG 追光
  - `tokens/shadow/ambient-float` · 超轻 ambient + hover md + pulse 辉光
