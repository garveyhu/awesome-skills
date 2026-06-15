# self-improving-workflow

> 面向 Claude Code 项目的通用方法论 skill。无技术栈模板，无分档系统。两大支柱。

> English version: [README.md](README.md)

## 两大支柱

**支柱 1 — 多智能体协同学习**

四个专职子 agent 在四个层次评审每一个计划、任务、切片和阶段。它们的发现会自动晶化为项目规则，无需人工逐步审批。

| 评审者 | 触发时机 |
|---|---|
| `planner-critic` | 每次新计划 / 重新规划 |
| `implementation-reviewer` | 每个任务完成后 |
| `requirement-auditor` | 每个切片完成后 |
| `integration-checker` | 每个阶段完成后 |

**支柱 2 — 长任务不间断执行**

单一 `/run <topic>` 命令驱动分层计划（`phase → slice → task`）自主运行至完成。仅在以下情况停止：
1. `guard.sh` 检测到不可逆操作（数据丢失、远程写入、凭据变更、对外通信、进程强杀）
2. 同一目标连续 3 次评审失败

每个非平凡决策都记录到 `.claude/state/decisions.jsonl`，供事后审计。

---

## 快速开始

在项目根目录，确保 skill 已安装到 `~/.agents/skills/` 后：

```
# 第 1 步（每个项目一次）—— 用 skill 名字调用，触发 bootstrap。
# 这一步会把 commands/ 和 agents/ 镜像到 .claude/ 下，
# 让 Claude Code 能发现它们，并种好 state/ 和 memory/。
/self-improving-workflow

# 第 2 步 —— 启动完全自主的规划→执行→评审循环
/run 实现用户搜索功能

# 严格模式 —— 在 topic-auditor 端到端验证通过前拒绝标记 done
# 比 /run 慢，但能证明任务真的完成
/run-strict 上线密码重置功能，要求带邮件发送链路

# 仅规划，不执行；含 Planner-Critic 评审
/plan 重构认证模块

# 恢复中断的计划
/resume
```

第 1 步完成后，项目里就有自己的 `.claude/{commands,agents,state,memory,rules}/`。这一步是幂等的 —— skill 升级后再次调用会拉新加的 commands/agents，但永远不会覆盖你本地的修改。

---

## 工作机制 — 由表及里

### 一句话定位

**给 AI 一个长任务，AI 自己规划、执行、自评、改进，直到完成；过程中 4 个评审 agent 互相把关，踩到的坑自动沉淀成下次的规则。**

### 用户视角 — 你只做 3 件事

```
1. 装上 skill（git clone awesome-skills，里面就有 self-improving-workflow）
2. 在任意项目里说一句：/run 帮我加个用户登录功能
3. 等。看终端跑就行了。
```

中间不需要你做任何决定。AI 跑完会告诉你 "done" 或者 "卡住了"。

### AI 视角 — 收到 `/run` 之后发生什么

把 `/run` 当成一个有限状态机：

```
[bootstrap]                                ← 第一次跑：init.sh 种 .claude/ 骨架
     ↓
[写 plan]                                  ← AI 把任务拆成 phase→slice→task 三层树
     ↓
[planner-critic 评审 plan]                 ← 评审 1：plan 本身够不够好？
     ↓ pass
[执行循环] ←──────────────────────────────┐
     ↓                                      │
   挑下一个 pending 的 task                 │
     ↓                                      │
   guard.sh 检查每条 bash 命令              │ 命中不可逆 → BLOCKED 退出
     ↓ allowed                              │
   AI 写代码 / 跑测试 / commit              │
     ↓                                      │
   [implementation-reviewer 评审 task]      │ 评审 2：这个 task 做对了吗？
     ↓ pass                                 │
   slice 全 done? → [requirement-auditor]   │ 评审 3：这个 slice 满足 user_value 了吗？
     ↓ pass                                 │
   phase 全 done? → [integration-checker]   │ 评审 4：phase 内部模块对得上吗？
     ↓ pass                                 │
   plan 全 done? → [crystallize.sh] → done  │
     ↓ no                                   │
     └──────────────────────────────────────┘
```

