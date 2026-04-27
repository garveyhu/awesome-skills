---
id: pages/detail/style-vault/sidebar-preview-detail
type: page
name: 侧栏 + 预览 详情页
description: 面包屑 → 340px 左侧栏（meta 标题 + 复制 Prompt + 平台/主题 chip + tags + 关联组分组折叠）+ 右列 browser-chrome 预览框
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
preview: /preview/pages/detail/style-vault/sidebar-preview-detail
---

# Sidebar Preview Detail

> Style Vault 单条 item（token / component / block / page / style）详情页骨架。和 `sticky-toc-product` 区分：那个是 product 聚合页（masonry 全展），本条是单 item 钻取（sidebar + preview）。

## 视觉特征

```
┌──────────────────────────────────────────────┐
│ 面包屑 · 白底 + 1px slate-100 切割（h-44）     │
│  ← 返回   /   组件   /   深色胶囊主 CTA       │
├──────────────────────────────────────────────┤
│ ┌─────────────┬────────────────────────────┐ │
│ │ 340px       │ Viewport Select + 全屏预览  │ │
│ │ aside       │                            │ │
│ │             │ ┌───────────────────────┐  │ │
│ │ Tag         │ │ ◯◯◯  浏览器 chrome    │  │ │
│ │ Title 32    │ ├───────────────────────┤  │ │
│ │ Desc        │ │                       │  │ │
│ │             │ │  PreviewComp          │  │ │
│ │ [复制 Prompt] │  （按视口 max-width 缩） │  │ │
│ │             │ │                       │  │ │
│ │ Web · 浅色   │ └───────────────────────┘  │ │
│ │             │                            │ │
│ │ Tags 三段    │                            │ │
│ │  · 风格      │                            │ │
│ │  · 氛围      │                            │ │
│ │  · 技术栈    │                            │ │
│ │             │                            │ │
│ │ 依赖 (5)     │                            │ │
│ │  ▾ 原语 4    │                            │ │
│ │   • ...      │                            │ │
│ │  ▾ 模块 1    │                            │ │
│ │ 被引用 (2)   │                            │ │
│ │  ...         │                            │ │
│ └─────────────┴────────────────────────────┘ │
└──────────────────────────────────────────────┘
```

### 面包屑（白底独立条）

容器 `border-b border-slate-100 bg-white`，内部 `mx-auto max-w-[1600px] flex items-center gap-4 px-8 py-3 text-[13px]`：

- `← 返回` 按钮：`flex items-center gap-1 text-slate-500 hover:text-slate-900` —— `<ArrowLeftOutlined />` 配合
- `/` 分隔：`text-slate-300`
- type 文字：`text-slate-500`（如"组件"）
- item 名：`font-medium text-slate-900`（如"深色胶囊主 CTA"）

### 左 sidebar（340px 固定，**不 sticky**）

`<aside className="w-[340px] shrink-0">`，内部 `space-y-8` —— **故意不 sticky**：避免长 page detail 时滚到底部右列还在跑而左列贴顶造成"粘滞感"。Editorial 节奏要求左右**同步滚动**。

#### 标题块

- 顶行：antd `<Tag color={typeColor[type]} bordered={false}>` 极简彩 tag + `FavoriteButton`（爱心 icon）
- h1 `font-display text-[32px] font-bold leading-[1.15] tracking-[-0.03em]`
- 描述 `text-[14px] leading-relaxed text-slate-600`

#### 主 CTA · 复制 Prompt（描边幽灵）

走 `components/buttons/style-vault/ghost-bordered-cta`，**fullWidth**：
```tsx
<button className="ghost-bordered-cta w-full">
  <CopyOutlined /> 复制 Prompt
</button>
```

#### 平台 / 主题 chip

- 平台：`bg-slate-900 text-white px-2 py-0.5 rounded-md text-[11px] font-medium` —— **小黑标**
- 主题：`border border-slate-200 text-slate-600 px-2 py-0.5 rounded-md text-[11px]` —— 白底浅描边
- 多个 platform 时并排，gap-1.5

#### Tags 紧凑网格

三段：风格 / 氛围 / 技术栈。每段 layout：
- 左 `w-14 shrink-0 pt-0.5 text-[11px] font-semibold uppercase tracking-wider text-slate-400` 段标签
- 右 `flex flex-wrap gap-1.5` 包含 chips：`rounded-md bg-slate-100 px-2 py-0.5 text-[12px] text-slate-700`

#### 关联组（依赖 / 被引用）—— 分组折叠

按 `type` 分组（product/style/page/block/component/token），每组：
- 组 header：`flex justify-between rounded-md px-1 py-1 text-[11px] font-medium text-slate-500 hover:bg-slate-50`
  - 左 type-dot + type 中文 + 数量徽章
  - 右 `<DownOutlined>` 旋转 -90° 表收起
- 默认每组只展前 4 项（`PER_GROUP_COLLAPSE = 4`），多余通过"展开剩余 N 项"折叠
- 每条目卡片 `<RelatedItem>`：`flex gap-3 rounded-xl bg-slate-50/60 px-3 py-2.5 hover:bg-white hover:border-slate-200`

### 右列：viewport 工具条 + browser chrome

直接套 `blocks/layout/style-vault/browser-chrome-frame`，无变化。

## 适配指南

- 整页容器 `mx-auto flex max-w-[1600px] gap-10 px-8 py-10` —— left/right 之间 `gap-10`（40px）
- aside 不要加 sticky —— 编辑式节奏要求双列同步滚动；详情页本身不长（描述 + tags + 关联组通常 < 800px）
- 关联组**必须按 type 分组**而不是统一一个长列表 —— Style Vault 的核心价值就是 6 层语义清晰，详情页正是教育用户这件事的场所
- **每组超过 `PER_GROUP_COLLAPSE = 4` 项**自动收起；点 type header 整组收起；**两套独立交互**（不互锁）
- 复制 Prompt 成功要触发 `spring-toast` —— success kind + "Prompt 已复制"

## 反模式

- 不要把 sidebar 改成 sticky —— 长 page 时右列预览滚远，左 sidebar 贴顶有粘滞感
- 不要把关联组合并为单列表 —— 失去层级语义
- 不要把"复制 Prompt"换成 dark-pill —— 它是次要操作，不是 hero CTA（dark-pill 留给"进入风格库"这种主路径）
- 不要在 breadcrumb 加路径深度（多级）—— Style Vault 的 IA 是扁平的（只有 type → name 两级）
- 不要给 chip / tag 加 hover 高亮 —— 它们是只读元数据，不是交互链接
