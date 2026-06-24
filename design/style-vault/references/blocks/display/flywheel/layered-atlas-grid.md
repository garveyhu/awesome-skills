---
id: blocks/display/flywheel/layered-atlas-grid
type: block
name: 分层硬卡网格
description: 撞色头 + 硬阴影卡的响应式网格，每张卡一层/一类，卡内点状清单 —— 五区图/skill 地图同款
platforms: [web]
theme: light
tags:
  aesthetic: [brutalist, bento]
  mood: [confident, playful]
  stack: [react-tailwind]
uses:
  - tokens/palettes/flywheel/memphis-collision
  - tokens/shadow/flywheel/hard-offset-stack
  - components/display/flywheel/hard-shadow-card
preview: /preview/blocks/display/flywheel/layered-atlas-grid
---

# 分层硬卡网格

> 把"一组分层信息"摊成撞色头硬卡的响应式网格——每张卡一层/一类，撞色头标题 + 卡内点状清单。五区地图、skill 地图都是它

## 视觉特征

- 容器 `grid grid-cols-1 gap-4 md:grid-cols-2`（或 3 列）；条目多的卡 `md:col-span-2` 占满一行
- **每张硬卡**（`card-hard` · 2.5px 边 + 6px 硬阴影 · `p-0` 让头出血）：
  - **撞色头条**：`flex justify-between px-4 py-2`，底色按层取撞色（`bg-blue/mint/red/yellow/ink` + 反相文字），左 `font-display font-black` 层名，右 `font-mono text-[11px]` 小注
  - **卡体**：`grid gap-x-4 gap-y-1.5 p-4`，每行 `[小圆点] [mono 条目名] [灰色一句话]`
  - 圆点二态区分语义：实心 mint = 主/本类；空心 `border-blue bg-paper` = 次/共享
- 顶部常配**统计条**：几张小硬卡并排，大号数字（`text-4xl font-black`）+ 说明 + 图例点
- 撞色头每层不同色，但**同屏控制在 3–4 个撞色**，不是每卡都艳

## 与同 bucket 区分

- **vs 普通 bento 卡网格**：本条**强制撞色头 + 硬阴影 + 点状清单**三件套，是分类/分层信息的承载，不是图片瀑布
- **vs `components/display/flywheel/hard-shadow-card`**：那是单卡原子；本条是"多卡 + 撞色头 + 清单"的布局块，复用它

## 核心代码

```tsx
type Layer = { name: string; note: string; accent: 'yellow' | 'blue' | 'red' | 'mint' | 'ink'; items: { label: string; role: string; shared?: boolean }[] };
const HEAD: Record<Layer['accent'], string> = {
  yellow: 'bg-yellow text-ink', blue: 'bg-blue text-paper', red: 'bg-red text-paper',
  mint: 'bg-mint text-ink', ink: 'bg-ink text-paper',
};

export function AtlasGrid({ layers }: { layers: Layer[] }) {
  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
      {layers.map((l) => (
        <div key={l.name} className={`flex flex-col overflow-hidden border-[2.5px] border-ink bg-paper shadow-[6px_6px_0_#1A1A1A] ${l.items.length > 5 ? 'md:col-span-2' : ''}`}>
          <div className={`flex items-center justify-between px-4 py-2 ${HEAD[l.accent]}`}>
            <span className="font-display text-lg font-black">{l.name}</span>
            <span className="font-mono text-[11px] opacity-80">{l.note}</span>
          </div>
          <div className={`grid gap-x-4 gap-y-1.5 p-4 ${l.items.length > 5 ? 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3' : 'grid-cols-1'}`}>
            {l.items.map((it) => (
              <div key={it.label} className="flex items-baseline gap-2">
                <span className={`mt-1.5 h-2 w-2 shrink-0 rounded-full ${it.shared ? 'border-[2px] border-blue bg-paper' : 'bg-mint'}`} />
                <code className="shrink-0 font-mono text-[13px] font-bold text-ink">{it.label}</code>
                <span className="truncate text-xs text-ink/60">{it.role}</span>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
```

## 适配指南

- 撞色头按层轮色但同屏 ≤ 3–4 撞色；信息密度大的层用 `col-span-2 + 多列内格`
- 圆点实/空心承担"本类 vs 共享/次级"二元语义，配一句图例
- 统计条放网格上方：大数字 + 中性说明，数字用 `font-black` 思源黑
- 条目名用 mono（像代码/标识），一句话职责用 `text-ink/60` 退让

## 反模式

- ❌ 每张卡都用高饱和撞色头（花，要控 3–4 色 + 退让色）
- ❌ 软阴影卡（破坏 brutalist）
- ❌ 清单不用点状二态（区分不出主/次）
- ❌ 撞色头文字不反相（黄底白字 / 蓝底黑字看不清）
