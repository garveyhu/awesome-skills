<!-- [English](README.md) · [中文](README.zh-CN.md) -->

# 🧠 记忆宫殿 Memory Palace

> 一套平台无关的个人记忆系统。一座本地 Obsidian vault（纯 Markdown），让 Claude Code / Codex /
> Gemini / 任何 CLI **共读共写**——每个 AI agent 都越用越懂**你**。记忆**可见、可改、可带走**，
> 不被任何厂商的黑箱锁死。

本 skill 引导任何人搭建、充实、维护自己的记忆宫殿。vault 是你的私有数据，skill 是通用工具（零个人信息）。

## 子命令

| 命令 | 干什么 |
|------|--------|
| `/memory-palace help` | 打开原理讲解页（自包含 HTML）+ 菜单 |
| `/memory-palace init` | 脚手架一座空宫殿（五层 + 契约）+ 接上各 AI 工具 |
| `/memory-palace interview` | 深度访谈，把「你是谁」问出来、变成记忆（挖掘深） |
| `/memory-palace extract` | 从本地 Claude/Codex 的规则·会话导入已有记忆 |
| `/memory-palace distill` | 蒸馏最近会话 → 出候选草稿（飞轮） |
| `/memory-palace review` | 审批候选 → 晋升进宫殿（你拍板） |
| `/memory-palace analyze` | 体检宫殿 → 可执行的整理优化建议 |

## 五层结构

`00-RULES` 身份 & 铁律（你审批）· `01-PROJECTS` 每项目决定+打回（可多级嵌套）·
`02-SOURCES` 剪藏 · `03-MAPS` 图 · `04-FEEDBACK` 飞轮（journal → candidates → DREAMS）。

## 怎么越用越懂你（飞轮）

纠正/决策/偏好落进 `04-FEEDBACK/journal/` → `mp.py distill` 扫本地 agent 会话，**六维加权打分**出候选
（绝不动 `00-RULES`）→ 你 `review` 审批 → 下次任何 agent 先读 `00-RULES` + grep vault。
**升级一次，所有工具不再犯同样的错。**

核心哲学：LLM 只负责「抽候选」；打分、去重、晋升门**全是确定性规则**——记忆永不被模型幻觉污染。

## 引擎 `scripts/mp.py`

零依赖 CLI（Python ≥ 3.11），也能脱离 skill 单独用：
`mp.py <init|distill|promote|analyze|link> --vault <路径>`。

## 思想来源

Karpathy「Obsidian 当 AI 共享大脑」· OpenClaw 的 Dreaming 蒸馏 · Hermes 的 extraction-pass &
skill 即程序记忆 · open-second-brain 的「内核不调 LLM」确定性晋升 · mem0 的 ADD/UPDATE/NOOP 写回。
详见 `assets/explainer.html`。
