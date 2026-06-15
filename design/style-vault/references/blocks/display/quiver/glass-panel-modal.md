---
id: blocks/display/quiver/glass-panel-modal
type: block
name: 玻璃模态面板
description: 居中磨砂模态系统（标题 / 副标 / kv 行 / 底部行动）+ mac 三灯工人详情卡
platforms: [web]
theme: dark
tags:
  aesthetic: [glass, minimal]
  mood: [calm, serious]
  stack: [vanilla-css]
uses:
  - tokens/palettes/quiver/night-studio
  - tokens/typography/pairs/quiver/sf-system-duo
preview: /preview/blocks/display/quiver/glass-panel-modal
---

# 玻璃模态面板

> 全 app 复用的居中磨砂模态骨架（晨报/调度台/信任卡/设置都用它）+ 点小人弹出的三灯工人详情卡

## 视觉特征

- **遮罩 `.scrim`**：`rgba(5,8,16,.56)` + `blur(3px)`，淡入 `t-mid`，点击关闭
- **居中面板 `.panel`**：`width: min(560px, 92vw)`、`max-height: 84vh`，磨砂 `var(--s-2)` + `blur(13px)` + `1px solid var(--bd-strong)` + 圆角 `r-3` + 大阴影 `sh-3` + 顶部高光
  - 进出：`translate(-50%,-48%) scale(.985)` → `(-50%,-50%) scale(1)`，`t-mid` 缓动
  - 关闭态去磨砂 + `content-visibility: hidden`（省 GPU，避免 8 个面板的模糊层白耗）
  - 宽版 `.panel.wide` = `min(760px, 94vw)`（追溯室）
- **固定骨架**：`h2`（16px/660，`padding: 22px 24px 6px`）→ `.sub`（副标 + 底分隔线）→ `.body`（内容）→ `.foot`（右对齐行动，顶分隔 + `tint-hi` 底）
- **kv 行** `.kv`：左 label `tx-3 / 600 / min-width 64px`，右值可换行；底 `1px bd-soft` 分隔
- **决策/复核行 `.rev`**：`tint-hi` 底卡片 + hover 提亮，内含状态色文字（st-ok 绿 / st-bad 红 / st-warn 琥珀）+ mono 时间
- **面板按钮 `.pbtn`**：玻璃次级（`tint-hi` 底 + `bd-strong`）；主按钮 `.pbtn.go` 走青柠绿
- **输入 `.field`**：`s-inset` 底，聚焦 = **琥珀环** `border-color: rgba(255,210,122,.5)` + `box-shadow: 0 0 0 3px var(--accent-dim)`
- **工人详情卡 `.worksurf`** 变体：青边玻璃浮卡，标题栏带 **mac 三灯**（红 `#e2604f` / 黄 `#ffd27a` / 绿 `#6cc47a`）+ mono 标题，下方 spec / 事件流（按 tool/ok/bad/meta 着色）

## 核心代码

```tsx
<div className={`scrim${open ? ' on' : ''}`} onClick={close} />
<div className={`panel${open ? ' on' : ''}`}>
  <h2>晨报 <span className="h2-dim">昨晚结果</span></h2>
  <div className="sub">公司过夜跑完的交付与待办</div>
  <div className="body">
    <div className="kv"><b>通过</b><span>12 件 · main 是绿的</span></div>
    <div className="rev"><span className="grow">导出功能</span><span className="st-ok">已验收</span></div>
  </div>
  <div className="foot"><button className="pbtn">关闭</button><button className="pbtn go">打回重做</button></div>
</div>
```

## 适配指南

- 所有居中模态复用这套 `h2 / sub / body / foot` 骨架 + `.kv` / `.rev` 行——保证全 app 模态一致
- 输入聚焦环用琥珀（accent），与命令面板选中条同源，焦点色全局统一
- 关闭态务必去磨砂 + `content-visibility: hidden`，别让隐藏面板的 backdrop-filter 白耗 GPU

## 反模式

- 不要每个面板各搓一套头尾——统一骨架，差异只在 `.body`
- 不要给隐藏面板留 `backdrop-filter`——多个模糊层叠着是掉帧大来源
- 焦点环别用蓝/绿——全局焦点色归琥珀
