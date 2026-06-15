---
id: components/inputs/chameleon/dayjs-range-picker
type: component
name: dayjs 月历区间选择器
description: dayjs 自绘 MonthCalendar（周一首列 + 42 格 + 区间高亮）+ trigger/popover + 预设；两种布局（底部横排预设 / 左侧预设侧栏）
platforms:
- web
theme: light
tags:
  aesthetic:
  - minimal
  mood:
  - calm
  stack:
  - shadcn-radix
uses:
- components/feedback/chameleon/radix-overlay-primitives
preview: /preview/components/inputs/chameleon/dayjs-range-picker
---

# Chameleon dayjs 月历区间选择器

> 日期范围选择器，与 waveflow datetime-range-presets 同源（trigger + popover + 预设）但结构明显分叉：用 dayjs 自绘 `MonthCalendar`（点两次选起止、区间高亮）而非原生 `datetime-local`。两种布局：①`DateTimeRangePicker` 窄 280px popover + 底部横排预设（今天/近7天/近30天）+ 清空/应用 + mono 区间回显；②`DateRangePicker` 左侧 6 预设侧栏（今天/昨天/近7天/近30天/本月/上月）+ 右侧月历 + 底部 mono 预览 + 主色应用。trigger 显 `MM-DD ~ MM-DD` + Calendar icon。

## 视觉特征

### MonthCalendar（共享内核）

- **头行**：`mb-1.5 flex items-center justify-between px-1`：左右 `<ChevronLeft/Right className="h-3.5 w-3.5"/>` 按钮 `rounded p-1 text-stone-400 hover:bg-stone-100 hover:text-stone-700` + 中间月份 `text-[12.5px] font-medium text-stone-700` 「YYYY 年 M 月」
- **周名行**：`grid grid-cols-7 gap-y-0.5`，`WEEKDAYS=[一二三四五六日]` 每个 `py-1 text-center text-[10.5px] text-stone-400`（`leading=(first.day()+6)%7` → 周一首列）
- **42 天格**：button `mx-auto flex h-7(28px) w-7 items-center justify-center rounded-md(6px) text-[12px] transition`
  - 跨月 `text-stone-300` / 本月 `text-stone-700`
  - 区间内非端点 `bg-blue-50 text-blue-700`
  - 选中端点 `bg-blue-600 font-medium text-white hover:bg-blue-600`
  - 今天非选 `font-semibold text-blue-600`
  - 用字面 `blue-600/blue-50`（非 themeable primary）

### DateTimeRangePicker（窄 popover + 底部横排预设）

- **Trigger**：`flex items-center gap-2(8px) rounded-md(6px) border border-stone-300 bg-white px-2.5(10px) hover:border-stone-400 focus:border-blue-500(#3b82f6) focus:ring-2 focus:ring-blue-100(#dbeafe)` + size `sm h-7(28px) text-[12px]` / `md h-8(32px) text-[13px]`，triggerWidth 默认 200px
  - `<CalIcon className="h-3.5 w-3.5 shrink-0 text-stone-400"/>` + span `tnum flex-1 truncate text-left font-mono`（有值 `text-stone-800` / 占位 `!font-sans text-stone-400`）显 `MM-DD ~ MM-DD`
  - 已选时 X 清空 `rounded p-0.5 text-stone-400 hover:bg-stone-100 hover:text-stone-700` 内 `<X className="h-3 w-3"/>`
- **PopoverContent `!w-[280px]` align=start**：MonthCalendar + `mt-2 flex items-center justify-between border-t border-stone-100 pt-2`
  - 左：3 预设 `rounded border border-stone-200 px-1.5 py-0.5 text-[11px] text-stone-600 hover:border-stone-400 hover:text-stone-900`
  - 右：ghost「清空」+ primary「应用」（Button sm，disabled=!start）
  - 底回显 `mt-1.5 text-center font-mono text-[11px] text-stone-500` 显 `MM-DD ~ MM-DD` 或占位 `text-stone-400`「点选起止日期」

### DateRangePicker（左侧预设侧栏）

