---
id: pages/dashboard/style-vault/profile-collections
type: page
name: 个人中心收藏页
description: 大头像 hero（96px Avatar + 名字 + 邮箱 + 编辑按钮）+ sticky 类型 tab + ResponsiveGrid 卡片网格 + 编辑资料 modal + 空态浮起图标
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - tokens/layout/_shared/responsive-grid
  - tokens/layout/_shared/scroll-state-system
preview: /preview/pages/dashboard/style-vault/profile-collections
---

# Profile Collections

> 个人中心 ·"用户 hero + 收藏网格 by type"两段结构。是 Style Vault 唯一的"用户私域"页面。

## 视觉特征

```
┌──────────────────────────────────────┐
│ 居中头像 hero（白底）                  │
│   Avatar 96 · 名字 32 · 邮箱 14       │
│   [ 编辑资料 ] [ ⋯ 更多 ]              │
├──────────────────────────────────────┤
│ Sticky Tab · 类型筛选（top-64）        │
│   产品 N · 风格 N · 页面 N · ...      │ ← antd 风灰底激活，但 indicator 是 2px 黑底
├──────────────────────────────────────┤
│ Collections grid（ResponsiveGrid）    │
│   ┌─┐ ┌─┐ ┌─┐ ┌─┐                   │
│   └─┘ └─┘ └─┘ └─┘                   │ ← StyleCard 复用
└──────────────────────────────────────┘

空态：
┌────────────┐
│  ◯ heart   │  ← 浮起白方块 + 大投影 + 灰心形
│  还没收藏... │
│  [去浏览]   │
└────────────┘
```

### Hero（白底）

- 容器 `bg-white`，内层 `mx-auto max-w-[1700px] px-8 sm:px-12 pb-10 pt-12 text-center`
- `<Avatar size={96}>` 居中，`border border-slate-200`，缺省时 `{user.name?.[0]?.toUpperCase()}` 大字 fallback
- 名字 `font-display text-[32px] font-bold tracking-tight`，邮箱 `text-[14px] text-slate-400`
- 操作组：`编辑资料` ghost-bordered-cta（`rounded-full h-10` + `<EditOutlined />`）+ 圆形 `更多 ⋯` 同款边框 ghost（开 antd Dropdown 看到"退出登录"）

### Sticky Tab

- 容器 `sticky top-[64px] z-10 border-b border-slate-200 bg-white/90 backdrop-blur`
- nav `flex items-center gap-8 overflow-x-auto`，每条 tab `py-4 text-[15px]`
- 文字 active `font-semibold text-slate-900` / idle `font-medium text-slate-500 hover:text-slate-900`
- tab 标签后跟 mono 数字 `font-mono text-[12px] tabular-nums`：active=slate-400 / idle=slate-300
- active indicator：`absolute -bottom-px h-[2px] bg-slate-900 rounded-t`（**纯黑下划线**，不走 cool-editorial 的 cyan→slate gradient — profile 是私域，更素一档）
- URL 同步：`useSearchParams` 读 `?tab=xxx`，无值时 fallback 第一个非空分组

### Collections Grid

- `<ResponsiveGrid mode="fixed" min={300} gap={20}>` —— 自适应列数，最小列宽 300px，gap 20
- 每条用 `StyleCard`（即 `blocks/display/style-vault/preview-thumb-card`），点击：
  - `type === 'product'` → 跳 `/products/{slug}`
  - 其它 → 跳 `/item/{id}`
- **滚动 / 懒加载**：走 [`tokens/layout/_shared/scroll-state-system`](../../../../tokens/layout/_shared/scroll-state-system.md)，grid 抽成 `<FavGrid cacheKey={\`profile:fav:${current.type}\`} />` 内部用 `useInfiniteList`。每 tab 自己的翻页进度跨切换保留；收藏数较少时不触发懒加载，体验和原来全量渲染一致。详细机制见 token 条目。

### 空态

- 大块 padding `py-20 text-center`
- 浮起白方块 `h-20 w-20 rounded-2xl border border-slate-200 bg-white shadow-[0_8px_30px_-8px_rgba(15,23,42,0.15)]` 居中，里面 32px slate-300 心形 icon
- 大字 `font-display text-[22px] font-semibold` + 副文 `text-[13px] text-slate-500`
- CTA `dark-pill-cta` "去浏览"

### 编辑资料 Modal

- antd `<Modal width={420} centered destroyOnClose footer={null}>`
- header 大字 `font-display text-[20px] font-semibold`
- 单字段：name input `h-11 rounded-lg border border-slate-200 px-3 text-[14px]` + focus `border-slate-900 focus:ring-0` —— **不走 cyan focus**，是 slate-900 黑边
- 底部右对齐两按钮：`取消`（ghost-bordered）+ `保存`（slate-900 实色 rounded-lg，**不是 rounded-full**，这是 modal 内的按钮变体）
- 保存触发 `toast.success('资料已更新')` 或 `toast.error(msg)` —— 嵌入 spring-toast

## 适配指南

- Hero / Tab / Grid **三段**之间靠 `border-b border-slate-200/100` 分割，**不用** padding 撑开
- Tab 高度 56px，hero 之后内容用 `top-[64px]` sticky 是因为这页**没有 TopBar**？不，TopBar 也在，所以累加。**直接用项目里的实测值**：sticky `top-[64px]` 对应"无 TopBar 偏移"的特殊布局，因为 ProfilePage 用了独立的 max-w 1700 排版宽度，比其他页宽 100px
- 编辑 modal 的"name 字段 focus 黑边"是私域专属——**不要**复用 cyan focus（那是浏览态的高亮）
- Modal 内按钮形状 `rounded-lg`（8px）不是 `rounded-full`——modal 是"操作集中地"，胶囊形态会喧宾夺主
- 收藏取消（在 StyleCard 内）触发 grid 自动重排——别加额外 transition，复用 StyleCard 自带的卡片浮起即可

## 反模式

- 不要在 hero 加 banner / KPI 数字（profile 是简洁的人物名片，不是 dashboard 大屏）
- 不要把 Tab 下划线改成 editorial-underline-tab 的 gradient（profile 私域 = 素 + 黑）
- 不要把空态心形换成 emoji / 彩色图（保持 slate 灰阶）
- 不要在编辑 modal 加超过 2-3 个字段（多字段拆出独立 settings 页）
- 不要让 Grid `min` < 280 或 > 360（视觉密度的甜区）
