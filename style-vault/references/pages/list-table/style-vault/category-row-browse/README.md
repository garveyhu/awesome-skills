---
id: pages/list-table/style-vault/category-row-browse
type: page
name: 类目行浏览页
description: TopBar + Sticky CategoryTabs + 每类一行的卡片浏览页（按断点 useCols 列数 + slice 只展一行）
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
preview: /preview/pages/list-table/style-vault/category-row-browse
---

# Category Row Browse

> Style Vault BrowsePage 完整骨架——五个类目（style / page / block / component / token）每类只展一行 + 查看更多

## 视觉特征

```
┌─────────────────────────────────────────┐
│ TopBar （sticky 72px）                   │
├─────────────────────────────────────────┤
│ CategoryTabs （sticky top-72 56px）      │ ← editorial-underline-tab 大档
├─────────────────────────────────────────┤
│  ◷                                       │
│  风格                          查看更多 →│ ← 一行 = 当前断点列数（lg=4 / 2xl=6）
│  ┌─┐ ┌─┐ ┌─┐ ┌─┐                       │
│  └─┘ └─┘ └─┘ └─┘                       │
│                                          │
│  页面                          查看更多 →│
│  ┌─┐ ┌─┐ ┌─┐ ┌─┐                       │
│  └─┘ └─┘ └─┘ └─┘                       │
│                                          │
│  ... block / component / token 各一行   │
└─────────────────────────────────────────┘
```

### Sticky 双层导航

- TopBar 72px sticky `top-0`（来自 `blocks/nav/style-vault/sticky-platform-topbar`）
- CategoryTabs 56px sticky `top-[72px] z-40`，背景 `bg-[#fafafa]/90 backdrop-blur-md`
  - 5 个 tab：风格 / 页面 / 模块 / 组件 / 原语（路由 `/browse/style` 等）
  - 在 `/browse` 总览页**不激活任何 tab**（用 useLocation 从 pathname 取 active）
  - 大档 16px tab `sv-underline-tab--lg`

### Per-type Section

每个类目一行：

```jsx
<section>
  <header className="mb-5 flex items-baseline justify-between gap-4">
    <h2 className="font-display text-[22px] font-semibold tracking-[-0.015em] text-slate-900">
      {platformText} {typeLabel}
    </h2>
    <Link to={`/browse/${type}`} className="sv-text-link">
      查看更多
      <ArrowRightOutlined className="sv-text-link-arrow text-[11px]" />
    </Link>
  </header>
  <div className="grid gap-4" style={{ gridTemplateColumns: `repeat(${cols}, minmax(0, 1fr))` }}>
    {preview.map((item) => <StyleCard key={item.id} item={item} onClick={() => nav(`/item/${item.id}`)} />)}
  </div>
</section>
```

**`useCols` hook**：根据视口宽度返回断点列数（sm=2 / md=3 / lg=4 / xl=5 / 2xl=6）。`preview = items.slice(0, cols)` —— 永远刚好填满一行不溢出。

### "查看更多" 链接

走 `sv-text-link` 全局类（来自 `tokens/motion/style-vault/editorial-flow`）：
- 默认下方 `1px scaleX(0.35)` 短下划线 + 箭头 inline-flex
- hover 时下划线 `scaleX(1)` 铺满（260ms） + 箭头 `translateX(4px)` 位移

### 平台过滤

通过 `usePlatform()` 读全局 platform context（来自 TopBar 平台切换）。`matchesPlatform(item.platforms, platform)` 决定是否显示：
- 当前 Web → 只显含 `web` 的条目
- 当前 iOS → 只显含 `ios` 或 `any` 的条目

### 空态

当所有类目为空（如选 iOS 但当前没 iOS 内容）：

```jsx
<div className="rounded-2xl border border-dashed border-slate-200 bg-white p-16 text-center text-slate-400">
  当前「{platformText}」下暂无内容
</div>
```

虚线边框 + 空白巨多 + 灰字 —— editorial 的"留白即留白"。

## 适配指南

- 一定 sticky 双层（TopBar + CategoryTabs）—— 滚远后还能看到当前位置
- 行间距 `space-y-14`（56px） —— 比常规 `space-y-8` 大一档，留白要够
- "查看更多"必须文字链 + 箭头组合 —— 不要换 button（破坏 editorial）
- 当类目数据为空时**整段不渲染**（`if (items.length === 0) return null`）—— 不显示空标题占位

## 反模式

- 不要把每行用 `overflow-x-auto` 横滑（破坏断点列数 = 整齐网格的特性）
- 不要把 CategoryTabs 改成 chip 实色（变成 community 风）
- 不要给 section header 加 background—— editorial 节奏
- 不要 BrowsePage 总览也激活某个 tab（活在所有 tab 上方的"全景"）
