---
name: docsify-station-creator
description: Generate a fully-featured Docsify documentation site from an existing docs/ folder. Use when the user asks to create a documentation site, generate a Docsify site, or turn markdown files into a browsable doc portal. Features include dark/light theme toggle, right-side TOC with scroll highlight, full-text search, Mermaid diagram rendering, code highlighting with copy button, and responsive layout. Supports an optional Animation Mode that embeds a GSAP/D3 animation engine and authors interactive per-concept animations (动画驱动, 图 >> 文字) for a richer, animation-driven site.
---

# Docsify Station Creator

From an existing `docs/` folder with markdown files, generate a complete Docsify documentation site.

## Pre-requisites

Identify project info (ask user if not available from code/context):

1. `{{PROJECT_NAME}}` — project name (cover title, sidebar title, page `<title>`)
2. `{{PROJECT_DESCRIPTION}}` — one-line description (cover subtitle, page `<title>`)

The favicon is a built-in gradient mark — **no emoji/icon input needed** (`{{PROJECT_ICON}}` is gone).

### Authoring the docs first (optional)

This skill turns an **existing** `docs/` of markdown into a site. If the project has no docs yet (or they're thin), generate them first with the sibling skill **`wiki-creator`** (deep-scans the codebase → structured `docs/` with Mermaid), then run this skill on the result. If `wiki-creator` isn't installed, skip it and just use whatever `docs/` exists — don't hard-depend on it.

## 设计原则：克制 emoji（重要）

This skill produces a deliberately refined, "high-end" site. **Avoid emoji wherever you can** — none in the sidebar tree, group headers, page/section titles, the cover, mermaid node labels, or callout markers. Emoji read as cheap / AI-generated. Lean on the built-in gradient accents, SVG icons, and typography for hierarchy. Only keep incidental emoji already present in the source prose if the user explicitly wants them.

## Mode selection (ask first)

Before generating, **ask the user which mode** (use AskUserQuestion). Default to **Standard** if they don't care.

- **Standard** (default) — clean docs site, no animations. Just the Workflow below.
- **Animated** — everything in Standard, **plus** embed an animation engine and author interactive GSAP/D3 animations for the project's core concepts (动画驱动, 图 >> 文字). After the Workflow, also do [Animation Mode](#animation-mode-optional).

## Workflow

### Step 1: Create directory structure

The **entire docsify site is self-contained in `docs/docsify/`** — so it never mixes with whatever content directories an AI may create under `docs/`:

```
docs/                          # 文档内容（各业务/章节目录，可由 AI 自由创建）住这里
├── docsify/                   # ← docsify 站点的全部文件都在这一个目录
│   ├── index.html             #   入口（已设 basePath:"/" 以加载 docs/* 的内容）
│   ├── _sidebar.md
│   ├── _coverpage.md
│   ├── README.md              #   首页 landing（route #/docsify/README）
│   ├── scripts/
│   │   ├── start-docs.sh
│   │   ├── start-docs.bat
│   │   └── build-offline.py   #   可选：编译成单文件离线版 offline.html
│   └── assets/                #   仅 Animated 模式：anim-kit + 各动画模块
├── guide/  business/  ...     # 内容 markdown（兄弟目录，保持原样）
└── ...
```

The HTTP server runs from **`docs/` root** (content is in `docs/*`); the site opens at **`/docsify/`**. `index.html` sets `basePath: "/"`, so a route like `#/business/x` loads `docs/business/x.md` while the station's own files resolve under `docsify/`.

### Step 2: Scan existing markdown files

Scan `docs/` and subdirectories for all `.md` files. **Exclude**:
- `docs/docsify/` (the whole station: index.html, config, scripts, assets), `node_modules/`, `.git/`
- `_sidebar.md`, `_navbar.md`, `_coverpage.md`
- `docs/docsify/README.md`

Record the file list for sidebar generation.

### Step 3: Generate sidebar navigation

From the scanned file list:

1. Sort by filename (numeric prefix first if present)
2. Extract title: read first `# heading` from each file; fallback to filename without `.md`
3. Group files (precedence — apply the first that matches):
   - **Subdirectories exist → group by subdirectory, always, regardless of file count.** The dir structure carries meaning; never flatten it into a single list.
   - **Single flat folder → group by numeric-prefix pattern** (`01-`, `02-`) into common groups (入门指南, 核心概念, 使用指南, 开发文档, 其他). Exception: if that flat folder has **fewer than 5 files**, use a flat list with no group headers.

**Path format**: relative to `docs/` root (the server root, i.e. `basePath: "/"`), e.g. `business/start.md` → route `#/business/start`. No `../` prefix. The landing item links to `docsify/README.md`.

Example `_sidebar.md`:

```markdown
- 开始
  - [文档首页](docsify/README.md)
- 入门指南
  - [快速开始](01-quick-start.md)
  - [项目简介](02-introduction.md)
- 核心概念
  - [架构设计](03-architecture.md)
```

For files in subdirectories (e.g., `docs/guide/start.md`): link is `guide/start.md`.

Strip numeric prefixes from display names (e.g., `01-quick-start.md` → "快速开始").

**No emoji** in group headers or item titles — strip any leading emoji from extracted titles.

**Landing link (cover ↔ home routing)**: the first item must link to the landing doc as a real route — `[文档首页](docsify/README.md)` → `#/docsify/README`. Do **NOT** link it to `/`; `/` is reserved for the cover page. Because docsify aliases links to its `homepage` file back to `/`, this skill sets **no `homepage`** option, so `docsify/README.md` resolves to its own route `#/docsify/README` (clicking the sidebar **title/app-name** goes to the cover at `#/`; clicking **文档首页** goes to the home page — two independent routes).

### Step 4: Generate files

Generate the files below from the templates — 4.1–4.6 required, 4.7 optional. This skill produces **no `_navbar.md`** (no top navbar by design).

#### 4.1 `docs/docsify/index.html`

Copy from [assets/index.html](assets/index.html). Replace `{{PROJECT_NAME}}` and `{{PROJECT_DESCRIPTION}}`. There is **no** `{{PROJECT_ICON}}` (favicon is a built-in gradient mark). The entire reading-experience design system — cover support, settings drawer (gear, bottom-left), ⌘K command palette, theme/accent/typography, mermaid neutral theming, performance fixes — ships inside this one file; Standard mode needs no extra wiring.

#### 4.2 `docs/docsify/_sidebar.md`

Use the navigation from Step 3 (landing item → `docsify/README.md`; no emoji).

#### 4.3 `docs/docsify/_coverpage.md`

Copy from [assets/_coverpage.md](assets/_coverpage.md) and fill:
- `{{PROJECT_NAME}}` / `{{PROJECT_DESCRIPTION}}` — cover title / subtitle
- `{{COVER_TAGLINE}}` — one short punchy line
- `{{TAG_1..4}}` — 3–5 keyword pills (**no emoji**)
- `{{FIRST_CONTENT_ROUTE}}` / `{{FIRST_CONTENT_TITLE}}` — secondary button → an early content page (e.g. `business/02-...` → "三级筛查体系")

Strip the template's authoring comment header (the leading `<!-- ... -->` block) from the final file. Cover lives at `#/` (`onlyCover: true`, no scroll-into-content). Primary button "开始阅读" → home page `#/docsify/README`.

#### 4.4 `docs/docsify/README.md`

The **home page** (route `#/docsify/README`, independent from the cover). Generate (no emoji):
- Project name as `# heading`
- `{{PROJECT_DESCRIPTION}}` as the intro callout (`> ...`)
- A brief "what / who / how" + a small table linking to the main sections
- A short "怎么读本站" note (⌘K 搜索 · 左下角齿轮调阅读设置)

#### 4.5 `docs/docsify/scripts/start-docs.bat`

Copy from [assets/start-docs.bat](assets/start-docs.bat) verbatim.

#### 4.6 `docs/docsify/scripts/start-docs.sh`

Copy from [assets/start-docs.sh](assets/start-docs.sh) verbatim. Set executable: `chmod +x`. (Both serve from `docs/` root and print the `/docsify/` URL.)

#### 4.7 `docs/docsify/scripts/build-offline.py` (可选但建议一并放好)

Copy from [assets/build-offline.py](assets/build-offline.py) verbatim. Lets the user later compile a single-file offline build — see「离线单文件」below.

### Step 5: Verify

Confirm to user:
- [ ] Directory structure created (`docsify/`, `scripts/`)
- [ ] All `.md` files scanned with correct paths
- [ ] `index.html` generated with `{{PROJECT_NAME}}` / `{{PROJECT_DESCRIPTION}}` substituted
- [ ] `_sidebar.md` contains all content links (landing → `docsify/README.md`, no emoji)
- [ ] `_coverpage.md` generated (no emoji) — cover at `#/`, home at `#/docsify/README`
- [ ] `README.md` home page complete (no emoji)
- [ ] Startup scripts generated

Provide startup instructions:

**Windows**: `docs\docsify\scripts\start-docs.bat`
**Linux/Mac**: `chmod +x docs/docsify/scripts/start-docs.sh && ./docs/docsify/scripts/start-docs.sh`

Then visit **`http://localhost:3000/docsify/`** (server root is `docs/`; the site lives under `/docsify/`).

## 内置阅读体验（已固化在 index.html，无需额外接线）

Know it exists so you don't fight it and can point it out to the user:

- **封面 / 首页 独立路由**：`#/` 是纯封面（粒子背景 + 渐变标题，`onlyCover` → 不可下滑进正文）；首页内容在 `#/docsify/README`。点侧栏标题(app-name)→封面，点「文档首页」→首页。
- **左下角齿轮 → 设置抽屉**（玻璃拟态）。顶部是「搜索文档 ⌘K」入口（命令面板，复用 docsify 全文索引 + 快捷动作）；其下是阅读偏好，全部持久化到 localStorage：主题（跟随系统/亮/暗）· 强调色(5 套，渐变以强调色起头推导) · 字号 · 正文宽度 · 正文字体(无衬线/衬线) · 行距 · **目录密度**(紧凑/标准/宽松) · 专注模式 · 动效(开/减弱) · 阅读进度条 · 右侧目录开关。
- **⌘K / Ctrl+K** 全局唤出命令面板（方向键选择、Enter 跳转）。搜索框已**收进设置面板**，右上角不再放搜索。命令面板「视图切换」组含常用开关并标注单键快捷键：**专注模式 `F` · 收起/展开左侧菜单 `M` · 收起/展开右侧目录 `O` · 阅读进度条 `B`**。
- **单键快捷键**（跨平台一致、无需 Cmd/Ctrl）：`F`/`M`/`O`/`B` 对应上面四个开关；仅在不聚焦输入框、命令面板/设置抽屉未打开时触发。左侧菜单走 docsify 原生 `body.close`（桌面端隐藏了 hamburger，靠此快捷键/命令收起）。
- **目录树**：渐变标题、分组小标题、选中项淡色 pill、无下划线、**无 emoji**、密度可调。
- **右侧悬浮目录（`#right-toc`）滚动条自动隐藏**：默认不显示滚动条（thumb 透明 + Firefox `scrollbar-color: transparent`），滚动该目录时淡入、停止约 0.7s 或鼠标移开后淡出（`.scrolling` 类由 scroll 监听加/防抖移除，叠加 `:hover`）——不占视觉、不挤内容。
- **正文质感**：画布氛围光、软化字色、行内代码 chip、引用 callout、表格圆角卡片、h1–h4 层次。
- **宽表格横向滚动**：doneEach 给每个 `<table>` 外包一层 `.table-wrap`（`overflow-x:auto`），表 `width:max-content; min-width:100%`——**窄表仍撑满正文列、宽表（含长代码标识符等不可断内容）在正文列内左右滚动**，绝不溢出到右侧悬浮目录。其横向滚动条与右侧目录一致：默认隐藏、悬停 `.table-wrap` 时才淡入。
- **Mermaid**：跟随亮/暗主题、流程图子图与时序图 Note 一律中性灰蓝（**无黄色塑料感**）、卡片化、点击放大。
- **性能**：毛玻璃仅在浮层可见时启用、粒子离开封面即停、滚动监听单实例 rAF 节流 → 滚动顺滑。

Don't add emoji, and don't move search back to the top-right (it's intentionally merged into the settings panel).

## 离线单文件（可选，无需服务器）

docsify 默认靠 HTTP 拉取 markdown，所以**不能直接 `file://` 双击打开**（浏览器禁止 file:// 下取本地 md）。若要一个「双击即开、零服务器」的单文件版本：

```
python3 docs/docsify/scripts/build-offline.py
```

脚本把**本项目自己的东西**内联进单个 HTML：所有 markdown（`window.__MD__` + XHR/fetch 拦截，**后缀匹配**兼容 file:// 下相对 `_sidebar`/`_coverpage` 被拼前缀的情况）+ 本地相对资源（Animated 的 `assets/anim*`）。**共享第三方库（`cdn.archeruuu.com/libs` 的 docsify/mermaid/gsap/prism…）保持引用、不内联**。产出 **`docs/docsify/offline.html`**。

- **小巧**：只内联项目内容/动画（典型几百 KB），不再把 MB 级库塞进去。
- **双击即开**：file:// 打开即可、无需本地服务器；**需联网**以从 github 取共享库。
- **只请求你的 github**：除共享库走 `cdn.archeruuu.com` 外无任何外部请求（无 CDN、无网络字体）。
- 文档/动画改动后**重跑脚本**刷新。
- 正经**部署**直接当静态站托管即可（任意静态服务器，无需 Node）。

## Animation Mode (optional)

Only when the user picked **Animated**. Goal: a documentation site where the **core concepts are explained by interactive animations** (图 >> 文字), not just text + static diagrams. The engine lives in [assets/anim-kit/](assets/anim-kit/) — read [assets/anim-kit/README.md](assets/anim-kit/README.md) for the API.

### A. Copy the engine into the site

Copy this skill's `assets/anim-kit/` into the generated site:

```
docs/docsify/assets/anim-kit/{anim-core.js, anim.css, anim/...}   ← engine + 3 个通用范例 + _template.js
docs/docsify/assets/anim/                                          ← 本项目实际用到的动画（改范例或新写，放这里）
```

### B. Wire `index.html`

Paste the two snippets from [assets/anim-kit/head-snippet.html](assets/anim-kit/head-snippet.html):
- `<head>`: `<link rel="stylesheet" href="assets/anim-kit/anim.css" />`
- before `</body>`: GSAP from the self-hosted CDN (`cdn.archeruuu.com/libs/gsap/…`, **no external CDN** — if a new animation needs D3/anime, add it to the cdn repo first) + `anim-core.js` + one `<script src="assets/anim/<name>.js">` **per animation used** + the mount hook (a docsify `doneEach` plugin calling `AnimCore.mountAll()`).

Theme: `anim.css` defines the CSS color variables for both `body.dark` (this skill's convention) and `html[data-theme]`, and `anim-core.js` reads them from `document.body` — so animations auto-match the site's light/dark theme. No extra wiring.

### C. Author the animations (the heart of Animated mode)

**Mine the project for everything worth animating, and make a lot.** For each core concept, embed one minimal tag in the markdown and provide its module:

1. **Scan** the docs/codebase for **animatable concepts** — anything with motion, sequence, transformation, structure, or trade-off:
   - data / request flow through layers or a pipeline
   - algorithms · state machines · scheduling · concurrency / parallelism
   - architecture & dependency relationships, before/after comparisons
   - domain processes (AI: tokenize / attention / RAG / agent loop / KV-cache; web: request lifecycle / caching / scaling; data: ETL / query plan; etc.)
2. For each, choose the cheapest path that fits:
   - **Adapt** one of the 3 generic examples (`request-lifecycle` 穿层流程 / `dag-execution` 并行分支 / `crud-template` 模板 fan-out) when a concept maps to its shape — copy to `assets/anim/`, tweak its data / labels / `meta`.
   - **Author new** from [`anim-kit/anim/_template.js`](assets/anim-kit/anim/_template.js) — the common case for project-specific concepts.
3. **Embed** at the right spot in the markdown — one minimal tag, nothing else:
   ```html
   <div class="anim" data-anim="<name>"></div>
   ```
   (title + caption live in the JS `meta`, never in the markdown.)
4. **Aim for ≥1 animation per major doc page / core concept.** Richer is the whole point of this mode. Use `util.colors()` for theming, always guard `window.gsap`.

### D. Verify

- Every `data-anim="x"` in markdown has a matching `assets/anim/x.js` loaded by a `<script>` in `index.html`.
- `node --check assets/anim/*.js` passes.
- Serve and confirm animations play on scroll-into-view and the「↻ 重播」button works, in both light and dark.

## 静态资源（自托管，不用第三方 CDN）

所有与文档项目无关的第三方库与主题，统一托管在个人 CDN 仓库 **`garveyhu/cdn`** 的 `libs/` 下，经 **Cloudflare Worker 反代 + 自定义域名**访问（非 GitHub Pages、非第三方 CDN）。`index.html` 模板里已把全部资源链接写成：

```
https://cdn.archeruuu.com/libs/<lib>/<path>
```

- 涵盖：`docsify/`（核心 + vue.css 主题 + search/copy-code/pagination 插件）、`prism/components/`、`mermaid/`、`gsap/`、`panzoom/`、`katex/`（含 `fonts/`，数学公式）。
- **不引用任何第三方 CDN（jsdelivr 等）**；vue.css 已剥除 gstatic 字体 `@import`，站点用系统字体栈，**不加载任何网络字体**。
- 生成的站点天然只请求 `cdn.archeruuu.com` + 本站自己的 md / 项目专属动画（`docsify/assets/anim*`）。
- 要加一个库或 prism 语言：把文件放进 `cdn` 仓库的 `libs/<lib>/` 对应目录、`git push`（Cloudflare 边缘缓存随源站更新），再在 `index.html` 加一行引用即可。
- 这是个人化托管地址；若换人使用，需自建同结构的资源仓库（Cloudflare Worker + 域名，或 GitHub Pages）并把基地址改成自己的。
- 注意：更新 vue.css 等**压缩单行**文件时，剥 `@import` 要用「子串替换」而非「删整行」——整行就是整张表，删行会把样式删空。

## Customization

For theme color, favicon, code language, or markdown conventions, see [references/customization.md](references/customization.md).
