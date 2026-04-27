# modify-workflow · 修改已有条目

**适用触发**：用户明确要改已有条目的 frontmatter 字段、正文章节，或对应的 preview tsx。

**核心定位**：本路径**不走 discovery**（条目已经在仓里）——它直接复用 [shared-workflow](shared-workflow.md) 的写入 / commit / 报告基础设施，差异只在"生成 diff 而非生成方案"。

---

## 入口

用户触发语示例：

- `改 tokens/palettes/acme/slate-cyan-ice 的 description`
- `把 blocks/display/skillhub/table 的 aesthetic 加上 organic`
- `把 slate cyan 那个 palette 的 mood 改成 calm`（模糊——靠 name 反查）
- `重写 products/acme-cold-saas 的"视觉特征"章节`

### 入口参数：id 识别

**精确 id** → 直接用。当前的 id 形态：

| 层 | 形态 | 例子 |
|---|---|---|
| product | `products/<slug>` | `products/acme-cold-saas` |
| style | `styles/<form>/<slug>` | `styles/saas-tool/cold-industrial-saas` |
| token / component / block / page | `<layer>/<bucket>/<namespace>/<slug>` | `components/buttons/acme/cyan-cta` · `tokens/layout/_shared/responsive-grid` |

**用户给了不带 namespace 的旧 id**（如 `components/buttons/ghost-button`）→ 不要直接报"找不到"，先 grep 同 bucket 下所有 namespace：

```bash
ls ~/.agents/skills/style-vault/references/components/buttons/*/ghost-button.md 2>/dev/null
# 命中 1 条 → 自动补 namespace 段，告诉用户"我找到 components/buttons/acme/ghost-button"
# 命中多条（同 base-name 跨 namespace）→ 列给用户选
# 命中 0 条 → 走 search --name 模糊反查
```

**模糊 id / 只给了名字** → 用 `search --name` 反查：

```bash
python3 ~/.agents/skills/style-vault/scripts/taxonomy.py \
  search --name "<用户说的名字>" --json
```

- 命中 1 条 → 贴出来让用户确认："`找到 1 条：products/acme-cold-saas · Acme 冷感工业 SaaS · 改这条？`"
- 命中多条 → 列出 id + name，让用户选序号
- 命中 0 条 → 提示用户换关键字，或换用 `type` / `tag` 过滤

### 不支持：改 id（重命名）

**明确拒绝**：修改不能改 id，因为 id 是依赖图的锚点——改了 id 就要同步改所有 refs 指向它的条目的 frontmatter，等于"删旧 + 建新"。

遇到这种请求，直接贴给用户：

```
改 id 语义上等于"删旧 + 建新"。请走两步：
  1. /delete-workflow 删掉 <旧 id>（带 cascade 清理引用者）
  2. /sediment-from-scratch 新建 <新 id>

直接 rename 会破坏依赖图，不支持。
```

---

## 支持的改动范围

**frontmatter 字段**（全部可改，除 `id` 外）：

| 字段 | 是否可改 | 注意 |
|---|---|---|
| `id` | × | 见上方 |
| `type` | × | 改 type 等于换层，也走"删+建" |
| `category` | ✓ | 新 slug 必须在 `taxonomy.json` 的 `category` 里 |
| `tags.aesthetic` / `tags.mood` / `tags.stack` | ✓ | 每个值必须在对应 tag 组里 |
| `platforms` | ✓ | 必须在 `platforms` 清单 |
| `theme` | ✓ | 必须在 `themes` 清单 |
| `name` | ✓ | 自由文本 |
| `description` | ✓ | 自由文本 |
| `refs.*`（product / style 层） | ✓ | 新目标 id 必须已存在，且拓扑方向正确（上层→下层） |
| `uses`（block / page 层） | ✓ | 同上 |
| `preview` | ✓ | 若改了路径，要真的把 tsx 挪到新位置 |

**正文章节**：

- `## 视觉特征`
- `## Tokens`（token 层必须；其它层可选）
- `## 核心代码`（tsx / css 代码块）
- `## 适配指南`
- `## 反模式`

**对应的 preview tsx**：**只在正文涉及组件重构时动**。仅改 frontmatter 或 description → 不碰 tsx。改了 `## 核心代码` 或结构 → 同步更新 tsx。

