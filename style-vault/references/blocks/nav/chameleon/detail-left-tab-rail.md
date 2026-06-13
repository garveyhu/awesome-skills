---
id: blocks/nav/chameleon/detail-left-tab-rail
type: block
name: 详情页左窄栏竖向 tab（含应用级 rail）
description: KB/编辑器详情用左窄栏竖向 tab - 顶部「← 返回 + 名称/key」身份块 + 主分组按钮 + 分隔 + 「进阶」小标 + 进阶按钮；选中态 blue-50/blue-700。含 Dify 式应用级 graph-app-rail 变体
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
- tokens/palettes/chameleon/node-type-hue-system
- tokens/palettes/waveflow/warm-paper-ink-blue
preview: /preview/blocks/nav/chameleon/detail-left-tab-rail
---

# Chameleon 详情页左窄栏竖向 tab

> 知识库 / 编辑器详情用的左窄栏竖向 tab，URL `?tab=` 驱动（离开再返回精确恢复所在 tab）。两个形态：**(A) 轻量 detail-left-tab-rail（KB 详情）**——`nav w-44(176px)` 顶部「← 返回 + 名称/key」身份块 + 主分组按钮（文档/召回测试/概览）+ 分隔线 + 「进阶」UPPERCASE 小标 + 进阶按钮（元数据/评测/一致性/服务 API/设置）；**(B) 重量 graph-app-rail（编辑器应用栏）**——`aside w-64(256px) border-r bg-white`，含应用头（返回/图标块/名称/类型切换下拉/key/发布徽标/保存态点）+ 二级导航（编排/监测，active 左 3px 蓝条）+ 应用卡片（Web App / 后端服务 API，含可用状态胶囊），可收起成 w-12 图标栏。两者都用 `blue-50/blue-700` 选中态。

## 视觉特征 · (A) 轻量 KB 详情 tab rail

- **`nav w-44(176px) shrink-0 space-y-0.5`**
- **身份块 `mb-3 flex items-center gap-2 px-1`**：返回 `Link h-6 w-6 shrink-0 rounded-md text-stone-400 hover:bg-stone-100 hover:text-stone-700` 内含 `ArrowLeft h-4 w-4`；名称 `truncate text-[14px] font-semibold text-stone-900` + key `truncate font-mono text-[10.5px] text-stone-400`
- **navBtn `flex w-full items-center gap-2.5 rounded-lg px-3 py-2 text-left text-[13px] font-medium transition`**：active `bg-blue-50 text-blue-700` / 默认 `text-stone-600 hover:bg-stone-100 hover:text-stone-900`；icon `h-4 w-4`
- **分隔 `my-2 border-t border-stone-200/60`**
- **「进阶」小标 `px-3 pb-1 text-[10.5px] tracking-wider text-stone-400 uppercase`**
- **主内容并排**：`flex h-[calc(100vh-5.5rem)] gap-4` —— 左 nav + 右 `min-w-0 flex-1 overflow-hidden rounded-xl border border-stone-200 bg-[var(--color-paper)]`（或 SectionCard）

## 视觉特征 · (B) 重量 graph-app-rail 编辑器应用栏

- **`aside flex h-screen w-64(256px) shrink-0 flex-col border-r border-slate-200/80 bg-white transition-[width]`**（收起 `w-12`(48px)）
- **应用头 `border-b border-slate-200/80 p-3.5`**：
  - 返回 `-ml-1 inline-flex items-center gap-1 rounded-md py-0.5 pr-1.5 pl-1 text-[11.5px] font-medium text-stone-500 hover:bg-stone-100`+ `ChevronLeft h-3.5 w-3.5`；右侧 Sliders / ChevronsLeft 收起按钮 `p-1.5 text-stone-400`
  - 图标块 `flex h-9 w-9(36px) shrink-0 items-center justify-center rounded-xl shadow-sm ring-1`：chat=`bg-violet-50 text-violet-600 ring-violet-200/60` + `MessageSquare h-[18px] w-[18px]` / workflow=`bg-sky-50 text-sky-600 ring-sky-200/60` + `Workflow h-[18px] w-[18px]`
  - 名 `truncate text-[13px] leading-tight font-semibold text-stone-900` + key `mt-0.5 truncate font-mono text-[10.5px] text-stone-400`
  - 底行 `mt-2.5 flex items-center gap-1.5`：KindSelect `h-6 w-[88px] text-[11.5px]` + 发布徽标（已发布 `bg-emerald-50 text-emerald-700 ring-1 ring-emerald-200/60` + `Rocket h-2.5 w-2.5 v{n}` / 草稿 `bg-amber-50 text-amber-700`）+ 保存态点 `ml-auto`（saving `text-blue-500` + `animate-pulse bg-blue-400` / dirty `text-amber-600` + `bg-amber-400` / saved `text-stone-400` + `bg-stone-300`，点 `h-1.5 w-1.5 rounded-full`）
