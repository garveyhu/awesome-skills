---
id: pages/detail/sage/datasource-detail-tabs
type: page
name: 数据源详情三 tab
description: 顶部 ManagementLayout 头 + Card 内 Steps（连接信息 / 元数据 / 向量训练）3 步切换 · 异步任务（同步 / 训练）轮询 + 进度条
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm, serious]
  stack: [react-antd-tailwind]
preview: /preview/pages/detail/sage/datasource-detail-tabs
uses:
  - blocks/feedback/sage/vector-test-modal
  - components/inputs/sage/sql-editor-monaco
---

# DataSource Detail (3-Step Tabs)

> sage 单个数据源的详情 + 操作页。`p-6 h-full overflow-auto` + Card 内部 antd `<Steps>` 把三段流程串起来：① 连接信息 ② 元数据（表/字段同步）③ 向量训练。每一步对应一个独立子组件，所有异步任务（同步表 / 训练向量）走任务 ID 2s 间隔轮询。

## 整体外壳

```jsx
<ConfigProvider theme={{ token: { colorPrimary: themeHex } }}>
  <div className="p-6 h-full overflow-auto">
    <Header />
    <Card>
      <Steps current={currentStep} onChange={setStep} items={[…3 step…]} />
      {step === 0 && <Connection />}
      {step === 1 && <Metadata />}
      {step === 2 && <Vector />}
    </Card>
    <TableDetailDrawer / VectorTestModal / AddTableModal />
  </div>
</ConfigProvider>
```

## Header

`flex justify-between items-center mb-6`：
- 左：`<Button icon={<ArrowLeft />}>` 返回 + DatabaseOutlined + Title (`color: '#1e293b'`) + Tag（数据源类型 mysql/oracle/...）
- 右：占位，主操作按钮在 Steps 内

## Steps

`<Steps current={currentStep} onChange={setStep}` `items={[
  { title: '连接信息', icon: <CloudSyncOutlined /> },
  { title: '元数据', icon: <DatabaseOutlined /> },
  { title: '向量训练', icon: <ThunderboltOutlined /> },
]}>`

step 切换不 unmount 子组件 —— 但通常用 if/else 渲染（保留上次操作消息）

## Step 0：Connection

`<DataSourceConnection>` 子：
- Form 双列：host / port / user / password / database / schema
- 操作行：测试连接（绿√/红×反馈）+ 保存

## Step 1：Metadata

`<DataSourceMetadata>`：
- 顶部操作行：`<Button icon={<CloudSync>}>` 同步元数据（异步任务）+ `<Button icon={<PlusOutlined>}>` 添加单表
- 进度横幅（异步态）：`<Alert>` "同步中：50/200 ..."
- 表列表 antd Table：表名 / 注释 / 字段数 / 同步状态 / 操作（详情 Drawer / 删除）

## Step 2：Vector

`<DataSourceVector>`：
- `<Button icon={<Thunderbolt>}>` 训练向量（异步任务） / 仅训练未训练
- 进度横幅（异步态）：`<Alert>` "训练中：30/200 表完成 ..."
- `<Button icon={<Search>}>` 向量测试 → 触发 `<VectorTestModal>`

## 异步任务模式

```js
syncMetadataAsync()
→ 收到 taskId
→ setInterval 2s: getTaskStatus(taskId) → 更新 progress %
→ 完成（或超时 30min）取消 setInterval + Toast
```

## 视觉要点

1. **Steps 不路由**：步骤切换是 state，不改 URL —— 让用户在三步间快速跳跃
2. **icon 在 Steps 上而非 button**：每步用 antd icon 标识动作类型（云同步 / 数据库 / 闪电）
3. **Tag 标数据源类型**：紧跟标题展示 mysql / oracle —— 让用户知道当前 schema 风格
4. **Alert 横幅做进度**：异步任务进行中页面顶部 Alert + 进度数字 + 不阻塞操作其它步骤

## 反模式

- ❌ 不要 unmount Steps 内子组件 —— 切换 step 后回来时同步状态会丢失
- ❌ 不要把异步任务做同步 await —— 同步元数据动辄 1-30 分钟，必须任务 ID + 轮询

## 使用上游
- `pages/list-table/sage/datasource-grid`（点卡片进入 `/datasource/:id`）

## 内嵌
- `blocks/feedback/sage/vector-test-modal`（向量测试触发）
- `components/inputs/sage/sql-editor-monaco`（表详情 Drawer 内嵌只读 DDL）
