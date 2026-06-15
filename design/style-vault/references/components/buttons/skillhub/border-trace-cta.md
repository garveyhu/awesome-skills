---
id: components/buttons/skillhub/border-trace-cta
type: component
name: 追光边框 CTA
description: 黑底 CTA 外缘跑 SVG 双环追光（cyan 主线 + purple 副线），品牌级召唤按钮
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/skillhub/skillhub-teal-mist
  - tokens/motion/skillhub/gentle-flow
preview: /preview/components/buttons/skillhub/border-trace-cta
---

# Border Trace CTA

> SkillHub 首页"发布 Skill"那个 signature 按钮——黑底 `#2b2b2b` + SVG 光点绕边一圈 3 秒 + 二级 purple 光 4.5 秒错开

## 视觉特征

- 按钮本体：`rounded-2xl` + 黑底 `#2b2b2b` + 白字 + `font-bold text-sm` + `px-8 py-3`
- 外层 SVG 在按钮外缘 `inset: -3px`（多 6px 空间）画追光
- 主追光：cyan-200 `#a5f3fc`，2px 宽，占 20% 边长，3 秒转一圈
- 副追光：purple-300 `#c4b5fd`，1.5px 宽，占 10% 边长，4.5 秒转一圈，错开 2s 起跑
- 静态底边：slate-400 `#94a3b8` 透明 0.2 的 1px 描边（不随转）
- 内置细微渐变：按钮背景叠一层 opacity-0.12 的横向 cyan→purple→cyan 渐变，20s 慢漂移
- hover/tap：framer-motion `scale 1.03 / 0.97`

## 核心代码

```tsx
import { Sparkles } from 'lucide-react';
import { motion } from 'framer-motion';
import { useEffect, useRef, useState } from 'react';

export const BorderTraceButton = ({
  onClick,
  icon = <Sparkles size={15} />,
  children,
}: {
  onClick?: () => void;
  icon?: React.ReactNode;
  children: React.ReactNode;
}) => {
  const btnRef = useRef<HTMLButtonElement>(null);
  const pathRef = useRef<SVGRectElement>(null);
  const [perim, setPerim] = useState(400);

  // ResizeObserver 实时测量按钮实际周长（尺寸变化时重算）
  useEffect(() => {
    const measure = () => {
      if (pathRef.current) setPerim(pathRef.current.getTotalLength());
    };
    measure();
    if (!btnRef.current) return;
    const ro = new ResizeObserver(() => requestAnimationFrame(measure));
    ro.observe(btnRef.current);
    return () => ro.disconnect();
  }, []);

  const trail = perim * 0.2;
  const gap = perim - trail;

  return (
    <div className="relative">
      <svg
        className="absolute inset-[-3px] w-[calc(100%+6px)] h-[calc(100%+6px)]
                   pointer-events-none overflow-visible"
      >
        {/* 测量 rect（不渲染） */}
        <rect ref={pathRef}
          x="3" y="3" width="calc(100% - 6px)" height="calc(100% - 6px)"
          rx="16" ry="16" fill="none" stroke="none" />

        {/* 静态底边 */}
        <rect x="3" y="3" width="calc(100% - 6px)" height="calc(100% - 6px)"
          rx="16" ry="16" fill="none"
          stroke="#94a3b8" strokeOpacity="0.2" strokeWidth="1" />

        {/* 主追光 (cyan-200) */}
        <rect x="3" y="3" width="calc(100% - 6px)" height="calc(100% - 6px)"
          rx="16" ry="16" fill="none"
          stroke="#a5f3fc" strokeWidth="2" strokeLinecap="round"
          strokeDasharray={`${trail} ${gap}`} opacity="0.7">
          <animate attributeName="stroke-dashoffset"
            from="0" to={`${-perim}`} dur="3s" repeatCount="indefinite" />
        </rect>

        {/* 亮头（overlay 提亮追光前端）*/}
        <rect x="3" y="3" width="calc(100% - 6px)" height="calc(100% - 6px)"
          rx="16" ry="16" fill="none"
          stroke="#e0f2fe" strokeWidth="1.5" strokeLinecap="round"
          strokeDasharray={`${trail * 0.25} ${perim - trail * 0.25}`} opacity="0.9">
          <animate attributeName="stroke-dashoffset"
            from="0" to={`${-perim}`} dur="3s" repeatCount="indefinite" />
        </rect>

        {/* 副追光 (purple-300)，错开起跑 */}
        <rect x="3" y="3" width="calc(100% - 6px)" height="calc(100% - 6px)"
          rx="16" ry="16" fill="none"
          stroke="#c4b5fd" strokeWidth="1.5" strokeLinecap="round"
          strokeDasharray={`${trail * 0.5} ${perim - trail * 0.5}`} opacity="0.4">
          <animate attributeName="stroke-dashoffset"
            from="0" to={`${-perim}`} dur="4.5s" repeatCount="indefinite" begin="-2s" />
        </rect>
      </svg>

      <motion.button
        ref={btnRef}
        onClick={onClick}
        className="relative inline-flex items-center gap-2.5 px-8 py-3
                   text-white text-sm font-bold rounded-2xl overflow-hidden"
        whileHover={{ scale: 1.03 }}
        whileTap={{ scale: 0.97 }}
      >
        <span className="absolute inset-0 bg-[#2b2b2b]" />
        {/* 内部慢速横向渐变流（20s）加深氛围 */}
        <span
          className="absolute inset-0 opacity-[0.12] bg-[length:300%_100%]
                     animate-[flow-right_20s_linear_infinite]"
          style={{
            backgroundImage:
              'linear-gradient(90deg, transparent 0%, rgba(165,243,252,0.8) 20%, transparent 40%, rgba(196,181,253,0.6) 60%, transparent 80%, rgba(165,243,252,0.8) 100%)',
          }}
        />
        <span className="relative z-10 inline-flex items-center gap-2">
          {icon}
          <span className="tracking-wide">{children}</span>
        </span>
      </motion.button>
    </div>
  );
};
```

