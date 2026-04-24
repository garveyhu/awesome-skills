# style-vault-sediment skill

**个人风格资产库 · 写侧** · 新增 / 修改 / 删除风格资产的完整工作流。

这是 style-vault 三件套中的**写 skill**——**只有创作者 / 社区维护者需要装**。普通消费者用网站 + [`style-vault`](../style-vault/) 读 skill 即可。

读操作（消费资产、查分类字典）走兄弟 skill [`style-vault`](../style-vault/)。本 skill 只负责写。

---

## 三件套架构

```mermaid
graph TB
    classDef read fill:#2B6CB0,stroke:#1E5090,stroke-width:2px,color:#fff
    classDef write fill:#48BB78,stroke:#38A169,stroke-width:2px,color:#fff
    classDef web fill:#ED8936,stroke:#C66A32,stroke-width:2px,color:#fff

    A["style-vault skill<br/>读 · 消费 + 分类字典"]:::read
    B["style-vault-sediment skill<br/>写 · 新增 / 修改 / 删除"]:::write
    C["style-vault web<br/>浏览 · 发现 · 分发 prompt"]:::web

    B ==>|运行时：读字典 + 查询| A
    B -.->|沉淀时：写 MD 条目| A
    B -.->|沉淀时：写 preview 组件| C
    C ==>|yarn sync：镜像 taxonomy + 扫描 references| A
```

| 项目 | 类型 | 作用 |
|---|---|---|
| **style-vault skill** | Claude Code skill | AI 消费风格 + 查询分类字典 |
| **style-vault-sediment skill**（本仓） | Claude Code skill | AI 沉淀 / 修改 / 删除风格 |
| **style-vault web** | React + FastAPI 仓库 | 浏览网站 + prompt 卡片分发 |

两个 skill 装到你 Claude Code 的 skills 目录下（互为兄弟目录）。具体路径取决于你的配置。

---

## 本 skill 做什么

把风格**沉淀**到 style-vault——覆盖风格资产的完整生命周期：

### 三种操作模式（由触发语自动路由）

| 用户说… | 走的路径 |
|---|---|
| "沉淀" / "加到 vault" / `/style-vault-sediment` | **默认 create**（新增） |
| "修改 `<id>`" / "改 `<id>` 的 tag" | `modify-workflow` |
| "删除 `<id>`" / "下掉 `<id>`" | `delete-workflow` |

### Create 的四种起点

默认 create 会先问用户沉淀的起点：

```
1) 本地项目路径（扫项目反向归类到六层资产）
2) 在线资源（URL / 截图 / 设计稿，视觉分析重写）
3) 从零创作（有想法，对话式迭代到落地）
4) 其他 / 不确定
```

全流程见 [SKILL.md](SKILL.md) 和 [references/shared-workflow.md](references/shared-workflow.md)。

---

## 三档深度 · 先选再沉淀

进入 discovery 前第一步先问**挖掘深度**——决定要抽多少条、扫多细。详见 [references/depth-tiers.md](references/depth-tiers.md)。

| 档位 | 名称 | 目标条目 | 时间 | 典型场景 |
|:---:|---|:---:|:---:|---|
| **1** | 精髓（essence） | 5–8 | 20–30 min | 给别人看 5 样最代表这个风格的东西 |
| **2** | 基础（foundation） | 12–18 | 1–1.5 h | 能启动一个同风格新产品的最小设计系统 · **默认** |
| **3** | 全量（comprehensive） | 30–50+ | 3–4 h | 尽可能 100% 复刻 · 每条主路由独立 page |

**Tier 3 硬下限**（不达标不能进入写入阶段）：

- 全路由枚举 → 主路由 ≥ 80% 被沉淀为独立 page
- 跨文件 className 模式扫描 → 至少 3 条"全局模式"沉淀为 token/component（抓"负空间一致性"——整站统一的按钮/输入/圆角等）
- 表单 / 状态 / 动效清单 → 覆盖率 ≥ 80%

越高档对 discovery 要求越严，避免"抽样式"沉淀漏掉核心信息。

---

## Skill 自迭代 · 教训回写

Skill 会**自己修自己**——每次沉淀出错（用户指出差异大 / AI 发现抽象错了），把**错误模式**抽象成硬规矩回写到对应 workflow 文件，后续所有沉淀自动遵守。详见 [references/lessons-loopback.md](references/lessons-loopback.md)。

### 流程

```
沉淀出错
  ↓
诊断性质
  ↓
[一次小错] → 改条目即可
[模式错]   → 回写 3 步：
             1. 抽象问题（一句话"为什么会犯这类错"）
             2. 定位所属 workflow 文件
             3. 写硬规矩 + 自检问题
  ↓
登记到 lessons-loopback.md 的 append-only 清单
  ↓
同 commit 推送（message 前缀 docs(skill): 沉淀教训 · xxx）
```

### 反污染硬规矩

- 不允许把"具体错误"（某条字段值错）当教训写入
- 不允许重复加同义规则——先 grep 搜已有的
- 规则必须"必须/不允许"强制语气——温馨提示会被 AI 忽略
- 清单 append-only，过时条目只标注"已失效"不删

### 已回写的典型教训

- **路由覆盖率**：Tier 2 沉淀 skillhub 漏 10/12 主路由 → 改到 `depth-tiers.md` 加 Tier 3 硬下限 checklist
- **必须通读 JSX**：写 page 条目时只读文件头 150 行（state/hooks）凭印象抽象 → 改到 `sediment-from-project.md` 加"写 page 前必须通读 JSX + 文件长度分级读法 + 4 项自检问题"
- **antd 默认主色**：用 antd Button `type="primary"` 没覆盖 `colorPrimary` 导致 preview 出现默认蓝 → 改到 preview 写法约定里（见该教训登记）

