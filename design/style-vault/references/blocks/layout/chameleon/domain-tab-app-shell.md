---
id: blocks/layout/chameleon/domain-tab-app-shell
type: block
name: 域 tab 全屏壳
description: 顶栏(h-14 域 tab 切换) + 无边二级导航(w-56 细 rail) + Outlet 内容(px-6 py-4 自动滚)的全屏 full-bleed 三段壳；导航主轴搬到顶栏域 tab，二级导航降级为同表面细 rail，内容占满
platforms:
- web
theme: light
tags:
  aesthetic:
  - industrial
  - minimal
  mood:
  - calm
  - serious
  stack:
  - shadcn-radix
uses:
- tokens/border/waveflow/translucent-stone-system
- tokens/palettes/waveflow/warm-paper-ink-blue
preview: /preview/blocks/layout/chameleon/domain-tab-app-shell
---

# 域 tab 全屏壳

> Chameleon 的 `MainLayout`（`core/components/layout/main-layout.tsx`）——顶栏（域 tab 切换）+ 无边二级导航 + Outlet 内容的全屏 full-bleed 三段壳。与传统左侧栏布局根本不同：导航主轴搬到**水平顶栏域 tab**（工作台 / 知识库 / 观测 / 设置），二级导航降级为同表面**细 rail**（无边框、不另起底色），内容区 full-bleed 占满。CommandPalette（⌘K）+ NavProgressBar 挂在 shell 外。

## 视觉特征

- **外层**：`div.flex h-screen flex-col bg-[var(--color-warm)]`（#fafaf7）
- **顶部 TopBar**：`header.flex h-14 flex-shrink-0 items-center gap-4 border-b border-stone-200/70 bg-[var(--color-paper)] px-4`（高 56px）
  - 品牌：logo `h-7 w-7` + `span.text-[15px] font-semibold tracking-tight text-stone-800`「Chameleon」
  - 分隔竖线：`h-5 w-px bg-stone-200`
  - **域 tabs（左对齐）**：`nav.flex items-center gap-1`，每个 `Link.flex items-center gap-2 rounded-[10px] px-3.5 py-2 text-[13.5px] font-semibold transition`
    - active：`bg-blue-50 text-blue-700`，icon `h-[17px] w-[17px] text-blue-600`
    - idle：`text-stone-600 hover:bg-stone-100/70 hover:text-stone-900`，icon `text-stone-400`
  - 右侧账户：`ml-auto flex items-center`，头像 `h-8 w-8 rounded-full`
- **下方主体**：`div.flex min-h-0 flex-1` 横排
  - **SecondaryNav（细 rail）**：`aside.flex w-56 flex-shrink-0 flex-col overflow-y-auto bg-[var(--color-warm)] px-3 py-4`（宽 224px，**与内容同底色无边框**）
    - 分组标题：`px-3 pb-1.5 text-[10.5px] font-bold tracking-[0.06em] text-stone-400 uppercase`，第二组起 `pt-5`
    - 叶子项：`Link.relative flex items-center gap-3 rounded-[10px] px-3 py-2 text-[13px] font-medium transition`
      - active：`bg-blue-50 font-semibold text-blue-700` + 左侧书签竖条 `absolute top-2 bottom-2 left-0 w-[3px] rounded-r-[3px] bg-blue-600 shadow-[0_0_8px_rgba(59,130,246,0.45)]`
      - idle：`text-stone-600 hover:bg-stone-200/40 hover:text-stone-900`
      - icon `h-4 w-4`，active `text-blue-600` / idle `text-stone-400`
    - **单项域（如知识库）二级导航不渲染**（`allVisible.length <= 1` 返回 null）——内容直接铺满
  - **main**：`main.flex-1 overflow-auto px-6 py-4`（横 24px / 纵 16px）包 `<Outlet />`
- **shell 外浮层**：`CommandPalette`（⌘K modal）+ `NavProgressBar`（顶部进度条）挂在 `RequireAuth` 内、shell 外

## 核心代码

```tsx
<RequireAuth>
  <div className="flex h-screen flex-col bg-[var(--color-warm)]">
    <TopBar />               {/* h-14 域 tab 切换，左对齐 */}
    <div className="flex min-h-0 flex-1">
      <SecondaryNav />       {/* w-56 无边细 rail，与内容同底色 */}
      <main className="flex-1 overflow-auto px-6 py-4">
        <Outlet />
      </main>
    </div>
  </div>
  <CommandPalette />
  <NavProgressBar />
</RequireAuth>
```

## 与 waveflow/data-console-shell 区分

供 AI 消费时选对：

| 维度 | waveflow/data-console-shell | chameleon/domain-tab-app-shell |
|------|------|------|
| **导航主轴** | 左 sidebar（w-60 / 240px）单段竖导航 + 上 topbar（h-12 / 48px） | **顶栏域 tab 水平切换**（h-14 / 56px）+ 二级导航降级为细 rail |
| **二级导航** | 无（sidebar 即全部导航） | `w-56` 细 rail，**无边框、与内容同 warm 底色**，按当前域显示分组叶子 |
| **底色层级** | 三档：warm → warm-2（sidebar）→ paper（卡片） | 顶栏 paper + rail/内容 warm（两档），靠书签竖条 + 蓝药丸做选中 |
| **选中态** | sidebar 项常规高亮 | active 域药丸 `bg-blue-50` + 二级叶子左侧 `w-[3px]` 发光书签竖条 |
| **单项域** | 总有 sidebar | 单项域（知识库）**二级导航整条隐藏**，内容 full-bleed |
| **内容区** | 双层（外 px-6 py-4 + 内 rounded-xl 卡片） | main `px-6 py-4` 直接包 Outlet，页面自定卡片 |

选型：传统 admin 单层左导航 → waveflow data-console-shell；多域产品（每域内有自己的子导航）+ 想把横向空间还给内容 → 本变体。

## 适配指南

- 用 React Router v6 `<Outlet />`，MainLayout 不 unmount，切页只换 Outlet
- 域定义在 `nav-config`（域 → 分组 → 叶子），TopBar 读 `DOMAINS` 渲染顶 tab，SecondaryNav 读 `findActiveDomain(pathname)` 渲染当前域子导航
- 权限过滤：域 / 叶子按 `hasPermission(perm)` 过滤，无可见叶子的域整个隐藏
- 二级导航单叶子时返回 null——别给只有一页的域留一条空 rail

## 反模式

- ❌ 给二级 rail 加边框 / 另起底色——它要「与内容同表面」，靠书签竖条 + 蓝药丸表达层级
- ❌ 把导航主轴留在左侧栏——本壳的核心是把横向空间还给内容、主轴上移到顶栏
- ❌ 单项域仍渲染空 rail——`allVisible.length <= 1` 必须返回 null
- ❌ 内容区再套一层固定卡片外框——main 只给 `px-6 py-4`，卡片由各页自定
