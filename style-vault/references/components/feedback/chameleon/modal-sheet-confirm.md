---
id: components/feedback/chameleon/modal-sheet-confirm
type: component
name: 分档 Modal + 滑入 Sheet + 命令式 confirm
description: 4 档宽 rounded-2xl 三段式 Modal（Header/滚动 Body/暖底 Footer）+ 右/左滑入 Sheet 抽屉 + 命令式 confirm() Promise
platforms:
- web
theme: light
tags:
  aesthetic:
  - minimal
  mood:
  - calm
  - serious
  stack:
  - shadcn-radix
uses:
- tokens/shadow/waveflow/soft-card-pop-trio
preview: /preview/components/feedback/chameleon/modal-sheet-confirm
---

# Chameleon 分档 Modal + 滑入 Sheet + 命令式 confirm

> 三个互补的覆盖层原语，都基于 `@radix-ui/react-dialog`。`Modal` 比裸 Dialog 更完整——4 档固定宽（400/520/720/960px）+ `rounded-2xl` + Header/滚动 Body/暖底 Footer 三段式 + `preventClose`/`closeOnBackdrop` 控制。`Sheet` 是从右/左滑入的全高抽屉（默认 480px）。`confirm()` 是命令式 helper：动态挂 React root 渲染 ConfirmDialog，确认/取消后延时 200ms 卸载（等 Radix close 动画跑完防 flash），替换原生 `window.confirm`。

## 视觉特征

### Modal（4 档分档模态壳）

- **Overlay**：`modal-overlay fixed inset-0 z-50 bg-stone-950/20`
- **Content**：`modal-content fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-50 flex max-h-[90vh] flex-col overflow-hidden rounded-2xl(16px) border border-stone-200 bg-paper(#fffefb) shadow-pop` + SIZE_CLASS
- **4 档宽**：`sm:w-[400px] / md:w-[520px] / lg:w-[720px] / xl:w-[960px]`（默认 md）
- **Close**：`absolute right-3.5(14px) top-3.5 rounded-md p-1 text-stone-400 opacity-80 hover:bg-stone-100 hover:text-stone-700 hover:opacity-100 focus:ring-1 focus:ring-blue-200` 内 `<X className="h-4 w-4" strokeWidth={1.75}/>`
- **Header**：`flex flex-col gap-1(4px) border-b border-stone-200/70 px-5(20px) pb-3.5(14px) pt-4(16px)`
- **Body**：`flex-1 overflow-y-auto px-5 py-4(16px)`（独立滚动区）
- **Footer**：`flex items-center justify-end gap-2(8px) border-t border-stone-200/70 bg-warm-2/30 px-5 py-3(12px)`（暖底 warm-2 30% 透明）
- **Title** `text-[14px] font-semibold tracking-tight text-stone-900`；**Description** `text-[12px] leading-relaxed text-stone-500`

### Sheet（右/左滑入抽屉）

- **Overlay**：`fixed inset-0 z-50 bg-stone-950/20`
- **Content**：`fixed inset-y-0 z-50 flex h-full flex-col bg-[var(--color-paper)] shadow-pop border-stone-200` + side right `right-0 w-[480px] border-l` / left `left-0 w-[480px] border-r`（width prop 可覆写）
- **Close**：`absolute right-4(16px) top-4 rounded-sm opacity-70 hover:opacity-100` 内 `<X className="h-4 w-4"/>`
- **Header**：`flex flex-col space-y-2(8px) border-b border-stone-200 p-6(24px)`；**Body**：`flex-1 overflow-auto p-6`；**Footer**：`flex justify-end gap-2(8px) border-t border-stone-200 px-6 py-4(16px)`
- **Title** `text-lg(18px) font-semibold`；**Description** `text-xs(12px) text-stone-500`

### confirm（命令式 helper，无自身 JSX）

- `confirm({ title, description?, confirmText='确认', cancelText='取消', danger? }) → Promise<boolean>`
- `document.body` 挂 host div + `createRoot` + `render(<ConfirmDialog open variant={danger?'danger':'default'} .../>)`
- close 时先 `setTimeout(200ms)` 再 `root.unmount()`（等 Radix close 动画跑完防 flash），同步 `resolve(result)`

## 核心代码

```tsx
const SIZE_CLASS = { sm:'w-[400px]', md:'w-[520px]', lg:'w-[720px]', xl:'w-[960px]' };

// Footer 暖底是 Modal 与裸 Dialog 的关键区分
<ModalFooter className="flex items-center justify-end gap-2 border-t border-stone-200/70 bg-warm-2/30 px-5 py-3" />

// 命令式 confirm
export function confirm(opts): Promise<boolean> {
  return new Promise(resolve => {
    const host = document.createElement('div');
    document.body.appendChild(host);
    const root = createRoot(host);
    const close = (result: boolean) => {
      setTimeout(() => { root.unmount(); host.parentNode?.removeChild(host); }, 200);
      resolve(result);
    };
    root.render(<ConfirmDialog open variant={opts.danger ? 'danger' : 'default'}
      onConfirm={() => close(true)} onCancel={() => close(false)} {...opts} />);
  });
}
// 用法：if (await confirm({ title:'删除文档?', danger:true })) deleteMut.mutate(id)
```

## 适配指南

- 模态用 `Modal`（分档 + 三段式 + 暖底 footer），不要用裸 Dialog——表单场景需要 Body 独立滚动 + Footer 钉底
- 表单宽度按内容选档：单列表单 sm/md，双列或带预览 lg，全屏编辑 xl
- 详情 / 设置抽屉用 `Sheet`（默认右侧 480px），不抢主区焦点
- 删除二次确认用 `await confirm({ danger:true })`，逻辑里直接 `if` 拿布尔——比声明式管 open 状态干净

## 反模式

- ❌ 用裸 Dialog 做长表单——它无独立滚动 Body，内容超高顶到 viewport
- ❌ Footer 不用 `bg-warm-2/30` 暖底——三段式分层会糊在一起，按钮区不突出
- ❌ confirm 卸载不延时 200ms——Radix close 动画没跑完就卸载，弹窗 flash 一下消失
- ❌ Modal 圆角用 `rounded-lg(8px)`——这里刻意 `rounded-2xl(16px)`，比裸 Dialog 更柔
