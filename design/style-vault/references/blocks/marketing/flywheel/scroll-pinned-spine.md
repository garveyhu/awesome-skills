---
id: blocks/marketing/flywheel/scroll-pinned-spine
type: block
name: 钉滚脊梁穿行交互
description: signature moment —— 钉住的暗场节，滚动时数据令牌沿脊梁穿过各阶段、详情卡切换、产物累积
platforms: [web]
theme: dark
tags:
  aesthetic: [brutalist, editorial]
  mood: [confident, energetic]
  stack: [react-tailwind]
uses:
  - tokens/palettes/flywheel/memphis-collision
  - tokens/motion/flywheel/reveal-pin-scroll
  - tokens/shadow/flywheel/hard-offset-stack
  - components/display/flywheel/hard-shadow-card
preview: /preview/blocks/marketing/flywheel/scroll-pinned-spine
---

# 钉滚脊梁穿行交互

> 整页**唯一的 signature moment**：一段钉住的暗场，滚动推进时一个数据令牌沿"脊梁线"横穿各阶段，详情卡随之切换、右侧产物逐项累积——把一条流程"演"给你看

## 视觉特征

- **结构**：外层超高容器 `height:~520vh`（≈ 阶段数 ×55vh）+ 内层 `sticky top-0 h-screen flex flex-col justify-center`——滚 5+ 屏，画面钉住、内容随进度变
- **暗场**：`bg-ink`（#1A1A1A）+ 极淡点阵，文字 `text-paper`，signature 薄荷青在这里最跳
- **脊梁线**：一条 `h-1.5 bg-paper/15` 横线 + `bg-mint` 进度填充（宽度 = scroll 进度）；一个黄色"数据令牌"（`bg-yellow border-[2.5px] border-ink`）骑在填充末端横移，带标签
- **阶段节点排**：N 个圆点等距排开，当前点放大填色（创意段 mint / 机械段 blue 双色分段，虚线 band 标 `①–④ / ⑤–⑨`）
- **详情卡**（左，硬阴影卡）：随 `active` 阶段 keyed 重渲（`motion.div key={active}` 淡入横移，**不用 AnimatePresence wait**），显当前阶段名/职责/输入→输出/调用项
- **产物累积**（右，硬阴影卡）：N 行清单，`i<=active` 的点亮 ✓（mint），其余暗——"看着产物一路攒齐"
- 底部 `滚动推进 · 令牌 = 贯穿全程的 X` 提示

## 与同 bucket 区分

- **vs `blocks/layout/flywheel/numbered-section-shell`**：那条是静态承载节（90% 的节）；本条是**带钉滚交互的特例**，整页只一处
- **vs 普通 marketing hero**：本条不是首屏，是中段的"机制演示"，靠 scroll 驱动而非自动播放

## 核心代码

```tsx
import { useRef, useState } from 'react';
import { motion, useScroll, useTransform, useMotionValueEvent } from 'framer-motion';

export function PinnedSpine({ stages }: { stages: { name: string; artifact: string }[] }) {
  const ref = useRef<HTMLElement>(null);
  const { scrollYProgress } = useScroll({ target: ref, offset: ['start start', 'end end'] });
  const [active, setActive] = useState(0);
  useMotionValueEvent(scrollYProgress, 'change', (v) =>
    setActive(Math.min(stages.length - 1, Math.max(0, Math.floor(v * stages.length * 0.999)))),
  );
  const fill = useTransform(scrollYProgress, [0, 1], ['0%', '100%']);

  return (
    <section ref={ref} id="pipeline" className="relative bg-ink" style={{ height: '520vh' }}>
      <div className="sticky top-0 flex h-screen flex-col justify-center overflow-hidden px-6">
        {/* 脊梁线 + 进度填充 + 令牌 */}
        <div className="relative mx-auto h-1.5 w-full max-w-6xl rounded-full bg-paper/15">
          <motion.div className="absolute left-0 top-0 h-full rounded-full bg-mint" style={{ width: fill }} />
          <motion.div className="absolute top-1/2 z-20 -translate-x-1/2 -translate-y-1/2" style={{ left: fill }}>
            <span className="flex h-7 w-7 items-center justify-center rounded-full border-[2.5px] border-ink bg-yellow font-mono text-[9px] font-bold">JSON</span>
          </motion.div>
        </div>
        {/* 节点排 */}
        <div className="mx-auto mt-3 flex w-full max-w-6xl justify-between">
          {stages.map((s, i) => (
            <div key={s.name} className="flex flex-1 flex-col items-center">
              <div className={`flex h-9 w-9 items-center justify-center rounded-full border-[2.5px] font-mono text-sm font-bold transition-all ${i === active ? 'scale-125 border-ink bg-mint text-ink' : i < active ? 'border-mint bg-paper/90 text-ink' : 'border-mint bg-transparent text-paper/50'}`}>{i + 1}</div>
              <span className={`mt-2 text-[11px] font-bold ${i === active ? 'text-paper' : 'text-paper/40'}`}>{s.name}</span>
            </div>
          ))}
        </div>
        {/* 详情卡 keyed 重渲 + 产物累积 —— 见适配指南 */}
        <div className="mx-auto mt-8 grid w-full max-w-6xl grid-cols-1 gap-5 md:grid-cols-[1.6fr_1fr]">
          <motion.div key={active} initial={{ opacity: 0, x: 24 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.35 }} className="border-[2.5px] border-ink bg-paper p-6 shadow-[6px_6px_0_#1A1A1A]">
            <h3 className="text-3xl font-black text-ink">{active + 1} · {stages[active].name}</h3>
          </motion.div>
          <div className="border-[2.5px] border-ink bg-paper/95 p-5 shadow-[3px_3px_0_#1A1A1A]">
            {stages.map((s, i) => (
              <div key={s.name} className={`flex items-center gap-2 ${i <= active ? '' : 'opacity-25'}`}>
                <span className={`flex h-5 w-5 items-center justify-center rounded-full text-[10px] font-bold ${i <= active ? 'bg-mint text-ink' : 'bg-paper-2 text-ink/40'}`}>{i <= active ? '✓' : i + 1}</span>
                <span className="font-mono text-xs text-ink">{s.artifact}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
```

## 适配指南

- 容器高度 = `阶段数 × ~55vh`；阶段切换详情卡**用 keyed `motion.div`（重渲）不用 `AnimatePresence mode="wait"`**——快跳会留空白帧（踩过）
- 令牌横移 `left` 直接绑 `useTransform` 的百分比 motion value，和脊梁填充同步
- 双色分段（创意/机械）用虚线 band 在脊梁上方标范围，节点边框跟着分色
- 详情卡 + 产物卡都用硬阴影卡（暗场上 paper 卡 + 黑阴影）
- scroll-spy 把整个钉滚 section 当一个 id，钉住期间它一直高亮（中线窄带 rootMargin 成立）

## 反模式

- ❌ 整页造多个 signature（只许一个，其余静态节让路）
- ❌ `AnimatePresence mode="wait"` 做阶段卡（快跳空帧）
- ❌ 令牌用 `width` 动画而非 `transform`（卡）
- ❌ 钉滚容器太矮（< 阶段数×40vh，步进太挤分不清）
- ❌ 暗场里不给 paper 卡背板（详情/产物卡直接黑底文字，糊）
