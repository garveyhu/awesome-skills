---
name: style-vault
description: >
  Personal frontend component style library (React + Ant Design + Tailwind CSS).
  Use when: creating UI components, tables, forms, toolbars, cards, modals,
  or any frontend element that should match personal style preferences.
  Triggers: "用我的风格", "按照我的样式", "style-vault", "组件样式",
  building admin panels, dashboards, management interfaces,
  or when the user asks to make UI look good / match existing style.
---

# Style Vault

## 技术栈

React + Ant Design + Tailwind CSS

## 使用方式

### 场景一：新项目初始化

读取 tokens/ 下的全局设计 token，再根据页面需求从 composites/ 和 atoms/ 中挑选组件，批量生成符合风格的基础组件集。

### 场景二：日常开发

需要某个组件时，查阅对应的组件文件，直接使用核心代码，根据样式要点和 Ant Design 覆盖配置调整细节。

### 场景三：沉淀新组件

用户对当前组件样式满意后，按下方维护指南的格式规范新增条目。

---

## 维护指南

> 本节面向所有对话中的 AI 助手。任何 AI 在任何对话中都可以按此规范维护本样式库。

### 三层分类

| 目录 | 说明 | 举例 |
|------|------|------|
| `references/atoms/` | 有独立风格的单个元素 | 按钮、Tag、输入框、分页器 |
| `references/composites/` | 多个元素的场景级组合 | 表格+分页+工具栏、数据卡片组 |
| `references/tokens/` | 全局设计变量 | 间距体系、配色偏好、字号层级 |

### 收录原则

- **收录**：用户明确满意的、经过反复调试确认的风格
- **不收录**：临时方案、未经用户确认的试验、一次性 hack

### 单组件文件格式

每个组件一个 `.md` 文件，格式如下（没有的部分直接省略）：

~~~
# 组件名

> 一句话描述用途和场景

## 技术栈

React + Ant Design + Tailwind CSS

## 预览效果

(文字描述视觉效果和关键样式特征)

## 核心代码

```tsx
// 完整的可复用组件代码
```

## 样式要点

- 要点：记录"为什么这样写"，不只是"是什么"

## Ant Design 覆盖

```tsx
// ConfigProvider theme 覆盖配置（如果有）
```

## 使用示例

```tsx
// 在页面中如何使用
```
~~~

### 新增组件流程

1. 确认用户对组件样式满意
2. 判断归入 atoms / composites / tokens 哪个分类
3. 在对应目录下创建 `组件名.md`，按上方格式填写
4. 更新本文件的「组件索引」表
5. 核心代码必须是可直接复制使用的完整组件
6. Ant Design 覆盖（ConfigProvider theme + CSS override）单独列出

---

## 组件索引

### 全局 Token

| 文件 | 内容 |
|------|------|
| *(暂空，后续积累)* | |

### 场景组合

| 文件 | 内容 |
|------|------|
| [composites/admin-table.md](references/composites/admin-table.md) | 管理后台表格：无边框、统一分页、中文本地化、行 hover 减淡 |
| [composites/admin-toolbar.md](references/composites/admin-toolbar.md) | 表格工具栏：搜索+筛选左对齐、功能按钮右对齐 |

### 原子组件

| 文件 | 内容 |
|------|------|
| *(暂空，后续积累)* | |