Skill 越用越准——每次真实使用后都比上一次少犯一类错。

---

## 核心工作流（shared-workflow 8 步 + step 9 教训回写）

所有路径（create / modify / delete）都汇入同一条 8 步主干 +（条件触发）第 9 步：

```
0. 档位门                （Tier 1/2/3，见上节）
1. 加载分类字典         （调 taxonomy.py overview）
2. 授权 auto-fill       （Y / N / 逐条决定）
3. 生成完整写入方案     （拓扑序 + frontmatter + 正文骨架）
4. 整批 review          （用户确认后 plan.md 落盘 · Tier 3 跑覆盖率核对）
5. path.json 分叉        （VAULT_OK 判定 + 并发锁）
6. 逐条写入             （skill 仓 + 网站仓，每条跑 yarn sync）
7. 网站仓 commit         （若 VAULT_OK=true）
8. 沉淀报告 + skill 仓聚合 commit
9. 教训回写（条件触发）  （用户指出差异大 / 要求重写时走）
```

## 硬约束

- **档位先行**——进入 discovery 前先选 Tier 1/2/3
- **写入前必须整批 review**——用户确认后才落盘
- **Tier 3 写入前必须覆盖率核对 ≥ 80%**——未达标打断询问补齐 / 降档 / 手动放行
- **AI 自动填元信息需一次性授权**（Y/N/逐条决定）
- **双仓独立 commit**，不 push，由用户手动
- **新 tag / category 必须先改 taxonomy.json 再写条目**
- **每次沉淀产生报告**，落盘到 `assets/sediment-history/<author>/<date-topic>/`
- **Skill 可自迭代**——沉淀结果出错时区分"一次小错"与"模式错"，模式错回写到对应 workflow 文件并登记 `lessons-loopback.md`

---

## 目录结构

```
style-vault-sediment/
├── SKILL.md                              入口路由（按触发语分发）
├── README.md                             本文件
├── references/
│   ├── README.md                         workflow 索引
│   ├── shared-workflow.md                共享 8 步主干 + step 9 教训回写
│   ├── depth-tiers.md                    3 档深度（精髓 / 基础 / 全量）
│   ├── lessons-loopback.md               skill 自迭代 · 教训回写清单
│   ├── sediment-from-project.md          Create 起点 1：本地项目
│   ├── sediment-from-web.md              Create 起点 2：在线资源
│   ├── sediment-from-scratch.md          Create 起点 3：从零创作
│   ├── sediment-from-other.md            Create 起点 4：兜底路由
│   ├── modify-workflow.md                修改已有条目
│   └── delete-workflow.md                删除已有（含 cascade）
├── assets/
│   └── sediment-history/                 沉淀历史（按作者分目录）
│       ├── .author-config.example.json
│       ├── .gitignore                    忽略真实 .author-config.json
│       └── <author-slug>/
│           └── YYYY-MM-DD-<topic>/
│               ├── plan.md               沉淀计划
│               ├── report.md             沉淀报告
│               └── source.md (可选)       原始素材溯源
└── scripts/                              预留（未来可能加工具）
```

---

## 沉淀历史的价值

每次沉淀都会在 `assets/sediment-history/` 留下三种文件（视情况）：

- **plan.md** —— 步骤 4 用户确认方案后落盘，即使后续写入失败也保留
- **report.md** —— 步骤 8 落盘，记录实际写入了什么、元信息怎么来的
- **source.md** —— from-web / from-project 才有，溯源 URL / 截图 / 项目路径

按 **作者 slug + 日期 + 主题** 分目录——未来支持社区多人维护时，每人一个文件夹不冲突。

查询历史：`taxonomy.py history`（归在读侧 skill 里），见 [../style-vault/](../style-vault/)。

---

## 与其它两件的关系

### 硬依赖 `style-vault` skill

运行时**每次沉淀都会**：
- 读 `../style-vault/assets/taxonomy.json` 做分类合法性校验
- 调 `../style-vault/scripts/taxonomy.py` 查 id / 反向引用（删除前依赖检查）

两 skill **必须成对安装**。

### 按需写入 `style-vault web`

沉淀时判断 `path.json`（存放网站仓路径的配置文件，skill 约定位置见 [shared-workflow.md](references/shared-workflow.md)）+ 网站仓 marker，成立则：
- 写 `frontend/src/preview/<id>.tsx`
- 跑 `cd $VAULT/frontend && yarn sync` 做校验
- 双仓独立 commit

不成立（`VAULT_OK=false`）时走 **skill-only 沉淀**——只写 skill 仓，不动网站。

---

## 相关链接

- [SKILL.md](SKILL.md) · 入口路由表
- [references/shared-workflow.md](references/shared-workflow.md) · 8 步主干 + step 9 教训回写
- [references/depth-tiers.md](references/depth-tiers.md) · 3 档深度定义 + 硬下限 checklist
- [references/lessons-loopback.md](references/lessons-loopback.md) · skill 自迭代机制 + 已回写教训清单
- [references/README.md](references/README.md) · workflow 索引
- 兄弟 skill：[style-vault](../style-vault/)（消费者必装的读 skill）
- 网站仓：https://github.com/garveyhu/style-vault
