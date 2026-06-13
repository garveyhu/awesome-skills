---
id: tokens/motion/quiver/pixel-steps
type: token
name: 像素步进动效
description: steps() 驱动的像素角色动画 + LED 低频随机明灭 + 体积光束呼吸 + 失焦冻结，整套低开销「活着的办公室」运动语言
platforms: [web]
theme: dark
tags:
  aesthetic: [pixel, retro]
  mood: [playful, nostalgic]
  stack: [vanilla-css]
---

# 像素步进动效

> 角色用 steps() 跳帧、灯光低频随机闪、整套动效失焦即冻——「活着但不烧电」的像素世界运动语言

## 视觉特征

- **角色动画一律 `steps(2)` 跳帧，不平滑补间**：敲键 `typebob .46s steps(2)`、走路 `walkbob .42s steps(2)`、影子 `shadowpace .42s steps(2)`、眨眼 `blinkeye 4.2s steps(1)`、猫 `bob 2.4s steps(2)`——跳帧是像素游戏的灵魂，平滑过渡反而破坏 8-bit 质感
- **待机呼吸用 ease**：身体 `sway 3.4s ease-in-out`、思考点 `thinkpulse 1.4s`、盆栽 `leafsway 4.2s`（三层错相位 -1.3s/-.6s）——只有「活着的轻微摆动」走平滑
- **LED 不挂无限动画，由 JS 低频随机驱动**：`useLedFlicker` 每 **540ms** 一拍，随机翻转 **2–4 颗** `.pled.b` 的 opacity 到 `DIM=0.22`，`transition: opacity .22s linear`——视觉上比整排同步呼吸更像真机房，且脏矩形只覆盖那几像素（整排 CSS 无限动画曾是整机卡顿主因）
- **体积光束缓慢呼吸**：`godray shaft 7.5s`（次光束 9.5s / delay -3s），`skewX` + `scaleX` 微动
- **失焦即冻结**：`useFreezeOnBlur` 给 `<html>` 挂 `.anim-frozen` → `animation: none !important`（比 `paused` 更彻底，后者 WebKit 仍当活动动画）——窗口失焦时不再让 macOS 合成器每帧重栅格化整窗
- **统一缓动 + 双时长**：`--ease: cubic-bezier(.32,.72,.24,1)`，`--t-fast: .12s` / `--t-mid: .2s`；相机滚轮 `.13s ease-out`、复位/下钻 `.6s cubic-bezier(.45,.02,.2,1)`

## Tokens

```json
{
  "step-anim": {
    "typebob": ".46s steps(2) infinite",
    "walkbob": ".42s steps(2) infinite",
    "shadowpace": ".42s steps(2) infinite",
    "blinkeye": "4.2s steps(1) infinite",
    "cat-bob": "2.4s steps(2) infinite"
  },
  "breath-anim": {
    "sway": "3.4s ease-in-out infinite",
    "thinkpulse": "1.4s ease-in-out infinite",
    "leafsway": "4.2s ease-in-out infinite",
    "godray-shaft": "7.5s ease-in-out infinite"
  },
  "led-flicker": { "interval-ms": 540, "flips-per-tick": "2-4", "dim-opacity": 0.22, "transition": "opacity .22s linear" },
  "freeze-on-blur": { "html-class": "anim-frozen", "rule": "animation: none !important" },
  "ease": { "main": "cubic-bezier(.32,.72,.24,1)", "camera-smooth": "cubic-bezier(.45,.02,.2,1)" },
  "duration": { "fast": ".12s", "mid": ".2s", "camera-fast": ".13s", "camera-smooth": ".6s", "walk": ".6s" }
}
```

## 适配指南

- 任何「角色/精灵」动作走 `steps(2)`；任何「环境呼吸」（灯、植物、光束）走 ease-in-out 长循环——两类别混
- **几十个以上的重复闪烁元素（LED/星点）不要各挂 CSS 无限动画**：改成一个 JS 定时器低频随机翻 opacity，脏矩形从「整窗」降到「几像素」
- **任何持续动画都要配失焦冻结**：失焦时 `animation:none`，否则大 retina 窗口空占系统合成器拖累整机

## 反模式

- 不要给像素角色用平滑 transition/补间——破坏跳帧的 8-bit 手感
- 不要用 `animation-play-state: paused` 当「冻结」——WebKit 仍按活动动画处理，照样卡
- 不要全屏平移动画（grain/扫描线滚动）——脏矩形撑满整窗、每帧重栅格化，是掉帧元凶（Quiver 把 grain 改成静态缓存）
