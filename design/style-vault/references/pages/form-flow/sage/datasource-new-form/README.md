---
id: pages/form-flow/sage/datasource-new-form
type: page
name: 新建数据源（4 步表单）
description: 4-step Wizard · ① 类型选择（Radio.Button 网格 + developing 灰态）② 连接（host/port/proxy 条件分支）③ 表选择（Transfer + 通配符 *? 批量）④ 确认。Form 始终 mounted（display:none 切换），保留输入
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm]
  stack: [react-antd-tailwind]
preview: /preview/pages/form-flow/sage/datasource-new-form
---

# DataSource New Form (4-Step Wizard)

> sage 创建数据源的引导。4 步固定流程：类型 → 连接 → 选表 → 确认。Form 全程 mount 用 `display: none` 切换 step，保留所有字段值（绕过用户填到一半切回又重填的痛）。表选择步骤支持通配符（`*` 任意 / `?` 单字符）批量勾选。

## 整体外壳

```jsx
<ConfigProvider>
  <div className="p-6 h-full overflow-auto">
    <Header (back + Title "新建数据源") />
    <Card>
      <Steps current={step} className="mb-6"
             items={[类型, 连接, 选表, 确认]} />
      <Form layout="vertical" form={form}>  {/* 始终 mount */}
        <div style={{ display: step === 0 ? 'block' : 'none' }}><Step0 /></div>
        <div style={{ display: step === 1 ? 'block' : 'none' }}><Step1 /></div>
        <div style={{ display: step === 2 ? 'block' : 'none' }}><Step2 /></div>
        <div style={{ display: step === 3 ? 'block' : 'none' }}><Step3 /></div>
      </Form>
      <Footer (上一步 / 下一步 / 提交) />
    </Card>
  </div>
</ConfigProvider>
```

## Step 0：类型选择

`<Radio.Group className="w-full">` + Row gutter=24
- 每个 Radio.Button：`height: 96, display: flex flex-col items-center justify-center`
- 内容：`<img className="w-8 h-8 object-contain">` + `<div className="mt-1">` 类型名
- 已支持类型：mysql / postgresql / oracle / kingbase / dm
- 开发中类型：`opacity: 0.6` + `<Tag color="processing">developing</Tag>`
- 选中：inline `borderColor: primaryColor, color: primaryColor`

## Step 1：连接

条件分支字段（按 selectedType 切换）：
- sqlite：仅一个 `<Input>` 数据库文件路径
- 其它：host / port / user / password / database / schema
- 部分类型：
  - dm：无 database 字段
  - oracle：connectMode Radio（service_name | sid）+ Service Name label 替代 Database
  - sqlserver / postgresql / kingbase / dm：显 schema
- proxy 模式（kingbase / mysql 部分场景）：Switch + proxy_url + proxy_api_key

底部：`<Button>` 测试连接 + 测试结果（绿√/红×）

## Step 2：选表

容器：`flex flex-col gap-4 max-w-[800px] mx-auto`

### Pattern 控制条
`flex gap-2 items-center p-3 bg-gray-50 rounded-lg border border-gray-100`：
- `<span className="text-gray-600 font-medium whitespace-nowrap">` "通配符"
- `<Input placeholder="如 user_*" />`
- 全选匹配 / 取消匹配 两个 Button
- 末：`<span className="ml-auto text-xs text-gray-400">` "* 任意 / ? 单字符"

isMatch logic：
```js
new RegExp('^' + pattern.split('*').join('.*').split('?').join('.') + '$', 'i').test(text)
```

### Transfer
- 居中 `flex justify-center`
- `dataSource={tables.map(n => ({ key: n, title: n }))}`
- titles: `["未选 (N)", "已选 (M)"]`
- listStyle: `{ width: 350, height: 400 }`
- showSearch

## Step 3：确认

居中 `py-4 text-center`：
- 大 DatabaseOutlined `fontSize: 64`
- 三 Card `Row gutter=[16,16]` 摘要：类型 / 连接 / 已选表数 + Tag

## Footer

`flex justify-between items-center mt-6`：
- 左：`<Button>` 上一步（step > 0 才显）
- 右：`<Button type="primary" loading={...}>` 下一步 / 创建（step 3）

## 视觉要点

1. **Form 永远 mount + display 切换**：用户切回某步表单数据完整保留
2. **Radio.Button 卡片 96px**：高于普通 Radio 让 logo + 文字两行 ok 排
3. **developing 灰态 + Tag**：让用户清楚未实装类型不能选
4. **Pattern 灰盒**：放在 Transfer 上方独立段，不混进 Transfer 内部
5. **Step 验证守卫**：进 Step 1→2 必须 testResult==='success'，否则按钮禁用 —— 防止填错连接进选表

## 反模式

- ❌ 切 step 不要 unmount —— 保留 form state 是首要原则
- ❌ 通配符不要做正则 —— 普通用户不懂 regex，*/? 已足够
- ❌ developing 不要做"敬请期待"弹窗 —— 直接 disable + 灰底已经够了

## 使用上游
- `pages/list-table/sage/datasource-grid` （"+ 新建" 按钮入口）
