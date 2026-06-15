---
id: tokens/texture/waveflow/login-floating-geom-quartet
type: token
name: 登录页 4 SVG 浮件 + RAF 动态连线
description: 同心圆紫 / 圆角方粉 / 三角青 / 圆点橙 4 个 SVG 几何浮件 + decor-drift 漂浮 + 鼠标 ↔ 浮件 / 浮件 ↔ 浮件 RAF 动态 SVG 连线
platforms: [web]
theme: light
tags:
  aesthetic: [editorial, minimal]
  mood: [dreamy, playful]
  stack: [shadcn-radix]
uses:
  - tokens/motion/waveflow/keyframes-suite
preview: /preview/tokens/texture/waveflow/login-floating-geom-quartet
---

# Waveflow Login Floating Geom Quartet

> 登录左半页"会动的星座"：4 个尺寸不一的 SVG 几何（紫同心圆 48px / 粉圆角方 36px / 青三角 40px / 橙圆点 28px），各自走 decor-drift-1/2/3 keyframe 漂浮 + 自旋。第二个 RAF 循环把每个浮件的实时坐标喂给一个全屏 SVG，鼠标 → 最近 2 个浮件 + 浮件 ↔ 浮件 < 240px 距离时画 0.5–0.8px indigo 连线。这是 waveflow 登录页"editorial 性格"的根。

## Tokens

```json
{
  "geoms": [
    {
      "id": "geo1",
      "shape": "同心圆 · 紫",
      "size": "48 × 48 px",
      "svg": "<circle r=22 stroke=#6366f1 sw=1 op=0.5/> + <circle r=14 fill=#6366f1 op=0.18/>",
      "position": "top: 22%; right: 18%",
      "animation": "decor-drift-1 7s ease-in-out infinite",
      "z": 3
    },
    {
      "id": "geo2",
      "shape": "圆角方 · 粉",
      "size": "36 × 36 px",
      "svg": "<rect rx=6 stroke=#ec4899 sw=1 op=0.6/> + <rect 内 rx=3 fill=#ec4899 op=0.15/>",
      "position": "top: 50%; right: 8%",
      "animation": "decor-drift-2 8s ease-in-out infinite",
      "z": 3
    },
    {
      "id": "geo3",
      "shape": "三角形 · 青",
      "size": "40 × 40 px",
      "svg": "<polygon stroke=#06b6d4 sw=1 op=0.55/> + <polygon 内 fill=#06b6d4 op=0.18/>",
      "position": "top: 70%; right: 28%",
      "animation": "decor-drift-3 9s ease-in-out infinite",
      "z": 3
    },
    {
      "id": "geo4",
      "shape": "圆点 · 橙",
      "size": "28 × 28 px",
      "svg": "<circle r=3 fill=#f59e0b/> + <circle r=12 stroke=#f59e0b sw=1 op=0.4/>",
      "position": "top: 38%; right: 35%",
      "animation": "decor-drift-1 6s ease-in-out infinite",
      "z": 3
    }
  ],
  "dynamic-lines": {
    "max-dist": 240,
    "rendering": "innerHTML 全替换 (svg.innerHTML = lines.join(''))",
    "mouse-to-geom": {
      "trigger": "mouse 在区域内时取最近 2 个",
      "stroke": "#6366f1",
      "stroke-width": "0.8",
      "opacity": "((1 - d/MAX_DIST) * 0.55).toFixed(3)  动态"
    },
    "geom-to-geom": {
      "trigger": "所有 pair（4 取 2 = 6 对）距离 < 240 时",
      "stroke": "#6366f1",
      "stroke-width": "0.5",
      "opacity": "((1 - d/MAX_DIST) * 0.25).toFixed(3)"
    }
  },
  "z-order": "0 dot grid · 1 dynamic SVG · 2 mouse glow · 3 floating geoms"
}
```

## 视觉特征

- **4 个不同形状**：圆 / 方 / 三角 / 点——基本几何全凑齐，但每个**结构都是"线+实"两层**（外描边 + 内填充），让小尺寸也有"重量"
- **配色 4 色对应右半 Three.js 三色 + 一**：紫 indigo / 粉 / 青 ↔ Three.js icosahedron 三色 + 橙 → 整页色彩闭环
- **drift 用独立 translate/rotate L4 属性**：和 mouseover transform 解耦，所以连线测量用 getBoundingClientRect 永远拿到真实位置
- **连线粗细差 60%**：鼠标→浮件 0.8px，浮件→浮件 0.5px——区分"主动" vs "环境"
- **opacity 与距离线性衰减**：< 240px 才连，连线在边界处自然淡到 0

## 适配指南

- DOM 层级必须严格：底 dot grid (z 0) → svg 连线 (z 1) → 柔光 (z 2) → 浮件 (z 3)，否则浮件被柔光盖住
- RAF tick 每帧做：`svg.setAttribute('viewBox', ...)` + 重算 6 对距离 + `svg.innerHTML = lines.join('')`
- 浮件 ref 用 `useRef` 数组传给 RAF 闭包；不要用 state（每帧 rerender 会卡）
- 测量浮件中心：`getBoundingClientRect()` 减去 parent rect 偏移

## 反模式

- ❌ 用 emoji / png 替代 SVG——丢失 stroke/opacity 可控性
- ❌ 浮件配色用同色相——失去"星座感"
- ❌ 连线 > 1px 粗——立刻显廉价
- ❌ MAX_DIST 太大（> 350）—— 每个浮件都连，太"密"
