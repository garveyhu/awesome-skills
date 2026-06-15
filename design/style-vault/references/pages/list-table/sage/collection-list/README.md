---
id: pages/list-table/sage/collection-list
type: page
name: 收藏夹列表
description: 4 列卡片网格 · 每张含会话徽章 + 主问题 truncate + 时间 + 字段预览（bg-slate-50 grid-cols-2/3）+ inline 编辑备注 Modal · 顶部"批量管理"切多选删
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm]
  stack: [react-antd-tailwind]
preview: /preview/pages/list-table/sage/collection-list
---

# Collection List

> sage 收藏的 SQL 问答历史。一张表 = 一次完整的"问题 + 答案"快照（包含 SQL、结果列名、可重放）。卡片网格展示，"管理 / 批量删除"按钮切换多选模式。

## 整体外壳

```jsx
<ConfigProvider>
  <div className="flex-1 bg-white bg-slate-50 p-6">
    <Header />
    {loading ? <Spin /> : empty ? <Empty /> : <Grid />}
    <Modal title="编辑备注" open={!!editing}>
      <Input.TextArea rows={4} showCount maxLength={200} />
    </Modal>
  </div>
</ConfigProvider>
```

## Header
`flex justify-between items-center mb-6`：
- 左：`<h1 className="text-2xl font-bold text-slate-800 flex items-center gap-2">` + `<Star />` + "收藏夹"
- 右：`flex items-center gap-2`
  - `<Tooltip>` + `<PanelLeftOpen />` 切换 sidebar 收起
  - 操作按钮：
    - 普通态：`<Button className={themeClasses.bg + themeClasses.bgHover}>` "管理"
    - 批量态：`<Button danger>` `<Trash2 />` 删除（{count}）

## 网格
- `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4`
- 卡片：`tour-collection-card relative bg-white rounded-lg border p-4 cursor-pointer`
  - 选中：`${themeClasses.border} ring-1 ${themeClasses.ring}`
  - 未选：`border-slate-200`
- 批量勾选 Checkbox：`absolute top-3 right-3 z-10`

### 卡片标题段
`mb-3 flex-1`：
- 会话徽章：`text-[10px] font-medium text-slate-500 bg-[rgb(252,252,252)] px-2 py-0.5 rounded-full inline-block` "本月销售 Top 10"
- 主文：`font-semibold text-slate-800 line-clamp-2 text-sm` 用户原问题
- 编辑铅笔：`<Pencil />` 14px `p-0.5 ${themeClasses.textHover}` —— hover 弹 inline 编辑（实际是触发 Modal）

### 元信息
`text-xs text-slate-400`：时间戳 "2 小时前 · 123 行"

### 数据预览
`bg-slate-50 rounded p-3 border border-slate-100`：
- 字段网格 `grid grid-cols-2 md:grid-cols-3 gap-2`
- 每个字段一个 `<Bubble>`（截断显示），溢出 Tooltip max-w-xs

## 视觉要点

1. **卡片不分会话归类**：所有收藏一锅展示，标题徽章告诉用户来源 —— 比按会话分组更扁平
2. **会话徽章 #fcfcfc 几乎贴白**：作为辅助信息存在，不抢卡片主标题
3. **line-clamp-2**：主问题超长截两行 + ... 防止卡片高度爆炸
4. **bg-slate-50 数据预览**：让"字段列表"视觉与卡片标题分层
5. **批量态用 danger 红**：操作按钮立刻提醒"危险动作"

## 反模式

- ❌ 不要把卡片做成行 list —— 4 列网格是 sage 视觉密度核心
- ❌ inline 编辑铅笔 hover 才显 —— 不要常驻，避免视觉杂乱

## 使用上游
- `core/components/layout/MainLayout`（sidebar "收藏夹" 按钮）

## 内嵌
- `<Bubble>`（通用 truncate + tooltip 文本组件）
