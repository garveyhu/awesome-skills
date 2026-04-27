---
id: blocks/nav/sage/revolver-menu-fab
type: block
name: 雪人飘雪左轮菜单
description: 圆形浮动菜单（内环 4 + 外环最多 12）+ 雪人化身 + 飘雪 + 旋转地球，sage 最独特的"彩蛋型"全局导航
platforms: [web]
theme: light
tags:
  aesthetic: [skeuomorph, retro]
  mood: [playful, dreamy]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/sage/twelve-theme-spectrum
  - tokens/motion/sage/styled-keyframes
preview: /preview/blocks/nav/sage/revolver-menu-fab
---

# Revolver Menu FAB

> sage 屏幕右下角的 64×64 圆形浮动按钮（FAB）。常态闭合显地球图标；点开后菜单项以 30° 步长沿圆环展开（内环 ≤4 项 140px 半径，外环最多 8 项 200px 半径）；钉住（pin）后地球开始 8s 自转 + 整个 FAB 雪花飘落。**Pin + drag 的可玩性**：可以把雪人帽子拖出来再戴回去。

## 视觉特征 / 关键结构

- 主按钮 `MainButton`：`width: 64px; height: 64px; border-radius: 50%; background: ${$isOpen ? color : transparent}; box-shadow: 0 4px 15px rgba(0,0,0,0.2)`
- 三层 hover 反馈：`bling 1s` 缩放 / `wobble 0.6s` 雪人摇摆 / box-shadow `0 0 15px ${color}` 发光
- pinned 态：`scale(1.1) + box-shadow 0 0 20px ${color}, 0 0 40px rgba(255,255,255,0.2) + opacity 1`
- 雪人 SnowmanIcon：head 19×19 白圆 + body 30×30 白圆 + scarf 22×6 主题色 + 2 黑眼 + 橘鼻 + 2 黑扣子
- SnowmanHat：20×14 主题色矩形 + 5px 白檐 + 8×8 主题色顶球 + custom SVG hand cursor 拖拽
- ScrollArea 360×360 圆形透明感应区
- PulseRing 100% → 200% scale + opacity 0.5 → 0 · 1.5s ease-out
- MenuItemContainer transform：`rotate(${30*i + rotation}deg) translateX(-${ring === 'outer' ? 200 : 140}px) rotate(${-(30*i + rotation)}deg) scale(1)` —— 反向旋转保证图标朝上
- 项展开延迟：`transition-delay: ${i * 0.03}s` —— 错落入场
- MenuItemButton hover：`bg: rgba(255,255,255,0.95) → bg: white + color: ${$color} + scale(1.15) + box-shadow: 0 0 20px ${color}40 + border-color: ${color}`
- OrbitRing 默认 hidden，hover 显 `border: 1px dashed ${color}40 + earthSpin 3s linear infinite` 转动
- 每个 MenuItemButton 右侧 60px Tooltip `bg: rgba(15,23,42,0.9) backdrop-blur-4 + slide-in`

## 适配指南

- 整个组件依赖 styled-components keyframes（`tokens/motion/sage/styled-keyframes`），不能纯 Tailwind 复刻
- 项数 ≤4 走内环，>4 多余走外环；超过 12 项的需求请用 CommandPalette 而不是 RevolverMenu
- pinned 态下雪花是 30 个随机参数 Snowflake instance，每个 delay/left/size/duration/opacity 都不同
- 主题色注入靠 `$color` prop，不能放 className——keyframes 内部插值需要 styled-components

## 反模式

- ❌ 替换为常规 dropdown menu —— 失去 sage 的彩蛋性格
- ❌ 在生产严肃后台开雪花 —— 这个组件本来就是"打开就是冬天玩具"，建议在登录前 / 首次引导 / pinned 时才触发雪花
- ❌ 加更多动画类型（春天花、夏天蝉……）—— 规则说"4 个 keyframes 一组"，多了破坏节奏
