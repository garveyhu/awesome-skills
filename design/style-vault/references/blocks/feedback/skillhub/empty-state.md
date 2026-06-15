---
id: blocks/feedback/skillhub/empty-state
type: block
name: 空态
description: 虚线容器 + 灰色 icon + 标题 + 一行提示，无 CTA 的克制空态
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/skillhub/skillhub-teal-mist
preview: /preview/blocks/feedback/skillhub/empty-state
---

# Empty State

> 搜索无结果 / 列表空 / 评论空等场景的统一空态——**白底 + dashed border + gray-300 icon + 1 标题 + 1 提示**，不配 CTA（CTA 放在容器外）。

## 视觉特征

- 容器：`bg-white rounded-2xl border border-gray-200 border-dashed p-16 text-center`
- Icon：`w-12 h-12 text-gray-300 mx-auto mb-3`（Lucide 48px，淡到若有若无）
- 标题：`text-base font-bold text-gray-900 mb-1`
- 提示：`text-gray-500 text-[13px]`

## 核心代码

```tsx
import { Box, type LucideIcon } from 'lucide-react';

interface EmptyStateProps {
  icon?: LucideIcon;
  title: string;
  hint?: string;
  action?: React.ReactNode;   // 可选：在空态内或外放一个 CTA
}

export const EmptyState = ({ icon: Icon = Box, title, hint, action }: EmptyStateProps) => (
  <div className="bg-white rounded-2xl border border-gray-200 border-dashed p-16 text-center">
    <Icon className="w-12 h-12 text-gray-300 mx-auto mb-3" />
    <h3 className="text-base font-bold text-gray-900 mb-1">{title}</h3>
    {hint && <p className="text-gray-500 text-[13px]">{hint}</p>}
    {action && <div className="mt-4">{action}</div>}
  </div>
);
```

## 使用示例

### 无搜索结果

```tsx
<EmptyState
  icon={Box}
  title="未找到 Skill"
  hint="尝试更换搜索词或重置过滤器。"
/>
```

### 无评论

```tsx
<EmptyState
  icon={MessageCircle}
  title="还没有评论"
  hint="第一个留下想法的人就是你。"
/>
```

### 带 CTA（发布引导）

```tsx
<EmptyState
  icon={Sparkles}
  title="你还没发布过实践"
  hint="把你踩过的坑、发现的技巧分享给大家"
  action={
    <DarkPrimaryCta size="md" onClick={() => navigate('/practice/create')}>
      发布第一篇
    </DarkPrimaryCta>
  }
/>
```

## 适配指南

- 虚线 border + 白底是关键信号——跟实际卡（实线 border）区分"这里没内容"
- padding `p-16`（64px）大得起来才显得"空"——不要改 `p-8` 让它看起来像个小卡
- icon 用 `text-gray-300` 近乎融入背景——它是陪衬不是主角；**不要**用 teal 或其它彩色
- 标题 `text-base font-bold` 不要 uppercase——空态本身已经视觉薄了，meta 字会更弱
- CTA 要放在 `mt-4` 分隔开，不要塞在 hint 旁行内

## 反模式

- 不要用 `<Empty>` Antd 默认（带小花图）——Antd 的 emoji 风不匹配 skillhub 克制基调
- 不要在空态里放 illustration / 大插画——和整站极简不搭
- 不要配 "刷新 / 重试" 按钮（除非真是错误态）——空态 ≠ 错误态，错误态用 `error-banner`
