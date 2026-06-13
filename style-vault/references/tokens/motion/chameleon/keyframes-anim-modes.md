---
id: tokens/motion/chameleon/keyframes-anim-modes
type: token
name: Chameleon 动效套件 + 三档动画模式
description: accordion + modal fade + ping-soft + shimmer + float-soft + halo-pulse + decor-drift ×3 + cmdk 样式 + :root[data-anim] 三档全局过渡时长切换
platforms:
- web
theme: light
tags:
  aesthetic:
  - industrial
  - minimal
  mood:
  - calm
  stack:
  - shadcn-radix
uses: []
preview: /preview/tokens/motion/chameleon/keyframes-anim-modes
---

# Chameleon Keyframes + Anim Modes

> Chameleon 全站自定义 CSS 动画的总集（与 waveflow 同源分叉）：手风琴展开、Radix Dialog **纯 opacity** fade、状态点呼吸、暖灰 shimmer 骨架、空态图标漂浮 + 辉光呼吸、登录浮件 drift ×3、顶部进度带，外加 cmdk 命令面板专属样式；再叠一层 `:root[data-anim]` 三档（disabled / agile / smooth）全局过渡时长切换。

## Tokens

```json
{
  "accordion-down": {
    "var": "--animate-accordion-down: accordion-down 0.2s ease-out",
    "css": "from { height: 0 } to { height: var(--radix-accordion-content-height) }"
  },
  "accordion-up": {
    "var": "--animate-accordion-up: accordion-up 0.2s ease-out",
    "css": "from { height: var(--radix-accordion-content-height) } to { height: 0 }"
  },
  "modal-overlay": {
    "in": ".modal-overlay[data-state=open] → modal-overlay-in 150ms ease-out (opacity 0→1)",
    "out": ".modal-overlay[data-state=closed] → modal-overlay-out 120ms ease-in (opacity 1→0)"
  },
  "modal-content": {
    "in": ".modal-content[data-state=open] → modal-content-in 150ms cubic-bezier(0.16,1,0.3,1) (opacity 0→1，无 translate)",
    "out": ".modal-content[data-state=closed] → modal-content-out 120ms ease-in (opacity 1→0)",
    "why": "刻意只动 opacity，定位走 className 的 fixed left-1/2 top-1/2 + -translate-x-1/2 -translate-y-1/2，避免 keyframe translate 与 Tailwind transform 组合冲突的浮动感"
  },
  "ping-soft": {
    "duration": ".pulse-soft → ping-soft 2s ease-in-out infinite",
    "css": "0,100% { opacity: 1 } 50% { opacity: 0.6 }"
  },
  "shimmer": {
    "duration": ".skeleton → shimmer 1.6s ease-in-out infinite",
    "css": "0% { background-position: -200px 0 } 100% { background-position: 200px 0 }",
    "bg": "linear-gradient(90deg, #ebe9e3 0%, #f5f4ee 50%, #ebe9e3 100%); background-size: 400px 100%"
  },
  "float-soft": {
    "duration": ".anim-float → float-soft 3.4s ease-in-out infinite",
    "css": "0,100% { transform: translateY(0) } 50% { transform: translateY(-7px) }",
    "用法": "长留页面的空态图标漂浮"
  },
  "halo-pulse": {
    "duration": ".anim-halo → halo-pulse 3s ease-in-out infinite",
    "css": "0,100% { transform: scale(1); opacity: 0.6 } 50% { transform: scale(1.12); opacity: 1 }",
    "用法": "空态图标背后辉光呼吸"
  },
  "global-progress": {
    "css": "0% { transform: translateX(-100%) } 100% { transform: translateX(100%) }",
    "用法": "翻页 / 改筛选时顶部 indeterminate 进度带"
  },
  "decor-drift-1": {
    "css": "0,100% { translate: 0 0 } 50% { translate: 0 -12px }"
  },
  "decor-drift-2": {
    "css": "0,100% { translate: 0 0; rotate: 0deg } 50% { translate: 0 -8px; rotate: 8deg }"
  },
  "decor-drift-3": {
    "css": "0,100% { translate: 0 0; rotate: 45deg } 50% { translate: 0 -14px; rotate: 50deg }",
    "用法": "登录左侧几何浮件，用 CSS L4 独立 translate/rotate 属性避开 JS transform 冲突"
  },
  "cmdk": {
    "group-heading": "padding 6px 10px 4px; font-size 10.5px; weight 600; uppercase; letter-spacing 0.04em; color rgb(120 113 108)",
    "item": "display flex; gap 10px; padding 7px 10px; radius 6px; font-size 12.5px; transition background 0.12s",
    "item-selected": "[data-selected=true] → bg rgb(239 246 255); color rgb(29 78 216)",
    "item-hover": ":hover → bg rgb(245 244 238)"
  },
  "anim-modes": {
    "disabled": ":root[data-anim=disabled] * / *::before / *::after { transition-duration: 0ms !important; animation-duration: 0ms !important; animation-iteration-count: 1 !important }",
    "agile": ":root[data-anim=agile] * { transition-duration: 80ms !important }；:hover/:focus { transition-duration: 100ms !important }",
    "smooth": "默认态，不写覆盖"
  }
}
```

