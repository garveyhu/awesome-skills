---
name: docs-site-creator
description: 创建文档站点的统一入口(双 provider 路由)。简单/内部/单项目文档 → Docsify provider(零构建、markdown 即站、可编译单文件离线 HTML);专业/对外/规模化文档 → Docusaurus provider(顶部多模块导航 + 侧栏 + 本页目录 + 中文本地搜索 + 暗色模式 + 可深度定制主题)。Use when the user asks to create a documentation site, docs portal, developer docs, or turn markdown files into a browsable site. Triggers: 建文档站, 文档站点, 文档网站, 生成文档站, docsify 站, docusaurus 站, documentation site, docs portal, developer docs。用户没点名引擎时,由本 skill 的选型表来判。
---

# Docs Site Creator(文档站统一入口)

一个 skill 管「把文档变成网站」这件事,底下两个 provider,**先选型、再读对应手册干活**:

| provider | 一句话 | 手册 |
|---|---|---|
| **Docsify** | 零构建:markdown 放好就是站,浏览器端渲染;可编译成双击即开的单文件离线 HTML | [providers/docsify/PROVIDER.md](providers/docsify/PROVIDER.md) |
| **Docusaurus** | 静态构建的专业文档站:顶部多模块标签 + 左侧栏 + 右侧本页目录 + 中文本地搜索 + 暗色模式,主题可定制到品牌级 | [providers/docusaurus/PROVIDER.md](providers/docusaurus/PROVIDER.md) |

## 选型(用户没点名引擎时按这张表判)

**默认倾向:简单用 Docsify,专业用 Docusaurus。** 逐条对信号,命中多的一边赢;五五开就问用户一句。

| 信号 | 选 |
|---|---|
| 单项目内部文档 / 速查手册 / 想「现在就能看」 | Docsify |
| `docs/` 里已有一堆 markdown,只想套个壳浏览 | Docsify |
| 要离线单文件(发微信 / 拷 U 盘 / 双击即开) | Docsify |
| 不想引入 Node 构建链(纯静态目录 + 任意 http server) | Docsify |
| **对外发布**的产品 / 开发者文档,代表门面 | Docusaurus |
| 读者分多类,需要**顶部模块标签**切换(用户手册 / API / 教程…) | Docusaurus |
| 要可靠的**全文搜索**(本地中文索引,页面多也快) | Docusaurus |
| 文档会**长大**:多人维护、版本化、i18n、以后加自定义页面 | Docusaurus |
| 要品牌级定制(设计 token、自定义首页、React 组件页共存) | Docusaurus |
| 站里要挂**独立子站**(如另一个前端应用挂在子路径下) | Docusaurus |

拿不准的边界情形:**内容 ≤ 20 页且读者是自己人 → Docsify;否则 Docusaurus。**

## 两个 provider 共同守的规矩

1. **内容先行**:站是壳,内容是身。`docs/` 还没有内容(或很薄)时,先用兄弟 skill
   **`wiki-creator`** 深扫代码库生成结构化 markdown,再回来套站;没装就用现有内容,不硬依赖。
2. **克制审美,禁 emoji**:侧栏、分组标题、页面标题、封面、mermaid 节点一律无 emoji;
   视觉产出按 `frontend-aesthetic` 规约走(三旋钮 + 设计读数,文档站取克制档)。
3. **不引第三方公共 CDN**:Docsify 走自托管库资源,Docusaurus 走 npm 依赖 + `@fontsource`
   自托管字体——生成的站点不请求 jsdelivr / unpkg / Google Fonts。
4. **mermaid 按渲染安全规范**(`classDef` 五属性、无 `%%{init:}%%`、note 黄底要兜底覆盖)。
5. **交付必验证**:起本地服务确认能开、侧栏齐、搜索可用(Docusaurus 还要构建零 broken link),
   再把访问方式一步步告诉用户。
