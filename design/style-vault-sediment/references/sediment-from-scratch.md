# sediment-from-scratch · 从零创作

**适用触发**：用户只有想法（"想做一个冷感 SaaS 后台"、"做一套品牌站风格"），没有具体的项目路径 / URL / 截图。

**核心能力**：**对话式对齐**（3–5 问）→ moodboard → 代码草案 → 迭代到可沉淀。

---

## 档位门 · step 0（必做）

进入对齐前**先问档位**（见 [depth-tiers.md](depth-tiers.md)）。

```
本次沉淀想要多深？

  1) 精髓级（5–8 条 · 20–30 min）     ← 从零创作最常用
  2) 基础级（12–18 条 · 1–1.5 h）
  3) 全量级（30–50+ 条 · 3–4 h，**from-scratch 时不推荐**——从零同时造 30+ 条容易失去一致性，建议先做 Tier 1/2 后再升档补齐）

回 1 / 2 / 3（默认 1）。
```

from-scratch 档位的不同：

- **默认档位是 Tier 1**（不是 Tier 2）：从零创作的第一版通常只聚焦核心视觉语言，过度扩张反而让风格不稳
- **Tier 3 不推荐**：从零造 30+ 条条目难以保证内部一致性，建议先做 Tier 1 → 使用若干次回流验证 → 再升档

---

## 对齐阶段（最多 5 问，ideally 3 问）

**目标**：在 3–5 轮对话内收敛到足够产出沉淀计划。

### 问 1 · 气质方向

```
你想要的气质大概是哪个方向？
  A) 冷 / 严肃 / 工业感（像 Linear、Vercel）
  B) 暖 / 放松 / 人文（像 Notion、Stripe 近几代）
  C) 简约 / 中性（像 Apple、GitHub）
  D) 俏皮 / 彩色 / 有趣（像 Figma 早期、很多 D2C 品牌站）
  E) 编辑 / 内容型（像 Medium、Substack）

挑一个最接近的，或者自己描述。
```

### 问 2 · 参考对标

```
想像哪个现有产品的风格？
  - Linear / Vercel / Stripe / Notion / Figma / Apple / GitHub / Framer / Arc / Raycast / Superhuman / Height / ...
  - 或者提其它名字，或者就说"不像任何一个，我来描述"。

对标站不代表抄它——只是让我快速对齐气质。
```

### 问 3 · 技术栈

```
落地到哪套技术栈？
  1) react-tailwind        （React + Tailwind，裸）
  2) react-antd-tailwind   （React + antd + Tailwind，用 antd 组件）
  3) shadcn-radix          （React + shadcn/ui + Radix Primitives）
  4) html-tailwind         （纯 HTML + Tailwind，无 React）

默认 react-antd-tailwind（你当前项目的主栈）。
```

### 问 4 · 主色 + 字体偏好

```
有没有指定的主色？
  - hex 值（如 #5E6AD2）
  - 色相（冷蓝 / 暖橙 / 中性灰）
  - "你定"（AI 根据气质推荐）

字体？
  - 常见候选：Inter / Satoshi / Geist / IBM Plex Sans / Manrope / Playfair Display
  - "你定"也可以
```

### 问 5 · 产品类型

```
目标产品是哪一类？
  - productivity（效率工具 / 管理后台 / dashboard）
  - content（内容站 / blog / landing）
  - commerce（电商 / 购物）
  - social（社交 / 聊天）
  - tool（开发工具 / API 站）
  - brand（品牌站 / marketing）
  - lifestyle / entertainment / ...

决定 `products/<slug>` 和 `styles/<bucket>/<slug>` 的 category。
```

### 跳问规则

- 用户在问 1 就提了参考站（如"像 Linear 那样"）→ 跳过问 2
- 用户指定了产品定位（如"冷 SaaS 管理后台"）→ 跳过问 5
- 用户直接给 hex 主色 → 跳过问 4 的主色部分

