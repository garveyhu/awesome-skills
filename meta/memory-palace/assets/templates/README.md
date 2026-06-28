---
title: 记忆宫殿 · 导览
type: readme
---

# 🧠 我的记忆宫殿（Memory Palace）

> 一座**平台无关**的第二大脑：关于「我是谁 / 我的项目 / 我的偏好 / 我的决策」的记忆都在这里，
> 用纯 Markdown 存——**可见、可改、可带走**。不管 AI 工具怎么换，大脑是我自己的资产。

机器读的契约在 [[PROTOCOL]]（**唯一入口**）；这篇给人看。

## 五层结构（按生命周期切，互不重叠）

| 层 | 装什么 | 谁能写 |
|----|--------|--------|
| `00-RULES/` | **身份层**：我是谁、沟通风格、禁用词、跨领域铁律。最高法律 | 只能晋升 + 我审批 |
| `01-PROJECTS/` | **项目层**：每项目一目录，内分 `decisions`+`feedback`；支持多级嵌套 | agent 可直接写 |
| `02-SOURCES/` | **资料层**：爬回来的文章 / 工具 / 文档 | agent / 插件 |
| `03-MAPS/` | **图层**：流程图 / 决策树 / 架构 | agent / 我 |
| `04-FEEDBACK/` | **飞轮中枢**：每日 journal + 蒸馏候选 + 留痕 DREAMS | 引擎 + 我审批 |

## 怎么用（`/memory-palace` skill）

| 命令 | 干什么 |
|------|--------|
| `/memory-palace help` | 看原理讲解页 |
| `/memory-palace interview` | 深度访谈，建立 / 充实我的身份记忆 |
| `/memory-palace extract` | 从本地 Claude/Codex 规则·会话导入记忆 |
| `/memory-palace distill` | 蒸馏出候选（飞轮·出草稿） |
| `/memory-palace review` | 审批候选 → 晋升（飞轮·我拍板） |
| `/memory-palace analyze` | 体检宫殿 → 优化建议 |

## 越用越懂我（飞轮）

工作中的纠正/决策/偏好落进 `04-FEEDBACK/journal/` → 夜间蒸馏六维加权打分出候选（**不直接改 00-RULES**）→ 我审批晋升 → 下次任何 agent 上来先读 `00-RULES` + grep vault。**升级一次，全工具不再犯同样的错。**

## 备份

建议装 **Obsidian Git** 自动 commit，或自己 `git` 托管——记忆有历史、可回滚。
