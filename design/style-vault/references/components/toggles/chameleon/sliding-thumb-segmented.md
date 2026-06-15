---
id: components/toggles/chameleon/sliding-thumb-segmented
type: component
name: 弹性滑块分段控件
description: 二/多选一分段控件 · pill thumb 在选项间弹性 cubic-bezier 滑动 (ResizeObserver 实测定位) · 选中态 themeable primary-700 文字
platforms:
- web
theme: light
tags:
  aesthetic:
  - minimal
  mood:
  - confident
  stack:
  - shadcn-radix
uses:
- tokens/palettes/chameleon/themeable-8x4-system
preview: /preview/components/toggles/chameleon/sliding-thumb-segmented
---

# Chameleon Sliding-Thumb Segmented Control

> chameleon 全站表单「二选一 / 多选一」统一控件——一块白色 pill thumb 漂在 stone-100 凹槽里，切换时用带回弹的 cubic-bezier 平滑滑到目标选项下方。thumb 位置/尺寸不写死，由 `ResizeObserver` 实测每个选项 button 的 `getBoundingClientRect` 算出 `translate(x,y) + width/height`，所以无论选项文字宽窄都贴合。signature = **带回弹的滑块 thumb**（`duration-300 ease-[cubic-bezier(.34,1.4,.5,1)]`，曲线含 >1 的 1.4 故末段轻微过冲再回弹）。

## 视觉特征

- **tablist 容器**：`relative flex w-fit items-center gap-0.5(2px) rounded-lg(8px) border border-stone-200(#e7e5e4) bg-stone-100/70(70% #f5f5f4) p-0.5(2px)`
  - `relative` 承载滑块 · `w-fit` 块级独占行但宽度收紧到内容
- **滑块 thumb**（`absolute`，ResizeObserver 测量定位）：`pointer-events-none absolute left-0 top-0 z-0 rounded-md(6px) bg-paper(#fffefb) shadow-sm transition-[transform,width,height] duration-300 ease-[cubic-bezier(.34,1.4,.5,1)]`
  - inline style：`transform: translate(${x}px, ${y}px)` + `width` + `height`（全来自实测）
  - 测量时减去左/上各 1px 边框（absolute 原点是 padding-box，offset 量来自 border-box）
- **选项 button**：`relative z-10 rounded-md(6px) font-medium transition-colors disabled:cursor-not-allowed disabled:opacity-40`
  - size `sm`：`px-3(12px) py-1(4px) text-[12px]`（行内紧凑场景）
  - size `md`（**默认**）：`px-3.5(14px) py-1.5(6px) text-[12.5px]`（表单）
  - active：`text-primary-700`（随 `data-primary` 主题切换）
  - 非 active：`text-stone-500(#78716c) hover:text-stone-800`
- thumb 在 `z-0`、button 在 `z-10`——文字浮在白片之上

## 核心代码

```tsx
const [thumb, setThumb] = useState<{x:number;y:number;w:number;h:number}|null>(null);

useLayoutEffect(() => {
  const measure = () => {
    const list = listRef.current, el = btnRefs.current[value];
    if (!list || !el) return;
    const lr = list.getBoundingClientRect(), br = el.getBoundingClientRect();
    setThumb({ x: br.left - lr.left - 1, y: br.top - lr.top - 1, w: br.width, h: br.height });
  };
  measure();
  const ro = new ResizeObserver(measure);
  if (listRef.current) ro.observe(listRef.current);
  return () => ro.disconnect();
}, [value, options]);

<div ref={listRef} role="tablist"
  className="relative flex w-fit items-center gap-0.5 rounded-lg border border-stone-200 bg-stone-100/70 p-0.5">
  {thumb && (
    <span aria-hidden
      className="pointer-events-none absolute left-0 top-0 z-0 rounded-md bg-paper shadow-sm
                 transition-[transform,width,height] duration-300 ease-[cubic-bezier(.34,1.4,.5,1)]"
      style={{ transform: `translate(${thumb.x}px, ${thumb.y}px)`, width: thumb.w, height: thumb.h }} />
  )}
  {options.map(opt => (
    <button role="tab" aria-selected={opt.value === value} key={opt.value}
      className={cn('relative z-10 rounded-md font-medium transition-colors',
        size === 'sm' ? 'px-3 py-1 text-[12px]' : 'px-3.5 py-1.5 text-[12.5px]',
        opt.value === value ? 'text-primary-700' : 'text-stone-500 hover:text-stone-800')}>
      {opt.label}
    </button>
  ))}
</div>
```

## 适配指南

- 二选一 / 三四选一切换（视图模式、范围、tab-lite）一律用它，不用一排 radio
- thumb 定位**必须**靠实测——选项文字一中一英宽度不一时，等宽假设会错位
- 选中色用 themeable `primary-700`（跟站点主题），不写死蓝
- 切换内容若触发容器宽度变化，ResizeObserver 会自动重测，无需手动刷新

## 反模式

- ❌ 用纯 CSS `:checked ~ .thumb { left: 50% }` 等宽假设——选项文字不等宽会错位
- ❌ thumb 用线性 ease——失去 signature 的回弹手感（必须 `cubic-bezier(.34,1.4,.5,1)`）
- ❌ active 文字写死蓝 `text-blue-700`——破坏 themeable 主题切换
- ❌ thumb 圆角 = 容器圆角（都 `rounded-lg`）——thumb 应 `rounded-md` 略小一档，嵌在凹槽里
