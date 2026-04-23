# Style Vault References

本目录是 style-vault skill 的资产库。按五层分层组织风格原语、原子件、场景块、页面样板和整站调性。

## 五层结构

| 层 | 一条资产 = 什么 | 能引用 | 被谁引用 |
|---|---|---|---|
| `vibes/` | 整站调性：结构+配色+字体全绑死的完整形象 | archetypes / composites / atoms / primitives | —— |
| `archetypes/` | 页面样板：只管页面结构，色字可换 | composites / atoms / primitives | vibes |
| `composites/` | 场景块：一个完整功能块 | atoms / primitives | vibes / archetypes |
| `atoms/` | 原子件：单个交互元素 | primitives | vibes / archetypes / composites |
| `primitives/` | 设计原语：最细粒度的 token（色板/字体/间距等） | —— | 所有上层 |

## ID 约定

**ID = 路径**（不含 `.md` 扩展名）。

- 文件式条目：`composites/display/table.md` → id = `composites/display/table`
- 文件夹式条目：`composites/display/table/README.md` → id = `composites/display/table`（取文件夹路径）
- 路径段一律 kebab-case
- 冲突加后缀：`table-striped` / `table-compact`

## Frontmatter 规范

每个资产文件顶部必须有 YAML frontmatter。

### 必填字段

- `id` — 与路径一致
- `type` — 所在层：`vibe` / `archetype` / `composite` / `atom` / `primitive`
- `name` — 人类可读名
- `description` — 一句话定位
- `tags` — 从 `_tags.yaml` 取值；新值要先改字典

### 各层差异

| 层 | `preview` | `uses` | `tokens` |
|---|---|---|---|
| vibe | 必填 | 推荐 | —— |
| archetype | 必填 | 推荐 | —— |
| composite | 必填 | 推荐 | —— |
| atom | 必填 | 可选 | —— |
| primitive | 可选 | —— | **必填**（可 JSON.parse） |

### 示例 frontmatter

```yaml
---
id: composites/display/table
type: composite
name: Admin Table
description: 管理后台无边框表格，统一分页、中文本地化、行 hover 减淡
tags:
  aesthetic: [minimal]
  mood: [calm, serious]
  theme: [light]
  stack: [react-antd-tailwind]
uses:
  - primitives/palettes/admin-slate
preview: /preview/composites/display/table
---
```

## 正文章节顺序

1. `# 条目名`
2. `> 一句话定位`
3. `## 视觉特征`
4. `## Tokens`（primitive 必填；其他层若有自己的局部 token 也放这里）
5. `## 核心代码`
6. `## 适配指南`
7. `## 反模式 / 禁忌`
8. `## 引用关系`（列出 uses / 被 used by）

## 外部入口

- 各层边界与二级桶说明：见每层下的 `_CATEGORY.md`
  - [vibes/_CATEGORY.md](./vibes/_CATEGORY.md)
  - [archetypes/_CATEGORY.md](./archetypes/_CATEGORY.md)
  - [composites/_CATEGORY.md](./composites/_CATEGORY.md)
  - [atoms/_CATEGORY.md](./atoms/_CATEGORY.md)
  - [primitives/_CATEGORY.md](./primitives/_CATEGORY.md)
- Tag 字典（sync 脚本校验权威源）：[_tags.yaml](./_tags.yaml)

## 维护

新增条目走 SKILL.md 里的 10 步沉淀流程。不要在本目录直接手搓文件——经 skill 流程写入可以顺带生成 preview、跑 sync 校验。
