---
id: pages/detail/sage/collection-detail
type: page
name: 收藏夹详情（问答重放）
description: 顶部头 + 取消收藏 / 重新执行 · 中间用 ChatMessage 复用展示原问答（用户/AI 双气泡 + 表 + 图）· 底部 antd Table 展示历次执行日志（status / duration / preview / download）
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm]
  stack: [react-antd-tailwind]
preview: /preview/pages/detail/sage/collection-detail
uses:
  - pages/dashboard/sage/agent-chat-stream
---

# Collection Detail (Replay)

> sage 收藏的问答的"详情 + 重放"页面。复用 ChatMessage 渲染原始问答（最大化保留原视觉），下方 Table 展示历次"重新执行"的日志（成功 / 失败 / 时长 / 行数 / 操作）。点 Eye 弹原结果，Play 重新跑 SQL 以拿到最新数据。

## 整体外壳

```jsx
<ConfigProvider>
  <div className="flex-1 w-full flex flex-col h-full bg-white">
    <Header />
    <Main (chat replay + log table) />
    <Fullscreen Portal (QueryResult)? />
  </div>
</ConfigProvider>
```

## Header

`flex justify-between items-center p-4 border-b border-slate-200`：
- 左：`<PanelLeftOpen />` + `<Button icon={<ArrowLeft />} h-10 w-10>`
- 中（absolute）：`font-semibold text-slate-700` "本月销售 Top 10 · 主问题截断"
- 右 `space-x-2`：
  - `<Button>` `<Play size={14} />`（或 `<Loader2 animate-spin />` loading）→ 重新执行
  - `<Button>` `<Star fill />` → 取消收藏（已在收藏页所以默认 fill）

## Main 内容区

`flex-1 overflow-auto p-6 space-y-6 bg-white`，内层 `max-w-4xl mx-auto space-y-6`：

### 重放（复用 ChatMessage）
- 1 条用户气泡（`bg-[rgb(246,246,246)] rounded-3xl`）
- 1 条 AI 气泡（透明背景 + 嵌 NarrationCard + QueryResult + TrustBadge）
- 完全复用 chat 页面的渲染管线

### 执行日志表格

容器 `bg-white p-6 rounded-xl shadow-sm border border-slate-200 w-full`：
- 标题 `flex items-center gap-2 mb-4` + `<History size={16} />` "执行历史"
- antd `<Table size="small" pagination={false}>`：
  - executedAt：格式化日期
  - status：`bg-green-100 text-green-700` 或 `bg-red-100 text-red-700` chip
  - executionDuration：`fontFamily: monospace` 持续秒数
  - resultSummary：行数 + 列数
  - actions：`<Eye>` 预览（弹 QueryResult 全屏）+ `<Download>` 导出 Excel

## Fullscreen QueryResult

条件 `isFullscreen` 时 `<div className="fixed inset-0 z-[9999]">` 套整张 QueryResult。

## 视觉要点

1. **复用 ChatMessage 而不是重做**：保证收藏的问答视觉与对话页 100% 一致
2. **Play / Loader2 切换**：单按钮即时反馈"正在重新执行"
3. **status chip 双色**：green-100/700 成功 vs red-100/700 失败 —— 颜色直接映射结果
4. **History icon 标识表格语义**：与上方 chat 重放区隔开
5. **导出 Excel 用 ExcelJS + file-saver**：客户端生成，避免服务端往返

## 反模式

- ❌ 不要重写 ChatMessage —— 直接复用，否则收藏页与对话页视觉漂移
- ❌ Fullscreen 不要用 antd Modal —— inset-0 + z-[9999] 全屏覆盖更轻量

## 使用上游
- `pages/list-table/sage/collection-list`（点收藏卡片进入）

## 内嵌
- `<ChatMessage>` from chat 模块（用户气泡 + AI 气泡 + 渲染器）
- `<QueryResult>`（fullscreen portal 展示原查询结果）
- `<DataQAProvider>`（包 ChatMessage 注入 showSQL / enableDownloadExcel）
