---
name: style-vault
description: >
  Personal style library with 5-tier hierarchy (vibe / archetype / composite / atom / primitive).
  Use when: building frontend UI to match personal style preferences, sinking new styles after they're approved,
  or consuming prompts from the style-vault website.
  Triggers: "/style-vault", "沉淀风格", "存一下样式", "加到 vault", "用 xxx 风格",
  "使用 style-vault skill", "参考 style-vault 里的", 组件样式、管理后台、落地页等前端生成场景。
---

# Style Vault

本 skill 是一套按五层分层组织的个人风格资产库：`vibes` / `archetypes` / `composites` / `atoms` / `primitives`。每一层的"一条资产"粒度和能被谁引用的规则，见 [references/README.md](references/README.md) 和每层下的 `_CATEGORY.md`。

skill 有**两种工作模式**：**沉淀（Maintenance）** 负责把满意的风格写入资产库，**消费（Consumption）** 负责在生成前端代码时读取资产并合成规格。AI 根据用户的 trigger 关键词先路由到正确模式，再按对应流程执行。两种模式互不混用——消费模式永远只读、沉淀模式才写入。

## 两种模式路由

| Trigger 关键词 | 进入模式 |
|---|---|
| `/style-vault`、"沉淀"、"存一下"、"加到 vault"、"记录这个风格"、"保存这套样式" | Maintenance |
| "用 xxx 风格"、Prompt 卡片含 "使用 style-vault skill"、"参考 style-vault 里的 xxx"、"按 vault 里的 xx 生成" | Consumption |
| 仅出现 "style-vault" 裸词（不带沉淀或消费意图） | 询问用户意图再分叉 |

歧义场景一律回问，不要猜。典型例子：用户只说"style-vault 里有没有表格样式？"——这既可能是消费前的探查，也可能是沉淀前的去重检查，要先问清楚再动手。

### 两模式快速对比

| 维度 | 消费（Consumption） | 沉淀（Maintenance） |
|---|---|---|
| 读写 | 只读 | 读 + 写 |
| 触达范围 | 仅 skill 仓 `references/` | skill 仓 + 可选的网站仓 |
| 典型产出 | 一段满足用户场景的前端代码 | 一条新资产 + 两个独立 commit |
| 需要 path.json | 否 | 是（决定是否联动网站） |
| 失败影响 | 仅当前对话 | 可能留下未 commit 改动，需回滚 |
| 用户期望 | "给我结果" | "帮我把这套沉下来" |

混用是危险的——消费模式里顺手写 skill，或者沉淀模式里顺手生成业务代码，都会让用户失去对"哪些已入库 / 哪些只在本对话里"的判断。

## 消费模式（Consumption，5 步）

1. **解析主体 ID 和叠加 ID**
   从 Prompt 卡片、用户指令或上下文里提取要用的资产 ID。主体可能是任意一层：vibe / archetype / composite / atom / primitive。叠加 ID 可以是"在主体基础上再套一个 primitive 调色板"之类的附加项。若用户只给了人类名字（如"管理后台表格"），先根据描述去 `references/<layer>/_CATEGORY.md` 反查 ID，不确定就问。
2. **Read 主条目 md**
   `~/.agents/skills/style-vault/references/<id>.md`。若 id 对应的是文件夹形式（vibe / archetype 通常是文件夹），读 `<id>/README.md`。路径错误、文件不存在时立即报错，不要猜替代项。
3. **递归 Read `frontmatter.uses` 的每个 ID**
   把依赖链上的所有资产都读进来合成完整规格。uses 里出现悬空引用（对应 md 不存在）时跳过并在最终输出里提示一次。深度通常 ≤ 3 层（vibe → composite → atom → primitive），不需要防环，但遇到同一 ID 重复出现时记得去重。
