---
id: blocks/form/sage/row-column-rule-builder
type: block
name: 行/列规则可视化构造器
description: ruleType=row 走嵌套条件树（VisualRuleTree），ruleType=column 走字段卡网格（每卡含启用开关 + 脱敏策略 Select），双形态在同一组件内 if-else
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [serious]
  stack: [react-antd-tailwind]
preview: /preview/blocks/form/sage/row-column-rule-builder
---

# Row / Column Rule Builder

> sage 业务规则的两种形态可视化：行规则（WHERE 条件树）和列规则（按字段配置脱敏 + 启用）。同一组件 `<RuleBuilder ruleType="row|column">`，根据 `ruleType` 走两条完全不同的渲染路径。

## ruleType="row" 路径

- 容器：`flex gap-4`
- 左 `flex-1`：`<VisualRuleTree value fields onChange />` 嵌套 AND/OR 树
- 右 `w-72 flex-shrink-0`（条件 `showVariablePanel`）：`<SystemVariablePanel />` 系统变量列表（点选注入到当前条件值）

## ruleType="column" 路径（ColumnRuleBuilder 子组件）

### 批量操作栏
- `flex gap-2 mb-4`
- `<Button size="small">` 全部启用 / 全部禁用 + `text-sm text-gray-500 ml-2` 提示文案

### 字段网格
- `grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2`
- 每个字段一张 `<Card size="small">`：
  - 启用：`border-green-300 bg-green-50`
  - 禁用：`border-red-300 bg-red-50 opacity-60`
  - 整卡 `cursor-pointer` onClick 切换启用
- 卡内：`flex items-center justify-between gap-2`
  - 左：`flex-1 truncate`
    - 字段名：`font-medium text-sm truncate`
    - 字段注释：`text-xs text-gray-500 truncate`（条件）
  - 右：状态点 `w-3 h-3 rounded-full bg-green-500 / bg-red-500`
- **脱敏策略 Select**（仅启用态显示）：
  - `mt-2`，`onClick={(e) => e.stopPropagation()}` 阻止冒泡（不让点击 Select 切换启用态）
  - `<Select size="small" style={{ width: '100%' }} placeholder="不脱敏" allowClear>`
  - options 来自 `maskStrategyApi.list()` 接口，每条 `{ label: displayName, value: id }` + 一行 `text-xs text-gray-500` 给 example

### 空状态
- `text-center text-gray-500 py-8` "暂无字段"

## 视觉要点

1. **绿/红双色态**：启用 `border-green-300 bg-green-50`，禁用 `border-red-300 bg-red-50 + opacity-60` —— 双色对比能让用户一眼看出哪些字段开了
2. **状态点 12px**：绿/红 1×1 实心圆，`flex-shrink-0` 防止被字段名挤压
3. **stopPropagation 阻止冒泡**：Select 嵌在卡内但不能触发卡的 onClick（卡 click 切启用态）—— 是个常见 trap
4. **行规则 / 列规则不同色板**：行规则走主题色（primary），列规则用绿 / 红硬编码 —— 因为列规则的"启用 / 禁用"是布尔语义，绿红比主题色更直观

## 反模式

- ❌ 不要把行规则和列规则拆成两个组件文件 —— 调用方都用 `<RuleBuilder ruleType=...>`，统一入口
- ❌ 列规则 Select 不要用 `e.stopPropagation` 之外的方法（如 onClick capture）—— stopPropagation 最干净
- ❌ 不要给 `border-green-300` 加 hover 态变绿（如 hover:border-green-400）—— 启用状态本身就是绿，再 hover 反馈不明显

## 使用上游
- `pages/form-flow/sage/rule-set-stepper-modal` —— 步骤 1 内嵌，行/列各一份
