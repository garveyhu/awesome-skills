# anim-kit —— docsify 文档动画引擎

一套轻量、自包含的文档动画系统：markdown 里写一个极简单标签，实现放在 `assets/anim/` 一动画一文件。配合 GSAP / D3 做「动画驱动」的技术文档（图 >> 文字）。**仅在「动画模式」下引入。**

## 文件

| 文件 | 作用 |
|---|---|
| `anim-core.js` | 框架：注册表 + IntersectionObserver 可见即播 + 重播按钮 + 主题取色 |
| `anim.css` | 动画卡片样式 + 主题色变量（兼容 `body.dark` / `html[data-theme]`） |
| `anim/_template.js` | 写新动画的模板（带注释的范例） |
| `anim/*.js` | 3 个**通用范例**（`request-lifecycle` / `dag-execution` / `crud-template`），当写法参考 |

> mermaid 图的点击放大用本 skill 自带的 panzoom 方案（见 `assets/index.html`），不在 anim-kit 内。

## 在 markdown 里用

```html
<div class="anim" data-anim="request-lifecycle"></div>
```
仅此一行。标题与底部说明写在动画 JS 的 `meta` 里，不在 markdown 重复。

## 写一个新动画

1. 复制 `anim/_template.js` → `anim/<名字>.js`。
2. 改 `AnimCore.register('<名字>', factory, { title, caption })`。
3. `factory(stage, host, util)` 里用 `util.svg()` 画 SVG、`util.colors()` 取主题色、`window.gsap` 做时间线，返回 `{ play, reset }`。
4. markdown 里嵌 `<div class="anim" data-anim="<名字>"></div>`。
5. 在站点 `index.html` 末尾加一行 `<script src="assets/anim/<名字>.js"></script>`。

### API 速记
- `factory(stage, host, util)` → 返回 `{ play, reset }`
- `util.colors()` → `{ bg, fg, soft, mut, border, accent, accent2, accent3, warn, danger }`（**一律用它取色，勿硬编码**）
- `util.svg(tag, attrs)` → 建 SVG 元素
- 滚动进视口自动 `play()`；右上角「↻ 重播」自动 `reset()` 后 `play()`
- 务必判 `window.gsap`，无 gsap 时给静态终态兜底

## 通用范例（写法参考）

只内置 3 个**与具体业务无关**的范例，覆盖三种常见动画写法，供照着写：

- `request-lifecycle` —— 一个包**线性穿过多层**，每站点亮 + 旁白（适合任何流水线 / 调用链 / 分步流程）
- `dag-execution` —— **并行 + 分支的图调度**（适合任何并发 / 条件分支流程）
- `crud-template` —— **一套模板 fan-out 到 N 个对象**（适合"一处定义、多处复用"的结构）

> 动画模式的精髓是**为本项目的核心概念做专属动画**：相近的范例改 `meta` / 数据即可，没有对应的照 `_template.js` 新写。不要硬套不相干的范例。

## 接入站点（动画模式 index.html 要加的）

`<head>` 里加 `anim.css`：
```html
<link rel="stylesheet" href="assets/anim-kit/anim.css" />
```
`</body>` 前加引擎库（GSAP 必需；D3/anime 按需）+ 各动画 + 挂载钩子：见 `head-snippet.html`。
