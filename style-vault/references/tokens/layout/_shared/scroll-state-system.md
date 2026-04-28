---
id: tokens/layout/_shared/scroll-state-system
type: token
name: 滚动状态原语
description: 双 Map 滚动还原 + IO sentinel 懒加载稳定 · 4 场景决策矩阵（tab 间记忆 / push 置顶 / 浏览器前进后退还原 / 懒加载零位移）
platforms: [web]
theme: both
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses: []
preview: /preview/tokens/layout/_shared/scroll-state-system
---

# Scroll State System · 滚动状态原语

> 一套 SPA 滚动行为契约：tab 间切换记忆位置 · 点击进入详情置顶 · 浏览器前进后退还原历史滚动条 · 懒加载内容生长不让视口跳。
> 由两个文件 + 一条挂载规则组成，零外部依赖，任何 React Router SPA 都能直接抄。

## 4 个场景的决策矩阵

| 场景 | 触发条件 | 实现机制 | 期望行为 |
|------|---------|---------|---------|
| **A · Tab 间记忆** | URL 切到同域不同 pathname（如 `/browse/style` ↔ `/browse/page`） | `byPath: Map<pathname, scrollY>` | 切回每个 tab 还原各自的滚动位置 |
| **B · Click 入详情** | PUSH 到全新 pathname（`/products/foo`） | `byPath` miss → `target = 0` + 多帧钉顶 | 新页面置顶 |
| **C · 浏览器后退/前进** | `useNavigationType() === 'POP'`（同 pathname 多次访问区分历史条目） | `byKey: Map<history.key, scrollY>` 优先于 `byPath` | 精准还原历史条目位置（同 pathname 多次访问也能分开） |
| **D · 懒加载内容生长** | 列表底部 sentinel 滚入视口 | `useInfiniteList` IO + `overflow-anchor: none` | 视口下方追加，已渲染区零位移 |

### 为什么需要双 Map（byKey + byPath）

只有 `byPath` → 同一 pathname 多次访问会互相覆盖（用户先看 `/products/foo`，下钻 `/products/foo/spec` 再后退，再点另一个 spec 又后退到 `/products/foo`，第二次到的位置会冲掉第一次记的）。

只有 `byKey` → 内部 nav 切换 tab（`/browse/block` → `/browse/component` → 再点回 `/browse/block` 是 PUSH 到新 history.key，与之前的 key 无关），切回去时 byKey miss，落空。

**双 Map**：POP 优先 `byKey`（精准），PUSH/REPLACE 走 `byPath`（粒度刚好）。

### 为什么 PUSH 时也要钉顶 30 帧

PUSH 后页面初始内容可能异步长高（图片加载、registry 拉取、动画占位变实体），浏览器自动 anchor 把视口拉到当前可见元素，造成"明明应该在顶部却落到中段"。30 帧 ≈ 500ms 内多次 `setY(0)` 把它压回顶部。

### 为什么 POP 还原也要重试 60 帧

异步内容生长可能让 `scrollY` 还达不到目标位置（例如懒加载尚未渲染完上次到达的位置）。多帧重试直到达到 `target` 或超时（≈1 秒）。

## Tokens

```json
{
  "lazyLoad": {
    "rootMargin": "300px 0px",
    "rowsPerPageDefault": 4,
    "rafLockFrames": 2,
    "minPageSize": 8
  },
  "scrollRestore": {
    "maxFrames_pinTop": 30,
    "maxFrames_restorePos": 60,
    "tolerance_px": 1
  },
  "behaviors": {
    "history": "manual",
    "overflowAnchor": "none"
  }
}
```

| key | 值 | 含义 |
|---|---|---|
| `lazyLoad.rootMargin` | `'300px 0px'` | sentinel 距底 300px 时已触发加载，体感"无等待" |
| `lazyLoad.rowsPerPageDefault` | `4` | 每批加载 `cols * 4` 项；列数 6 就是 24 项一批 |
| `lazyLoad.rafLockFrames` | `2`（rAF double） | 一次 IO 触发只加载一批，避免 sentinel 还在视口里时连续触发 |
| `lazyLoad.minPageSize` | `8` | 极窄屏 cols=1 时也至少一次加载 8 项，避免一行一加载 |
| `scrollRestore.maxFrames_pinTop` | `30` | PUSH 钉顶最大帧数（约 500ms） |
| `scrollRestore.maxFrames_restorePos` | `60` | POP 还原最大重试帧数（约 1s） |
| `scrollRestore.tolerance_px` | `1` | 还原位置误差阈值，达到即停止重试 |
| `behaviors.history` | `'manual'` | 关闭浏览器自动 scrollRestoration，全权接管 |
| `behaviors.overflowAnchor` | `'none'` | 列表容器禁用浏览器 anchor 反弹，避免和懒加载冲突 |

## 核心代码

### ScrollToTop · 全局滚动还原（挂在 App 顶层）

