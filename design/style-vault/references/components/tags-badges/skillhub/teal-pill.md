---
id: components/tags-badges/skillhub/teal-pill
type: component
name: Teal 胶囊标签
description: 圆角 full 的 teal 系分类标签，用于 skill 分类 / 版本号等轻量元信息
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/skillhub/skillhub-teal-mist
preview: /preview/components/tags-badges/skillhub/teal-pill
---

# Teal Pill

> 轻量元信息小胶囊——teal-50 底、teal-600 字、teal-100 边，11-12px 字号，一眼认出"这是个分类 / tag"

## 视觉特征

- 完整圆角 `rounded-full`
- 三色 teal 组合：底 `bg-teal-50`（近白绿）/ 字 `text-teal-600`（饱和适中）/ 边 `border border-teal-100`
- 字号 `text-[11px]` 最小、`text-xs` 常规，`font-semibold`（600）
- padding `px-2.5 py-0.5`（左右 10px 上下 2px），内容紧凑
- 超长用 `truncate max-w-[110px]` 切断
- 无阴影、无 hover（它是被动的信息胶囊，不是按钮）

## 核心代码

```tsx
type TealPillProps = {
  children: React.ReactNode;
  size?: 'xs' | 'sm';
  maxWidth?: number;
};

const TealPill = ({ children, size = 'xs', maxWidth = 110 }: TealPillProps) => (
  <span
    className={`inline-block font-semibold rounded-full
                bg-teal-50 text-teal-600 border border-teal-100
                ${size === 'xs' ? 'text-[11px] px-2.5 py-0.5' : 'text-xs px-3 py-1'}
                truncate`}
    style={{ maxWidth }}
  >
    {children}
  </span>
);
```

## 变体

### 版本号（slate 色系的兄弟变体）

```tsx
<span className="text-[10px] font-semibold text-slate-500 bg-slate-50
                 px-1.5 py-0.5 rounded">
  v{version}
</span>
```

版本号用 `rounded`（4px 非 full）区分"这是数据不是分类"。

### 可操作变体（配合 hover + cursor-pointer）

```tsx
<button className="inline-flex items-center gap-1 text-xs font-semibold
                   rounded-full bg-teal-50 text-teal-600 border border-teal-100
                   px-3 py-1 hover:bg-teal-100 transition-colors">
  <span>{tag.name}</span>
  <X size={10} />
</button>
```

## 适配指南

- 改色系：把 `teal-*` 全量替换为其它 tonal family（如 indigo-50/600/100）即可换基调，结构不变
- 长内容用 `max-w-[110px]` 截断，放旁边卡片内容区的右上角最合理
- 行内一条消息里最多出现 1-2 个 pill，多了变成"标签条"，该用 `blocks/display/tag-row` 那种容器
- 不要直接和 primary CTA 同行并列——胶囊是次级信号，CTA 是主级，一行里并列会抢视觉权

## 反模式

- 不要做成 hover 放大 / 跳色——胶囊是静态的
- 不要加 shadow——会显得廉价
- 不要超过 8 个字符直接展示——truncate 是对的选择
