---
id: blocks/feedback/skillhub/skeleton-card
type: block
name: 骨架卡片
description: 和 skill-card / 其它主卡等尺寸的 animate-pulse 骨架占位
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/skillhub/skillhub-teal-mist
  - tokens/motion/skillhub/gentle-flow
preview: /preview/blocks/feedback/skillhub/skeleton-card
---

# Skeleton Card

> 列表/网格加载时的占位骨架。和对应实际卡**同尺寸 + 同圆角 + 同 border**，只是内部替换为纯白底 + animate-pulse。视觉上"形还在，内容在生成"。

## 视觉特征

- 纯白底 `bg-white`
- 同实际卡的 `rounded-2xl` + `border border-gray-100`
- `h-48`（和 skill-card 的高度对齐）
- `animate-pulse` 让整体透明度在 1 <-> 0.5 间脉冲
- **不要**画假文字线条——极简路线只做容器脉冲

## 核心代码

```tsx
interface SkeletonCardProps {
  height?: number;       // 默认 192 (h-48)
  rounded?: string;      // 默认 rounded-2xl
  count?: number;        // 生成几个
}

export const SkeletonCard = ({ height = 192, rounded = 'rounded-2xl', count = 6 }: SkeletonCardProps) => (
  <>
    {Array.from({ length: count }).map((_, i) => (
      <div
        key={i}
        className={`bg-white border border-gray-100 ${rounded} animate-pulse`}
        style={{ height }}
      />
    ))}
  </>
);
```

## 使用示例

```tsx
{isLoading ? (
  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
    <SkeletonCard count={6} />
  </div>
) : (
  <SkillGrid skills={skills} />
)}
```

## 变体

### 带占位线条（较复杂骨架）

只在"用户期望看到 10+ 秒加载"的场景才用；常规小加载保持极简。

```tsx
<div className="bg-white border border-gray-100 rounded-2xl p-5 animate-pulse">
  <div className="flex gap-3 mb-3">
    <div className="w-10 h-10 rounded-full bg-gray-100" />
    <div className="flex-1 space-y-2 pt-1">
      <div className="h-3 w-32 rounded bg-gray-100" />
      <div className="h-2.5 w-16 rounded bg-gray-100" />
    </div>
  </div>
  <div className="h-3 w-full rounded bg-gray-100 mb-2" />
  <div className="h-3 w-4/5 rounded bg-gray-100" />
</div>
```

## 适配指南

- 骨架 height 必须和实际卡等高，否则加载完成后会"跳"
- Tailwind 的 `animate-pulse` 是 opacity 1↔.5 不是 shimmer——skillhub 的基调偏克制，pulse 比 shimmer 更合
- count 建议 6（2 行 × 3 列），太多骨架抢视觉
- 网格容器同等 gap + cols 规则要跟实际卡一致
- 骨架期间不要显示 "加载中..." 文字——pulse 本身就是状态指示

## 反模式

- 不要做成深灰（`bg-slate-200`）——太像 stackoverflow 那种硬骨架
- 不要给骨架加 shadow——静态无阴影是本 style 的基调
- 不要让骨架播报信息（如显示"已加载 50%"）——越多装饰越显得慢
