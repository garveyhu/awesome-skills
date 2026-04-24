---
name: style-vault
description: >
  Personal style library organized in 6 tiers (product / style / page / block / component / token).
  Use when: the user pastes a prompt copied from the style-vault website ("用 style-vault 里的 xxx 生成…"),
  or asks to build frontend matching a personal style preference.
  Triggers: "用 xxx 风格", "使用 style-vault skill", "参考 style-vault 里的",
  网站 Prompt 卡片粘贴、组件样式 / 管理后台 / 落地页等前端生成场景。
---

# Style Vault

一套按 **6 层粒度** 组织的个人风格资产库。主消费场景：**用户在 style-vault 网站浏览 → 复制某条风格的 prompt → 粘贴到本地 AI 会话 → 本地 AI（装了这个 skill）读取对应资产，生成对齐那套风格的前端代码**。

skill 的核心价值不在"能查到什么"，而是 **"拿到一个 id，就能按完整规格产出代码"**。资产条目把 tokens、样式要点、核心代码、反模式全部写死，消费时按层级自下而上合并即可。

## 六层结构

| 层 | 一条资产 = | 能引用 | 例子 |
|---|---|---|---|
| `products/` | 一个完整产品聚合：绑定一个 style + 若干 pages / blocks / components / tokens | 所有下层 | `products/acme-cold-saas` |
| `styles/` | 整套设计语言：配色 + 字体 + 气质全绑死 | pages / blocks / components / tokens | `styles/saas-tool/cold-industrial-saas` |
| `pages/` | 页面样板：结构节奏，色字可换 | blocks / components / tokens | `pages/landing/saas-landing` |
| `blocks/` | 场景块：一个完整功能段（表格 + 工具栏 + 分页） | components / tokens | `blocks/display/table` |
| `components/` | 原子件：单个交互单元（按钮、输入、卡片） | tokens | `components/buttons/ghost-button` |
| `tokens/` | 值与资源：调色板、字体、动效、边框、图标 | —— | `tokens/palettes/slate-cyan-ice` |

**引用方向严格自上而下**。`product` 是聚合视图（只引用、不产出新实现）；`token` 是最底层（不引用任何东西）。

## 读 / 写分工

本 skill 只负责**读**——消费资产 + 查询分类。**写入（新增 / 修改 / 删除风格）不在本 skill 处理**，请调 `style-vault-sediment` skill。

| 触发语 | 调哪个 skill |
|---|---|
| "用 xxx 风格" / 网站 prompt 卡片 / "参考 style-vault 里的 xxx" | **style-vault**（本 skill，走消费模式） |
| "沉淀" / "加到 vault" / "记录这套风格" / `/style-vault-sediment` | **style-vault-sediment** |
| "修改 <id>" / "删除 <id>" / "下掉 <id>" | **style-vault-sediment**（显式触发修改/删除） |

两 skill 硬依赖：`style-vault-sediment` 读 `style-vault/assets/taxonomy.json` 和 `style-vault/scripts/taxonomy.py`，安装时两个 skill 必须成对。

---

## 消费模式（Consumption，5 步）

**典型入口**：用户粘贴从 style-vault 网站复制的 prompt，里面含某条资产的 id（如 `styles/saas-tool/cold-industrial-saas` 或 `products/acme-cold-saas`）。

1. **解析主体 id 和叠加项**
   从 prompt 正文提取要用的资产 id。如果只给了人类名（"冷感 SaaS 风格"），先用 `scripts/taxonomy.py search --name "冷感"` 反查；找不到就问用户。叠加项是 prompt 里"改一下颜色"、"换 dark 主题"之类的变形请求，记在心里最后调。

2. **Read 主条目 md**
   ```
   ~/.agents/skills/style-vault/references/<id>/README.md   # 文件夹式（products / styles / pages）
   ~/.agents/skills/style-vault/references/<id>.md          # 单文件（blocks / components / tokens）
   ```
   路径错误立刻报错，不要猜替代。判断文件夹 vs 单文件：看该层的 `_CATEGORY.md` 的命名约定。

3. **递归读 `refs` / `uses` 链**
   - **products** 用 `refs`（显式声明 style / pages / blocks / components / tokens）
   - 其它层用 `uses`（依赖列表）
   把链上所有条目都读进来。悬空引用（id 对应文件不存在）跳过，最终提示一次。深度通常 ≤ 4 层。

4. **合并规格**
   Tokens 按 **下层给值、上层覆盖** 的顺序叠加（token 打底 → component → block → page → style → product）。"反模式 / 禁忌"是硬约束，生成代码时必须避开。冲突 token 以上层为准，在输出里一句话说明"xxx token 被 style 覆盖"。

5. **生成代码**
   按合并后的 tokens + 各层的"核心代码" + "样式要点"，结合用户需求产出代码。按上下文裁剪（用户只要表格就别把 page 的 hero 也塞进来）。输出末尾一两句话说明引用链 + 做了哪些取舍。

**消费模式永远只读**：不触发 sync、不写入 skill、不进网站仓。

### 消费模式示例

用户粘贴：
> 使用 style-vault skill，按 `products/acme-cold-saas` 给我做一个订单列表页。

