---
mode: modify
date: 2026-04-28
author: links
scope: 多条目联动 sync · TopBar / SearchPanel / CategoryTabs / 懒加载 / StyleCard inert
---

# 沉淀计划 · 同步 nav / search / browse 三类变更

## 改动摘要

网站代码已完成（`frontend/src/components/TopBar.tsx`、`SearchPanel.tsx`、`CategoryTabs.tsx`、`StyleCard.tsx`、`hooks/useInfiniteList.ts`、`pages/BrowseCategoryPage.tsx`、`pages/ProfilePage.tsx`），本次沉淀同步 6 条 skill 条目 + 3 处 preview tsx。

## 受影响条目（按优先级）

### A · `blocks/nav/style-vault/sticky-platform-topbar.md`
- TopBar 主导航「浏览」「产品集」加 active state（`sv-underline-tab` + `data-on` 跟随 pathname）
- 文字补 `pt-2.5` 抵消自带 `padding-bottom: 10px`，配合 `items-center` 容器视觉居中
- 同步 preview tsx：默认让"浏览"激活，演示下划线 pattern

### B · `components/toggles/style-vault/editorial-underline-tab.md`
- 用法档位补充：13px 小档现还用在 TopBar 主导航
- 加"`items-center` 容器对称居中"小节：`pt-2.5` 抵消 `padding-bottom: 10px`

### C · `blocks/search/style-vault/cmd-k-search-panel.md`
- `searchPanel` singleton 接口加 `closeForNavigation`
- 加新章节"跨导航持久化"：module-level `storedQ/Type/Platform` + `pendingReopen` + 浏览器 POP 时自动复活
- 修改 `openItem` 实现：用 `closeForNavigation()` 替代 `onClose()`
- 修改"反模式"措辞：主动关 = 清状态；点结果 = 跨导航保留

### D · `pages/list-table/style-vault/category-row-browse/README.md`
- CategoryTabs 改成 6 tab（**总览** / 风格 / 页面 / 模块 / 组件 / 原语），`/browse` 时激活"总览"
- 反模式删掉"不要 BrowsePage 总览也激活某个 tab"
- 加"二级类别页（/browse/:type）"小节：IO sentinel 自动懒加载，`cacheKey = browse:${type}`
- 同步 preview tsx：CategoryTabs 加 `总览` tab

### E · `pages/dashboard/style-vault/profile-collections/README.md`
- "Collections Grid" 加 IO sentinel 懒加载，`cacheKey = profile:fav:${type}` 跨 tab 保留进度

### F · `blocks/display/style-vault/preview-thumb-card.md`
- 核心代码骨架的预览容器加 `inert`
- 加"防焦点劫持"小节：autoFocus 触发 scroll-into-view 导致整页跳动；`inert` 禁焦点

## 不动的条目

经 grep 确认仅引用 TopBar 但未涉及 active state 细节：

- `pages/list-table/style-vault/sticky-filter-product-list/README.md`
- `products/style-vault/README.md`
- `styles/portfolio-studio/style-vault-cool-editorial/README.md`
- `blocks/filters/style-vault/sticky-chip-filter-panel.md`
- `blocks/marketing/style-vault/cool-blob-hero.md`
- `components/buttons/style-vault/dark-pill-cta.md`

## 不改 SKILL.md

SKILL.md 是 skill 元规范（消费模式 5 步 / frontmatter schema），不直接涉及具体组件实现。

## 用户确认

用户回复"直接动" · 整体确认 ✓
