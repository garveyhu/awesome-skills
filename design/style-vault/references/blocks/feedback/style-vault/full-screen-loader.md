---
id: blocks/feedback/style-vault/full-screen-loader
type: block
name: 全屏柔光加载页
description: 居中 logo 脉动 + emerald→slate 渐变旋转弧 + 柔光呼吸晕 + uppercase 弹跳点文案 · 双模式（fullscreen 接管视口 / inline 60vh 嵌段）
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/style-vault/slate-cyan-cool
  - tokens/typography/pairs/style-vault/inter-editorial-display
  - tokens/motion/style-vault/editorial-flow
preview: /preview/blocks/feedback/style-vault/full-screen-loader
---

# Full Screen Loader

> 项目 Suspense fallback / 路由切换 / 初始化场景的统一加载视觉 —— 不闪烁、不焦虑、有呼吸

## 视觉特征

四层叠加，从下到上：

1. **柔光晕**（最底）—— `top-8` 偏上，`h-40 w-40 rounded-full blur-3xl`，渐变 `from-emerald-200/60 to-slate-200/40`，跑 `sv-breathe` 2.4s ease-in-out infinite（opacity 0.55→0.85 + scale 1→1.05）
2. **静态背景环** —— `circle r=36 stroke=#e2e8f0 strokeWidth=2`，全圆完整描线，提供"轨道"语义
3. **旋转 accent 弧** —— 同尺寸圆，stroke 走 `linearGradient(emerald-500 → slate-900)`，`strokeDasharray="60 180"`（弧长 60、间隔 180 → 1/4 圆露出），`animate-spin` 1.1s linear infinite
4. **中心 logo** —— 真 `<img src="/logo.svg">` 40×40，`sv-logo-pulse` 1.8s ease-in-out infinite（opacity 0.95→1 + scale 1→1.04）

底部文案：
- `flex items-center gap-1`
- `text-[11px] font-medium uppercase tracking-[0.32em] text-slate-400`
- "Loading · · ·" —— 三个 `<span>·</span>` 分别套 `.sv-dot.sv-dot-{1|2|3}`，跑 `sv-dot-bounce` 1.4s ease-in-out infinite，延迟 `0 / 0.16s / 0.32s` 错位 → 三点轮流弹（0.2 → 1 → translateY -3px）

## 双模式

```tsx
<GlobalLoading fullscreen />        // Suspense fallback / 全屏接管
<GlobalLoading fullscreen={false} /> // inline · 嵌段（60vh 居中）
```

- `fullscreen=true`（默认）：`fixed inset-0 z-[9999] bg-white` 全屏接管，z-index 凌驾 modal / topbar / 全部
- `fullscreen=false`：`flex min-h-[60vh] items-center justify-center` 嵌入容器，给 section 内"列表加载中"等场景

## 与同 bucket 区分

- **vs `blocks/feedback/acme/saas-status-banner`**：那条是 30+ px 高的横条状告警（healthy/degraded/critical 三态 inline 持续显示）；本条是全屏 / 大块加载视觉
- **vs 还未沉淀的 skeleton 卡片**：skeleton 是"我知道你这里要显示卡片，先骨架占位"；本条是"什么都还没来，先全屏占位"——粒度差一档

## 核心代码

