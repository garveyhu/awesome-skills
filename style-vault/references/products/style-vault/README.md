---
id: products/style-vault
type: product
name: Style Vault · 风格库
description: 为 AI 编码而造的设计风格库——六个层级（token / component / block / page / style / product），AI 复用每条资产时自带风格不出 AI 味
platforms: [web]
theme: light
category: design
refs:
  style: styles/portfolio-studio/style-vault-cool-editorial
  pages:
    - pages/landing/style-vault/editorial-cool-landing
    - pages/detail/style-vault/sticky-toc-product
    - pages/detail/style-vault/sidebar-preview-detail
    - pages/list-table/style-vault/category-row-browse
    - pages/dashboard/style-vault/profile-collections
  blocks:
    - blocks/marketing/style-vault/cool-blob-hero
    - blocks/display/style-vault/preview-thumb-card
    - blocks/display/style-vault/floating-cover-row
    - blocks/layout/style-vault/browser-chrome-frame
    - blocks/nav/style-vault/sticky-platform-topbar
  components:
    - components/buttons/style-vault/dark-pill-cta
    - components/buttons/style-vault/ghost-bordered-cta
    - components/tags-badges/style-vault/cyan-dot-meta-pill
    - components/toggles/style-vault/editorial-underline-tab
    - components/overlays/style-vault/spring-toast
  tokens:
    palette: tokens/palettes/style-vault/slate-cyan-cool
    typography: tokens/typography/pairs/style-vault/inter-editorial-display
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, cold, confident]
  stack: [react-antd-tailwind]
uses: []
---

## 设计叙事

Style Vault 是为 AI 编码协作打造的设计风格库——把"风格"按粒度切成六层，每条资产带 Prompt 模板，让 AI 写出的代码自带风格而非"AI slop"美学。

- **作品才是主角**：所有视觉决策让位于"让作品被看见"——dark CTA 同屏 1 个、cyan accent ≤ 3 处、blob 只在 hero
- **白上叠白靠 hairline**：白卡叠在 #fafafa 浅底上，靠 1px slate hairline 区分；hover 才用三层柔投影把卡片浮起
- **冷不冷漠**：cyan blob + 标题渐变（cyan-700 → slate-900）+ manifesto italic（"看见 / 记住"）让冷里有温度
- **编辑式呼吸**：section py-32 / Logo 墙 gap-12 / 价值段 space-y-36 —— 留白是身份
- **Mono 撑数字**：所有索引（01/02/03）/ ID 字串 / 数字徽标用 mono —— 编辑节奏锚点
- **单字族打天下**：Inter 一种字，靠尺寸 + letter-spacing + uppercase tracking 拉层级，不引第二种字族

## 组成（Tier 2 · 20 条聚合）

### Style
- `styles/portfolio-studio/style-vault-cool-editorial` · 整站调性

### Pages · 5 条

| 路由 | Page | 用途 |
|---|---|---|
| `/` | `pages/landing/style-vault/editorial-cool-landing` | 落地页（hero + Logo 墙 + 3 段价值叙事 + manifesto + footer） |
| `/products/:slug` | `pages/detail/style-vault/sticky-toc-product` | 产品详情（cover hero + sticky 数字 TOC + masonry 分段） |
| `/item/*` | `pages/detail/style-vault/sidebar-preview-detail` | 单条 item 详情（340px sidebar + 右列 chrome 预览框） |
| `/browse` | `pages/list-table/style-vault/category-row-browse` | 浏览页（双 sticky 导航 + 每类一行卡片） |
| `/profile` | `pages/dashboard/style-vault/profile-collections` | 个人中心（头像 hero + 类型 tab + 收藏网格 + 编辑 modal） |

### Blocks · 5 条

- `blocks/marketing/style-vault/cool-blob-hero` · 占首屏 hero（双 blob + fade-up cascade + dark CTA）
- `blocks/display/style-vault/preview-thumb-card` · 1440 虚拟视口缩放卡片（StyleCard）
- `blocks/display/style-vault/floating-cover-row` · 浮起作品照行卡（产品列表）
- `blocks/layout/style-vault/browser-chrome-frame` · mac dot 浏览器 chrome + 视口选择器
- `blocks/nav/style-vault/sticky-platform-topbar` · sticky 玻璃感顶栏 + 视口绝对居中 platform pill

### Components · 5 条

- `components/buttons/style-vault/dark-pill-cta` · slate-900 rounded-full 主 CTA（带深柔投影）
- `components/buttons/style-vault/ghost-bordered-cta` · 1.5px 描边幽灵次 CTA（hover 收紧）
- `components/tags-badges/style-vault/cyan-dot-meta-pill` · 玻璃感 uppercase tracking pill
- `components/toggles/style-vault/editorial-underline-tab` · scaleX cyan→slate-900 渐变 underline tab
- `components/overlays/style-vault/spring-toast` · spring overshoot 顶部居中胶囊操作回执

### Tokens · 4 条

- `tokens/palettes/style-vault/slate-cyan-cool` · 配色（slate 全阶 + cyan 单点 + #fafafa 底）
- `tokens/typography/pairs/style-vault/inter-editorial-display` · 字体（Inter 单字族 + display 字距 + ss01 features）
- `tokens/gradient/style-vault/cool-blob-decor` · 双 blob 漂浮装饰（**signature 元素**）
- `tokens/motion/style-vault/editorial-flow` · 标志 cubic-bezier(0.2,0.7,0.2,1) + fade-up cascade + 卡片浮起

## 复刻要点

要做出"Style Vault 风"的设计目录站，最小动作：

1. 套 `styles/portfolio-studio/style-vault-cool-editorial` 注入 CSS 变量
2. Hero 直接用 `cool-blob-hero` —— blob 是签名
3. TopBar 用 `sticky-platform-topbar` —— 玻璃感 + 视口绝对居中 pill
4. 列表卡片用 `preview-thumb-card`（虚拟视口缩放真组件）
5. 详情页右列用 `browser-chrome-frame`，左列窄 sidebar
6. 主 CTA 一律 `dark-pill-cta`，次 CTA `ghost-bordered-cta`
7. Section eyebrow / item meta / type 标识全用 `cyan-dot-meta-pill`
8. 大栏目导航用 `editorial-underline-tab`（scaleX gradient 是身份）
9. 节奏：mono 索引 01/02/03 + uppercase tracking caption + section py-32 留白

## 不要复制的反模式

- 不要在 hero 之外用 blob —— 氛围泛滥
- 不要给卡片加 scale 整卡放大 —— 违反"卡片浮起 + 内容缩放"的分离
- 不要把 cyan 当大面积背景 —— 破坏单点高亮
- 不要 manifesto 之外的段加 dark panel —— dark 是 manifesto 语义
- 不要引衬线字 / 第二种 sans —— Inter 一种字到底
- 不要 sentence-case caption —— uppercase + tracking 是身份

## 调性定位

| 维度 | 选择 |
|---|---|
| 网站类别 | 设计目录 / 作品 portfolio / 风格库 / design system showcase |
| 主要受众 | 设计师 / AI 编码协作者 / 寻找视觉灵感的开发者 |
| 关键差异点 | 不是"漂亮模板站"（dribbble），而是"按粒度切割的设计语言库"——每条都附 Prompt 给 AI 用 |
| 适配 vs 不适配 | ✓ 设计 portfolio / 内容目录 / 灵感库；✗ 电商 / 社交 / SaaS 控制台 |
