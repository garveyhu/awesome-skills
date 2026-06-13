---
id: components/display/chameleon/dynamic-virtual-list
type: component
name: 动态行高虚拟列表
description: '@tanstack/react-virtual 封装的动态行高虚拟列表 — measureElement 自动测高 + 可选 stickToBottom 贴底（聊天流/流式逐 chunk）+ overscan'
platforms:
- web
theme: light
tags:
  aesthetic:
  - minimal
  mood:
  - calm
  stack:
  - shadcn-radix
preview: /preview/components/display/chameleon/dynamic-virtual-list
---

# 动态行高虚拟列表

> Chameleon 全站大列表 / 移动端长列表的虚拟化原语（`VirtualList`，基于 `@tanstack/react-virtual`）。**纯结构组件，无固定视觉色**——色彩、间距全由 `renderItem` 自管。核心能力：① `measureElement` 动态测量每行真实高度（无需预知行高），② 可选 `stickToBottom`（聊天流/流式 chunk 追加时自动贴底），③ `overscan` 缓冲区。调用方**必须**通过 `className` 给滚动容器固定高度（`h-full` / `max-h-[...]`）才能虚拟化。

## 视觉特征

- 滚动容器：`overflow-y-auto` + 调用方传入的 `className`（**须含高度**）；带 `ref={scrollRef}` 作为 `getScrollElement`
- 内层定位层：`relative w-full`，`style.height = virtualizer.getTotalSize()`（撑出完整滚动高度）
- 每个虚拟项：`absolute left-0 top-0 w-full` + `itemClassName`，`style.transform = translateY(${vi.start}px)`（**绝对定位 + transform 偏移**，非 DOM 流）
- 每项带 `data-index={vi.index}` + `ref={virtualizer.measureElement}`（用于动态测高）
- 默认 `estimateSize = 60`（测量前的占位预估高），`overscan = 8`（视口外预渲染 8 行）
- `stickToBottom = true` 时：`useEffect` 依赖 `items` 引用，每次变化调 `scrollToIndex(items.length - 1, { align: 'end' })`——流式中逐 chunk 贴底，静态列表 items 不变则不打扰用户上滚

## 核心代码

```tsx
const virtualizer = useVirtualizer({
  count: items.length,
  getScrollElement: () => scrollRef.current,
  estimateSize: () => estimateSize,   // 默认 60
  overscan,                            // 默认 8
  getItemKey: index => getKey(items[index], index),
});

useEffect(() => {
  if (stickToBottom && items.length > 0) {
    virtualizer.scrollToIndex(items.length - 1, { align: 'end' });
  }
}, [stickToBottom, items, virtualizer]);

return (
  <div ref={scrollRef} className={cn('overflow-y-auto', className)}>
    <div className="relative w-full" style={{ height: virtualizer.getTotalSize() }}>
      {virtualizer.getVirtualItems().map(vi => (
        <div
          key={vi.key}
          data-index={vi.index}
          ref={virtualizer.measureElement}
          className={cn('absolute left-0 top-0 w-full', itemClassName)}
          style={{ transform: `translateY(${vi.start}px)` }}
        >
          {renderItem(items[vi.index], vi.index)}
        </div>
      ))}
    </div>
  </div>
);
```

## 适配指南

- **必须给容器固定高度**——`<VirtualList className="h-full" .../>` 或 `max-h-[60vh]`；没有高度则虚拟化失效（getTotalSize 算不出视口）
- 聊天流场景传 `stickToBottom`——依赖的是 `items` 引用变化，所以流式时每次 setState 替换数组就会贴底；要避免无意义贴底就保持 items 引用稳定
- 行高差异大（聊天气泡长短不一）才用动态测量；等高行可直接用 estimateSize 精确值省去抖动
- `getKey` 必须稳定唯一——用消息 id / 行 id，不要用 index（会导致测量缓存错乱）

## 反模式

- ❌ 容器不给高度——虚拟化静默失效，退化成全量渲染
- ❌ 在 `renderItem` 里写昂贵的非 memo 计算——每次滚动重渲可见行
- ❌ stickToBottom 配静态列表——会在用户上滚时被强行拽回底部
- ❌ 把视觉样式写进 VirtualList——它是纯结构件，色/间距归 renderItem
