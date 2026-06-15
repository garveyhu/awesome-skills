---
id: components/indicators/sage/hairline-scrollbar
type: component
name: 极细滚动条体系
description: 7px 全局 / 3px 下拉 / 4px 侧栏 / 0px 隐藏 四档自定义 webkit-scrollbar，sage 不留滚动条视觉债的关键
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/sage/neutral-rgb-ladder
preview: /preview/components/indicators/sage/hairline-scrollbar
---

# Hairline Scrollbar

> sage 不忍受默认浏览器滚动条——`index.less` 全局把 `::-webkit-scrollbar` 砍到 7px、`.sage-dropdown-scroll` 砍到 3px、Sidebar 砍到 4px、CommandPalette 干脆隐藏。一套自定义的滚动条体系，处处可见但永远不抢戏。

## 视觉特征

```css
/* 全局默认 · 7px */
::-webkit-scrollbar { width: 7px; height: 7px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgb(215, 215, 215); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: rgb(185, 185, 185); }

/* AntD select / dropdown 内的滚动 · 3px */
.sage-dropdown-scroll {
  &::-webkit-scrollbar { width: 3px; height: 3px; }
  &::-webkit-scrollbar-track { background: transparent; }
  &::-webkit-scrollbar-thumb { background: rgb(0 0 0 / 2%); border-radius: 1.5px; transition: background-color 0.3s ease; }
  &:hover::-webkit-scrollbar-thumb { background: rgb(0 0 0 / 10%); }
}

/* Sidebar list · 4px (在 styled.div) */
.space-list {
  &::-webkit-scrollbar { width: 4px; }
  &::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 2px; }
}

/* 完全隐藏 · CommandPalette / sessions list / theme picker */
.no-scrollbar {
  scrollbar-width: none;
  -ms-overflow-style: none;
  &::-webkit-scrollbar { width: 0; height: 0; display: none; }
}
```

## 适配指南

- **不是组件，是全局 utility class**：`<div className="sage-dropdown-scroll">...</div>` 直接生效
- AntD Select 注入：`classNames={{ popup: { root: 'sage-dropdown-scroll sage-select-dropdown' } }}`
- 需要"看不见但能滚"用 `no-scrollbar` —— sessions list / theme dot scroller 在用
- macOS 浮层滚动条本来就细，主要适配 Windows 下默认 16px 灰条的辣眼

## 反模式

- ❌ 在某个组件里硬覆盖到 12px+ —— 整体视觉会突兀
- ❌ 给 thumb 加颜色（蓝/绿等）—— 滚动条不要参与主题着色，让它隐形
