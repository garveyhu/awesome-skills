---
id: pages/detail/chameleon/kb-detail-tabbed-workbench
type: page
name: 知识库详情工作台（左竖 tab rail + 右主区）
description: 左竖向 tab 导航（核心 文档/召回测试/概览 + 进阶 元数据/评测/一致性/服务API/设置 两组）+ 右主区按 tab 切（文档表 / 检索测试三栏 / 评估列表 / 概览统计）；知识库 Dify 级工作台
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
- blocks/display/chameleon/kb-hit-test-3pane
- blocks/nav/chameleon/detail-left-tab-rail
preview: /preview/pages/detail/chameleon/kb-detail-tabbed-workbench
---

# Chameleon KB Detail Tabbed Workbench

> 知识库详情整页（`/kbs/:id`）—— Dify 级知识库工作台。`flex gap-4`：**左** 竖向 tab rail（w-44，顶部 KB 身份块替代面包屑 + 「核心」三 tab + 分隔 + 「进阶」分组标签 + 五 tab），**右** 主区 `SectionCard min-w-0 flex-1` 按当前 tab 切内容（概览统计卡 / 文档上传区+表 / 召回测试三栏 / 评估列表 / 元数据 / 集合 / 一致性 / 设置）。服务 API tab 特殊：右主区改 `flex h-[calc(100vh-5.5rem)] rounded-xl border bg-[var(--color-paper)]` 给有界高度让内部文档滚动。

## 视觉特征

- 外层 `flex gap-4`（gap 16px）
- **左 rail**（detail-left-tab-rail）`w-44 shrink-0 space-y-0.5`（176px）：
  - KB 身份块 `mb-3 flex items-center gap-2 px-1`：返回 Link `h-6 w-6 rounded-md text-stone-400 hover:bg-stone-100`（ArrowLeft h-4）+ 名称 `text-[14px] font-semibold text-stone-900 truncate` + kb_key `font-mono text-[10.5px] text-stone-400 truncate`
  - 核心三 tab（文档 FileText / 召回测试 Search / 概览 BarChart3）
  - 分隔 `my-2 border-t border-stone-200/60`
  - 「进阶」分组标签 `px-3 pb-1 text-[10.5px] tracking-wider text-stone-400 uppercase`
  - 进阶五 tab（元数据 Tag / 评测 FlaskConical / 一致性 ShieldCheck / 服务 API KeyRound / 设置 Settings）
  - 每个 tab 按钮 `flex w-full items-center gap-2.5 rounded-lg px-3 py-2 text-[13px] font-medium`，选中 `bg-blue-50 text-blue-700`、未选 `text-stone-600 hover:bg-stone-100 hover:text-stone-900`；图标 `h-4 w-4`
- **右主区**：普通 tab 用 `SectionCard min-w-0 flex-1`（白卡）；service-api tab 用 `min-w-0 flex-1 overflow-hidden rounded-xl border border-stone-200 bg-[var(--color-paper)]` + 整页 `flex h-[calc(100vh-5.5rem)]`
- 概览 tab：4 列统计卡 `grid grid-cols-4 gap-3`，每个 `rounded-lg border border-stone-200/70 bg-stone-50/60 px-4 py-3`——label `text-[11px] text-stone-500` + 值 `tnum mt-1 font-mono text-[20px] text-stone-900`；下方 2 列 KvCard `grid grid-cols-2 gap-3 text-[12.5px]`，每个 `rounded-md border border-stone-200/70 bg-white px-3 py-2`（label stone-500 + value stone-800，mono 项 tnum font-mono）
- 召回测试 tab（HitTestPanel）三栏 `grid lg:grid-cols-[260px_minmax(0,1fr)_minmax(0,1.05fr)] gap-3`：① 参数（query Textarea / top_k range `accent-amber-600` / 召回模式 Select / 多查询 Switch / 标签 / 元数据过滤 / 搜索 Button）② 命中 chunk 列表（HitCard `rounded-lg border p-2.5`，active `border-amber-300 ring-1 ring-amber-200`，含 `#rank` font-mono + 文档标题 + seq + score breakdown + content line-clamp-2）③ 选中原文 `rounded-lg border bg-white`（标题 Link + score breakdown + 高亮原文 whitespace-pre-wrap）
- KB 卡族图标 tile 走 emerald（`bg-emerald-50 text-emerald-600` Database），区别于应用卡的多 kind 色

