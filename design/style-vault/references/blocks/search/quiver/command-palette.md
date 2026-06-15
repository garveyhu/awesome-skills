---
id: blocks/search/quiver/command-palette
type: block
name: ⌘K 命令面板
description: 磨砂玻璃命令启动器，模糊过滤 + mono 键帽 + 琥珀选中条 + 全键盘导航
platforms: [web]
theme: dark
tags:
  aesthetic: [glass, minimal]
  mood: [calm, serious]
  stack: [vanilla-css]
uses:
  - tokens/palettes/quiver/night-studio
  - tokens/typography/pairs/quiver/sf-system-duo
preview: /preview/blocks/search/quiver/command-palette
---

# ⌘K 命令面板

> 一个 ⌘K 唤起的磨砂玻璃启动器：输入即模糊过滤、上下键导航、回车执行——桌面 app 的「全局动作入口」

## 视觉特征

- **悬浮卡** `.cmdk`：`top: 17%`、`width: min(540px, 92vw)`，磨砂 `var(--s-2)` + `blur(13px)` + `1px solid var(--bd-strong)` + 圆角 `r-3` + 大阴影 `sh-3`
- **进出动效**：`opacity` + `translateY(-10px)→0` + `scale(.99)→1`，`t-fast .12s` 缓动
- **输入行**：透明底、无边框、`font-size: 15px`、`padding: 15px 17px`，底部 `1px` 分隔线；placeholder 走 `tx-3`，文案如「输入命令…  例如 新任务 / 验收 / 急停 / 设预算」
- **命令行 `.row`**：`padding: 9px 13px`、圆角 `r-1`、`font-size: 13px`、`color: tx-2`；左是 `命令名 · 灰提示`，右是 mono 键帽 `kbd`
- **选中态 `.row.sel`**：底 `var(--accent-dim)` + 文字提亮 + **左侧琥珀竖条**（`2.5px` + `box-shadow: 0 0 8px rgba(255,210,122,.5)` 辉光）——选中靠琥珀，呼应全局暖强调
- **键帽 `kbd`**：mono `10.5px/600`，`var(--s-inset)` 底，`border-bottom-width: 2px`（仿实体键凸起），如 `⌘N` / `M` / `⌃.`
- **全键盘**：↑↓ 循环（wrap）、Enter 执行、hover 即选中、点击执行
- 13 条命令：新任务/经理工作台/人事部/系统设置/追溯室/记忆库/调度台/晨报验收/信任设置/派活/派一批/急停/时间线

## 核心代码

```tsx
<div className={`cmdk${open ? ' on' : ''}`}>
  <input placeholder="输入命令…  例如 新任务 / 验收 / 急停 / 设预算" />
  <div id="cmdk-list">
    {filtered.map((c, i) => (
      <div className={`row${i === sel ? ' sel' : ''}`}>
        <span>{c.label} <span className="cmdk-hint">· {c.hint}</span></span>
        {c.kbd && <kbd>{c.kbd}</kbd>}
      </div>
    ))}
  </div>
</div>
```

## 适配指南

- 选中条用全局琥珀强调（accent + accent-dim + 辉光），保持「暖 = 当前焦点」语义一致
- 键帽统一 mono + `border-bottom-width: 2px` 的凸起感；快捷键提示别用裸文字
- 模糊过滤 label + hint 两字段，命令命中更宽

## 反模式

- 不要给选中态用蓝/绿——焦点色全局归琥珀，换色破坏一致性
- 不要省键盘导航——命令面板的价值就在「不碰鼠标」，必须 ↑↓/Enter 全通
- 关闭态别保留磨砂层——`backdrop-filter` 关时仍每帧采样，白耗 GPU