**唯一的两个停机条件**：
1. `guard.sh` 拦下一条不可逆命令（删数据 / 强推 / 改密钥 / 发 webhook / kill -9 / drop table）
2. 同一个目标连续 3 次评审 fail（plan 烂 / task 修不好 / slice 漏需求）

其他任何 "该选 A 还是 B" 的事，**AI 自己拍**，写一行到 `decisions.jsonl`，继续干。

### Plan 的形状（核心数据结构）

```
Plan
├── Phase 1（无上限）
│   ├── Slice 1.1 — 必须有 user_value 和 acceptance
│   │   ├── Task 1.1.1 — 必须动词开头
│   │   ├── Task 1.1.2
│   │   └── ...
│   ├── Slice 1.2
│   └── ...
├── Phase 2
└── ...
```

`plan_lint.sh` 用 jq 强校验这个 schema。AI 写出 "100 个 task 一个 phase" 那种鬼东西会被 planner-critic 直接 reject 重写。

**为什么三层**：颗粒度对应不同评审深度。
- task 完成 → implementation-reviewer 检查代码
- slice 完成 → requirement-auditor 检查"用户价值"是不是真的实现了
- phase 完成 → integration-checker 检查跨 slice 的接口/状态/事件是不是对得上

### 4 个评审 agent 各管一段

| Agent | 触发时机 | 看什么 | 失败时怎么修 |
|---|---|---|---|
| **planner-critic** | plan 写完 / 重写后 | plan 本身 + 历史教训 | AI 重写 plan |
| **implementation-reviewer** | 每个 task 完成时 | 这个 task 的代码改动 | AI 重做这个 task |
| **requirement-auditor** | 每个 slice 完成时 | slice 的 user_value + 所有 task 产出 | 把缺的需求加成新 task |
| **integration-checker** | 每个 phase 完成时 | phase 内所有 slice 的衔接 | 把缺的衔接加成新 slice |

**关键约束**：评审 agent **只读**，不写代码。它们只产 JSON 报告（pass / fail + issues），主循环根据报告自己改。这避免了"评审者抢方向盘"。

### 两根支柱怎么实际运转

**支柱 1 — 多智能体协作学习**

不是简单的"多个 agent 一起干活"。是三类角色互相隔离：
- **执行者**（跑 task 的 AI 主循环）
- **4 个评审者**（4 个独立 subagent，各管一段）
- **学习者**（`crystallize.sh`，确定性脚本）

具体怎么"学"：

```
implementation-reviewer 发现："这个 task 没校验 null 输入"
    ↓
写一条 episodic 到 .claude/memory/episodic/ep-xxx.json
    fingerprint: "boundary:null-input:user-service"
    confidence: 0.8
    ↓
crystallize.sh 跑（每 phase 完成时 + 退出时）
    ↓
聚合：fingerprint 的前 2 段 "boundary:null-input" 已经出现 3 次了？
    且 avg_confidence ≥ 0.7？
    ↓ yes
自动 append 一条规则到 .claude/rules/dev-lessons.md
    ↓
下次 /run 启动时，planner-critic 和 implementation-reviewer
都会自动读 dev-lessons.md，对照新规则审 plan 和代码
```

**阈值写死**：≥3 次 + ≥0.7 置信度。不可调。设计上故意防止用户调成"少学"或"多学"。

**支柱 2 — 长任务不间断执行**

关键点不是"AI 一直跑"那么简单。是：
- **决策权下放**：所有非不可逆决策 AI 自己做（选 lib、命名、要不要加 cache、用 mock 还是真依赖……）
- **决策可审计**：`decisions.jsonl` append-only 记录所有非平凡选择，事后你能看 AI 当时为什么选 A 不选 B
- **跨 session 续跑**：`plan.json` + `decisions.jsonl` 是状态快照，进程被杀了下次 `/resume` 从第一个非 done task 继续
- **task 必须幂等**：被中断重做不会留垃圾。implementation-reviewer 把"幂等性"列入审查项

### 文件布局怎么对应这个机制

**关键设计**：`scripts/` 留在 skill 仓库（用绝对路径调用）；`commands/` 和 `agents/` 在 bootstrap 时从 skill 镜像到每个项目的 `.claude/`（Claude Code 只能从 `.claude/` 下发现 slash 命令和 subagent，所以必须落地）。state / memory / rules 一次性种到项目里，随使用增长。

