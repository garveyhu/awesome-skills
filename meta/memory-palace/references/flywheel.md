# distill / review — 飞轮（蒸馏 + 审批）

「越用越懂你」的闭环。`distill` 出草稿，`review` 你审批晋升。两步分离——LLM 抽候选、确定性规则打分、**人审批才进永久记忆**。

## distill（蒸馏出草稿）

1. 跑：`<SKILL_DIR>/scripts/mp.py distill --vault <VAULT>`
   - `--shadow` 只预览不落盘；`--no-llm` 纯启发式（离线、不外发会话）；`--days N` 改扫描窗口。
   - 它扫 `journal/` + 本地 Claude/Codex 会话 → 六维加权打分 → 达标的写进 `04-FEEDBACK/candidates.md`，**绝不动 00-RULES**。
2. 把结果摘要念给用户（扫了多少、出了几条候选）。

## review（你审批 → 晋升）

1. 读 `<VAULT>/04-FEEDBACK/candidates.md`，把**未处理**（`- [ ]` 且带 `<!--cand`）的候选逐条列给用户，每条给：陈述、建议落点 `dest`、`action`、`freq`、`score`、`conf`、证据，加你**一句话建议**（值不值得记、放得对不对）。
2. 按用户决定改 `candidates.md`：
   - 通过 → `- [ ]` 改 `- [x]`（保留 `<!--cand ...-->` 注释别动）。
   - 暂缓 → 留 `- [ ]`。
   - 否决 → 删整条。
   - 落点不对 → 改注释里的 `"dest"`（支持多级 `01-PROJECTS/父/子/decisions.md`）再勾。
3. 落地：`<SKILL_DIR>/scripts/mp.py promote --vault <VAULT> --commit`（先 `--dry-run` 看一眼）。
4. 复述：晋升几条、落哪、git 是否提交。提示 `DREAMS.md` 有留痕、可回滚。

## 自动化（可选）
夜间 cron 自动出草稿，用户白天只 review：
```
0 3 * * * <SKILL_DIR>/scripts/mp.py distill --vault <VAULT>
```
（cron 精简 PATH，建议把 config 里 provider 的 command 改绝对路径；无登录态时用 `--no-llm`。）

## 纪律
- 只执行用户勾选的，**绝不替用户决定记什么**。
- 晋升进 `00-RULES/` 的是用户最高法律，拿不准让其二次确认。
