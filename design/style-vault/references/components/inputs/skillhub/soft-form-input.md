---
id: components/inputs/skillhub/soft-form-input
type: component
name: 柔边表单输入
description: 统一的表单级输入——slate-300 边 + rounded-xl + primary-500/20 focus ring
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/skillhub/skillhub-teal-mist
preview: /preview/components/inputs/skillhub/soft-form-input
---

# Soft Form Input

> 表单场景（登录 / 注册 / 编辑资料 / 发布）共用的输入基调——边框 slate-300 · 圆角 xl · focus 时 primary-500 + ring-2 ring-primary-500/20

## 视觉特征

- 底色：`bg-white`
- 边框：`border border-slate-300`（静态）→ `focus:border-primary-500`（focused）
- 焦点环：`focus:ring-2 focus:ring-primary-500/20`
- 圆角：`rounded-xl`（12px，偏软 modernist）
- 内距：`px-4 py-3`（高 input，登录 / 编辑表单专用）
- 字：`text-sm text-gray-900 placeholder:text-gray-400`
- 过渡：`transition-all outline-none`

## 核心代码

```tsx
interface SoftFormInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  hint?: string;
}

export const SoftFormInput = ({ label, error, hint, id, ...rest }: SoftFormInputProps) => {
  const inputId = id || React.useId();
  return (
    <div>
      {label && (
        <label htmlFor={inputId} className="block text-sm font-bold text-slate-900 mb-1.5">
          {label}
        </label>
      )}
      <input
        id={inputId}
        {...rest}
        className={`w-full bg-white border rounded-xl px-4 py-3 text-sm
                    focus:ring-2 transition-all outline-none
                    ${error
                      ? 'border-rose-300 focus:border-rose-500 focus:ring-rose-500/20'
                      : 'border-slate-300 focus:border-primary-500 focus:ring-primary-500/20'}
                    ${rest.className || ''}`}
      />
      {hint && !error && <p className="mt-1 text-xs text-slate-400">{hint}</p>}
      {error && <p className="mt-1 text-xs text-rose-600">{error}</p>}
    </div>
  );
};
```

## 变体

### Textarea（多行）

```tsx
<textarea
  rows={4}
  className="w-full bg-white border border-slate-300 rounded-xl px-4 py-3 text-sm
             focus:ring-2 focus:border-primary-500 focus:ring-primary-500/20
             transition-all outline-none resize-none"
/>
```

### 低 input（搜索 / 筛选，非表单域）

```tsx
<input
  className="w-full bg-white border border-slate-200 rounded-lg px-3 py-1.5 text-sm
             focus:border-slate-400 focus:ring-1 focus:ring-slate-200
             transition-all outline-none"
/>
```

**低 input 和高 input 的区分**：
- 高（本组件）：表单域 · px-4 py-3 · rounded-xl · primary-500 focus
- 低：搜索 / 筛选 · px-3 py-1.5 · rounded-lg · slate focus

## 适配指南

- `primary-500` 对应 `tokens/palettes/skillhub/skillhub-teal-mist` 的 teal-500（`#14b8a6`）——换色系时批量换 primary
- 高 input 用 `py-3` 是有意为之，比 Antd 默认的 `py-2` 多 4px 呼吸
- 错误态 border 用 rose 不用 red——与状态色系对齐
- label 固定 `font-bold text-slate-900`——不要弱化成 gray-500，表单域的 label 是导航
- 错误提示 `text-xs text-rose-600`，hint `text-xs text-slate-400`——用颜色对比区分

## 反模式

- 不要给表单域用低 input（rounded-lg + py-1.5）——太瘦，输入体验差
- 不要用 `focus:ring-4`——会把环做得太胖像 bootstrap
- 不要去掉 `transition-all`——focus 跳变很突兀
- 不要混 border-gray-200（偏轻）和 border-slate-300（偏重）——一套表单只用一种
