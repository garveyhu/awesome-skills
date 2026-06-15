---
id: pages/form-flow/sage/rule-set-stepper-modal
type: page
name: 规则集分步弹窗
description: 1200px 大弹窗 + Steps + 双段（规则配置 / 用户分配）+ 嵌套 Card + Transfer 用户穿梭框
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm, serious]
  stack: [react-antd-tailwind]
uses:
  - blocks/layout/sage/management-layout-header
preview: /preview/pages/form-flow/sage/rule-set-stepper-modal
---

# Rule Set Stepper Modal

> sage `/admin/rules` 的核心：表格 + "+ 新建/编辑"弹窗。弹窗用 1200px 宽 antd Modal + 顶部 Steps（规则配置 / 用户分配）+ 嵌套 Card 嵌套 Card 的密集表单 + 第二步 Transfer 穿梭框分配用户。**关键**：Card 内 Card，3 级嵌套（基础信息卡 → 规则列表卡 → 添加规则表单卡）。

## 页面骨架

### 表格页（外层）
- `<ManagementLayout title="规则管理" onSearch={...} themeColor={themeColor} rightActions={<Button type="primary" icon={<Plus className="w-4 h-4"/>} onClick={handleAdd} className={tc.bg}>新建</Button>}>`
- 内部：`<Table columns={columns} dataSource={ruleSets} rowKey="id" pagination={{ showSizeChanger: true, showTotal }} size="middle" />`
- 列：ID / 名称（FolderOpen icon themed + description 副行） / 规则数 Tag（主题色填充） / 启用 Switch / 创建时间 / 操作（Settings / Users / Trash2 三按钮）

### 弹窗（核心）
- `<Modal title="新建规则集 / 编辑规则集" width={1200} onCancel={...} styles={{ body: { padding: '24px', maxHeight: '70vh', overflowY: 'auto' } }} footer={...}>`

#### 步骤指示
- `<Steps current={currentStep} onChange={setCurrentStep}` `items={[{ title: '规则配置', icon: <Layers /> }, { title: '用户分配', icon: <Users /> }]} />`

#### Step 1 · 规则配置
- 隐显：`<div className={`flex flex-col gap-2 ${currentStep === 0 ? '' : 'hidden'}`}>`
- **嵌套 Card #1**：`<Card title="基本信息" size="small">` + `<Form layout="vertical">` 内 grid-cols-2：name + description
- **嵌套 Card #2**：`<Card title="规则列表" extra={<Tag style={{ backgroundColor: primary, color: '#fff' }}>{rules.length}</Tag>} size="small">`
  - 空：`<Empty description="还未添加规则" />`
  - 有：`<div className="space-y-2">` 每条 `<div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg border" style={{ borderColor: primary }}>` + 行/列 Tag + 名 + 数据源/表 副 + 编辑/删除 Button
- **嵌套 Card #3**：`<Card title="添加规则 / 编辑规则" extra={editingRule && <Button type="link">取消编辑</Button>} size="small">`
  - 4 列 grid：name / type Select (行/列) / 数据源 Select / 表 Select
  - `selectedTableId &&` 条件下显 `<RuleBuilder ruleType fields value onChange showVariablePanel={false} />`（这是另一组件，承载行/列规则的 visual builder）
  - 末尾 "+ 添加" 按钮

#### Step 2 · 用户分配
- 隐显：`<div style={{ display: currentStep === 1 ? 'block' : 'none' }}>`
- `<Card title="选择用户" size="small">` 
  - 描述 + Spin loading + 居中 `<Transfer dataSource={allUsers} titles={['未分配', '已分配']} targetKeys={selected} showSearch render={item => <Avatar+name>} styles={{ section: { width: 280, height: 300 } }} showSelectAll />`
  - 底部 `<div className="mt-4 text-gray-400 text-xs text-center">` 已分配 N 人

#### Footer
- 左：`{currentStep > 0 && <Button>上一步</Button>}`
- 右：`<Space>` 取消 / 下一步（step 0）/ 保存（step 1）

## 视觉要点

1. **Card 三级嵌套** —— 基础信息 / 规则列表 / 添加规则各占独立卡片，视觉清晰但密度高
2. **行/列规则 Tag 双色**：行规则用 primaryColor；列规则用 hardcoded `#9850fdff`（紫色）—— 唯一不走主题的颜色对，固定区分两种规则类型
3. **规则项 borderColor inline 注入 primaryColor** —— 让选中态/列表项跟随主题
4. **Transfer 居中**：`<div className="flex justify-center"><Transfer ... /></div>`，sage 用 antd Transfer 默认样式
5. **width=1200** —— 是 antd Modal 默认 520 的 2.3 倍，强调"这是个复杂表单，给我空间"

## 反模式

- ❌ Step 切换用 conditional render（unmount/mount） —— sage 用 className hidden / display none，保留 form state
- ❌ 把"添加规则"和"规则列表"合并 —— 编辑某一条时需要同时看其它条目作上下文
