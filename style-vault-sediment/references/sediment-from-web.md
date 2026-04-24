# sediment-from-web · 在线资源解析

**适用触发**：用户给 URL、截图路径、设计稿图片，希望把对应风格沉淀到 vault。

**核心能力**：视觉分析（读色 + 识字体 + 读气质）+ **重写代码**（源码不可得）+ 溯源落盘。

---

## 档位门 · step 0（必做）

进入 discovery 前**先问档位**（见 [depth-tiers.md](depth-tiers.md)）。

```
本次沉淀想要多深？

  1) 精髓级（5–8 条 · 20–30 min）
  2) 基础级（12–18 条 · 1–1.5 h）  ← 默认
  3) 全量级（30–50+ 条 · 3–4 h，**from-web 时慎选**——没源码无法做全路由枚举，实际能出的多半是 Tier 2 的量）

回 1 / 2 / 3（默认 2）。
```

from-web 相比 from-project 的特殊约束：

- **没源码 → 跨文件模式扫描失效**：只能靠肉眼看截图归纳；Tier 3 的"全局模式清单"改为"截图标注法"（见下）
- **没路由枚举**：只能以可见页面为限；Tier 3 建议要求用户再多提供 3-5 张不同路由的截图
- **动效不可见**：从 URL + 截图无法完整捕获；Tier 3 动效清单改为"站点可见的动效列表"（hero 动效 / 滚动效果 / hover 等），不完整不扣分

详细 Tier 3 调整见下面"Tier 3 for web"节。

---

## 输入形式 3 种

### 1. URL

用户触发语如 `沉淀 https://linear.app`、`参考这个网站 https://xxx`。

**获取方式**：

- 优先用 `WebFetch` 工具拉页面 HTML + 文本描述
- 把 URL 作为**访问依据**记录，但不假设能把源代码原样借过来
- **重要**：任何拉到的代码都**只能作视觉/结构的参考**，不直接抄——因为 (a) 版权 (b) 在线站点的代码混淆压缩后本来也读不出意图

若 `WebFetch` 直接返回了视觉关键信息（主色、字体、布局），跳到"视觉分析 checklist"。若只返回 HTML text content，还要让用户贴一张截图或再描述一下视觉，以弥补视觉维度。

### 2. 本地截图路径

用户触发语如 `沉淀 ~/Downloads/ref-screenshot.png`、`参考这张图 /tmp/dribbble.jpg`。

**获取方式**：

- Claude 多模态直接读图（Read 工具对 PNG / JPG 直接拿）
- 读完后 AI 描述视觉要点

### 3. 粘贴 HTML / base64 截图 / 多张图

用户可能直接在对话里粘 HTML 片段、base64 的截图、或一次给多张图。

- 粘贴 HTML → 当 URL 分支处理，但没有 URL 可溯源，只记"粘贴的 HTML 片段（N KB）"
- base64 截图 → 当截图处理，保存到临时文件再读
- 多张图混合 → 让用户指定"主样本"（下面"常见降级"有详细处理）

---

## 视觉分析 checklist

对拿到的素材（HTML 文本 / 截图）逐项分析：

### 主色

- **主 CTA 按钮色**：通常是整站主色
- **Hero 区背景色**：若大面积着色，是辅助主色
- **品牌 logo 色**：可能等于主色或是强调色
- **中性色系**：slate / gray / zinc / neutral 哪种色温

记录格式（精度到 hex）：

```
主色：#0EA5E9（冷蓝）
辅色：#F8FAFC（冷白）/ #64748B（冷灰）
强调：#F59E0B（橙，用于警告态）
```

### 字体

- **标题字体**：hero 大标题、h1-h3
- **正文字体**：段落、说明文字
- **等宽字体**：code / 数据区

常见字体识别线索（从 URL 分支 CSS link 或目测字形）：

| 字形特征 | 候选字体 |
|---|---|
| 开放几何无衬线 | Inter / Satoshi / Geist |
| 瘦高优雅 | Plus Jakarta Sans / Manrope |
| 高易读性正文 | Source Sans / Open Sans |
| 等宽干净 | JetBrains Mono / IBM Plex Mono / Geist Mono |
| 衬线优雅（编辑风） | Playfair Display / Fraunces |

**不确定就记为"待确认字体，目测像 Inter 家族"**，让用户在步骤 4 review 时确认。