```tsx
// src/components/ScrollToTop.tsx
import { useEffect, useLayoutEffect, useRef } from 'react';
import { useLocation, useNavigationType } from 'react-router-dom';

if (typeof window !== 'undefined' && 'scrollRestoration' in window.history) {
  window.history.scrollRestoration = 'manual';
}

const byKey = new Map<string, number>();
const byPath = new Map<string, number>();

const getY = () =>
  window.scrollY ||
  document.documentElement.scrollTop ||
  document.body.scrollTop ||
  0;

const setY = (y: number) => {
  window.scrollTo(0, y);
  document.documentElement.scrollTop = y;
  document.body.scrollTop = y;
};

export function ScrollToTop() {
  const { key, pathname } = useLocation();
  const navType = useNavigationType();
  const currentKeyRef = useRef(key);
  const currentPathRef = useRef(pathname);

  // capture 阶段监听所有 scroll，内层 overflow 容器也覆盖
  useEffect(() => {
    const onScroll = () => {
      const y = getY();
      byKey.set(currentKeyRef.current, y);
      byPath.set(currentPathRef.current, y);
    };
    window.addEventListener('scroll', onScroll, { passive: true, capture: true });
    document.addEventListener('scroll', onScroll, { passive: true, capture: true });
    return () => {
      window.removeEventListener('scroll', onScroll, { capture: true });
      document.removeEventListener('scroll', onScroll, { capture: true });
    };
  }, []);

  useLayoutEffect(() => {
    currentKeyRef.current = key;
    currentPathRef.current = pathname;

    let cancelled = false;
    let attempts = 0;

    // 优先级：POP → byKey（精准）；其它 → byPath（粒度合适）；都 miss → 顶部
    let target = 0;
    if (navType === 'POP') {
      target = byKey.get(key) ?? byPath.get(pathname) ?? 0;
    } else {
      target = byPath.get(pathname) ?? 0;
    }

    const tryRestore = () => {
      if (cancelled) return;
      setY(target);
      attempts++;
      if (target > 0) {
        // 还原位置：连续重试直到到达或超时
        if (attempts < 60 && Math.abs(getY() - target) > 1) {
          requestAnimationFrame(tryRestore);
        }
      } else {
        // 钉顶：连续 30 帧防止异步长高时被自动 anchor 拉回
        if (attempts < 30) {
          requestAnimationFrame(tryRestore);
        }
      }
    };
    tryRestore();
    return () => { cancelled = true; };
  }, [key, pathname, navType]);

  return null;
}
```

### useInfiniteList · 列表懒加载 + 进度持久化

```tsx
// src/hooks/useInfiniteList.ts
import { useCallback, useEffect, useRef, useState } from 'react';

const visibleCountCache = new Map<string, number>();

export function useInfiniteList<T>(
  items: T[],
  cols: number,
  options: { rowsPerPage?: number; cacheKey?: string } = {},
) {
  const { rowsPerPage = 4, cacheKey } = options;
  const pageSize = Math.max(8, cols * rowsPerPage);

  const [visibleCount, setVisibleCount] = useState(() => {
    if (cacheKey && visibleCountCache.has(cacheKey)) {
      return Math.min(items.length, visibleCountCache.get(cacheKey)!);
    }
    return pageSize;
  });

  const isLoadingRef = useRef(false);
  const observerRef = useRef<IntersectionObserver | null>(null);

  // cacheKey 切换：从 cache 恢复
  useEffect(() => {
    if (cacheKey && visibleCountCache.has(cacheKey)) {
      const cached = visibleCountCache.get(cacheKey)!;
      setVisibleCount(Math.min(items.length, Math.max(pageSize, cached)));
    } else {
      setVisibleCount(pageSize);
    }
    isLoadingRef.current = false;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [cacheKey]);

  // items 内容变化（同模块筛选）：clamp
  useEffect(() => {
    setVisibleCount(c => Math.min(c, items.length || pageSize));
  }, [items.length, pageSize]);

  // 写 cache
  useEffect(() => {
    if (cacheKey) visibleCountCache.set(cacheKey, visibleCount);
  }, [cacheKey, visibleCount]);

  const total = items.length;
  const hasMore = visibleCount < total;
  const visible = items.slice(0, visibleCount);

  const stateRef = useRef({ hasMore, total, pageSize });
  stateRef.current = { hasMore, total, pageSize };

  const loadMore = useCallback(() => {
    const s = stateRef.current;
    if (!s.hasMore || isLoadingRef.current) return;
    isLoadingRef.current = true;
    setVisibleCount(c => Math.min(s.total, c + s.pageSize));
    // rAF double 锁：等渲染完一帧再开，避免 IO 立刻再触发
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        isLoadingRef.current = false;
      });
    });
  }, []);

  const loadMoreRef = useRef(loadMore);
  loadMoreRef.current = loadMore;

  // callback ref · sentinel mount/unmount/replace 都能挂回 IO
  const sentinelRef = useCallback((el: HTMLDivElement | null) => {
    if (observerRef.current) {
      observerRef.current.disconnect();
      observerRef.current = null;
    }
    if (!el) return;
    const io = new IntersectionObserver(
      entries => {
        for (const e of entries) {
          if (e.isIntersecting) {
            loadMoreRef.current();
            break;
          }
        }
      },
      { rootMargin: '300px 0px' },
    );
    io.observe(el);
    observerRef.current = io;
  }, []);

  useEffect(() => {
    return () => {
      if (observerRef.current) {
        observerRef.current.disconnect();
        observerRef.current = null;
      }
    };
  }, []);

  return { visible, sentinelRef, loadMore, hasMore, total, visibleCount };
}
```

