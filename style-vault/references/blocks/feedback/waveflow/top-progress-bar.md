---
id: blocks/feedback/waveflow/top-progress-bar
type: block
name: 顶部 2px indeterminate progress bar
description: fixed top h-[2px] z-300 indeterminate blue gradient bar - 500ms 防闪 + 100% fade-out + RouteChange + axios pending 双源触发
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm]
  stack: [shadcn-radix]
uses:
  - tokens/motion/waveflow/keyframes-suite
preview: /preview/blocks/feedback/waveflow/top-progress-bar
---

# Waveflow Top Progress Bar (GlobalProgress)

> waveflow 切页 / API pending 时顶部出现的 2px 极细蓝色 indeterminate 条 (`GlobalProgress.tsx`)。**500ms 防闪**（API ≤ 500ms 完成时不显示）+ **100% fade-out**（完成时进度条做完一次完整滑过 + opacity 渐隐 120ms）。RouteChange + axios pending 任意一项触发即可，所有 pending 归零 + 路由稳定 ≥ 120ms 才结束。

## 视觉特征

- **fixed inset-x-0 top-0 z-[300] h-[2px]**：顶部 2px 极细 —— 不抢任何视觉
- **outer**: `pointer-events-none overflow-hidden bg-stone-200/20`
- **inner 滑动条**：
  - `h-full`
  - `background: linear-gradient(90deg, transparent 0%, #3b82f6 40%, #2563eb 60%, transparent 100%)` —— 4-stop 渐变，中间深蓝，两端 transparent
  - `animation: global-progress 1.1s ease-in-out infinite` —— `translateX -100% → 100%`
  - `opacity: fading ? 0 : 1` + `transition: opacity 120ms ease-out`
- **z-[300]**：高于全屏 modal（z-200），低于 Toast（默认 z-9999）

## 行为细节

- **show delay 500ms**：busy 持续 500ms 才显示——避免快速请求闪
- **hide delay 120ms**：busy 归零后等 120ms 再判断（防再次很快又起 pending）
- **路由切换 + axios pending 双源**：useLocation() 监听 path/search 变化 + subscribePending(getPendingCount)
- **fading 状态**：busy 归零先 setFading(true)，让条做 fade-out 再 unmount

## 关键代码

```tsx
const SHOW_DELAY = 500;
const HIDE_DELAY = 120;

useEffect(() => {
  const evaluate = () => {
    if (getPendingCount() > 0) {
      // schedule show after 500ms
    } else {
      // schedule hide after 120ms with fading
    }
  };
  const unsub = subscribePending(evaluate);
  evaluate();
  return () => unsub();
}, []);

useEffect(() => evaluate(), [location.pathname, location.search]);

return visible ? (
  <div aria-hidden className="pointer-events-none fixed inset-x-0 top-0 z-[300] h-[2px] overflow-hidden bg-stone-200/20">
    <div className="h-full" style={{
      background: 'linear-gradient(90deg, transparent 0%, #3b82f6 40%, #2563eb 60%, transparent 100%)',
      animation: 'global-progress 1.1s ease-in-out infinite',
      opacity: fading ? 0 : 1,
      transition: 'opacity 120ms ease-out',
    }} />
  </div>
) : null;
```

## 适配指南

- axios interceptor 维护 pendingCount + subscribePending notify—— 业务无感
- SHOW_DELAY 500ms / HIDE_DELAY 120ms 是黄金组合：500 让短请求不闪 / 120 让"快速接连请求"看起来是同一次
- 配合表格 shimmer skeleton 用 —— 顶部 bar + 表格骨架双指示

## 反模式

- ❌ progress 不防闪—— 短请求闪一下烦人
- ❌ 用真正的 0-100% bar —— 后端不上报进度时假数据不准
- ❌ 用 4-6px 粗 bar —— 抢内容视觉
