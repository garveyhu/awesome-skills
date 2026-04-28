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
uses:
  - tokens/layout/_shared/fixed-cols-row
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
  - **6 个 tab：总览 / 风格 / 页面 / 模块 / 组件 / 原语**（路由 `/browse` + `/browse/style` 等）
  - **永远有且仅有一个 tab 激活**：`/browse` 激活「总览」；`/browse/:type` 激活对应类型 tab；用 useLocation regex `^/browse/([^/?]+)` 取 active key，没匹配上就 fallback `'all'`
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

## 二级类别页（/browse/:type）的懒加载

`/browse` 是"每类一行 + 查看更多"的概览节奏；点查看更多进二级（`/browse/style` 等）就是单类别的全量浏览。二级页用 IntersectionObserver sentinel 自动懒加载（不是手动翻页按钮，也不是 `content-visibility: auto`）：

```tsx
const { visible, sentinelRef, hasMore, visibleCount, total } = useInfiniteList(
  filteredItems, cols, { rowsPerPage: 4, cacheKey: `browse:${type}` }
);

return (
  <div style={{ overflowAnchor: 'none' }}>
    <div className="grid gap-4" style={{ gridTemplateColumns: `repeat(${cols}, minmax(0, 1fr))`, overflowAnchor: 'none' }}>
      {visible.map((item) => <StyleCard key={item.id} item={item} ... />)}
    </div>
    {hasMore ? (
      <>
        <div ref={sentinelRef} aria-hidden style={{ height: 1 }} />
        <div className="mt-8 flex items-center justify-center">
          <span className="text-[11px] text-slate-400 font-medium tracking-[0.18em] uppercase">
            {visibleCount} / {total}
          </span>
        </div>
      </>
    ) : (
      <div className="mt-12 flex items-center justify-center">
        <span className="text-[11px] text-slate-300 ...">· {total} · End ·</span>
      </div>
    )}
  </div>
);
```

### 为什么这样设计

- **新增条目永远追加在视口下方** → 浏览器渲染上半屏不位移 → 视觉稳定。`overflowAnchor: 'none'` 同步禁掉浏览器自带 anchor 反弹。
- **`cacheKey: browse:${type}`** → 用户在 5 个类别 tab 间切换，每个 tab 的翻页位置（`visibleCount`）保留在模块顶层 `Map` 里，切回来不用从头翻
- **`rootMargin: '300px 0px'`** → 用户滚到距底 300px 时就已经在加载下一批，几乎感觉不到"等待"
- **rAF double 锁** → 一次 IO 触发只加载一批，避免 sentinel 还在视口里时连续触发刷出 N 批

### 为什么不用 `content-visibility: auto`

试过：全量渲染所有卡 + 估算 `containIntrinsicSize` 占位高度。问题是估算的占位高度（如 320px）和真实卡片高度（310–380px 浮动）不一致 → 浏览器在 viewport 内外切换渲染态时 document 总高频繁抖动 → 滚动条跳。**视口下方追加内容的 IO 模式才是稳定方案**。

## 反模式

- 不要把每行用 `overflow-x-auto` 横滑（破坏断点列数 = 整齐网格的特性）
- 不要把 CategoryTabs 改成 chip 实色（变成 community 风）
- 不要给 section header 加 background—— editorial 节奏
- 不要让 CategoryTabs 在 `/browse` 时一个 tab 都不激活 —— 用户会"不知道自己在哪个模块"。永远要有视觉锚点（"总览"就是为这个加的）
- 二级页不要用 `content-visibility: auto` 替代 IO sentinel —— 估算占位高度 vs 真实高度的偏差会让滚动条跳
- 二级页不要用手动翻页按钮 —— 移动端 / 大屏滚动用户都习惯无缝懒加载
