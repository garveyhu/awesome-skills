---
id: tokens/layout/_shared/fixed-cols-row
type: token
name: 断点列数 · 一行快照栅格
description: useCols + slice(0, cols) · 列数 = 显示数 · 卡宽在同屏下恒定不受数据量影响
platforms: [web]
theme: both
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses: []
preview: /preview/tokens/layout/_shared/fixed-cols-row
---

# Fixed Cols Row

> "一行快照"栅格策略。用 `useCols` hook 按 Tailwind 断点算出当前列数 N，再 `items.slice(0, N)` 让**数据量 = 列数**——无论数据有多少、同一屏下卡片宽度恒定（= 容器宽 / N）。

## 适用场景

- **首页每分类预览 1 行**：列数 = 显示数，永远刚好铺满 1 行
- **Hero 下方"精选"横排**：要求任一屏下卡宽统一（品牌一致）
- **"Top N"榜单横排**：N 跟随屏宽，不是硬编码
- 任何"**展示结果是一行**"的场景

## 不适用

- 需要展示**全部数据**的列表页 → 用 [auto-fit-fluid](./auto-fit-fluid.md)
- 搜索结果 / 分页列表 / 多行网格

## 断点映射

按 Tailwind 断点阶梯：

| 视窗宽 | 断点 | 列数 |
|---|:---:|:---:|
| < 640px | base | 1 |
| ≥ 640 | sm | 2 |
| ≥ 768 | md | 3 |
| ≥ 1024 | lg | 4 |
| ≥ 1280 | xl | 5 |
| ≥ 1536 | 2xl | 6 |

## 核心代码

### Hook · `useCols.ts`

```ts
import { useSyncExternalStore } from 'react';

const BREAKPOINTS = [
  { query: '(min-width: 1536px)', cols: 6 },
  { query: '(min-width: 1280px)', cols: 5 },
  { query: '(min-width: 1024px)', cols: 4 },
  { query: '(min-width: 768px)',  cols: 3 },
  { query: '(min-width: 640px)',  cols: 2 },
] as const;

function subscribe(callback: () => void): () => void {
  if (typeof window === 'undefined') return () => {};
  const mqls = BREAKPOINTS.map((bp) => window.matchMedia(bp.query));
  mqls.forEach((m) => m.addEventListener('change', callback));
  return () => mqls.forEach((m) => m.removeEventListener('change', callback));
}

function getSnapshot(): number {
  if (typeof window === 'undefined') return 4;
  for (const { query, cols } of BREAKPOINTS) {
    if (window.matchMedia(query).matches) return cols;
  }
  return 1;
}

function getServerSnapshot(): number {
  return 4; // SSR 默认 lg · 客户端首帧不一致时 React 自己校正
}

export function useCols(): number {
  return useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot);
}
```

### 使用方式

```tsx
import { useCols } from '@/hooks/useCols';

export function PreviewRow({ items }: { items: Item[] }) {
  const cols = useCols();
  const visible = items.slice(0, cols);

  return (
    <div
      className="grid gap-4"
      style={{ gridTemplateColumns: `repeat(${cols}, minmax(0, 1fr))` }}
    >
      {visible.map((item) => <Card key={item.id} item={item} />)}
    </div>
  );
}
```

## 关键要点

1. **`grid-template-columns` 用 inline style 动态生成** `repeat(${cols}, minmax(0, 1fr))` —— 不能用 Tailwind JIT 的 `grid-cols-${N}`（JIT 不识别动态类，除非 safelist）
2. **`minmax(0, 1fr)` 的 min=0 很关键** —— 否则内容撑破网格、`truncate` 失效
3. **实现用 `useSyncExternalStore`** 而非 `useEffect + useState`——React 18+ 推荐的外部状态订阅方式，避免 tearing
4. **`getSnapshot` 必须返回原语或稳定引用** —— 不允许返回 `{ cols, label }` 这种每次新对象。React 用 `Object.is` 比较，新对象永远 !== 旧的 → 触发 rerender → 再 call snapshot → 再得新对象 → **无限循环、页面白屏**、控制台 "The result of getSnapshot should be cached to avoid an infinite loop"。派生值（如断点 label）应在 hook 外层计算
5. **SSR fallback 用 lg（4）** —— 最通用的桌面尺寸，hydration 后再校正
6. **slice 必须在 render 里做** —— 而非 `useMemo([cols, items])`，保持依赖清晰

## 反模式

- ❌ 用 Tailwind 显式 `grid-cols-1 sm:2 md:3 lg:4 xl:5 2xl:6`——列数固定但没按 cols 切 items，多余项会换行破坏"一行"
- ❌ 用 `auto-fit` + slice——两套机制打架，结果不可预期
- ❌ 给数据量小的情况加 "fallback 最少 N 张"——那就违背了"数据量 = 列数"的承诺
- ❌ 用 `useEffect` 监听 window resize——tearing 风险 + 首帧错位
- ❌ `getSnapshot` 返回 `{ cols, label }` 这种新对象——**必定无限循环白屏**，必须只返回原语

## 坑

- **Tailwind JIT safelist 或 inline style 二选一**：如果一定要用 class，需在 `tailwind.config.js` 里：
  ```js
  safelist: ['grid-cols-1', 'grid-cols-2', 'grid-cols-3', 'grid-cols-4', 'grid-cols-5', 'grid-cols-6']
  ```
  否则生产构建会 purge。推荐用 inline style（更显式，无构建配置依赖）
- **子组件 useCols 会多次订阅**：同屏下多处调用 hook 会各自订阅 matchMedia，低开销可接受；高频复用可改成 Context 单例

## 命名出处

"一行快照"——每次渲染都在"当前屏宽下的 1 行"，不溢出、不留白、不受数据量干扰。
