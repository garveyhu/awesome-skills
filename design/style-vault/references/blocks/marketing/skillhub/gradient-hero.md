---
id: blocks/marketing/skillhub/gradient-hero
type: block
name: 流光渐变 Hero
description: 超大号 Hero 标题 + 某一强调词用 4 色流动渐变 + 双 CTA（追光主 + ghost 次）
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/skillhub/skillhub-teal-mist
  - tokens/typography/pairs/skillhub/inter-jetbrains-duo
  - tokens/motion/skillhub/gentle-flow
  - components/buttons/skillhub/border-trace-cta
preview: /preview/blocks/marketing/skillhub/gradient-hero
---

# Gradient Hero

> SkillHub 首页 hero——大号粗体标题把最后一个短语（"流动起来"）用 4 色流光渐变显示，配一对 CTA

## 视觉特征

- 容器：`max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16`
- 标题尺寸：`text-4xl md:text-5xl lg:text-6xl font-extrabold tracking-tight leading-[1.15]`，文字色 `text-gray-900`
- 强调词：`bg-clip-text text-transparent` + `linear-gradient` + `background-size: 300% 100%` + `animate-[flow-right_14s_linear_infinite]`
- 副标题：`text-gray-400 text-lg mb-10`
- CTA 区：`flex items-center justify-center gap-4`
  - 左：`BorderTraceButton`（追光黑底，品牌 CTA）
  - 右：`border border-gray-300 hover:border-gray-400 rounded-xl text-gray-700 text-sm font-bold px-7 py-3 active:scale-95`（ghost）
- 入场：`motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} duration: 0.3`

## 核心代码

```tsx
import { ArrowRight } from 'lucide-react';
import { motion } from 'framer-motion';
import { BorderTraceButton } from '../components/buttons/BorderTraceButton';

interface GradientHeroProps {
  prefix: string;            // "让 AI 技能 "
  flowWord: string;          // "流动起来"
  subtitle: string;
  primaryLabel: string;
  onPrimary?: () => void;
  secondaryLabel?: string;
  onSecondary?: () => void;
  /** 渐变色序列，首尾同色以实现无缝循环 */
  gradient?: string[];
  durationSec?: number;
}

export const GradientHero = ({
  prefix,
  flowWord,
  subtitle,
  primaryLabel,
  onPrimary,
  secondaryLabel = '探索全部',
  onSecondary,
  gradient = ['#14b8a6', '#06b6d4', '#0ea5e9', '#f472b6'],
  durationSec = 14,
}: GradientHeroProps) => {
  const stops = [...gradient, ...gradient, gradient[0]].join(', ');

  return (
    <section className="relative overflow-hidden">
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
        <div className="flex flex-col items-center text-center max-w-3xl mx-auto">
          <motion.div
            className="w-full"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-extrabold
                           text-gray-900 tracking-tight leading-[1.15] mb-5">
              {prefix}
              <span
                className="bg-[length:300%_100%] bg-clip-text text-transparent
                           animate-[flow-right_14s_linear_infinite]"
                style={{
                  backgroundImage: `linear-gradient(90deg, ${stops})`,
                  animationDuration: `${durationSec}s`,
                }}
              >
                {flowWord}
              </span>
            </h1>

            <p className="text-gray-400 text-lg mb-10">{subtitle}</p>

            <div className="flex items-center justify-center gap-4">
              <BorderTraceButton onClick={onPrimary}>{primaryLabel}</BorderTraceButton>

              {secondaryLabel && (
                <button
                  onClick={onSecondary}
                  className="inline-flex items-center gap-2 px-7 py-3
                             border border-gray-300 hover:border-gray-400
                             text-gray-700 text-sm font-bold rounded-xl
                             transition-all duration-200 hover:bg-white/60 active:scale-95"
                >
                  {secondaryLabel}
                  <ArrowRight size={16} />
                </button>
              )}
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
};
```

### 全局 keyframe（放在 index.less/css）

```css
@keyframes flow-right {
  from { background-position: 300% 50%; }
  to   { background-position: 0% 50%; }
}
```

## 使用示例

```tsx
<GradientHero
  prefix="让 AI 技能 "
  flowWord="流动起来"
  subtitle="发现、安装、分享高质量的 AI Skill 技能包"
  primaryLabel="发布 Skill"
  onPrimary={() => navigate('/publish')}
  secondaryLabel="探索全部技能"
  onSecondary={scrollToGrid}
/>
```

## 适配指南

- 标题 H1 固定在 3 档响应式（4xl/5xl/6xl），再大/再小都会打破"气势感 vs 可读性"的平衡
- 渐变至少 4 色，不要少于 3 色——否则动的时候像"色块闪"而不是"流"
- 渐变色组合保持"同温度"：给 teal + cyan + sky + rose 是科技 + 温暖的撞色；换 rose-orange-amber 会偏活泼；换 cyan-blue-indigo 会偏冷
- 强调词字符数 2-6 个最佳；太长的话流光循环周期会拉长
- `durationSec` 慢于 10s 会显得有点装腔，快于 8s 又显得不沉稳；12-16s 是舒适区
- 副标题用 `text-gray-400` 不要重——否则会和主标题争

## 反模式

- 不要在主标题里动多个词——流光只能 1 处，否则视觉飞了
- 不要在渐变里混黑或白——clip-text 会看起来"缺一块"
- 不要把 CTA 放成并列 2 个 primary（都是追光或都是黑底）——主 + ghost 的对照才是对的
- 不要在 hero 背景上再叠动效背景——流光词已经是动的中心
