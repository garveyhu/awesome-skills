---
id: blocks/feedback/acme/saas-status-banner
type: block
name: SaaS 状态告警条
description: 32px 全宽顶部告警条 · 三态（neutral/warning/critical）· critical 才出 pulse
platforms: [web]
theme: dark
tags:
  aesthetic: [minimal, industrial]
  mood: [cold, serious]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/acme/slate-cyan-ice
  - tokens/typography/pairs/acme/ibm-plex-duo
  - components/indicators/acme/status-pulse
preview: /preview/blocks/feedback/acme/saas-status-banner
---

# SaaS Status Banner

> 顶栏下方的全局告警条：三态色阶 + 等宽时间戳 + 一键关闭。

## 视觉特征

- 高度 32px；全宽；位于 topbar 之下、内容区之上
- 三态：
  - **neutral**: 仅信息提示。`bg-slate-900` + `border-b border-slate-800`，slate-300 字
  - **warning**: 性能 / 局部异常。`bg-amber-950/60` + `border-b border-amber-700/50`，amber-200 字
  - **critical**: 故障 / outage。`bg-rose-950/70` + `border-b border-rose-700/60`，rose-200 字 + 左侧 `<StatusPulse status="critical" />`（critical 唯一动态）
- 行内 layout：左侧 dot（仅 critical 显示）+ Plex Mono 时间戳 `02:14:08 UTC` + 主文案 + 右侧 dismiss `×`
- 不要任何渐变 / 阴影 / 圆角

## 核心代码

```tsx
import { StatusPulse } from '../../components/indicators/acme/status-pulse';

type Severity = 'neutral' | 'warning' | 'critical';

const cls: Record<Severity, string> = {
  neutral:  'bg-slate-900 border-slate-800 text-slate-300',
  warning:  'bg-amber-950/60 border-amber-700/50 text-amber-200',
  critical: 'bg-rose-950/70 border-rose-700/60 text-rose-200',
};

export function SaasStatusBanner({
  severity,
  timestamp,
  message,
  onDismiss,
}: {
  severity: Severity;
  timestamp: string;
  message: string;
  onDismiss?: () => void;
}) {
  return (
    <div
      role="alert"
      className={`h-8 px-4 border-b text-[12px] flex items-center gap-3 ${cls[severity]}`}
    >
      {severity === 'critical' && <StatusPulse status="critical" size={6} />}
      <span className="font-mono text-[11px] tracking-wider opacity-70">
        {timestamp}
      </span>
      <span className="flex-1 truncate">{message}</span>
      {onDismiss && (
        <button
          onClick={onDismiss}
          className="opacity-60 hover:opacity-100 transition-opacity duration-150 ease-out"
          aria-label="dismiss"
        >
          ×
        </button>
      )}
    </div>
  );
}
```

## 适配指南

- 永远位于 topbar 下方、内容区上方
- timestamp 用 ISO 短时 + 时区（UTC / local）；不用相对时间
- 多个 banner 堆叠时按"critical → warning → neutral"顺序，每条 32px 累加高度
- 没有 banner 时**不**保留占位空白（不要 placeholder）

## 反模式

- 不要让 banner 高度变化（≥ 2 行就该换 toast / drawer）
- 不要 warning / neutral 也加 pulse
- 不要给 banner 加 CTA 按钮——出问题就上 incident 详情页
- 不要圆角
