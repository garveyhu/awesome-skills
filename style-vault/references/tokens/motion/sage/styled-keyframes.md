---
id: tokens/motion/sage/styled-keyframes
type: token
name: 七段装饰性动画
description: bling/earthSpin/snowFall/wobble/shimmer/pulse/stripes 七段专属 keyframes，承载 RevolverMenu 飘雪与 CrystalProgress 流光
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, retro]
  mood: [playful, dreamy]
  stack: [react-antd-tailwind]
uses: []
preview: /preview/tokens/motion/sage/styled-keyframes
---

# Sage Styled Keyframes

> 当 tailwindcss-animate 不够用时，sage 用 `styled-components` 的 `keyframes` 写复杂动画。所有 keyframes 集中在 7 个：4 个给 `RevolverMenu`（雪人 + 飘雪 + 旋转）、3 个给 `CrystalProgress`（流光条纹）。

## Tokens

```json
{
  "keyframes": {
    "bling": {
      "duration": "1s infinite",
      "use": "RevolverMenu 主按钮 hover 缩放呼吸",
      "css": "0% scale(1) → 50% scale(1.1) → 100% scale(1)"
    },
    "earthSpin": {
      "duration": "8s linear infinite (geo) / 3s linear infinite (orbit)",
      "use": "RevolverMenu 地球图标自转 / Orbit ring hover 转动",
      "css": "0% rotate(0deg) → 100% rotate(360deg)"
    },
    "snowFall": {
      "duration": "随机 4-12s linear infinite",
      "use": "RevolverMenu pinned 时雪花从顶向下飘",
      "css": "0% translateY(-10px) translateX(0) opacity 0 → 10% opacity 1 → 90% opacity 1 → 100% translateY(100px) translateX(20px) opacity 0"
    },
    "wobble": {
      "duration": "0.6s ease-in-out",
      "use": "RevolverMenu hover 雪人左右摇摆",
      "css": "0% rotate(0) → 25% rotate(-8deg) → 50% rotate(8deg) → 75% rotate(-4deg) → 100% rotate(0)"
    },
    "shimmer": {
      "duration": "1.5s infinite",
      "use": "CrystalProgress 玻璃流光",
      "css": "0% translateX(-150%) skewX(-15deg) → 50%/100% translateX(100%) skewX(-15deg)"
    },
    "pulse": {
      "duration": "2s infinite ease-in-out",
      "use": "CrystalProgress / RevolverMenu Ring 呼吸阴影",
      "css": "0% box-shadow 0 0 8px 0px rgba(c,0.3) → 50% 0 0 16px 2px rgba(c,0.5) → 100% 0 0 8px 0px rgba(c,0.3)"
    },
    "stripes": {
      "duration": "1s linear infinite",
      "use": "CrystalProgress 进度条对角条纹平移",
      "css": "0% background-position 0 0 → 100% background-position 30px 0"
    }
  },
  "transitionEasings": {
    "snappy":  "cubic-bezier(0.34, 1.56, 0.64, 1)",
    "smooth":  "cubic-bezier(0.2, 0.8, 0.2, 1)"
  }
}
```

## 视觉特征

- `bling` + `wobble` 给 RevolverMenu 一个"活物"的人格——呼吸 + 撒娇
- `snowFall` 是 RevolverMenu pinned（钉住打开）时的环境效果，让圆形菜单变成一个迷你雪景球
- `shimmer` 在 `CrystalProgress` 里以 `skewX(-15deg)` 倾斜扫过，是玻璃质感的关键
- `earthSpin` 跟 `pulse` 配对：地球转 + 阴影呼吸，给"加载中 / 思考中"赋予存在感
- 所有 keyframes 时间偏长（0.6s 起、最长 12s）—— 是装饰，不是反馈

## 适配指南

- 用 `import styled, { keyframes } from 'styled-components'` 引入
- 容器组件需要传入 `$color` / `$delay` 等 prop，让 keyframes 跟随主题色
- snowFall 实例要随机 `$delay` / `$left` / `$size` / `$duration` / `$opacity` —— 否则雪花变成机械方阵

## 反模式

- ❌ 把这些动画用在普通 hover 反馈 —— 太戏剧化
- ❌ 在不支持 styled-components 的纯 CSS 里硬抄 —— sage 用了 6 个文件 keyframes，纯 CSS 无法复用变量