## 原理要点

1. **ResizeObserver 测真实周长**：按钮文字/尺寸可能变，`getTotalLength()` 得到当前 rect 的周长作为 dasharray 的基准，否则尺寸变化后追光会错位
2. **`strokeDasharray={trail} {gap}`**：画一段亮 + 一段空，`stroke-dashoffset` 动画让这段"亮段"绕边跑
3. **三层叠加**：底边（静）+ 主追光（`#a5f3fc` 粗）+ 亮头（`#e0f2fe` 细，只占追光的 25%）+ 副追光（`#c4b5fd`）错开节奏
4. **`overflow-visible`**：SVG 默认 clip，追光在 `inset: -3px` 位置必须显式 overflow-visible

## 使用指南

- 全站只给 1-2 个地方用：首页 Hero 的主 CTA、可能再加一处"发布"按钮
- 不要放在行内流里——必须有足够留白让追光"跑得起来"
- 需要响应式：`width: 6px; height: 6px` 这种硬编码 inset 在小屏上需检查是否溢出
- 暗底环境下（如 slate-950 底）把内层 `bg-[#2b2b2b]` 改 `bg-[#1a1a1a]` + 追光色改 cyan-300 / purple-400 提对比

## 反模式

- 不要同时给 2 个追光按钮都 3s 节奏——同步会变成节拍器，不是流光
- 不要把追光色替换成 teal-*——teal 是平面上的主色，追光应该是"破格"的异色（cyan/purple）
- 不要用 `<div>` 伪元素 + 旋转 + mask 实现追光——rect + strokeDasharray 是稳定跨浏览器的唯一正路
- 不要去掉 ResizeObserver——按钮文本变化后追光立即错位，一眼被发现
