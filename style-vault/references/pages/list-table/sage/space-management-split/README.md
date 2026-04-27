---
id: pages/list-table/sage/space-management-split
type: page
name: 工作区管理分屏
description: 280 sidebar (空间列表) + 主区 (空间详情 + 成员表 + 角色 + Tab)，AgentStorePage 同款骨架
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm, serious]
  stack: [react-antd-tailwind]
uses:
  - blocks/layout/sage/sidebar-detail-split
preview: /preview/pages/list-table/sage/space-management-split
---

# Space Management Split

> sage `/spaces` + `/spaces/:id/models` + `/spaces/:id/core-config` —— 空间生命周期管理。和 AgentStore 共用 `sidebar-detail-split` 骨架（280 + 主区），但内容不同：sidebar 是空间列表 + "+ 新建空间"；主区是空间名 / 描述 / Avatar 集合 + "+ 添加成员" + 成员表 + 角色管理 / Models 配置 / Core Config 三 Tab。

## 页面骨架

### Sidebar
- 标题 "工作区" + 右上 "+ 新建空间" `.add-btn`（主题色淡底圆角按钮）
- 搜索框（同 agent-store）
- SpaceItem：active 加 `bg: #f5f5f5 + border: 1px #e5e5e5`，icon 12×12 主题色淡底 + `.space-name` 14px medium + `.space-desc` 11px slate-400 副行（成员数 / 数据源数）

### MainContent
- **ContentHeader**：左 大 icon (12×12 themed) + h2 + 描述；右 "+ 添加成员" 主题色 CTA
- **DetailSection**（Tabs 标准 antd）：
  - **成员**：Table（avatar / name / 角色 Tag / 加入时间 / 移除）
  - **模型配置**：ModelConfig 嵌入（model 列表 + 启用 Switch + 主题色注入）
  - **核心配置**：CoreConfigPage 嵌入（默认 datasource / 是否允许下载 Excel 等空间级 toggle）
- **新建/编辑空间 Modal**：name + description + 高级配置（成员邀请 / 默认 datasource）

## 视觉要点

1. **Sidebar 列表项 4 行**：name + desc + (可选) 标签徽章 —— 比 agent-store 单行多一层
2. **成员表 Avatar 用 themedCircleAvatar block** —— 头像走主题色
3. **角色 Tag** 用主题色填充（白字）—— `<Tag style={{ backgroundColor: primary, color: '#fff', borderColor: primary }}>{role.name}</Tag>`
4. **"+ 添加成员" 后弹 UserAssignmentModal** —— sage 的标准用户分配 Modal 走 Transfer 穿梭框
5. **Models / Core Config Tab 切换不刷新** —— 用 antd Tabs 默认 keep-alive

## 反模式

- ❌ 把 Models / Core Config 拆为独立路由 —— sage 选择"在 Tab 里切"，因为它们都是当前 space 的属性
- ❌ Sidebar 列表 hover 加阴影 —— 跟 active 态混淆，sage 只用 bg/border 双层区分 active vs idle
