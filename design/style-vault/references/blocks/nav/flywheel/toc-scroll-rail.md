---
id: blocks/nav/flywheel/toc-scroll-rail
type: block
name: 右侧悬浮 TOC 导航
description: 右侧悬浮硬阴影卡的章节目录，全标签常显 + scroll-spy 高亮当前节 + 首页隐藏，点击平滑跳转
platforms: [web]
theme: light
tags:
  aesthetic: [brutalist, minimal]
  mood: [confident]
  stack: [react-tailwind]
uses:
  - tokens/palettes/flywheel/memphis-collision
  - tokens/shadow/flywheel/hard-offset-stack
  - tokens/motion/flywheel/reveal-pin-scroll
preview: /preview/blocks/nav/flywheel/toc-scroll-rail
---

# 右侧悬浮 TOC 导航

> 长内容站的章节目录：右侧悬浮的硬阴影卡，全标签常显、scroll-spy 高亮当前节、**首页隐藏滚进正文才淡入**、点击平滑跳转

## 视觉特征

- **悬浮卡**：`fixed right-5 top-1/2 -translate-y-1/2 z-40`，`rounded-2xl border-[2.5px] border-ink bg-paper/85 p-2.5 shadow-[4px_4px_0_#1A1A1A] backdrop-blur-md`——自带 paper 背板，**在暗场节上也清晰可读**（关键：浮层跨明暗背景必须有底板）
- **首页隐藏**：`active === 'top'` 时 `opacity-0 translate-x-4 pointer-events-none`，否则淡入——hero 上不显示导航
- **每行**：`[左竖条] [mono 序号] [标签]`；当前节 = 薄荷青竖条 `w-[3px] bg-mint` + `bg-paper-2` 底 + `font-black text-ink`；其余 `bg-ink/15` 竖条 + `text-ink-soft`，hover 加深
- 全标签常显（不靠 hover），靠**字重/色阶/薄荷青竖条**做主次，不拥挤
- 仅 `lg:` 及以上显示；移动端隐藏
- scroll-spy：`IntersectionObserver` rootMargin `-48% 0px -48% 0px`（中线窄带），对超高钉滚节也只高亮一个

## 与同 bucket 区分

- **vs 顶部 navbar**：本条是**右侧竖排目录**，服务长滚动内容站，不占顶部横向空间
- **vs `components/indicators/flywheel/scroll-progress-bar`**：那条是顶部一条进度线（读到哪了）；本条是可点的章节目录（去哪）

## 核心代码

```tsx
import { useEffect, useState } from 'react';

function useScrollSpy(ids: readonly string[], rootMargin = '-48% 0px -48% 0px') {
  const [active, setActive] = useState(ids[0] ?? '');
  useEffect(() => {
    const els = ids.map((i) => document.getElementById(i)).filter(Boolean) as HTMLElement[];
    const ob = new IntersectionObserver(
      (es) => es.forEach((e) => e.isIntersecting && setActive(e.target.id)),
      { rootMargin, threshold: 0 },
    );
    els.forEach((el) => ob.observe(el));
    return () => ob.disconnect();
  }, [ids, rootMargin]);
  return active;
}

export function TocRail({ sections }: { sections: { id: string; num: string; label: string }[] }) {
  const active = useScrollSpy(sections.map((s) => s.id));
  const show = active !== 'top';
  const jump = (id: string) => document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  return (
    <nav className={`fixed right-5 top-1/2 z-40 hidden -translate-y-1/2 flex-col gap-0.5 rounded-2xl border-[2.5px] border-ink bg-paper/85 p-2.5 shadow-[4px_4px_0_#1A1A1A] backdrop-blur-md transition-all duration-300 lg:flex ${show ? 'opacity-100' : 'pointer-events-none translate-x-4 opacity-0'}`}>
      {sections.map((s) => {
        const on = active === s.id;
        return (
          <button key={s.id} onClick={() => jump(s.id)} className={`group flex items-center gap-2 rounded-lg py-1 pl-1.5 pr-3 text-left transition-colors ${on ? 'bg-paper-2' : 'hover:bg-paper-2/60'}`}>
            <span className={`h-4 w-[3px] shrink-0 rounded-full ${on ? 'bg-mint' : 'bg-ink/15 group-hover:bg-ink/40'}`} />
            <span className={`font-mono text-[9px] ${on ? 'text-mint' : 'text-ink-soft/70'}`}>{s.num}</span>
            <span className={`whitespace-nowrap text-[12px] ${on ? 'font-black text-ink' : 'font-medium text-ink-soft group-hover:text-ink'}`}>{s.label}</span>
          </button>
        );
      })}
    </nav>
  );
}
```

## 适配指南

- **首个 section id 用 `top`**（hero），导航据 `active==='top'` 隐藏
- 浮层**必须有 `bg-paper/85 + backdrop-blur`** 背板——否则在暗场节上文字消失（踩过：纯浮文字在 ink 节看不见）
- 全标签常显时靠字重 + 色阶 + 竖条做主次，别再加常显 emoji/图标（拥挤）
- 超长距离跳转的 `scroll-behavior:smooth` 会扫屏，可接受；要瞬跳就去掉 smooth

## 反模式

- ❌ 浮层无背板（暗场节上文字看不见）
- ❌ 标签靠 hover 才显（用户要的是常显 + 主次）
- ❌ scroll-spy 用元素整框 isIntersecting（多节同时命中会乱跳）——要中线窄带 rootMargin
- ❌ 移动端硬塞这条竖排（挤）——`lg:` 以上才显
