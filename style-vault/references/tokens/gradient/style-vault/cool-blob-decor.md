---
id: tokens/gradient/style-vault/cool-blob-decor
type: token
name: 冷感漂浮气泡装饰
description: 双 blob 漂浮装饰 —— cyan-100 + slate-200，blur-3xl 模糊 + 长周期 keyframes 漂移
platforms: [any]
theme: light
tags:
  aesthetic: [minimal, organic]
  mood: [calm, dreamy]
  stack: [react-antd-tailwind, html-tailwind]
preview: /preview/tokens/gradient/style-vault/cool-blob-decor
---

# Cool Blob Decor

> Hero 区上方"漂浮的冷光"——靠 2 颗 blur 圆形色块 + 慢漂移制造冷感却不死板的氛围

## 视觉特征

两颗模糊圆斑作为 hero / cover 的氛围底——

- **左大** `520x520`，cyan-100 半透明（`bg-cyan-100/50`），偏左上 `-left-40 -top-40` 露出 4/5
- **右小** `440x440`，slate-200 半透明（`bg-slate-200/55`），偏右上 `-right-40 top-20` 露出 3/4
- 都套 `blur-3xl`（约 64px 高斯模糊），变成纯氛围色而非可辨形状
- 父容器必须 `relative overflow-hidden`——blob 用 absolute 锚点定位，本身 `pointer-events-none` 不挡交互
- 各自跑独立 keyframe：左 14s `translate3d(20px,-30px) scale(1.08)` ease-in-out infinite，右 18s `translate3d(-30px,20px) scale(1.12)` ease-in-out infinite——**异步周期**让画面始终在动但永不同步
- 一侧 hue 偏冷 cyan、一侧 hue 偏中性 slate——**绝不**双侧同色（变成"两个发光球"，密度感差）

## Tokens

```json
{
  "blobs": [
    {
      "name": "cyan-lead",
      "size": "520px",
      "color": "rgba(207,250,254,0.5)",
      "anchor": { "left": "-160px", "top": "-160px" },
      "blur": "64px",
      "animation": "blob-drift",
      "duration": "14s",
      "easing": "ease-in-out",
      "iteration": "infinite"
    },
    {
      "name": "slate-trail",
      "size": "440px",
      "color": "rgba(226,232,240,0.55)",
      "anchor": { "right": "-160px", "top": "80px" },
      "blur": "64px",
      "animation": "blob-drift-slow",
      "duration": "18s",
      "easing": "ease-in-out",
      "iteration": "infinite"
    }
  ],
  "keyframes": {
    "blob-drift":      "0%,100% { transform: translate3d(0,0,0) scale(1); } 50% { transform: translate3d(20px,-30px,0) scale(1.08); }",
    "blob-drift-slow": "0%,100% { transform: translate3d(0,0,0) scale(1); } 50% { transform: translate3d(-30px,20px,0) scale(1.12); }"
  },
  "container": {
    "position": "relative",
    "overflow": "hidden",
    "z-index": "blob 在 z-0；内容必须 z-10+ 或 relative"
  }
}
```

## 适配指南

- **必须** parent 加 `relative overflow-hidden`，否则 blob 会溢出搞乱布局
- blob 一定 `pointer-events-none`，否则会拦下面的点击
- 内容层叠顺序：blob 默认 z-0，内容包一层 `relative` 或 `z-10` 即升到上面
- **同屏 ≤ 1 处** blob 群——hero 用了就不要再在下面 section 重复用，避免视觉拥挤
- 暗色面板上要把颜色调到 `cyan-500/10` + `slate-500/15`（透明度更低 + 色相加深，否则在 dark 上看不见）
- 两颗大小要保持差距（520 vs 440 = 1.18×）——双方等大会失去层次

## 反模式

- 不要 ≥ 3 颗 blob——画面会糊成"果冻底"
- 不要不加 blur 直接用纯色圆——立刻变成 80 年代海报
- 不要把 blob 颜色换成暖色（橙/玫红/黄）——破坏冷感系统的核心
- 不要把 duration 缩到 < 8s——肉眼能感知到运动会变焦虑
- 不要双侧 keyframes 同周期——画面在脉冲而不是漂浮
