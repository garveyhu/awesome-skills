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

单一 `/run <topic>` 命令驱动分层计划（`phase → slice → task`，上限 4×5×7）自主运行至完成。仅在以下情况停止：
1. `guard.sh` 检测到不可逆操作（数据丢失、远程写入、凭据变更、对外通信、进程强杀）
2. 同一目标连续 3 次评审失败

每个非平凡决策都记录到 `.claude/state/decisions.jsonl`，供事后审计。

---

## 快速开始

在项目根目录，确保 skill 已安装到 `~/.agents/skills/` 后：

```
# 启动完全自主的规划→执行循环
/run 实现用户搜索功能

# 仅规划，不执行；含 Planner-Critic 评审
/plan 重构认证模块

# 恢复中断的计划
/resume
```

首次调用 `/run` 时，`init.sh` 会自动初始化 `.claude/` 骨架（幂等操作；已存在的文件永不覆盖）。

---

## 命令

| 命令 | 用途 |
|---|---|
| `/run <topic>` | 主入口 — 完整的自主规划 + 执行 + 评审循环 |
| `/plan <topic>` | 仅规划，不执行；包含 Planner-Critic 评审 |
| `/review [scope]` | 诊断性派发评审者，只读 |
| `/learn` | 手动触发记忆晶化（episodic → rules） |
| `/resume` | 从第一个未完成任务继续执行未完成的计划 |

---

## Skill 仓库布局

slash 命令和评审 subagent 直接放在 skill 根目录 — 用户装好 skill 立即可用，没有拷贝步骤。

```
self-improving-workflow/
├── SKILL.md
├── README.md / README.zh-CN.md
├── commands/                         ← skill 级 slash 命令
│   ├── run.md
│   ├── plan.md
│   ├── review.md
│   ├── learn.md
│   └── resume.md
├── agents/                           ← skill 级评审 subagent
│   ├── planner-critic.md
│   ├── implementation-reviewer.md
│   ├── requirement-auditor.md
│   └── integration-checker.md
├── scripts/
│   ├── init.sh                       ← 把每个项目的状态种子写进 .claude/
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

`init.sh` 只会种"项目级状态" — slash 命令和评审 agent 不会拷到项目里：

```
.claude/
├── CLAUDE.md                          ← 来自 seeds/
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

`.gitignore` 会被幂等追加，排除 `episodic/` 和 `working/`。

---

## 参考文档

- [`references/methodology.md`](references/methodology.md) — 两大支柱的设计理由与混合架构方法
- [`references/plan-schema.md`](references/plan-schema.md) — phase/slice/task 树形结构与硬性上限
- [`references/reviewer-contracts.md`](references/reviewer-contracts.md) — 四个评审者的触发条件与 IO 格式
- [`references/learning-loop.md`](references/learning-loop.md) — episodic→semantic→rules 晶化算法
- [`references/migration-from-tiered.md`](references/migration-from-tiered.md) — 从旧分档版本迁移的指南
