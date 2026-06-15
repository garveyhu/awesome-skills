---
id: blocks/feedback/sage/spin-fullscreen-loader
type: block
name: 全屏加载
description: AntD Spin + 主题色注入 + slate-50 背景 + 可选 fullScreen 占据 100vh
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/sage/twelve-theme-spectrum
preview: /preview/blocks/feedback/sage/spin-fullscreen-loader
---

# Spin Fullscreen Loader

> sage 整站 Suspense fallback / 页面切换 loading 用同一个组件——Antd `Spin` 包裹在 styled wrapper 里：背景 slate-50，主题色注入到 `.ant-spin-dot-item`，可选 fullScreen 撑满 100vh。出现在 ChatPage 加载、admin overlay 切换、Layout Suspense fallback。

## 视觉特征

- Wrapper：styled.div `display: flex; align-items: center; justify-content: center; width: 100%; height: 100%; background: #f8fafc /* slate-50 */`
- fullScreen 模式：额外 `min-height: 100vh`
- 主题注入：`.ant-spin .ant-spin-dot-item { background-color: ${primaryColor}; }`
- 三种 size：'small' / 'default' / 'large'，sage 默认 large（最显眼）
- 使用场景：
  - ChatPage 切换会话：`absolute inset-0 bg-white flex items-center justify-center z-50 + <Loader />`
  - Suspense fallback：直接 `<Loader fullScreen themeColor={themeColor} />`
  - admin overlay 切换：`h-full flex items-center justify-center + <Loader />`

## 核心代码

```tsx
import { Spin } from 'antd';
import styled, { css } from 'styled-components';
import { THEME_HEX_COLORS, type ThemeColor } from '@/core/utils/themeUtils';

const StyledWrapper = styled.div<{ $primaryColor: string; $fullScreen: boolean }>`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  background: #f8fafc;

  ${p => p.$fullScreen && css`min-height: 100vh;`}

  .ant-spin .ant-spin-dot-item {
    background-color: ${p => p.$primaryColor};
  }
`;

export default function Loader({
  themeColor = 'blue', size = 'large', fullScreen = false,
}: { themeColor?: ThemeColor; size?: 'small' | 'default' | 'large'; fullScreen?: boolean }) {
  const primary = THEME_HEX_COLORS[themeColor] || '#3b82f6';
  return (
    <StyledWrapper $primaryColor={primary} $fullScreen={fullScreen}>
      <Spin size={size} />
    </StyledWrapper>
  );
}
```

## 适配指南

- 不传 themeColor 默认 blue —— 防止登录前 / 错误状态下没主题
- `fullScreen` 用在 Suspense fallback；普通容器内 loading 用默认（撑满父容器）
- 可以叠加 `<Loader />` 在 absolute inset-0 + bg-white 之上做 overlay loading

## 反模式

- ❌ 自己写 `<div className="animate-spin border-2 border-current"></div>` —— 失去 antd Spin 的语义和 a11y
- ❌ 背景用纯白 —— sage 内容区已经是白底，loading 必须有微弱差色（slate-50）才能被看到
