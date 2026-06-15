---
id: blocks/nav/chameleon/domain-tab-topbar-account
type: block
name: h-14 paper 域 tab 顶栏 + 账户菜单
description: 浅 paper 通栏顶栏 - 品牌(logo+Chameleon) | 竖分隔 | 左对齐域 tabs(工作台/知识库/观测/设置, 药丸) ……右上角头像账户 dropdown
platforms:
- web
theme: light
tags:
  aesthetic:
  - industrial
  - minimal
  mood:
  - calm
  - confident
  - serious
  stack:
  - shadcn-radix
uses:
- tokens/border/waveflow/translucent-stone-system
- tokens/palettes/waveflow/warm-paper-ink-blue
- tokens/shadow/waveflow/soft-card-pop-trio
preview: /preview/blocks/nav/chameleon/domain-tab-topbar-account
---

# Chameleon 域 tab 顶栏 + 账户菜单

> app-shell 浅 paper 通栏顶栏（h-14）。左到右：**品牌**（logo-sm.png 28px + 「Chameleon」15px font-semibold）→ 竖分隔（h-5 w-px stone-200）→ **左对齐域 tabs**（工作台 / 知识库 / 观测 / 设置，圆角 10px 药丸，active=`bg-blue-50 text-blue-700`）→ `ml-auto` 右上角**头像账户 dropdown**（语言 / API 文档 / 系统配置 / 退出，从旧侧栏底部迁移而来）。signature = 左对齐域 tab 药丸 + 右上头像账户菜单；搜索移到 ⌘K（无搜索按钮、无在线 ping）。

## 视觉特征

- **header `flex h-14(56px) flex-shrink-0 items-center gap-4(16px) border-b border-stone-200/70 bg-[var(--color-paper)](#fffefb) px-4(16px)`**
- **品牌 Link `flex items-center gap-2.5(10px)`**：`img /logo-sm.png h-7 w-7(28px) flex-shrink-0 object-contain` + `span text-[15px] font-semibold tracking-tight text-stone-800(#292524)` Chameleon
- **分隔 `span h-5(20px) w-px bg-stone-200`**
- **域 nav `flex items-center gap-1(4px)`**，每个域 Link `flex items-center gap-2(8px) rounded-[10px] px-3.5(14px) py-2(8px) text-[13.5px] font-semibold transition`：
  - active：`bg-blue-50(#eff6ff) text-blue-700(#1d4ed8)` + icon `text-blue-600(#2563eb)`
  - default：`text-stone-600(#57534e) hover:bg-stone-100/70 hover:text-stone-900` + icon `text-stone-400(#a8a29e)`
  - 域 icon `h-[17px] w-[17px]`（lucide Boxes / Database / Telescope / Settings）
- **右侧 `ml-auto flex items-center`** → AccountMenu
- **AccountMenu 触发**：`button rounded-full outline-none hover:brightness-105 focus-visible:ring-2 focus-visible:ring-blue-500/40`，内 `img /default-avatar.jpg h-8 w-8(32px) rounded-full object-cover`
- **Dropdown content `w-64(256px) rounded-xl(12px) border-stone-200/80 p-1.5(6px) shadow-[var(--shadow-pop)]`**（align=end side=bottom sideOffset=8）：
  - 用户头部 `flex items-center gap-3 px-2.5 py-2.5`：`h-9 w-9(36px) rounded-full` 头像 + 用户名 `truncate text-[13.5px] font-semibold text-stone-800` + email `truncate text-[11.5px] text-stone-400`
  - 分隔 `bg-stone-200/60`
  - item `gap-2.5 rounded-lg px-2.5 py-2 text-[13px]`：API 文档（BookOpen `h-4 w-4 text-stone-400`）/ 系统配置（Settings）/ 退出（LogOut，`text-red-600 hover:bg-red-50 focus:bg-red-50`）

## 核心代码

```tsx
<header className="flex h-14 flex-shrink-0 items-center gap-4 border-b border-stone-200/70 bg-[var(--color-paper)] px-4">
  <Link to="/dashboard" className="flex items-center gap-2.5">
    <img src="/logo-sm.png" className="h-7 w-7 flex-shrink-0 object-contain" />
    <span className="text-[15px] font-semibold tracking-tight text-stone-800">Chameleon</span>
  </Link>
  <span className="h-5 w-px bg-stone-200" />
  <nav className="flex items-center gap-1">
    {visibleDomains.map(d => (
      <Link key={d.key} to={d.to} className={cn(
        'flex items-center gap-2 rounded-[10px] px-3.5 py-2 text-[13.5px] font-semibold transition',
        active ? 'bg-blue-50 text-blue-700' : 'text-stone-600 hover:bg-stone-100/70 hover:text-stone-900')}>
        <Icon className={cn('h-[17px] w-[17px]', active ? 'text-blue-600' : 'text-stone-400')} />
        {d.fallbackTitle}
      </Link>
    ))}
  </nav>
  <div className="ml-auto flex items-center"><AccountMenu /></div>
</header>
```

lucide：Boxes / Database / Telescope / Settings（域）+ BookOpen / Settings / LogOut（账户菜单）。

## 适配指南

- 域 / 域内叶子从 nav-config 单一数据源取（顶栏与左导航共用，避免漂移）
- 权限就绪后再过滤域（`hydrated` 门控）避免首屏域闪烁
- active 域用 `findActiveDomain(pathname)`（最长命中叶子所在域）
- 搜索不放顶栏——交给 ⌘K 命令面板（见 cmdk-grouped-palette）；顶栏只保留品牌 + 域 + 账户

## 与 waveflow/topbar-search-ping 区分

| 维度 | waveflow topbar-search-ping | 本条 domain-tab-topbar-account |
|------|-----------------------------|--------------------------------|
| 高度 | h-12 暖底 | h-14 paper 底（#fffefb） |
| 中段 | 260px 搜索按钮（占据中部） | **左对齐域 tab 药丸**（工作台/知识库/观测/设置） |
| 右段 | emerald ping 在线 dot（无头像） | **右上头像账户 dropdown**（语言/API 文档/设置/退出） |
| 搜索 | 顶栏内搜索按钮 | 移到 ⌘K，顶栏无搜索 |
| 在线指示 | 有 emerald ping | 无 |

选条原则：要「带搜索按钮 + 在线 ping 的应用顶栏」用 waveflow；要「域切换 tab + 账户菜单（搜索走 ⌘K）」用本条。

## 反模式

- ❌ 域 tab 居中或右对齐——必须左对齐紧贴品牌分隔，是 IA 主轴
- ❌ 顶栏塞搜索框——交给 ⌘K，顶栏保持品牌 + 域 + 账户三段
- ❌ 账户菜单退出项用中性灰——必须 `text-red-600 hover:bg-red-50` 危险语义
- ❌ 权限未就绪就渲染全部域——首屏会闪烁后再隐藏无权限域
