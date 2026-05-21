---
id: pages/form-flow/waveflow/json-build-stepper
type: page
name: JSON 构建 4 步 Stepper
description: Reader → Writer → 字段映射 → 构建 4-step + 各步 Panel (数据源 select + Schema/Table 二级 select + Column 双列 transfer) + drawer 模板选择器 + Textarea JSON preview + 复制按钮
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, industrial]
  mood: [serious]
  stack: [shadcn-radix]
uses:
  - blocks/form/waveflow/stepper-section-form
  - components/selects/waveflow/multi-select-popover
preview: /preview/pages/form-flow/waveflow/json-build-stepper
---

# Waveflow JSON Build 4-Step Stepper

> waveflow 任务构建器 (`/job/jsonBuild` 和 `/job/jsonBuildBatch`)——4-step Stepper 表单：**1. Reader**（数据源 select → schema select (动态) → table select → column 双列 transfer + splitPk select + where 输入 + querySql Textarea）→ **2. Writer**（同 Reader 结构 + writeMode select + preSql/postSql Textarea）→ **3. 字段映射**（Reader 列 ←→ Writer 列 拖拽/下拉对应）→ **4. 构建 & 模板**（构建 button → 生成 JSON → Drawer 选择已有模板覆盖 → Textarea preview + Copy 按钮 → 最终"创建任务"）。

## 适用场景

| 路由 | 实际名称 | 差异 |
|---|---|---|
| `/job/jsonBuild` | 任务构建 | 单 Reader → 单 Writer |
| `/job/jsonBuildBatch` | 任务批量构建 | 多 Reader 表批量 → 单 Writer 库（一次配置多任务） |

## 页面骨架

```tsx
<div className="h-full px-6 py-4">
  <section className="rounded-xl border border-stone-200/40 bg-[var(--color-paper)] p-5 shadow-[var(--shadow-soft)]">
    <h2 className="mb-3 text-[15px] font-semibold tracking-tight text-stone-900">任务构建</h2>

    <div className="mb-5">
      <Stepper items={[{ label: 'Reader' }, { label: 'Writer' }, { label: '字段映射' }, { label: '构建 & 模板' }]} active={active} onChange={setActive} />
    </div>

    <div className="border-t border-stone-100 pt-4">
      {active === 0 && <PanelHeader title="步骤 1：构建 Reader"><ReaderPanel value={reader} onChange={...} /></PanelHeader>}
      {active === 1 && <PanelHeader title="步骤 2：构建 Writer"><WriterPanel value={writer} onChange={...} /></PanelHeader>}
      {active === 2 && <PanelHeader title="步骤 3：字段映射"><MapperPanel left={readerCols} right={writerCols} value={mapper} onChange={setMapper} /></PanelHeader>}
      {active === 3 && (
        <div className="space-y-3">
          <div className="text-[13px] font-medium text-stone-700">步骤 4：构建与选择模板</div>
          <div className="flex flex-wrap gap-2">
            <Button variant="primary" onClick={buildJson}>1. 构建</Button>
            <Button variant="primary" onClick={() => setDrawerOpen(true)}>
              {selectedTpl ? `已选模板：${selectedTpl.id} (${selectedTpl.jobDesc})` : '2. 选择模板'}
            </Button>
            <Button variant="outline" onClick={handleCopy}><Copy /> 复制 JSON</Button>
          </div>
          <Textarea rows={16} className="font-mono text-[11.5px]" value={configJson} onChange={...} placeholder="构建后的 JSON 将显示在此" />
        </div>
      )}
    </div>

    <div className="mt-5 flex gap-2 border-t border-stone-100 pt-4">
      <Button variant="ghost" disabled={active === 0} onClick={handlePrev}>上一步</Button>
      <Button variant="primary" onClick={handleNext}>{active === 3 ? '创建任务' : '下一步'}</Button>
    </div>
  </section>

  <Drawer open={drawerOpen} onOpenChange={setDrawerOpen}>
    <DrawerContent>
      <DrawerHeader><DrawerTitle>选择模板</DrawerTitle><DrawerCloseIcon /></DrawerHeader>
      <DrawerBody>
        <DataTable columns={tplColumns} rows={tplRows} ... />
        <TablePagination ... />
      </DrawerBody>
    </DrawerContent>
  </Drawer>
</div>
```

## 视觉要点

1. **Stepper 4 步**：水平圆圈数字 + 已完成 ✓ + blue-600 + ring-2 + label
2. **panel 标题**: `text-[13px] font-medium text-stone-700` "步骤 N：xxx" —— 比节 title 小一档
3. **Reader / Writer panel 结构**：5-7 个 form field 垂直，每个 Label + Select/Input
4. **column 双列 transfer**：左 available columns / 右 selected columns，Checkbox 选 + 中间按钮移；额外 batch 粘贴文本输入区（逗号/空格/换行分隔）
5. **mapper panel**：每个 reader 列右侧一个 Select 让用户选对应 writer 列；未配对的留空
6. **JSON Textarea**: rows=16 + `font-mono text-[11.5px]` —— 工程师看 JSON 习惯
7. **Drawer 模板选择**：右侧滑出全屏 drawer，内嵌完整 DataTable + Pagination —— 选模板等同打开"任务模板"页

## 适配指南

- step state 在 page 顶 useState 管，子 panel 接 value+onChange
- 数据源切换时 reset schemaList/tableName/columns；NEED_SCHEMA 集合判断（postgresql/oracle/sqlserver/dm/kingbase）才显 schema select
- "复制 JSON" 用 `navigator.clipboard.writeText(configJson)` + toast.success
- 模板选好后**直接覆盖** Reader/Writer/Mapper 三个 state—— 不弹"是否覆盖"确认

## 反模式

- ❌ 每步走独立路由—— 失去 state 共享 + 状态恢复
- ❌ JSON 不让用户改—— 高阶用户想直接编辑
- ❌ "下一步"前做严格验证—— 允许反复横跳查值
