---
id: blocks/nav/chameleon/borderless-bookmark-rail
type: block
name: 224px 无边书签竖条二级导航
description: 与内容同 warm 表面的无边左导航 - UPPERCASE 分组头 + 圆角药丸叶子 + 选中态浅蓝药丸 + 左侧蓝色书签竖条(霓虹微光)
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
- components/typography-atoms/waveflow/meta-caps-mono-pair
- tokens/palettes/waveflow/warm-paper-ink-blue
preview: /preview/blocks/nav/chameleon/borderless-bookmark-rail
---

# Chameleon 无边书签竖条导航

> 224px 二级左导航——**与内容区同 `var(--color-warm)`(#fafaf7) 表面，无 border、无独立底色**。自上而下：UPPERCASE 分组头（10.5px font-bold tracking-0.06em stone-400）+ 圆角 10px 药丸叶子。**signature = 选中态**：浅蓝药丸（`bg-blue-50` + `text-blue-700` + `font-semibold`）叠加**左侧 3px 蓝色书签竖条带霓虹微光**（`absolute top-2 bottom-2 left-0 w-[3px] rounded-r-[3px] bg-blue-600 shadow-[0_0_8px_rgba(59,130,246,0.45)]`）。当前域可见叶子 ≤ 1 时整个 aside 返回 null（如知识库单项域，顶部 tab 已表明所在域，内容直接铺满）。

## 视觉特征

- **aside `flex w-56(224px) flex-shrink-0 flex-col overflow-y-auto bg-[var(--color-warm)](#fafaf7) px-3(12px) py-4(16px)`** —— 无 border、无 shadow，融进内容表面
- **分组头 `px-3 pb-1.5(6px) text-[10.5px] font-bold tracking-[0.06em] text-stone-400(#a8a29e) uppercase`**：首组 `pt-0`、其余 `pt-5(20px)`
- **叶子 Link `relative flex items-center gap-3(12px) rounded-[10px] px-3(12px) py-2(8px) text-[13px] font-medium transition`**
  - active：`bg-blue-50(#eff6ff) font-semibold text-blue-700(#1d4ed8)`
  - default：`text-stone-600(#57534e) hover:bg-stone-200/40 hover:text-stone-900`
- **【signature 书签竖条】** active 时绝对定位 span：`absolute top-2 bottom-2 left-0 w-[3px] rounded-r-[3px] bg-blue-600(#2563eb) shadow-[0_0_8px_rgba(59,130,246,0.45)]` —— 霓虹蓝微光从竖条向左晕开
- **叶子 icon `h-4 w-4(16px) flex-shrink-0`**：active=`text-blue-600(#2563eb)` / default=`text-stone-400(#a8a29e)`
- **标签 span `flex-1 truncate`**
- **`allVisible.length <= 1` 时整个 aside `return null`** —— 单项域不渲染左栏

## 核心代码

```tsx
<aside className="flex w-56 flex-shrink-0 flex-col overflow-y-auto bg-[var(--color-warm)] px-3 py-4">
  {groups.map((g, i) => (
    <div key={g.i18nKey}>
      <div className={cn('px-3 pb-1.5 text-[10.5px] font-bold tracking-[0.06em] text-stone-400 uppercase',
        i === 0 ? 'pt-0' : 'pt-5')}>
        {g.fallbackTitle}
      </div>
      {g.children.map(leaf => <LeafItem key={leaf.to} leaf={leaf} active={leaf.to === activeTo} />)}
    </div>
  ))}
</aside>

const LeafItem = ({ leaf, active }) => (
  <Link to={leaf.to} className={cn(
    'relative flex items-center gap-3 rounded-[10px] px-3 py-2 text-[13px] font-medium transition',
    active ? 'bg-blue-50 font-semibold text-blue-700'
           : 'text-stone-600 hover:bg-stone-200/40 hover:text-stone-900')}>
    {active && <span className="absolute top-2 bottom-2 left-0 w-[3px] rounded-r-[3px] bg-blue-600 shadow-[0_0_8px_rgba(59,130,246,0.45)]" />}
    <Icon className={cn('h-4 w-4 flex-shrink-0', active ? 'text-blue-600' : 'text-stone-400')} />
    <span className="flex-1 truncate">{leaf.fallbackTitle}</span>
  </Link>
);
```

## 适配指南

- 域 / 分组 / 叶子从 nav-config 单一数据源取（top-bar 与 secondary-nav 共用，避免漂移）
- 「唯一选中」跨分组只亮一个：用 `activeLeafTo`（最长命中叶子）算出 activeTo
- 单项域（仅一个可见叶子）直接 `return null`，不要渲染只有一项的左栏
- 书签竖条只在 active 时出现，是这个导航的记忆点——不要给 hover 也加竖条

## 与 waveflow/tree-line-sidebar 区分

| 维度 | waveflow tree-line-sidebar | 本条 borderless-bookmark-rail |
|------|----------------------------|-------------------------------|
| 宽度 | 240px | 224px |
| 边框/底 | `border-r border-stone-200/70` + `bg-warm-2` 独立底色 | **无 border + 无独立底（同内容区 `bg-warm`）** |
| 层级表达 | tree-line L 钩子项（父 `tree-line ml-4`、子 `pl-8` + L 形连线） | **扁平无 tree-line**（分组头 + 平铺叶子） |
| active 态 | `bg-paper + soft shadow` 悬浮语 + icon 蓝 | **浅蓝药丸 + 左侧 3px 蓝书签竖条（霓虹微光）** |
| 附件 | count chip（`font-mono text-[10px]`）+ 底部 user dropdown（头像 + 在线 dot + Settings） | 无 count chip、**无底部 user**（账户迁到顶栏） |
| brand | 自带 brand 段（logo + 折叠按钮） | 无 brand（品牌在顶栏） |

选条原则：要「全局后台树形侧栏（含 brand + 多级展开 + count + 底部账户）」用 waveflow；要「域内二级导航（无边融表面 + 药丸书签竖条 + 账户已在顶栏）」用本条。

## 反模式

- ❌ 给 aside 加 border / 独立底色——破坏「融进内容表面」的无边语义
- ❌ 单项域仍渲染只有一项的左栏——浪费 224px，应 return null
- ❌ active 用整块 shadow 悬浮——那是 waveflow 语，本条是药丸 + 书签竖条
- ❌ 书签竖条不带 shadow 微光——失去 signature 的霓虹质感
