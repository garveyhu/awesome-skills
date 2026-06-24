---
id: components/typography-atoms/flywheel/kicker-collision-mark
type: component
name: 等宽 kicker + 撞色高亮 mark
description: 每节的 mono uppercase 小标签 + 词级撞色块高亮（薄荷青/活力黄托字）两个排版原子
platforms: [web]
theme: light
tags:
  aesthetic: [brutalist, editorial]
  mood: [confident, energetic]
  stack: [react-tailwind]
uses:
  - tokens/palettes/flywheel/memphis-collision
  - tokens/typography/pairs/flywheel/han-black-grotesk
preview: /preview/components/typography-atoms/flywheel/kicker-collision-mark
---

# 等宽 kicker + 撞色高亮 mark

> 两个高频排版原子：节前的 mono 小标签（kicker）+ 大标题里被撞色块托住的关键词（mark）

## 视觉特征

**kicker（节标签）**：
- `font-mono · 0.72rem · letter-spacing:0.18em · uppercase · color:ink-soft(#6E6A62)`
- 常配一个小序号圆：`h-9 w-9 rounded-full border-[2.5px] border-ink bg-ink text-mint font-mono`（黑底薄荷青号）
- 形态：`[①号圆] [KICKER 英文 · 中文副题]`，放大标题正上方

**collision mark（撞色高亮）**：
- `mark-mint`：`background:#16C79A · color:#FFF8EC · padding:0 0.18em · box-decoration-break:clone` —— 薄荷青块托米白字
- `mark-yellow`：`background:#FFD12E · color:#1A1A1A` —— 活力黄块托黑字
- 用在 `heading-xl` 大标题里点 1–2 个关键词，**像马克笔划重点**，跨撞色块也能 clone 续行
- 同一标题里 mark ≤ 2 处

## 与同 bucket 区分

- **vs 普通 `<mark>` 黄色高亮**：本条是**撞色块 + 反相文字**（mint 托米白 / 黄托黑），是品牌签名色，不是浏览器默认黄
- **vs 任意 badge/chip**：kicker 是"只读节标签"非交互；chip 是可点筛选件

## 核心代码

```tsx
export function Kicker({ index, label }: { index?: string; label: string }) {
  return (
    <div className="mb-3 flex items-center gap-3">
      {index && (
        <span className="flex h-9 w-9 items-center justify-center rounded-full border-[2.5px] border-ink bg-ink font-mono text-sm font-bold text-mint">
          {index}
        </span>
      )}
      <span className="font-mono text-[0.72rem] uppercase tracking-[0.18em] text-ink-soft">
        {label}
      </span>
    </div>
  );
}
```

```css
.mark-mint   { background: #16C79A; color: #FFF8EC; padding: 0 0.18em; box-decoration-break: clone; }
.mark-yellow { background: #FFD12E; color: #1A1A1A; padding: 0 0.18em; box-decoration-break: clone; }
```

## 适配指南

- kicker 英文大写 + 中文副题用 `·` 分隔：`THE ASSEMBLY LINE · 九阶段`
- mark 用在 `font-black` 大标题里才有冲击；正文里慎用（会乱）
- 暗场里 kicker 文字提到 `paper/60`，序号圆底保持 ink + mint
- 换脸：mark 色跟 accent（mint/yellow）走，反相文字跟 paper/ink 走

## 反模式

- ❌ kicker 用非等宽字体（失去"标签"质感）
- ❌ 一个标题里 mark 超过 2 处（变花）
- ❌ mark 文字不反相（黄底黑字 / 青底米白才清晰，别青底黑字）
- ❌ kicker 字间距太小（要 0.18em 才"展开"）
