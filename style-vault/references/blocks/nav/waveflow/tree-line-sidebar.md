---
id: blocks/nav/waveflow/tree-line-sidebar
type: block
name: 暖底 Tree-line 侧栏
description: 240px sidebar - brand + UPPERCASE 分组头 + Tree-line 子项 + count badge + bottom user dropdown - 完整侧栏单元
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, industrial]
  mood: [calm, serious]
  stack: [shadcn-radix]
uses:
  - tokens/iconography/waveflow/engineer-detail-classes
  - tokens/palettes/waveflow/warm-paper-ink-blue
  - components/typography-atoms/waveflow/meta-caps-mono-pair
preview: /preview/blocks/nav/waveflow/tree-line-sidebar
---

# Waveflow Tree-line Sidebar

> waveflow 整站标志性侧栏——240px 宽暖底（`var(--color-warm-2)`），上中下三段：**brand**（waveflow logo + 折叠按钮）/ **nav**（一级菜单 + 分组头 + 可展开 group + 子项 tree-line L 钩）/ **bottom user**（黑猫头像 + 用户名 + 在线小绿点 + Settings dropdown）。

## 页面骨架

1. **aside**: `flex h-full w-60 flex-shrink-0 flex-col border-r border-stone-200/70 bg-[var(--color-warm-2)]`
2. **brand**（h-14 = 56px）:
   - `<img className="h-7 w-7 rounded ..."/>`（28px logo）
   - `<span className="text-[15.5px] font-semibold tracking-tight text-stone-800">Waveflow</span>`
   - 右侧折叠按钮（PanelLeftClose 14px / stone-500 / hover stone-200/60 stone-800）
3. **nav**: `flex-1 space-y-0.5 overflow-auto px-3 pb-2 pt-1 text-[14px]`
   - **TOP_ITEMS**（顶级菜单 · 运行报表 / 项目管理 / 数据源）
   - **分组头 "调度"**: `px-3 pb-1 pt-3 text-[11px] font-medium uppercase tracking-wider text-stone-400`
   - **NavGroup 任务管理**（可展开）：ChevronDown/Right toggle button + 主 Link + 末尾 count chip
   - **NavGroup 任务集**（带动态子项 status dot）
   - **SCHEDULE_LEAVES**（日志管理 等叶子项）
   - **分组头 "系统"**
   - **SYSTEM_ITEMS**（执行器 / 用户管理 / 资源监控 / 工具）
4. **bottom user**: DropdownMenuTrigger button
   - `group flex w-full items-center gap-2.5 border-t border-stone-200/70 bg-transparent p-2.5 text-left hover:bg-stone-200/40`
   - 头像 `<img className="h-7 w-7 rounded-full"/>` + 用户名 `text-[12px] text-stone-800` + 在线状态行 `text-[10px] text-stone-500` + Settings icon 14px

## 视觉特征

- **NavLeafItem active 态**：`bg-[var(--color-paper)] text-stone-900 shadow-[var(--shadow-soft)]` + icon `text-blue-600`
- **NavLeafItem default**：`text-stone-700 hover:bg-[var(--color-paper)] hover:shadow-[var(--shadow-soft)]`
- **icon 17px**：`h-[17px] w-[17px]` —— 比 16px 略大半像素，更"实"
- **子项 tree-line**：父 `<div className="tree-line ml-4 mt-0.5 space-y-0.5">`，每个子 `tree-item flex items-center gap-2 rounded-lg py-1.5 pl-8 pr-3 text-[13.5px]`
- **子项 active**：`bg-blue-50/70 font-medium text-blue-700` + icon `text-blue-600`
- **NavGroup 计数 chip**：`font-mono text-[10px] tnum`，active 时 `text-blue-500`，default 时 `text-stone-400`
- **任务集子项 dot**：动态根据 set 状态映射 emerald/red/stone—— 用 `<Dot />` 组件作为 icon 槽
- **底部用户在线 dot**：`h-1.5 w-1.5 rounded-full bg-emerald-500`

## 关键代码

```tsx
<aside className="flex h-full w-60 flex-shrink-0 flex-col border-r border-stone-200/70 bg-[var(--color-warm-2)]">
  <div className="flex h-14 items-center gap-2.5 px-4">
    <img src={logo} className="h-7 w-7" />
    <span className="text-[15.5px] font-semibold tracking-tight text-stone-800">Waveflow</span>
    <button onClick={onToggle} className="ml-auto rounded-md p-1 text-stone-500 hover:bg-stone-200/60">
      <PanelLeftClose className="h-3.5 w-3.5" />
    </button>
  </div>
  <nav className="flex-1 space-y-0.5 overflow-auto px-3 pb-2 pt-1 text-[14px]">
    {TOP_ITEMS.map(item => <NavLeafItem ... />)}
    <div className="px-3 pb-1 pt-3 text-[11px] font-medium uppercase tracking-wider text-stone-400">
      调度
    </div>
    <NavGroupItem group={JOB_GROUP} ... />
    {/* ... */}
  </nav>
  <BottomUser />
</aside>
```

## 适配指南

- 分组头分隔："调度" / "系统" 两组——超过 8 个顶级项必分组，否则视觉混乱
- count 是必要："任务管理 / 12" 让用户一眼看到规模
- 折叠态切到 `icon-collapsed-sidebar` block（独立条目）
- 任务集子项用 `<Dot />` 子组件包 status-dot——动态色不要硬编码到 className

## 反模式

- ❌ 子项不走 tree-line —— L 钩消失，层级感塌方
- ❌ 顶级 active 同时高亮多个—— 用 `pathname === to || pathname.startsWith(to+'/')` 严格匹配
- ❌ count chip 用粗体—— 抢主菜单字
- ❌ brand 字体改 mono—— 失去"产品名"气质
