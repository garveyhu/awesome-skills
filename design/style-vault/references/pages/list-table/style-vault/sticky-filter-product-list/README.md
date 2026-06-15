---
id: pages/list-table/style-vault/sticky-filter-product-list
type: page
name: Sticky 筛选 + 行卡产品集
description: TopBar + 260px sticky 玻璃感筛选面板 + 1fr 浮起作品照行卡列表（space-y-4 垂直堆叠）+ 双态空提示
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - blocks/nav/style-vault/sticky-platform-topbar
  - blocks/filters/style-vault/sticky-chip-filter-panel
  - blocks/display/style-vault/floating-cover-row
  - tokens/layout/_shared/scroll-state-system
preview: /preview/pages/list-table/style-vault/sticky-filter-product-list
---

# Sticky Filter Product List

> Style Vault `/products` 路由完整骨架 —— 左 sticky 筛选 + 右纵向排列的"浮起作品照"行卡

## 视觉特征

```
┌──────────────────────────────────────────────────┐
│ TopBar  72px sticky                               │
├──────────────────────────────────────────────────┤
│ main · pt-4 (16px)                               │
│ ┌──────┬─────────────────────────────────────┐   │
│ │ 260  │ ┌───────────────────────────────────┐ │ │
│ │ px   │ │ floating-cover-row                │ │ │
│ │ 玻璃 │ ├───────────────────────────────────┤ │ │
│ │ 筛选 │ │ floating-cover-row                │ │ │
│ │ panel│ ├───────────────────────────────────┤ │ │
│ │      │ │ floating-cover-row                │ │ │
│ │ sticky│└───────────────────────────────────┘ │ │
│ └──────┴─────────────────────────────────────┘   │
└──────────────────────────────────────────────────┘
```

### 双栏 grid

- 容器 `main className="px-10 pb-20 pt-4"` —— `pt-4` (16px) 是右列卡片顶距，**必须** 等于左列 sticky 顶
- 内层 `<div className="grid items-start gap-8" style={{ gridTemplateColumns: '260px 1fr' }}>` —— 260px 固定 + 1fr 弹性
- gap-8（32px）是栏间距；`items-start` 让两栏从顶对齐

### 左 · sticky filter panel

直接套 `blocks/filters/style-vault/sticky-chip-filter-panel`，无变化。

**关键**：sticky `top-[88px]` = TopBar(72) + main pt-4(16)。这个 88 是**唯一正确值**：
- 大于 88（如 96）→ sticky 立即生效，panel 比卡片低 8px → 永远视觉对齐 bug
- 小于 88（如 72）→ sticky 卡到 TopBar 玻璃感面下面，露出来的部分被 TopBar 半透白模糊

参考 commit `5dcc2aa` 修过 96→88 的对齐 bug。

### 右 · 行卡纵列

`<div className="space-y-4">` —— 卡间距 16px 垂直堆叠。每条 `floating-cover-row`：
- 整体 380×220 + 92%/86% 浮起白卡 + 真实组件缩略
- hover 走 `.sv-card` 三层柔投影浮起

### 显式优先级排序

`PRODUCT_PRIORITY` 数组写死显示顺序（如 `['products/style-vault', 'products/skillhub', 'products/acme-cold-saas']`）。未列出的产品按 registry 自然序落在末尾。

理由：vault 自身条目数 < 30 且需要"突出新作 / 主推"语义，**不靠时间戳**（registry 没存）也**不靠字母序**（按字母 acme 永远第一）。显式数组维护成本低且语义清晰。

### 平台过滤 + 筛选交叉

按 platform context（来自 TopBar 平台切换）筛掉不符合的产品 → 用 `matchProductFilters` 再筛。两层独立。

### 空态分级

```tsx
{platformMatched.length === 0 ? (
  <Empty>当前「{platform}」下暂无产品</Empty>
) : visible.length === 0 ? (
  <Empty>当前筛选条件下无匹配产品</Empty>
) : (
  <div className="space-y-4">{/* rows */}</div>
)}
```

两个不同空态文案 —— **平台维度无产品**（用户的设备选择无内容）vs **筛选条件无匹配**（已加筛选条件）—— 文案差异是用户排错的关键线索。

空态卡片：`rounded-2xl border border-dashed border-slate-200 bg-white p-16 text-center text-slate-400`。

## 滚动行为

走 [`tokens/layout/_shared/scroll-state-system`](../../../../tokens/layout/_shared/scroll-state-system.md) 的 4 场景契约。本页落到的是**场景 B + C**：

- **B · Click 入详情** —— 用户从行卡点进 `/products/<slug>`，PUSH 到全新 pathname → `byPath` miss → `target=0` + 30 帧钉顶。详情页一定置顶不留尾
- **C · 后退还原** —— 详情页按返回 / 浏览器后退键回到 `/products` → `useNavigationType()='POP'` → `byKey` 精准还原到刚才的滚动条位置（不是 top）

产品集本页通常 ≤ 12 条，**不挂 `useInfiniteList`**（场景 D 不适用）—— 数据量不到一屏的列表挂懒加载等于多余复杂度。

## 适配指南

- 260px 是甜区——更窄（< 220）chip 流换得太碎；更宽（> 320）右列 row 卡比例失调
- `gap-8` (32px) **不要**收紧——筛选 chip 是密集色块区，右侧 row 卡是大留白区，过渡需要呼吸
- pt + sticky top **必须配对**（参考上面 88px 的核心约束）
- 当未来产品数 ≥ 12 时，应该补一个右上"X 个产品"计数 / 按钮组，不要直接堆 row（会变成长得没头）—— 但这是后续迭代，**现在不要预设**

## 反模式

- 不要把 sticky panel 改成 fixed positioning —— sticky 与 grid 的 `items-start` 联动，能在短列表场景自动放弃 sticky；fixed 永远脱离流
- 不要把 row 卡改成 grid 网格（如 2/3 列）—— 行卡的"浮起作品照"宽度（380px）是被 380 + 1fr 这个布局绑死的，并排会让封面变窄
- 不要给 panel 和 row 加共同 hover 联动（如 hover row 高亮 panel 的对应 chip）—— 加了交互复杂度但用户从不需要
- 不要在 panel 顶部塞搜索框 —— Style Vault 的产品集不是大数据量场景，4 组 chip 已足
