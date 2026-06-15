---
id: tokens/typography/pairs/skillhub/inter-jetbrains-duo
type: token
name: Inter × JetBrains Mono 字体对
description: Inter + Space Grotesk 备选（正文）· JetBrains Mono（等宽）· 开启 Inter 现代字形特性
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses: []
preview: /preview/tokens/typography/pairs/skillhub/inter-jetbrains-duo
---

# Inter × JetBrains Duo

> 正文 Inter、代码 JetBrains Mono；开启 Inter 的 cv02 / cv03 / cv04 / cv11 字形特性，获得更现代的 a / i / l / 数字形态

## Tokens

### 字体栈

```css
--font-sans: 'Inter', 'Space Grotesk', system-ui, sans-serif;
--font-mono: 'JetBrains Mono', monospace;
```

Space Grotesk 只作为加载失败的审美近似备选，非主字体。

### OpenType features

```css
body {
  font-feature-settings: 'cv02', 'cv03', 'cv04', 'cv11';
  -webkit-font-smoothing: antialiased;
}
```

- `cv02`：更现代的小写 a（单层）
- `cv03`：小写 i 带 tittle 的标准形
- `cv04`：l 有上升辨识尾
- `cv11`：0 不带斜线（和非代码数字配合更干净）

### 字号 / 字重节奏

| 角色 | Tailwind | 像素 | 字重 | tracking |
|---|---|---|---|---|
| Hero H1 | `text-4xl md:text-5xl lg:text-6xl` | 36 / 48 / 60 | `font-extrabold` | `tracking-tight` / `leading-[1.15]` |
| Section H2 | `text-2xl` | 24 | `font-bold` | — |
| Block H3 | `text-lg` | 18 | `font-bold` | — |
| Card Title | `text-sm` | 14 | `font-bold` | — |
| Body | `text-sm` / `text-[13px]` | 14 / 13 | `font-medium` | `leading-relaxed` |
| Meta | `text-xs` / `text-[11px]` | 12 / 11 | `font-medium` or `font-semibold` | — |
| Table Head | `text-xs` | 12 | `font-bold` | `uppercase tracking-wider` |

### 重要模式

- **小号大写 + 宽字距**：表头 / 榜单列名 / ATOM 标签全部用 `text-xs font-bold uppercase tracking-wider text-gray-400`
- **粗中对比**：标题 `font-extrabold`，正文 `font-medium`——不用 regular（400）因会在 Inter 下显得稀）
- **行高对比**：标题 `leading-[1.15]` 紧凑、正文 `leading-relaxed` 疏朗 —— 层次靠行高拉开

## 使用示例

```tsx
<h1 className="text-5xl font-extrabold tracking-tight leading-[1.15] text-gray-900">
  让 AI 技能 <span>流动起来</span>
</h1>
<p className="text-lg text-gray-400">发现、安装、分享高质量的 AI Skill</p>

<code className="font-mono text-[11px]">{skill.slug}</code>
```

## 适配指南

- Tailwind `@theme` 块里把 `--font-sans` / `--font-mono` 设好，其它组件全部依靠 font-sans 默认继承
- 页面根节点加 `className="font-sans"` 作为冗余保险（对抗 antd 组件的默认 fallback）
- 代码/slug/时间戳等单独用 `font-mono` class 标出
- Inter 从 Google Fonts 导入时开齐 cv02/03/04/11，否则字形特性失效

## 反模式

- 不要混入第三种无衬线——Space Grotesk 只是 fallback，不作主字
- 不要把 JetBrains Mono 当标题字体——它只进 code / slug / 时间戳
- 不要用 `font-normal`（400 字重）做正文——Inter 在 UI 密度下会显得太细，统一上升到 500
