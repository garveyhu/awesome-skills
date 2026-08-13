# 共享主流程 · shared-workflow

所有 create 分支（from-project / from-web / from-scratch / from-other）以及 modify / delete 在进入具体 discovery / 差异逻辑后，都**汇入这里**完成剩余步骤。本文档是 skill 的主干。

---

## 前置语境

执行前须知：

- **skill 仓真实 git 根**：`~/.agents/skills/src/mirror/`（也就是 `~/.agents/skills/src/mirror/`）
- **网站仓路径**：读 `~/.agents/path.json` 的 `"style-vault"` 字段（见步骤 5 的判定逻辑）
- **分类字典真相源**：`~/.agents/skills/src/mirror/style-vault/assets/taxonomy.json`
- **查询工具**：`~/.agents/skills/src/mirror/style-vault/scripts/taxonomy.py`（用 `python3` 调，依赖 PyYAML）
- **沉淀历史归档**：`~/.agents/skills/src/mirror/style-vault-sediment/assets/sediment-history/<author>/<date-topic>/`

---

## 步骤 1 · 加载分类字典

**目的**：拿到当前所有合法的 category / tag / platform / theme 值。保证后续写入的条目不引入不存在的 slug。

**操作**：

```bash
python3 ~/.agents/skills/src/mirror/style-vault/scripts/taxonomy.py overview --json
```

输出是 JSON，结构大致：

```json
{
  "total_items": N,
  "types": { "product": {...}, "style": {...}, "block": {...}, ... },
  "categories": { "productivity": {...}, "content": {...}, ... },
  "tag_groups": {
    "aesthetic": ["minimal", "organic", "industrial", ...],
    "mood": ["calm", "playful", "serious", ...],
    "stack": ["react-tailwind", "react-antd-tailwind", "html-tailwind", "shadcn-radix", ...]
  },
  "platforms": ["web", "mobile", ...],
  "themes": ["light", "dark", ...]
}
```

**把这个 JSON 的合法值清单记在当前对话的工作集里**——后面步骤 3 生成方案、步骤 4 用户 review 时要反复用它校验。

**如果 taxonomy.py 报错**：说明依赖缺失（`style-vault` skill 未安装 / `python3` 不在 PATH / PyYAML 未安装）。停止、让用户修环境，不往下走。

---

## 步骤 2 · 授权 auto-fill

**目的**：一次性拿到用户对"元信息由 AI 自动填"的授权。避免后续每条都问一次。

**Prompt 模板**（直接贴给用户）：

```
本次沉淀预计 <N> 条条目。元信息（category / tags / platforms / theme / name / description）
由 AI 根据上下文自动填入，还是由你来填？

  Y) 全部由 AI 自动填（推荐，后面整批 review 时还能单条改）
  N) 全部留空占位，我在步骤 3 逐条手填
  M) 逐条决定（每条问一次）

请回复 Y / N / M。
```

**分支**：

- **Y** → 步骤 3 中 AI 填所有字段，用户在步骤 4 review 时增删改
- **N** → 步骤 3 中所有字段留 `<TODO>` 占位，用户逐字段填
- **M** → 步骤 3 中每条开始前单独问一次

**默认**：用户没回复或给了含糊回答（如"可以""好的"）→ 按 **Y** 处理，但在步骤 3 开始时明说"我按 Y 模式自动填，可在步骤 4 整批 review 时修改"。

---

## 步骤 3 · 生成完整写入方案

**目的**：把各 create 分支（或 modify / delete）产出的"沉淀计划"扩展成**完整的写入方案**——每条条目要有完整的 frontmatter + 正文骨架，不是只有 id 列表。

### 3.a · namespace 归属判定（必做 · 写 frontmatter 之前）

