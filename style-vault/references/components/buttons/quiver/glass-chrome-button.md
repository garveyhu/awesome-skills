---
id: components/buttons/quiver/glass-chrome-button
type: component
name: 玻璃 chrome 按钮
description: 磨砂玻璃底 + 内嵌 mono 快捷键药丸 + 纯 CSS 图标态的工具栏控件按钮
platforms: [web]
theme: dark
tags:
  aesthetic: [glass, minimal]
  mood: [calm, serious]
  stack: [vanilla-css]
uses:
  - tokens/palettes/quiver/night-studio
preview: /preview/components/buttons/quiver/glass-chrome-button
---

# 玻璃 chrome 按钮

> 顶栏/控件区的「次级工具按钮」——磨砂玻璃底、可内嵌快捷键药丸、图标用纯 CSS 画

## 视觉特征

- **磨砂玻璃底**：`background: var(--s-1)`（`rgba(18,24,42,.82)`）+ `backdrop-filter: blur(8px) saturate(1.2)` + 顶部内高光 `inset 0 1px 0 var(--hairline-top)`
- **发丝边框** `1px solid var(--bd)`，圆角 `r-2 = 11px`，内边距 `7px 11px`（图标版 `7px 9px`）
- **文字** `var(--tx-2)` → hover 提到 `var(--tx-1)`，底色 hover 到 `rgba(30,38,64,.9)`、边框到 `bd-strong`
- **内嵌快捷键药丸** `.cmd`：mono 字 `11px/600`、`var(--tx-1)`、`1px solid var(--bd-strong)`、圆角 5px、`padding: 1px 5px`——把 `⌘K` 这种提示做成小键帽
- **图标全是纯 CSS，不用图标库**：
  - 暂停 `.ico.pause`：两条 `3px` 竖条（`::before` 左 / `::after` 右）
  - 播放 `.ico.play`：一个 `border-left: 8px solid currentColor` 的三角
- **按下** `transform: translateY(1px) scale(.985)`
- DPR=1 非 retina 屏自动退磨砂、换近不透明实底（`rgba(26,33,56,.96)`）防字糊

## 核心代码

```tsx
<button className="b-gh"><span className="cmd">⌘K</span> 命令栏</button>
<button className="b-gh b-icon"><span className="ico pause" /></button>
```
```css
.b-gh { color: var(--tx-2); background: var(--s-1);
  backdrop-filter: var(--blur-sm); box-shadow: inset 0 1px 0 var(--hairline-top); }
.b-gh:hover { color: var(--tx-1); background: rgba(30,38,64,.9); border-color: var(--bd-strong); }
.b-gh .cmd { font-family: var(--mono); font-size: 11px; font-weight: 600;
  border: 1px solid var(--bd-strong); border-radius: 5px; padding: 1px 5px; }
```

## 适配指南

- 用作所有「次级/工具」动作：打开面板、切播放/暂停、⌘K 入口；主行动留给青柠出发按钮
- 成组时用 `.ctrl-grp`（组内 gap 3）分隔功能簇、组间 gap 11——靠留白分组，不用竖分隔线
- 快捷键提示一律做成 `.cmd` / `kbd` 小键帽，别用裸文字

## 与 ghost-button 区分

vault 里已有 `components/buttons/*/ghost-button`（简洁描边幽灵按钮，浅色内容区的次级 CTA）。**本条不同**：

- ghost-button 是**浅色/内容语境**的描边幽灵按钮，无磨砂、无快捷键键帽。
- glass-chrome-button 是**深色 chrome 工具栏**专用：磨砂玻璃 + `backdrop-filter` + 内嵌 mono 快捷键药丸 + 纯 CSS 暂停/播放图标态，且自带 DPR=1 退磨砂防糊逻辑。它是「应用外壳的控件键」，不是「内容里的次级 CTA」。

## 反模式

- 不要在它上面再叠强色——它的职责是退让，存在感低于主按钮
- 不要用图标库/emoji 替代纯 CSS 图标——Quiver 全程零图标依赖，pause/play/箭头都用 border 画
- 浅色背景别用它——磨砂 + 低 alpha 边框在浅底上糊成一团
