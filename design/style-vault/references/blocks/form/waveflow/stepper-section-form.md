---
id: blocks/form/waveflow/stepper-section-form
type: block
name: Stepper 多步骤表单
description: 顶部 Stepper（圆圈数字 / 已完成 ✓ / blue-600 当前 ring-blue-100）+ section divider + 当前步内容 + 底部 prev/next ghost+primary 按钮
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, industrial]
  mood: [serious, calm]
  stack: [shadcn-radix]
uses:
  - components/buttons/waveflow/cva-engineer-button
preview: /preview/blocks/form/waveflow/stepper-section-form
---

# Waveflow Stepper Section Form

> waveflow 多步骤表单的容器（如 json-build 4 步：Reader → Writer → Mapper → Build & 模板）。**Stepper** 在顶（圆圈数字 → 已完成 √）+ **section divider** + **当前 step 内容**（`步骤 N：xxx` 13px font-medium stone-700 + 表单区）+ **底部固定 prev/next 按钮行**。

## 视觉特征

### Stepper（components/ui/stepper.tsx）

- **`<ol className="flex items-center gap-0">`**
- 每 step：`<li className="flex flex-1 flex-col items-center">` + clickable `<button>` 包圆圈 + label
  - 圆圈：`flex h-6 w-6 items-center justify-center rounded-full border text-[11.5px] font-semibold transition`
  - done：`border-blue-600 bg-blue-600 text-white` + `<Check className="h-3 w-3" />`
  - current：`border-blue-600 bg-white text-blue-600 ring-2 ring-blue-100`
  - upcoming：`border-stone-300 bg-white text-stone-400`
- label text-[12px]：current font-medium stone-900 / done stone-600 / upcoming stone-400
- 连接线：`<span className="-mt-7 h-px flex-1 transition" + done ? 'bg-blue-600' : 'bg-stone-200'`

### 容器布局

```tsx
<div className="h-full px-6 py-4">
  <section className="rounded-xl border border-stone-200/40 bg-[var(--color-paper)] shadow-[var(--shadow-soft)] p-5">
    <h2 className="mb-3 text-[15px] font-semibold tracking-tight text-stone-900">任务构建</h2>

    <div className="mb-5">
      <Stepper items={[{ label: 'Reader' }, { label: 'Writer' }, { label: '字段映射' }, { label: '构建 & 模板' }]} active={active} onChange={setActive} />
    </div>

    <div className="border-t border-stone-100 pt-4">
      {active === 0 && <Section title="步骤 1：构建 Reader"><ReaderPanel ... /></Section>}
      {active === 1 && <Section title="步骤 2：构建 Writer"><WriterPanel ... /></Section>}
      {/* ... */}
    </div>

    <div className="mt-5 flex gap-2 border-t border-stone-100 pt-4">
      <Button variant="ghost" disabled={active === 0} onClick={handlePrev}>上一步</Button>
      <Button variant="primary" onClick={handleNext}>{active === 3 ? '创建任务' : '下一步'}</Button>
    </div>
  </section>
</div>
```

## 适配指南

- 步骤 ≤ 5 用 Stepper（视觉宽度刚好）；> 5 切其它流程（侧栏 navigator / 折叠步骤）
- 步骤间数据共享：父组件管 reader/writer/mapper 三个 state，子 panel 接 value+onChange
- 进入最后一步显示"创建任务"而非"下一步"——文案变化即"动作变化"
- 步骤前不验证：用户可以反复横跳查/改

## 反模式

- ❌ Stepper 用 vertical 横排——和 admin 横向工作流不和谐
- ❌ 步骤标题用大于 15px——抢主表单字
- ❌ 连接线用粗 2px+ —— 反客为主