## 使用契约

### 1. 全局挂载（一次）

```tsx
// src/App.tsx
<BrowserRouter>
  <ScrollToTop />        {/* ← 必须在 Routes 同级或外层 */}
  <Routes>
    <Route path="/browse/:type" element={<BrowseCategoryPage />} />
    {/* ... */}
  </Routes>
</BrowserRouter>
```

`ScrollToTop` 渲染 `null`，纯副作用组件。**不要**包到 `<Suspense>` 里 —— 会延迟挂载导致首页 scrollRestoration 来不及关。

### 2. 列表页用 hook

```tsx
const { visible, sentinelRef, hasMore } = useInfiniteList(items, cols, {
  rowsPerPage: 4,
  cacheKey: `browse:${type}`,    // ← 关键：跨切换持久进度
});

return (
  <div style={{ overflowAnchor: 'none' }}>
    <div className="grid gap-4" style={{ gridTemplateColumns: `repeat(${cols}, 1fr)`, overflowAnchor: 'none' }}>
      {visible.map((item) => <Card key={item.id} item={item} />)}
    </div>
    {hasMore && <div ref={sentinelRef} aria-hidden style={{ height: 1 }} />}
  </div>
);
```

### 3. cacheKey 命名规范

| 场景 | 命名 | 例子 |
|---|---|---|
| 单一路径，多筛选 tab | `<page>:<tab>` | `browse:style` / `browse:block` |
| 同一页面多 tab 收藏 | `<page>:<sub>:<tab>` | `profile:fav:product` / `profile:fav:style` |
| 跨筛选条件保留 | `<page>:<filterHash>` | `search:q=cool&type=block` |

**禁忌**：
- `cacheKey` 不能撞名 → 不同列表共用 `cacheKey` 会互相覆盖进度
- `cacheKey` 不能含动态 timestamp → 每次进页都是新 key，等于关掉缓存
- `cacheKey` 应该和 URL 语义同步 → 否则用户 POP 回来 ScrollToTop 还原了滚动条但 hook 重置了 visibleCount，列表只渲染一页结果滚动位置落到无内容的下方

## 反模式

- ❌ **混 `content-visibility: auto`** —— 估算 `containIntrinsicSize` 和真实卡高度不一致 → document 总高频繁抖动 → 滚动条跳。验证过，弃用，参见 [沉淀历史](#沉淀历史)
- ❌ **手动翻页按钮** —— 用户期望"一直滚就一直有"；按钮打断节奏，且按下瞬间需要复杂的 scroll lock（多帧 `scrollTo` 强按位置）才能不跳，复杂度反而高
- ❌ **grid 容器漏 `overflow-anchor: none`** —— 浏览器自带 anchor 会在新内容入场时把视口元素挪向某个 anchor，和 IO 追加冲突
- ❌ **POP 时做 `window.scrollTo` 之外的副作用**（比如 `element.scrollIntoView`）—— 和 React Router 的 nav 时序冲突，多帧 setY 会被打回去
- ❌ **不设 `cacheKey`** —— 用户切 tab 回来从头翻，体验断裂
- ❌ **`cacheKey` 撞名** —— 不同列表共用同一 key，互相覆盖
- ❌ **`scrollRestoration` 留默认（auto）** —— 浏览器自带还原会和手动 setY 抢，PUSH 时偶发"先滚到底再钉顶"的可见跳动
- ❌ **`useInfiniteList` 用在虚拟列表（react-window 等）** —— 虚拟列表已经有自己的 visibleRange，再套一层 visibleCount 是双重门控

## 沉淀历史

### v1 · 手动翻页按钮（commit `3c552c1`）
"加载下一页"按钮 + 15 帧 `scrollTo` lock 防止点击瞬间跳屏。问题：移动端 / 大屏滚动用户都习惯无缝懒加载，按钮打断节奏。

### v2 · `content-visibility: auto`（短暂）
全量渲染 + 浏览器自动跳过视口外。`containIntrinsicSize: 320px` 估算占位，但实际卡片高度 310–380px 浮动 → document 高度抖动 → 滚动条跳。**用户报障，弃用**。

### v3 · IO sentinel（当前）
sentinel 距底 300px 触发追加。新内容永远在视口下方 → 已渲染区零位移。配合 `cacheKey` 跨切换持久 + `ScrollToTop` 双 Map 还原 = 完整 4 场景闭环。

## 命名出处

"原语" —— 不是 token 的传统语义（值），而是"约定 + 行为契约"的 first-class 抽象：
- 一处定义（这个 token）
- 多处引用（pages 通过 `uses:` 声明依赖）
- 改一处全链路同步
