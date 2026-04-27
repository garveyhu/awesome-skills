---
id: pages/list-table/sage/agent-store-split-tabs
type: page
name: 智能体商店分屏
description: 280px sidebar agent list + 主区 ContentHeader + Tabs (config / run) + AgentConfigModal
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - blocks/layout/sage/sidebar-detail-split
  - components/buttons/sage/theme-bg-cta
preview: /preview/pages/list-table/sage/agent-store-split-tabs
---

# Agent Store Split Tabs

> sage `/admin/agent-store` —— 平台所有 Agent（System Agents + Dify Apps + 自定义）的统一商店。左 280 sidebar：标题 + 同步按钮 + 搜索 + agent 列表（icon + name + 类型徽章）；右主区：选中 agent 的 ContentHeader（大 icon + 名 + 描述 + "+ 添加到空间"）+ Tabs（Config / Run）+ Table 显示 spaceApp 配置。

## 页面骨架

### 左 Sidebar（280px）
- `.sidebar-header`：标题 "Agent Store" + 右上 `.sync-btn` 圆形按钮（RefreshCw icon · syncing 时 animate-spin）
- `.search-box`：搜索 input（同 sidebar-detail-split block 的样式）
- `.agent-list`：`<AgentItem $active $primaryColor>` 重复
  - 含 `.agent-icon` 32×32 + `.agent-info`：`.agent-name` + `.agent-type`（System / 自定义）
  - 空态：`flex flex-col items-center py-8 text-slate-400 + Bot 48 + "no agents"`

### 右 MainContent
- **未选**：`<EmptyState>` 大 Bot icon + 提示文字
- **选中**：
  - **ContentHeader**：左侧 `<div className="agent-title">` flex gap-16 + `w-12 h-12 rounded-xl flex center bg: ${primaryColor}15 color: ${primaryColor}` + `<h2>` 22px bold + 副 description；右侧条件按钮：未加到空间显 "+ 添加到空间" CTA
  - **DetailSection**：`<Tabs items={[{ key: 'config', label: <Settings + 配置>, children: ... }, { key: 'run', label: <Play + 运行>, children: <AgentRunPanel /> }]} />`
    - **Config Tab**：当 currentSpaceApp 存在 → `<Table columns dataSource={[currentSpaceApp]} pagination={false}>`（5 列：name / type / config / visibleConfig / actions）；不存在 → 居中 Bot icon + "未添加" + 链接式 CTA
    - **Run Tab**：嵌入 `<AgentRunPanel agentId={selectedAgent.id} />`

### AgentConfigModal（独立 Modal · 配置 agent）
- 触发：表格 actions 的 Settings 图标 / 顶部 "+ 添加到空间"
- 内部：详细配置表单 + visibleConfig 多选 + isEnabled Switch

## 视觉要点

1. **agent-icon 12×12 with `${primary}15` 背景 + `${primary}` icon** —— 主题色淡背 + 同色 icon，比纯填充柔和
2. **Tab 切换条件**：Dify App 如果 `meta?.hideConfigTab=true`，自动隐 Config Tab，激活 Run Tab —— 即"无配置项的 Dify App 直接进运行"
3. **ContentHeader border-bottom 1px #f5f5f5** —— 极淡分割
4. **Sidebar agent-type 字段** 14px slate-400 —— "System / 自定义" 提示但不抢戏
5. **+ 添加到空间** primary CTA 是 antd Button type="primary" + style={{ background: primary }}（双重保险）

## 反模式

- ❌ 不区分 System / Dify / 自定义 三种 agent —— sage 通过 sidebar `.agent-type` 副字段做视觉区分
- ❌ Run Tab 嵌入完整 page —— 用嵌入式 Panel，保持 overlay 的"工具"感