**合并问题**：问 1 + 2 + 5 可以一次问："想要什么气质 + 对标谁 + 做什么产品？" 让用户一次回答。

**硬上限**：**最多 5 轮对话**。再问下去就陷入无限迭代——直接进 moodboard 让用户纠偏。

---

## Moodboard 输出

对齐后 AI **不直接产代码**，先给一个结构化的"风格草图"让用户确认。

### Moodboard 格式

```markdown
=== 风格草图 · 冷薄荷 SaaS 管理后台 ===

## 主色卡
- 主色：#10B981（薄荷绿）
- 辅色：#F0FDF4（极浅薄荷）/ #064E3B（深薄荷）
- 中性：slate 系（冷灰）
- 强调：#F59E0B（警告橙）

## 字体对
- 标题 + 正文：Inter（400 / 600）
- 等宽：IBM Plex Mono（400）

## 气质描述
低饱和薄荷绿 + 冷灰 slate 的组合。视觉冷静、专注、不打扰。
留白中等，卡片带细微边框（1px slate-200），hover 加薄影不加色。
按钮走 ghost / outline 风，主按钮实心但饱和度压低。

## 目标产品
管理后台 / analytics dashboard（category: productivity）

## 技术栈
react-antd-tailwind

## 预计沉淀条目
- tokens/palettes/cold-mint
- tokens/typography/cold-mint-inter-pair
- blocks/display/mint-stat-card
- blocks/display/mint-table
- styles/saas-tool/cold-mint-saas
- products/mint-analytics

---
下一步：确认推进 / 再调 / 放弃
```

### 让用户表态

每次给完 moodboard 都附 exit 提示：

```
下一步：
  A) 确认推进 → 进代码草案
  B) 再调 → 告诉我要改哪里（色 / 字体 / 气质 / 条目清单）
  C) 放弃 → 我们停止

请回 A / B / C，或直接说要改什么。
```

---

## 代码草案

