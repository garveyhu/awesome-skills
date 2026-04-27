---
id: pages/dashboard/sage/analytics-feedback
type: page
name: 用户反馈分析
description: 反馈占比饼图 + 时间趋势 + 反馈列表（带详情）三段式仪表盘
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, serious]
  stack: [react-antd-tailwind]
uses:
  - blocks/layout/sage/management-layout-header
preview: /preview/pages/dashboard/sage/analytics-feedback
---

# 用户反馈分析

> sage `/analysis/feedback` —— admin 看用户对 AI 回答的 👍 / 👎 反馈分布。三段：① 顶部 KPI 卡片行（总反馈数 / 👍 占比 / 👎 占比）② 时间趋势折线图（@antv/g2）③ 反馈详情列表 + 点击展开看完整对话。

## 页面骨架

1. **ManagementLayout**：title "用户反馈分析" + 时间范围 Select（today / 7d / 30d / 自定义）+ 导出 Excel 按钮
2. **KPI 卡片行** `grid grid-cols-3 gap-4 mb-6`
   - 每张：`bg-white rounded-xl border border-slate-200 p-5`
   - 标题 `text-xs uppercase tracking-wider text-slate-400`
   - 数值 `text-3xl font-bold text-slate-900`
   - 副：环比 ↑/↓ 百分比 + 灰色 "vs 上周"
   - "👍 占比" 卡用 `text-emerald-600`，"👎 占比" 用 `text-rose-600`
3. **时间趋势** `bg-white rounded-xl border border-slate-200 p-5 mb-6`
   - 标题 + 切换 toggle "按天 / 按周"
   - g2 双折线图（👍 / 👎 / 主题色 baseline）+ x 轴时间 / y 轴数量
4. **反馈列表** Table
   - 列：用户 / 时间 / message snippet（line-clamp-1）/ 反馈类型 Tag（👍 emerald / 👎 rose）/ 操作（"查看详情" 链接）
   - 点 "查看详情" 弹 Modal（max-w-3xl）显完整 user message + AI message + 反馈原文（如有）

## 视觉要点

1. **KPI 数字 text-3xl** —— sage 仪表盘最大字号
2. **g2 图表配色**：用主题色 + emerald/rose 双对比色，**不**用主题色当反馈类型色（反馈 ≠ 用户主题）
3. **反馈 Tag 颜色固定**：👍 emerald-50/700/200 三阶；👎 rose-50/700/200。永远不走主题
4. **详情 Modal max-w-3xl** —— 单列大块，让用户能完整阅读对话
5. **Excel 导出**：用 exceljs 在前端打包，按 admin overlay 内规范

## 反模式

- ❌ 反馈 Tag 用主题色 —— 反馈语义独立于用户主题
- ❌ KPI 卡片加阴影 —— sage 仪表盘选 border 而非 shadow，更"仪表"感
