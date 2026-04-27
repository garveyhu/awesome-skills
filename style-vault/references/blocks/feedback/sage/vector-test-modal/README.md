---
id: blocks/feedback/sage/vector-test-modal
type: block
name: 向量测试检索弹窗
description: 1000px Modal · 用户问题灰盒 + 5 列 stat card 切 tab + 不同 tab 的表格（表/规则/预制 SQL/用户 SQL/低质 SQL）+ 距离 Tag 4 色阶
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [serious]
  stack: [react-antd-tailwind]
preview: /preview/blocks/feedback/sage/vector-test-modal
uses:
  - components/inputs/sage/sql-editor-monaco
---

# Vector Test Modal

> sage 数据源向量库的 debug 工具。输入一个用户问题，向量检索同时跑 5 类资源（表 / 规则 / 预制 SQL / 用户 SQL / 低质 SQL），返回每类的命中条目 + 余弦距离。Modal 上半 5 张 stat card 当 tab 切换，下半根据当前 tab 渲染对应的列结构表格。

## Modal 容器

```jsx
<Modal width={1000} footer={null} maskClosable
  title={<><ThunderboltOutlined /> 向量测试结果 <Popover .../></>}
/>
```

content：`mt-4`

## 用户问题盒

`mb-4 p-4 bg-gray-50 rounded-lg border border-gray-200`：
- 上行：`<UserOutlined />` + `<Text type="secondary">` "用户问题"
- 下行：原始问题文本

## 5 列 stat cards 网格

`grid grid-cols-5 gap-4 mb-6 mt-3`，每张：

```jsx
<Card size="small" hoverable
  className={`cursor-pointer transition-all ${
    isActive ? `${themeClasses.bgLight} border-l-4` : 'border-gray-200'
  }`}
  style={{ borderLeftColor: isActive ? primaryColor : undefined }}
  onClick={() => setActiveTab(type)}
>
  <div className="flex justify-between items-start">
    <div className="flex-1">
      <div className="flex items-center gap-2">
        <div className={`p-2 rounded-lg ${themeClasses.iconBg}`}>{icon}</div>
        <span className="text-xs">{title}</span>
      </div>
      <div className="text-lg font-bold mt-2">{count}</div>
    </div>
    <Badge count={foundCount} color={primaryColor} overflowCount={99} />
  </div>
</Card>
```

5 张卡：
1. **表** `<DatabaseOutlined />` `tables`
2. **规则** `<FileTextOutlined />` `rules`
3. **预制 SQL** `<CodeOutlined />` `prefab`
4. **用户 SQL** `<UserOutlined />` `user`
5. **低质 SQL** `<ExclamationCircleOutlined />` `low_quality`

## 表格区（按 activeTab 切换）

`<Table size="small" pagination={false} scroll={{ y: 400 }} tableLayout="fixed">` —— 5 个 case 各自有自己的 columns：

### 距离 Tag 4 色阶（共用）
```ts
function renderDistanceTag(v: number) {
  const color = v >= 0.5 ? 'red' : v >= 0.3 ? 'orange' : v >= 0.2 ? 'blue' : 'green';
  return <Tag color={color}>{v.toFixed(4)}</Tag>;
}
```

### 各 tab 的 columns
- **tables**：表名 / 注释 / 距离 Tag
- **rules**：rule name / 内容（whitespace-pre-wrap） / 距离
- **prefab**：question / SQL 预览（嵌内联 SqlEditor 200px height）
- **user**：question / SQL / user / 命中次数
- **low_quality**：question / SQL / 反馈原因（red Tag）

## Popover hint

`<Popover title="距离说明" content={<div className="max-w-xs text-xs">距离越小越相近...</div>}>` 包 `<QuestionCircleOutlined className="text-gray-400 cursor-help" />`

## 视觉要点

1. **Stat card 左 4px 主题色边表激活态**：`isActive` 时 `border-l-4` + inline `borderLeftColor: primaryColor` —— 比换整张卡的 background 更克制
2. **iconBg 走 themeClasses.iconBg**：图标背景跟主题色，文字本体保持 slate
3. **Badge overflowCount=99**：用于显"99+"，避免大数撑爆卡片
4. **Tag color 4 阶（绿/蓝/橙/红）**：直接用 antd 预设色 —— 距离强弱直观，不走主题色
5. **scroll.y=400 + tableLayout=fixed**：长列表内部滚，不让 Modal 长得离谱

## 反模式

- ❌ 不要在 Tab 切换时 unmount 表格 —— 用 activeTab + switch 渲染保持一致性能
- ❌ 不要把 stat card 做成普通 chip —— Card hoverable + Badge 让用户感觉是"可点切换"

## 使用上游
- `agents/data-qa/pages/datasource/DataSourceDetail` （Step 3 向量测试按钮触发）

## 内嵌
- `components/inputs/sage/sql-editor-monaco`（prefab/user tab 表格里的 SQL 列）