4. **合并规格**
   tokens 按"下层给值、上层覆盖"的顺序叠加（primitive 打底，vibe 最后覆盖）。按"反模式 / 禁忌"章节做负向过滤——这些是硬约束，生成代码时必须避开。冲突的 token 以上层为准，但要在最终输出里简要说明"xxx token 被 vibe 覆盖"，方便用户追踪。
5. **生成代码**
   按合并后的 tokens + "核心代码" + "样式要点"，结合用户的具体需求产出代码。不要机械复制，按上下文裁剪；用户要的是"数据表格"，就算 composite 带了完整的 filter 栏也要按需砍掉。生成完毕后用一两句话说明你引用了哪几条资产、做了哪些取舍。

**消费模式不读 `path.json`，不进网站，不写入 skill。** 只读。

### 消费模式示例

用户说："按 vault 里的 `composites/display/table` 给我做一个订单列表，主题用 dark。"

AI 按步骤执行：
1. 解析：主体 = `composites/display/table`，叠加 = `theme:dark`（从语义推断，不从 ID 取）
2. 读 `references/composites/display/table.md`
3. 发现 frontmatter.uses 里有 `primitives/palettes/admin-slate`，继续读它
4. 合并：primitive 给基础配色、composite 定义表格结构；叠加 dark 后把 primitive 里的 light 色值整体翻转
5. 生成 React + AntD + Tailwind 代码，附一句："用了 composites/display/table + primitives/palettes/admin-slate，按 dark 主题反色"

消费链路短、只读、不 commit——这是它和沉淀模式最大的边界。

## 沉淀模式（Maintenance，10 步）

1. **定位主体**
   从当前对话上下文识别用户想沉淀的风格对象。不确定归哪一层、或是主体级还是叠加级，一次只问一个问题——不要一口气抛"这是 composite 还是 atom？tag 填哪些？要不要生成 preview？"这种连环问，会把用户问烦。
2. **归类**
   读对应层的 `_CATEGORY.md`，按边界判据归档。关键两问："能不能脱离整站单独用？""是不是纯 token？"前者区分 vibe / archetype，后者区分 primitive 和其他层。不确定就列出两个候选层的对比，让用户拍板。
3. **生成 ID = 路径**
   ID 必须与相对路径完全一致，kebab-case。冲突时加语义后缀（`table-striped` / `table-compact`），不要 `-v2` 这种纯版本号命名——资产库追踪的是"形态差异"，不是"修订历史"。
4. **Tag 校验**
   读 `references/_tags.yaml`。新 tag 值必须**先改字典、再写条目**，顺序不能颠倒（否则 sync 会 reject）。四个 group 各司其职：`aesthetic` 描述视觉风格大类，`mood` 描述情绪基调，`theme` 只有 light/dark，`stack` 锚定技术栈。不要把 mood 混进 aesthetic。
5. **写 skill 条目**
   按 [references/README.md](references/README.md) 的 frontmatter schema + 正文章节顺序写：`# 条目名` → `> 一句话定位` → `## 视觉特征` → `## Tokens` → `## 核心代码` → `## 适配指南` → `## 反模式 / 禁忌` → `## 引用关系`。primitive 强制带 `## Tokens` 下的可 `JSON.parse` 的代码块。
6. **处理 uses 悬空引用**
   如果 frontmatter.uses 里引用了还不存在的 ID，列出来让用户选"一起沉 / 先放着"。悬空引用允许存在，网站 sync 会给 warning，不是 error。用户选"一起沉"时退回第 1 步针对每一条悬空 ID 重跑流程，不要在一个对话里同时写多条却不走完整流程。
7. **path.json 分叉**
   判定是否有可用的网站仓：
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
   `VAULT_OK=false` → 直接跳到第 9 步（skill-only 沉淀）；`VAULT_OK=true` → 进第 8 步（双仓同步）。三重校验分别覆盖：字段缺失、路径失效、目录存在但不是 style-vault 网站。

   若 `VAULT_OK=true`，进入第 8 步前先检查/创建并发锁：
   - 若 `$VAULT/.style-vault-lock` 存在 → 拒绝启动，提示"另一个会话正在沉淀"
   - 否则：`touch "$VAULT/.style-vault-lock"`