### 布局密度

- 大留白、hero 占屏 50%+ → 疏朗、品牌型
- 紧凑栅格、上下 padding 小 → 数据密集型
- 左右对齐 aesthetic 的栅格数 → 12 列 / 10 列 / 自由

### 气质（aesthetic / mood）

参照 taxonomy.json 的 tag_groups 做映射：

| 视觉线索 | aesthetic | mood |
|---|---|---|
| 冷色 + 无衬线 + 大留白 | minimal | calm |
| 锐利几何 + 冷色 + 紧凑 | industrial | serious / cold |
| 暖色 + 圆角 + 手绘感 | organic | playful |
| 亮饱和 + 高对比 | brutalist | energetic |
| 衬线字体 + 大块文字 | editorial | thoughtful |

每一项**挑 1–2 个** tag，别堆一堆。步骤 4 用户可以增删。

---

## 实现代码生成（源码不可得必须重写）

### 重写原则

- **不 copy 原站代码**。哪怕 `WebFetch` 拉到了 JSX / HTML，也当作"视觉参考"看一眼就放下
- 代码基于 **style-vault 约定的 stack**（默认 react-tailwind，可用户指定 react-antd-tailwind / shadcn-radix / html-tailwind）
- 代码遵循 **style-vault 的 frontmatter + tokens 约定**（见 [shared-workflow.md 步骤 3](shared-workflow.md#步骤-3--生成完整写入方案)）

### 结构

每条条目按拓扑序产出（同 [shared-workflow 步骤 3](shared-workflow.md#步骤-3--生成完整写入方案)）：

- `tokens/palettes/<slug>` · 从视觉分析抽出来的色板
- `tokens/typography/<slug>` · 字体对
- `components/<bucket>/<slug>`（可选）· 识别到的交互元素
- `blocks/<bucket>/<slug>` · 主要的可复用区域（hero、feature-grid、table）
- `styles/<bucket>/<slug>` · 总体视觉聚合
- `products/<slug>` · 产品定位描述

### Token 层示例（重写的 tailwind config 片段）

frontmatter：

```yaml
id: tokens/palettes/linear-cold-slate
type: token
category: —          # tokens 不填 category
tags:
  aesthetic: [minimal, industrial]
  mood: [calm, serious]
  stack: [react-tailwind]
platforms: [web]
theme: [light, dark]
name: Linear 冷 Slate 调色板
description: 受 Linear 启发的冷蓝 + 冷灰色板（重写，不抄源码）
preview: frontend/src/preview/tokens/palettes/linear-cold-slate.tsx
```

正文：

```markdown
## 视觉特征
主色 #5E6AD2（冷蓝紫），中性 slate 系，整体冷调、低饱和。

## Tokens
```ts
// 可直接粘到 tailwind.config.ts 的 theme.extend.colors
export const palette = {
  brand: {
    50:  '#EEF0FF',
    500: '#5E6AD2',
    600: '#4B56B8',
    700: '#39419C',
  },
  slate: {
    50:  '#F8FAFC',
    200: '#E2E8F0',
    500: '#64748B',
    700: '#334155',
    900: '#0F172A',
  },
}
```

## 反模式
别把 brand.500 用作大面积背景——这个色设计为 accent。大面积背景用 slate.900 / slate.50。
```

### Block 层示例

frontmatter 的 refs 必须引下层 token：

```yaml
refs:
  tokens:
    palette: tokens/palettes/linear-cold-slate
    typography: tokens/typography/inter-mono-pair
```

正文的 `## 核心代码` 是 AI 根据视觉重写的 JSX，不是拷贝。

---

## 溯源落盘 source.md 模板

落盘路径（走 shared-workflow 步骤 8）：

```
~/.agents/skills/style-vault-sediment/assets/sediment-history/<author>/<date>-<topic>/source.md
```

模板：

```markdown
# 素材溯源 · <主题>

## URL
- 参考站点：https://linear.app（访问时间：2026-04-24 13:20）
- 辅助参考：https://dribbble.com/shots/xxx
- 若无 URL，留空或写"粘贴的 HTML 片段（N KB）"

## 截图
- 本地路径（临时）：/tmp/linear-hero.png
- 截图哈希（sha256）：ab12cd34...
- 关键截图要点：
  - 主视觉色 #5E6AD2（冷蓝紫）
  - Typography 用 Inter + Inter Mono
  - Hero 区大留白，字重偏轻
  - 布局密度：疏朗

## 视觉分析结论
- 主色：#5E6AD2 + slate 系
- 字体：Inter（标题/正文）+ Inter Mono（代码）
- aesthetic: [minimal, industrial]
- mood: [calm, serious]
- stack 建议：react-tailwind

## 对话摘录
<AI 精炼提取的和用户的关键对话片段，比如用户说"我觉得它的表格太紧凑了，我要松一点"的决策>

## 免责声明
本素材仅作视觉参考。所有 vault 条目中的代码为 AI 重写，未直接复制原站源码。
```

---

## 汇入共享主流程

视觉分析 + 沉淀计划就绪后，**汇入 [shared-workflow.md 步骤 2](shared-workflow.md#步骤-2--授权-auto-fill)**。

后续 8 步由 shared-workflow 统一处理。本分支的专属产物 `source.md` 在 [shared-workflow.md 步骤 8](shared-workflow.md#步骤-8--沉淀报告) 与 `report.md` 一起落盘 + 纳入 skill 仓 commit。

---

## 常见降级

### WebFetch 失败

**场景**：URL 登录墙、反爬虫、404、超时。

**降级**：

```
无法直接访问 <URL>（原因：<超时/403/...>）。
有两条路径：
  1) 贴一两张截图给我（拖图或给本地路径）
  2) 用文字描述主视觉（主色 / 字体 / 布局密度 / 气质）
挑一个推进。
```

### 截图模糊 / 分辨率太低

**场景**：读图后关键细节（按钮色、字体）看不清。

**降级**：

```
这张截图分辨率/清晰度不够，看不清 <具体项>。
需要：
  - 换一张高清版（推荐 2x 分辨率、不压缩）
  - 或者直接文字告诉我 <主色的 hex / 字体名>
```

**不要瞎猜**。视觉分析不确定就打断。

### 多页面混合（多个 shot / 多个 URL）

**场景**：用户一次给 3 个 Dribbble shot / 2 个网站 URL。

**降级**：

```
收到 3 张素材，它们风格：
  [1] <简述> （偏 minimal）
  [2] <简述> （偏 editorial）
  [3] <简述> （偏 industrial）

这三个气质有差异。建议你选一个作"主样本"走 from-web 沉淀主条目，
其它两张作为参考素材在 source.md 里记录但不作为视觉真相源。

主样本选哪个？
```

用户指定后，主样本走正常流程；其它素材的路径 / URL 作为辅助登记到 `source.md` 的 "辅助参考" 节。

### HTML 粘贴太长

**场景**：用户粘了 10k 行混淆 JSX。

**降级**：

```
粘贴的 HTML 太长，直接看源码推不出视觉。建议：
  - 描述视觉关键（主色 / 字体 / 要沉淀哪些区块）
  - 或给一张截图
```

### 视觉和用户主观描述冲突

**场景**：用户说"这个很活泼"但图上是冷工业风。

**降级**：把视觉分析结论 + 用户描述都贴出来让用户决策：

```
视觉分析：主色冷蓝、无衬线、紧凑 → 偏 industrial / serious
用户描述：活泼、friendly

两者有冲突。以哪个为准？
  A) 以视觉为准（走 industrial）
  B) 以你的描述为准（走 playful）
  C) 混合：主色保留冷调，但用圆角 + 手绘感补"活泼"
```

---

## 典型流程示例

假场景：用户说 `沉淀 https://linear.app`。

**1. WebFetch 拉页面**：拿到 hero 区文字 + 颜色 tokens + 字体 link
**2. 视觉分析**：主色 #5E6AD2，字体 Inter，aesthetic=minimal+industrial，mood=calm+serious
**3. 出沉淀计划**：

```
沉淀计划：
  目标：沉淀 Linear 的冷工业风
  起点：from-web (https://linear.app)
  新增条目（拓扑序）：
    1. tokens/palettes/linear-cold-slate      来源：视觉分析
    2. tokens/typography/linear-inter-pair    来源：视觉分析
    3. blocks/display/linear-issue-row        来源：issue 列表视觉
    4. blocks/nav/linear-sidebar              来源：左侧导航视觉
    5. styles/saas-tool/linear-cold-industrial 来源：整体视觉聚合
```

**4. 汇入 shared-workflow 步骤 2**
