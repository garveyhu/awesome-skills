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

## 文件布局 — 项目侧（`.claude/`）

`init.sh` 在项目中运行后生成：

```
.claude/
├── CLAUDE.md
├── commands/
│   ├── run.md
│   ├── plan.md
│   ├── review.md
│   ├── learn.md
│   └── resume.md
├── agents/
│   ├── planner-critic.md
│   ├── implementation-reviewer.md
│   ├── requirement-auditor.md
│   └── integration-checker.md
├── rules/
│   ├── autonomy-stops.md
│   └── dev-lessons.md
├── state/
│   ├── plan.json
│   ├── plan.schema.json
│   ├── decisions.jsonl
│   └── archive/
└── memory/
    ├── README.md
    ├── episodic/               (已 gitignore)
    ├── semantic-patterns.json  (git 追踪)
    └── working/                (已 gitignore)
```

`.gitignore` 会被幂等追加，排除 `episodic/` 和 `working/`。

---

## Skill 仓库布局

```
self-improving-workflow/
├── SKILL.md
├── README.md / README.zh-CN.md
├── scripts/
│   ├── init.sh            ← 初始化，无分档/技术栈/合规参数
│   ├── guard.sh           ← 不可逆操作正则检测
│   ├── crystallize.sh     ← episodic→semantic→rules 晶化
│   └── plan_lint.sh       ← plan.json schema 校验
├── templates/             ← 单一目录，无分档子目录
│   ├── CLAUDE.md.template
│   ├── commands/{run,plan,review,learn,resume}.md.template
│   ├── agents/{planner-critic,implementation-reviewer,
│   │          requirement-auditor,integration-checker}.md.template
│   ├── rules/{autonomy-stops,dev-lessons}.md.template
│   ├── state/{plan.schema.json,.gitkeep}
│   └── memory/{README.md.template,episodic/.gitkeep}
└── references/
    ├── methodology.md
    ├── plan-schema.md
    ├── reviewer-contracts.md
    ├── learning-loop.md
    └── migration-from-tiered.md
```

---

## 参考文档

- [`references/methodology.md`](references/methodology.md) — 两大支柱的设计理由与混合架构方法
- [`references/plan-schema.md`](references/plan-schema.md) — phase/slice/task 树形结构与硬性上限
- [`references/reviewer-contracts.md`](references/reviewer-contracts.md) — 四个评审者的触发条件与 IO 格式
- [`references/learning-loop.md`](references/learning-loop.md) — episodic→semantic→rules 晶化算法
- [`references/migration-from-tiered.md`](references/migration-from-tiered.md) — 从旧分档版本迁移的指南
