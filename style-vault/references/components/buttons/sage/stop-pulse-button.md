---
id: components/buttons/sage/stop-pulse-button
type: component
name: 停止生成脉冲按钮
description: 三层 ping/pulse + 渐变 sheen + 白色内嵌方块，告诉用户"AI 正在跑，按这里中止"
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/sage/twelve-theme-spectrum
  - tokens/motion/sage/animate-in-suite
preview: /preview/components/buttons/sage/stop-pulse-button
---

# Stop Pulse Button

> Chat 流式响应中，发送按钮原位变成"停止"——三层主题色波纹（外发光 blur + 中环 ping + 主体 bg）+ 顶部白色斜向 sheen + 中心 2.5×2.5 白色方块。这是 sage 整站最复杂的按钮，承担"AI 在思考"的视觉锚点。

## 视觉特征

- **外发光**：`absolute -inset-2.5 rounded-full ${themeClasses.bg} opacity-30 blur-lg animate-pulse`
- **中环 ping**：`absolute inset-0 rounded-full ${themeClasses.bg} opacity-20 animate-ping` + `animationDuration: 2s`
- **主体**：`relative z-10 w-8 h-8 rounded-full ${themeClasses.bg} text-white shadow-md group-hover:shadow-lg group-hover:scale-105 group-active:scale-95 border border-white/30 ring-1 ring-white/10 backdrop-blur-md`
- **白色斜向 sheen**：`absolute inset-x-0 -top-[60%] h-[120%] bg-gradient-to-b from-white/40 via-white/5 to-transparent transform -skew-y-12`
- **中心方块**：`relative z-10 w-2.5 h-2.5 bg-white rounded-[1.5px] shadow-sm group-hover:scale-90 transition-transform duration-200`

## 核心代码

```tsx
<Tooltip title="Stop generating">
  <button
    type="button"
    onClick={onStop}
    className="group relative flex items-center justify-center w-8 h-8 outline-none transform transition-transform"
  >
    <span className={`absolute -inset-2.5 rounded-full ${tc.bg} opacity-30 blur-lg animate-pulse`} />
    <span
      className={`absolute inset-0 rounded-full ${tc.bg} opacity-20 animate-ping`}
      style={{ animationDuration: '2s' }}
    />
    <div
      className={`relative z-10 flex items-center justify-center w-8 h-8 rounded-full ${tc.bg} text-white shadow-md transition-all duration-300 ease-out group-hover:shadow-lg group-hover:scale-105 group-active:scale-95 border border-white/30 ring-1 ring-white/10 backdrop-blur-md overflow-hidden`}
    >
      <div className="absolute inset-x-0 -top-[60%] h-[120%] bg-gradient-to-b from-white/40 via-white/5 to-transparent transform -skew-y-12 pointer-events-none" />
      <div className="relative z-10 w-2.5 h-2.5 bg-white rounded-[1.5px] shadow-sm group-hover:scale-90 transition-transform duration-200" />
    </div>
  </button>
</Tooltip>
```

## 适配指南

- 仅在 `isLoading=true` 期间替换 send 按钮
- 用 `${themeClasses.bg}` 让按钮继承用户主题——红色用户得到红色脉冲，cyan 用户得到 cyan 脉冲
- ping 的 `animationDuration: '2s'` 是手设的（默认是 1s），让节奏更平稳

## 反模式

- ❌ 简化成单层 animate-pulse —— 只有三层叠加才有"AI 在思考"的存在感
- ❌ 用 red 强制色 —— 用户会误以为是错误状态，sage 用主题色暗示"一切都正常，你想停就停"
