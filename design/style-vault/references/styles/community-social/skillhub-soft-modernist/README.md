---
id: styles/community-social/skillhub-soft-modernist
type: style
name: SkillHub 柔雾现代风
description: 浅色底 + teal 主色 + 玻璃 pill 导航 + 彩虹流光 + 12 色柔和头像 + framer-motion 微动，社区 × 工具双重气质
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/skillhub/skillhub-teal-mist
  - tokens/typography/pairs/skillhub/inter-jetbrains-duo
  - tokens/motion/skillhub/gentle-flow
  - tokens/shadow/skillhub/ambient-float
  - components/buttons/skillhub/dark-primary-cta
  - components/buttons/skillhub/border-trace-cta
  - components/inputs/skillhub/soft-form-input
  - components/tags-badges/skillhub/teal-pill
  - components/avatars-icons/skillhub/letter-avatar
  - components/indicators/skillhub/pulse-dot
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
preview: /preview/styles/community-social/skillhub-soft-modernist
---

# SkillHub Soft Modernist

> 社区工具型产品的整站调性——浅色底、内容至上、teal 做唯一交互强调、navbar 玻璃 + pill 浮在顶端、hero 用流光字引导注意力、卡片 / 榜单 / 表格三级信息密度

## 视觉语言

### 1. 色彩
- **主底**：`#f5f7fa`（近白但带极淡 slate）;  容器 `#ffffff`
- **主字**：`gray-900`（#111827）标题；`gray-500/600` 正文；`gray-400` 元信息
- **主色 Teal**：分类胶囊 / 搜索按钮 / 分页激活；`teal-500` 主态、`teal-600` 悬浮
- **CTA 黑**：`#1a1a1a`（登录 / 发布实践）; nav 激活胶囊 `#2b2b2b`
- **流光四色**：teal → cyan → sky → rose → teal，只出现在 Hero 强调词
- **12 色头像 + 3 色 Rank**：辅助身份辨识，不作主色
- **状态色**：emerald（正常）/ orange（通知）/ rose（错误）

### 2. 字体
- Inter（正文）+ Space Grotesk（备选）+ JetBrains Mono（代码）
- 开启 cv02 / cv03 / cv04 / cv11 特性
- 大标题 `extrabold tracking-tight leading-[1.15]`；正文 `medium leading-relaxed`
- Meta 全部 `uppercase tracking-wider text-xs font-bold text-gray-400`

### 3. 圆角
- 软现代：`rounded-xl` (12px) 输入 / 按钮；`rounded-2xl` (16px) 卡片 / pill；`rounded-full` 胶囊、头像
- Antd ConfigProvider `borderRadius: 8`（菜单 / Tab / 等内部控件）

### 4. 阴影
- 静态 `0 1px 4px rgba(0,0,0,0.04)`（Navbar pill 用）
- 卡片默认无阴影，hover 才 `shadow-md`
- Pulse 辉光只给状态点

### 5. 动效
- 入场 `fade + y: 20`（modules）/ `y: 24`（sections），`duration: 0.3`
- Hover `y: -4`（卡片浮）/ `scale: 1.03`（按钮）
- Tap `scale: 0.95-0.97`
- 装饰 flow 渐变 `14s`（hero 字）/ `20s`（追光 overlay）
- SVG 追光 3s / 4.5s 双环

### 6. 层级
- Navbar 浮（玻璃 + 内 pill）
- Hero 全宽（白底 + 流光）
- 榜单 `max-w-4xl`（紧凑一体）
- 分类 / 搜索 `max-w-2xl-7xl`
- 卡片网格 `max-w-7xl` 3 列
- 管理后台 `max-w-7xl` + Tabs

## 适配指南

### 注入变量
```css
/* Tailwind v4 @theme 注入 */
@theme {
  --font-sans: 'Inter', 'Space Grotesk', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  --color-primary-50:  #f0fdfa;
  --color-primary-500: #14b8a6;
  --color-primary-600: #0d9488;
  /* ... */
}
```

### Antd ConfigProvider
```tsx
<ConfigProvider theme={{
  token: {
    colorPrimary: '#0f172a',
    borderRadius: 8,
    fontFamily: '"Inter", "Space Grotesk", system-ui, sans-serif',
  },
}}>
  ...
</ConfigProvider>
```

### 全局 keyframes
```css
@keyframes flow-right { from { background-position: 300% 50%; } to { background-position: 0% 50%; } }
@keyframes shimmer    { 0%,100% { background-position: 100% 50%; } 50% { background-position: 0% 50%; } }
@keyframes fadeIn     { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }
```

### 组合规则
- 全局只留 1 个 BorderTraceButton，其它 CTA 用纯黑 / ghost
- 榜单后必接网格，两种"列表"形态不混用
- 表格区域（管理 / 详情）必须用 `blocks/display/skillhub/table` + `blocks/layout/skillhub/toolbar-bar` 组合，不要自己写
- 所有头像降级：真实 URL 不在 → LetterAvatar

## 反模式

- 不要在内容区（hero 外）再做流光 / 多色渐变——视觉聚焦只给 hero
- 不要用深色底（除非明确切换到 dark theme——但此 style preview 是 light 定调）
- 不要把 teal 放进正文字体色——它只进按钮 / 标签 / 链接 / 分页
- 不要把 navbar pill 替换成全宽顶栏——那是另一种 style（saas-tool 系）
- 不要叠 3 种以上的 shadow 层级——最多 2 层（静 ambient + 交互 md）

## 反差 · 和 `cold-industrial-saas` 的区别

| 维度 | skillhub-soft-modernist | cold-industrial-saas |
|---|---|---|
| theme | light（默认） | both（偏 dark） |
| 主色 | teal-500（绿蓝） | cyan-400（冷蓝） |
| 字体 | Inter + JetBrains Mono | IBM Plex Sans + Plex Mono |
| 圆角 | 12-16px（软）| ≤ 4px（硬）|
| 阴影 | 有（轻微） | 无 |
| 密度 | 中—疏 | 紧凑 |
| 气质 | 社区 × 工具 | quant 驾驶舱 |
| 动效 | framer-motion 微动 | 150ms ease-out 简过渡 |

两种 style 不要混用——选一。
