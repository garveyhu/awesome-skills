---
id: components/indicators/quiver/autonomy-pill-badge
type: component
name: 自治状态药丸
description: 绿渐变发光的「自治中」文字状态药丸，打开 app 一眼判断公司是否在自主跑
platforms: [web]
theme: dark
tags:
  aesthetic: [glass, minimal]
  mood: [confident, calm]
  stack: [vanilla-css]
uses:
  - tokens/palettes/quiver/night-studio
preview: /preview/components/indicators/quiver/autonomy-pill-badge
---

# 自治状态药丸

> 一颗带文字的状态药丸：开（自治中）= 醒目绿发光，关（手动）= 沉默灰——二元状态一眼可读

## 视觉特征

- **药丸形** `border-radius: var(--r-pill)`，`padding: 3px 9px`，`font-size: 11px; font-weight: 600; letter-spacing: .2px`，`max-width: 190px` 超长截断省略号
- **关态（手动调度）**：弱灰 `color: var(--tx-3)`，底 `var(--s-inset)`，边 `1px solid var(--bd-soft)`——沉默、不抢眼
- **开态（自治中）`.on`**：
  - 底 `background: linear-gradient(180deg, #a6eaa6, #6cc47a)`
  - 字 `color: #0e1a10`（深墨压亮绿）
  - 去边框 `border-color: transparent`
  - 外发光 `box-shadow: 0 0 12px rgba(108,196,122,.3)`——「公司在自己跑」用光感强调
- **文字即状态**：开态显示 `自治推进:{目标}`（超 14 字截断 `…`）或 `自治中`；关态显示 `手动调度`——状态写在脸上，不只靠颜色
- 常驻于玻璃 HUD 最左，作为整条顶栏的「公司心跳」锚点

## 核心代码

```tsx
<span className={`hud-auto${autonomous ? ' on' : ''}`}>
  {autonomous ? (goal ? `自治推进:${trunc(goal, 14)}` : '自治中') : '手动调度'}
</span>
```
```css
.hud-auto { font-size: 11px; font-weight: 600; padding: 3px 9px; border-radius: var(--r-pill);
  color: var(--tx-3); background: var(--s-inset); border: 1px solid var(--bd-soft); }
.hud-auto.on { color: #0e1a10; background: linear-gradient(180deg, #a6eaa6, #6cc47a);
  border-color: transparent; box-shadow: 0 0 12px rgba(108,196,122,.3); }
```

## 适配指南

- 用于任何「系统是否在自主运转」的二元长态：自治 / 手动、监听 / 暂停、在线 / 离线
- 开态复用青柠出发按钮的绿渐变——让「行动绿」语义贯通（绿 = 系统在动）
- 文字必须随状态变，别只换颜色——颜色 + 文字双编码，色盲也能读

## 与 pulse-dot 区分

vault 的 `components/indicators/*` 已有 `pulse-dot` / `status-pulse` / `pulse-ping-dot` / `status-dot-ring` 一族——那是**纯圆点 + 呼吸/涟漪**的极简状态点。**本条不同**：

- pulse-dot 家族是**无文字的圆点**，靠颜色 + 脉冲表达「活着/告警」，体量极小、嵌在行内。
- autonomy-pill-badge 是**带文字的状态药丸**，开态用青柠渐变 + 外发光做强存在感，专门承载「公司是否在自主跑 + 当前自治目标」这种需要被一眼读懂的长态，是 HUD 的语义锚点，不是装饰性小点。

## 反模式

- 不要把它缩成纯圆点——那就退化成 pulse-dot，丢了「文字即状态」的可读性
- 不要给关态也加发光——关态的克制（沉默灰）正是为了反衬开态的醒目
- 不要用琥珀做开态——开态语义是「行动/运转中」，归绿；琥珀留给氛围/选中
