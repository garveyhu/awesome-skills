---
id: tokens/layout/_shared/responsive-grid
type: token
name: 弹性自适应栅格
description: 双模式响应式栅格 · fill（auto-fit + 1fr 拉伸填行）/ fixed（auto-fill + 1fr 等宽留白）
platforms: [web]
theme: both
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses: []
preview: /preview/tokens/layout/_shared/responsive-grid
---

# Responsive Grid · 双模式

> 一个极简的响应式栅格原语，支持两种行为模式 —— **fill**（auto-fit）和 **fixed**（auto-fill），
> 都基于 `minmax(min, 1fr)`，唯一的差别是 `auto-fit` vs `auto-fill`，但视觉差异显著。

## 两种模式

| 模式 | CSS | 数据少时 | 适用场景 |
|------|-----|---------|---------|
| **fill** | `repeat(auto-fit, minmax(min, 1fr))` | 空列**折叠**，已有卡片**拉宽**占满整行 | 搜索结果、全量列表，视觉上"必须填满" |
| **fixed** | `repeat(auto-fill, minmax(min, 1fr))` | 空列**保留**，卡片保持容器自然列宽，**右侧留白** | 个人主页收藏、作品集，视觉上"不能扯大" |

### 列数公式（两种模式相同）

```
cols = floor((container_width + gap) / (min_card_width + gap))
```

### 关键区别（数据少于 cols 时）

- **fill**：`auto-fit` 把多余空 track 折叠为 0 → 现有卡片用 `1fr` 拉伸瓜分容器宽 → 1 张卡也撑满整行
- **fixed**：`auto-fill` 保留多余空 track → 每个 track（包括空的）都按 `1fr` 等分容器宽 → 已填卡片维持"满 cols 时的宽度"，剩下的空 track 留白

## 适用场景

### 用 fill

- **全量列表页**：数据不确定，希望永远填满
- **搜索结果页**：结果数会变动
- 任何"**展示全部、不能露白**"的场景

### 用 fixed

- **个人主页 · 收藏 tab**：少量数据时不能让单卡撑得很宽
- **作品集 / Portfolio**：卡片有"作品"语义，宽度需要稳定
- 任何"**卡宽优先于填满**"的场景

### 都不用 → 用 [fixed-cols-row](./fixed-cols-row.md)

- 「只展一行」的预览场景（首页每分类预览 1 行）
- 列数 = 显示数（数据量 = 列数），用 `useCols` + `slice` 严格切

## 实现 · ResponsiveGrid 组件

```tsx
// src/components/ResponsiveGrid.tsx
import type { CSSProperties, ReactNode } from 'react';

type Mode = 'fill' | 'fixed';

interface ResponsiveGridProps {
  /** fill: auto-fit + 1fr / fixed: auto-fill + 1fr */
  mode?: Mode;
  /** 卡片最小宽度 px —— 决定最大列数 */
  min?: number;
  /** 卡片间距 px */
  gap?: number;
  className?: string;
  style?: CSSProperties;
  children: ReactNode;
}

export function ResponsiveGrid({
  mode = 'fixed',
  min = 280,
  gap = 20,
  className = '',
  style,
  children,
}: ResponsiveGridProps) {
  const tracks = mode === 'fill' ? 'auto-fit' : 'auto-fill';
  const cols = `repeat(${tracks}, minmax(${min}px, 1fr))`;
  return (
    <div
      className={`grid ${className}`}
      style={{ gridTemplateColumns: cols, gap, ...style }}
    >
      {children}
    </div>
  );
}
```

## 使用示例

```tsx
// fill —— 哪怕只有 1 张卡也撑满整行
<ResponsiveGrid mode="fill" min={300}>
  {searchResults.map((r) => <Card key={r.id} item={r} />)}
</ResponsiveGrid>

// fixed —— 容器能放 4 张时，2 张数据也按 4 张时的宽度排
<ResponsiveGrid mode="fixed" min={300}>
  {favorites.map((f) => <Card key={f.id} item={f} />)}
</ResponsiveGrid>
```

## 参数调优

### `min` 选取

- 文字/元信息卡：`240-280px`
- 带预览图卡：`280-320px`
- 大块信息卡（标题 + 描述 + 标签 + 预览图）：`300-380px`

太小 → 窄屏列数多、内容挤压；太大 → 宽屏列数少、单卡过宽。

### `gap` 选取

- 桌面网格：`16-24px`（Tailwind `gap-4 / gap-5 / gap-6`）
- 移动：`12-16px`

### 防止 fill 模式下"少量数据过度拉宽"

fill 模式下数据只有 1-3 条时单卡会被拉很宽。两种解法：

1. **首选**：换成 `mode="fixed"` —— 卡宽不再受数据量影响
2. **保留 fill**：给容器加 `maxWidth` 封顶
   ```tsx
   <div style={{ maxWidth: 'calc(380px * 5 + 1rem * 4)' }}>
     <ResponsiveGrid mode="fill" min={300}>...</ResponsiveGrid>
   </div>
   ```

## 关键要点

1. **`auto-fit` vs `auto-fill` 是唯一开关**，其他完全相同 —— 选 fill 还是 fixed 由"少数据时是否要填满"决定
2. **`minmax(X, 1fr)` 的 `1fr` 必须保留**：
   - 用 `1fr`：列数确定后均分容器宽
   - 用具体 px（`minmax(X, 380px)`）：上限会导致右侧"漏白"，破坏两种模式的语义
3. **不用 JS 算列数**：纯 CSS 实现，比 useCols 方案简单且不需要订阅 resize
4. **响应是阶梯式**：每过 `min + gap` 宽度多/少一列，不是平滑过渡

## 反模式

- ❌ 用 `repeat(auto-fill, minmax(X, MAX_PX))`（MAX 是硬 px 上限）—— MAX 会挤压 1fr 分配，造成右侧不规则留白（本仓 `BrowseCategoryPage` 历史 bug：`minmax(300px, 400px)` 在 Mac 屏宽下留白 80-120px）
- ❌ 对"一行展示"场景用此栅格 —— 数据量 ≥ cols 时会换行，破坏"一行"语义，应该用 [fixed-cols-row](./fixed-cols-row.md)
- ❌ fill 模式没 maxWidth 封顶 —— 单条数据时单卡会撑爆容器
- ❌ 用 `1fr` 做 min（`minmax(1fr, 1fr)`）—— 窄屏卡片会被压到 100px 以下

## 沉淀历史

- **v1**：仅有 `auto-fit-fluid` 一种模式（auto-fit + 1fr 强填行）
- **v2 当前**：合并 fixed 模式（auto-fill + 1fr 留白），统一为 `ResponsiveGrid` 组件，按 `mode` 切换。
  动机：个人主页收藏区少量数据时不应被拉宽，但仍需一致的卡宽节奏 —— 单一 fill 模式不够。

## 命名出处

"双模式" —— `auto-fit` / `auto-fill` 一字之差，是 CSS Grid 里最常被混用、视觉差异最大的两种行为，
同一组件提供两种模式，让调用方按 "数据少时怎么看" 决定。
