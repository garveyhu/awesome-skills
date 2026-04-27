---
id: styles/portfolio-studio/style-vault-cool-editorial
type: style
name: 冷感 Editorial 设计目录站
description: "浅底 #fafafa + slate-cyan 冷感 + Inter 单字族 editorial 节奏 + 漂浮 blob 装饰 + 浮起卡片 — 设计目录 / portfolio 网站的整站调性"
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, cold, confident]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/style-vault/slate-cyan-cool
  - tokens/typography/pairs/style-vault/inter-editorial-display
  - tokens/gradient/style-vault/cool-blob-decor
  - tokens/motion/style-vault/editorial-flow
  - tokens/layout/_shared/fixed-cols-row
  - tokens/layout/_shared/responsive-grid
  - components/buttons/style-vault/dark-pill-cta
  - components/buttons/style-vault/ghost-bordered-cta
  - components/tags-badges/style-vault/cyan-dot-meta-pill
  - components/toggles/style-vault/editorial-underline-tab
  - components/overlays/style-vault/spring-toast
  - blocks/marketing/style-vault/cool-blob-hero
  - blocks/display/style-vault/preview-thumb-card
  - blocks/display/style-vault/floating-cover-row
  - blocks/layout/style-vault/browser-chrome-frame
  - blocks/nav/style-vault/sticky-platform-topbar
  - blocks/filters/style-vault/sticky-chip-filter-panel
  - blocks/search/style-vault/cmd-k-search-panel
  - blocks/feedback/style-vault/full-screen-loader
  - pages/landing/style-vault/editorial-cool-landing
  - pages/detail/style-vault/sticky-toc-product
  - pages/detail/style-vault/sidebar-preview-detail
  - pages/list-table/style-vault/category-row-browse
  - pages/list-table/style-vault/sticky-filter-product-list
  - pages/dashboard/style-vault/profile-collections
preview: /preview/styles/portfolio-studio/style-vault-cool-editorial
---

# Style Vault Cool Editorial

> 设计目录站的整站调性 —— "白上叠白靠 hairline 切割 + 冷感 cyan 单点 + 编辑感 mono 索引"

## 设计哲学

**作品才是主角**——所有视觉装饰都让位于"让作品被看见"。这意味着：

- 极少抢戏：dark CTA 全站同屏 1 个，cyan accent ≤ 3 处，blob 只在 hero 出现
- 编辑式呼吸：section 间距 32-36 / py-32，Logo 墙、价值段都给足留白
- 切割不靠投影：白卡叠在白底上，靠 1px slate-100/200 hairline 区分；hover 才用三层柔投影把卡片"浮起"
- 单字族打天下：Inter 一种字，靠尺寸（11→17→26→44→88px）和 letter-spacing 拉层级，不靠衬线 / 装饰字
- 冷感 + 编辑：调色冷（slate + cyan，绝无暖色）；节奏编辑（mono 数字索引 / uppercase tracking caption / italic 强调只在 manifesto）

## 视觉特征

- **页面底色**：`#fafafa`，panel/card 白；切割全靠 `border-slate-100` (separator) 或 `border-slate-200/80` (card)
- **文字色**：slate 7 阶梯队（900 标题 / 700 strong / 500 body / 400 caption / 300 icon idle）
- **唯一 accent**：cyan-500 圆点 / cyan-100 blob / cyan-700→slate-900 标题渐变 / cyan-300 italic 强调
- **唯一 dark 面板**：manifesto bg-slate-900——其它地方一律浅底
- **字体**：Inter 一种字，display 收 letter-spacing −0.035em，caption uppercase tracking-[0.22em]，索引 mono
- **动效**：标志 cubic-bezier(0.2,0.7,0.2,1)；hero fade-up cascade 0/150/300/500ms；卡片浮起 translate −4 + 三层柔投影；blob 14s/18s 异步漂移；tab 下划线 scaleX gradient cyan→slate-900

## 设计原则

1. **白上叠白**：永远先尝试 hairline 切割，只有 hover 才用大投影
2. **冷不冷漠**：blob + 渐变标题 + manifesto cyan italic 让冷里有温度
3. **编辑式留白**：宁可 py-32 也不 py-16；Logo 墙 / 价值段必须呼吸到位
4. **mono 撑数字**：所有索引（01/02/03）/ ID 字串 / 数字徽标用 mono——和正文 sans 形成节奏
5. **作品优先**：StyleCard / PreviewOnlyCard 都是真组件缩放，不用图片占位
6. **blob 只在 hero**：landing hero 双 blob、product detail cover 弱 blob，其它地方禁用——避免氛围泛滥

## Tokens 注入

```css
:root {
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'PingFang SC', sans-serif;
  --font-mono: ui-monospace, 'SF Mono', Menlo, monospace;

  --color-bg-page:   #fafafa;
  --color-bg-panel:  #ffffff;
  --color-bg-subtle: #f8fafc;
  --color-bg-dark:   #0f172a;

  --color-fg-heading: #0f172a;
  --color-fg-body:    #64748b;
  --color-fg-muted:   #94a3b8;

  --color-border-soft: #f1f5f9;
  --color-border-base: #e2e8f0;

  --color-accent-blob:   #cffafe;  /* cyan-100 */
  --color-accent-dot:    #06b6d4;  /* cyan-500 */
  --color-accent-italic: #67e8f9;  /* cyan-300 */
  --color-accent-deep:   #0891b2;  /* cyan-700 */

  --easing-signature: cubic-bezier(0.2, 0.7, 0.2, 1);
  --duration-card:    400ms;
  --duration-hero:    900ms;
}
```

## 适配指南

- 套该 style 后只需覆盖以上 CSS 变量即可适配新产品
- Hero 必须 `cool-blob-hero`；其它 section 不要再用 blob
- 列表 / 浏览类页面用 `preview-thumb-card` 系列；产品聚合页用 `floating-cover-row` + masonry
- 详情页右列用 `browser-chrome-frame`，左列窄 sidebar 元信息
- TopBar 永远 sticky 玻璃感 + 视口绝对居中的 platform underline tab
- mono uppercase 是身份特征——索引数字 / category 标识 / Section eyebrow 都不要切回 sans

## 反模式

- 不要在 hero 之外用 blob（氛围会糊）
- 不要给卡片加 `scale(1.02)` 整卡放大（违反 editorial-flow 卡片浮起 + 内容缩放）
- 不要把 cyan 当大面积 background（破坏单点高亮逻辑）
- 不要让段间距 < `py-16`（破坏编辑感呼吸）
- 不要引第二种字族（Inter 一种字到底）
- 不要把 manifesto 的 dark panel 复用到其它 section（dark 是 manifesto 的语义身份）