用户说 A (确认推进) 后，AI 产出**完整的 frontmatter + 正文骨架**（同 [shared-workflow 步骤 3](shared-workflow.md#步骤-3--生成完整写入方案)）。

**重点**：代码草案是"按 moodboard 落地"，不是再问一次用户细节。该留白的留空（如 `## 反模式`），让用户在 shared-workflow 步骤 4 review 时补。

### 产物结构

按拓扑序：

1. `tokens/palettes/cold-mint` · 色板（完整 tailwind config 片段）
2. `tokens/typography/cold-mint-inter-pair` · 字体对
3. `blocks/display/mint-stat-card` · 数据卡片（完整 JSX）
4. `blocks/display/mint-table` · 表格（完整 JSX）
5. `styles/saas-tool/cold-mint-saas` · 风格聚合（正文描述视觉主张 + uses 引用 blocks）
6. `products/mint-analytics` · 产品定位

---

## 迭代 exit 机制

**每一轮**（对齐问 / moodboard / 代码草案）都在结尾给三选：

```
A) 确认推进 / B) 再调这里： / C) 放弃
```

**硬规则**：
- 总迭代轮次不超过 **6 轮**（问 + moodboard + 代码）
- 超过 6 轮没收敛 → AI 主动打断：

```
我们已经迭代 6 轮了。再改可能要先把要求写清楚再来。
建议：
  1) 把当前 moodboard + 你的最新要求写成一段文字，我用这段作为"最终口径"生成
  2) 暂停，等你想好再叫我
```

- 用户说 C → 立即停止，不写任何文件，不汇入主流程

---

## 汇入共享主流程

代码草案就绪 + 用户确认 "A 确认推进" 后，**汇入 [shared-workflow.md 步骤 2](shared-workflow.md#步骤-2--授权-auto-fill)**。

由于 from-scratch 没有外部素材，`source.md` 的内容改记录**对话摘录**：

```markdown
# 素材溯源 · <主题>

## 起点
from-scratch · 没有外部素材

## 对话摘录
<关键对话片段>
- 用户："想做一个冷薄荷 SaaS 管理后台的风格"
- AI 问：气质方向？ 用户：冷调、专注
- AI 问：对标？ 用户：像 Linear 那样但主色换成薄荷绿
- AI 问：技术栈？ 用户：react-antd-tailwind
- AI 出 moodboard → 用户："薄荷绿再压饱和一点，从 500 改到 400"
- 用户："代码草案 OK，推进"

## 最终 moodboard
<完整 moodboard 内容>
```

---

## 示范对话

假场景：用户说 `想做一个冷薄荷 SaaS 管理后台的风格`。

---

**AI**：

```
收到。对齐 3 问：

1) 气质方向 → 你说"冷"，确认是 A（冷/严肃/工业感）还是 B（简约/中性，冷但不工业）？
2) 对标哪个现有产品？Linear / Vercel / Height / 自己描述？
3) 技术栈：react-antd-tailwind（默认）可以吗？
```

---

**用户**：

```
B，像 Linear 但主色换成薄荷绿。栈可以。
```

---

**AI**：

```
对齐完成。主色候选：
  - Tailwind emerald-500 (#10B981) — 偏鲜亮
  - Tailwind emerald-400 (#34D399) — 偏清淡
  - 自定义 #6EE7B7 — 更淡一些

你想要哪个？还是"你定"？
```

---

**用户**：

```
emerald-400 偏淡那个。字体 Linear 同款。
```

---

**AI**（出 moodboard）：

```markdown
=== 风格草图 · 冷薄荷 SaaS ===

## 主色卡
- 主色：#34D399（薄荷绿，emerald-400）
- 辅色：#F0FDF4 / #065F46
- 中性：slate 系
- 强调：#F59E0B

## 字体对
- Inter（标题 + 正文）
- JetBrains Mono（Linear 同款等宽）

## 气质描述
冷调 slate + 清爽薄荷。Hero / CTA 用薄荷，数据区用 slate 背景。
卡片 1px 边框 + hover 薄影。按钮实心但压饱和（不用 500 档）。

## 预计沉淀
- tokens/palettes/cool-mint
- tokens/typography/linear-pair
- blocks/display/mint-stat-card
- blocks/display/mint-table
- styles/saas-tool/cool-mint-saas
- products/mint-analytics

下一步：A 确认推进 / B 再调 / C 放弃
```

---

**用户**：

```
A
```

---

**AI**：产出 6 条条目的完整 frontmatter + 正文骨架，然后 → **汇入 [shared-workflow 步骤 2](shared-workflow.md#步骤-2--授权-auto-fill)**。

---

**用户体验关键**：
- 对齐不超过 3 问（这个例子 3 问）
- moodboard 1 次出，用户 A 就推进
- 总迭代 2 轮（1 对齐 + 1 moodboard），远没到 6 轮上限

---

## 沉淀出错时 → 教训回写

用户看到最终产出后说"不是我想要的气质"、"跟我描述的差得远"、要求推翻重做 → 走 [shared-workflow.md 步骤 9 · 教训回写](shared-workflow.md#步骤-9--教训回写条件触发) + [lessons-loopback.md](lessons-loopback.md)。

**from-scratch 最常见的"模式错"类型**：
- 对齐问题不够聚焦（问了 5+ 个抽象问题但没要具体对标 / 具体关键词），导致抽象偏差累积
- moodboard 跳过，直接出代码条目——用户看到最终条目才发现方向不对
- 默认跑 Tier 2 而不是 Tier 1（从零创作容易内部失一致性）
- 把用户"想要 A 风格"的模糊表达当成"就是 xxx 品牌的样子"直接套用

一次小错（字体 / 主色 / 某条条目内容具体调整）→ 按对话继续调，**不触发**教训回写。
