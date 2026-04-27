---
id: tokens/motion/skillhub/gentle-flow
type: token
name: 温和流动动效系统
description: framer-motion 入场 + hover 浮起 + active 缩放 + CSS 关键帧流光 + SVG 追光
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses: []
preview: /preview/tokens/motion/skillhub/gentle-flow
---

# Gentle Flow Motion

> 动效语言：进入轻柔（fade + translate）、悬浮浮起（y: -4）、点击回弹（scale 0.95-0.97）、装饰流光（渐变滚动 + SVG 追光）

## Tokens

### 入场动效（framer-motion）

```tsx
// 模块入场：20px 上浮 + fade
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.3 }}
/>

// 滚动入场：24px 上浮 + fade，进入视口触发一次
<motion.section
  initial={{ opacity: 0, y: 24 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, margin: '-60px' }}
  transition={{ duration: 0.3 }}
/>

// 列表逐项入场：每项延迟 20ms
<motion.div
  initial={{ opacity: 0 }}
  whileInView={{ opacity: 1 }}
  viewport={{ once: true }}
  transition={{ duration: 0.2, delay: idx * 0.02 }}
/>
```

### Hover 浮起 / Tap 缩放

```tsx
// 卡片浮起 4px
<motion.div
  whileHover={{ y: -4 }}
  transition={{ duration: 0.2 }}
/>

// CTA 按钮回弹
<motion.button
  whileHover={{ scale: 1.03 }}
  whileTap={{ scale: 0.97 }}
/>

// Tailwind 形态——无 framer-motion 时降级
className="active:scale-95 transition-transform"
```

### CSS 关键帧

```css
/* 渐变流光——Hero 强调词 / 装饰条 */
@keyframes flow-right {
  from { background-position: 300% 50%; }
  to   { background-position: 0% 50%; }
}
/* 用法: animate-[flow-right_14s_linear_infinite]（Hero 标题）
         animate-[flow-right_20s_linear_infinite]（装饰条，慢一点）  */

/* 骨架微光 */
@keyframes shimmer {
  0%, 100% { background-position: 100% 50%; }
  50%      { background-position: 0% 50%; }
}

/* 元素入场 */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

### SVG 追光（按钮边缘）

见 `components/buttons/skillhub/border-trace-cta`。核心模式：

```tsx
// 用 ResizeObserver 测真实周长，用 strokeDasharray 画出"亮段 + 空段"，
// 用 <animate attributeName="stroke-dashoffset"> 让它沿边线跑。
// 两条同速反色（cyan-200 #a5f3fc + purple-300 #c4b5fd），dur=3s / 4.5s
```

### 过渡时长 / 缓动

| 场景 | duration | easing |
|---|---|---|
| Hover 浮起 / 缩放 | 200ms | ease-out |
| 入场 | 300ms | ease-out |
| 列表逐项 | 200ms + 20ms × idx | ease-out |
| 大装饰流光 | 14 / 20s | linear |
| SVG 追光 | 3 / 4.5s | linear |
| Active 缩放 | 即时 | spring 默认 |

## 使用示例

```tsx
// 典型 Skill 卡片
<motion.div
  whileHover={{ y: -4 }}
  transition={{ duration: 0.2 }}
  className="bg-white rounded-2xl p-5 border border-gray-200
             hover:border-teal-200 hover:shadow-md transition-all"
>
  ...
</motion.div>

// 典型 Section 滚动入场
<motion.section
  initial={{ opacity: 0, y: 24 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, margin: '-60px' }}
>
  ...
</motion.section>
```

## 适配指南

- framer-motion 与 Tailwind 过渡并用时，不要同时设 `transition` class 和 `transition` prop——会打架。
- 大段装饰流光（14s+）不影响性能，但同屏同时 3+ 个不同步的 flow 会让人眼累——留 1 个就够
- SVG 追光仅给"发布 Skill"这种品牌级 CTA 用，泛滥会掉档次
- 列表逐项入场只在用户感知到"列表变化"时用（搜索结果切换、分页），初次渲染全体入场会拖慢首屏

## 反模式

- 不要 Hover 浮起超过 6px——过了就变成弹跳，不再是"浮"
- 不要用 bounce/spring easing 配 Inter 的理性字形——气质不合
- 不要在 Modal / Popover 里叠加入场动画——antd 已经给了，重复会打两次
