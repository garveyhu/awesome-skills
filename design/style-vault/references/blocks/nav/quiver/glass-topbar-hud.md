---
id: blocks/nav/quiver/glass-topbar-hud
type: block
name: 玻璃顶栏 HUD
description: 左统计 HUD + 右控件分组 + 主行动按钮的磨砂玻璃顶部指挥栏，悬浮在等距世界上方
platforms: [web]
theme: dark
tags:
  aesthetic: [glass, minimal]
  mood: [calm, confident]
  stack: [vanilla-css]
uses:
  - tokens/palettes/quiver/night-studio
  - tokens/typography/pairs/quiver/sf-system-duo
  - components/buttons/quiver/lime-go-button
  - components/buttons/quiver/glass-chrome-button
  - components/indicators/quiver/autonomy-pill-badge
preview: /preview/blocks/nav/quiver/glass-topbar-hud
---

# 玻璃顶栏 HUD

> 一条悬浮的磨砂玻璃顶栏：左边是公司统计 HUD，右边是控件组 + 出发按钮，从结构上杜绝两者重叠

## 视觉特征

- **外层 `.topbar` 是 flex 两端对齐**：`top: 14px; left/right: 16px`，HUD 居左、控件居右、中间自适应留白；容器本身 `pointer-events: none`（不挡办公室点击），只有 HUD/控件本体可点
- **HUD 胶囊**：`height: 42px`、`padding: 0 18px`、`gap: 18px`，磨砂玻璃 `var(--s-0)` + `blur(13px) saturate(1.25)` + `1px solid var(--bd)` + 圆角 `r-3 14px` + 顶部高光
  - 最左 = **自治状态药丸**（autonomy-pill-badge）
  - 4 个统计 `.stat`：`经理 / 运行 / 通过 / $今夜`，label 用 `tx-2 11.5px`、数字用 `.num`（mono + tabular-nums + 600）
  - 可选 **预算条** `.bar 92×6`：内陷底 + 渐变填充 `linear-gradient(90deg, #6cc47a, var(--accent))` + 琥珀辉光，宽度 = 花费/预算
- **右侧控件区 `.ctrls`**：按「看公司 / 配公司」分两组 `.ctrl-grp`（组内 gap 3、组间 gap 11），全是玻璃 chrome 按钮；最右一个**青柠出发按钮**（CEO 下目标 + 模式标签）
- **底部状态条 `.caption`**（成对出现）：屏幕底居中磨砂胶囊，呼吸绿点 `.dot`（`blink 1.6s`）+ 实时旁白文案
- 整条只有出发按钮是亮色，其余玻璃灰——视线天然落到「下目标」

## 核心代码

```tsx
<div className="topbar">
  <div className="hud">
    <span className="hud-auto on">自治中</span>
    <span className="stat">经理 <b className="num">1</b></span>
    <span className="stat">运行 <b className="num">3</b></span>
    <span className="stat">通过 <b className="num">12</b></span>
    <span className="stat">$<b className="num">4.20</b> 今夜</span>
    <span className="bar"><i style={{ width: '42%' }} /></span>
  </div>
  <div className="ctrls">
    <button className="b-gh b-icon"><span className="cmd">⌘K</span></button>
    <span className="ctrl-grp">{/* 经理 队列 追溯 晨报 */}</span>
    <span className="ctrl-grp">{/* 人事部 记忆 设置 */}</span>
    <button className="b-go">CEO 下目标</button>
  </div>
</div>
```

## 适配指南

- 顶栏容器一律 `pointer-events: none` + 子项 `auto`——浮层不能挡住底下的世界/画布
- 统计数字全挂 `.num`（tabular-nums），实时跳动不抖位
- 控件按功能簇用 `.ctrl-grp` + 留白分组，别用竖分隔线挤宽度；主行动只留出发按钮一个亮点

## 反模式

- 不要让 HUD 和控件可能重叠——用 flex `space-between` 从结构上隔开，别各自 fixed
- 非 retina 屏别给顶栏留磨砂——`backdrop-filter` 会让 subpixel 抗锯齿失效、字糊，退近不透明实底
- 不要在顶栏堆第二个亮色按钮——稀释主行动
