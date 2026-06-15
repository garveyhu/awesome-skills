---
id: components/buttons/quiver/lime-go-button
type: component
name: 青柠出发按钮
description: 青柠渐变 + 深墨字 + 绿辉光的主行动按钮，深色界面里唯一的「行动绿」
platforms: [web]
theme: dark
tags:
  aesthetic: [glass]
  mood: [confident, energetic]
  stack: [vanilla-css]
uses:
  - tokens/palettes/quiver/night-studio
preview: /preview/components/buttons/quiver/lime-go-button
---

# 青柠出发按钮

> 整个冷暗界面里唯一的「行动绿」——CEO 下目标 / 确认派活的主按钮，亮到一眼锁定

## 视觉特征

- **青柠竖向渐变**：`background: linear-gradient(180deg, #a6eaa6, #6cc47a)`，无边框（`border: 0`）
- **深墨字** `#0e1a10`，`font-weight: 600`——深色字压在亮绿上，对比强、像「实体亮键」
- **三层光影叠出实体感**：`box-shadow: var(--sh-1), 0 6px 18px rgba(108,196,122,.28), inset 0 1px 0 rgba(255,255,255,.4)`——外阴影 + 绿辉光 + 顶部内高光
- **hover 提亮**：`linear-gradient(180deg, #b0f0b0, #75cd83)`，辉光加深到 `.34`
- **按下** `transform: translateY(1px) scale(.985)`，像真键回弹
- **圆角** `r-2 = 11px`，内边距 `7px 11px`（顶栏版）/ `9px 14px`（面板版 `.pbtn.go`）
- **可带前箭头** `.arr`：纯 CSS `border-left: 5px solid currentColor` 三角，不用图标库
- 默认带模式小标签（`真实` / `模拟`），`margin-left: 6px; opacity: .8`

## 核心代码

```tsx
<button className="b-go">
  CEO 下目标 <span className="lbl">{mode === 'real' ? '真实' : '模拟'}</span>
</button>
```
```css
.b-go { color: #0e1a10; font-weight: 600; border: 0;
  background: linear-gradient(180deg, #a6eaa6, #6cc47a);
  box-shadow: var(--sh-1), 0 6px 18px rgba(108,196,122,.28), inset 0 1px 0 rgba(255,255,255,.4); }
.b-go:active { transform: translateY(1px) scale(.985); }
```

## 适配指南

- **一屏只放一个**——它是唯一的主行动锚点；次级动作交给玻璃 chrome 按钮（ghost）或面板 `.pbtn`
- 「绿=行动/成功」「琥珀=氛围/选中」分工要守住：别用琥珀做主按钮、也别用绿做选中条
- 面板内版本用 `.pbtn.go`，去掉 sh-1 外阴影、辉光收到 `.26`

## 反模式

- 不要给它描边或改成幽灵态——它的存在感来自实色亮绿 + 深字，描边会泄气
- 不要在同屏出现第二个亮绿按钮——会稀释「这就是要点的那个键」
- 不要用浅字压亮绿——对比不足，失去「实体键」的厚重感
