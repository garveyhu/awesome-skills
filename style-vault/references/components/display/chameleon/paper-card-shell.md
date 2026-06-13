---
id: components/display/chameleon/paper-card-shell
type: component
name: Paper 基础卡片原语
description: rounded-lg + stone-200 边 + paper 底 + shadow-card 的基础卡片，含 Header/Title/Description/Content/Footer 组件群（p-5 / space-y-1.5）
platforms:
- web
theme: light
tags:
  aesthetic:
  - minimal
  mood:
  - calm
  stack:
  - shadcn-radix
uses:
- tokens/shadow/waveflow/soft-card-pop-trio
preview: /preview/components/display/chameleon/paper-card-shell
---

# Paper 基础卡片原语

> Chameleon 全站卡片的最底层原语（`card.tsx`）。shadcn 风格的 `Card` + 子组件群（`CardHeader` / `CardTitle` / `CardDescription` / `CardContent` / `CardFooter`），全 `forwardRef`。视觉基因：`rounded-lg`（8px 圆角）+ `border-stone-200`（暖灰发丝边）+ `bg-[var(--color-paper)]`（纯白纸底，主题变量）+ `shadow-card`（极淡双层投影）。所有更复杂的卡（metric / set / 配置面板）都基于它叠加。

## 视觉特征

- **Card**：`rounded-lg border border-stone-200 bg-[var(--color-paper)] text-stone-900 shadow-card`
  - radius lg = 8px
  - border = 1px `#e7e5e0`（stone-200）
  - bg = `var(--color-paper)`（默认 `#ffffff`）
  - `shadow-card` = `0 1px 3px rgb(0 0 0 / 5%), 0 2px 8px rgb(0 0 0 / 3%)`（双层极淡，几乎贴地）
- **CardHeader**：`flex flex-col space-y-1.5 p-5`（竖排，子间距 6px，内边距 20px）
- **CardTitle**：`text-base font-semibold leading-none tracking-tight`（16px / 600 / 行高贴紧 / 字距收紧）
- **CardDescription**：`text-xs text-stone-500`（12px 暖灰）
- **CardContent**：`p-5 pt-0`（20px，**上内边距清零**——紧贴 Header）
- **CardFooter**：`flex items-center p-5 pt-0`（横排居中，上内边距清零）

## Tokens

局部结构 token：

```json
{
  "card": {
    "radius": "8px",
    "border": "1px solid #e7e5e0",
    "bg": "var(--color-paper)",
    "bgDefault": "#ffffff",
    "text": "#1c1917",
    "shadow": "0 1px 3px rgb(0 0 0 / 5%), 0 2px 8px rgb(0 0 0 / 3%)",
    "padding": "20px",
    "headerGap": "6px",
    "title": { "size": "16px", "weight": 600, "tracking": "-0.02em" },
    "description": { "size": "12px", "color": "#78716c" }
  }
}
```

## 核心代码

```tsx
export const Card = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref}
      className={cn('rounded-lg border border-stone-200 bg-[var(--color-paper)] text-stone-900 shadow-card', className)}
      {...props} />
  ),
);

// 子组件群
<CardHeader className="flex flex-col space-y-1.5 p-5">
  <CardTitle className="text-base font-semibold leading-none tracking-tight">…</CardTitle>
  <CardDescription className="text-xs text-stone-500">…</CardDescription>
</CardHeader>
<CardContent className="p-5 pt-0">…</CardContent>
<CardFooter className="flex items-center p-5 pt-0">…</CardFooter>
```

## 适配指南

- 内容紧贴标题用 Header + Content（Content 的 `pt-0` 与 Header 的 `p-5` 衔接）；只放内容不要标题时直接 `<CardContent className="pt-5">`（手动补回上边距，见 DistributionCard）
- `shadow-card` 是「贴地」级投影——不要换成 shadow-lg/xl，Chameleon 卡片刻意压低高度感，靠 border 而非阴影分层
- bg 用 `var(--color-paper)` 而非 `bg-white`——主题切换（暖纸/纯白）时跟变量走
- 需要更立体的浮层（弹窗/下拉）才用 `shadow-pop`，常驻卡片永远 `shadow-card`

## 反模式

- ❌ 卡片用 `rounded-xl`/`rounded-2xl`——基础卡固定 `rounded-lg`(8px)，xl 留给 StatTile/MiniStat 等指标卡
- ❌ `bg-white` 硬编码——破坏主题，用 `bg-[var(--color-paper)]`
- ❌ 堆 `shadow-lg`——Chameleon 全站克制投影，靠 stone-200 边线分层
- ❌ CardContent 不清 pt——会与 Header 的 p-5 叠出双倍上边距
