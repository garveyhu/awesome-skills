# extract — 从本地 agent 平台导入已有记忆

目标：把用户**已经散落在各 AI 工具里**的规则、偏好、决策一次性导入宫殿——不用从零访谈。

## 两个来源

### A. 显式配置（最高信号，先做）

读用户已写死的规则/指令，提炼成结构化记忆候选：
- Claude：`~/.claude/CLAUDE.md`、`~/.claude/rules/*.md`、`~/.claude/commands/*.md`
- Codex：`~/.codex/AGENTS.md`
- Gemini/其它：对应入口文件
- 项目级：各仓库的 `CLAUDE.md` / `AGENTS.md`

对每份：判断它是**身份/偏好/铁律/工程规范**哪类，提议落点：
- 跨领域的「我是谁/我怎么沟通/我的默认」→ `00-RULES/*`
- 反复出现的铁律 → `00-RULES/_principles/`
- 工程规范（react/python…）→ 若想中央集权，搬进 `00-RULES/rules/` 并软链回去（见 `mp.py link`），否则只在 preferences 里指过去
- **逐条复述 + 用户确认**后再写。**绝不**把密钥/凭据搬进 vault。

### B. 会话历史（行为信号）

```bash
<SKILL_DIR>/scripts/mp.py distill --vault <VAULT> --bootstrap
```
`--bootstrap` 全量扫历史会话（不止近几天），抽出反复出现的纠正/偏好 → 写进 `candidates.md`。然后走 `/memory-palace review` 审批晋升。

## 流程

1. 先 A（显式配置）：读 → 分类 → 提议 → 用户确认 → 写对应文件。
2. 再 B（会话历史）：`distill --bootstrap` → `review`。
3. 收尾：建议接着 `/memory-palace interview` 补 A/B 没覆盖到的身份盲区（如「品味/反模式」往往没写在配置里、得问）。

## 纪律
- 显式配置是高置信来源，`confidence` 可给 high；会话抽取走飞轮的确定性门。
- 改/搬任何用户文件前确认；密钥绝不入库。