## 视觉特征

- **modal fade 刻意只动 opacity**：overlay `modal-overlay-in 150ms ease-out` / `out 120ms ease-in`；content `modal-content-in 150ms cubic-bezier(0.16,1,0.3,1)` / `out 120ms ease-in`——keyframe 不带 translate，定位完全交给 className 的 `fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2`，否则会出现"先左上、再滑到中间"的浮动感
- **shimmer 改 background-position**：暖灰渐变 `#ebe9e3 → #f5f4ee 50% → #ebe9e3`、`background-size: 400px 100%`、`1.6s ease-in-out`，不是改 opacity
- **空态双件套 float + halo**：`.anim-float` 图标上下 ±7px 漂（3.4s），`.anim-halo` 背后辉光 scale 1→1.12 + opacity 0.6→1 呼吸（3s），同图一起用造出"图标浮在光晕上"的空态氛围
- **ping-soft 比 animate-pulse 慢**：2s ease-in-out（默认 1s），更安静的状态点呼吸
- **三档 anim 全局覆盖**：`disabled` 把所有 transition/animation 时长清 0、迭代次数压到 1（无障碍/性能/调试）；`agile` 全局过渡缩到 80ms、hover/focus 100ms（约 ½）；`smooth` 是默认态不写任何覆盖
- **cmdk 命令面板**：分组标题 10.5px / 600 / uppercase / `letter-spacing 0.04em`、stone-500 灰；item 7px 10px / radius 6px / 12.5px、gap 10px，选中底 blue-50 文字 blue-700，hover 底 warm-2

## 适配指南

- 自定义 keyframe 触发：空态用 `className="anim-float"` / `anim-halo`；骨架加 `.skeleton`；状态点 `.pulse-soft`
- Radix Dialog 套：overlay 加 `.modal-overlay`、content 加 `.modal-content`，靠 `data-state` 自动 in/out
- 全局动画档由 JS 写 `document.documentElement.dataset.anim = 'agile' | 'disabled'`（smooth 留空），与 8×4 主题切换同源，构成用户偏好可切换体系
- Tailwind v4 注入：`@theme { --animate-accordion-down: accordion-down 0.2s ease-out }`

## 反模式

- ❌ 给 modal content keyframe 加 translate——与 Tailwind transform 组合产生浮动感
- ❌ shimmer 改用 `animate-pulse`（改 opacity）——丢掉暖灰渐变流过的高级感
- ❌ 给 admin 主体加 decor-drift——这是登录专属语言
- ❌ 把 float/halo 用到非空态的常驻 UI——长时间漂浮会分神

## 与 waveflow/keyframes-suite 区分

同源分叉，但视觉语言与覆盖范围不同——AI 选用时按下表对齐：

| 维度 | waveflow/keyframes-suite | chameleon/keyframes-anim-modes |
|------|--------------------------|--------------------------------|
| **共有** | accordion-down/up · decor-drift-1/2/3 · ping-soft · global-progress · shimmer | 全保留（drift 数值同：-12/-8+8deg/-14+45→50deg；ping 同；shimmer 同暖灰渐变） |
| **modal 动画** | 无（Radix 走 Tailwind `animate-pulse` + data-state） | 新增 `.modal-overlay` / `.modal-content` 纯 opacity fade（去 translate 防浮动），150ms in / 120ms out |
| **空态 flair** | 无 | 新增 `.anim-float`（±7px 漂 3.4s）+ `.anim-halo`（scale 1.12 辉光呼吸 3s） |
| **启动 loading** | 有 `boot-dot`（三点 ·· ·· ·） | **删除**，无 boot-dot |
| **cmdk 命令面板** | 无 | 新增整套 `[cmdk-group-heading]` / `.cmdk-item` 样式 |
| **全局动画档** | 无 | 新增 `:root[data-anim]` 三档（disabled / agile 80ms / smooth），全局 `transition-duration !important` 覆盖 |
| **气质** | 单纯暖工业动效集 | 暖工业 + 用户偏好可切换体系（与 8×4 主题切换同源） |

需要"纯净 waveflow 暖工业动效集 + 启动三点"→ 选 waveflow；需要"带 modal fade、空态漂浮辉光、命令面板、三档动画速度可切"→ 选 chameleon。
