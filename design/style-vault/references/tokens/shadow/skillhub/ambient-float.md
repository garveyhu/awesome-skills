---
id: tokens/shadow/skillhub/ambient-float
type: token
name: 环境悬浮阴影
description: 超轻环境阴影（≤0.04 透明度）+ hover:shadow-md 浮起 + 脉冲辉光
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses: []
preview: /preview/tokens/shadow/skillhub/ambient-float
---

# Ambient Float

> 阴影哲学：默认状态几乎看不出阴影（0.04 透明度级别），hover 才给一档可见的 md，避免卡片静态就"漂浮"

## Tokens

### 静态层

```css
--shadow-ambient:   0 1px 4px rgba(0, 0, 0, 0.04);   /* navbar pill 等永远在场的容器 */
--shadow-glass:     0 1px 3px rgba(0, 0, 0, 0.04);   /* 玻璃层底色 */
--shadow-card:      none;                             /* 卡片静态无阴影，只靠 border-gray-200 */
```

### 交互层

```css
--shadow-card-hover: var(--tw-shadow-md);  /* Tailwind 默认 md */
--shadow-active:     var(--tw-shadow-md);  /* 选中分页、Tab active */
--shadow-float:      var(--tw-shadow-lg);  /* Popover / Dropdown 面板 */
```

### 辉光（点状）

```css
/* 状态脉冲（emerald "systems operational" 脉冲点）*/
--shadow-pulse-ok:    0 0 8px rgba(16, 185, 129, 0.8);
/* 头像 / tag 的底色辉光 */
--shadow-pulse-teal:  0 0 8px rgba(20, 184, 166, 0.3);
```

### 命名要点

- `ambient`：只是"存在感"阴影，不做层级暗示
- `float`：明确"浮起"层级
- `pulse`：动态辉光，配合 `animate-pulse` 用

## 使用示例

```tsx
// Navbar pill（永远在 header 里，静态就可见但极轻）
<div className="shadow-[0_1px_4px_rgba(0,0,0,0.04)] border border-gray-100 bg-white rounded-2xl">
  ...
</div>

// Skill 卡（静态无阴影，hover 才浮起）
<div className="border border-gray-200 bg-white rounded-2xl
                hover:shadow-md hover:border-teal-200 transition-all">
  ...
</div>

// 分页 active
<button className="bg-teal-600 text-white shadow-md rounded-xl">3</button>

// Systems Operational 小点
<div className="w-1.5 h-1.5 rounded-full bg-emerald-500
                shadow-[0_0_8px_rgba(16,185,129,0.8)] animate-pulse" />
```

## 适配指南

- 静态 `0 1px 4px rgba(0,0,0,0.04)` 比 Tailwind 默认 shadow-sm 还轻，肉眼几乎察觉不到，但在无 border 的白底里能"悄悄把边界分出来"
- 所有卡片默认 `shadow-none`（靠 border-gray-200），只在 hover 才升 `shadow-md`——这是阴影的唯一层级跳跃
- 辉光（`shadow-[0_0_8px_...]`）只能套最多 8px blur、最多一个色——再大就变成 glow-card，偏题
- 从 Antd 组件进来的 shadow（Dropdown / Popover）默认 lg 级，调成 md 级保持整体层级压缩

## 反模式

- 不要给卡片默认就加 shadow-sm 以上的阴影——阴影泛滥是减分项
- 不要用色阴影（colored shadow，如 teal-500/30）做卡片层级——只留给 pulse 辉光
- 不要超过 2 档阴影（静态 ambient + 交互 md）；如果你在想 shadow-lg 做什么，大概率你需要 border 或 backdrop-blur 而不是更深的阴影
