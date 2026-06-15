---
id: blocks/form/chameleon/select-summary-cron-builder
type: block
name: 下拉式 Cron 构建器
description: 用 Select 下拉切频率（每小时/每天/每周/每月/自定义）+ 时/分/周/日各自 Select + 底部实时人类可读摘要 + mono cron 字符串；非整点落 custom 裸 mono input；输出 5 段标准 cron
platforms:
- web
theme: light
tags:
  aesthetic:
  - industrial
  - minimal
  mood:
  - serious
  stack:
  - shadcn-radix
uses:
- tokens/palettes/waveflow/warm-paper-ink-blue
preview: /preview/blocks/form/chameleon/select-summary-cron-builder
---

# 下拉式 Cron 构建器

> Chameleon 的 `CronBuilder`（`core/components/common/cron-builder.tsx`）——可视化生成 5 段标准 cron。受控组件：value 是 cron 字符串、onChange 吐新表达式。用 `Select` 下拉切频率（非 RadioGroup），时 / 分 / 周 / 日各自 Select，底部实时人类可读摘要 + mono cron 字符串；非整点 / 复杂表达式落 custom 模式裸 mono input 原样编辑。

## 视觉特征

- **外层**：`space-y-2`（8px）
- **频率行**：`flex flex-wrap items-center gap-2`（8px）
  - 频率 Select：SelectTrigger `w-[120px]`（每小时 / 每天 / 每周 / 每月 / 自定义表达式）
  - 周天 Select：`w-[92px]`（周日~周六），仅 weekly 显示
  - 月日 Select：`w-[92px]`（1 号~31 号），仅 monthly 显示
  - 时 Select：`w-[78px]`（00 时~23 时，`padStart(2,'0')`），daily/weekly/monthly 显示，后跟 `span.text-stone-400` 的 `:`
  - 分 Select：`w-[78px]`（00/05/10/15/20/30/45 分，`padStart(2,'0')`），非 custom 显示
- **custom 模式**：`Input value=customText placeholder="* * * * *（分 时 日 月 周）" className="font-mono"`
- **摘要行**：`flex items-center gap-2 text-[11px]`，custom 且无文本 `text-stone-400` 否则 `text-stone-500`，含 `span` 人类可读摘要 + `span.font-mono.text-stone-400` 显示当前 cron 表达式

## 核心代码

```tsx
<div className="space-y-2">
  <div className="flex flex-wrap items-center gap-2">
    <Select value={state.freq} onValueChange={...}>
      <SelectTrigger className="w-[120px]"><SelectValue /></SelectTrigger>
      <SelectContent>{FREQ_OPTIONS.map(o => <SelectItem value={o.value}>{o.label}</SelectItem>)}</SelectContent>
    </Select>
    {state.freq === 'weekly' && <Select><SelectTrigger className="w-[92px]">…周天…</SelectTrigger></Select>}
    {state.freq === 'monthly' && <Select><SelectTrigger className="w-[92px]">…月日…</SelectTrigger></Select>}
    {['daily','weekly','monthly'].includes(state.freq) && (
      <><Select><SelectTrigger className="w-[78px]">…时…</SelectTrigger></Select>
        <span className="text-stone-400">:</span></>
    )}
    {state.freq !== 'custom' && <Select><SelectTrigger className="w-[78px]">…分…</SelectTrigger></Select>}
  </div>

  {state.freq === 'custom' && (
    <Input value={customText} placeholder="* * * * *（分 时 日 月 周）" className="font-mono" />
  )}

  <div className={cn('flex items-center gap-2 text-[11px]',
    state.freq === 'custom' && !customText.trim() ? 'text-stone-400' : 'text-stone-500')}>
    <span>{summary}</span>
    <span className="font-mono text-stone-400">
      {state.freq === 'custom' ? customText.trim() : buildCron(state)}
    </span>
  </div>
</div>

// buildCron 输出 5 段：分 时 日 月 周
// hourly → `${m} * * * *` / daily → `${m} ${h} * * *` / weekly → `… ${weekday}` / monthly → `… ${dom} * *`
```

## 与 waveflow/cron-builder-modal 区分

供 AI 消费时选对：

| 维度 | waveflow/cron-builder-modal | chameleon/select-summary-cron-builder |
|------|------|------|
| **频率切换** | `RadioGroup` 行内（5 mode 一眼看完） | `Select` 下拉（w-[120px]，更省横向空间） |
| **字段控件** | `NumberField`（mono Input type=number，arrow 步进） | 全部 `Select` 枚举下拉（时 23 项 / 分 7 档预设 / 周 7 项 / 月日 31 项） |
| **cron 格式** | 6/7 段 xxljob（`秒 分 时 日 月 周 年`） | **5 段标准**（`分 时 日 月 周`） |
| **next time** | 配套 next trigger time popover | 无 next（只给人类可读摘要 + mono 表达式） |
| **复杂表达式回退** | 自定义 mode 写 raw | custom Select 项 → 裸 mono Input 原样编辑 |
| **摘要** | 实时反馈 cron 字符串 | 双行：人类可读摘要 + mono cron 表达式同行 |

选型：xxljob / Quartz 6-7 段 cron + 需要 next time 预览 → waveflow 版；标准 5 段 cron（Linux crontab / APScheduler）+ 极简下拉 → 本变体。

## 适配指南

- 分钟只给 0/5/10/15/20/30/45 七档预设——覆盖绝大多数定时场景，避免 60 项下拉
- 反向解析只在挂载时跑一次（`useState(() => parseCron(value))`），之后由内部交互驱动——避免 value 回灌引起的循环
- 月份字段非 `*` 一律落 custom——builder 只覆盖「每月固定日」，更复杂走裸表达式
- 摘要用 `describe()` 生成中文（如「每周三 09:30 触发」），mono 表达式给工程师核对

## 反模式

- ❌ 分钟用 0-59 全量下拉——60 项滚动列表反人类，给常用档位即可
- ❌ value prop 每次变都重解析回 builder——只挂载时解析一次，否则交互被打断
- ❌ 摘要只给 cron 字符串不给人话——双行（人话 + mono）才是给运营 + 工程师两类人看
