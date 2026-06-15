---
id: pages/dashboard/skillhub/admin-overview
type: page
name: 运营概览页
description: 管理后台 overview tab 独立成页——4 格渐变 stat card + 数据分布条 + 趋势迷你卡
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - blocks/nav/skillhub/glass-pill-navbar
  - blocks/display/skillhub/gradient-stat-card
  - tokens/palettes/skillhub/skillhub-teal-mist
  - tokens/typography/pairs/skillhub/inter-jetbrains-duo
preview: /preview/pages/dashboard/skillhub/admin-overview
---

# Admin Overview

> 管理后台"运营概览"tab 的独立页面化。`admin-console` 是 Tabs 骨架，这条专注"概览"这一 tab 的内容：**4 格渐变 stat card + 2 列布局（数据分布条 / 平台趋势 mini card 2×2）**。

## 页面骨架

```
┌─ GlassPillNavbar ────────────────────────────────────────┐
│                                                          │
│  ┌─ Admin 外框 max-w-7xl px-4 py-6 ─────────────────┐    │
│  │                                                   │    │
│  │  [H1 "管理后台"]                                   │    │
│  │                                                   │    │
│  │  [admin-console 用到的 Tabs]（内嵌时只 active 概览）│    │
│  │                                                   │    │
│  │  ┌─ 4 格 stat card（grid-cols-4）───────────────┐ │    │
│  │  │  [indigo 技能资产] [blue 实践案例]            │ │    │
│  │  │  [purple 社区评论] [emerald 注册用户]         │ │    │
│  │  └─────────────────────────────────────────────┘ │    │
│  │                                                   │    │
│  │  ┌─ 2 列：数据分布 / 平台趋势 ──────────────────┐ │    │
│  │  │ ┌─ 数据分布 ─────────┐ ┌─ 平台趋势 ─────────┐│ │    │
│  │  │ │ 技能 ───── 76      │ │ [同步成功率 98%]    ││ │    │
│  │  │ │ 实践 ─────── 184   │ │ [活跃数据源 11]     ││ │    │
│  │  │ │ 评论 ────── 920    │ │ [待审提交 4]        ││ │    │
│  │  │ │ 数据源 ── 12       │ │ [内容密度 0.8]      ││ │    │
│  │  │ └──────────────────┘ └──────────────────────┘│ │    │
│  │  └─────────────────────────────────────────────┘ │    │
│  └─────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘
```

## 核心代码

