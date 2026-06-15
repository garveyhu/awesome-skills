---
id: blocks/display/sage/chart-card-tabs
type: block
name: 图表分析卡（多 Tab）
description: 顶部多 Tab 标题切换 + 右上 dropdown 类型切换 + Download + Fullscreen，body 区 G2 渲染（柱/折线/饼/条），350px 固定高
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, swiss]
  mood: [calm, serious]
  stack: [react-antd-tailwind]
preview: /preview/blocks/display/sage/chart-card-tabs
---

# Chart Card with Tabs

> sage 数据问答里的图表卡。区别于普通 antd Card：顶部是**多个图表标题的 Tab 切换**（一次回答可能产出 2-3 个分析图），右侧是**图表类型切换 dropdown** + Download + Fullscreen。底部 G2 v5 渲染 350px 高图表。

## 整体结构

外层：`border border-gray-200 rounded-lg overflow-hidden flex flex-col bg-white transition-all duration-300`，hover 升级 `hover:shadow-md hover:border-gray-300`，全屏时 `fixed inset-4 z-[9999] shadow-2xl`。

### Header（Tabs + Actions）

容器：`flex items-center justify-between border-b border-gray-100 bg-gray-50/50`

**左：Tabs 区** `flex overflow-x-auto no-scrollbar flex-1 mr-4`
- 每个 tab：`flex items-center gap-2 px-4 py-3 text-sm font-medium whitespace-nowrap transition-all border-r border-gray-100/50 outline-none`
- 选中：`text-${themeColor}-600 bg-white border-b-2 border-b-${themeColor}-500 -mb-[1px] shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.02)]`
- 未选中：`text-gray-500 hover:text-gray-700 hover:bg-gray-100/50 border-b-2 border-b-transparent`
- 圆点：`w-1.5 h-1.5 rounded-full ${isSelected ? 'bg-${themeColor}-500' : 'bg-gray-300'}`
- Tooltip 包裹（标题 > 14 字时显完整）+ `truncate max-w-[200px]`

**右：Actions** `flex items-center gap-1 px-2 border-l border-gray-100 bg-transparent h-full shrink-0`
1. 类型 Dropdown button：`flex items-center gap-1.5 px-2 py-1.5 text-sm text-gray-600 hover:text-${themeColor}-600 hover:bg-${themeColor}-50 rounded-md` + 当前类型 icon + 名称 + ChevronDown(14, gray-400)
   - 选项：`table` / `column` / `bar`（90° 旋转的 BarChartOutlined）/ `line` / `pie`，全用 antd 老 Outlined icon
2. 分隔线：`w-px h-3 bg-gray-200 mx-2`
3. Download：`p-1.5 text-gray-500 hover:text-gray-700 hover:bg-gray-50 rounded-md`（仅 enableDownloadExcel 时）
4. Fullscreen：`p-1.5 ...` 同上 — Maximize / Minimize2 切换

### Body

`w-full bg-white ${isChartFullscreen ? 'p-6 h-[calc(100%-48px)]' : 'h-[350px]'}`

内嵌 `<ChartRenderer>`：传 G2 v5 ChartConfig + ChartData + height={350}，`key={selectedChartIndex}-${activeChartType}` 强制重渲染。

## G2 实践

- 多系列（seriesField 存在）→ `chart.options({ paddingTop: 35 })` + 顶部图例
- 无显式 series → `chart.legend(false)` 隐藏冗余图例
- 主题色板：G2 默认 10 色（蓝 #5B8FF9 / 青 #5AD8A6 / 灰蓝 #5D7092 / 黄 #F6BD16 / 橙 #E8684A 等），不跟随主题色
- 柱图、条图（90° 旋转）共享 `interval` 形状 + transpose 坐标变换

## 视觉要点

1. **Tab + Dropdown 双切换**：tab 切的是"哪张图"（不同维度的多张分析），dropdown 切的是"用什么形状画"（柱/折/饼）
2. **选中 tab 的 -mb-[1px]**：让 tab 底部的 border-b-2 主题色线和外层 border-b border-gray-100 融为一体（无双边线毛刺）
3. **shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.02)]**：选中 tab 微弱顶部阴影，模拟"浮起"感
4. **dropdown 用纯按钮不用 antd Button**：完全自定义文字 + icon + ChevronDown，色随主题
5. **fullscreen 用 fixed inset-4 z-[9999]**：四边各 16px 留白避免贴满屏幕

## 反模式

- ❌ 不要用 antd `Tabs` 组件 —— 视觉风格无法精细控制（tab 的下划线高度、间距）
- ❌ 不要把 ChartRenderer 的 key 写死 —— 切类型时必须 unmount 让 G2 重画，否则坐标系会保留旧状态

## 使用上游
- `agents/data-qa/components/QueryResult` （唯一调用方）
