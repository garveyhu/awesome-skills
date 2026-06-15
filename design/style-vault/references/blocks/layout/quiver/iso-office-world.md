---
id: blocks/layout/quiver/iso-office-world
type: block
name: 等距像素办公室
description: 菱形地板 + 体素家具 + 7 房间分区配色 + 暖冷天花灯 + 可点房间标签的等距场景容器
platforms: [web]
theme: dark
tags:
  aesthetic: [pixel, retro]
  mood: [playful, nostalgic]
  stack: [vanilla-css]
uses:
  - tokens/palettes/quiver/night-studio
  - tokens/motion/quiver/pixel-steps
  - tokens/layout/quiver/iso-grid
  - components/avatars-icons/quiver/pixel-worker-sprite
preview: /preview/blocks/layout/quiver/iso-office-world
---

# 等距像素办公室

> 一间俯视的像素办公室：地板铺满菱形瓦片、家具是体素、房间用配色 + 灯光分区、小人在工位敲键——整个产品的「世界」

## 视觉特征

- **13×9 网格舞台**，`buildScene()` 一次性把瓦片/墙/家具/灯光/猫/浮尘拼成一棵 `SceneNode[]`，由 Office 组件无脑 map 成绝对定位 div
- **7 个房间，各有专属地板 tint + 墙色**（房间靠配色分区，不靠隔墙）：
  - 休息室 `lounge`（c0-3）紫 `rgba(120,90,140,.16)` · 工位区 `work`（c5-9）蓝 `rgba(90,120,170,.13)` · 质检台 `verify`（c11-13,r0-1）青 `rgba(80,150,130,.16)` · 领导区 `dispatch`（r2-3）金 `rgba(200,160,90,.13)` · ＋可扩展 `build`（r4-5）透明 · 运维·预算 `ops`（r6-7）暖棕 · 发货口 `ship`（r8-9）灰蓝
  - 走廊列 `[4, 10]` 用 `HALL_TINT rgba(255,255,255,.045)` 提亮
- **暖冷灯光分区**（`ceilLamp` 径向光斑，不用 filter:blur）：休息室/运维/经理 暖 `rgba(255,200,150,.5)`，工位/质检 冷 `rgba(150,190,255,.46)` / 青 `rgba(150,230,200,.46)`——「干活区冷、休息区暖」的体感分区
- **12 个工位** 3×4 矩阵（列 `[5,7,9]` × 行 `[1,3,5,7]`），最多 5 个员工 `EMP_COUNT` 同时敲键；经理在领导区 `(11.5, 3.3)`、审计在质检台 `(11.2, 0.95)`
- **家具是体素三面体**：工位（冷紫椅 `#4a3a5a` + 木桌 + `#2a3a55` 屏幕 + 扫描线 + 键盘灯）、服务器机架（8 层抽屉 + 三色 LED 循环 `#6cc47a/#ffd27a/#5ce0ff`）、白板、台灯、绿植（三层叶冠 + 摇曳）、饮水机、看板、记忆书、发货卷帘门、货箱堆、蜷着的猫
- **落地窗月光 + 体积光束**：玻璃 `rgba(143,208,255,.20)`、月亮 `#ffe6ad` 带光晕、godray 斜射呼吸
- **房间标签 = 可点入口**：屏幕空间浮层（相机 project 定位，1:1 不糊），点「楼」开对应面板（运维→设置、领导→经理台、质检→追溯、发货→晨报…）；运维楼标签实时拼今夜花费 `· 今夜 $x.xx`
- **滚轮缩放 + 点小人下钻**：相机 `fit ~ fit×10`，点小人弹工人详情卡

## 核心代码

```tsx
const scene = useMemo(() => buildScene(), []);   // SceneNode[] + roomLabels
<div className="world" style={camera.worldStyle}>
  {scene.nodes.map(n => <div key={n.key} className={n.className} style={n.style}>{children(n)}</div>)}
  {workers.map(w => <Worker key={w.id} worker={w} onDive={dive} />)}
</div>
// 房间标签走屏幕空间浮层，相机 project → 1:1 清晰
{scene.roomLabels.map(l => <div className="roomlabel clickable" style={camera.project(l.wx, l.wy)} />)}
```

## 适配指南

- 新房间 = 在 rooms.ts 加一段网格范围 + tint + 墙色 + 标签；新家具 = 写一个 `furnishXxx()` 用 SceneBuilder 原语拼体素
- 分区**靠地板 tint + 灯光冷暖**，不靠实体隔墙——保持开阔俯视感
- 标签/人名/气泡一律走屏幕空间浮层，永不画进 world

## 反模式

- 不要把房间用满边框/隔断围死——Quiver 的通透感来自「同一片地板、配色分区」
- 不要给每件家具的灯各挂 CSS 无限动画——用 LED flicker hook 低频随机驱动
- 不要用 canvas/引擎重写——纯 DOM 体素可直接 CSS 调试、随相机重栅格化更清晰
