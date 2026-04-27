---
id: components/overlays/style-vault/spring-toast
type: component
name: Spring Toast 操作反馈胶囊
description: 顶部居中胶囊式操作反馈，spring overshoot 入场（cubic-bezier(0.34, 1.56, 0.64, 1)），三态圆点 + 文本，2s 自动消失
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind, html-tailwind]
uses:
  - tokens/palettes/style-vault/slate-cyan-cool
  - tokens/typography/pairs/style-vault/inter-editorial-display
preview: /preview/components/overlays/style-vault/spring-toast
---

# Spring Toast

> 唯一允许 spring 回弹的元素 —— 顶部居中、白底带圆点、复制 / 保存 / 错误等操作的"轻量回执"

## 视觉特征

**形态**：`rounded-full border border-slate-200 bg-white px-4 py-2 text-[13px] font-medium`，顶部居中胶囊
- 白底 + 1px slate-200 描边 + `shadow-[0_12px_30px_-12px_rgba(15,23,42,0.18)]` 中距离投影 —— 区别于卡片浮起的三层投影
- 文字 13px medium slate-900 —— 比 caption 大一档，比 body 紧凑

**圆点三态**：1.5×1.5px，按 `kind` 切色：
- `success` → `bg-emerald-500` (#10b981)
- `error` → `bg-rose-500` (#f43f5e)
- `info` → `bg-slate-400` (#94a3b8)

文字色统一 slate-900——**只圆点变色**，不染整条胶囊（避免和品牌 cyan 抢戏，也不让"红 / 绿"成为语义噪音）。

**spring 入场动效**：
```css
@keyframes sv-toast-in {
  from { opacity: 0; transform: translateY(-8px); }
  to   { opacity: 1; transform: translateY(0); }
}
.sv-toast-anim {
  animation: sv-toast-in 320ms cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

cubic-bezier(0.34, 1.56, 0.64, 1) 是 **overshoot 1.56**——胶囊从上方 8px "钻"出来，越过最终位置 ~1.56× 再回弹。这是全站**唯一**允许回弹的动效（与 editorial-flow 系统其它 cubic-bezier(0.2, 0.7, 0.2, 1) signature 形成对比）。

**视口锚点**：`fixed inset-x-0 top-3 z-[10000] flex flex-col items-center gap-2`，pointer-events-none 父 + pointer-events-auto 子（不挡背后操作但可点击 toast 自身）。

**生命周期**：默认 2000ms 自动消失（`duration` 可覆盖）；多个并存时按时间顺序竖排，新的从上方冒出推下旧的。

## 与同 bucket 区分

- **vs antd `<message>`**：antd 默认带图标 + 圆形背景；本条只用圆点 + 纯文本，更"编辑式"
- **vs `<Alert>`**（block 级）：alert 是 inline 嵌入式状态条，常驻；toast 是顶部一过性回执，2s 后消失

## 核心代码

```tsx
'use client';
import { useEffect, useState } from 'react';

type ToastKind = 'success' | 'error' | 'info';
interface ToastItem { id: number; kind: ToastKind; content: string; }

let nextId = 0;
let items: ToastItem[] = [];
const listeners = new Set<() => void>();

function emit() { listeners.forEach((l) => l()); }

function push(kind: ToastKind, content: string, duration = 2000) {
  const id = ++nextId;
  items = [...items, { id, kind, content }];
  emit();
  if (duration > 0) {
    window.setTimeout(() => {
      items = items.filter((t) => t.id !== id);
      emit();
    }, duration);
  }
}

export const toast = {
  success: (c: string, d?: number) => push('success', c, d),
  error:   (c: string, d?: number) => push('error',   c, d),
  info:    (c: string, d?: number) => push('info',    c, d),
};

export function ToastViewport() {
  const [, force] = useState(0);
  useEffect(() => {
    const cb = () => force((n) => n + 1);
    listeners.add(cb);
    return () => { listeners.delete(cb); };
  }, []);
  return (
    <div className="pointer-events-none fixed inset-x-0 top-3 z-[10000] flex flex-col items-center gap-2">
      {items.map((t) => <ToastBubble key={t.id} item={t} />)}
    </div>
  );
}

function ToastBubble({ item }: { item: ToastItem }) {
  const dot = item.kind === 'success' ? 'bg-emerald-500'
            : item.kind === 'error'   ? 'bg-rose-500'
            :                           'bg-slate-400';
  return (
    <div className="sv-toast-anim pointer-events-auto flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-[13px] font-medium text-slate-900 shadow-[0_12px_30px_-12px_rgba(15,23,42,0.18)]">
      <span className={`h-1.5 w-1.5 rounded-full ${dot}`} />
      {item.content}
    </div>
  );
}
```

依赖全局 keyframe（来自项目 `index.css`）：

```css
@keyframes sv-toast-in {
  from { opacity: 0; transform: translateY(-8px); }
  to   { opacity: 1; transform: translateY(0); }
}
.sv-toast-anim { animation: sv-toast-in 320ms cubic-bezier(0.34, 1.56, 0.64, 1); }
```

## 适配指南

- **单例 store**：用 `let items[]` + `Set<listener>` —— 不要走 React Context（toast 是全局副作用，绕开 React 树更轻）
- **app 根挂一次** `<ToastViewport />` 即可，组件内 `import { toast } from '...'` 直接调
- 调用方式：`toast.success('Prompt 已复制')` / `toast.error('复制失败')`
- 默认 2000ms 适合短反馈；> 5s 的内容应该用 modal / banner 而非 toast
- `pointer-events-none` 父 + `pointer-events-auto` 子是**铁律**——不能让 toast 区域挡住下方操作

## 反模式

- 不要给 toast 加 close 按钮——它是一过性的，用户不应该跟它交互
- 不要把 kind=error 的胶囊染红底——颜色信息已在圆点
- 不要换 spring overshoot（1.56 是这个组件的身份）
- 不要把 toast 用作"分步引导提示"——那是 popover 的领地
- 不要批量 push（同时 3+ 条）——视觉拥挤；高频操作应该 debounce
- 不要把它放在 `top-0`（贴顶）/ `bottom-X`（底部）—— `top-3`（12px 留白）是这套 toast 的固定锚点
