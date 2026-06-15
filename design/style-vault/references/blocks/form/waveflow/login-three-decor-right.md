---
id: blocks/form/waveflow/login-three-decor-right
type: block
name: 登录右半 Three.js 装饰区
description: dark linear gradient + radial overlay glow + Three.js icosahedron canvas + bottom tagline (11px tracking-[0.4em] 上 / 30px serif italic 诗句下) - 仅 lg+ 显示
platforms: [web]
theme: dark
tags:
  aesthetic: [editorial, minimal]
  mood: [dreamy, confident]
  stack: [shadcn-radix]
uses:
  - tokens/motion/waveflow/three-icosahedron-bg
preview: /preview/blocks/form/waveflow/login-three-decor-right
---

# Waveflow Login Three Decor Right (Right Half)

> 登录右半页——只在 `lg+` 显示。背景由 3 层叠加：底层 dark `linear-gradient(135deg, #0a0e1a 0%, #1a1530 50%, #0a1822 100%)` 太空感 + radial 双光源 (indigo 30%/cyan 20% transparent 60%) 局部发亮 + 上层 Three.js 三层 icosahedron + 200 星点。底部诗句区两段叠（小副标 11px tracking-[0.4em] + 30px sans + serif italic 词组）。

## 页面骨架

```tsx
<div className="relative hidden w-1/2 overflow-hidden lg:block">
  {/* 底层 dark gradient */}
  <div className="absolute inset-0"
    style={{ background: 'linear-gradient(135deg, #0a0e1a 0%, #1a1530 50%, #0a1822 100%)' }} />

  {/* radial 双光源（pointer-events-none 防遮挡） */}
  <div className="pointer-events-none absolute inset-0" style={{
    background: 'radial-gradient(circle at 30% 40%, rgba(99,102,241,0.3), transparent 60%), '
              + 'radial-gradient(circle at 70% 70%, rgba(6,182,212,0.2), transparent 60%)'
  }} />

  {/* Three.js canvas */}
  <ThreeBackground />

  {/* 底部诗句 */}
  <div className="pointer-events-none absolute inset-x-0 bottom-0 z-10 flex flex-col p-10 text-white">
    <p className="mb-2 text-[11px] tracking-[0.4em] text-white/40" style={{ writingMode: 'horizontal-tb' }}>
      实时编排 · 数据中枢
    </p>
    <h2 className="text-[30px] font-light leading-tight tracking-tight" style={{ letterSpacing: '-0.01em' }}>
      让数据，
      <span className="text-white/85"
        style={{ fontFamily: 'var(--font-serif)', fontStyle: 'italic', fontWeight: 400 }}>
        自如流转。
      </span>
    </h2>
  </div>
</div>
```

## 视觉特征

- **`hidden lg:block`**：仅 1024px+ 显示——移动设备只见左半表单
- **dark gradient 3 stop**：从黑紫(`#0a0e1a`)→暗紫(`#1a1530`)→暗青(`#0a1822`)——3 色让"夜空"立体
- **radial 2 glow**：indigo 30% (左上) + cyan 20% (右下)——和 Three.js mesh 同色相，呼应
- **诗句两段对比**：小副标 `tracking-[0.4em]` 极宽（0.4em ≈ 5px 字距）+ stone-white/40 极淡 → 30px serif italic + white/85 较实
- **`font-weight 300` (font-light)**：30px 大标题用 light 而非 medium——editorial 显瘦
- **`writing-mode: horizontal-tb` 显式声明**：兼容某些浏览器把它默认竖排
- **整个底部 `p-10` (40px) padding**：让诗句不贴底

## 适配指南

- 用 lazy import 加载 ThreeBackground：`const ThreeBackground = React.lazy(...)` —— Three.js 600KB gzip 后 140KB，登录不应在首屏就加载（实际 waveflow 没 lazy，因登录就是首页）
- 诗句文案可换，但保持"上小副标全大写宽字距 + 下大字 serif italic"的两段对比模式
- 不在右半放任何 interactive 元素——纯装饰

## 反模式

- ❌ 右半放表单 —— 失去 editorial split 的对比感
- ❌ 文字用 white 实色 —— 在彩色 Three.js 上下不够柔和（用 white/85 / white/40）
- ❌ Three.js 加交互（点击 mesh 等）—— 抢登录表单焦点
- ❌ serif 不用 italic —— 失去"editorial 诗句"气质
