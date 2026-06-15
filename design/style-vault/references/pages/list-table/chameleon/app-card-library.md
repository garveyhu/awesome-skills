---
id: pages/list-table/chameleon/app-card-library
type: page
name: 应用卡片库（Dify 风货架）
description: kind 过滤 tab + 搜索 + 卡片网格（创建入口卡 + 应用卡）+ 新建应用编排选择器 Modal；/agents 与 /kbs 同卡族
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
- blocks/display/chameleon/app-card-gallery-grid
preview: /preview/pages/list-table/chameleon/app-card-library
---

# Chameleon App Card Library

> Chameleon 的「应用 / 知识库」着陆页（`/agents`、`/kbs`）—— 不是 waveflow 那种密集表格，而是 **Dify 式卡片货架**：顶部一行 kind 过滤 tab（图标 + 标签 + 计数）+ 右侧搜索框，下方 `grid sm:2 lg:3 xl:4` 卡片网格，首格永远是虚线「新建入口卡」，其余是统一外观的应用卡（图标 tile + 名称 + key + 描述 + 类型徽标 + 状态徽标 + 更新时间 + 悬浮三点菜单）。点「新建应用」弹 Dify 式编排方式选择器（对话 / 流程 / 生图 / 代码 四选一 grid）。

## 视觉特征

- 工具条：`mb-3 flex flex-wrap items-center gap-2`。过滤 tab 组 `flex items-center gap-1`，每个 `rounded-md px-2.5 py-1 text-[12px] font-medium`，选中 `bg-blue-50 text-blue-700`（图标 text-blue-600 + 计数 text-blue-400）、未选 `text-stone-500 hover:bg-stone-100`（图标 text-stone-400 + 计数 text-stone-400），图标 `h-3.5 w-3.5`，计数 `text-[10px]`
- 搜索框 `ml-auto` 右推：相对容器 + 左内嵌 `Search h-3.5 w-3.5 text-stone-400 left-2.5`，Input `h-8 w-56 pl-8 text-[12.5px]`
- 网格 `grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4`（gap 12px）
- **创建入口卡**：`h-[148px]`（KB 页 `h-[132px]`）虚线卡 `rounded-xl border border-dashed border-stone-300 bg-white/60`，hover `border-blue-400 bg-blue-50/40 text-blue-600`；居中 圆 tile `h-9 w-9 rounded-full bg-stone-100`（hover `bg-blue-100`）含 `Plus h-5 w-5 strokeWidth 1.75` + `text-[13px] font-medium` 标题 + `text-[11px] text-stone-400` 副文
- **应用卡**（AppCard）：`h-[148px] rounded-xl border border-stone-200/80 bg-white p-4 shadow-sm`，hover `border-primary-200 shadow-md`；hover 顶部高光线 `inset-x-4 top-0 h-0.5 bg-gradient-to-r from-transparent via-primary-500 to-transparent`；头行 图标 tile `h-9 w-9 rounded-lg`（有图标 `bg-stone-100`，否则按 kind 取 `meta.tile`，hover `-rotate-6 scale-105`）+ 名称 `text-[13.5px] font-medium text-stone-900` + key `font-mono text-[10.5px] text-stone-400`；描述 `mt-2 line-clamp-2 text-[11.5px] text-stone-500`；底行 类型徽标 `rounded px-1.5 py-0.5 text-[10px] font-medium`（meta.badge）+ 状态徽标（已发布 v3 emerald-50/700 / 草稿 stone-100/500 / 已嵌入 blue-50/700）+ `ml-auto text-[11px] text-stone-400` 更新时间
- kind 配色（KIND_META）：代码 indigo-50/600(tile) indigo-50/700(badge) · 对话 sky · 流程 violet · 外部 amber；KB 卡图标 tile 固定 `bg-emerald-50 text-emerald-600`（Database）
- 悬浮三点菜单 `absolute right-2 top-2 opacity-0 group-hover:opacity-100`，MoreVertical `h-7 w-7 rounded-md`，DropdownMenuContent `w-36 rounded-xl shadow-lg`，项 `rounded-lg px-2.5 py-1.5 text-[12.5px]`，删除项 `text-rose-600 focus:bg-rose-50`
- 新建应用 Modal（size md）：编排方式 `grid grid-cols-1 gap-2 sm:grid-cols-2`，每个选项卡 `rounded-lg border p-2.5`，选中 `border-stone-900 bg-stone-50 ring-1 ring-stone-900`、未选 `border-stone-200 hover:border-stone-300`；标题行 图标 `h-3.5 w-3.5` + `text-[12.5px] font-medium text-stone-900`，副文 `mt-1 text-[10.5px] text-stone-500`；四方式：对话编排(MessageSquare) / 流程编排(Workflow) / 生图应用(ImagePlus) / 代码应用(Code2)

## 核心代码

```tsx
{/* kind 过滤 tab */}
{KIND_FILTERS.map(({ key, label, icon: Icon }) => (
  <button onClick={() => setKindFilter(key)}
    className={cn('flex items-center gap-1.5 rounded-md px-2.5 py-1 text-[12px] font-medium transition',
      kindFilter === key ? 'bg-blue-50 text-blue-700' : 'text-stone-500 hover:bg-stone-100 hover:text-stone-700')}>
    <Icon className={cn('h-3.5 w-3.5', kindFilter === key ? 'text-blue-600' : 'text-stone-400')} />
    {label}
    <span className={cn('text-[10px]', kindFilter === key ? 'text-blue-400' : 'text-stone-400')}>{counts[key]}</span>
  </button>
))}

{/* 网格：创建入口卡 + 应用卡 */}
<div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
  <button className="group flex h-[148px] flex-col items-center justify-center gap-2 rounded-xl border border-dashed border-stone-300 bg-white/60 text-stone-500 transition hover:border-blue-400 hover:bg-blue-50/40 hover:text-blue-600">
    <div className="flex h-9 w-9 items-center justify-center rounded-full bg-stone-100 transition group-hover:bg-blue-100">
      <Plus className="h-5 w-5" strokeWidth={1.75} />
    </div>
    <span className="text-[13px] font-medium">新建应用</span>
    <span className="text-[11px] text-stone-400">对话 / 流程编排，或接入代码应用</span>
  </button>
  {filtered.map(c => <AppCard key={c.cardId} card={c} … />)}
</div>
```

## 适配指南

- 过滤 tab 选中状态用 `bg-blue-50 text-blue-700`（蓝主题），与 waveflow 黑底 segment 不同——这里要「轻」、可放多个 tab
- 卡片固定高度（148 / 132px）保证网格整齐；描述用 `line-clamp-2 + flex-1` 撑开，底行 `mt-auto` 钉底
- 选中 tab + 搜索过滤组合走 `useMemo` 客户端筛选；tab 选择落 sessionStorage（路由切换重挂后恢复）
- 三点菜单 `onClick={e => e.stopPropagation()}` 阻止冒泡到卡片 onOpen
- 新建 Modal 用「选项卡 grid」而非 RadioGroup，每卡带语义副文案说清两种类型的真实区别

## 反模式

- ❌ 把应用列表做成密集表格——这是 Dify 风货架，卡片才有「产品入口」的邀请感
- ❌ 卡片不固定高度——描述长短不一会让网格参差
- ❌ 过滤 tab 用黑底实心选中——这里 tab 多且要轻，用浅蓝底
- ❌ 创建入口卡和应用卡混排在网格中间——创建卡永远是首格
- ❌ 状态徽标用饱和实色——已发布 / 草稿 / 已嵌入用 *-50 浅底 + *-700 文字
