# Products · 产品

## 层定义

**产品聚合视图**：把一个完整产品的风格组成一次性绑定起来——一个 Style（整站设计语言）+ 若干 Pages / Blocks / Components / Tokens。Product **不产出任何新实现**，只是把已有资产组装成"一个产品长这样"的引用包。

一个 Product 的价值在于 **快速复刻一整个产品的外观气质**——用户在网站上看到 Acme SaaS 风格喜欢，拿 id 粘给 AI，AI 沿着 `refs` 链一次性拉齐所有依赖，生成代码时色、字、按钮、表格全都对齐 Acme 的调性，不用每一维度单独指定。

## 分类（category）

与其它层用 **文件夹二级桶** 不同，Products 的分类由 frontmatter 的 `category` 字段决定，值从 [`../../assets/taxonomy.json`](../../assets/taxonomy.json) 的 `category` 字典取（单一真相源，中文 label / 排序 / 颜色都在那里）。

当前合法 slug：

| slug | 中文 | 适用 |
|---|---|---|
| `productivity` | 效率工具 | SaaS、驾驶舱、管理后台、表格 / Dashboard 类 |
| `content` | 内容 | 博客、长文阅读、新闻、播客、资讯流 |
| `lifestyle` | 生活 | 习惯追踪、健康、日记、冥想、家居 |
| `social` | 社交 | 社区、动态流、IM、创作者社区 |
| `commerce` | 电商 | 商城、购物车、支付、订单 |

新增 slug → 先改 `assets/taxonomy.json`，再用新 slug 写 product frontmatter；顺序反了 sync reject。

## 收录边界

**先问一句**：要不要产出新实现？
- **不产出新实现，只是把已有资产捆绑成一个"长这样的产品"** → 归 Products（本层）
- **要产出新实现**（新设计语言 / 新页面结构 / 新功能段 / 新控件 / 新 token）→ 按粒度归到对应下层（style / page / block / component / token）

Products 是 **最高层聚合视图**，和相邻层的边界：

- **Products ↔ Styles**：Style 定义整套设计语言（palette + typography + 气质）；Product 只引用一个 Style，不自己定义新语言。判定：如果这条条目本身在定义"冷感工业风要用哪些色"，归 Styles；如果它是说"Acme 这个产品用冷感工业风 + 这些页面 + 这些模块"，归 Products
- Products 不带 `preview` 页面渲染（前端 ProductCard 会拿 `refs.pages[0]` 的 preview 作为封面）
- Products 的 `refs` 是 **显式声明**，不用通用的 `uses` 字段——`refs` 把 style / pages / blocks / components / tokens 分门别类地列出来，方便前端聚合展示

## 一个 Product 必备

frontmatter 里：

- `type: product`
- `category` —— 英文 slug（见上表）
- `platforms` —— 支持的客户端（web / ios / android / any）
- `theme` —— light / dark / both
- `refs.style` —— 绑定一个 Style（必填，否则 sync reject）
- `refs.pages` / `refs.blocks` / `refs.components` / `refs.tokens` —— 可选但强烈建议至少有 1 个 page

## 命名约定

- Product 目录直接挂在 `products/` 下（没有二级桶子目录）
- 条目都是文件夹形式：`products/<slug>/README.md`
- slug 全程 kebab-case，可带品牌前缀（`acme-cold-saas`、`notion-like-workspace`）
- 一经收录不随意改名——外部网站的 prompt 卡片 id 会指过来

## 正文章节（简化）

Product 的正文比其它层短很多（因为真正的实现细节都在被引用的下层）：

1. `# 产品名`
2. `> 一句话定位`
3. `## 设计叙事` —— 这个产品想传达的气质、为什么这么组合
4. `## 组成` —— 引用链列表（Style · Pages · Blocks · Components · Tokens），附一句每条为什么被选

不需要 `## 核心代码`、`## 反模式`——这些都在下层资产里。Product 只做"一句话介绍 + 引用清单"。
