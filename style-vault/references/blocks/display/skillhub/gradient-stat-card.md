---
id: blocks/display/skillhub/gradient-stat-card
type: block
name: 渐变图标统计卡
description: 运营概览专用——icon 独占右侧 42×42 渐变圆角底 + 色阴影 + 左侧大号数字
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/skillhub/skillhub-teal-mist
  - tokens/shadow/skillhub/ambient-float
preview: /preview/blocks/display/skillhub/gradient-stat-card
---

# Gradient Stat Card

> SkillHub 运营概览的招牌——白底 14px 圆角 + 左边大号 extrabold 数字 + 右边 42×42 渐变色块里塞 icon + 底色配"色影"（`shadow-indigo-500/25`）。用 **indigo / blue / purple / emerald** 四色矩阵做 2×2 或 1×4 分层。

## 视觉特征

- 外框：`bg-white rounded-[14px] border border-slate-200/60 p-[18px] cursor-pointer hover:shadow-md`
- 内部布局：`flex justify-between items-start`
  - 左侧（信息列）：
    - 标签 `text-[11px] text-slate-400 font-semibold tracking-wide mb-1.5`
    - 数值 `text-[28px] font-extrabold text-slate-900 leading-none`（等宽数字感）
    - Hint `text-[11px] text-slate-400 font-medium mt-1.5`（"点击查看详情 →"）
  - 右侧（icon 块）：
    - `w-[42px] h-[42px] rounded-xl bg-gradient-to-br from-<c>-500 to-<c>-400`
    - `shadow-lg shadow-<c>-500/25`（**带色阴影**，不是普通灰阴影）
    - Icon 居中 `text-white` size 20
- 网格：`grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5`（4 卡并排）

## 4 色预设

| key | 用途 | gradient | shadow |
|---|---|---|---|
| indigo | 技能资产 | `from-indigo-500 to-indigo-400` | `shadow-indigo-500/25` |
| blue | 实践案例 | `from-blue-500 to-blue-400` | `shadow-blue-500/25` |
| purple | 社区评论 | `from-purple-500 to-purple-400` | `shadow-purple-500/25` |
| emerald | 注册用户 | `from-emerald-500 to-emerald-400` | `shadow-emerald-500/25` |

（可扩 amber / rose，但建议每个 overview 面板控制在 4 张卡以内）

## 核心代码

```tsx
import type { LucideIcon } from 'lucide-react';

type StatColor = 'indigo' | 'blue' | 'purple' | 'emerald' | 'amber' | 'rose';

const colorCls: Record<StatColor, { grad: string; shadow: string }> = {
  indigo:  { grad: 'from-indigo-500 to-indigo-400',   shadow: 'shadow-indigo-500/25' },
  blue:    { grad: 'from-blue-500 to-blue-400',       shadow: 'shadow-blue-500/25' },
  purple:  { grad: 'from-purple-500 to-purple-400',   shadow: 'shadow-purple-500/25' },
  emerald: { grad: 'from-emerald-500 to-emerald-400', shadow: 'shadow-emerald-500/25' },
  amber:   { grad: 'from-amber-500 to-amber-400',     shadow: 'shadow-amber-500/25' },
  rose:    { grad: 'from-rose-500 to-rose-400',       shadow: 'shadow-rose-500/25' },
};

interface GradientStatCardProps {
  label: string;
  value: number | string;
  icon: LucideIcon;
  color?: StatColor;
  hint?: string;
  onClick?: () => void;
}

export const GradientStatCard = ({
  label, value, icon: Icon, color = 'indigo', hint = '点击查看详情 →', onClick,
}: GradientStatCardProps) => {
  const c = colorCls[color];
  return (
    <div
      onClick={onClick}
      className="bg-white rounded-[14px] border border-slate-200/60 p-[18px]
                 cursor-pointer hover:shadow-md transition-all"
    >
      <div className="flex justify-between items-start">
        <div>
          <div className="text-[11px] text-slate-400 font-semibold tracking-wide mb-1.5">
            {label}
          </div>
          <div className="text-[28px] font-extrabold text-slate-900 leading-none">
            {value}
          </div>
          {hint && (
            <div className="text-[11px] text-slate-400 font-medium mt-1.5">{hint}</div>
          )}
        </div>
        <div
          className={`w-[42px] h-[42px] rounded-xl bg-gradient-to-br ${c.grad}
                      flex items-center justify-center shadow-lg ${c.shadow}`}
        >
          <Icon className="text-white" size={20} />
        </div>
      </div>
    </div>
  );
};
```

## 网格容器

```tsx
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5">
  <GradientStatCard label="技能资产" value={overview.skillCount} icon={Database} color="indigo" />
  <GradientStatCard label="实践案例" value={overview.practicePostCount} icon={Activity} color="blue" />
  <GradientStatCard label="社区评论" value={overview.commentCount} icon={MessagesSquare} color="purple" />
  <GradientStatCard label="注册用户" value={overview.activeUserCount} icon={Users} color="emerald" />
</div>
```

## 配套：数据分布条 + 趋势 mini card

管理后台 overview tab 通常和两个同家族组件一起用：

### 数据分布条（横向渐变填充）

```tsx
<div className="flex items-center gap-3">
  <span className="text-[11px] text-slate-400 w-14 shrink-0">{row.label}</span>
  <div className="flex-1 bg-slate-100 rounded-full h-2 overflow-hidden">
    <div
      className={`bg-gradient-to-r ${row.color} h-full rounded-full transition-all`}
      style={{ width: `${pct}%` }}
    />
  </div>
  <span className="text-[11px] font-bold text-slate-600 w-8 text-right">{row.value}</span>
</div>
```

### Trend mini card（2×2）

```tsx
<div className="rounded-xl bg-slate-50 p-3.5">
  <div className="text-[11px] text-slate-400 font-semibold">同步成功率</div>
  <div className="text-[22px] font-extrabold text-slate-900 mt-1 leading-none">98%</div>
  <div className="text-[10px] text-emerald-600 font-semibold mt-1.5">528/540 次同步</div>
</div>
```

## 适配指南

- `shadow-<c>-500/25` 是 Tailwind 的色阴影——25% 透明度，不刺眼但能感知；不能简单替换成 `shadow-lg`（灰阴影），会失去"色"的表现力
- 圆角用 `rounded-[14px]` 而不是 `rounded-xl`（12）或 `rounded-2xl`（16）——14 是本 block 的节奏基调，夹在中间，和 icon 块的 `rounded-xl`（12）错开 2px 形成层次
- 数字尺寸 `28px` 不是 Tailwind 默认 `text-3xl`（30）——微小差异让 overview 不争戏
- label `tracking-wide`（不是 `tracking-wider`）——stat 的 label 要含蓄，不要 uppercase
- hint 可选，但"点击查看详情 →"的模式让整卡变成交互入口，别丢掉箭头

## 反模式

- 不要在同一个 overview 里混超过 4 种色——色影泛滥，视觉分层塌
- 不要用 `bg-gradient-to-r`（横向）——overview 的渐变全部 `bg-gradient-to-br`（右下，更规整）
- 不要给卡加 shadow 常态——hover 才 shadow-md，静态靠 border 分层
- 不要把数字做成 `font-mono`——Inter 的 `font-extrabold` 数字本身够 tabular 了