AI 执行：
1. id = `products/acme-cold-saas`
2. 读 `references/products/acme-cold-saas/README.md`
3. 沿 `refs` 读：style (cold-industrial-saas) + page (saas-landing) + block (table, toolbar-bar) + component (ghost-button) + tokens (slate-cyan-ice, ibm-plex-duo)
4. 合并：palette 走 slate-cyan-ice；排版走 ibm-plex-duo；表格结构取自 block/display/table；按钮取自 ghost-button
5. 产出 React + AntD + Tailwind 代码，附："引用了 1 个 product + 1 style + 1 page + 2 blocks + 1 component + 2 tokens"

---

## 分类探索工具

skill 提供 `scripts/taxonomy.py`，AI 和人都可以用它查询分类体系与资产状况。**比直接读 MD 文件高效得多**——特别是在消费模式第 1 步反查 id、或用户问"vault 里有什么"时。

```bash
# 依赖：PyYAML。运行要用用户的全局 venv python：
~/.venvs/current/bin/python ~/.agents/skills/style-vault/scripts/taxonomy.py <subcommand>
```

常用子命令：

```bash
... taxonomy.py                                # 全貌总览 + 各维度计数
... taxonomy.py categories                     # 所有 product 分类
... taxonomy.py category productivity          # 某分类下的产品
... taxonomy.py tags aesthetic                 # 某 tag group 的所有值
... taxonomy.py tag aesthetic minimal          # 用了 minimal 这个 tag 的所有条目
... taxonomy.py type style                     # 所有 styles
... taxonomy.py platform web                   # 所有 web 条目
... taxonomy.py item products/acme-cold-saas   # 某条目详情 + refs + usedBy
... taxonomy.py search --aesthetic minimal --mood cold    # 多条件过滤
... taxonomy.py search ... --json              # 任意子命令加 --json 切 JSON 输出
... taxonomy.py history                            # 列出所有沉淀历史
... taxonomy.py history --author links             # 过滤某作者
... taxonomy.py history --since 2026-04-01         # 日期范围
... taxonomy.py history --mode delete              # 按模式过滤
... taxonomy.py history show <date-topic>          # 查看某批次 plan+report
```

沉淀历史的真相源在 `style-vault-sediment/assets/sediment-history/<author>/<date-topic>/`。

真相字典：**`assets/taxonomy.json`**（唯一源，前端仓 sync 时会复制一份过去）。

## Frontmatter 最小示例

Product（聚合层）：

```yaml
---
id: products/acme-cold-saas
type: product
name: Acme · 冷感工业 SaaS
description: 为量化团队打造的效率驾驶舱——密集表格、等宽数字、无暖色装饰。
platforms: [web]
theme: dark
category: productivity           # 英文 slug，中文 label 由前端字典展示
refs:
  style: styles/saas-tool/cold-industrial-saas
  pages: [pages/landing/saas-landing]
  blocks: [blocks/layout/toolbar-bar, blocks/display/table]
  components: [components/buttons/ghost-button]
  tokens:
    palette: tokens/palettes/slate-cyan-ice
    typography: tokens/typography/pairs/ibm-plex-duo
tags:
  aesthetic: [minimal, industrial]
  mood: [cold, serious]
  stack: [react-antd-tailwind]
uses: []
---
```

非 product 层（block / component / token 等）：

```yaml
---
id: blocks/display/table
type: block
name: Admin Table
description: 管理后台无边框表格，统一分页、中文本地化、行 hover 减淡
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm, serious]
  stack: [react-antd-tailwind]
uses: []
preview: /preview/blocks/display/table
---
```

Token 条目必带 `## Tokens` 下可 `JSON.parse` 的代码块。schema 全貌见 [references/README.md](references/README.md)。

## 常见错误

- 消费去网站仓拉资产（网站是 preview；权威源永远是 skill 的 `references/`）
- 合并 token 时层级覆盖顺序错（正确：token 打底 → component → block → page → style → product）
- 文件夹式条目 id 填了路径但文件名不对（`README.md` 必须）
- 跨层错误引用（token 引用了上层 / block 引用另一个 block）——消费时遇到直接跳过并提示

## 术语速查

- **资产（asset）**：`references/` 下的一条 md（或文件夹 + README.md）
- **主体 id / 叠加项**：消费模式里 prompt 指定的基础资产和附加变形
- **uses / refs**：前者是各层的依赖列表，后者是 product 的显式引用字段
- **悬空引用**：uses/refs 里写了 id 但对应文件不存在；消费时跳过并提示
- **category**：product 层专用，英文 slug，中文 label 存在 `assets/taxonomy.json`

## 入口索引

- 6 层总览与 frontmatter 规范：[references/README.md](references/README.md)
- 权威字典（tag / category / platform / theme）：[assets/taxonomy.json](assets/taxonomy.json)
- 分类查询工具：[scripts/taxonomy.py](scripts/taxonomy.py)
- 各层边界与二级桶：
  - [products/_CATEGORY.md](references/products/_CATEGORY.md)
  - [styles/_CATEGORY.md](references/styles/_CATEGORY.md)
  - [pages/_CATEGORY.md](references/pages/_CATEGORY.md)
  - [blocks/_CATEGORY.md](references/blocks/_CATEGORY.md)
  - [components/_CATEGORY.md](references/components/_CATEGORY.md)
  - [tokens/_CATEGORY.md](references/tokens/_CATEGORY.md)

## 维护原则

- **消费模式禁止触发任何 commit / sync / 写入**
- **skill 仓真实 git 根在 `/Users/links/.agents/skills/`**，git 命令用 `git -C /Users/links/.agents/skills` 形式
