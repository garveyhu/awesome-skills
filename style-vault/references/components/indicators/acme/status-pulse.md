---
id: components/indicators/acme/status-pulse
type: component
name: 状态脉冲指示
description: 8px 状态点四态（healthy 带 pulse 光晕 / degraded / critical / idle）
platforms: [web]
theme: dark
tags:
  aesthetic: [minimal, industrial]
  mood: [cold, serious]
  stack: [react-antd-tailwind, html-tailwind]
uses:
  - tokens/palettes/acme/slate-cyan-ice
  - tokens/motion/acme/instant-snap
preview: /preview/components/indicators/acme/status-pulse
---

# Status Pulse

> 服务状态指示器：8px dot 四态色 + healthy 态独有的呼吸光晕。

## 视觉特征

- 直径 8px 实心圆 dot；6px 紧凑变体可选（行高 ≤ 28px 的密集表格用）
- 四态色：
  - `healthy` `#10b981` emerald-500 + 呼吸光晕（box-shadow keyframe）
  - `degraded` `#f59e0b` amber-500，**静态**
  - `critical` `#ef4444` rose-500，**静态**
  - `idle` `#64748b` slate-500，**静态**
- 唯一动效：`healthy` 态的呼吸光晕（`box-shadow: 0 0 0 0 rgba(16,185,129,.6) → 0 0 0 4px rgba(16,185,129,0)`，2s 循环）
- 可带 inline label（同行右侧 8px 间距），label 用 Plex Mono 11px uppercase tracking-wider

**与 components/indicators/skillhub/pulse-dot 区分**：那条 4 色都用 `animate-pulse`（不分场景全闪），用于"在线 / 未读 / 录制"等社交语义；本条仅 healthy 才动，其余全静态——服务运维的"问题态不打扰"原则。

## 核心代码

```tsx
import clsx from 'clsx';

type Status = 'healthy' | 'degraded' | 'critical' | 'idle';

const colorMap: Record<Status, string> = {
  healthy: '#10b981',
  degraded: '#f59e0b',
  critical: '#ef4444',
  idle: '#64748b',
};

interface StatusPulseProps {
  status: Status;
  size?: 6 | 8;
  label?: string;
  className?: string;
}

export function StatusPulse({ status, size = 8, label, className }: StatusPulseProps) {
  const color = colorMap[status];
  const isHealthy = status === 'healthy';
  return (
    <span className={clsx('inline-flex items-center gap-2', className)}>
      <span
        className="rounded-full"
        style={{
          width: size,
          height: size,
          background: color,
          animation: isHealthy ? 'status-pulse-glow 2s ease-out infinite' : undefined,
        }}
      />
      {label && (
        <span className="font-mono text-[11px] uppercase tracking-wider text-slate-400">
          {label}
        </span>
      )}
    </span>
  );
}

/* in global stylesheet */
/*
@keyframes status-pulse-glow {
  0%   { box-shadow: 0 0 0 0   rgba(16,185,129,0.55); }
  70%  { box-shadow: 0 0 0 5px rgba(16,185,129,0);    }
  100% { box-shadow: 0 0 0 0   rgba(16,185,129,0);    }
}
*/
```

## 适配指南

- 表格密集列（行高 32-40px）用 `size=6`，否则 `size=8`
- label 用 inline 形式：`<StatusPulse status="healthy" label="All systems operational" />`
- 不要把 dot 装到 button 内做 icon；本组件是**纯展示**
- 跟随 `instant-snap` 的"零浪漫"原则，degraded / critical 入场不淡入——直接切色

## 反模式

- 不要给 degraded / critical 也加 pulse——告警态闪烁会引发疲劳
- 不要 size > 8——再大就该用 Tag / Banner
- 不要 dot 加 border——纯色实心更清晰
- 不要用 `bg-red-500` / `bg-amber-500`——固定用 rose / amber，与 palette 体系对齐
