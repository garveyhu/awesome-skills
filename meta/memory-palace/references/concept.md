# help — 概念引导

目标：让第一次接触的人 1 分钟内理解「记忆宫殿是什么、为什么、怎么用」。

## 步骤

1. **打开讲解页**（自包含 HTML，离线可看）：
   - macOS：`open "<SKILL_DIR>/assets/explainer.html"`
   - 其它/无 GUI：把绝对路径告诉用户，让 TA 自己浏览器打开。
   - 同时一句话概括：**记忆宫殿 = 一座平台无关的 Obsidian vault，用纯 markdown 存「你是谁/你的项目/偏好/决策」，让 Claude/Codex/任何 CLI 共读共写、越用越懂你；记忆可见、可改、可带走，不被厂商锁死。**

2. **列子命令菜单**（告诉用户接下来能干什么）：

   | 命令 | 干什么 |
   |------|--------|
   | `/memory-palace init` | 搭一座自己的空宫殿（脚手架五层 + 契约 + 适配 stub） |
   | `/memory-palace interview` | 深度访谈，把「你是谁」问出来、建立身份记忆 |
   | `/memory-palace extract` | 从本地 Claude/Codex 的规则·会话里导入已有记忆 |
   | `/memory-palace distill` | 蒸馏最近会话 → 出候选草稿（飞轮） |
   | `/memory-palace review` | 审批候选 → 晋升进宫殿（飞轮·你拍板） |
   | `/memory-palace analyze` | 体检宫殿 → 给整理优化建议 |

3. 问用户想从哪开始（新用户→`init`；已有宫殿→`interview`/`extract`/`analyze`）。

## 纪律
- 只读不写。这是认知引导，不改任何文件。
