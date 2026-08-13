# 沉淀计划 · style-vault 自指沉淀

日期：2026-04-27
作者：links
模式：create
起点：from-project（$PROJECT = ~/Coding/Archer/style-vault，即 vault 项目自身）
档位：Tier 2 · 基础级（目标 12–18 条 · 实际 18 条）

## 目标

把 style-vault 网站项目自身的 UI 风格沉淀回 vault —— 自指沉淀。捕获"冷感 editorial 设计目录站"的整套设计语言，让 AI 后续能复刻同款。

## taxonomy 字典改动

新增 category：
```
"design": { "zh": "设计", "dot": "#6366f1", "order": 6 }
```

`products/style-vault.category` = `design`。

## 涉及条目（依赖拓扑序 · 18 条）

### Tokens · 4
1. `tokens/palettes/style-vault/slate-cyan-cool` — slate 全阶 + cyan 单点 + #fafafa 底
2. `tokens/typography/pairs/style-vault/inter-editorial-display` — Inter 单字族 editorial 字距
3. `tokens/gradient/style-vault/cool-blob-decor` — 双 blob 漂浮装饰（用户点名要的）
4. `tokens/motion/style-vault/editorial-flow` — cubic-bezier(0.2,0.7,0.2,1) + fade-up + 卡片浮起

### Components · 4
5. `components/buttons/style-vault/dark-pill-cta` — slate-900 rounded-full 主 CTA
6. `components/buttons/style-vault/ghost-bordered-cta` — 1.5px 描边幽灵次 CTA
7. `components/tags-badges/style-vault/cyan-dot-meta-pill` — uppercase tracking 玻璃感胶囊
8. `components/toggles/style-vault/editorial-underline-tab` — scaleX cyan→slate-900 渐变 tab

### Blocks · 5
9. `blocks/marketing/style-vault/cool-blob-hero` — 双 blob hero
10. `blocks/display/style-vault/preview-thumb-card` — 1440 虚拟视口缩放卡片（StyleCard）
11. `blocks/display/style-vault/floating-cover-row` — 浮起作品照行卡（产品列表）
12. `blocks/layout/style-vault/browser-chrome-frame` — mac dot 浏览器 chrome
13. `blocks/nav/style-vault/sticky-platform-topbar` — 玻璃感顶栏 + 视口绝对居中 platform pill

### Pages · 3
14. `pages/landing/style-vault/editorial-cool-landing` — HomePage（hero + Logo 墙 + 3 段叙事 + manifesto + footer）
15. `pages/detail/style-vault/sticky-toc-product` — ProductDetailPage（cover hero + sticky TOC + masonry）
16. `pages/list-table/style-vault/category-row-browse` — BrowsePage（双 sticky + 每类一行）

### Style + Product · 2
17. `styles/portfolio-studio/style-vault-cool-editorial` — 整站调性
18. `products/style-vault` — category=design，绑全部上面 17 条

## 依赖关系

```
products/style-vault
  → refs.style: styles/portfolio-studio/style-vault-cool-editorial
  → refs.pages: [14, 15, 16]
  → refs.blocks: [9, 10, 11, 12, 13]
  → refs.components: [5, 6, 7, 8]
  → refs.tokens: { palette: 1, typography: 2 }

styles/portfolio-studio/style-vault-cool-editorial
  uses: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

每条 block / component 的 uses 包含相关 tokens
blocks/marketing/cool-blob-hero uses += tokens/gradient/cool-blob-decor
```

## 元信息填写方式

- AI 自动填（用户授权 Y 模式）：全部 18 条
- 用户手改：无

## 执行状态

☑ 用户已确认 · 已写入
