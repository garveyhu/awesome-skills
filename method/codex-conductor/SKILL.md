---
name: codex-conductor
description: 「Claude 当大脑、Codex 当手」的委派工作流——把实现类任务经 codex:codex-rescue agent 派给本机 Codex CLI，Claude 负责拆任务、写任务书、独立验收、合并提交。用户说「派 codex / 让 codex 干 / codex 实现」，或有成批实现任务需要委派时用。
---

# Codex Conductor（Claude 指挥 · Codex 实干）

把「Claude 编排 + Codex 实现」跑成稳定流水线的工作流。从一场真实战役（MediaStudio 插件体系 9 个工作包全部由 Codex 实现、Claude 验收合并）沉淀而来。

## 分工铁律

- **Claude（大脑）**：拆解需求 → 写任务书 → 派发 → **独立验收** → 亲自 commit / merge。
- **Codex（手）**：只按任务书实现，不参与验收自己的活。
- **验收权不下放**：Codex 的完工报告一律不作数——以 Claude 亲自跑出的验证门（build / test / lint 全绿）+ 逐提交 diff 审查为准。

## 前提

- 本机装有 openai-codex 插件（提供 `codex:codex-rescue` agent）+ codex CLI 已登录（`codex login status`）。
- 没配好时引导用户跑 `/codex:setup`，不要自造 auth 流程。

## 派发方式

用 Agent 工具派 `codex:codex-rescue`，任务书写进 prompt，路由旋钮附在末尾：

```
Agent(subagent_type: "codex:codex-rescue",
      prompt: "<任务书> --write --background",
      run_in_background: false)
```

| 旋钮（写在 prompt 里） | 何时用 |
|---|---|
| `--write` | 要改文件就带上（纯诊断 / 评审 / 调研不带 = 只读） |
| `--background` | 长任务让 Codex 后台跑，subagent 秒回 job-id，Claude 腾出手干别的 |
| `--resume` | 续上一个 Codex 会话（「继续 / 修掉刚才那个问题 / 再深挖」） |
| `--model spark` | 机械杂活降档提速 |
| `--effort high` | 最难啃的调试 / 设计升档 |

**模型与推理强度默认一律不传**——继承用户 `~/.codex/config.toml` 里设好的慣用型号与强度；用户改习惯只动 config 一处，skill 与 prompt 永不硬编码型号。

长任务两种等法（选一）：prompt 带 `--background` 后用下方 companion 轮询；或 Agent 调用本身 `run_in_background: true`，等 harness 通知。

## 任务书写法（实战沉淀）

1. **开头给锚**：仓库绝对路径、当前分支、必读文档（工程宪法 / 设计规范 / 契约文档的具体路径）。
2. **交付定义 + done-gate**：明确列「跑什么命令、什么算绿」。测试**攒一大批一起跑**，别让 Codex 每小步都测（会拖拉）。
3. **多任务并成波次**：一份大任务书列 N 个子任务、让 Codex 自排顺序，好过 N 次零碎派发。
4. **提交规矩写进任务书**：Angular commitlint（type 英文小写、subject 不许大写字母开头）、一任务一提交、scope 用包名。
5. **长写盘任务令其自开 worktree 干**，严禁在主目录切分支——真实事故：Codex 中途切走主目录分支，Claude 的提交落到错误分支上。
6. 项目有「用户把关门」（需要用户肉眼确认的节点）时，在任务书里标明停点。

## 验收协议（每波必做）

1. Codex 报完工 → Claude **亲自**跑 done-gate（turbo / test / lint），全绿才算数。
2. `git log` + `git show` 逐提交审查：范围有没有越界、有没有夹带无关文件（lint-staged 失败会把文件留在暂存区，最易夹带）。
3. Codex 在 worktree 干的 → Claude 亲自 merge 回主分支；**提交前先 `git branch --show-current` 确认所在分支**。
4. 有疑点：派 `/codex:review` 或 `/codex:adversarial-review` 交叉审，或 `--resume` 打回让 Codex 重修。

## 后台任务管理

主线程直接查 companion（路径含插件版本号会变，动态解析）：

```bash
COMPANION=$(ls -d ~/.claude/plugins/cache/openai-codex/codex/*/scripts/codex-companion.mjs | tail -1)
node "$COMPANION" status --all      # 看全部任务
node "$COMPANION" result <job-id>   # 取某任务结果
node "$COMPANION" cancel <job-id>   # 取消
```

## 禁止

- ❌ 把 Codex 的完工报告当验收结果直接汇报给用户（必须亲验）
- ❌ Codex 后台写盘期间在同一目录做 git 操作（commit / checkout / merge）
- ❌ prompt 里硬编码模型型号（默认档一律继承用户 config）
- ❌ 几分钟能干完的小活也派 Codex（自己干更快）
- ❌ 替用户 push（对外操作，先确认）
