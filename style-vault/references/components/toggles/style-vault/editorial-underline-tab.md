---
id: components/toggles/style-vault/editorial-underline-tab
type: component
name: 编辑式 Tab 下划线
description: 2px scaleX 渐变下划线（cyan→slate-900）的 editorial 风 tab，配色文转黑表达 active
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind, html-tailwind]
uses:
  - tokens/palettes/style-vault/slate-cyan-cool
  - tokens/motion/style-vault/editorial-flow
preview: /preview/components/toggles/style-vault/editorial-underline-tab
---

# Editorial Underline Tab

> 编辑感的 tab 切换：依靠"色文 + scaleX 下划线"双语义，无 background fill / 无 border / 无 chip

## 视觉特征

两档尺寸：
- **小（13px）** —— 用在 TopBar 平台切换（Web / iOS / Android）+ TopBar 主导航（浏览 / 产品集，路径激活）
- **大（16px · `--lg`）** —— 用在 sticky CategoryTabs（总览 / 风格 / 页面 / 模块 / 组件 / 原语）

文字色三态：
- idle `text-slate-400` (#94a3b8)
- hover `text-slate-700` (#334155)
- active `text-slate-900` (#0f172a)

下划线：
- `2px` 高，`scaleX(0)` → `scaleX(1)`，`transform-origin: left center`
- 填充 `linear-gradient(90deg, #0891b2, #0f172a)`（cyan-700 → slate-900）—— 这条渐变是 style-vault 的视觉签名
- transition `transform 320ms cubic-bezier(0.2, 0.7, 0.2, 1)`

间距：
- 小档 `padding-bottom: 10px`
- 大档 `padding-bottom: 14px`
- tab 之间 `gap-7`（小）/ `gap-8`（大）

## 与同 bucket 区分

- **vs antd `<Tabs>` 自带样式**：antd 默认是 box-shadow 下划线，本条用 scaleX gradient——节奏和颜色都不同
- **vs `components/buttons/skillhub/teal-pill`**（实色 chip）：chip 抢视觉、合适内容卡片切换；本条低调、合适大栏目导航

## 核心代码

```tsx
'use client';
import clsx from 'clsx';

interface UnderlineTabProps {
  size?: 'sm' | 'lg';
  active?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}

export function EditorialUnderlineTab({
  size = 'sm',
  active,
  onClick,
  children,
}: UnderlineTabProps) {
  return (
    <button
      type="button"
      data-on={active}
      onClick={onClick}
      className={clsx(
        'sv-underline-tab whitespace-nowrap',
        size === 'lg' && 'sv-underline-tab--lg',
      )}
    >
      {children}
    </button>
  );
}
```

依赖的全局 CSS（来自项目 `index.css`）：

```css
.sv-underline-tab {
  position: relative;
  font-size: 13px;
  font-weight: 500;
  color: #94a3b8;
  letter-spacing: 0.02em;
  padding-bottom: 10px;
  transition: color 200ms ease;
}
.sv-underline-tab:hover { color: #334155; }
.sv-underline-tab[data-on="true"] { color: #0f172a; }
.sv-underline-tab::after {
  content: ""; position: absolute; left: 0; right: 0; bottom: 0;
  height: 2px; border-radius: 2px;
  background: linear-gradient(90deg, #0891b2, #0f172a);
  transform: scaleX(0); transform-origin: left center;
  transition: transform 320ms cubic-bezier(0.2, 0.7, 0.2, 1);
}
.sv-underline-tab[data-on="true"]::after { transform: scaleX(1); }
.sv-underline-tab--lg { font-size: 16px; padding-bottom: 14px; }
```

## 适配指南

- 一组 tab 的 `gap` 必须 ≥ 28px——下划线 scaleX 时不会和邻居粘连
- 配 `sticky top-x bg-[#fafafa]/90 backdrop-blur-md` 容器使用——切换时 active 下划线不被 hero 吞掉
- 下划线渐变 **不要**改方向（始终 cyan→slate-900）；不要换颜色——这条渐变是身份标志
- 在 dark panel 上要把字色翻转：idle `text-slate-500` / hover `text-slate-300` / active `text-white`

### `items-center` 容器对称居中

`.sv-underline-tab` 自带 `padding-bottom: 10px`（小档）/ `14px`（大档）给下划线让位。在 `items-baseline` 容器（如 TopBar 中央 platform pill / CategoryTabs 顶部 baseline-aligned 行）里没问题——baseline 和文字底对齐，padding-bottom 在 baseline 下方不影响视觉。

但放进 `items-center` 容器（如 TopBar 主导航 nav，需要和 36px 高的搜索胶囊一起垂直居中）时，盒子相对文字不对称 → 文字偏上。**必须补对称的 padding-top**：

```tsx
{/* 小档配 items-center */}
<Link className="sv-underline-tab pt-2.5" ...>浏览</Link>
{/* 大档配 items-center（少见） */}
<NavLink className="sv-underline-tab sv-underline-tab--lg pt-3.5" ...>...</NavLink>
```

`pt-2.5` = 10px，对应小档 padding-bottom；`pt-3.5` = 14px，对应大档。

## 反模式

- 不要给 active 加 background fill（违反编辑感）
- 不要把 transition origin 改成 center——left-origin 是"翻页"质感的关键
- 不要把 height 撑到 3px+——视觉变粗破坏精致
- 不要换非 cubic-bezier(0.2,0.7,0.2,1) 的 easing（spring/bounce 都会让导航跳脱）
