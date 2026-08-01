---
name: pdf-craft
description: Turn content into print-grade PDF documents via HTML+CSS and headless Chrome. Ships four battle-tested layout systems — govdoc (Chinese official/government filing), proposal (design-forward business proposal), report (technical whitepaper), resume — plus a typography linter that catches the mistakes that actually happen (straight quotes in Chinese text, justified text tearing apart in narrow table cells, tables split across pages, missing fonts). Use when the user wants a PDF deliverable: 商业计划书, 政府申报材料, 立项书, 结题报告, 技术方案, 白皮书, 调研报告, 简历, 正式文件, 出个 PDF, 排版成 PDF, 做成 PDF, 生成 PDF, business plan PDF, proposal PDF, whitepaper PDF, resume PDF, print-ready document, typeset a document. NOT for reading/merging/splitting existing PDFs (use the `pdf` skill), Word output (use `docx`), or screen-reading web articles (use `beautiful-article`).
---

# PDF Craft

把内容排成**印刷级 PDF**。技术路径固定：**HTML + CSS → headless Chrome → PDF**。

为什么不是 Markdown/Word 转换：那些工具只能操作模板暴露的几个旋钮，做不了封面出血、精确分页控制、自绘图表、三线表。CSS 有完整的分页排版能力（`@page` / `page-break-*` / 精确到 mm），这是唯一能做到"印刷级"的路径。

**这个 skill 的价值不在转换脚本（二十行），在 `templates/` 里的版式规范和 `lint.mjs` 里的自检——那些是踩坑踩出来的。**

```
pdf-craft/
├── scripts/     build（出 PDF）· lint（排版自检）· preview（截图验版式）
├── templates/   govdoc · proposal · report · resume —— 每个都是自包含单文件，复制即用
└── references/  typography-zh（中文排版规范）· components（图表组件）· pitfalls（踩坑账）
```

模板**内联完整 CSS**、不拆公共样式表：各版式的基线参数本就不同（公文页边距 25mm/白底，简历 12mm/高密度），拆开只会变成双份维护，而单文件复制到任何地方都能直接跑。

---

## 第一步：选版式（不要跳过）

问自己"这份东西给谁看、在什么场合用"，然后对号入座：

| 版式 | 用在哪 | 视觉特征 |
|---|---|---|
| **govdoc** | 政府申报、立项书、结题报告、正式方案、对公文件 | 白底、居中封面、中文数字章节（一、（一）1.）、三线表、单色、页码 |
| **proposal** | 给投资人/客户看的 BP、产品方案、品牌提案 | 有设计感：品牌色、大字排版对比、卡片、数据块 |
| **report** | 技术方案、架构设计、白皮书、调研报告 | 结构化、代码块、图表编号、术语表、可带页眉导航 |
| **resume** | 简历 | 单页高密度、时间线、技能矩阵、无封面 |

**选错版式比排版丑更糟。** 拿 proposal 的设计感版式去交政府材料，对方会觉得不严肃；拿 govdoc 去见投资人，会显得没想法。

不确定时问用户：「这份东西是递给政府/甲方走流程的，还是给投资人/客户看的？」

---

## 第二步：选模式

| 模式 | 输入 | 什么时候用 |
|---|---|---|
| **A · 内容优先** | 已有 Markdown → 套版式 | 纯文本类文档（报告正文、说明材料），快 |
| **B · 版式优先** | 直接写 HTML | **需要封面、自绘图表、框注、复杂表格时必须走这条** |

**关键判断**：Markdown 表达不了封面、象限图、柱状图、框注、跨列表格。**只要文档需要其中任何一样，直接走模式 B**，别先转 md 再修——那会浪费两遍功夫。

商业计划书、提案、白皮书基本都是模式 B。

### 模式 A 的做法
读 md → 生成语义化 HTML（`<h2>` / `<table>` / `<ol>`）→ `<link>` 引对应版式 CSS → build。

### 模式 B 的做法
从 `templates/<版式>.html` 复制骨架 → 填内容 → 需要的图表用纯 CSS/DOM 画（见 `references/components.md`）→ build。

---

## 第三步：生成与验证

```bash
# 1. 出 PDF
node <skill>/scripts/build.mjs <input.html> <output.pdf>

# 2. 排版自检（必跑）
node <skill>/scripts/lint.mjs <input.html>

# 3. 肉眼验版式（PDF 没法直接看，用打印模式截图代替）
node <skill>/scripts/preview.mjs <input.html> 5
# 然后用 Read 工具逐张看 preview-*.png
```

**三步都要做完。** 只 build 不 lint 不 preview，等于没验证——今天所有的排版事故都是这么来的。

看完预览图记得删掉：`rm -f preview-*.png`

---

## 自检清单（lint.mjs 覆盖 + 人工确认）

`lint.mjs` 自动查：

| 检查项 | 为什么 |
|---|---|
| 正文含中文的英文直引号 `"` | 中文排版必须用 `“ ”`，直引号一眼就露怯 |
| 引号配对（总数 + 逐行） | 正则批量替换极易配对错乱 |
| `text-align: justify` 用在窄容器 | **最阴的坑**：单元格里一行后面跟着不可断开的长 token（代码名/英文词），前半行会被强行拉满、字距散开 |
| 表格缺 `page-break-inside: avoid` | 表格被撕成两页 |
| 引用了网络字体 | 离线渲染必失败，静默 fallback |
| 标题缺 `page-break-after: avoid` | 标题孤零零落在页尾 |

**人工必须确认**（脚本查不了）：

- [ ] 数字表格内部自洽——分项之和 = 合计，利润 = 收入 − 成本（**拿计算器验一遍**，有人会验算）
- [ ] 中文词没被容器切断
- [ ] 封面信息完整（文件名称、编制人、日期、版本）
- [ ] 页码正常
- [ ] 长表格跨页时表头是否需要重复

---

## 中文排版规范

**动手前读 [references/typography-zh.md](references/typography-zh.md)**，那里是最容易错的部分：引号、中文数字 vs 阿拉伯数字的分工、中英文间距、首行缩进、标点缩进、三线表规范、避头尾。

---

## 依赖

需要 Playwright（脚本会自动在几个常见位置找）。找不到时按提示装：

```bash
npm i -D playwright && npx playwright install chromium
```

或用环境变量指定已有的：`export PDFCRAFT_PLAYWRIGHT=/path/to/node_modules`

字体全部走**本机系统字体**（PingFang SC / Songti SC / JetBrains Mono），**绝不引网络字体**——离线渲染时会静默 fallback，字全变样还不报错。

---

## 常见坑

完整踩坑账见 [references/pitfalls.md](references/pitfalls.md)。三条最要命的：

1. **`justify` + 窄容器 + 不可断开 token = 字距爆散**。表格一律左对齐，正文才用两端对齐。
2. **改数字要全局改**。同一个数字往往出现在摘要、正文表、图表标注三处，漏一处就穿帮。改完用 grep 扫一遍旧值。
3. **`preferCSSPageSize: true` 时 `@page :first { margin: 0 }` 会让首页没有页脚空间**——正好可以用来让封面不显示页码，但要知道这是有意为之。

---

## 输出约定

- PDF 放用户指定位置；没指定就和源文件同级
- **HTML 源文件保留**（放 `_pdf/` 或同级），下次改内容重新 build 即可，不要生成完就删
- 把 `build.mjs` 的调用方式写进交付说明，让用户以后能自己重新生成
