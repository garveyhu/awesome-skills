---
id: blocks/display/style-vault/preview-thumb-card
type: block
name: 虚拟视口预览缩略卡
description: 1440×900 虚拟视口缩放成卡片缩略 + 悬停内容缩放 + type 圆点元信息 + 收藏按钮
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/style-vault/slate-cyan-cool
  - tokens/typography/pairs/style-vault/inter-editorial-display
  - tokens/motion/style-vault/editorial-flow
  - tokens/layout/_shared/fixed-cols-row
preview: /preview/blocks/display/style-vault/preview-thumb-card
---

# Preview Thumb Card

> 把 1440×900 虚拟视口的真实组件按容器宽度等比缩成卡片缩略——而不是渲染截图

## 视觉特征

**结构**：`<article>` 包外，`overflow-hidden rounded-xl border border-slate-200/80 bg-white`

**预览区**：
- 高度按 type 分档（product/style/page=220 / block=180 / component/token=160）
- 内层 `1440×900` 真实组件，`origin-top-left + transform: scale(W/1440)`
- `useLayoutEffect` 同步测量后再设 scale，避免首帧用猜测值——首次切分类时 40%+ scale 差距非常显眼
- ResizeObserver 持续监听容器宽度变化（响应式列数变化跟着重算）
- hover 时内容 `scale(1.05) translateZ(0)`，origin top center，600ms

**信息区**：
- 顶行：type-dot（6 色之一）+ type 文字 + platform chip · 右侧收藏 / 全屏 icon-only btn
- 标题 `text-[15px] font-semibold leading-snug text-slate-900`，font-display 拉印刷感
- 描述 `text-[12px] line-clamp-2 text-slate-500`
- 底部 tags chip：bg-slate-100 / px-1.5 py-0.5 / text-[10px] —— **超过 5 个就 slice**

**hover 效果**：
- 卡片本体 `translate3d(0,-4px,0)` + 三层柔投影（`0 2px 6px / 0 14px 32px / 0 24px 48px`）
- 同步预览内容 scale 1.05（origin top center）
- 整体 transition 400-600ms cubic-bezier(0.2,0.7,0.2,1)

## 核心代码骨架

```tsx
const PREVIEW_VIRTUAL_WIDTH = 1440;
const PREVIEW_VIRTUAL_HEIGHT = 900;
const SIZE_BY_TYPE = {
  product: { h: 220 }, style: { h: 220 }, page: { h: 220 },
  block:   { h: 180 }, component: { h: 160 }, token: { h: 160 },
};

export function PreviewThumbCard({ item, onClick }) {
  const ref = useRef<HTMLDivElement>(null);
  const [scale, setScale] = useState<number | null>(null);

  useLayoutEffect(() => {
    const el = ref.current; if (!el) return;
    const apply = (w: number) => w > 0 && setScale(w / PREVIEW_VIRTUAL_WIDTH);
    apply(el.getBoundingClientRect().width);
    const ro = new ResizeObserver((es) => { for (const e of es) apply(e.contentRect.width); });
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  return (
    <article onClick={onClick} className="sv-card group ...">
      <div ref={ref} style={{ height: SIZE_BY_TYPE[item.type].h }} className="relative overflow-hidden bg-slate-50">
        {scale !== null && PreviewComp && (
          <div
            className="sv-card-preview-inner pointer-events-none absolute origin-top-left"
            style={{
              width: PREVIEW_VIRTUAL_WIDTH, height: PREVIEW_VIRTUAL_HEIGHT,
              transform: `scale(${scale})`,
            }}
            aria-hidden
            inert  /* ← 禁焦点：见下方"防焦点劫持" */
          >
            <PreviewComp />
          </div>
        )}
      </div>
      {/* type-dot meta · title · desc · tags */}
    </article>
  );
}
```

依赖全局 CSS（`.sv-card`，从 `tokens/motion/style-vault/editorial-flow`）：

```css
.sv-card { transition: transform 400ms ..., box-shadow 400ms ..., border-color 400ms ...; }
.sv-card:hover { transform: translate3d(0,-4px,0); box-shadow: 0 2px 6px ..., 0 14px 32px ..., 0 24px 48px ...; }
.sv-card .sv-card-preview-inner { transition: transform 600ms ...; transform-origin: top center; }
.sv-card:hover .sv-card-preview-inner { transform: scale(1.05) translateZ(0); }
```

## 防焦点劫持（重要）

预览容器 **必须** `inert`。原因：部分预览组件本身有 `autoFocus`（如命令面板的搜索 input、对话历史 modal 的输入框、列表行的 inline rename input）。卡片懒加载渲染瞬间，input 自动获得焦点 → 浏览器立即 "scroll focused element into view" → **整页滚到那张新卡的位置**。用户视角是"懒加载触发，页面突然跳到末尾"。

`pointer-events-none` 阻止鼠标交互但**不阻止程序焦点**；`aria-hidden` 影响无障碍但**不阻止焦点**；只有 `inert` 把整个子树从焦点 / 交互树里完全摘除。React 19 原生支持 JSX `inert` 属性。

独立预览页 `/preview/<id>` 是直接 mount，不在 `inert` 父级里，autoFocus 还能正常工作 —— 只有缩略图 mount 上下文需要禁。

## 适配指南

- 卡片宽度变化场景（用 `useCols` 做断点列数）必须 ResizeObserver——否则切分类会闪
- type 圆点 6 色（purple/rose/indigo/cyan/emerald/amber）—— 颜色映射来自 `palette.type-dot`，**不要**自己改
- 在 BrowsePage 中用 `gridTemplateColumns: repeat(${cols}, minmax(0,1fr))` —— 不要用 columns CSS（masonry 会破坏 useLayoutEffect 同步测量）
- 预览容器**必须** `inert`（见上方）—— 不加这条会让带 autoFocus 的 preview 在懒加载时把整页拽到末尾

## 反模式

- 不要用 `<img src=".png" />` 静态截图——切换语言/数据时缩略图脱节，且失去 hover 内容缩放
- 不要给卡片加 `scale(1.02)` 整卡放大（违反 editorial-flow motion）
- 不要在 hover 切边框颜色——本设计是"投影制造层次"
- 不要把虚拟视口改成 1280/1920——下游 preview tsx 都按 1440 写
- 不要省略 `inert`，也不要换成 `tabIndex={-1}`（只阻止 Tab 导航，不阻止 `autoFocus` 的程序聚焦）