8. **网站侧**
   - 按层级模板在 `$VAULT/frontend/src/preview/<id>.tsx` 创建 preview 页（模板位于 `$VAULT/frontend/src/preview/_templates/`，按层取对应模板）
   - 跑 `cd $VAULT/frontend && yarn sync`（重建 `registry.json` + 校验 frontmatter / tag / primitive tokens）
   - 校验失败就**停**，不 commit，不覆盖，把 sync 的错误原样报给用户。不要自作主张改 frontmatter 绕过校验——校验 reject 一定意味着条目本身有问题。
9. **双仓独立 commit（不 push）**
   - skill 仓：`feat(style-vault): add <id>` 或按 type 拆 `feat(<type>): add <id>`
   - 网站仓：`feat(preview): add <id>`
   - 两个 commit 独立签名，不跨仓。所有 commit 末尾加 `Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>`
   - push 永远留给用户——网站那边可能还要跑 `yarn dev` 预览调整
10. **输出行动摘要**
    ID / 路径 / 命中的 tag / 两个 commit hash；提示用户"切到 `$VAULT/frontend` 跑 `yarn dev` 查看 preview"。如果是 skill-only 分支（VAULT_OK=false），摘要里也要说明"未联动网站仓，原因：xxx"。

    最后无论成败，若第 7 步创建了锁文件，需 `rm -f "$VAULT/.style-vault-lock"` 释放。

### 沉淀模式 Checklist

每次走完流程前对照检查，少一项就不算写完：

- [ ] 用户在本对话里已明确表示"满意"或"想沉下来"，不是顺口一提
- [ ] ID 与文件路径完全一致，kebab-case，无版本号后缀
- [ ] frontmatter 五项必填齐全（`id` / `type` / `name` / `description` / `tags`）
- [ ] tag 值全部在 `_tags.yaml` 字典里；新值已先进字典
- [ ] primitive 条目的 `## Tokens` 代码块可 JSON.parse
- [ ] uses 链上的悬空 ID 已向用户列示并取得决定
- [ ] 若 `VAULT_OK=true`，preview 页已建且 `yarn sync` 绿灯
- [ ] 两仓各自独立 commit，footer 有 Co-Authored-By
- [ ] 摘要贴给用户，说明命中的 tag 与下一步查看路径

## 分层结构

详见 [references/README.md](references/README.md) 和各层 `_CATEGORY.md`。简表：

| 层 | 一条资产 = | 二级桶数 |
|---|---|---|
| vibes | 整站调性：结构+配色+字体全绑死 | 8 |
| archetypes | 页面样板：只管结构，色字可换 | 12 |
| composites | 场景块：一个完整功能块 | 10 |
| atoms | 原子件：单个交互元素 | 9 |
| primitives | 设计原语：色板/字体/间距等 | 12（typography 有三级） |

引用方向**严格自上而下**：`vibes → archetypes → composites → atoms → primitives`。primitive 不能引用上层，否则循环。同层之间也不建议互相引用——场景块需要复用时，该抽到下一层（atom 或 primitive）里共享。

判层决策树（简版）：
- 绑死配色 + 字体 + 结构且无法独立使用 → vibe
- 只管页面骨架（区块划分、留白节奏）、色字可替换 → archetype
- 一个完整功能块（表格 + 工具栏 + 分页）→ composite
- 单个交互元素 → atom
- 纯 token（颜色 / 间距 / 字体 / 阴影 / 圆角）→ primitive

## Tag 字典与 Frontmatter