学习是项目维度的——A 项目踩的坑不会污染 B 项目。下次 `/run` 同一个项目时，已晶化的规则会自动变成 plan 评审和代码评审的 checklist——这个 skill 是"越用越懂你这个项目"。

### 一个具体例子穿起来看

```
你输入：/run 给项目加一个用户注册接口

[bootstrap] init.sh 跑（如果 .claude/ 不存在）

[plan]  AI 写出：
        Phase 1: 用户注册 MVP
        ├── Slice 1.1: 数据库 schema
        │   ├── T1: 实现 User model
        │   ├── T2: 写 alembic migration
        │   └── T3: 验证 migration 在测试库
        ├── Slice 1.2: 注册 endpoint
        │   ├── T1: 实现 POST /register
        │   ├── T2: 加邮箱格式校验
        │   ├── T3: 加密码 hash
        │   └── T4: 写集成测试
        └── Slice 1.3: 错误处理 + 限流

[planner-critic] pass

[execute T1.1.1] AI 写 model
[guard.sh "vim models/user.py"]  exit 0
[guard.sh "alembic upgrade head"] exit 0
[implementation-reviewer T1.1.1] pass
[execute T1.1.2] ...
[implementation-reviewer T1.1.2] FAIL — "migration 没用 batch_alter_table，SQLite 会挂"
   AI 修
   [implementation-reviewer T1.1.2] pass
   写 episodic: fingerprint=spec:sqlite-batch-alter:migration, confidence=0.9
[execute T1.1.3] ...

[slice 1.1 done → requirement-auditor] pass

[execute slice 1.2 ...] ...
[implementation-reviewer T1.2.2] FAIL — "邮箱校验没处理 Unicode"
   AI 修
   写 episodic: fingerprint=boundary:unicode:input-validation, confidence=0.7

[slice 1.2 done → requirement-auditor]
   FAIL — "user_value 说'用户能注册'，但没看到任何返回 token 的逻辑"
   注入新 task: T1.2.5 实现 注册成功后返回 JWT
[execute T1.2.5] ...
[requirement-auditor 重审] pass

[slice 1.3 done] [phase 1 done → integration-checker] pass

[plan done → crystallize.sh]
   episodic 聚合 → 没有任何 fingerprint 凑够 3 次 → 不晋升
   （这次 /run 没产生新规则，但 episodic 已经存着了，下次 /run 累计到 3 就晋升）

[退出] plan.meta.status = done
```

第二次跑同一个项目时：planner-critic 和 implementation-reviewer 会读 `dev-lessons.md`，已晶化的规则变成 plan 评审和代码评审的硬 checklist。第一次跑可能踩很多坑，跑十次之后规则库就稳定下来了。

### 严格模式 (`/run-strict`)

当任务无法接受半成品时（生产发布、面向用户的功能、安全相关），用 `/run-strict` 代替 `/run`。三层差异：

- **计划入口闸**：`planner-critic` 强制执行 Universal Completion Chain —— 每个 acceptance 都必须有一条 task 链能追到 observable proof（测试输出、命令 stdout、文件内容、日志关键行）。链不闭合的浅 plan 在执行之前就被拒绝。
- **单任务闸**：`implementation-reviewer` 要求 evidence 必须是运行时证据，纯 commit sha 一律拒绝。纯重构/重命名走 `static-only: <reason>` 显式豁免。
- **整体收尾闸**：第 5 个 reviewer `topic-auditor` 在所有 phase 完成后跑一次，被授权执行只读 smoke 命令（`pytest`、`curl`、`cat` 等）。它只回答一个问题："如果一个全新用户只看到这个 topic 和这些产物，他会不会说'这事完成了'？" 不会 → 把缺的链路作为新 slice 注入到那个特殊的 `P_recovery` phase，重新进 execute loop。`status: done` 必须由 `topic-auditor` 说 yes 之后才能写。

严格模式还使用 **进度感知 strike rule**：3 次 fail 才挂的规则只在 reviewer 的 issue 文本完全相同时触发 —— 在慢慢进步的修复永远不会被打断。

`/run-strict` 大约比 `/run` 慢 2-5×。要用就要明白自己在做什么。

---

