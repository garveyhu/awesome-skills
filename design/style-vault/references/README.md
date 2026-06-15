# Style Vault References

本目录是 style-vault skill 的资产库。按 **6 层粒度** 组织：product / style / page / block / component / token。

## 六层结构

| 层 | 一条资产 = | 能引用 | 被谁引用 |
|---|---|---|---|
| `products/` | 产品聚合：绑一个 style + 若干 pages/blocks/components/tokens | 所有下层 | —— |
| `styles/` | 整套设计语言：配色+字体+气质绑死 | pages / blocks / components / tokens | products |
| `pages/` | 页面样板：结构节奏，色字可换 | blocks / components / tokens | products / styles |
| `blocks/` | 场景块：一个完整功能段 | components / tokens | products / styles / pages |
| `components/` | 原子件：单个交互单元 | tokens | products / styles / pages / blocks |
| `tokens/` | 值与资源：调色板、字体、动效、边框、图标 | —— | 所有上层 |

引用方向**严格自上而下**。`product` 只做聚合视图（`refs` 字段显式声明），不产出新实现；`token` 是最底层（不引用任何东西）。

## ID 约定

**ID = 路径**（不含 `.md` 扩展名）。

- 单文件条目：`blocks/display/skillhub/table.md` → id = `blocks/display/skillhub/table`
- 文件夹条目：`products/acme-cold-saas/README.md` → id = `products/acme-cold-saas`（取文件夹路径）
- 所有路径段 kebab-case
- 冲突时加语义后缀（`table-striped` / `table-compact`），不用 `-v2`

### Namespace 子目录（强制）

`tokens` / `components` / `blocks` / `pages` 这 4 层在 bucket 下**必须**有一级 namespace 目录：

```
<layer>/<bucket>/<namespace>/<slug>[.md | /README.md]
```

- `<namespace>` = 拥有此条目的产品的短名（与 `products/<slug>` 末段对应：`acme` / `skillhub` / ...）
- 唯一例外：`_shared`——不被任何 product 关联的中性件
- `styles/` 和 `products/` 层不带 namespace（styles 已用 `<form>/<slug>` 二级桶；product 自身就是 namespace 源头）

**归属判定**（写入新条目时强制问自己）：

> 这条会被某个 product 关联吗？
> - 是 → 归 `<namespace>/`，namespace = 那个 product 的短名
> - 否（确定通用，多 style 可注入色字而成立） → 归 `_shared/`

**实战经验**：默认归 product namespace，只有"色字完全由上层注入、本身完全中性"才进 `_shared/`。多个 product 引用同一条优先归"视觉真正绑定的那个 product"，错引用的另一方走 unlink。

### 跨 namespace 引用

允许：一个 product 可以 `refs` 别 namespace 下的条目（包括 `_shared/`）。引用时写完整 id，sync 只校验目标存在，不校验 namespace 一致。

## Frontmatter 规范

每个资产顶部必须有 YAML frontmatter。

### 必填字段

- `id` — 与路径一致
- `type` — 所在层：`product` / `style` / `page` / `block` / `component` / `token`
- `name` — 人类可读名（可中文）
- `description` — 一句话定位（可中文）
- `tags` — 从 [`../assets/taxonomy.json`](../assets/taxonomy.json) 取值；新值要先改字典

### 可选字段

- `platforms` — `[web, ios, android, any]` 的子集，默认 `[any]`
- `theme` — `light` / `dark` / `both`
- `uses` — 依赖的下层 id 列表
- `preview` — 网站预览路由（非 token 层必填）

### product 专属字段

- `category` — 英文 slug，从 [`../assets/taxonomy.json`](../assets/taxonomy.json) 的 `category` 字典取（`productivity` / `content` / `lifestyle` / ...）。中文 label 由前端 `categoryMeta` 负责显示
- `refs` — 显式引用：`{ style, pages[], blocks[], components[], tokens{} }`

### 各层差异

| 层 | `preview` | `uses` | `refs` | `category` | `## Tokens` |
|---|---|---|---|---|---|
| product | 可选（有则走 pages[0]） | 通常空 | **必填** | **必填** | —— |
| style | 必填 | 推荐 | —— | —— | 推荐 |
| page | 必填 | 推荐 | —— | —— | —— |
| block | 必填 | 推荐 | —— | —— | —— |
| component | 必填 | 可选 | —— | —— | —— |
| token | 可选 | —— | —— | —— | **必填（可 JSON.parse）** |

### 示例

Product（聚合）：

```yaml
---
id: products/acme-cold-saas
type: product
name: Acme · 冷感工业 SaaS
description: 为量化团队打造的效率驾驶舱
platforms: [web]
theme: dark
category: productivity
refs:
  style: styles/saas-tool/cold-industrial-saas
  pages: [pages/landing/acme/saas-landing]
  blocks: [blocks/display/skillhub/table]
  components: [components/buttons/acme/ghost-button]
  tokens:
    palette: tokens/palettes/acme/slate-cyan-ice
    typography: tokens/typography/pairs/acme/ibm-plex-duo
tags:
  aesthetic: [minimal, industrial]
  mood: [cold, serious]
  stack: [react-antd-tailwind]
---
```

Block（场景块）：

```yaml
---
id: blocks/display/skillhub/table
type: block
name: Admin Table
description: 管理后台无边框表格
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm, serious]
  stack: [react-antd-tailwind]
uses: []
preview: /preview/blocks/display/skillhub/table
---
```

## 正文章节顺序

1. `# 条目名`
2. `> 一句话定位`
3. `## 视觉特征`
4. `## Tokens`（token 层必填，其他层有局部 token 也放这里）
5. `## 核心代码`
6. `## 适配指南`
7. `## 反模式 / 禁忌`
8. `## 引用关系`（可选，列 uses / used by）

## 外部入口

- 权威字典（tag / category / platform / theme）：[../assets/taxonomy.json](../assets/taxonomy.json)
- 分类查询工具：[../scripts/taxonomy.py](../scripts/taxonomy.py)
- 各层二级桶边界：
  - [styles/_CATEGORY.md](./styles/_CATEGORY.md)
  - [pages/_CATEGORY.md](./pages/_CATEGORY.md)
  - [blocks/_CATEGORY.md](./blocks/_CATEGORY.md)
  - [components/_CATEGORY.md](./components/_CATEGORY.md)
  - [tokens/_CATEGORY.md](./tokens/_CATEGORY.md)

## 维护

新增条目走 SKILL.md 里的沉淀流程。不要直接在本目录手搓文件——经 skill 流程写入可以顺带生成 preview、跑 sync 校验。
