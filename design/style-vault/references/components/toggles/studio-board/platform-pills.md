---
id: components/toggles/studio-board/platform-pills
type: component
name: 平台切换胶囊组
description: 四平台切换 pill——激活=该平台品牌色实底白字·未激活=淡墨填充中性字；logo 带品牌色、文字中性，克制不花
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm, confident]
  stack: [react-tailwind]
uses:
  - tokens/palettes/studio-board/warm-sand-ink
preview: /preview/components/toggles/studio-board/platform-pills
---

# 平台切换胶囊组

> 首页顶栏的四平台（Bilibili/抖音/小红书/YouTube）切换。**激活态才染该平台品牌色实底**，未激活是淡墨填充——一组里只有一个亮，其余安静。

## 视觉特征

- **胶囊**：`rounded-full · px-3.5 py-1.5 · text-xs · font-bold · inline-flex items-center gap-1.5`
- **激活态**：`background: <品牌色>` 实底 + `color:#fff`；logo 也转白。品牌色如 B 站粉蓝、YouTube 红、抖音黑、小红书红
- **未激活态**：`background: color-mix(in srgb, var(--sb-ink-soft) 9%, transparent)`（淡墨 9% 填充）+ `color: var(--sb-ink)`（暖墨字）；logo 保留各自品牌色
- **logo 带品牌色、文字中性**：未激活时靠小 logo 的品牌色点缀识别，文字始终暖墨——避免四个彩色文字一起「花」
- hover `opacity-90`，`transition-colors`
- 同款「激活=实底 / 未激活=淡填充」范式也用于右栏 tab 切换（激活 `bg-focus text-white`、未激活 `bg-surface/60`）

## 核心代码

```tsx
<button
  className="flex items-center gap-1.5 rounded-full px-3.5 py-1.5 text-xs font-bold transition-colors hover:opacity-90"
  style={ active
    ? { background: brandColor, color: '#fff' }
    : { background: 'color-mix(in srgb, var(--sb-ink-soft) 9%, transparent)', color: 'var(--sb-ink)' } }
>
  <PlatformLogo className="h-3.5 w-3.5" color={active ? '#fff' : brandColor} />
  {label}
</button>
```

## 适配指南

- 「激活染主色 / 未激活淡墨填充」是本套所有分段切换的统一范式——右栏 tab、平台切换都复用
- 品牌色只在激活态铺，未激活只留小 logo 的品牌色点——控制彩色面积
- 用淡墨**填充**而非纯描边药丸（描边药丸显「默认组件级」）

## 反模式

- 不要未激活也染品牌色（一组里只一个亮）
- 不要文字也上品牌色（四个彩字=花；文字中性、靠 logo 点色）
- 不要纯描边胶囊（要淡填充，更有完成度）
