---
id: pages/dashboard/quiver/office-command-deck
type: page
name: 办公室指挥甲板
description: 单屏 CEO 甲板——等距像素办公室舞台 + 玻璃顶栏 + 底部状态条 + 居中叠层 + 整屏氛围后期
platforms: [web]
theme: dark
tags:
  aesthetic: [pixel, glass]
  mood: [calm, playful]
  stack: [vanilla-css]
uses:
  - blocks/layout/quiver/iso-office-world
  - blocks/nav/quiver/glass-topbar-hud
  - blocks/search/quiver/command-palette
  - blocks/feedback/quiver/world-ambience
  - blocks/display/quiver/glass-panel-modal
preview: /preview/pages/dashboard/quiver/office-command-deck
---

# 办公室指挥甲板

> 整个应用就是一屏：一间活着的像素办公室占满视口，所有功能从「点楼 / 顶栏 / ⌘K」唤起的叠层进入

## 视觉特征 / 页面骨架

- **三层 z 结构**：底层 `#stage`（径向舞台 + 等距办公室 world）→ 中层悬浮 chrome（顶栏 HUD + 底部状态条）→ 顶层叠层（scrim + 命令面板/各模态/工人详情）→ 最上整屏氛围后期（flashfx / vignette / grain / sky / budgetTint / rededge）
- **舞台 `#stage`**：`position: fixed; inset: 0`，径向渐变底；急停时 `.frozen` 全场 `grayscale(.92) brightness(.62)` 灰化压暗
- **没有传统导航/侧栏**：功能入口是「办公室的楼」——点运维楼开设置、点领导区开经理台、点质检台开追溯……顶栏控件 + ⌘K 是补充入口
- **单一主行动**：顶栏右侧青柠出发按钮「CEO 下目标」是全屏唯一亮色锚点
- **状态全靠旁白 + 氛围**：底部状态条实时讲「公司在干嘛」，氛围层把预算/交付翻成体感（转冷转暗 / 边缘泛光）
- **键盘全局**：⌘K 命令面板、`M` 经理台、`⌃.` 急停、`Esc` 收叠层
- **窗口默认 1280×820、最小 880×600**；失焦冻结所有动画

## 核心代码

```tsx
<>
  <div id="stage" className={`stage${frozen ? ' frozen' : ''}`}>
    <Office onOpenPanel={p => setOverlay(p)} />
  </div>
  <div className="topbar"><Hud … /><Ctrls … /></div>
  <Caption text={caption} />
  <div className={`scrim${overlay !== 'none' ? ' on' : ''}`} onClick={close} />
  <CommandPalette open={overlay === 'cmdk'} />
  {/* …各模态面板：晨报 / 经理台 / 追溯 / 记忆 / 调度台 / 设置 / 人事部 … */}
  <Atmosphere spentUsd={…} budgetCapUsd={…} />
  <div id="flashfx" /><div id="vignette" /><div id="grain" />
</>
```

## 适配指南

- 同一时刻至多一个叠层（`Overlay` 单值状态机）；scrim 点击 / Esc 统一收起
- 功能入口优先「点世界里的物体」，顶栏/命令面板作冗余入口——沉浸感来自「楼即入口」
- chrome 与叠层都浮在 world 之上，容器 `pointer-events: none` + 子项 auto，不挡画布

## 反模式

- 不要加传统左侧栏/顶部 tab 导航——会打破「这是一个世界不是一个后台」的错觉
- 不要同时开多个模态——单值 overlay 状态机，互斥
- 不要让叠层挡死世界还不能点空白关闭——scrim 必须可点关
