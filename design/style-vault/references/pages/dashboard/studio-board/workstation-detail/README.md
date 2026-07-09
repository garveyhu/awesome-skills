---
id: pages/dashboard/studio-board/workstation-detail
type: page
name: 详情页三栏工作台
description: 视口定高三栏白玻璃工作台——浮动玻璃顶栏 + 260px 生产管线轨 + 主玻璃卡(步头+块内滚内容) + 360px 发布备料玻璃卡；4 玻璃块各自块内滚、壳不滚
platforms: [web]
theme: both
tags:
  aesthetic: [glass, minimal, editorial]
  mood: [warm, calm, serious]
  stack: [react-tailwind]
uses:
  - components/display/studio-board/warm-glass-card
  - blocks/nav/studio-board/pipeline-rail
  - blocks/display/studio-board/publish-hero
  - tokens/palettes/studio-board/warm-sand-ink
  - tokens/texture/studio-board/warm-paper-grain
preview: /preview/pages/dashboard/studio-board/workstation-detail
---

# 详情页三栏工作台

> 一条内容的生产工作台：暖砂颗粒底上浮着**四块独立白玻璃**（顶栏 / 管线轨 / 主工作台 / 发布备料），视口定高、各块内部各滚、外壳不滚 → 零抖动。

## 页面骨架

- **外壳**：`flex min-h-screen flex-col gap-3 p-3 sm:gap-4 sm:p-4 lg:h-screen lg:overflow-hidden`——lg 起锁视口高、壳 `overflow-hidden`，滚动交给各块内部
- **① 浮动玻璃顶栏**（`studio-glass rounded-lg px-4 py-3 · shrink-0`）：`← 看板` 返回 pill + 标题(`text-[15px] font-semibold`)/slug(mono) + 冲突计数徽标(陶土·`X 处记录对不上`) + 右侧 HeaderProgress（进度圆点 `●●● ●●●●●` + `全部完成`）+ 交付 chip（`已发布 · 74.6MB · 7-05 17:58`）+ 亮/暗切换 `◐` 按钮
- **② 主区**（`grid lg:grid-cols-[260px_1fr] · lg:min-h-0 lg:flex-1`）：
  - **左 260px = 管线轨**（[[pipeline-rail]]）
  - **右 = 工作台 Outlet**：内部再 `grid lg:grid-cols-[minmax(0,1fr)_360px]`
    - **主玻璃卡**：`studio-glass flex-col overflow-hidden` → 步头(定高·`border-b px-7 py-2.5`：状态灯 + 步名 `font-display text-lg` + 创意/制作 tag + 状态胶囊 + 更新时间 mono + 刷新按钮) + 内容区(`sb-thin-scroll overflow-y-auto`·块内滚：发布步顶部整宽挂 [[publish-hero]]，下方 `px-7 py-5` 资源/编辑器/动作)
    - **右 360px 备料玻璃卡**：`studio-glass overflow-y-auto p-4` → 步骤详情 / 发布备料（平台核对 + 一键预填 CTA + 回填链接）
- **视觉要点**：底是 [[warm-paper-grain]]（颗粒 + 金光弥散 + `bg-attachment:fixed`）；四块玻璃卡靠间距 `gap-3/4` 浮起、互不重叠；亮=暖砂、暗=冷 slate（顶栏 `◐` 切 `data-theme` + localStorage 持久）

## 适配指南

- 「视口定高 + 各块内部各滚」是零抖动的关键：外壳 `lg:h-screen overflow-hidden`，每块 `overflow-y-auto` + `lg:min-h-0`
- 三栏比例 `260px / 1fr / 360px`——导航轨窄、主台弹性、备料定宽；窄屏 `grid-cols-1` 堆叠
- 玻璃卡数量克制在「四大功能区各一块」，别再往里套玻璃叠玻璃

## 反模式

- 不要整页一个大滚动容器（会满屏抖 + 顶栏跟滚）——四块各自内滚
- 不要玻璃卡堆叠玻璃卡（模糊叠模糊浑浊）
- 不要暗态沿用暖砂 + 颗粒（改冷 slate + 关颗粒）

## 引用关系

- uses：warm-glass-card · pipeline-rail · publish-hero · warm-sand-ink · warm-paper-grain
- used by：`styles/content-media/warm-sand-workbench` · `products/studio-board`
