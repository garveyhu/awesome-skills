---
name: memory-palace
description: >-
  引导任何人用「记忆宫殿」机制重塑个人记忆管理：一座平台无关的 Obsidian vault（纯 markdown），
  让 Claude / Codex / Gemini 等任何 CLI 共读共写「你是谁 / 你的项目 / 偏好 / 决策」，越用越懂你，
  记忆可见可改可带走、不被厂商锁死。子命令路由：help(原理讲解页) · init(脚手架空宫殿) ·
  interview(深度访谈建身份) · extract(从本地 agent 规则·会话导入) · distill+review(蒸馏飞轮·你审批) ·
  analyze(体检优化)。引擎是 scripts/mp.py（确定性·仅标准库）。
  当用户想：搭建/重塑个人 AI 记忆体系、让 AI 越来越懂自己、跨工具共享同一份「我」、把散落各处的规则偏好
  集中成第二大脑、给现有记忆库做体检、或复刻这套机制时使用。Triggers: /memory-palace, 记忆宫殿,
  memory palace, second brain, 个人记忆体系, 让 AI 懂我, 跨平台记忆, 沉淀记忆, 蒸馏记忆, build my memory system,
  make AI understand me, personal memory vault。
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Memory Palace · 记忆宫殿引导 skill

把「跨平台、越用越懂你」的个人记忆机制，从一套个人配置变成**任何人可复刻**的体系。
本 skill 是**调度器**：按子命令路由到 `references/` 里的具体流程；确定性操作交给 `scripts/mp.py`。

## 用法

`/memory-palace <子命令> [参数]`。无子命令或 `help` → 走概念引导。

| 子命令 | 流程文档 | 干什么 |
|--------|---------|--------|
| `help` | `references/concept.md` | 打开去个人化讲解页 + 列菜单（首用建立概念） |
| `init` | `references/init.md` | 脚手架一座空宫殿 + 接上各 AI 工具 |
| `interview` | `references/interview.md` | 深度访谈，把「你是谁」问出来（挖掘深） |
| `extract` | `references/extract.md` | 从本地 Claude/Codex 规则·会话导入已有记忆 |
| `distill` | `references/flywheel.md` | 蒸馏最近会话 → 出候选草稿 |
| `review` | `references/flywheel.md` | 审批候选 → 晋升（你拍板） |
| `analyze` | `references/analyze.md` | 体检宫殿 → 优化建议 |

## 执行约定（每次先做）

1. **认子命令**：取第一个参数当子命令；缺省/`help` 走 concept。
2. **定 `<SKILL_DIR>`**：本 skill 自己的目录（`scripts/mp.py`、`assets/` 都相对它）。
3. **定 `<VAULT>`**：grep `~/.claude/CLAUDE.md` 或 `~/.codex/AGENTS.md` 里的「记忆宫殿/MemoryPalace」路径拿到 vault 绝对路径；
   - 拿不到且子命令是 `init` → 正常（init 就是来建它的）。
   - 拿不到且子命令不是 `init` → 问用户 vault 在哪，或建议先 `init`。
4. **读对应 `references/<子命令>.md` 并严格按它执行。**

## 引擎 `scripts/mp.py`（也可脱离 skill 当 CLI 用）

`mp.py <init|distill|promote|analyze|link> --vault <路径> [选项]`，仅标准库（Python ≥ 3.11）。
打分/去重/晋升门**全是确定性规则**，LLM 只负责「抽候选」——记忆永不被模型幻觉污染。

## 设计哲学（吸收自）

Karpathy「Obsidian 当 AI 共享大脑」骨架 · OpenClaw 的 Dreaming 六维加权蒸馏 · Hermes 的 extraction pass / skill 即程序记忆 · open-second-brain 的「内核不调 LLM」确定性晋升 + 一 vault 多运行时 · mem0 的 ADD/UPDATE/NOOP 写回。详见 `assets/explainer.html`。

## 纪律（跨所有子命令）

- **skill = 工具（零个人数据），vault = 数据（用户私有）**。本 skill 里绝无任何具体个人信息。
- 改用户全局配置（CLAUDE.md/AGENTS.md）或删除/合并记忆前**必须确认**。
- **绝不**把密钥/凭据写进 vault。
- `00-RULES/` 是用户最高法律，只能经飞轮 + 用户审批晋升，agent 不直接写。
