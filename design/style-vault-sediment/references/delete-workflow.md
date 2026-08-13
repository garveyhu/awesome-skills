# delete-workflow · 删除已有条目

**适用触发**：用户明确要删已有条目（单条或批量）。

**核心定位**：删除 = 从 skill 仓和网站仓**移除**条目文件 + **维护**依赖图。本路径**不走 discovery**——重点是**反向引用检查**和 **cascade 语义**，其余（锁 / commit / 报告）全部复用 [shared-workflow](shared-workflow.md)。

---

## 入口

用户触发语示例：

- `删 tokens/palettes/acme/slate-cyan-ice`
- `删掉 components/buttons/acme/ghost-button`
- 批量：`删 blocks/display/skillhub/table, components/buttons/acme/ghost-button`
- 模糊：`把 slate cyan 那个 palette 删了`（走 `search --name` 反查，同 [modify-workflow 入口参数](modify-workflow.md#入口参数id-识别)）

**入口参数处理**：

1. 解析出一条或多条 id
2. 每条都用 `taxonomy.py item <id> --json` 校验存在性
   - 不存在 → 让用户确认拼写
   - 存在 → 进入流程

---

## Cascade 语义（重点）

**cascade = 把引用者里指向被删 id 的那一条 ref 清掉**。**只改引用者的 frontmatter**，不删引用者本身。

### 具体例子

**例 1 · 删 token**

删：`tokens/palettes/mint-analytics/cold-mint`

引用者：`blocks/display/mint-analytics/mint-table`，它的 frontmatter：

```yaml
refs:
  tokens:
    palette: tokens/palettes/mint-analytics/cold-mint  # ← 这一条指向被删 id
```

cascade 动作：把 `refs.tokens.palette` **清空**（把 key 整条删掉，或根据 taxonomy 约定设为 null）。mint-table 本身**保留**。

改后：

```yaml
refs:
  tokens: {}
```

**例 2 · 删 block，被 product 引用**

删：`blocks/display/acme/saas-data-table`

引用者：`products/acme-cold-saas`，它的 frontmatter：

```yaml
refs:
  blocks:
    - blocks/nav/acme/saas-cold-topbar
    - blocks/display/acme/saas-data-table       # ← 这一项被清
```

cascade 动作：从 `refs.blocks` 数组里**移除这一项**（不是整个数组）。product 本身保留。

改后：

```yaml
refs:
  blocks:
    - blocks/nav/acme/saas-cold-topbar
```

**例 3 · 同时删多条，互相引用**

删：`[tokens/palettes/mint-analytics/cold-mint, blocks/display/mint-analytics/mint-table]`

若 `mint-table` 引用了 `cold-mint`——这两条都在删除列表，**无需 cascade**（引用者本身也被删）。只需处理被删集合**之外**的引用者。

### 为什么默认拒绝有引用者的删除

依赖图完整性是 vault 的硬约束——断链的条目会让 `yarn sync` 报错，让上层条目变成孤儿。默认拒绝迫使用户**显式授权 cascade**，避免误删连锁破坏。

---

## 流程 8 步

### 步骤 1 · 加载 taxonomy

**复用** [shared-workflow 步骤 1 · 加载分类字典](shared-workflow.md#步骤-1--加载分类字典)。

**为什么要**：删除本身不涉及新 slug，但 cascade 改引用者 frontmatter 时要校验剩余值仍然合法（如删空数组后是否留下非法结构）。

### 步骤 2 · 反向引用检查

对**每条**待删 id 调：

```bash
python3 ~/.agents/skills/src/mirror/style-vault/scripts/taxonomy.py \
  item <id> --json
```

**读输出的 `usedBy` 字段**（反向引用列表，由 taxonomy.py 扫所有条目的 `refs` / `uses` 反向汇总）。结构形如：

```json
{
  "id": "tokens/palettes/mint-analytics/cold-mint",
  "usedBy": [
    {"id": "blocks/display/mint-analytics/mint-table", "field": "refs.tokens.palette"},
    {"id": "styles/saas-tool/cold-mint-saas", "field": "refs.tokens.palette"}
  ]
}
```

> **fallback**：若当前 taxonomy.py 版本还没有 `usedBy` 字段（历史工具未升级），用 `search` + 枚举所有 item 的 refs 做一次全扫代替——但正常情况 taxonomy.py 应直接提供 `usedBy`。

**汇总**成这样的表，贴给用户：

```
=== 反向引用检查 ===

[1] tokens/palettes/mint-analytics/cold-mint
    被 2 条引用：
    - blocks/display/mint-analytics/mint-table · refs.tokens.palette
    - styles/saas-tool/cold-mint-saas · refs.tokens.palette

[2] components/buttons/acme/ghost-button
    被 1 条引用：
    - products/acme-cold-saas · refs.components[0]

[3] blocks/display/skillhub/table
    无引用方（可直接删）
```

### 步骤 3 · 若有引用者 → 三选

**只要有任何一条待删 id 的 usedBy 非空**，默认拒绝，给用户三选：

```
上述条目有引用者。默认拒绝删除（防破坏依赖图）。请选：

  1) 先修引用者：我退出，你手动把引用者改掉（或走 /modify-workflow），再回来删
  2) 退出：这次不删了
  3) cascade（强删）：把引用者 frontmatter 里指向这些 id 的那一条 ref 清掉，保留引用者本身

回复 1 / 2 / 3。
```

**用户选 2（退出）** → 直接结束，**不释放任何锁**（还没到步骤 5 上锁），**不落盘 plan.md**，对话结束。

**用户选 1（先修）** → 同样结束，可贴一句提示："好，你修完再来；若想用 cascade 省事，下次直接选 3。"

**用户选 3（cascade）** → 进入步骤 4。首次使用 cascade 需要额外提示，见"安全兜底"节。

**若所有待删 id 的 usedBy 都空** → 跳过三选，直接进步骤 4。

### 步骤 4 · 整体确认

**复用** [shared-workflow 步骤 4 · 整批 review](shared-workflow.md#步骤-4--整批-review) 的整批确认机制，差异在展示内容：

```
=== 删除预览 ===

## 将删除的文件（N 条）

| 条目 | skill 仓文件 | 网站仓 tsx |
|---|---|---|
| tokens/palettes/cold-mint | style-vault/references/tokens/palettes/cold-mint.md | frontend/src/preview/tokens/palettes/cold-mint.tsx |
| components/buttons/ghost-button | style-vault/references/components/buttons/ghost-button.md | frontend/src/preview/components/buttons/ghost-button.tsx |
| products/acme-cold-saas | style-vault/references/products/acme-cold-saas/ (整目录) | frontend/src/preview/products/acme-cold-saas.tsx |

## Cascade 改动（N 个引用者）

| 引用者 | 改动 |
|---|---|
| blocks/display/mint-table | refs.tokens.palette 清空 |
| styles/saas-tool/cold-mint-saas | refs.tokens.palette 清空 |

=== 确认执行？===
  Y) 确认，执行删除 + cascade
  N) 放弃
```

用户操作词典：

| 操作 | 示例 |
|---|---|
| 确认执行 | "确认"、"go"、"Y" |
| 放弃 | "算了"、"reject"、"N" |
| 从批次里去掉某条 | "别删 ghost-button" |

**二次确认触发条件**：见"安全兜底"节。

**用户确认后立即落盘 `plan.md`**（与 shared-workflow 步骤 4 一致）。路径见"步骤 8 · 沉淀报告"节。

**放弃** → 结束，不删不改，**不落盘 plan.md**。

### 步骤 5 · 执行删除

**复用** [shared-workflow 步骤 5 · path.json 分叉](shared-workflow.md#步骤-5--pathjson-分叉) 判定 VAULT_OK + 上并发锁。

执行顺序（**反拓扑序**——先删上层再删下层，避免瞬时断链；但由于我们用 cascade 而非顺序 sync，实际上顺序不那么关键，统一"先删所有文件再跑 sync"即可）：

#### 5.a skill 仓 rm

```bash
cd ~/.agents/skills/src/mirror

# 文件形条目
rm -f style-vault/references/tokens/palettes/cold-mint.md

# 文件夹形条目（product / 复杂 style）——必须 rm -rf 整目录
rm -rf style-vault/references/products/acme-cold-saas/
```

**易错点**：文件夹形条目只删 `README.md` 会留下其它子文件造成孤儿目录。必须 `rm -rf` 整个目录。

#### 5.b 网站仓 rm（仅 VAULT_OK=true）

```bash
cd "$VAULT"

rm -f frontend/src/preview/tokens/palettes/cold-mint.tsx
rm -f frontend/src/preview/components/buttons/ghost-button.tsx
rm -f frontend/src/preview/products/acme-cold-saas.tsx
```

#### 5.c Cascade patch 引用者（仅用户选了 cascade）

按步骤 2 汇总的 usedBy 清单，对每个引用者：

1. 读引用者的 MD 文件
2. 解析 frontmatter YAML
3. 根据 `field` 路径定位到那一条 ref：
   - 单值字段（如 `refs.tokens.palette`）→ 整条 key 删掉，或设为 null（与 taxonomy 约定一致）
   - 数组项（如 `refs.blocks[N]` / `refs.components[N]` / `uses[N]`）→ 从数组里移除这一项
4. 写回 MD（保留正文不变）

**并行网站仓 preview tsx**：引用者的 tsx 不强制改（preview 通常不依赖 refs 字段），但若 preview 渲染时 import 了被删组件 → sync 会报错，按常规 sync 失败处理。

### 步骤 6 · yarn sync 校验

**复用** [shared-workflow 步骤 6 · 逐条写入](shared-workflow.md#步骤-6--逐条写入) 里的 sync 逻辑：

```bash
cd "$VAULT/frontend" && yarn sync
```

- 校验所有剩余条目无断链
- 校验 cascade 改过的引用者 frontmatter 合法
- 校验 preview 目录无孤儿 tsx（被删 id 对应的 tsx 真的删了）

**sync 失败 → 回滚**，见下方"常见错误"节。

**VAULT_OK=false** 时没有 `yarn sync` 可跑——用 skill 侧轻量自检代替：
- 确认被删条目的 MD 真的没了
- 遍历剩余条目的 refs / uses，没有指向已删 id 的
- cascade 改过的条目 YAML 合法

### 步骤 7 · 双仓 commit

**复用** [shared-workflow 步骤 7 · 网站仓 commit](shared-workflow.md#步骤-7--网站仓-commitskill-仓延后到步骤-8)，commit message **用 `feat(...): remove` 前缀**（设计文档 § 5.2 钦定）：

**网站仓**（仅 VAULT_OK=true）：

```bash
cd "$VAULT"
git add -u frontend/src/preview/   # -u 包含删除
git commit -m "$(cat <<'EOF'
feat(preview): remove <id 或"N 条"> preview

<正文：列被删的 preview tsx / cascade 改过的 preview（若有）>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

**skill 仓**（步骤 8 末尾聚合）：

```bash
cd ~/.agents/skills/src/mirror
git add -u style-vault/references/   # -u 包含删除
git add style-vault/references/      # cascade 改过的 MD 也一起 add
git add style-vault-sediment/assets/sediment-history/<author>/<date-topic>-delete/
git commit -m "$(cat <<'EOF'
feat(style-vault): remove <id 或"N 条">

<正文：
- 被删条目清单
- cascade 改过的引用者清单
- 起点：用户指定 id
>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

**不 push**。

### 步骤 8 · 沉淀报告 + 落盘

**复用** [shared-workflow 步骤 8 · 沉淀报告](shared-workflow.md#步骤-8--沉淀报告) 的结构，差异：

- **folder 名**：`YYYY-MM-DD-<id-slug>-delete`
  - 单条：`<id-slug>` = id 尾段（`tokens/palettes/cold-mint` → `cold-mint`）
  - 批量：取主删条目的 slug，或用户给的"批次主题"slug，如 `YYYY-MM-DD-mint-cleanup-delete`
- **report.md 的 `模式` 字段**：`delete`
- **多两节 `## 删了什么` / `## cascade 改了哪些`**

示例 report.md：

```markdown
# 沉淀报告 · 清理 mint 系列

日期：2026-04-24
模式：delete
起点：用户指定 id
作者：links

## 删了什么（3 条）

| 类型 | ID | skill 路径 | 网站 tsx |
|---|---|---|---|
| token | tokens/palettes/cold-mint | references/tokens/palettes/cold-mint.md | preview/tokens/palettes/cold-mint.tsx |
| block | blocks/display/mint-table | references/blocks/display/mint-table.md | preview/blocks/display/mint-table.tsx |
| component | components/buttons/mint-btn | references/components/buttons/mint-btn.md | preview/components/buttons/mint-btn.tsx |

## cascade 改了哪些（2 个引用者）

| 引用者 | 字段 | 改动 |
|---|---|---|
| styles/saas-tool/cold-mint-saas | refs.tokens.palette | 清空（指向已删的 cold-mint） |
| products/mint-analytics | refs.blocks[1] | 移除（指向已删的 mint-table） |

## Commit

- skill 仓：`<hash>` · `feat(style-vault): remove mint cleanup (3 条)`
- 网站仓：`<hash>` · `feat(preview): remove mint cleanup preview (3 条)`
- **均未 push**

## 下一步

1. `cd $VAULT/frontend && yarn dev` 肉眼过一遍，确认 cascade 改过的 cold-mint-saas / mint-analytics 还能渲染
2. OK 后 `git push` 两仓
3. 发现问题 `git reset --soft HEAD~1` 回到工作区（skill 和网站仓各自操作）

---
*由 style-vault-sediment skill 生成 · 模式：delete*
```

落盘路径：

```
~/.agents/skills/src/mirror/style-vault-sediment/assets/sediment-history/<author>/YYYY-MM-DD-<id-slug>-delete/
  ├── plan.md     (步骤 4 已落盘)
  └── report.md   (本步骤落盘)
```

不需要 `source.md`——delete 的"素材"是被删条目本身（git history 就是溯源）。

**释放并发锁**：`rm -f "$VAULT/.style-vault-lock"`。

**打印给用户**：report.md 完整内容贴到对话。

---

## 安全兜底

为防手滑 / 大规模误删，额外触发二次确认的场景：

### 1. 批量删除 > 3 条

```
⚠️ 本次将删除 <N> 条条目（>3 触发二次确认）：
<完整清单>

确认删除这 <N> 条？请**重复输入** "确认删除 <N> 条"（原字符匹配才继续）。
```

### 2. cascade 改动 > 5 个引用者

```
⚠️ 本次 cascade 将修改 <M> 个引用者的 frontmatter（>5 触发二次确认）：
<引用者清单>

这是范围比较大的改动。确认继续？请**重复输入** "确认 cascade <M> 个引用者"。
```

### 3. 用户首次使用 cascade

在本机的 `sediment-history/` 里**没有任何** `*-delete/plan.md` 记录"mode: delete, cascade: true"的情况 → 判定为首次：

```
提示：你即将首次使用 cascade 删除。

cascade 会**修改引用者条目的 frontmatter**（不是只删一条）：
  - 把引用者的 refs / uses 里指向被删 id 的那一项清掉
  - 引用者条目本身保留

这对依赖图完整性是有影响的改动，不可 undo（除了 git）。

确认使用 cascade？(Y / 改选退出)
```

（用 `taxonomy.py history --mode delete` 也可以查——但那是 Phase 4 才有。在 Phase 3 阶段用 `ls ... | grep -c delete` 之类的兜底探测亦可。）

### 二次确认失败

任何一项二次确认用户没给出原字符 → 视为**退出**，不删不改，不落盘 plan.md，释放锁。

---

## 常见错误

| 场景 | 动作 |
|---|---|
| 删了但引用者没 cascade（用户选了"强删"但我漏 patch 了某个引用者） | sync 报层级断链 → **全部回滚**：`git checkout -- style-vault/references/ frontend/src/preview/`；释放锁；打印差错指引；plan.md 保留可重跑 |
| 文件夹式条目只删了 README.md 漏了其它子文件 | 手动 `rm -rf` 整目录；若已 commit → 补一个 commit 删剩余文件 |
| cascade 时 YAML 解析失败（引用者 frontmatter 语法有问题） | 停，报路径让用户先修 YAML，不自动继续 |
| sync 成功但用户事后发现误删 | 用 git：`cd ~/.agents/skills/src/mirror && git reset --soft HEAD~1`；网站仓同样操作。commit 未 push 所以可逆。 |
| 并发锁冲突 | 拒启，对标 [shared-workflow 步骤 5.c](shared-workflow.md#5c-并发锁) |
| VAULT_OK=false | 只操作 skill 仓；report 注明"未联动网站"；skill 侧轻量自检代替 sync |
| 用户输入的 id 不存在 | 步骤 1 / 2 就拦住，让用户确认 |
| usedBy 字段缺失（taxonomy.py 版本旧） | Fallback：遍历所有条目的 refs / uses 做一次全扫；若找不到全扫能力 → 提示用户升级 taxonomy.py |

---

## 约束复盘（delete 专属）

1. **反向引用检查必做**：任何删除前都查一遍 usedBy。
2. **cascade 是显式选项，不默认**：有引用者时必须等用户明说 "cascade"。
3. **cascade 只改引用者 frontmatter，不删引用者本身**：这是强语义区分，避免连锁删除。
4. **文件夹式条目 rm -rf 整目录**：防孤儿子文件。
5. **批量 > 3 / cascade > 5 二次确认**：防手滑。
6. **首次 cascade 额外提示**：显式告知"改别的条目 frontmatter"的副作用。
7. **sync 失败整体回滚**：单次 delete 的"部分成功"状态没有保留价值。
8. **plan.md / report.md 模式字段必须是 "delete"**：方便 Phase 4 的 `taxonomy.py history` 子命令筛选。

---

## 入口索引

- 主干：[shared-workflow](shared-workflow.md)
- 兄弟分支：[modify-workflow](modify-workflow.md)
- 上级：[../SKILL.md](../SKILL.md)
