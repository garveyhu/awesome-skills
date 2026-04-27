---
id: components/indicators/skillhub/pulse-dot
type: component
name: 脉冲状态点
description: 6-8px 圆点 + 颜色辉光 + animate-pulse 的状态指示器
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/skillhub/skillhub-teal-mist
  - tokens/shadow/skillhub/ambient-float
preview: /preview/components/indicators/skillhub/pulse-dot
---

# Pulse Dot

> 小尺寸圆点（6-8px）+ 同色 8px blur 辉光 + CSS `animate-pulse`。用于 "All Systems Operational" / 在线 / 未读标记 / 录制中 等非干扰性状态提示。

## 视觉特征

- 尺寸：`w-1.5 h-1.5`（6px · 极小）/ `w-2 h-2`（8px · 标准）
- 形状：`rounded-full`
- 辉光：`shadow-[0_0_8px_rgba(<color>,0.8)]`
- 动画：`animate-pulse`（Tailwind 内置，1s 50% opacity 脉冲）
- 变体色：emerald（正常）· orange（通知）· rose（故障）· teal（在线）

## 核心代码

```tsx
type PulseColor = 'emerald' | 'orange' | 'rose' | 'teal';

const colorMap: Record<PulseColor, { bg: string; glow: string }> = {
  emerald: { bg: 'bg-emerald-500', glow: '0 0 8px rgba(16,185,129,0.8)' },
  orange:  { bg: 'bg-orange-500',  glow: '0 0 8px rgba(249,115,22,0.8)' },
  rose:    { bg: 'bg-rose-500',    glow: '0 0 8px rgba(244,63,94,0.8)' },
  teal:    { bg: 'bg-teal-500',    glow: '0 0 8px rgba(20,184,166,0.8)' },
};

interface PulseDotProps {
  color?: PulseColor;
  size?: 6 | 8;
  label?: string;           // 同行标签
  labelClassName?: string;
  animated?: boolean;
}

export const PulseDot = ({
  color = 'emerald',
  size = 6,
  label,
  labelClassName = 'text-xs font-medium text-slate-400',
  animated = true,
}: PulseDotProps) => {
  const c = colorMap[color];
  const dim = size === 8 ? 'w-2 h-2' : 'w-1.5 h-1.5';
  return (
    <div className="inline-flex items-center gap-1.5">
      <span
        className={`${dim} rounded-full ${c.bg} ${animated ? 'animate-pulse' : ''}`}
        style={{ boxShadow: c.glow }}
      />
      {label && <span className={labelClassName}>{label}</span>}
    </div>
  );
};
```

## 使用示例

```tsx
// Footer 系统正常
<PulseDot color="emerald" label="All Systems Operational" />

// Nav 未读消息小点（不带 label）
<span className="relative">
  <MessageSquare size={15} />
  {hasUnread && (
    <span className="absolute -top-1 -right-1 w-1.5 h-1.5 rounded-full bg-orange-500" />
  )}
</span>

// 录制中 / LIVE
<PulseDot color="rose" size={8} label="LIVE" labelClassName="text-xs font-bold text-rose-600" />
```

## 适配指南

- 尺寸只有 6px / 8px 两档——再大就变成徽标，该用别的组件（Tag / Badge）
- animated 默认 true，但用在大量重复位置（如列表每行都有状态点）可以关——避免同屏闪烁
- 辉光的 blur 固定 8px，再大会像"光晕特效"，再小又没辨识度
- 作为"未读红点"放在 icon 角上时用 `absolute -top-1 -right-1`，不要用 PulseDot 组件本身（它是行内版）

## 反模式

- 不要用 `bg-red-500` 替代 rose——red 偏刺眼，rose 更柔与主色系对齐
- 不要给 dot 加 border——同色圈+辉光已经够视觉分层
- 不要静止 dot 配 glow——没动时的 glow 看起来像没点亮的 LED，矛盾；静态用纯 `bg-emerald-500` 就够