- Tag 字典：[references/_tags.yaml](references/_tags.yaml)。四大分组 `aesthetic` / `mood` / `theme` / `stack`。字典是权威源，sync 会严格校验。
- Frontmatter schema：[references/README.md](references/README.md)。必填 `id` / `type` / `name` / `description` / `tags`；vibe / archetype / composite / atom 带 `preview` 路径，vibe / archetype / composite 建议填 `uses`；atom 可选；primitive 不填（最底层）。
- primitive 必填 `## Tokens` 下的可 `JSON.parse` 代码块（网站的色卡、字阶、间距 preview 从这里取值渲染）。
- composite / atom / archetype / vibe 的局部 token 也写在 `## Tokens` 节里，但不强制 JSON.parse——带注释、变量引用都可以。

### Frontmatter 最小示例

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
  - atoms/buttons/ghost-button
preview: /preview/composites/display/table
---
```

primitive 的 `## Tokens` 代码块示例（必须可 JSON.parse）：

````markdown
## Tokens

```json
{
  "palette": {
    "bg": "#FAFBFC",
    "surface": "#FFFFFF",
    "border": "#E4E7EC",
    "text-primary": "#1F2937",
    "text-secondary": "#6B7280"
  }
}
```
````

不要在 JSON 里写注释或变量引用，sync 会直接 `JSON.parse()` 失败。需要解释的色值，在 `## 视觉特征` 节里描述。

## 容错矩阵

| 情况 | 动作 |
|---|---|
| `~/.agents/path.json` 不存在 | 只更 skill；提示用户可加 `"style-vault"` 字段开启网站联动 |
| 有 path.json 但无 `style-vault` 字段 | 同上，只更 skill |
| 字段值对应目录不存在 | 只更 skill；警告字段失效，问用户是否顺手清掉 |
| 目录存在但 `frontend/package.json` 无 `"style-vault-site": true` marker | 拒写网站侧，报错并提示用户手动加 marker 或确认路径 |
| skill 写入成功 / 网站 sync 失败 | 回滚网站侧未 commit 改动（`git -C $VAULT checkout -- ...`、删未追踪 preview 文件）；skill 改动保留但**不 commit**；提示用户修复后重跑 |
| 外部用户（只 clone 了 skill，没有网站仓） | VAULT_OK=false，走 skill-only 分支，无感知 |
| 用户手改 preview 未反映回 skill | sync 产生反向 orphan warning，不自动删；提示用户回补 skill 条目 |
| 并发 `/style-vault`（两个对话同时沉淀） | 检测 `$VAULT/.style-vault-lock`，存在则拒启，等另一侧完成或用户手动清锁 |
| 消费时 uses 悬空 | 跳过该依赖，最终合并规格里给 warning，不阻断代码生成 |

容错的核心原则：**永不丢数据、永不 silent fail、永不越权**。skill 改动即便没跟上网站 sync，也保留未 commit，让用户决定修复还是丢弃；网站 sync 失败立刻回滚，不留半成品；检测到并发锁就拒启，不赌另一侧会不会打断自己。

## 维护指南（给所有 AI）

- **不自动起 dev server** —— 生命周期归用户。sync 只做一次性校验，不常驻。
- **不自动 push** —— 两仓的 push 都由用户决定。skill 仓 push 到远端前，可能还要跑整仓 sync；网站仓 push 前用户多半要本地 `yarn dev` 肉眼过一遍。
- **不自动删 orphan** —— skill 这边 / 网站那边有任一方孤立时，先 warning，人工确认再删。
- **新 tag 值先改字典再写条目**，顺序反了 sync 直接 reject。
- **新二级桶先改对应层 `_CATEGORY.md`**，再写条目文件。桶的边界定义先于内容。
- **primitive 必带 `## Tokens` 下可 JSON.parse 的代码块**，否则网站 preview 的色卡/字阶渲染不出来。
- **commit 格式**：Angular 风格中文 subject；footer 追加 `Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>`。
- **skill 仓真实 git 根在 `/Users/links/.agents/skills/`**，git 命令统一用 `git -C /Users/links/.agents/skills` 形式，避免 cwd 漂移。
- **文件夹式条目 vs 文件式条目**：vibe / archetype 通常是文件夹（下面还有 overview / layout / token 等多文件），读 `<id>/README.md`；composite / atom / primitive 通常是单文件 `<id>.md`。ID 一律取相对路径、不含扩展名。
- **消费模式禁止触发任何 commit / sync / 写入**；沉淀模式每一步都要让用户能中断——尤其是第 5 步写入前，建议把要写的 frontmatter + 正文大纲先贴给用户预览。