---

## 流程 7 步

以下步骤**大量复用** shared-workflow 的子步骤。本文档只列差异；步骤跳转用链接。

### 步骤 1 · 加载 taxonomy + 反查当前条目

**复用** [shared-workflow 步骤 1 · 加载分类字典](shared-workflow.md#步骤-1--加载分类字典)：先拿合法值清单。

**新增**：紧接着反查要改的条目全貌：

```bash
python3 ~/.agents/skills/style-vault/scripts/taxonomy.py \
  item <id> --json
```

输出的 JSON 保留到工作集——步骤 3 要用它和用户提议的改动做 diff。

**若 item 不存在**（返回 `Error: item '<id>' not found.`）→ 停止，让用户确认 id 拼写（或换用 `search`）。

### 步骤 2 · 展示当前条目 + 问"改什么"

把上一步的 JSON 渲染成人读版预览，直接贴给用户：

```
=== 当前条目 · products/acme-cold-saas ===

type:        product
category:    productivity
platforms:   [web]
theme:       dark
name:        Acme · 冷感工业 SaaS
description: 为量化团队打造的效率驾驶舱——密集表格、等宽数字、无暖色装饰。

tags:
  aesthetic: [minimal, industrial]
  mood:      [cold, serious]
  stack:     [react-antd-tailwind]

refs:
  style:     styles/saas-tool/cold-industrial-saas
  tokens.palette:    tokens/palettes/acme/slate-cyan-ice
  tokens.typography: tokens/typography/pairs/acme/ibm-plex-duo
  blocks:    [blocks/nav/acme/saas-cold-topbar, blocks/display/acme/saas-data-table]
  components: [components/buttons/acme/ghost-button, components/buttons/acme/cyan-cta]

preview:     /preview/products/acme-cold-saas
_path:       products/acme-cold-saas/README.md

--- 正文章节（由 _path 文件解析） ---
## 视觉特征 · 18 行
## 核心代码 · 62 行
## 适配指南 · 9 行
## 反模式   · 4 行

=== 想改什么？ ===
- 直接说字段（"description 改成 xxx"）
- 或说章节（"重写视觉特征"）
- 或说整段贴给我
```

**等用户说出具体改动意图**——不要自作主张帮他挑。

### 步骤 3 · 生成 diff

根据用户的话把改动整理成结构化 patch：

- **frontmatter 改动** → 用**对比表**展示（左：当前 / 右：改后）
- **正文改动** → 用 **unified diff** 格式

diff 预览模板：

````
=== 改动预览 · products/acme-cold-saas ===

## frontmatter 对比

| 字段 | 当前 | 改后 |
|---|---|---|
| description | 为量化团队打造的效率驾驶舱…… | 为量化 / 风控团队打造的效率驾驶舱…… |
| tags.aesthetic | [minimal, industrial] | [minimal, industrial, organic] |

## 正文 diff

```diff
--- products/acme-cold-saas/README.md (当前)
+++ products/acme-cold-saas/README.md (改后)
@@ ## 视觉特征 @@
-- 深 slate 底 + cyan 高亮
+- 深 slate 底 + cyan 高亮；辅以 organic green 做成功态
 - 等宽数字用 IBM Plex Mono
```

## preview tsx 改动
（无——本次不动 preview）

=== 合法值校验 ===
✓ tags.aesthetic 新增 "organic" 在 taxonomy.json
✓ 其它字段无新增 slug
````

**校验**（与 shared-workflow 步骤 3 的校验等价）：
- 所有新值必须在步骤 1 的合法值清单里
- 不在字典的 tag / category → 不要偷偷 auto-fill，打断让用户决策：`"<slug> 不在 taxonomy.json，先改字典还是换已有 slug？"` 与 [shared-workflow 错误处理矩阵](shared-workflow.md#错误处理矩阵) 的"步骤 3 AI 填了字典里没有的 tag"一致。

### 步骤 4 · 整体 review

**复用** [shared-workflow 步骤 4 · 整批 review](shared-workflow.md#步骤-4--整批-review) 的整批确认流程，差异在：

| 方面 | shared-workflow 原行为 | modify 分支行为 |
|---|---|---|
| 展示内容 | 完整写入方案（N 条条目的 frontmatter + 正文骨架） | 单条条目的 diff（见步骤 3） |
| 用户操作词典 | 整批确认 / 单条删 / 改 slug / 改 tag / 改正文 | 整体确认 / 撤销某项改动 / 再改 |
| 落盘文件 | `plan.md`（模式字段 "create"） | `plan.md`（模式字段 "modify"，带 `## 改动摘要` 节） |

用户操作动词：

| 操作 | 示例 |
|---|---|
| 整体确认 | "确认"、"go" |
| 撤销某项 | "别改 aesthetic"、"去掉 description 那条改动" |
| 再追加改动 | "顺便把 theme 改成 both" |
| 整体放弃 | "算了"、"reject" |

**用户确认后立即落盘 `plan.md`**（在执行改动前落盘，保证留痕）。落盘路径见下方"步骤 7 · 沉淀报告"节。

**整体放弃** → 结束，不做任何改动，**不落盘 `plan.md`**。

### 步骤 5 · 执行改动

**复用** [shared-workflow 步骤 5 · path.json 分叉](shared-workflow.md#步骤-5--pathjson-分叉) 判定 VAULT_OK + 上并发锁；
再**复用** [shared-workflow 步骤 6 · 逐条写入](shared-workflow.md#步骤-6--逐条写入) 的写入逻辑，差异在：

- **不是 Write 整文件，是 patch 现有文件**：
  - frontmatter 改动：读 MD → 解析 YAML → 改字段 → 写回（保留正文不变）
  - 正文改动：按章节定位 → 替换该章节 → 写回（保留其它章节不变）
- **只涉及 1 条条目，没有拓扑序**
- **sync 仍要跑**（网站仓改了 frontmatter 或 tsx 都要）

错误处理（sync 失败 / 用户 Ctrl-C）**复用** [shared-workflow 错误处理矩阵](shared-workflow.md#错误处理矩阵)，差异在**回滚方式**：

```bash
# skill 仓：用 git checkout 恢复单文件
cd ~/.agents/skills
git checkout -- style-vault/references/<id>.md
#  文件夹形条目：
git checkout -- style-vault/references/<id>/

# 网站仓（仅 VAULT_OK=true）：
cd "$VAULT"
git checkout -- frontend/src/preview/<id>.tsx

# 释放锁
rm -f "$VAULT/.style-vault-lock"
```

与 create 模式"前 k-1 条已写的保留供 debug"不同——**modify 失败就整个 checkout 回去**，因为只改了一条，没有保留意义。

### 步骤 6 · 双仓 commit

**复用** [shared-workflow 步骤 7 · 网站仓 commit](shared-workflow.md#步骤-7--网站仓-commitskill-仓延后到步骤-8)，但 commit message **用 `refactor` 前缀**：

**网站仓**（仅 VAULT_OK=true）：

```bash
cd "$VAULT"
git add frontend/src/preview/<id>.tsx
git commit -m "$(cat <<'EOF'
refactor(preview): update <id> preview

<正文：一句话说明改了 tsx 的什么（若 tsx 没动就跳过本步骤）>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

**若本次没动 tsx** → 跳过网站仓 commit。报告里注明"preview tsx 未变更"。

**skill 仓**（步骤 7 末尾聚合）：

```bash
cd ~/.agents/skills
git add style-vault/references/<改动的 MD>
git add style-vault-sediment/assets/sediment-history/<author>/<date-topic>-modify/
git commit -m "$(cat <<'EOF'
refactor(style-vault): modify <id>

<正文：列改了哪些字段 / 章节>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

**不 push**。

### 步骤 7 · 沉淀报告 + 落盘

**复用** [shared-workflow 步骤 8 · 沉淀报告](shared-workflow.md#步骤-8--沉淀报告) 的结构，差异：

- **folder 名**：`YYYY-MM-DD-<id-slug>-modify`（`<id-slug>` = id 的尾段，去斜杠换 dash，如 `products/acme-cold-saas` → `acme-cold-saas`）
- **report.md 的 `模式` 字段**：`modify`
- **多一节 `## 改了什么`**：列出改了哪几个字段 / 正文段

示例 report.md：

```markdown
# 沉淀报告 · 给 acme-cold-saas 加 organic tag

日期：2026-04-24
模式：modify
起点：用户指定 id
作者：links

## 改了什么

**frontmatter**：
- `tags.aesthetic` · `[minimal, industrial]` → `[minimal, industrial, organic]`
- `description` · 补充"风控团队"受众

**正文**：
- `## 视觉特征` · 加一句"辅以 organic green 做成功态"

**preview tsx**：未变更

## Commit

- skill 仓：`<hash>` · `refactor(style-vault): modify products/acme-cold-saas`
- 网站仓：未 commit（preview tsx 未变更）
- **均未 push**

## 下一步

1. `cd $VAULT/frontend && yarn dev` 肉眼过 preview 无 regression
2. OK 后 `git push`
3. 发现问题 `git reset --soft HEAD~1` 回到工作区

---
*由 style-vault-sediment skill 生成 · 模式：modify*
```

落盘路径：

```
~/.agents/skills/style-vault-sediment/assets/sediment-history/<author>/YYYY-MM-DD-<id-slug>-modify/
  ├── plan.md     (步骤 4 已落盘)
  └── report.md   (本步骤落盘)
```

不需要 `source.md`——modify 模式的"素材"就是原条目本身 + 用户指令。

**释放并发锁**：`rm -f "$VAULT/.style-vault-lock"`（与 shared-workflow 步骤 8 一致）。

**打印给用户**：把 report.md 完整内容贴到对话。

---

## 边界情况

| 场景 | 动作 |
|---|---|
| 改 `refs.style`（product 换底层 style） | 允许。sync 会校验新 style 存在——sync 失败就回滚。 |
| 改 `refs.tokens.palette`（换底层 palette） | 允许。同上，依靠 sync 校验。 |
| `tags.aesthetic` 加值 `minimal` → `[minimal, organic]` | 允许。只要 `organic` 在 taxonomy.json。 |
| 改 `category` 从 `productivity` → `content` | 允许。新 slug 必须在 `taxonomy.json` 的 `category` 里。 |
| 改了不在字典的 tag / category 新值 | 拒绝。对标 [shared-workflow 错误处理矩阵](shared-workflow.md#错误处理矩阵) 的"步骤 3 AI 填了字典里没有的 tag"，让用户先改字典。 |
| 只改 `name` / `description` | 允许。这种最常见，走完整 7 步但 tsx 不动、网站仓不 commit。 |
| 改 `preview` 字段指向新路径 | 允许，但必须同步把 tsx 真的挪到新位置（`git mv`），不然 sync 挂。 |
| 改 `uses` 数组加一项指向**不存在**的 block | 拒绝。sync 会报断链——在生成 diff 时就用 taxonomy.py 预校验目标条目存在。 |
| 用户说了 id 但 diff 里什么都没改（空改动） | 询问用户是否确认执行（可能只是想看看当前条目）；若用户说 "算了" → 结束不落盘。 |
| sync 失败 | 回滚：`git checkout -- <改动文件>`；skill 仓和网站仓分别处理；释放锁；打印错误 + 修复指引；**plan.md 保留**便于重跑 |
| VAULT_OK=false（网站仓不可联动） | 只改 skill 仓。report.md 注明"未联动网站"。没有 `yarn sync` 可跑——用 skill 侧轻量自检（frontmatter YAML 合法 + refs 目标存在）代替。 |
| 并发锁冲突 | 拒启，与 [shared-workflow 步骤 5.c 并发锁](shared-workflow.md#5c-并发锁) 一致。 |

---

## 约束复盘（modify 专属）

1. **id / type 不可变**：遇到就引导用户走 "delete + from-scratch"。
2. **patch 而非 rewrite**：修改用 patch 语义，保留未改章节的原样，避免 AI 顺手改别的。
3. **单 commit 原则继承自 shared-workflow**：skill 仓 + 网站仓各一个 commit；preview 没动就不 commit 网站仓。
4. **sync 失败整体回滚**：modify 不保留"部分成功"的状态，因为只改一条。
5. **plan.md / report.md 模式字段必须是 "modify"**：方便 Phase 4 的 `taxonomy.py history` 子命令筛选。

---

## 入口索引

- 主干：[shared-workflow](shared-workflow.md)
- 兄弟分支：[delete-workflow](delete-workflow.md)
- 上级：[../SKILL.md](../SKILL.md)
