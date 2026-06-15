---
id: components/indicators/sage/crystal-progress-bar
type: component
name: 玻璃质感进度条
description: 10px 圆角条 + 玻璃反光 + 对角条纹 + shimmer 流光 + pulse 阴影呼吸的复合进度组件
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, skeuomorph]
  mood: [calm, dreamy]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/sage/twelve-theme-spectrum
  - tokens/motion/sage/styled-keyframes
preview: /preview/components/indicators/sage/crystal-progress-bar
---

# Crystal Progress Bar

> sage 的"非数字进度"——4 层视觉叠加做出玻璃质感：① 主题色底 + alpha10 容器；② 容器顶部线性渐变白色反光；③ 进度条本体 + 45° 对角白色条纹（stripes 平移）；④ 进度条上 shimmer 倾斜流光扫过；⑤ 进度条尾端 6px 白色光点（带 white shadow）；⑥ 整条 pulse 呼吸阴影。

## 视觉特征

- 容器：`height: 10px; backdrop-filter: blur(8px); border: 1px solid ${color}30; border-radius: 20px; box-shadow: inset 0 2px 4px rgba(0,0,0,0.05)`
- 容器底色：`${color}10` —— 主题色 6% 透明度
- 容器反光：`::before` 50% 高 + `linear-gradient(to bottom, rgba(255,255,255,0.2), transparent)`
- 进度本体：`height: 100%; width: ${percent}%; background: ${color}; border-radius: 20px; transition: width 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)` —— 弹簧曲线
- 进度条纹：`linear-gradient(45deg, rgba(255,255,255,0.15) 25%, transparent 25%, ...)` 30×30px tile，`stripes 1s linear infinite` 平移
- 进度尾光：`::after` 6px 白色 + `box-shadow: 0 0 10px 2px #fff`
- 进度 shimmer：`::before linear-gradient(90deg, transparent, rgba(255,255,255,0.6), transparent)` skewX(-15deg) translateX(-150% → 100%) 1.5s infinite
- pulse：进度条 box-shadow `0 0 8px 0 rgba(c,0.3) → 0 0 16px 2px rgba(c,0.5) → 0 0 8px 0 rgba(c,0.3)` 2s

## 核心代码

```tsx
import styled, { keyframes } from 'styled-components';

const shimmer = keyframes`/* 见 styled-keyframes token */`;
const pulse = keyframes`/* ... */`;
const stripes = keyframes`/* ... */`;

const Container = styled.div<{ $color: string }>`
  height: 10px;
  width: 100%;
  background: ${p => `${p.$color}10`};
  border: 1px solid ${p => `${p.$color}30`};
  border-radius: 20px;
  overflow: hidden;
  backdrop-filter: blur(8px);
  position: relative;
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);

  &::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 50%;
    background: linear-gradient(to bottom, rgba(255,255,255,0.2), transparent);
    pointer-events: none;
  }
`;

const Fill = styled.div<{ $percent: number; $color: string }>`
  height: 100%;
  width: ${p => p.$percent}%;
  background: ${p => p.$color};
  border-radius: 20px;
  transition: width 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
  background-image: linear-gradient(45deg, rgba(255,255,255,0.15) 25%, transparent 25%, transparent 50%, rgba(255,255,255,0.15) 50%, rgba(255,255,255,0.15) 75%, transparent 75%, transparent);
  background-size: 30px 30px;
  animation: ${stripes} 1s linear infinite, ${pulse} 2s infinite ease-in-out;
  position: relative;

  &::after {
    content: '';
    position: absolute;
    top: 0; bottom: 0; right: 0;
    width: 6px;
    background: #fff;
    box-shadow: 0 0 10px 2px #fff;
    border-radius: 0 20px 20px 0;
    opacity: 0.8;
  }

  &::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.6) 50%, transparent 100%);
    transform: translateX(-150%) skewX(-15deg);
    animation: ${shimmer} 1.5s infinite;
  }
`;

export default function CrystalProgress({ percent, color }: { percent: number; color: string }) {
  return (
    <Container $color={color}>
      <Fill $percent={Math.min(100, Math.max(0, percent))} $color={color} />
    </Container>
  );
}
```

## 适配指南

- 用在"批量导入 / 同步进度"等长时间任务，不用做即时进度（即时进度会切得太快看不到效果）
- color 必须是 hex 串（不是 Tailwind 类），从 `THEME_HEX_COLORS[themeColor]` 注入
- percent < 5% 时尾光会叠在容器边缘有点丑，业务可加 `Math.max(percent, 5)` fallback

## 反模式

- ❌ 把它换 `<Progress />` antd 默认进度 —— 会丢掉所有玻璃质感
- ❌ 高频更新 percent —— 0.6s 弹簧曲线 + 1s stripes 节奏会被打乱