## 命令

| 命令 | 用途 |
|---|---|
| `/run <topic>` | 主入口 — 完整的自主规划 + 执行 + 评审循环 |
| `/run-strict <topic>` | 严格模式 — 5 个评审者循环，在 topic-auditor 验证端到端交付前拒绝标记完成 |
| `/plan <topic>` | 仅规划，不执行；包含 Planner-Critic 评审 |
| `/review [scope]` | 诊断性派发评审者，只读 |
| `/learn` | 手动触发记忆晶化（episodic → rules） |
| `/resume` | 从第一个未完成任务继续执行未完成的计划 |

---

## Skill 仓库布局

```
self-improving-workflow/
├── SKILL.md
├── README.md / README.zh-CN.md
├── commands/                         ← bootstrap 时镜像到 .claude/commands/
│   ├── run.md
│   ├── run-strict.md
│   ├── plan.md
│   ├── review.md
│   ├── learn.md
│   └── resume.md
├── agents/                           ← bootstrap 时镜像到 .claude/agents/
│   ├── planner-critic.md
│   ├── implementation-reviewer.md
│   ├── requirement-auditor.md
│   ├── integration-checker.md
│   └── topic-auditor.md
├── scripts/                          ← 留在 skill，用绝对路径调用
│   ├── init.sh                       ← 在目标项目里种 .claude/
│   ├── guard.sh                      ← 不可逆操作正则检测
│   ├── crystallize.sh                ← episodic→semantic→rules 晶化
│   └── plan_lint.sh                  ← plan.json schema 校验
├── seeds/                            ← init.sh 拷到项目里的种子文件
│   ├── CLAUDE.md
│   ├── plan.schema.json
│   ├── rules/{autonomy-stops,dev-lessons}.md
│   └── memory/README.md
├── references/
│   ├── methodology.md
│   ├── plan-schema.md
│   ├── reviewer-contracts.md
│   ├── learning-loop.md
│   └── migration-from-tiered.md
└── tests/                            ← bats 测试套件 + fixtures
```

## 文件布局 — 项目侧（`.claude/`）

`init.sh` 在你的项目里跑完后：

```
.claude/
├── CLAUDE.md                          ← 来自 seeds/，仅当项目还没有时才写入
├── commands/                          ← 从 skill 镜像（Claude Code 在这里发现 slash 命令）
│   ├── run.md
│   ├── run-strict.md
│   ├── plan.md
│   ├── review.md
│   ├── learn.md
│   └── resume.md
├── agents/                            ← 从 skill 镜像（Claude Code 在这里发现 subagent）
│   ├── planner-critic.md
│   ├── implementation-reviewer.md
│   ├── requirement-auditor.md
│   ├── integration-checker.md
│   └── topic-auditor.md
├── rules/
│   ├── autonomy-stops.md              ← 来自 seeds/，可追加
│   └── dev-lessons.md                 ← 来自 seeds/，由 /learn 自动填充
├── state/
│   ├── plan.schema.json               ← 来自 seeds/
│   ├── plan.json                      ← 初始为 `{}`
│   ├── decisions.jsonl                ← 初始为空
│   └── archive/                       ← 历史 plan
└── memory/
    ├── README.md                      ← 来自 seeds/
    ├── episodic/                      (已 gitignore)
    ├── semantic-patterns.json         (git 追踪)
    └── working/                       (已 gitignore)
```

`commands/` 和 `agents/` 是按文件 write-once：升级 skill 后再跑 `init.sh`，新加的文件会被拉过来，但你本地改过的文件不会被覆盖。

`.gitignore` 会被幂等追加，排除 `episodic/` 和 `working/`。

---

## 参考文档

- [`references/methodology.md`](references/methodology.md) — 两大支柱的设计理由与混合架构方法
- [`references/plan-schema.md`](references/plan-schema.md) — phase/slice/task 树形结构与硬性上限
- [`references/reviewer-contracts.md`](references/reviewer-contracts.md) — 四个评审者的触发条件与 IO 格式
- [`references/learning-loop.md`](references/learning-loop.md) — episodic→semantic→rules 晶化算法
- [`references/migration-from-tiered.md`](references/migration-from-tiered.md) — 从旧分档版本迁移的指南
