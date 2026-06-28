---
title: 04-FEEDBACK · 飞轮中枢
type: readme
---

# 04-FEEDBACK · 越用越懂你的飞轮

> 最有用的不是记录对话，而是**升级迭代**。升级一次，所有 agent 都不再犯同样的错。

## 三件套

| 文件/目录 | 角色 | 谁写 |
|-----------|------|------|
| `journal/YYYY-MM-DD.md` | **原始层**：每日观察、纠正、决策、会话小结（append-only） | agent / 我随手记 |
| `candidates.md` | **晋升队列**：蒸馏出的候选，带证据计数 + 六维分 + 建议落点 | `mp.py distill` 自动写 |
| `DREAMS.md` | **梦境日记**：每次蒸馏/晋升做了什么，可复查、可回滚 | 引擎 + `mp.py promote` |

## 飞轮怎么转

1. **捕获** → 落 `journal/`（前缀 `决策:`/`偏好:`/`纠正:`/`观察:`）。
2. **蒸馏** → `mp.py distill` 扫 journal + 本地 agent 会话，**六维加权打分**，达标的写进 `candidates.md`。**绝不直接改 00-RULES。**
3. **审批** → `/memory-palace review`（或 `mp.py promote`），勾选通过的晋升到 00-RULES / 项目，留痕 `DREAMS.md`。
4. **注入** → 任何 agent 下次读 `00-RULES` + grep vault 即受益。
