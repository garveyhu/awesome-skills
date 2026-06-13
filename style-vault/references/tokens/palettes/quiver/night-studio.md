---
id: tokens/palettes/quiver/night-studio
type: token
name: 夜色工作室
description: 深夜蓝径向舞台 + 冷文字三阶 + 单一琥珀台灯暖强调 + 玻璃表面，治愈像素办公室的夜间基底
platforms: [web]
theme: dark
tags:
  aesthetic: [pixel, glass]
  mood: [calm, dreamy]
  stack: [vanilla-css]
preview: /preview/tokens/palettes/quiver/night-studio
---

# 夜色工作室

> 深夜蓝径向舞台 + 冷文字三阶 + 一个琥珀暖强调，整夜不眠的像素工作室基底

## 视觉特征

- **舞台是一束径向光，不是平涂底**：`radial-gradient(130% 100% at 50% 32%, #1b2440 0%, #10162b 62%, #0a0e1a 100%)`——画面中上方一团微亮，四周沉入近黑 `#0a0e1a`，像聚光灯打在夜里的桌面上
- **冷文字三阶**：`#eef2fb`（主）/ `#aab4cd`（次）/ `#76819c`（弱），全部偏冷蓝灰，给暖强调让路
- **唯一暖强调 = 琥珀 `#ffd27a`**：台灯、王冠、选中条、聚焦环都用它——整个深冷画面里**只有这一处暖**，是「温度锚点」。dim 态 `rgba(255,210,122,.14)`
- **4 色语义状态**：`ok #7bc47e` / `warn #f0b24a` / `bad #e2604f` / `info #8fd0ff`，各带 ~.13 alpha 的 soft 底
- **玻璃表面三档**：`s-0 rgba(11,15,26,.72)` / `s-1 rgba(18,24,42,.82)` / `s-2 rgba(22,29,50,.94)`，配 `backdrop-filter: blur(13px) saturate(1.25)`；内陷 `s-inset rgba(8,11,20,.55)`
- **发丝边框靠白色低 alpha 叠**：`bd .09` / `bd-soft .06` / `bd-strong .14` + 顶部高光 `hairline-top rgba(255,255,255,.10)`——不用实色描边
- **「出发绿」派生强调**：主行动按钮用青柠渐变 `#a6eaa6 → #6cc47a`（深墨字 `#0e1a10`），和琥珀分工：琥珀=氛围/选中，绿=行动/成功

## Tokens

```json
{
  "bg": {
    "deep": "#0a0e1a",
    "stage-gradient": "radial-gradient(130% 100% at 50% 32%, #1b2440 0%, #10162b 62%, #0a0e1a 100%)"
  },
  "text": {
    "1": "#eef2fb",
    "2": "#aab4cd",
    "3": "#76819c"
  },
  "accent": {
    "amber": "#ffd27a",
    "amber-dim": "rgba(255,210,122,.14)",
    "go-lime-from": "#a6eaa6",
    "go-lime-to": "#6cc47a",
    "go-ink": "#0e1a10"
  },
  "state": {
    "ok": "#7bc47e", "ok-soft": "rgba(123,196,126,.13)",
    "warn": "#f0b24a", "warn-soft": "rgba(240,178,74,.14)",
    "bad": "#e2604f", "bad-soft": "rgba(226,96,79,.13)",
    "info": "#8fd0ff"
  },
  "surface": {
    "s-0": "rgba(11,15,26,.72)",
    "s-1": "rgba(18,24,42,.82)",
    "s-2": "rgba(22,29,50,.94)",
    "s-inset": "rgba(8,11,20,.55)",
    "tint-hi": "rgba(255,255,255,.05)"
  },
  "border": {
    "bd": "rgba(255,255,255,.09)",
    "bd-soft": "rgba(255,255,255,.06)",
    "bd-strong": "rgba(255,255,255,.14)",
    "hairline-top": "rgba(255,255,255,.10)"
  },
  "radius": { "r-1": "8px", "r-2": "11px", "r-3": "14px", "r-pill": "999px" },
  "shadow": {
    "sh-1": "0 1px 2px rgba(0,0,0,.3), 0 4px 16px rgba(0,0,0,.28)",
    "sh-2": "0 2px 8px rgba(0,0,0,.34), 0 16px 48px rgba(0,0,0,.42)",
    "sh-3": "0 8px 24px rgba(0,0,0,.46), 0 32px 96px rgba(0,0,0,.52)"
  },
  "blur": { "blur": "blur(13px) saturate(1.25)", "blur-sm": "blur(8px) saturate(1.2)" }
}
```

## 适配指南

- 纯 CSS 项目直接把上面落进 `:root` CSS 变量（Quiver 原样如此）；React + Tailwind 项目落到 `theme.extend.colors`
- **径向舞台底不能换平涂**——少了那束中上方的光，整个「夜里一盏灯」的气质就塌成普通暗色后台
- **暖强调只留一处**：琥珀用于氛围/选中/聚焦，行动/成功交给「出发绿」；不要再引第三种暖色

## 与 deep-space-amber / hud-cyan-glass 区分

vault 里已有两套深蓝黑 + 状态色的冷调色板，**气质完全相反，别混用**：

- **mission-ops/deep-space-amber**（深空琥珀）：NASA MOCR / Bloomberg 终端，**严肃、冷峻、信息密集**，底色是 4 层平涂递进、靠工程网格线找秩序，琥珀是「告警色」。
- **tactical-hud/hud-cyan-glass**（HUD 青光玻璃）：贾维斯 / 战术屏，主色是 **HUD 青蓝**，玻璃卡片悬浮在深空蓝上，气质是科幻战术。
- **本条 night-studio**：是**温暖、治愈、俏皮**的像素游戏世界——径向舞台是「台灯光」不是「控制屏」，琥珀是**炉火/灯光的温度**不是告警，整体服务于「一间整夜亮着灯的小办公室」而非「工程控制台」。选它当你要的是 cozy 夜间游戏感，不是 terminal 严肃感。

## 反模式

- 不要把琥珀 `#ffd27a` 泛用成大面积底色——它是点睛的「唯一暖」，铺开就廉价
- 不要给玻璃表面加实色描边——边界靠白色低 alpha 发丝线 + 顶部高光
- 不要把状态 `bad` 红提到主文本明度——语义色不抢中性文本的位
