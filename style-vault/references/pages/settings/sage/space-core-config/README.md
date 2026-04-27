---
id: pages/settings/sage/space-core-config
type: page
name: 空间核心配置
description: 双列 Form 网格 · 左 7 卡 / 右 4 卡 · Banner Switch + InputNumber + Slider 4 marks · 顶部 Reload + Save loading 操作行
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [serious]
  stack: [react-antd-tailwind]
preview: /preview/pages/settings/sage/space-core-config
---

# Space Core Config Page

> sage 工作空间的核心配置页 —— 数十项参数全在一个滚动页面。两列布局：左 7 卡、右 4 卡 + 右上重置/保存按钮。配置行用 "Banner pattern"（灰底 + 大字 label + 右侧 Switch / InputNumber）保持视觉一致。

## 整体结构

```
ConfigProvider(colorPrimary=themeHex)
└─ div.h-full.bg-neutral-50.overflow-auto.custom-scrollbar
   └─ div.w-full.px-8.py-6
      ├─ Header (flex justify-between items-center mb-8)
      │   ├─ Title "空间配置"
      │   └─ [Reset Btn, Save Btn]
      └─ Conditional: Spin OR Form Grid (2 columns)
```

## Header
- `<Title level={3} style={{ color: '#1e293b' }}>` "空间配置"
- 右：`<Tooltip>` + `<ReloadOutlined>` 重置 + `<SaveOutlined loading={saving}>` 保存

## Form Grid 双列

### 左列 7 卡（gap-1）

每张 `<Card title="..." className="border-neutral-200 shadow-sm">`：

1. **输出配置**：`grid grid-cols-2 gap-6` —— OutputLanguage Select + SqlResultRowLimit InputNumber
2. **AI 功能**（含开关 + 联动禁用）：
   - Banner Switch："开启 AI 标题生成"（aiTitleGeneration）
   - 内部 grid 受开关控制：`transition-opacity ${!enabled ? 'opacity-50 pointer-events-none' : ''}`
3. **对话配置**：Banner（启用 Excel 下载）+ grid 2 列（对话内存上限 / DataQA 上下文上限）
4. **数据分析**：grid 2 列（文本分析采样数 / 图表分析采样数）
5. **模型角色**：Banner Switch（启用自定义角色） + `<Input.TextArea rows={3}>` 角色提示词
6. **安全**：grid 2 列（重试次数 / SQL 执行超时秒）
7. **向量搜索 limits**：grid 2 列 5 项（表 / 规则 / 预制 SQL / 用户 SQL / 低质 SQL）

### 右列 4 卡（gap-2）

1. **Vector limits 重复**（与左 #7 同形态）—— 但放右列分页方便滚动对照
2. **向量阈值**：5 个 `<Slider min={0} max={1} step={0.05} marks={THRESHOLD_MARKS} />`
3. **向量化开关**：2 Banner（点赞 SQL 入库 / 反馈 SQL 入库）
4. **查询重写**：Banner Switch + 改写次数 InputNumber

## 关键 Pattern：Banner

Switch 类配置统一长这样：

```jsx
<div className="px-4 py-3 bg-neutral-50 rounded-lg flex items-center justify-between">
  <div>
    <span className="font-medium text-neutral-700">开启 AI 标题生成</span>
    <p className="text-xs text-neutral-500 mt-0.5">大模型自动总结对话首条问题为标题</p>
  </div>
  <Switch checked={...} onChange={...} />
</div>
```

## Slider with Marks

```js
const MARKS = { 0: '0', 0.2: '0.2', 0.5: '0.5', 1: '1' };
<Slider min={0} max={1} step={0.05} marks={MARKS} />
```

## 视觉要点

1. **左 7 / 右 4 不平衡**：左列堆 SQL/AI 主功能，右列放向量参数 —— 让"主常用 + 高级调优"视觉分组
2. **Banner pattern 复用**：所有 Switch 都包成 `bg-neutral-50 rounded-lg` 灰盒，区别普通 Form.Item
3. **联动禁用 opacity-50 pointer-events-none**：开关关闭时下游字段灰掉但不消失，让用户知道配置项的依赖关系
4. **Slider marks 4 节点**：0 / 0.2 / 0.5 / 1，标 4 个对应"无关 / 弱 / 中 / 满"语义
5. **`text-neutral-700` 标题色**：不用 slate，配 bg-neutral-50 灰盒一致

## 反模式

- ❌ 不要把所有配置塞进一列 —— 左右双列 + 卡片分组让滚动距离减半
- ❌ 不要直接 `<Form>` 不分卡 —— 卡片分组 + 标题标 section 必不可少
- ❌ Reset 不要直接执行 —— 必须 `Modal.confirm okType="danger"` 防止误操作

## 使用上游
- `core/components/layout/MainLayout`（admin 路由 `/space/:id/config`）
