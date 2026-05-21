---
id: tokens/motion/waveflow/three-icosahedron-bg
type: token
name: Three.js 三层同心二十面体背景
description: 3 层不同尺寸 IcosahedronGeometry wireframe (indigo / pink / cyan) + 200 颗背景星点 + 自旋 + 鼠标 lerp 跟随；登录右半页专属
platforms: [web]
theme: dark
tags:
  aesthetic: [editorial]
  mood: [dreamy, confident]
  stack: [shadcn-radix]
uses: []
preview: /preview/tokens/motion/waveflow/three-icosahedron-bg
---

# Waveflow Three Icosahedron BG

> waveflow 登录右半页**唯一**的高科技动效：三层不同尺寸的二十面体线框 (Icosahedron · detail=1) + 200 颗星点，主网自旋 + 鼠标小幅跟随。Indigo `#6366f1` (主) / Pink `#ec4899` (内层) / Cyan `#06b6d4` (外层壳) 三色制造**三维深度感**。`<canvas>` 直挂 absolute inset-0，背景是 dark gradient + radial overlay。

## Tokens

```json
{
  "scene": {
    "camera": "PerspectiveCamera(45deg, container ratio, near 0.1, far 1000)",
    "camera-z": 6,
    "pixelRatio": "Math.min(window.devicePixelRatio, 2)",
    "antialias": true,
    "alpha": true,
    "background": "transparent (走父 div 的 linear+radial gradient)"
  },
  "geometries": {
    "main": {
      "type": "IcosahedronGeometry(1.6, detail=1)",
      "material": "MeshBasicMaterial(color: 0x6366f1, wireframe: true, opacity: 0.85)"
    },
    "inner": {
      "type": "IcosahedronGeometry(0.8, detail=0)",
      "material": "MeshBasicMaterial(color: 0xec4899, wireframe: true, opacity: 0.5)"
    },
    "outer": {
      "type": "IcosahedronGeometry(2.4, detail=1)",
      "material": "MeshBasicMaterial(color: 0x06b6d4, wireframe: true, opacity: 0.25)"
    },
    "stars": {
      "type": "Points 200 颗 · Float32 random ±15",
      "material": "PointsMaterial(color: 0xffffff, size: 0.03, opacity: 0.6)"
    }
  },
  "rotation-tick": {
    "main": "rotation.x += 0.003 / rotation.y += 0.005",
    "inner": "rotation.x -= 0.006 / rotation.y -= 0.008  (反向更快)",
    "outer": "rotation.x += 0.001 / rotation.y += 0.002  (最慢)",
    "stars": "rotation.y += 0.0003"
  },
  "mouse-follow": {
    "rotY": "((e.clientX - rect.left) / rect.width - 0.5) * 0.6",
    "rotX": "((e.clientY - rect.top)  / rect.height - 0.5) * 0.6",
    "lerp": "main.rotation += (target - main.rotation*0.001) * 0.001  (极柔)"
  },
  "background-layers": {
    "linear": "linear-gradient(135deg, #0a0e1a 0%, #1a1530 50%, #0a1822 100%)",
    "radial": "radial-gradient(circle at 30% 40%, rgba(99,102,241,0.3), transparent 60%), radial-gradient(circle at 70% 70%, rgba(6,182,212,0.2), transparent 60%)"
  },
  "lifecycle": {
    "cleanup": "返回 fn 取消 RAF + removeEventListener + dispose 全部 geo/mat + renderer.dispose + removeChild(canvas)"
  }
}
```

## 视觉特征

- **三层同心 + 异速反转**：main 顺时针 / inner 反向更快 / outer 顺时针最慢——三层"独立呼吸"，不是僵硬的同步旋转
- **detail=0 vs 1**：内层 detail=0（基础二十面体，20 个面）和外层 detail=1（细分一次，80 个面）形成"内粗外精"的微妙对比
- **鼠标 lerp 0.001**：极柔——用户能感到响应但不会眩晕；硬规矩是 < 0.005 给精确，> 0.01 给游戏
- **200 颗星 size=0.03**：白点几乎是亚像素级，靠 opacity 0.6 + 模糊渲染做"空间深度"
- 背景双层渐变：linear 给"夜空感"、radial 给"光源点"——单层会很扁

## 适配指南

- 仅用在**特定页面的局部背景**（如登录右半页）；不要全屏铺——CPU/GPU 占用不低
- 父容器必须 `position: relative + overflow: hidden + 给定尺寸`
- 离开页面 `useEffect cleanup` 必须 `dispose` 全部 geo/material + cancelAnimationFrame + 卸载 DOM
- 适配 retina：`renderer.setPixelRatio(Math.min(devicePixelRatio, 2))` 防 3x 屏过载
- 配色硬编码 hex：indigo `#6366f1` / pink `#ec4899` / cyan `#06b6d4`——和 LeftDecor 浮件配色保持同一组

## 反模式

- ❌ 给整站做 Three.js 背景——CPU 30%+，会被运维投诉
- ❌ 去掉 mouse lerp 直接 = target——会突跳很违和
- ❌ pixelRatio 不夹——4K/5K retina 渲染量爆炸
- ❌ 不 dispose——内存泄漏（每次进登录页都 +50MB）
