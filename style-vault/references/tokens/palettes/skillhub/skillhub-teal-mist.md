---
id: tokens/palettes/skillhub/skillhub-teal-mist
type: token
name: SkillHub 柔雾 Teal 调色板
description: Teal 主色 50-900 + Slate 中性 + 12 色柔和头像板 + Top3 红黄蓝 + 四色流动渐变
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses: []
preview: /preview/tokens/palettes/skillhub/skillhub-teal-mist
---

# SkillHub Teal Mist

> 浅色调色板——teal 贯穿所有交互强调，slate 承载内容层级，底色是接近白的 `#f5f7fa`

## Tokens

### Primary · Teal（交互强调，主搜索/分页/标签）

```css
--color-primary-50:  #f0fdfa;
--color-primary-100: #ccfbf1;
--color-primary-200: #99f6e4;
--color-primary-300: #5eead4;
--color-primary-400: #2dd4bf;
--color-primary-500: #14b8a6;   /* brand accent · 主搜索按钮底色 */
--color-primary-600: #0d9488;   /* hover / 分页 active */
--color-primary-700: #0f766e;   /* text active */
--color-primary-800: #115e59;
--color-primary-900: #134e4a;
```

### Neutral · Slate / Gray（内容层级）

```css
--color-bg-base:     #ffffff;   /* 卡片底、navbar 内 pill */
--color-bg-page:     #f5f7fa;   /* body 底（淡 slate 洗） */
--color-bg-subtle:   slate-50;  /* zebra 背景、tag 底 */

--color-fg-strong:   #1a1a1a;   /* 品牌字、CTA 底色 */
--color-fg-base:     gray-900;  /* 标题 */
--color-fg-body:     gray-700;  /* 正文 */
--color-fg-muted:    gray-500;  /* 描述 */
--color-fg-subtle:   gray-400;  /* 元信息、图标 */
--color-fg-ghost:    gray-300;  /* disabled、空榜位 */

--color-border-base:   gray-200;
--color-border-soft:   gray-100;
--color-border-strong: gray-300;
```

### Dark CTA（纯黑系,次选 slate-900）

```css
--color-cta-bg:      #1a1a1a;   /* 登录 / 发布实践按钮 */
--color-cta-bg-hover:#333;
--color-cta-active:  #2b2b2b;   /* nav 激活态 */
```

### Avatar Palette（12 色柔和——字母头像轮转）

```ts
export const AVATAR_COLORS = [
  '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
  '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9',
  '#F8C471', '#82E0AA',
];
```

用法：`AVATAR_COLORS[index % 12]` 作为圆形头像底色，白字加粗首字母。

### Rank Colors · Top3（榜单 Top3 专用）

```ts
export const RANK_COLORS = ['#FF6B6B', '#F7DC6F', '#45B7D1'];
// 第 4 名及之后：slate-300 (#cbd5e1)
```

### Gradient · Flow（Hero 强调词 / 装饰流光）

```css
background-image: linear-gradient(
  90deg,
  #14b8a6, #06b6d4, #0ea5e9, #f472b6,
  #14b8a6, #06b6d4, #0ea5e9, #f472b6, #14b8a6
);
background-size: 300% 100%;
animation: flow-right 14s linear infinite;
```

四色循环：teal → cyan → sky → rose → teal，首尾同色实现无缝。

### Status Colors

```css
--color-success: emerald-500;   /* #10b981 · "systems operational" 脉冲点 */
--color-warning: orange-500;    /* 未读消息红点 */
--color-danger:  rose-500;      /* 错误条带底色 rose-50 / 文字 rose-700 */
--color-focus:   teal-300;      /* 输入 focus:border */
--color-focus-ring: teal-100;   /* 输入 focus:ring */
```

## 使用示例

```tsx
// 搜索按钮
<button className="bg-teal-500 hover:bg-teal-600 text-white">搜索</button>

// 分类 pill（见 components/tags-badges/skillhub/teal-pill）
<span className="bg-teal-50 text-teal-600 border-teal-100 rounded-full">标签</span>

// 字母头像
<div style={{ backgroundColor: AVATAR_COLORS[idx % 12] }}
     className="w-10 h-10 rounded-full text-white font-bold">A</div>
```

## 适配指南

- Antd `ConfigProvider` 里把 `colorPrimary` 设 `#0f172a`（slate-900，用于默认按钮/链接），teal 由 Tailwind utility 单独接管交互点。两色并存，不冲突
- Tailwind config 在 `@theme` 块里注入 primary-50 ~ 900 为 teal 十阶（见 index.less）
- 页面纯白 CTA 用 `#1a1a1a`，非纯黑系 slate-900（`#0f172a`）——两者差异细微但与 slate-cyan-ice 不是同一套
- 头像色 12 色是"柔和但可辨"级别，不要替换成饱和度更高的色——会和 teal 主色互相压制

## 反模式

- 不要让 teal-500 出现在正文字体色里——它只进按钮、链接、标签 3 个入口
- 不要把头像 12 色用在非头像场景（tag/chart 等）——辨识度会稀释
- 流动渐变不要在普通标题里滥用，只给 Hero 的 1 个强调词