**所有** tokens / components / blocks / pages 类条目必须先确定 namespace（路径中间段）。规则见 [style-vault/references/README.md · Namespace 子目录](../../style-vault/references/README.md#namespace-子目录强制)。

判定流程：
1. 这条条目最终会被某个 `products/<slug>` 的 refs 引用吗？
   - **是** → namespace = 那个 product 的短名（`acme` / `skillhub` / ...）
   - **否（确定通用，跨 style 都成立）** → namespace = `_shared`
2. 同一条被 ≥ 2 个 product 引用时，归"视觉真正绑定"的那个，错引用方走 unlink
3. 拿不准时**优先归 product namespace**（用户原话："只要被产品关联都优先和产品绑定"）

> id 形态：`<layer>/<bucket>/<namespace>/<slug>`（`styles/` 与 `products/` 层不带 namespace）

### 3.b · 重名 grep（必做 · 写 frontmatter 之前）

**惨痛教训**（2026-04-27 acme rebuild）：差点新增 `cyan-cta` 时没发现 `dark-primary-cta` 已存在，新增 `status-pulse` 没发现 `pulse-dot` 已存在——同 bucket 跨 namespace 的近义条目幸亏 review 时撞上才发现。

**硬规矩**：每条新增条目在生成 frontmatter 前必须 grep 同 bucket 下的所有近义 slug。

```bash
# 例：要新增 components/buttons/acme/cyan-cta，先扫所有 buttons/
ls ~/.agents/skills/src/mirror/style-vault/references/components/buttons/*/

# 或用 taxonomy.py 列同类：
python3 ~/.agents/skills/src/mirror/style-vault/scripts/taxonomy.py search --type component --json \
  | grep -E '"id":\s*"components/buttons/'
```

发现近义条目（如 `dark-primary-cta` vs `cyan-cta` 都是 primary CTA）→ 在新条目 README 必须加 "**与 X 区分**" 章节，明确两者在风格世界 / 视觉语言上的差异。否则 AI 消费时容易选错。

### 3.c · tags 是受控枚举，不是描述字段（必做）

**惨痛教训**（2026-06-13 · chameleon Tier3 扇出写入）：把 74 条交给并行写入子智能体后，它们普遍把 `tags.aesthetic` / `tags.mood` 当成自由描述字段，填进"右侧滑入"/"AND/OR胶囊"/"neon"/"retro-future"/"工程克制" 等视觉词组（328 处越界），而非 `taxonomy.json` tag_groups 的受控值 → `yarn sync` 的 validateTags 全是 error，且污染前端按 tag 筛选。根因是扇出写入指引没把"tags 是闭集枚举"讲死——agent 手里没有字典就自由发挥。

#### 硬规矩

1. **`tags.aesthetic` / `tags.mood` / `tags.stack` 一律只能取 `taxonomy.json` tag_groups 里已存在的值**，绝不允许填视觉描述词组 / 中文形容词 / 自造英文 slug。
2. **委派写入给子智能体时，必须把这三组的合法值清单原样写进每个 agent 的 prompt**（不能只说"用 taxonomy 的值"，agent 没字典就会乱填）。
3. **想表达"右侧滑入 / 霓虹 / 工程克制"这类视觉特征 → 写进正文 `## 视觉特征`，不是塞进 tags**。tags 只回答"哪种美学流派 / 哪种气质 / 哪个技术栈"。
4. **不在字典里的新美学/气质值 → 先改 `taxonomy.json` 再用**，绝不在条目里直接造。
5. **整批写完、sync 之前，必须跑一次"对照 taxonomy 全量校验 tags"**（PyYAML 解析每条 frontmatter + 比对 tag_groups），把越界的批量归一回合法值。

#### 自检问题（生成 / 委派写 frontmatter 前自问）

- [ ] 我给写入子智能体的 prompt 里，有没有**原样列出** aesthetic/mood/stack 的合法值？
- [ ] 任一 tag 值是"短语 / 形容词 / 带空格的描述"吗？是 → 必越界，挪进 `## 视觉特征`
- [ ] 写完整批、sync 之前，有没有跑一次对照 taxonomy 的 tags 全量校验？

答不上 → 别 sync，先归一 tags。

### 依赖拓扑序

写入顺序**严格按底层到上层**：

```
tokens → components → blocks → pages → styles → products
```

原因：上层 refs 下层；写上层之前下层必须已存在（否则 `yarn sync` 的层级断链校验会挂）。

### 每条条目的最小完整形态

**对文件形条目**（大多数条目）：

```markdown
---
id: blocks/display/mint-analytics/mint-table
type: block
tags:
  aesthetic: [minimal]
  mood: [calm]
  stack: [react-tailwind]
platforms: [web]
theme: light
name: 薄荷表格
description: 低饱和配色的紧凑数据表格
uses:
  - tokens/palettes/mint-analytics/cold-mint
preview: /preview/blocks/display/mint-analytics/mint-table
---

# 薄荷表格

## 视觉特征
<一句话说明视觉锚点>

## Tokens
<如果是 token 层：`## Tokens` 必写；其它层可选，标出用到的外部 token>

## 核心代码
```tsx
<核心 JSX / 组件签名>
```

## 适配指南
<怎么嵌到其它 style / product 里>

## 反模式
<什么情况下不适用>
```

**对文件夹形条目**（product / style / 复杂 block 可能用）：
`references/<id>/README.md` + 其它子文件。同样的 frontmatter + 正文约定。

### 产物

把 N 条条目整理成一个 "**写入方案**" 结构，保留：
- id
- 完整 frontmatter（已用步骤 1 的合法值校验）
- 正文骨架
- 来源溯源（from-project 的源文件路径 / from-web 的 URL / from-scratch 的对话摘录）
- 依赖关系（refs 指向）

**校验**：
- 所有 `category` 必须在步骤 1 的 categories 清单里
- 所有 `tags.aesthetic` / `mood` / `stack` 必须在 tag_groups 里
- 所有 `platforms` / `theme` 必须在对应清单里
- 出现不在字典里的值 → 不要偷偷 auto-fill！打断让用户决策：("此 `<slug>` 不在 taxonomy.json，要先改字典还是换已有 slug？"）

---

## 步骤 4 · 整批 review

**目的**：让用户在一个视图里确认 / 修改整批条目，而不是每条问一次。**用户确认后立即落盘 `plan.md`**。

### 预览格式

把写入方案渲染成这样的预览（直接贴给用户）：

```
=== 写入预览 (N 条，按依赖拓扑序) ===

[1] tokens/palettes/mint-analytics/cold-mint              ← namespace: mint-analytics
    type: token
    tags: {aesthetic: [organic], mood: [calm], stack: [react-tailwind]}
    platforms: [web]    theme: light
    name: 冷薄荷调色板
    description: 低饱和薄荷绿 + 冷灰中性
    preview: /preview/tokens/palettes/mint-analytics/cold-mint
    --- 正文 50 字预览 ---
    ## Tokens: --mint-50 #F0FDF4 / --mint-200 #A7F3D0 / --mint-500 #10B981 / --slate-60...

[2] blocks/display/mint-analytics/mint-table              ← namespace: mint-analytics
    type: block
    tags: {aesthetic: [minimal], mood: [calm], stack: [react-tailwind]}
    platforms: [web]    theme: light
    uses: [tokens/palettes/mint-analytics/cold-mint]
    name: 薄荷表格
    description: 低饱和配色的紧凑数据表格
    preview: /preview/blocks/display/mint-analytics/mint-table
    --- 正文 50 字预览 ---
    ## 视觉特征：密度中等，行高 44px，zebra 用 mint-50…

...

=== 元信息来源 ===
AI 自动填：[1] [2] [3]
用户手填：（无）
```

### 用户操作词典

给用户这些操作动词：

| 操作 | 示例 |
|---|---|
| 整批确认 | "确认"、"都可以"、"go" |
| 整批 reject | "放弃"、"reject"、"全部作废" |
| 单条删 | "删 3"、"去掉 mint-table" |
| 单条改 slug | "把 1 的 slug 改成 cool-mint" |
| 单条改 tag | "把 2 的 aesthetic 加 organic" |
| 单条改正文 | "重写 3 的 `## 视觉特征`" |
| 新增条目 | "补一个 components/buttons/mint-btn" |

每次用户改动后**重渲染**整个预览，再次等待用户操作，直到 "确认" 或 "reject"。

### 落盘 plan.md

**用户一旦 "确认"**，立即落盘 `plan.md`（在执行写入之前就落盘，保证"尝试过"的记录）：

路径：
```
~/.agents/skills/src/mirror/style-vault-sediment/assets/sediment-history/<author>/<date>-<topic>/plan.md
```

`<author>` / `<date>` / `<topic>` 的生成见步骤 5 前的"作者 slug 初始化"子步骤 + 下面的"主题 slug 生成"。

`plan.md` 内容：

```markdown
# 沉淀计划 · <主题>

日期：2026-04-24
作者：links
模式：create | modify | delete
起点：from-web (https://dribbble.com/shots/xxx)
档位：Tier 2 · 基础级（目标 12–18 条）

## 目标
<一句话说明>

## 涉及条目（依赖拓扑序）
1. tokens/palettes/mint-analytics/cold-mint
2. blocks/display/mint-analytics/mint-table
3. styles/saas-tool/cold-mint-saas
4. products/mint-analytics

## 依赖关系
mint-analytics → cold-mint-saas → [mint-analytics/mint-table, mint-analytics/cold-mint]
mint-analytics/mint-table → mint-analytics/cold-mint

## 元信息填写方式
- AI 自动填: tokens/palettes/mint-analytics/cold-mint, blocks/display/mint-analytics/mint-table
- 用户手填: styles/saas-tool/cold-mint-saas

## Tier 3 覆盖率（仅 Tier 3 填）
- 路由 N/N
- 全局模式 K/K
- 表单 F/F
- 状态 S/S

## 执行状态
☑ 用户已确认 · 待写入
```

### 主题 slug 生成

- AI 从写入方案的"目标"里抽一个 kebab-case slug（如 `mint-analytics` / `acme-cold-saas`）
- 用户可在步骤 4 review 时手工改（说一句 "主题叫 xxx"）
- 同日同主题已存在 folder → 自动加后缀 `-02` / `-03`
- 模式后缀：modify 时 folder 名加 `-modify`；delete 时加 `-delete`

### 错误路径

**整批 reject** → 放弃所有改动，**不写任何文件**、不 commit、**`plan.md` 不落盘**。结束。

### Tier 3 覆盖率核对（仅 Tier 3 · 在"贴写入预览"之前必跑）

如果档位是 Tier 3，步骤 4 一开始必须先贴覆盖率核对表：

```
=== Tier 3 覆盖率核对 ===
路由       N/N → XX%
全局模式   K/K → XX%
表单       F/F → XX%
状态       S/S → XX%

门槛：全部 ≥ 80%
```

- **全部 ≥ 80%** → 进入整批 review 正常流程
- **任一 < 80%** → 打断用户，选项：
  1. 补齐缺口（回到 sediment-from-project.md 的 step 0.5 / 2.5 / 3.5 补扫 / 补条目）
  2. 降到 Tier 2（移除超出 Tier 2 范围的条目，以 Tier 2 流程继续）
  3. 手动放行（在沉淀报告里显式标注"Tier 3 覆盖率 XX% 未达标，用户手动放行"）

用户未明确选项时不要默认放行——缺口不补的默认值是"降到 Tier 2"。

### 档位区间校验（所有档位 · review 之前必做）

同时要校验**条目数**是否落在档位目标区间：

| 档位 | 目标区间 | 越界动作 |
|---|---|---|
| Tier 1 | 5–8（超 10 要砍） | > 10 → 列出"可砍候选"让用户选删哪些 |
| Tier 2 | 12–18（超 22 要砍） | > 22 → 同上 |
| Tier 3 | 30–50+（无上限，下限 ≥ 30） | < 30 → 问补齐或降档 |

---

## 步骤 5 · path.json 分叉

**目的**：判定是 skill-only 沉淀还是双仓同步。加并发锁防同时写。

### 5.a 作者 slug 初始化（子步骤）

**若已有 `.author-config.json`**：读 `author` 字段，直接用。

**若无**：

```bash
CONFIG=~/.agents/skills/src/mirror/style-vault-sediment/assets/sediment-history/.author-config.json
if [[ ! -f "$CONFIG" ]]; then
  # 推断 slug
  NAME=$(git config user.name 2>/dev/null || true)
  if [[ -n "$NAME" ]]; then
    # 小写 + 空格转 dash + 去非字母数字
    SLUG=$(echo "$NAME" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+|-+$//g')
    SOURCE="git-config"
  else
    SLUG=""
    SOURCE="manual-input"
  fi
fi
```

- 若推出了 slug → 贴给用户确认：`"检测到 git config user.name = <原名>，建议作者 slug 为 <slug>，确认？(Y / 改成 xxx)"`
- 若 `git config user.name` 为空 → `"git config user.name 为空，请手工输入你想用的作者 slug（建议小写 kebab，如 links / jiawei-hu）"`

用户确认后写入 `.author-config.json`：

```json
{
  "author": "links",
  "configured_at": "2026-04-24T12:00:00Z",
  "source": "git-config"
}
```

**注意**：`.author-config.json` 已在 `.gitignore`，不入 git。只 commit `.author-config.example.json` 模板。

### 5.b VAULT_OK 判定

完整 bash 脚本（沿用旧 `style-vault` skill 的判定逻辑）：

```bash
VAULT=$(jq -r '."style-vault" // empty' ~/.agents/path.json 2>/dev/null)
if [[ -z "$VAULT" || ! -d "$VAULT/frontend" ]]; then
  VAULT_OK=false
elif ! jq -e '.["style-vault-site"] == true' "$VAULT/frontend/package.json" >/dev/null 2>&1; then
  VAULT_OK=false
else
  VAULT_OK=true
fi
```

**说明**：
- `~/.agents/path.json` 存着用户本机各 project 的绝对路径
- `"style-vault"` 字段是 style-vault 网站仓根
- 再校验 `frontend/package.json` 里有 `"style-vault-site": true` marker，防串仓

**分支**：
- `VAULT_OK=false` → **skill-only 沉淀**。跳过所有网站仓操作。在步骤 8 沉淀报告里标注 "未联动网站"。
- `VAULT_OK=true` → **双仓同步**。下一步起网站仓。

### 5.c 并发锁

**仅当 `VAULT_OK=true`**：

```bash
LOCK="$VAULT/.style-vault-lock"
if [[ -f "$LOCK" ]]; then
  # 锁冲突
  OTHER=$(cat "$LOCK")
  echo "另一个会话正在沉淀 $OTHER，请等它完成，或手工 rm $LOCK"
  exit 1
fi
# 上锁（把本次主题写进锁文件便于诊断）
echo "<topic>" > "$LOCK"
```

**释放时机**：步骤 8 结束（或任何异常分支出口）一定要 `rm "$LOCK"`。

---

## 步骤 6 · 逐条写入

**目的**：按拓扑序写每条条目到 skill 仓 + （可选）网站仓，每条写完跑 `yarn sync` 做增量校验。

### 写入位置

**id 必须含 namespace 段**（tokens / components / blocks / pages 这 4 层）：`<layer>/<bucket>/<namespace>/<slug>`。`<namespace>` 优先 = 关联 product 的短名（如 `acme` / `skillhub`）；无产品关联用 `_shared`。详见 [style-vault/references/README.md · Namespace 子目录](../../style-vault/references/README.md#namespace-子目录强制)。

**skill 仓**（根 `~/.agents/skills/src/mirror/`）：

- 文件形：`style-vault/references/<id>.md`
  - 例：`style-vault/references/tokens/palettes/acme/slate-cyan-ice.md`
  - 例：`style-vault/references/components/buttons/_shared/ghost-button.md`
- 文件夹形（product / style / pages）：`style-vault/references/<id>/README.md`
  - 例：`style-vault/references/pages/auth/acme/auth-cold-split/README.md`
  - 例：`style-vault/references/products/acme-cold-saas/README.md`（product 不带 namespace）

**网站仓**（根 `$VAULT`，仅 `VAULT_OK=true` 时）：

- preview tsx：`$VAULT/frontend/src/preview/<id>.tsx`
  - 例：`$VAULT/frontend/src/preview/tokens/palettes/acme/slate-cyan-ice.tsx`

### 单条写入子步骤

对第 k 条（按拓扑序）：

1. **写 skill 仓文件**（mkdir -p 父目录 + Write 文件）
2. **若 VAULT_OK=true**：写网站仓 preview tsx（同样 mkdir -p）
3. **若 VAULT_OK=true**：跑增量 sync
   ```bash
   cd "$VAULT/frontend" && yarn sync
   ```
   - sync 校验：frontmatter 字段合法性、层级引用完整性、preview 路径正确性
   - **一条失败就停**：跳到"错误处理"节

**若 VAULT_OK=false**：只写 skill 仓。没有 `yarn sync` 可跑，但 skill 侧仍可做轻量自检（frontmatter yaml 合法性、refs 指向的条目在 skill 仓已存在）。

### 错误处理（步骤 6 中途失败）

**触发条件**：
- 某条 `yarn sync` 报错
- 用户 Ctrl-C
- skill 侧轻量自检挂

**动作**：

```bash
# 停止后续写入
# skill 仓：保留前 k-1 条 + 当前失败的第 k 条（用户可以肉眼 debug）
#   但不 git add 任何东西——没有 commit

# 网站仓：清理第 k 条可能已建的 tsx
if [[ "$VAULT_OK" == "true" ]]; then
  cd "$VAULT/frontend"
  git checkout -- src/preview/<id>.tsx 2>/dev/null || rm -f src/preview/<id>.tsx
  # 前 k-1 条也 git checkout，因为没有 commit，还没 add
  git checkout -- src/preview/
fi

# 释放并发锁
rm -f "$VAULT/.style-vault-lock"
```

**用户提示**：

```
第 k 条 <id> 写入失败：<错误详情>
已清理网站侧临时文件。skill 侧前 k-1 条保留供 debug，未 commit。
plan.md 已落盘在 <path>，可在修复后重跑。
```

**plan.md 保留**（步骤 4 已落盘）。不清理。

### sync 失败属于他批 / 并发会话时（不要误伤本批 · 必做）

**惨痛教训**（2026-06-13 · quiver 沉淀撞上活跃 chameleon 会话）：全量 `yarn sync` 因**另一批/并发会话**写入的半成品条目（未入字典的 tag / `@` 开头未引号的 YAML）而失败，本批 16 条本身全合法——但默认「sync 失败就停 + 清理」会误把合法的本批也中止/回滚。`yarn sync` 是**全树**校验，失败不等于本批失败。

#### 硬规矩

1. **sync 失败必须先看报错条目的 id 前缀（namespace），判定失败属于本批还是他批**：
   - 失败**全在本批 namespace** → 按上面「步骤 6 中途失败」原流程（停 + 清网站侧 + 不 commit）。
   - 失败**全在他批 / 别的 namespace**（并发或遗留会话的半成品）→ **不允许**当成本批失败而中止或回滚已写好的本批条目。
2. 他批污染时**一律**改走 **scoped 校验 + 精确提交 + 延后 registry**：
   - 对本批逐条复刻 sync 的校验（tags 全在 taxonomy / theme·platform·category 合法 / 非 token 的 preview 文件齐全 / uses·refs 目标均存在），全过才提交。
   - **不允许**重新生成 / 提交 `registry.json`——避免把他批的半成品/错误状态固化进 registry。报告里注明「registry 待下次干净 sync 自动登记」。
3. **不允许为了让全量 sync 变绿去改 / 删他批或并发会话的文件**。如需临时移出做隔离 sync，**必须**用 `rsync --ignore-existing` 无损还原；一旦发现对方会话仍在实时写入（被移走的目录又冒出新文件），**立即停手并还原**，不再干扰。

#### 自检问题（sync 失败时自问）

- [ ] 报错条目的 id 前缀属于本批 namespace，还是别的 namespace（他批/并发）？
- [ ] 本批每一条都过了 scoped 校验（tags / theme / platform / category / preview / uses / refs）吗？
- [ ] 我有没有为了绿 sync 去改、删、移别的会话的文件？移走的有没有无损还原？
- [ ] 我是不是重新生成并提交了 registry.json、把他批的错误状态固化了？

失败全属他批 + 本批 scoped 全过 → 精确提交本批、延后 registry，不中止。

---

## 步骤 7 · 网站仓 commit（skill 仓延后到步骤 8）

**仅当 步骤 6 全绿**。

本步骤**只处理网站仓的 commit**。skill 仓的 commit 延后到步骤 8 末尾做——等 `report.md` / `source.md` 落盘后一次聚合，避免 amend，单 commit 拿到所有新增内容。

### 网站仓 commit message 模板

**create 模式**：

```
feat(preview): add <主题> preview (N 条)

<正文：简述 preview 组件的结构>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**modify 模式**：`refactor(preview): update <id> preview`

**delete 模式**：`feat(preview): remove <id> preview`

### 执行（仅 VAULT_OK=true）

```bash
cd "$VAULT"
git add frontend/src/preview/<涉及的 tsx>
git commit -m "$(cat <<'EOF'
feat(preview): add <主题> preview (...)

<正文>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

**VAULT_OK=false** 时跳过本步骤，直接进步骤 8。

**不 push**。保留给用户。

### 精确 add 硬规矩（必做 · skill + vault 两仓都遵守）

**惨痛教训**（2026-04-27 acme rebuild · namespace 迁移）：`git add -A` 把 skill 仓里别的 skill 残留的循环 symlink `wiki-creator/wiki-creator` 拉进了 commit，事后单独打 chore commit 修。

**硬规矩**：

1. **绝不允许** skill 仓用 `git add -A` / `git add .`——skill 仓多 skill 共存（style-vault / style-vault-sediment / 其它），别人的状态会被误带入
2. **必须按路径精确 add**：
   ```bash
   # skill 仓
   cd ~/.agents/skills/src/mirror
   git add style-vault/references/<本次改动子路径>
   git add style-vault-sediment/assets/sediment-history/<本次 batch>

   # 网站仓（推荐同样精确 add）
   cd "$VAULT"
   git add frontend/src/preview/ frontend/src/data/registry.json
   ```
3. **commit 前 `git status --short` 自检**——确认 staging 里**所有**条目都属本次沉淀，遇陌生路径立刻 `git restore --staged <path>` 移除

### skill 仓 commit message 模板（步骤 8 使用）

下面是步骤 8 末尾要用的模板，提前放这里方便对照：

**create 模式**：

```
feat(style-vault): add <主题> (N 条: X tokens + Y blocks + Z styles + ...)

<正文：简述新增条目的作用、起点、依赖关系>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**modify 模式**：`refactor(style-vault): modify <id>`

**delete 模式**：`feat(style-vault): remove <id>`

---

## 步骤 8 · 沉淀报告

**目的**：给用户打印"做了什么 / 怎么分类的 / 下一步"总结；同时落盘到 `sediment-history/` 作为审计。

### 报告模板

```markdown
# 沉淀报告 · <主题>

日期：2026-04-24
模式：create | modify | delete
起点：from-web (https://dribbble.com/shots/xxx)
档位：Tier 2 · 基础级（目标 12–18 · 实际 N 条）
作者：links

## 涉及条目（N 条）

| 操作 | 类型 | ID | 名称 | 分类 / 标签 |
|---|---|---|---|---|
| 新增 | token | tokens/palettes/mint-analytics/cold-mint | 冷薄荷调色板 | aesthetic: [organic] · mood: [calm] |
| 新增 | block | blocks/display/mint-analytics/mint-table | 薄荷表格 | aesthetic: [minimal] · mood: [calm] · stack: [react-tailwind] |
| 新增 | style | styles/saas-tool/cold-mint-saas | 冷薄荷 SaaS | aesthetic: [minimal, organic] · mood: [calm] |
| 新增 | product | products/mint-analytics | Mint 分析后台 | category: productivity |

## 元信息来源

- AI 自动填（授权）：`tokens/palettes/mint-analytics/cold-mint`、`blocks/display/mint-analytics/mint-table`
- 用户手改：`styles/saas-tool/cold-mint-saas` 的 tags.aesthetic
- 纯手填：无

## Tier 3 覆盖率（仅 Tier 3 填）

| 维度 | 目标 | 实际 | 覆盖率 |
|---|---|---|---|
| 路由 | 11 | 10 | 91% ✅ |
| 全局模式 | 5 | 5 | 100% ✅ |
| 表单 | 4 | 4 | 100% ✅ |
| 状态 | 4 | 3 | 75% ⚠️（用户手动放行）|

## 分类决策说明

- `tokens/palettes/cold-mint` → 主色 #A7F3D0 + 冷灰；aesthetic=organic（色板偏有机），mood=calm（低饱和）
- `products/mint-analytics` → category=productivity（分析 dashboard）

## Commit

- skill 仓：`a3f9c21` · `feat(style-vault): add mint analytics suite (1 product + 1 style + 1 block + 1 token)`
- 网站仓：`b5d12fc` · `feat(preview): add mint analytics preview (4 条)`
- **均未 push**

## 下一步

1. `cd $VAULT/frontend && yarn dev` 肉眼过 preview
2. OK 后 `git push` 两仓
3. 发现问题 `git reset --soft HEAD~1` 回到工作区

---
*由 style-vault-sediment skill 生成 · 来源：from-web*
```

### 落盘路径

```
~/.agents/skills/src/mirror/style-vault-sediment/assets/sediment-history/<author>/<date>-<topic>/report.md
```

同时落盘（若来源是 from-web / from-project）：

```
.../sediment-history/<author>/<date>-<topic>/source.md
```

`source.md` 内容：

```markdown
# 素材溯源 · <主题>

## URL
- 参考站点：https://dribbble.com/shots/xxx（访问时间：2026-04-24 13:20）

## 截图
- 本地路径（临时）：/tmp/dribbble-mint-xxx.png
- 关键截图要点：主视觉色 #A7F3D0，typography 用 Inter + IBM Plex Mono

## 对话摘录
<AI 精炼提取的关键对话片段>
```

### skill 仓聚合 commit（步骤 7 延后的）

把 `references/` 下所有新增/修改/删除的条目 + `sediment-history/` 下的 plan.md / report.md / source.md 作为**同一个 commit** 提交：

```bash
cd ~/.agents/skills/src/mirror
git add style-vault/references/<涉及的 MD>
git add style-vault-sediment/assets/sediment-history/<author>/<date-topic>/
git commit -m "$(cat <<'EOF'
feat(style-vault): add <主题> (N 条: X tokens + Y blocks + Z styles + ...)

<正文：起点、依赖关系、元信息填写方式的简述>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

**不 push**。保留给用户。

**modify 模式** commit subject：`refactor(style-vault): modify <id>`
**delete 模式** commit subject：`feat(style-vault): remove <id>`

### 释放并发锁

```bash
rm -f "$VAULT/.style-vault-lock"
```

### 打印给用户

把报告完整内容直接打印到对话——不只给一句"已写入"。

---

## 步骤 9 · 教训回写（条件触发）

**目的**：让 skill 自己修自己。每次沉淀出错时，把**错误模式**（不是具体错误）抽象成硬规矩，回写到对应 workflow 文件，让后续所有沉淀自动遵守。详见 [lessons-loopback.md](lessons-loopback.md)。

### 触发条件（任一）

- 用户在 review 阶段拒绝，并给出**结构性**原因（不是"名字改一下"这种微调）
- 用户在写入后指出"差异大 / 风格不对 / 漏了 xxx / 跟真实站差太多"
- 用户要求重写整条条目
- AI 自己在通读源码或看用户截图后，发现之前抽象错了

**不触发**：用户做细节微调（改名、改圆角值、改色号等）→ 属于"一次小错"，改条目即可。

### 动作（3 步）

1. **诊断性质**：问自己"这是一次小错，还是 workflow 缺口？"
   - 一次小错 → **不回写**，直接修复条目
   - 模式错 → 继续第 2 步
2. **回写流程**：严格遵循 `lessons-loopback.md` 的 3 步（抽象问题 → 定位所属 workflow 文件 → 写硬规矩 + 自检问题）
3. **清单登记**：在 `lessons-loopback.md` 的"已回写教训清单"append 一行：日期 / 错误模式 / 回写位置 / 相关 sediment 目录

### Commit

教训回写和修复条目可以**同一个 commit**，message 前缀用：

```
docs(skill): 沉淀教训 · <简短模式描述>

<详细：抽象模式 + 回写到哪里 + 附带修的条目>
```

独立教训回写（不伴随条目修复）：`docs(skill): 沉淀教训 · xxx`。

### 反污染提醒

- 不是每次小错都写教训——**会污染 skill**
- 同一 workflow 里**不允许重复添加同义规则**——回写前 grep 搜一下已有规则
- 规则必须**"必须 / 不允许"强制语气** + 具体可操作动作——温馨提示会被 AI 忽略

---

## 错误处理矩阵

集中定义所有异常的处理动作：

| 场景 | 动作 |
|---|---|
| **步骤 4 用户整批 reject** | 放弃所有改动，不写任何文件，不 commit，**plan.md 不落盘**。正常结束对话。 |
| **步骤 6 某条 `yarn sync` 失败（报错属本批 namespace）** | 停止后续；skill 仓已写的前 k-1 条**保留**（未 commit）；网站仓 `git checkout -- src/preview/` 清理；释放锁；打印错误 + 修复指引；`plan.md` 已落盘保留 |
| **步骤 6 全量 sync 失败但报错全在他批/并发会话的 namespace** | 不当成本批失败：对本批做 scoped 校验（tags/theme/platform/category/preview/uses·refs），全过则**精确提交本批**、**不重生成 registry.json**（报告注明待下次干净 sync），**不改/删/固化他批文件**。详见步骤 6「sync 失败属于他批/并发会话时」节 |
| **用户 Ctrl-C / 打断** | 同 sync 失败：清网站侧，保 skill 侧未 commit 文件，释放锁 |
| **步骤 5 并发锁冲突** | 直接拒启，打印"另一个会话正在沉淀 `<other-topic>`"。**不做任何写入**，不释放锁（锁属于其它会话）。 |
| **步骤 1 taxonomy.py 报错** | 停止，提示用户修环境（`style-vault` skill 是否安装、`python3` 是否在 PATH、PyYAML 是否已安装） |
| **步骤 3 AI 填了字典里没有的 tag** | 打断用户："`<tag>` 不在 taxonomy.json，请先改字典或换已有 slug" |
| **步骤 5.a git config user.name 为空** | 让用户手工输入 author slug 到 prompt，存入 `.author-config.json` |
| **步骤 6 VAULT_OK=false 时依然有用户给的网站相关指令** | 忽略并在沉淀报告注明"未联动网站（VAULT_OK=false）" |
| **Tier 3 覆盖率核对不达标** | 打断三选：补齐缺口 / 降到 Tier 2 / 手动放行。默认值"降到 Tier 2"。放行需在 report.md 显式标注。|
| **档位区间越界（条目数超上限 / 低于下限）** | review 前打断：超上限列"可砍候选"，低于下限问补齐或降档 |

---

## 约束复盘

本流程的硬约束，实现和遵循时务必保证：

1. **拓扑序**：token → component → block → page → style → product。不允许乱序写入。
2. **整批 review 前不落盘**：步骤 4 用户说"确认"才落盘 plan.md；reject 不落盘。
3. **sync 失败不 commit**：步骤 6 任何一条失败，前 k-1 条不 add、不 commit。
4. **双仓 commit 独立**：skill 仓和网站仓各自一个 commit，message 不同，不用 monorepo 思维。
5. **永远不 push**：push 由用户手动。
6. **锁释放必达**：不管成功失败，步骤 5 上的锁在步骤 8 或异常出口一定要释放。
7. **作者 slug 只问一次**：`.author-config.json` 存在就别再问。
8. **新 tag / category 必须先改字典**：步骤 3 若 AI 想填字典里没的值，打断，不自己偷改 taxonomy.json。
9. **档位区间要卡**：步骤 4 在贴 review 前校验条目数是否在档位目标区间（Tier 1: 5–8 / Tier 2: 12–18 / Tier 3: 30–50+），越界打断。
10. **Tier 3 覆盖率门槛**：步骤 4 在贴 review 前跑覆盖率核对，任一维度 < 80% 打断询问。
11. **教训回写**：用户指出"差异大 / 风格不对"或要求重写整条时，先诊断是"一次小错"还是"模式错"；模式错必须走步骤 9 回写到对应 workflow 文件 + 登记 `lessons-loopback.md` 清单。

---

## 入口索引

- 从 create 分支汇入：[sediment-from-project](sediment-from-project.md) · [sediment-from-web](sediment-from-web.md) · [sediment-from-scratch](sediment-from-scratch.md) · [sediment-from-other](sediment-from-other.md)
- 从 modify / delete 汇入：[modify-workflow](modify-workflow.md) · [delete-workflow](delete-workflow.md)
- 上级 SKILL.md：[../SKILL.md](../SKILL.md)
