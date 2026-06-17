---
name: html-diagram
description: Render diagrams (system architecture, link/topology maps, narrative architecture decks, sequence flows, timelines, etc.) as self-contained single-file HTML by picking a style from the style library and adapting one of its samples. Triggers include `/html-diagram`, "画一张 HTML 图", "用 HTML 画 X", "html 架构图 / 链路图 / 流程图", "html 可视化", "single-file html diagram", "interactive html diagram", "deck-style html"。Output is one HTML file with inlined CSS/SVG/JS, no build step. PURE RENDERING LAYER — does NOT brainstorm content, only formalizes content already in context (chat history, design docs, markdown notes). DO NOT trigger for: mermaid charts (use mermaid-visualizer), Excalidraw boards (use excalidraw-diagram), PNG/PDF posters (use canvas-design), generic frontend pages (use frontend-design / website-creator).
metadata:
  version: 1.1.0
  changelog:
    - "1.1.0: Sediment 10 advanced patterns into dark-techy.md (multi-tier panel, platform-with-modules, type-differentiated visuals, region grouping, multi-row proxy, collapsible legend, elastic entrance, layout centering, naming consistency, ID stability)"
    - "1.0: Initial style library (dark-techy / slate-mono-grid)"
---

# HTML Diagram

把上下文中已有的结构化或半结构化内容（架构、链路、关系、流程等）渲染成单文件 HTML 图。

**核心维度只有一个：风格 (style)。** 每个风格 = 一整套视觉语言（色板、节点形状、装饰、动效、图例）。每个风格下有 1+ 个 **sample**（不同应用形态的成品），AI 选最贴近上下文内容形态的 sample 作脚手架，改填后落盘。

> sample 不是 category — 它们是该风格的不同应用实例。AI 看内容选 sample，不需要让用户先选"类别"。

---

## ⚠️ 重要边界：本 skill 不参与内容思路

这是**纯视觉化层**：

| 做 | 不做 |
|---|---|
| 把上下文已有内容渲染成 HTML | 头脑风暴"画什么、有哪些节点、关系怎么连" |
| 按指定风格套版式改填 | 补充用户没给的业务/架构内容 |
| 复用 sample 作为脚手架 | 决定"这张图的信息架构应该怎么组织" |

**如果上下文不足以画图（用户只说"画一张架构图"但没给任何节点/关系信息），直接告诉用户缺什么、停下，不要凭空发明内容。**

需要先做"画什么"的，引导用户用 `brainstorming`；零散需求 → `req-to-ai-spec`；写设计文档 → `doc-coauthoring`。本 skill 永远是"内容已就位"之后的最后一公里。

---

## 触发与决策

`/html-diagram` 三种调用形态：

| 调用 | 行为 |
|---|---|
| `/html-diagram`（裸） | 列出全部风格 + 每个风格下所有 sample 的 `file://` 绝对路径。用户复制到浏览器选风格、回填风格名继续。 |
| `/html-diagram <style>` 或 `/html-diagram <style> <描述>` | 用指定风格出图。AI 看上下文 + 描述自行选最贴近的 sample 作脚手架；模棱两可时反问。 |
| `/html-diagram <描述>`（无风格） | 看上下文 + 描述推荐 1–2 个风格 + 对应 sample 路径，等用户确认风格后出图。**不要在用户没确认前就生成。** |

---

## 路径自发现协议

SKILL.md 加载时 runtime 注入：

```
Base directory for this skill: /absolute/path/to/html-diagram
```

把它作为 `${SKILL_DIR}`。**所有给用户的 sample 路径必须是完整的 `file://${SKILL_DIR}/...` URL**（用户要直接复制到浏览器）。

---

## 工作流（一段式）

```
[1] 决定 style（按上面的决策表）
       │
       ▼
[2] Read references/styles/<style>.md     ← 风格规范（token / 节点 / 装饰 / 图例 / 动效 / sample 选用指引）
       │
       ▼
[3] 看上下文 + 描述选 sample，Read assets/styles/<style>/samples/<sample>.html
    （整文件 read 到内存作脚手架）
       │
       ▼
[4] 改填：把上下文里的内容替换 sample 里的演示内容
       - 保留：token / 装饰 / 动效 / 图例 / 降级 fallback / @media 响应式
       - 替换：文字、节点列表、连线列表、section 内容
       - 不要改：CSS 变量值、easing、动画时长（除非用户明确要求）
       │
       ▼
[5] Write 到当前工作目录，文件名 = 用户指定 或 <topic>.html
       │
       ▼
[6] 一句话回执：写到了哪个绝对路径、用了什么 style + 哪个 sample 作脚手架
```

### sample 选不到怎么办

如果上下文内容形态在该风格的现有 sample 里找不到匹配：

1. 取该风格**最接近的 sample** 作 token / 装饰 / 图例 base
2. 按上下文实际形态调整结构（增删 section / 重排 panel / 等）
3. 在文件 head 注释标注"based on <sample>, structurally adapted on YYYY-MM-DD"
4. 如果这个新形态值得沉淀，参照 `references/extending.md` 加为该风格的新 sample

---

## 风格清单 / sample 清单（懒加载）

不要在 SKILL.md 里展开。需要时 read：

- `references/styles.md` —— 全部风格速览 + 每风格的 sample 列表（裸 `/html-diagram` 触发时读）
- `references/styles/<style>.md` —— 风格详细规范（含 sample 选用指引）

---

## 输出格式

裸 `/html-diagram` 输出格式见 `references/styles.md` 末尾。

出图后回执遵循：

```
✅ 已生成：<工作目录>/<filename>.html
   风格：<style-name>
   脚手架：<sample-name>
   <一句话补充：节点 X 个、链路 Y 条、含 hover 联动 / 等>
```

---

## 维护与扩展

加新风格、加新 sample —— 见 `references/extending.md`。
