---
id: blocks/filters/style-vault/sticky-chip-filter-panel
type: block
name: Sticky 玻璃感筛选面板
description: 260px sticky 玻璃 panel · 4 组 chip toggle（category / aesthetic / mood / stack）+ 清除态 + category-dot 6 色随类目切换
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/style-vault/slate-cyan-cool
  - tokens/typography/pairs/style-vault/inter-editorial-display
  - tokens/motion/style-vault/editorial-flow
preview: /preview/blocks/filters/style-vault/sticky-chip-filter-panel
---

# Sticky Chip Filter Panel

> Style Vault `/products` 左侧的 260px 玻璃感筛选面板 —— 4 组 chip toggle，全部用一种"圆角胶囊"形态承担 category / aesthetic / mood / stack 四种语义

## 视觉特征

**容器（玻璃感 panel）**：
- `<aside>` 外层 `sticky top-[88px] self-start` —— 88 = TopBar 72 + main pt-4 16，与右列卡片顶严格对齐（**top 必须等于自然位**，否则 sticky 立即生效会让 panel 比卡片低一截）
- 内层 `relative overflow-hidden rounded-[20px] border border-slate-200/80 bg-white/60 p-5 backdrop-blur-xl` —— 20px 圆角 + 60% 半透白底 + 强 backdrop-blur 模拟玻璃感
- 滚动容器 `max-h-[calc(100vh-132px)] overflow-y-auto pr-1` —— 132 = 88 (sticky 顶) + 44 (panel 顶距 + 底部留白)。pr-1 给 scrollbar 让 4px 让位

**Header 行**：
- 标题 `text-[11px] font-medium uppercase tracking-[0.18em] text-slate-500` —— 一致的 caption 节奏
- "清除"按钮 **conditional render**——任意 group 有选中时才出现，淡 slate-500 文字 hover slate-900
- 顶部 `mb-4`（16px）和首组 group 隔开

**Group 列表**：4 组依序 `category · 分类` / `aesthetic · 风格` / `mood · 氛围` / `stack · 技术栈`，每组 `mb-5 last:mb-0`。

每组 layout：
- 标题 `font-mono text-[10px] font-medium uppercase tracking-[0.18em] text-slate-500` —— mono 字族 + 比 panel 标题再小一档
- chip 容器 `flex flex-wrap gap-1`（4px 行间距，紧凑）

**Chip 形态**（核心设计）：
- 默认态 `border-slate-200/80 bg-white/70 text-slate-600` + hover `border-slate-300 bg-white text-slate-900`
- 选中态 `border-slate-900 bg-slate-900 text-white` —— 反相黑底
- 形状 `rounded-full border px-2.5 py-[3px] text-[11px]` —— 完全胶囊
- 过渡 `transition` 短促 200ms

**Category dot（独有）**：
- category 组的 chip 前面加 `1.5×1.5px rounded-full` 圆点
- 颜色按 6 类目切：productivity=purple / content=cyan / lifestyle=amber / social=pink / commerce=emerald / design=indigo
- 选中态时 dot 翻成白色（`background: '#ffffff'`）—— 因为黑底圆点已经看不出原色

## 与同 bucket 区分

- **vs `components/toggles/style-vault/editorial-underline-tab`**：那条是大栏目下划线 tab（互斥单选 + 视觉强）；本条是多组多选 chip toggle，化整为零
- **vs `components/tags-badges/style-vault/cyan-dot-meta-pill`**：那条是只读 meta 胶囊 + 玻璃感（kicker 用）；本条是交互 chip + 反相态，承担"筛选按钮"语义

## 核心代码