```tsx
import { Activity, AreaChart, Database, MessagesSquare, Users } from 'lucide-react';
import { GradientStatCard } from '../blocks/display/GradientStatCard';

export const AdminOverviewPage = () => {
  const [overview, setOverview] = useState<AdminOverview>(emptyOverview);

  const distribution = [
    { label: '技能',   value: overview.skillCount,       color: 'from-indigo-500 to-indigo-400' },
    { label: '实践',   value: overview.practicePostCount, color: 'from-blue-500 to-blue-400' },
    { label: '评论',   value: overview.commentCount,     color: 'from-purple-500 to-purple-400' },
    { label: '数据源', value: overview.repositoryCount,  color: 'from-amber-500 to-amber-400' },
  ];
  const total = distribution.reduce((s, r) => s + r.value, 0);

  return (
    <>
      <GlassPillNavbar sticky={false} /* ... */ />

      <div className="max-w-7xl mx-auto px-4 py-6 font-sans">
        <h1 className="text-2xl font-extrabold text-slate-900 mb-6">管理后台</h1>

        <div className="px-4 pb-4">
          {/* 4 格 stat card */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5">
            <GradientStatCard label="技能资产" value={overview.skillCount}        icon={Database}       color="indigo" />
            <GradientStatCard label="实践案例" value={overview.practicePostCount} icon={Activity}       color="blue" />
            <GradientStatCard label="社区评论" value={overview.commentCount}      icon={MessagesSquare} color="purple" />
            <GradientStatCard label="注册用户" value={overview.activeUserCount}   icon={Users}          color="emerald" />
          </div>

          {/* 数据分布 + 平台趋势 */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mt-4">
            <PanelCard title="数据分布">
              <div className="space-y-3.5">
                {distribution.map((row) => {
                  const pct = total > 0 ? Math.max((row.value / total) * 100, row.value > 0 ? 3 : 0) : 0;
                  return (
                    <div key={row.label} className="flex items-center gap-3">
                      <span className="text-[11px] text-slate-400 w-14 shrink-0">{row.label}</span>
                      <div className="flex-1 bg-slate-100 rounded-full h-2 overflow-hidden">
                        <div
                          className={`bg-gradient-to-r ${row.color} h-full rounded-full transition-all`}
                          style={{ width: `${pct}%` }}
                        />
                      </div>
                      <span className="text-[11px] font-bold text-slate-600 w-8 text-right">{row.value}</span>
                    </div>
                  );
                })}
              </div>
            </PanelCard>

            <PanelCard title="平台趋势">
              <div className="grid grid-cols-2 gap-2.5">
                <TrendMini label="同步成功率" value={`${syncRate}%`} sub={`${success}/${total} 次同步`} subColor="text-emerald-600" />
                <TrendMini label="活跃数据源" value={activeRepos} sub={`共 ${totalRepos} 个源`} subColor="text-blue-600" />
                <TrendMini label="待审提交" value={pendingSubs} sub={`共 ${totalSubs} 个提交`} subColor="text-purple-600" />
                <TrendMini label="内容密度" value={density} sub="帖+评/活跃用户" subColor="text-amber-600" />
              </div>
            </PanelCard>
          </div>
        </div>
      </div>
    </>
  );
};

const PanelCard = ({ title, children }: { title: string; children: React.ReactNode }) => (
  <div className="bg-white border border-slate-200/60 rounded-[14px] p-[18px]">
    <div className="text-[13px] font-bold text-slate-900 mb-4">{title}</div>
    {children}
  </div>
);

const TrendMini = ({ label, value, sub, subColor }: { label: string; value: string | number; sub: string; subColor: string }) => (
  <div className="rounded-xl bg-slate-50 p-3.5">
    <div className="text-[11px] text-slate-400 font-semibold">{label}</div>
    <div className="text-[22px] font-extrabold text-slate-900 mt-1 leading-none tabular-nums">{value}</div>
    <div className={`text-[10px] font-semibold mt-1.5 ${subColor}`}>{sub}</div>
  </div>
);
```

## 视觉要点

- 整页的容器 `rounded-[14px]` 而非 `rounded-2xl`——运营概览模块独有的节奏（14px 夹在 12/16 之间）
- stat card 渐变 `bg-gradient-to-br` + 色阴影——这是整个 skillhub 最"装饰性"的一处，允许多色
- 数据分布条用 **gradient fill**（横向），和 stat card icon bubble 的 gradient 保持视觉家族
- 趋势 mini card 用 `bg-slate-50` 灰底而不是白底——和上一行 stat card 形成对比
- 数字全部 `tabular-nums`——让"98%"这种在不同数值下对齐

## 适配指南

- 此页和 `admin-console` 可以**并存**：
  - `admin-console` 是 Tabs 骨架页，概览在 Tab 1
  - `admin-overview` 是独立路由版（如果未来要拆出 `/admin/overview` 作为深链）
- 4 色 gradient + color-shadow 是整站**唯一允许**用这种多彩表达的地方——其它地方保持 teal + slate
- 指标数字从 API 来，不要写死；0 的时候进度条仍留 3% 最小可见条宽
- 响应式：大屏 4-col，中屏 2-col，小屏 1-col

## 反模式

- 不要在概览里插入 chart（面积图 / 折线图）——本 style 不配大型 chart 容器；需要的话另起 page
- 不要让渐变流到分布条以外的地方（如标题 / 按钮）——那是 hero 的专利
- 不要把数据源数量也用 gradient stat card——它属于系统元信息，用 TrendMini 就够
- 不要去掉色阴影——那是这个 block 最独特的视觉信号
