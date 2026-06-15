---
id: components/buttons/skillhub/dark-primary-cta
type: component
name: 黑底主 CTA
description: 全站统一的黑底 CTA（#1a1a1a / slate-900）+ active:scale-95 + hover:bg-[#333] 的黑白按钮骨架
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/skillhub/skillhub-teal-mist
preview: /preview/components/buttons/skillhub/dark-primary-cta
---

# Dark Primary CTA

> SkillHub 的"负空间一致性"骨架——全站除了追光 CTA 外，所有主动作按钮都是这一个形态：纯黑底 `#1a1a1a` / slate-900 + 白字 + `rounded-xl` + `active:scale-95`。跨 9 个文件 19 处使用。

## 视觉特征

- 底色三档：
  - **首选** `bg-[#1a1a1a]` / `hover:bg-[#333]`（登录、发布实践、关注等品牌级操作）
  - **副选** `bg-slate-900` / `hover:bg-slate-800`（Antd primary 配合场景 + 管理后台）
  - **第三态** `bg-[#2b2b2b]`（导航激活胶囊、专属追光按钮底）
- 字：`text-white text-sm font-medium` 或 `font-bold`（品牌级）
- 圆角：`rounded-xl` (12px) 或 `rounded-lg` (8px) 小号
- 间距：`px-4 py-1.5`（紧凑）/ `px-5 py-2.5`（中）/ `px-8 py-3`（大）
- Tap：`active:scale-95` 统一回弹
- 动效：`transition-all duration-200`

## 核心代码

```tsx
type DarkCtaSize = 'sm' | 'md' | 'lg';
type DarkCtaVariant = 'pure' | 'slate';  // pure = #1a1a1a, slate = slate-900

interface DarkPrimaryCtaProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  size?: DarkCtaSize;
  variant?: DarkCtaVariant;
  icon?: React.ReactNode;
  children: React.ReactNode;
}

const sizeCls = {
  sm: 'px-4 py-1.5 text-sm',
  md: 'px-5 py-2.5 text-sm',
  lg: 'px-8 py-3 text-sm font-bold',
};
const variantCls = {
  pure: 'bg-[#1a1a1a] hover:bg-[#333]',
  slate: 'bg-slate-900 hover:bg-slate-800',
};

export const DarkPrimaryCta = ({
  size = 'md',
  variant = 'pure',
  icon,
  children,
  className = '',
  ...rest
}: DarkPrimaryCtaProps) => (
  <button
    {...rest}
    className={`inline-flex items-center gap-2 rounded-xl text-white font-medium
                transition-all duration-200 active:scale-95
                ${sizeCls[size]} ${variantCls[variant]} ${className}`}
  >
    {icon}
    {children}
  </button>
);
```

## 变体

### 带扫光 overlay（发布实践按钮）

```tsx
<button className="group relative px-5 py-2.5 rounded-xl text-sm font-bold
                   bg-[#1a1a1a] text-white overflow-hidden active:scale-[0.97]">
  <span className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent
                   translate-x-[-200%] group-hover:translate-x-[200%]
                   transition-transform duration-700 ease-in-out" />
  <span className="relative z-10 inline-flex items-center gap-1.5">
    <Sparkles size={13} /> 发布实践
  </span>
</button>
```

### Antd 覆盖版（管理后台用）

```css
/* index.less */
.ant-btn-primary {
  @apply !bg-slate-900 !text-white !shadow-sm transition-all
         hover:!bg-slate-800 hover:!text-white active:!scale-95;
}
```

## 适配指南

- **与追光 CTA 互斥**：全站同时最多 1 个追光按钮；普通主动作一律用这个黑底
- **与 teal 搜索按钮分工**：黑底 = 动作（发布 / 登录 / 关注），teal-500 = 检索 / 确认筛选
- **与 ghost 次按钮搭配**：主 action 用 dark-primary-cta，次 action 用 `border border-gray-300 text-gray-700 rounded-xl` ghost
- Antd 覆盖建议用 `bg-slate-900` 而非 `bg-[#1a1a1a]`——和 `colorPrimary: '#0f172a'` token 对齐
- 自己写 tailwind className 时用 `bg-[#1a1a1a]`——与 navbar 激活 `#2b2b2b` 保持近色系

## 反模式

- 不要混用 `bg-black`（#000）——过深，和 `#1a1a1a` 有可感差异
- 不要给 Dark CTA 加 shadow——它靠对比度站住，阴影会弱化
- 不要让它 `rounded-full`——rounded-xl 是这套视觉的节奏基调
- 不要在同行并列 2 个 Dark CTA——主 + ghost 对照才对