```tsx
'use client';
import { useState } from 'react';

type FilterKey = 'category' | 'aesthetic' | 'mood' | 'stack';
type FilterState = Record<FilterKey, string[]>;

const empty: FilterState = { category: [], aesthetic: [], mood: [], stack: [] };

export function StickyChipFilterPanel({
  value,
  onChange,
}: {
  value: FilterState;
  onChange: (next: FilterState) => void;
}) {
  const toggle = (g: FilterKey, slug: string) => {
    const curr = value[g];
    const next = curr.includes(slug) ? curr.filter((v) => v !== slug) : [...curr, slug];
    onChange({ ...value, [g]: next });
  };
  const active =
    value.category.length + value.aesthetic.length + value.mood.length + value.stack.length > 0;

  return (
    <aside className="sticky top-[88px] self-start">
      <div className="relative overflow-hidden rounded-[20px] border border-slate-200/80 bg-white/60 p-5 backdrop-blur-xl">
        <div className="max-h-[calc(100vh-132px)] overflow-y-auto pr-1">
          {/* Header */}
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-[11px] font-medium uppercase tracking-[0.18em] text-slate-500">
              筛选
            </h2>
            {active && (
              <button
                type="button"
                onClick={() => onChange(empty)}
                className="text-[11px] text-slate-500 transition hover:text-slate-900"
              >
                清除
              </button>
            )}
          </div>

          {/* 4 groups */}
          <FilterGroup title="category · 分类" values={CATEGORIES} selected={value.category} onToggle={(v) => toggle('category', v)} />
          <FilterGroup title="aesthetic · 风格" values={AESTHETICS} selected={value.aesthetic} onToggle={(v) => toggle('aesthetic', v)} />
          <FilterGroup title="mood · 氛围" values={MOODS} selected={value.mood} onToggle={(v) => toggle('mood', v)} />
          <FilterGroup title="stack · 技术栈" values={STACKS} selected={value.stack} onToggle={(v) => toggle('stack', v)} />
        </div>
      </div>
    </aside>
  );
}

function FilterGroup({ title, values, selected, onToggle }: {
  title: string;
  values: { slug: string; label: string; dot?: string }[];
  selected: string[];
  onToggle: (slug: string) => void;
}) {
  return (
    <div className="mb-5 last:mb-0">
      <div className="mb-2 font-mono text-[10px] font-medium uppercase tracking-[0.18em] text-slate-500">
        {title}
      </div>
      <div className="flex flex-wrap gap-1">
        {values.map((v) => {
          const on = selected.includes(v.slug);
          return (
            <button
              key={v.slug}
              type="button"
              onClick={() => onToggle(v.slug)}
              className={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-[3px] text-[11px] transition ${
                on
                  ? 'border-slate-900 bg-slate-900 text-white'
                  : 'border-slate-200/80 bg-white/70 text-slate-600 hover:border-slate-300 hover:bg-white hover:text-slate-900'
              }`}
            >
              {v.dot && (
                <span
                  className="h-1.5 w-1.5 shrink-0 rounded-full"
                  style={{ background: on ? '#ffffff' : v.dot }}
                />
              )}
              {v.label}
            </button>
          );
        })}
      </div>
    </div>
  );
}
```

## 适配指南

- **sticky `top-[88px]` 是硬约束**：必须等于"TopBar 高 + main pt"。不等就会出现"卡片顶 vs panel 顶差 N px"的视觉 bug，有过历史踩坑 commit `5dcc2aa` 修过
- 面板宽度建议 `260px` —— 太窄（< 220）chip 流换太碎；太宽（> 320）和右列内容抢比重
- 4 组顺序固定 `category → aesthetic → mood → stack`，从"语义最强"到"工程细节"递减
- 标题 caption 11px slate-500 vs group 标题 10px mono slate-500 —— **字号差 1px + 字族差 sans/mono** 是层级表达，不要拉大字差
- `clearAll` 按钮**仅当任一 group 有选中时**渲染 —— 不要常驻占位（panel 是高频扫视区域，任何冗余都会变噪音）
- chip active 反相到 `bg-slate-900 text-white` 时，category-dot 必须翻成白色，否则 cyan/purple 圆点在黑底上 contrast 不够
- 内层滚动容器 `max-h-[calc(100vh-132px)]` 要随 sticky `top` + panel 上下 padding 算 —— 公式 `100vh - sticky-top - panel-vertical-padding × 2`

## 反模式

- 不要把 `bg-white/60` 改成 `bg-white` 实白 —— 玻璃感 + 视觉层级靠半透 + blur
- 不要去掉 `backdrop-blur-xl` —— 透明面板上必须强 blur 才不糊
- 不要把 chip 改成 `rounded-md`（圆角矩形）—— 圆角胶囊是这套筛选的视觉签名
- 不要给 chip active 态加 cyan / 高饱和填色 —— 反相黑白是为了"让数据说话"，加色破坏 editorial 节奏
- 不要在 panel 里塞输入框 / 下拉 / range slider —— 只用 chip 一种交互形态保持极简
- 不要 sticky `top-` 和右列 `pt-` 数值不等 —— 永远会出对齐 bug
