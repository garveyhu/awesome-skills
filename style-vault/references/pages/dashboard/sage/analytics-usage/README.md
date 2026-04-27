---
id: pages/dashboard/sage/analytics-usage
type: page
name: 模型用量分析
description: 模型 token / 请求次数 / 成本聚合仪表盘 + 模型对比 + 用户 Top10
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, serious]
  stack: [react-antd-tailwind]
uses:
  - blocks/layout/sage/management-layout-header
preview: /preview/pages/dashboard/sage/analytics-usage
---

# 模型用量分析

> sage `/analysis/usage` —— admin 监控各模型在空间内的调用情况。四段：① 顶部 KPI（总 tokens / 总请求 / 总耗时 / 估算成本）② 各模型用量对比柱状图 ③ 时间趋势折线 ④ Top10 用户表。

## 页面骨架

1. **ManagementLayout**：title "模型用量分析" + 时间范围 Select + 模型 multi-Select（默认全选）+ 导出
2. **KPI 卡片行** `grid grid-cols-4 gap-4 mb-6`
   - 每张：bg-white rounded-xl border border-slate-200 p-5
   - 4 张卡：`总 Tokens` / `总请求` / `平均耗时` / `估算成本（$）`
   - 数值 text-3xl font-bold + ↑/↓ 环比
   - 第 4 张（成本）用 `text-amber-600`（钱用琥珀色）
3. **模型对比** `bg-white rounded-xl border border-slate-200 p-5 mb-6`
   - g2 横向柱状图：每个 model 一行，长度按 tokens 数；主题色填充
   - 条侧 model.name + 副 (provider · base_model)
4. **时间趋势** `bg-white rounded-xl border border-slate-200 p-5 mb-6`
   - 双 y 轴：左 tokens（主题色） + 右 请求次数（slate）
5. **Top10 用户表**
   - 列：用户 avatar+name / 调用次数 / 累计 tokens / 最近调用时间 / 偏好模型 Tag

## 视觉要点

1. **g2 配色**：主图表用 `THEME_HEX_COLORS[themeColor]`；辅助色用 slate-300/400 灰阶
2. **成本卡 amber** —— 不是橙色 themeColor 会撞，sage 用 `amber-600`（区别于 orange-400 的主题）
3. **柱状图条用主题色填充**，hover 加深一档（`THEME_HEX_COLORS[themeColor]` 主色 + `bgHover` 加深）
4. **Top10 用户表 avatar 走 themedCircleAvatar block** —— 每个用户跟自己的主题色一致
5. **导出 Excel 按完整时间区间 / 模型筛选导出**

## 反模式

- ❌ 把 4 张 KPI 卡都涂成主题色 —— 仪表盘需要"中性数据"感，主题色只用于强调
- ❌ 柱状图用渐变 / 阴影 —— sage 仪表选纯色块，让数据本身说话