- **二级导航 `nav flex flex-col gap-0.5 p-2`**：按钮 `group relative flex items-center gap-2.5 rounded-lg py-1.5 pr-2.5 pl-3 text-[12.5px] font-medium`，active `bg-blue-50 text-blue-700` + **左条** `absolute top-1.5 bottom-1.5 left-0 w-[3px] rounded-full bg-blue-500`（active opacity-100 / 否则 0）；icon `h-4 w-4`，active `text-blue-600`
- **应用卡片区 `flex-1 space-y-2.5 overflow-y-auto border-t border-slate-200/80 bg-slate-50/40 p-2.5`**：
  - Card `rounded-xl border border-slate-200/80 bg-white p-3 shadow-sm ring-1 ring-stone-900/[0.02] hover:shadow-md`；头 `mb-2 flex items-center gap-1.5`：图标块 `h-5 w-5 rounded-md bg-stone-100 text-stone-500` + `Icon h-3 w-3` + 标题 `text-[12px] font-semibold text-stone-800` + 状态胶囊 `ml-auto rounded-full px-1.5 py-0.5 text-[9.5px] font-medium`（on `bg-emerald-50 text-emerald-600 ring-1 ring-emerald-200/50` + `bg-emerald-500` 点 / off `bg-stone-100 text-stone-400` + `bg-stone-300` 点）
  - RailAction `group flex flex-1 items-center justify-center gap-1.5 rounded-lg border border-slate-200/70 bg-slate-50 px-2 py-1.5 text-[11px] font-medium text-stone-600 hover:border-blue-200 hover:bg-blue-50 hover:text-blue-700`，icon `h-3 w-3 text-stone-400 group-hover:text-blue-500`
  - API 端点行 `font-mono text-[10px] text-stone-500` + `Copy h-3 w-3`

## 核心代码（A · navBtn）

```tsx
const navBtn = (t: TabDef) => (
  <button onClick={() => setTab(t.key)} className={cn(
    'flex w-full items-center gap-2.5 rounded-lg px-3 py-2 text-left text-[13px] font-medium transition',
    tab === t.key ? 'bg-blue-50 text-blue-700' : 'text-stone-600 hover:bg-stone-100 hover:text-stone-900')}>
    {t.icon}{t.label}
  </button>
);

<nav className="w-44 shrink-0 space-y-0.5">
  <div className="mb-3 flex items-center gap-2 px-1">
    <Link to="/kbs" className="flex h-6 w-6 shrink-0 ... rounded-md hover:bg-stone-100"><ArrowLeft className="h-4 w-4" /></Link>
    <div className="min-w-0">
      <div className="truncate text-[14px] font-semibold text-stone-900">{name}</div>
      <div className="truncate font-mono text-[10.5px] text-stone-400">{kb_key}</div>
    </div>
  </div>
  {NAV_PRIMARY.map(navBtn)}
  <div className="my-2 border-t border-stone-200/60" />
  <div className="px-3 pb-1 text-[10.5px] tracking-wider text-stone-400 uppercase">进阶</div>
  {NAV_ADVANCED.map(navBtn)}
</nav>
```

lucide：A → ArrowLeft / FileText / Search / BarChart3 / Tag / FlaskConical / ShieldCheck / KeyRound / Settings。B → ChevronLeft / ChevronsLeft / ChevronsRight / MessageSquare / Workflow / Layers / Activity / Globe / Server / Code2 / Copy / KeyRound / Rocket / Sliders。

## 适配指南

- tab 入 URL `?tab=`（`replace`）：离开再 `navigate(-1)` 精确恢复，不重置到默认
- 主分组放高频（文档/召回/概览），进阶分组放低频（元数据/评测/设置）—— 用分隔线 + UPPERCASE 小标分两段
- 应用级 rail 收起态走 `w-12` 图标栏（only icon + tooltip），不做内容裁剪
- 图标块走节点类型色（chat violet / workflow sky）—— 见 node-type-hue-system token
- 选中态统一 `blue-50/blue-700`；重量 rail 额外叠左 3px 蓝条（`bg-blue-500`）

## 反模式

- ❌ tab 状态只放组件 state 不入 URL——返回丢 tab
- ❌ 主 / 进阶不分段——一长串按钮失去频率层级
- ❌ 收起态裁剪卡片内容——应整段切到图标栏
- ❌ 应用头保存态点不区分 saving/dirty/saved 三态——用户不知改动是否已落库
