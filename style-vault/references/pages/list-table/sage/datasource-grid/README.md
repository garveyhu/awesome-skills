---
id: pages/list-table/sage/datasource-grid
type: page
name: 数据源网格页
description: 4 列 datasource card 网格 + filter + add，合并 list / new / detail 三路由的统一外壳
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm]
  stack: [react-antd-tailwind]
uses:
  - blocks/display/sage/datasource-card
  - blocks/feedback/sage/spin-fullscreen-loader
preview: /preview/pages/list-table/sage/datasource-grid
---

# Datasource Grid

> sage `/datasource` + `/datasource/new` + `/datasource/:id` 三路由共用的外壳。list 模式：grid card 网格 + 类型 filter + 关键词 search + "+ 新建"按钮；new 模式：表单（DataSourceNew）；detail 模式：表 + 字段（DataSourceDetail）。视觉模板由 list 主导，new/detail 是同布局的内容替换。

## 页面骨架（list 模式 · 主形态）

1. **整页**：`p-6 h-full overflow-auto`（在 admin overlay 内是 `pt-10`）
2. **顶栏** `flex justify-between items-center mb-6`
   - **左**：`<Title level={3} margin: 0 color: '#1e293b' />` "数据源" + `<Text type="secondary">` 副标
   - **右**：`flex gap-3`
     - 类型 Select `w-[140px]`（动态 typeOptions = unique types）
     - 关键词 Input `w-[200px]` 带 Search prefix
     - "+ 新建" Antd Button type="primary"（colorPrimary 走 themeHex）
3. **未选空间提示**：`<Alert type="warning" showIcon />`（"请先选择空间"）
4. **空状态**：`flex flex-col items-center justify-center h-64 bg-white rounded-xl border border-slate-200 + DatabaseOutlined fontSize 48 color #94a3b8 + Empty description`
5. **Grid 区**：`grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5`，每条 = `<DatasourceCard>` block
6. **QuickQuestionConfigModal**（条件渲染）—— 设置数据源的快捷提问模板

## new / detail 模式

- **/datasource/new**：表单标题 "新建数据源" + Form（type / 名称 / host / port / username / password / database / 描述 + 测试连接 + 保存）+ 取消 / 保存按钮
- **/datasource/:id**：表分组（顶部数据源信息卡 + tab：表列表 / 字段管理 / 同步设置）

## 视觉要点

1. **logo 36×36**（不是 48）—— 卡片紧凑感，sage 整体偏 dense
2. **默认 tag** 用 emerald 50/700/200 三阶 + `[10px]` 角标 —— "默认"是关键状态但不能抢戏
3. **类型 Filter Select 用 antd 默认 size**（不 small）—— 跟 search input 视觉对齐
4. **"+ 新建" 按钮用 antd Button type="primary"** —— 不自己写 Tailwind，让 ConfigProvider 接管色
5. **整个页面包在 ConfigProvider** `theme={{ token: { colorPrimary: themeHex } }}` —— 但 ant Title 颜色是 inline style 强制 #1e293b（不让主题影响标题字色）

## 反模式

- ❌ list / new / detail 三路由各写一套外壳 —— 视觉会漂移；sage 把三者合并成一个 card-grid 模板
- ❌ 数据库 logo 用 lucide Database 通用图标 —— 失去"我连接的是 mysql 还是 postgres"的视觉差异