## 常见错误

- 新条目写入后忘了跑 `yarn sync` → `registry.json` 过期，网站列表看不到新条目
- frontmatter 里 tag 值不在 `_tags.yaml` 字典 → sync 报 error 拒写 registry
- primitive 没有 `## Tokens` 块 → sync warning，网站 preview 的色卡/字阶无法渲染
- 文件夹式条目 ID 填了路径但文件名不对（比如建了 `vibes/minimal/minimal.md` 而不是 `vibes/minimal/README.md`）→ 规则是：文件夹条目读 `README.md`，文件条目用 `<id>.md`，混用会被 sync 跳过
- 跨层错误引用（composite 引用了另一个 composite / primitive 引用了上层）→ sync 报循环或层级倒挂
- 沉淀模式跳过 tag 校验直接写 → 等网站 sync 时才发现 tag 新值没进字典，要回补
- 消费模式去网站拉资产（网站只是 preview，资产权威源永远是 skill 仓的 `references/`）
- 合并 tokens 时没按层级覆盖顺序（primitive 打底 → atom → composite → archetype → vibe 最后覆盖），导致生成代码的色值偏离用户期望
- 沉淀时把 mood 和 aesthetic 混用（比如把 "calm" 塞进 aesthetic）→ sync 拒写；要先回读 `_tags.yaml` 的 group 划分
- commit 把两个仓的改动写在一个 commit message 里 → 必须双仓独立 commit，消息各自表述

## 术语速查

- **资产（asset）**：`references/` 下的一条 md 或一个文件夹条目，带 frontmatter + 正文
- **主体 ID / 叠加 ID**：消费模式里 Prompt 指定的基础资产和附加资产
- **uses / used by**：frontmatter 里声明的引用关系；sync 会反查反向引用列在 preview 页
- **悬空引用**：uses 里写了 ID 但对应 md 不存在；允许、会 warning
- **orphan**：skill / 网站任一方有、另一方没有的条目；sync 给 warning 但不自动删
- **sync**：网站仓 `yarn sync`，扫 skill 仓 → 重建 `registry.json` + 校验 frontmatter / tag / tokens
- **marker**：网站仓 `frontend/package.json` 里的 `"style-vault-site": true`，用于区分普通 React 仓和 style-vault 网站仓
- **VAULT_OK**：沉淀模式 step 7 的分支判定结果。`true` 表示 `~/.agents/path.json` 的 style-vault 字段有效、目录存在且 frontend/package.json 的 `style-vault-site` marker 为 `true`，`false` 表示任一项不满足，只沉淀到 skill 不联动网站。
- **layer（层）**：vibe / archetype / composite / atom / primitive 五个大类之一
- **bucket（桶）**：每层下的二级目录，如 `composites/display/` / `primitives/palettes/`

## 入口索引

- 五层总览与 ID / frontmatter 规范：[references/README.md](references/README.md)
- Tag 字典：[references/_tags.yaml](references/_tags.yaml)
- 各层边界与二级桶：
  - [vibes/_CATEGORY.md](references/vibes/_CATEGORY.md)
  - [archetypes/_CATEGORY.md](references/archetypes/_CATEGORY.md)
  - [composites/_CATEGORY.md](references/composites/_CATEGORY.md)
  - [atoms/_CATEGORY.md](references/atoms/_CATEGORY.md)
  - [primitives/_CATEGORY.md](references/primitives/_CATEGORY.md)
