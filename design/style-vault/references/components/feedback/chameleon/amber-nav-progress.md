---
id: components/feedback/chameleon/amber-nav-progress
type: component
name: 琥珀爬升导航进度条
description: 顶部 2px 琥珀色 determinate 爬升进度条 — pending 时 cubic-bezier 从 0% 慢升到 85%(永不到顶)，pending 清零瞬冲 100% + 淡出；琥珀发光阴影
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
uses:
- tokens/palettes/waveflow/warm-paper-ink-blue
preview: /preview/components/feedback/chameleon/amber-nav-progress
---

# 琥珀爬升导航进度条

> Chameleon 智能导航预取时的顶部反馈条（`NavProgressBar`）。订阅 `nav-pending` store（**非** axios pending），pending 期间用 cubic-bezier 把 2px 琥珀色条从 0% 慢升到 85%（**永远到不了 100%**，营造「还在加载」语义）；pending 清零瞬间冲 100% 再淡出。配琥珀发光 box-shadow。与 waveflow 蓝色 indeterminate 滑动渐变条同位但视觉/机制全异。

## 视觉特征

- 外层（visible 时）：`pointer-events-none fixed left-0 right-0 top-0 z-[1000] h-[2px] bg-transparent`（**z-[1000]**，2px 高，透明轨）
- 内层条：`h-full bg-amber-500 shadow-[0_0_8px_rgba(217,119,6,0.6)] transition-[width,opacity]`
  - `bg-amber-500` = #f59e0b（**单色实心琥珀**）
  - `shadow-[0_0_8px_rgba(217,119,6,0.6)]` = 8px 模糊深琥珀(#d97706/60%) 发光
- 动态 style：
  - `width = ${width}%`（0 → 85 → 100）
  - `opacity = (width === 100 && !pending) ? 0 : 1`（冲顶后淡出）
  - `transitionDuration = pending ? '600ms' : '200ms'`（爬升 600ms 慢 / 冲顶 200ms 快）
  - `transitionTimingFunction = pending ? 'cubic-bezier(0.16, 1, 0.3, 1)' : 'ease-out'`（**爬升用 expo-out 创意曲线**）
- 爬升逻辑：
  - pending → `setVisible(true)` + `setWidth(0)`，下一帧 `requestAnimationFrame(() => setWidth(85))`（触发 transition 慢升到 85%）
  - pending 清零 → `setWidth(100)`，250ms 后 `setVisible(false)` + `setWidth(0)`（冲顶 + 淡出）

## 核心代码

```tsx
useEffect(() => {
  let raf, fadeOut;
  if (pending) {
    setVisible(true);
    setWidth(0);
    raf = requestAnimationFrame(() => setWidth(85));  // 慢升永不到顶
  } else if (visible) {
    setWidth(100);                                     // 冲顶
    fadeOut = setTimeout(() => { setVisible(false); setWidth(0); }, 250);
  }
  return () => { cancelAnimationFrame(raf); clearTimeout(fadeOut); };
}, [pending, visible]);

if (!visible) return null;
<div className="pointer-events-none fixed left-0 right-0 top-0 z-[1000] h-[2px] bg-transparent">
  <div className="h-full bg-amber-500 shadow-[0_0_8px_rgba(217,119,6,0.6)] transition-[width,opacity]"
    style={{
      width: `${width}%`,
      opacity: width === 100 && !pending ? 0 : 1,
      transitionDuration: pending ? '600ms' : '200ms',
      transitionTimingFunction: pending ? 'cubic-bezier(0.16, 1, 0.3, 1)' : 'ease-out',
    }} />
</div>
```

## 与 waveflow/top-progress-bar 区分

| 维度 | waveflow/top-progress-bar | 本条 amber-nav-progress |
|------|---------------------------|--------------------------|
| 颜色/填充 | 蓝色 4-stop 渐变 `linear-gradient(90deg, transparent, #3b82f6 40%, #2563eb 60%, transparent)` | **单色实心 amber-500 (#f59e0b)** |
| 机制 | **indeterminate** 滑动（`translateX -100% → 100%` 1.1s `infinite` 循环） | **determinate 爬升**（width 0→85→100，无循环） |
| 时序曲线 | `ease-in-out` 匀速循环 | **`cubic-bezier(0.16,1,0.3,1)` expo-out 慢升 600ms** + 冲顶 ease-out 200ms |
| 阴影 | 无 | **琥珀发光 `shadow-[0_0_8px_rgba(217,119,6,0.6)]`** |
| z-index | `z-[300]` | **`z-[1000]`** |
| 防闪 | 500ms show-delay + 120ms hide-delay | 无 show-delay，直接 raf 起升；250ms fade-out |
| 触发源 | RouteChange + axios pending 双源 | **nav-pending store 单源（智能导航预取）** |
| 轨底 | `bg-stone-200/20` | `bg-transparent` |

选型：要「请求进行中的不确定等待」用 waveflow 蓝色循环条；要「导航预取这件确定的事在推进」用本条琥珀爬升条。

## 适配指南

- 这是「乐观爬升」套路（类 nprogress）——后端不上报真实进度，85% 上限是「装作快好了但留余地」的心理学
- 订阅源是 `nav-pending-store`（导航预取），别接到全局 axios pending——否则任何请求都触发，丧失「导航中」语义
- `requestAnimationFrame` 包 setWidth(85) 是关键——直接 setWidth 不触发 transition（同一帧 0→85 无过渡）

## 反模式

- ❌ width 直接到 100% 慢升——会显得「已加载完」但其实还在等，必须卡在 85%
- ❌ 去掉发光阴影——琥珀发光是本条区别于 waveflow 蓝条的视觉签名
- ❌ 不用 raf 包初始 setWidth——transition 不触发，条会瞬间跳到 85%
- ❌ 接 axios pending 当触发源——失去「智能导航预取」语义，变成通用 loading