```tsx
export function FullScreenLoader({ fullscreen = true }: { fullscreen?: boolean }) {
  return (
    <div
      className={
        fullscreen
          ? 'fixed inset-0 z-[9999] flex items-center justify-center bg-white'
          : 'flex min-h-[60vh] items-center justify-center'
      }
    >
      <div className="relative flex flex-col items-center gap-8">
        {/* 柔光晕 */}
        <div
          className="pointer-events-none absolute left-1/2 top-8 h-40 w-40 -translate-x-1/2 rounded-full bg-gradient-to-br from-emerald-200/60 to-slate-200/40 blur-3xl"
          style={{ animation: 'sv-breathe 2.4s ease-in-out infinite' }}
        />

        {/* 旋转环 + 中心 logo */}
        <div className="relative flex h-20 w-20 items-center justify-center">
          {/* 静态背景环 */}
          <svg className="absolute inset-0" viewBox="0 0 80 80" fill="none" aria-hidden>
            <circle cx="40" cy="40" r="36" stroke="#e2e8f0" strokeWidth="2" strokeLinecap="round" />
          </svg>

          {/* 旋转 accent 弧 */}
          <svg
            className="absolute inset-0 animate-spin"
            style={{ animationDuration: '1.1s' }}
            viewBox="0 0 80 80"
            fill="none"
            aria-hidden
          >
            <defs>
              <linearGradient id="sv-loading-grad" x1="0" y1="0" x2="80" y2="80" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stopColor="#10b981" />
                <stop offset="100%" stopColor="#0f172a" />
              </linearGradient>
            </defs>
            <circle
              cx="40" cy="40" r="36"
              stroke="url(#sv-loading-grad)" strokeWidth="2.4" strokeLinecap="round"
              strokeDasharray="60 180"
            />
          </svg>

          {/* 中心 logo */}
          <img
            src="/logo.svg"
            alt=""
            className="relative h-10 w-10"
            style={{ animation: 'sv-logo-pulse 1.8s ease-in-out infinite' }}
          />
        </div>

        {/* 文案 */}
        <div className="relative flex items-center gap-1 text-[11px] font-medium uppercase tracking-[0.32em] text-slate-400">
          <span>Loading</span>
          <span className="sv-dot sv-dot-1">·</span>
          <span className="sv-dot sv-dot-2">·</span>
          <span className="sv-dot sv-dot-3">·</span>
        </div>
      </div>
    </div>
  );
}
```

依赖全局 keyframes（`index.css`，参考 `tokens/motion/style-vault/editorial-flow`）：

```css
/* 柔光呼吸（与空态 blob 共用） */
@keyframes sv-breathe {
  0%, 100% { opacity: 0.55; transform: scale(1); }
  50%      { opacity: 0.85; transform: scale(1.05); }
}

/* logo 柔和脉动 */
@keyframes sv-logo-pulse {
  0%, 100% { opacity: 0.95; transform: scale(1); }
  50%      { opacity: 1;    transform: scale(1.04); }
}

/* 三个 dot 依次弹跳 */
@keyframes sv-dot-bounce {
  0%, 80%, 100% { opacity: 0.2; transform: translateY(0); }
  40%           { opacity: 1;   transform: translateY(-3px); }
}
.sv-dot   { display: inline-block; animation: sv-dot-bounce 1.4s ease-in-out infinite; font-size: 14px; line-height: 0; }
.sv-dot-1 { animation-delay: 0s; }
.sv-dot-2 { animation-delay: 0.16s; }
.sv-dot-3 { animation-delay: 0.32s; }
```

## 适配指南

- 接 Suspense / 路由切换场景用 `fullscreen=true`，`<Suspense fallback={<FullScreenLoader />}>`
- inline 用 `fullscreen={false}` —— 嵌入 section 时容器需要至少 60vh 才能居中得开；否则改用 skeleton
- **logo 必须放真 `/logo.svg` 资产**——脉动是品牌延伸，用泛字符 / 大圈圈替代会让识别度归零
- 如果换品牌（acme / skillhub）复用此结构，`linearGradient` 的两 stop 也要换成对应品牌色（如 acme cyan-400 + slate-950）
- 三个 sv-dot delay `0 / 0.16 / 0.32s` 不要平均 0/0.5/1s——节奏太均匀显机械；当前 1.4 / 5 ≈ 0.28 黄金错位
- 整体可见时长 ≥ 600ms 才让用户看清动画 → 短于这个时长建议直接不显，避免"闪一下又消失"破坏体验

## 反模式

- 不要把 logo 替换成 spinner icon（如 `<LoadingOutlined />`）—— 失去品牌 logo 的标识价值
- 不要 spin duration 缩到 < 1s —— 焦虑感
- 不要去掉 sv-breathe halo —— 没有这层柔光，旋转环看起来像机械加载条
- 不要用 cyan / 暖色替换 emerald 渐变 stop —— emerald 的 healthy/active 语义和"加载进行中"匹配；cyan 是品牌强调色，留给 CTA / focus
- 不要把"Loading"换成中文"加载中" —— 大写 + 0.32em tracking 是这套 caption 的视觉身份；中文 + tracking 字距会断
- 不要让全屏 z-index 低于 modal / toast —— 加载是最高优先级状态
