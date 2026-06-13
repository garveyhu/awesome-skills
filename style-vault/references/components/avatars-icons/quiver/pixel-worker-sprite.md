---
id: components/avatars-icons/quiver/pixel-worker-sprite
type: component
name: 像素工人精灵
description: 24×40 纯 CSS 手搓像素小人，连帽衫三阶明暗由 CSS 变量驱动，经理 / 审计 / 员工角色变体
platforms: [web]
theme: dark
tags:
  aesthetic: [pixel, retro]
  mood: [playful, nostalgic]
  stack: [vanilla-css]
uses:
  - tokens/palettes/quiver/night-studio
  - tokens/motion/quiver/pixel-steps
preview: /preview/components/avatars-icons/quiver/pixel-worker-sprite
---

# 像素工人精灵

> 一个 `24×40` 的小人，全部部件用绝对定位的 `<div>` + CSS 渐变堆出来——零图片资源、配色由 CSS 变量驱动

## 视觉特征

- **尺寸 `24×40`**，`margin-left: -12px; margin-top: -34px` 锚到脚底中心，`image-rendering: pixelated`
- **部件全是叠出来的小方块**（自下而上）：`legs 14×7` → `torso 20×15` → `face 10×7` → `hair 14×7` → `hood 18×12` → 眼 `2×2`
- **连帽衫/上衣三阶明暗 = 一条横向 3 段渐变**：`background: linear-gradient(90deg, var(--hoodL) 0 4px, var(--hood) 4px 14px, var(--hoodD) 14px 18px)`；亮/暗面由 `shade(base, ±)` 派生（hoodL +26、hoodD −34、torsoL +24、torsoD −30）
- **6 套员工配色对**（hood / torso）：`#5a86c0/#3f5f8f`(冷蓝) · `#a566a8/#7a3f7a`(紫罗兰) · `#46a0a0/#2f7070`(青绿) · `#6a6ad0/#43439a`(靛蓝) · `#c07888/#945565`(玫瑰) · `#5a8ab0/#3f6a8a`(钢蓝)
- **角色变体走 class**：
  - `.worker.mgr`（经理）：金棕配 `#e0a050/#b07a30`，加王冠 `crown` + 披风 `mantle` + 长袍 `robe`，发光金书 `book`（`box-shadow: 0 0 6px 2px rgba(255,200,90,.6)`），`margin-top: -40px` 略高
  - `.worker.aud`（审计）：青绿配，加护目镜 `visor #1e3a3a` + 写字板 `clip`
  - `.worker.emp`：加耳机 `phones`
- **状态 class 接动画**（见 pixel-steps）：`.working`(敲键 typebob)、`.moving`(走路 walkbob)、`.awaiting`(头顶思考点 thinkpulse)、`.lean`(前倾露手臂)、`.talk`(说话气泡)、`.sip/.stretch`(摸鱼)、`.cel`(庆祝 +100 XP 上浮)
- **落地接触影** `.shadow 18×6 rgba(0,0,0,.36)`，移动时 `shadowpace` 缩放
- **像素名牌气泡**：`#f4f6fb` 底 + 小三角，经理 `#fff2d6`、审计 `#d8f0e8`、思考 `#fff6e0`（屏幕空间浮层渲染，不进 world）

## 核心代码

```tsx
// 部件树：所有块绝对定位叠在 .body > .stack 里
<div className={`worker ${role} ${working && 'working'} ${awaiting && 'awaiting'}`}
     style={{ '--hood': hood, '--hoodL': shade(hood, 26), '--hoodD': shade(hood, -34),
              '--torso': torso, '--torsoL': shade(torso, 24), '--torsoD': shade(torso, -30) }}>
  <div className="shadow" /><div className="body"><div className="stack">
    <div className="hair" /><div className="hood" /><div className="phones"><i /></div>
    <div className="visor" /><div className="face" /><div className="eye" />
    <div className="torso" /><div className="arms" /><div className="legs" />
    {role === 'mgr' && <><div className="crown" /><div className="mantle" /><div className="robe" /></>}
  </div></div>
</div>
```

## 适配指南

- 换肤只改 `--hood` / `--torso` 两个变量，三阶明暗自动派生——别手填亮暗面
- 角色身份靠「加部件」而非「换整套 sprite」：经理=戴王冠加袍，审计=戴护目镜拿板，员工=戴耳机
- 动作用状态 class 切，不重画——所有动画 keyframes 已在 motion token 备好

## 反模式

- 不要用 png/精灵图替换——CSS div 堆叠的好处是可变色、可调试、零资源；换图就失去这套换肤能力
- 不要给小人补间平滑动画——用 `steps()`，保持像素跳帧手感
- 不要把名牌/气泡画进等距 world——会被相机缩放糊掉，必须走屏幕空间浮层