- **Trigger**：`bg-paper inline-flex h-7(28px) items-center gap-2(8px) rounded-md(6px) border border-stone-200 px-2.5(10px) text-[12px] text-stone-700 hover:border-stone-300`，`<CalendarIcon className="h-3.5 w-3.5 text-stone-400" strokeWidth={1.75}/>` + span.tnum `YYYY-MM-DD ~ YYYY-MM-DD` + `<ChevronDown className="h-3 w-3 text-stone-400"/>`
- **PopoverContent `!w-auto !p-0` align=end**：`flex` 布局
  - 预设侧栏：`ul w-24(96px) shrink-0 space-y-0.5 border-r border-stone-100 p-2(8px)`，每项 `w-full rounded-md px-2 py-1.5(6px) text-left text-[12px] text-stone-600 hover:bg-stone-100 hover:text-stone-900`（今天/昨天/近7天/近30天/本月/上月）
  - 日历区：`p-3(12px)` MonthCalendar + 底部 `mt-2 flex items-center justify-between border-t border-stone-100 pt-2` 左 mono 预览 + 右 primary「应用」

## 核心代码

```tsx
const WEEKDAYS = ['一','二','三','四','五','六','日'];
const leading = (first.day() + 6) % 7; // 周一为第 0 列
const days = Array.from({ length: 42 }, (_, i) => gridStart.add(i, 'day'));

<button className={cn('mx-auto flex h-7 w-7 items-center justify-center rounded-md text-[12px] transition',
  out ? 'text-stone-300' : 'text-stone-700',
  range && 'bg-blue-50 text-blue-700',
  sel && 'bg-blue-600 font-medium text-white hover:bg-blue-600',
  today && !sel && 'font-semibold text-blue-600')}>
  {d.date()}
</button>

// 点两次选起止
const pick = (d: Dayjs) => {
  if (!start || (start && end)) { setStart(d); setEnd(null); }
  else if (d.isBefore(start, 'day')) setStart(d);
  else setEnd(d);
};
```

## 适配指南

- 紧凑场景（toolbar 行内筛选）用窄 280px popover + 底部横排预设
- 仪表盘 / 报表用左侧预设侧栏布局——6 个常用范围一列罗列，比横排好扫
- 对外 API：窄版 `{start?, end?: 'YYYY-MM-DD HH:mm:ss'}`（起 00:00:00 止 23:59:59）；侧栏版 `{from, to: Date}`
- 区间端点 / 高亮用字面 blue-600/blue-50——这里不走 themeable primary，刻意固定蓝

## 与 waveflow/datetime-range-presets 区分

| 维度 | waveflow datetime-range-presets | chameleon dayjs-range-picker |
|------|---------------------------------|------------------------------|
| 日历 | **无日历**，两个原生 `<input type="datetime-local">` | **dayjs 自绘 MonthCalendar** 42 格点选起止 + 区间高亮 |
| popover 宽 | **~480px** `grid-cols-[160px_1fr]` | **280px 窄**（底部预设版）/ `!w-auto` 自适应（侧栏版） |
| 预设位置 | **左列竖排**（160px 列） | 底部横排（窄版）/ 左侧 96px 侧栏（侧栏版） |
| 依赖 | 原生 Date + 字符串解析，**不引 dayjs** | **dayjs**（区间判断 isBefore/isAfter/isSame） |
| 回显 | trigger 显 `start ~ end` | trigger + popover 底部双重 **mono `MM-DD ~ MM-DD`** 回显 |
| 精度 | 到 **HH:mm** 分钟 | 到 **日**（起止补 00:00:00 / 23:59:59） |

选型：需要精确到分钟（日志时间区间）用 waveflow 原生 datetime-local；只到日 + 要好看的月历点选 + 区间高亮用 chameleon dayjs 版。

## 反模式

- ❌ 引 react-day-picker 替自绘月历——dayjs + 42 格自绘已够，加包浪费 30KB
- ❌ 预设按钮 > 8 个——选择困难，最多 6 个（今天/昨天/近7/近30/本月/上月）
- ❌ 不校验 start ≤ end——pick 逻辑里 `d.isBefore(start)` 自动校正，别绕过
- ❌ 月历端点用 themeable primary——这里刻意固定 blue-600，跨主题保持日历可读性
