---
id: tokens/texture/waveflow/login-dot-grid-mask
type: token
name: 登录页 radial dot 网格 + radial 椭圆 mask
description: 24x24px 灰点阵 + radial 椭圆 mask 中实边羽化 + opacity 0.35 + 鼠标 480px multiply 柔光跟随
platforms: [web]
theme: light
tags:
  aesthetic: [editorial, minimal]
  mood: [calm, dreamy]
  stack: [shadcn-radix]
uses: []
preview: /preview/tokens/texture/waveflow/login-dot-grid-mask
---

# Waveflow Login Radial Dot Grid + Mask

> 登录页左半页背景的"几乎察觉不到"的纹理：24×24px 间距的灰色 1px 点阵，叠加一个椭圆 mask 让中心实、边缘羽化。`opacity: 0.35` 让它"在不在"都行。鼠标移动时一个 480×480px multiply 柔光跟随，与点阵叠合产生微妙互动。

## Tokens

```json
{
  "dot-grid": {
    "backgroundImage": "radial-gradient(circle, #d6d3d1 1px, transparent 1px)",
    "backgroundSize": "24px 24px",
    "opacity": 0.35
  },
  "radial-mask": {
    "maskImage":       "radial-gradient(ellipse at 70% 50%, black 30%, transparent 80%)",
    "WebkitMaskImage": "radial-gradient(ellipse at 70% 50%, black 30%, transparent 80%)"
  },
  "mouse-glow": {
    "size": "480 × 480 px circle",
    "background": "radial-gradient(circle, rgba(99,102,241,0.10), transparent 70%)",
    "mixBlendMode": "multiply",
    "transform": "translate(-50%, -50%)",
    "transition": "opacity 300ms",
    "tracking": "absolute left/top 跟随 onMouseMove (parent rect 相对坐标)"
  }
}
```

## 视觉特征

- **mask 中心偏右 70%**：因为登录表单在左半页左侧，点阵在右侧"漂浮"——mask 让右半最实、左半渐隐，避免点压住文字
- **点 1px 大小**：再大就显"圆点墙纸"，再小就消失——1px @ 24px 间距是临界
- **multiply 混合**：indigo 柔光乘以浅灰点阵，得到的是"点阵局部加深"而非"覆盖一层蓝"——这是看不出来的细节但气质就在这
- **opacity 0.35 + 巨大羽化**：点阵几乎是"暗示"而非装饰

## 适配指南

- 给登录页左半 container 做 `position: relative + overflow: hidden`，点阵和柔光都 absolute inset-0
- 柔光 div 用 `useRef` 让 onMouseMove 直接 `style.left = mouseX + 'px'`，**不用 React state**（每帧重渲染会卡）
- mouseleave 时设 `opacity:0` 让柔光淡出

## 反模式

- ❌ 用 `backgroundColor: indigo-100/30` 平铺——立刻"实色块"
- ❌ 把点阵 opacity 提到 0.6+——抢戏
- ❌ 柔光不用 `mixBlendMode: multiply`——变成"贴一层蓝纸"
