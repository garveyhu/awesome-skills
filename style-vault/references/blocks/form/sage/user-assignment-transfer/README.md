---
id: blocks/form/sage/user-assignment-transfer
type: block
name: 用户分配穿梭框
description: 700px Modal · 角色 Radio + 角色筛选 Select + 居中 Transfer 穿梭框（300×350，头像 + 名）+ 自定义全选 label 显示已分配数
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm, serious]
  stack: [react-antd-tailwind]
preview: /preview/blocks/form/sage/user-assignment-transfer
---

# User Assignment Transfer Modal

> sage 把用户分配给角色 / 模型 / 规则集 等的通用弹窗。三段：① 角色单选（可选）② 角色多选筛选 ③ Transfer 穿梭框 —— 三者层层缩窄候选用户范围，最终落到 targetKeys 数组。

## Modal 容器

```jsx
<Modal width={700} destroyOnHidden
  title={title} open={visible}
  onOk={handleOk} onCancel={onCancel}
  okButtonProps={{ disabled: !allowEmpty && targetKeys.length === 0 }}
  confirmLoading={submitting} />
```

内部：`space-y-4 py-2`

## 段 1：角色单选（条件：roleOptions.length > 0）

- 标题：`font-medium text-slate-700` "选择角色"
- `<Radio.Group className="flex gap-4">` 横向排列
- 每条 `<Radio>` + `text-sm` label

## 段 2：角色多选筛选

- 标题：`font-medium text-slate-700` "按角色筛选"
- `<Select mode="multiple" allowClear maxTagCount="responsive" style={{ width: '46%' }} />`
- options 来自 uniqueRoles（去重当前用户列表所有角色）

## 段 3：用户 Transfer

- loading：`flex justify-center py-8` + `<Spin />`
- ready：
  ```jsx
  <Transfer
    pagination={false}
    titles={['未分配', '已分配']}
    targetKeys={targetKeys}
    onChange={setTargetKeys}
    showSearch
    filterOption={(v, item) => item.title.toLowerCase().includes(v.toLowerCase())}
    render={item => <Avatar size="small" backgroundColor={themeHex} src={item.avatar} /> <span>{item.title}</span>}
    styles={{ section: { width: 300, height: 350 } }}
    selectAllLabels={[
      ({ selectedCount, totalCount }) => <span>未分配 {selectedCount}/{totalCount}</span>,
      ({ selectedCount, totalCount }) => <span>已分配 {selectedCount}/{totalCount}</span>,
    ]}
    showSelectAll
    footer={({ direction }) => direction === 'right' && (
      <Button onClick={clearAll} style={{ float: 'left', margin: 5 }}>清空</Button>
    )}
  />
  ```

## 视觉要点

1. **Avatar backgroundColor 走主题色**：所有用户头像一律主题色背景 + size="small"，让 Transfer 列表视觉协调
2. **selectAllLabels 自定义**：原生 Transfer 的"全选"是个 checkbox + 文字，sage 改成"未分配 N/M"格式，更具体
3. **footer 仅 right 方向**："清空"按钮只在已分配那侧显示，避免误操作
4. **width=46%**：角色筛选 Select 占内层一半 —— 表达"过滤是辅助"，不和搜索框等宽抢戏
5. **maxTagCount="responsive"**：标签数量超出时折叠，防止 Select 高度暴增

## 反模式

- ❌ 不要用 antd Form 包整个弹窗 —— Transfer 是受控组件，自己 setState 比 Form 拿值更直接
- ❌ Transfer 不要省略 styles.section 的 width/height —— 默认值会随候选数增加而失控

## 使用上游
- `system/space/pages/ModelConfig` —— 给模型分配可见用户
- `pages/list-table/sage/admin-table-management` —— 给角色批量分配用户
- `pages/form-flow/sage/rule-set-stepper-modal` —— 给规则集分配生效用户（Step 2）
