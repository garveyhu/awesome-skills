---
name: skill-management
description: >-
  把大量 AI agent skill 按「来源 → 分类 → skill」三级组织、用单一 registry.yaml 驱动、跨 Claude Code 与
  Codex 复用的 skill 管理方法论，自带可直接落地的工具（assets/skillctl.py + registry.example.yaml）。
  当有人想整理 / 组织 / 规模化管理很多 skill、把自己原创的 skill 与第三方分开、控制哪些常驻以省 token、
  只把自己的 skill 开源到 GitHub、一眼监视本机 skill 生态、或想复刻这套体系时使用。Triggers:
  管理 skill, 整理 skill, skill 太多/太乱, skill 目录结构, skill 生态, 组织 agent skills,
  registry 管理 skill, 来源/分类/skill 三级, 复刻 skill 管理方法, organize / manage AI skills at scale, skill registry.
---

# Skill 管理方法论（来源 → 分类 → skill）

把零散堆在一个目录里的几十上百个 skill，重构成一套 **可扩展、可监视、可选择性开源** 的体系。本 skill 既讲方法论，也自带可直接落地的工具——**任何 AI 读完即可为它的用户复刻同一套**（见末尾「复刻步骤」+ `assets/`）。

## 解决什么问题

当 skill 越来越多，把它们全部平铺在一个目录（如 `~/.claude/skills/*`）会同时出四个问题：

1. **找不到 / 看不清**：几十个同级目录，无法按场景归类、无法一眼看清生态。
2. **自有与第三方混在一起**：想开源自己的 skill 时，会把别人的也带出去——而你的定位是分享**自己独有**的能力，不是转发别人的。
3. **token 成本线性涨**：被自动装载的 skill，其描述对每个 agent 都是常驻上下文；低频 skill 不该常驻。
4. **多 agent 各搞一套**：Claude Code、Codex…各自的 skill 目录无法统一维护，容易漂移。

## 核心结构：来源 → 分类 → skill

物理上用**两级目录**承载，第三层是 skill 本身：

```
<root>/                       # 如 ~/.agents
├─ <来源A>/<分类>/<skill>/     # 例：mine/stack/react-best-practices/SKILL.md
├─ <来源B>/<分类>/<skill>/     # 例：community/method/brainstorming/
└─ …                          # 未来加来源 = 加一个顶层目录
```

- **来源（source）= 顶层目录**：按「谁创建的」分。`mine`（你自己的，= 会 push 的 GitHub 仓库）、`community`（开源 / 第三方）、未来可加 `company`（公司内部）…**加一个新来源只是加一个目录 + registry 加一行**。
- **分类（category）= 来源内的场景分组**：`stack` / `docs` / `design` / `media` / `method`…同一个分类可横跨多个来源。
- **skill = 第三层**：一个目录一个 `SKILL.md`。

> 关键解耦：「**分类**」给人看（物理文件夹，按场景导航）；「**加载策略**」给机器看（见下「三层」）。两者互不绑死。

## 单一事实源：registry.yaml

所有 skill 的 `source / category / tier` 集中登记在仓库外的一张表 `registry.yaml`。**它是唯一手维护的东西**，其余（镜像 / 软链 / 白名单）全部由工具据它派生。模板见 `assets/registry.example.yaml`。

## 派生物（从 registry 生成，不手维护）

1. **扁平镜像 `<root>/skills/`**：把 `tier=core` 的 skill 用软链拍平成一层，供「会扫描整个目录」的通用 agent 使用——这样物理上分了类，扁平扫描照样工作。
2. **各 agent 挂载点的软链**：把 `core + extra` 软链进每个 agent 的 skill 目录（`mounts` 列表，见下「跨 agent」）。
3. **白名单 `.gitignore`**：只有「会 push 的来源目录」是 git 仓库，且它整目录只含你自己的 skill——所以 `.gitignore` 只挡垃圾即可，**第三方天然不在这个目录、永不外泄**。

## 三层加载策略（控制 token）

每个 skill 在 registry 里标一个 `tier`：

| tier | 进扁平镜像（通用 always-on） | 进 agent 挂载点 | 用途 |
|---|---|---|---|
| `core` | ✅ | ✅ | 广泛常用、廉价 |
| `extra` | ❌ | ✅ | 重型 / 小众，按需 |
| `parked` | ❌ | ❌ | 仅留存，不装载 |

改 tier 即调装载范围——不挪文件、不动目录。

## 工具 skillctl

`assets/skillctl.py`，零第三方依赖，三个子命令：

```bash
python3 scripts/skillctl.py          # stats：一眼看生态（来源/分类/层级分布 + 挂载健康 + 未纳管 foreign）
python3 scripts/skillctl.py sync     # 据 registry 重建：扁平镜像 + 各挂载点软链 + 白名单 .gitignore
python3 scripts/skillctl.py doctor   # 体检：缺 SKILL.md / registry↔磁盘漂移 / 来源串味 / 孤儿·断链
```

工作流：**只改 registry.yaml → 跑 sync → doctor 验收**。`stats` 里的「未纳管 foreign」会暴露任何绕过 registry 偷偷塞进挂载点的 skill。

## 跨 agent：Claude Code 与 Codex

方法论本身与 agent 无关，**只有最后「软链挂到哪」按 agent 不同**——这正是 `mounts` 列表存在的意义，列出每个 agent 的目标目录，`sync` 一次同步到全部：

- **Claude Code**：原生在 `~/.claude/skills/<name>/SKILL.md` 自动发现 skill。挂载点填 `~/.claude/skills`。
- **Codex**：没有等价的 skill 自动发现机制。两种落地：① 把扁平镜像目录在 `AGENTS.md` 里引用，让 Codex 读到；② 软链进你让 Codex 读取的某个目录，挂载点填那个路径。
- **任何能读文件的 AI**：直接把本 `SKILL.md` 喂给它，按下方步骤执行即可复刻。

## 复刻步骤（AI 照此执行即可搭好）

1. **选 `<root>`**（如 `~/.agents`），建来源目录：`mine/`（你自己的，将来 git 仓库）、`community/`（第三方）。
2. **把每个 skill 放到 `<来源>/<分类>/<skill>/`**，每个 skill 一个 `SKILL.md`。
3. **写 `<root>/registry.yaml`**——参 `assets/registry.example.yaml`，填 `mounts`、`sources`、`categories`，以及每个 skill 的 `{source, category, tier}`。
4. **放工具**：把 `assets/skillctl.py` 拷到 `<root>/scripts/skillctl.py`。
5. **`python3 scripts/skillctl.py sync`** → 生成扁平镜像 + 各挂载点软链 + 白名单。
6. **`python3 scripts/skillctl.py`** 看 stats 总览；**`doctor`** 验收无漂移。
7. **发布自己的来源**：进 `mine/` 目录 `git init` + 配远程 + `push`。白名单保证只发布你自己的 skill，第三方留本地。

> 之后日常只有一件事：新增 / 调整 skill 时改 `registry.yaml` 一处，`sync` 一下。结构永不腐化。
