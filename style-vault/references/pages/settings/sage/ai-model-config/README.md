---
id: pages/settings/sage/ai-model-config
type: page
name: AI 模型配置
description: 4-view 状态机 · list（卡片网格）/ supplier-select（4×5 logo 网格）/ config-form（双列 Form）/ edit · view 间用 Steps 进度指示，Form 不 unmount 保留状态
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm, serious]
  stack: [react-antd-tailwind]
preview: /preview/pages/settings/sage/ai-model-config
uses:
  - blocks/form/sage/user-assignment-transfer
---

# AI Model Config Page

> sage 系统级模型管理。一个组件文件 + 4 个 view 状态切换：① list（已配模型卡片网格）② new_select_supplier（选 OpenAI / DashScope / Anthropic 等供应商）③ new_config（填 baseModel / apiKey 等）④ edit_config（同 ③ 但带 id）。view 切换不 unmount Form。

## View 1：list

容器：`p-6 h-full overflow-auto custom-scrollbar`

### Header
- `flex justify-between items-center mb-6`
- 左：`<Title level={3} style={{ color: '#1e293b' }}>` "模型管理"
- 右：`flex gap-3`
  - `<Select width={140}>` 模型类型筛选（LLM / Embedding / Audio）
  - `<Input prefix={<SearchOutlined />} width={200}>` 关键词
  - `<Button type="primary" icon={<PlusOutlined />}>` "新建模型"

### 卡片网格
- `grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5`
- 每张：`bg-white rounded-xl p-5 cursor-pointer hover:shadow-lg relative group border` + 动态 `borderColor: primaryColor || '#e2e8f0'`
- onMouseEnter/Leave 切 `hoveredCard`

#### 卡片内容
- 头：`flex items-start gap-3 mb-3` —— 32×32 supplier logo + name + 副标
- Tag：`color="blue|purple|orange"` 按 modelType（不走主题色，区分类型）
- Hover 浮层：`absolute top-2 right-2 flex gap-1 bg-white/95 backdrop-blur-sm rounded-lg p-1 opacity-0 group-hover:opacity-100`
  - 5 个按钮：`<UserOutlined>`（分配用户）/ `<StarOutlined>`（设默认）/ `<EditOutlined>` / `<StopOutlined / PlayCircleOutlined>` / `<DeleteOutlined>`

### 空状态
`flex flex-col items-center justify-center h-64 bg-white rounded-xl border border-slate-200 + DatabaseOutlined fontSize=48 + Empty`

## View 2：new_select_supplier

- Header：`<Button icon={<ArrowLeftOutlined>}>` 返回 + Title "选择供应商"
- Steps 进度：`renderSteps(0)` —— 自定义实现，圆点 + 主题色填充 + 连线
- 4×5 网格：`grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4`
- 卡片：`bg-white hover:bg-slate-50 border border-slate-200 hover:border-blue-400 rounded-xl p-6 h-[180px] group`
- 内：64×64 logo `<div className="w-16 h-16 rounded-2xl bg-white border border-slate-100 p-2 shadow-sm group-hover:scale-110">` + name

## View 3 / 4：config-form

容器：`p-6 h-full flex flex-col` + Steps `renderSteps(1)`（current=1）

3 张卡 stack：

### 基础信息
`bg-white p-6 rounded-xl border border-slate-100 mb-6 shadow-sm`
- `grid grid-cols-2 gap-4`：name / modelType Select / baseModel Select（showSearch）

### API 配置
- 同上 bg/border/radius
- apiDomain `<Input>` + apiKey `<Input.Password>`

### 自定义参数
`bg-slate-50 p-6 rounded-xl border border-slate-200/60 mb-6`
- 多行 key-value：`<Input>` + `<Input>` + `<Button icon={<DeleteOutlined>}>`

### Footer
`absolute bottom-0 left-0 right-0 px-6 py-4 pt-4 border-t border-slate-100 flex justify-end gap-3 bg-white/80 backdrop-blur-sm`
- 取消 + Primary（"创建" / "保存"）loading

## 视觉要点

1. **4-view 状态机不路由**：`viewMode` state 切换 + Form `useForm()` 在 view 2/3/4 间不 unmount，保留输入
2. **Tag color 按 modelType 硬编码**：blue=LLM / purple=Embedding / orange=Audio，不走主题色 —— 让用户快速识别类型
3. **hover 浮层 backdrop-blur-sm**：白底半透明 + 模糊，让 5 个 icon 浮在卡片上不挡内容
4. **rounded-2xl logo 容器**：16px 大圆角的 64px 容器 + group-hover:scale-110，呼应 supplier brand guidelines（多数 logo 是圆角矩形）
5. **Steps 自实现不用 antd**：`renderSteps(currentIdx)` 自定义圆点 + 主题色，避免 antd Steps 默认配色不跟主题

## 反模式

- ❌ 不要把 4 view 拆 4 个 component file —— state 切换比 router 切换快、保 Form
- ❌ Footer 不要 absolute 之外的方案 —— 模型创建的"操作行"必须钉底，对长表单极重要
- ❌ Tag 颜色不要走主题色 —— modelType 是分类不是状态

## 使用上游
- `core/components/layout/MainLayout` （admin 路由 `/admin/models`）

## 内嵌
- `blocks/form/sage/user-assignment-transfer`（点 `<UserOutlined>` 触发）