## 核心代码

```tsx
return (
  <div className="flex gap-4">
    {/* 左竖 tab rail */}
    <nav className="w-44 shrink-0 space-y-0.5">
      <div className="mb-3 flex items-center gap-2 px-1">
        <Link to="/kbs" className="h-6 w-6 rounded-md text-stone-400 hover:bg-stone-100"><ArrowLeft className="h-4 w-4" /></Link>
        <div className="min-w-0">
          <div className="truncate text-[14px] font-semibold text-stone-900">{kb.name}</div>
          <div className="truncate font-mono text-[10.5px] text-stone-400">{kb.kb_key}</div>
        </div>
      </div>
      {NAV_PRIMARY.map(navBtn)}
      <div className="my-2 border-t border-stone-200/60" />
      <div className="px-3 pb-1 text-[10.5px] tracking-wider text-stone-400 uppercase">进阶</div>
      {NAV_ADVANCED.map(navBtn)}
    </nav>
    {/* 右主区按 tab 切 */}
    <SectionCard className="min-w-0 flex-1">
      {tab === 'overview' && <OverviewTab kb={kb} />}
      {tab === 'documents' && <DocumentsTab kbId={kbId} />}
      {tab === 'search' && <HitTestPanel kb={kb} />}
      {tab === 'eval' && <EvaluationListTab kbId={kbId} />}
      …
    </SectionCard>
  </div>
);

const navBtn = (t) => (
  <button onClick={() => setTab(t.key)}
    className={cn('flex w-full items-center gap-2.5 rounded-lg px-3 py-2 text-left text-[13px] font-medium transition',
      tab === t.key ? 'bg-blue-50 text-blue-700' : 'text-stone-600 hover:bg-stone-100 hover:text-stone-900')}>
    {t.icon}{t.label}
  </button>
);
```

## 适配指南

- tab 入 URL（`?tab=`）`setSearchParams(next, { replace: true })`——navigate(-1) 返回能精确恢复所在 tab
- 左 rail 顶部用「KB 身份块」（返回 + 名称 + key）替代传统面包屑——竖 tab 工作台里身份信息钉左上更稳
- 两组 tab（核心 / 进阶）用 `border-t` + 「进阶」uppercase 小标题分隔——常用三项在上，低频五项收进进阶
- service-api tab 需要有界高度（`h-[calc(100vh-5.5rem)]` + `overflow-hidden rounded-xl`）让内嵌 API 文档内部滚动生效；其余 tab 走 SectionCard 自然高
- 召回测试 top_k 滑块用 `accent-amber-600`、命中卡选中态用 amber——KB 检索语境的强调色是琥珀，区别于全站蓝
- 选中 tab `bg-blue-50 text-blue-700`，与 graph-app-rail 二级导航同款语言

## 反模式

- ❌ 用顶部横 tab——KB 功能多（8 项），竖 rail 才放得下且可分组
- ❌ 八个 tab 平铺不分组——核心 / 进阶两组 + 分隔线，降低扫读负担
- ❌ 概览统计卡用纯白底——用 `bg-stone-50/60` 浅底，和右白卡区分出「数据格」
- ❌ 召回测试三栏用固定等宽——参数列 260px 固定，命中 / 原文用 `minmax(0,1fr)` / `minmax(0,1.05fr)` 弹性
- ❌ KB 图标 tile 用蓝——KB 卡族统一 emerald，和应用卡的 sky/violet/indigo 区分
