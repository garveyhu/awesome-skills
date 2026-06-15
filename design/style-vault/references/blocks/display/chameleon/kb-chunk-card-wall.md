---
id: blocks/display/chameleon/kb-chunk-card-wall
type: block
name: 知识库切块卡片墙
description: 文档详情的 chunk 段落管理墙 - responsive 卡片网格，每卡 seq + token + 正文(超 480 字截断展开) + 查看/编辑(重嵌)/启停/删除/复制行内动作 + 停用态弱化
platforms:
- web
theme: light
tags:
  aesthetic:
  - minimal
  - industrial
  mood:
  - calm
  - serious
  stack:
  - shadcn-radix
uses:
- tokens/palettes/waveflow/warm-paper-ink-blue
preview: /preview/blocks/display/chameleon/kb-chunk-card-wall
---

# 知识库切块卡片墙

> 文档详情页的 chunk 段落管理墙（Dify 段落管理范式）：responsive 卡片网格，每卡 `#seq + N tok + 命中数` 头 + 正文（超 480 字截断「…」+ 展开）+ hover 露出「复制/编辑(重嵌)/启停/删除」行内动作，双击进编辑态换 Textarea，保存「已保存并重嵌」toast，停用态整卡弱化。文档详情头：信息卡（tag-editor + doc-meta-fields）+「N 块」计数 + 搜索框 + 分页。waveflow 无 KB，全新。

## 视觉特征

- **网格**：`grid grid-cols-1 gap-3 md:grid-cols-2 xl:grid-cols-3`（卡间距 12px）
- **卡片**：`group rounded-lg(8) border border-stone-200/70 bg-white p-3 transition hover:border-amber-300 hover:shadow-sm`，双击进编辑；停用态叠 `opacity-55`
- **卡头**（`mb-2 flex items-center justify-between text-[11px] text-stone-500`）：
  - 左 `flex items-center gap-2 font-mono`：`#{seq}` + `{token} tok`（tnum）+ 命中数 `命中 N`（tnum text-emerald-600）+ 停用 `· 已停用`（text-stone-400）
  - 右动作组 `flex gap-1 opacity-0 transition group-hover:opacity-100`：每个 `rounded p-0.5 hover:bg-stone-100`，icon `h-3 w-3`
    - Copy 复制 / Pencil 编辑 / Eye(启用态)·EyeOff(停用态) 启停 / Trash2 删除（`text-stone-400 hover:bg-rose-50 hover:text-rose-500`）
- **正文（查看态）**：`text-[12.5px] leading-relaxed whitespace-pre-wrap text-stone-800`，>480 字（MAX_PREVIEW_CHARS）截断 `slice(0,480)…`
- **展开按钮**：`mt-1 text-[11px] text-amber-700 hover:underline`「展开（共 N 字）」
- **关键词 chip**（可选）：`mt-2 flex flex-wrap gap-1`，每个 `rounded bg-stone-100 px-1.5 py-0.5 text-[10px] text-stone-500`
- **编辑态**：`space-y-2`，Textarea `rows={8}` `font-mono text-[12.5px]`，底部 `flex justify-end gap-2`：ghost「取消」(X h-3 w-3) + primary「保存」(Check h-3 w-3)，保存 disabled 当 `draft === content || !draft.trim()`
- **文档详情头**（页面外层 `space-y-3`）：
  - Breadcrumb：`text-[12.5px] text-stone-500`，ArrowLeft h-3.5「知识库」/「KB N」/ 文档名
  - DocumentInfoCard：tag-editor + doc-meta-fields 字段填值，dirty 时显「保存」
  - SectionCard 头 `mb-3 flex items-center justify-between gap-3`：`h3 text-[14px] font-medium text-stone-900「切块卡片墙」` + 搜索框 `relative max-w-[280px] flex-1`（Search h-3.5 left-2.5 + Input `h-8 pr-7 pl-8 text-[12.5px]`）+ 右侧 `text-[11.5px] text-stone-500「共 N 块」`
  - 底部 TablePagination

## 核心代码

```tsx
const MAX_PREVIEW_CHARS = 480;
const needTruncate = !expanded && content.length > MAX_PREVIEW_CHARS;
const display = needTruncate ? `${content.slice(0, MAX_PREVIEW_CHARS)}…` : content;

<div className={cn(
  'group rounded-lg border border-stone-200/70 bg-white p-3 transition hover:border-amber-300 hover:shadow-sm',
  !chunk.enabled && 'opacity-55',
)} onDoubleClick={() => !editing && setEditing(true)}>
  <div className="mb-2 flex items-center justify-between text-[11px] text-stone-500">
    <span className="flex items-center gap-2 font-mono">#{chunk.seq} <span className="tnum">{chunk.token_count} tok</span></span>
    <div className="flex gap-1 opacity-0 transition group-hover:opacity-100">{/* Copy/Pencil/Eye/Trash2 */}</div>
  </div>
  <div className="text-[12.5px] leading-relaxed whitespace-pre-wrap text-stone-800">{display}</div>
</div>

// 保存成功 toast：'已保存并重嵌'（编辑切块触发重嵌入）
```

## 适配指南

- 编辑保存即触发后端重新嵌入，toast 明确写「已保存并重嵌」让用户知道向量已更新
- 启停 = 软开关（停用不参与检索但保留），停用态整卡 `opacity-55` 弱化但仍可操作
- 行内动作组默认 `opacity-0`，仅卡 hover 露出，保持卡片墙清爽
- 超长 chunk 截断 480 字 + 展开，避免单卡撑爆网格高度

## 反模式

- ❌ 删除动作不二次确认——切块删除不可恢复，必须 confirm danger
- ❌ 用蓝色 hover 边框——KB 调试域统一 amber 强调（`hover:border-amber-300`、展开按钮 `text-amber-700`）
- ❌ 停用态直接隐藏卡片——应弱化展示（`opacity-55`）仍可勾回启用
- ❌ 行内动作常驻——用 `opacity-0 group-hover:opacity-100`
