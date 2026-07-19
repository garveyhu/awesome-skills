# builder · 主力实现

## 何时选

核心功能、成批工作包（WP 波次）、跨包重构——需要理解架构、做设计判断的实现。

不选：规格完全明确、照施工图写就行（→ coder）；纯机械搬运（→ chore）。

## 旋钮

- 模型 / effort：**默认档**（继承 `~/.codex/config.toml`），一律不传参
- `--write` 必带；预计超十分钟或多任务波次加 `--background`
- 长写盘任务：任务书里令其**自开 worktree**

```
Agent(subagent_type: "codex:codex-rescue",
      prompt: "<任务书> --write --background")
```

## 任务书骨架

1. **锚**：仓库绝对路径、当前分支、必读文档路径（工程宪法 / 设计规范 / 契约文档）
2. **子任务清单**：N 个子任务 + 依赖关系，令其自排顺序（一份大任务书好过 N 次零碎派发）
3. **边界**：哪些文件 / 包可动、哪些是禁区（共享文件写明归属，防并行冲突）
4. **done-gate**：跑什么命令、什么算绿；测试**攒一大批一起跑**，别每小步都测
5. **提交规矩**：Angular commitlint（type 英文小写、subject 不许大写字母开头）、一任务一提交、scope 用包名
6. **worktree 指令**：`git worktree add ../<名> -b codex/<名>`，全程不许动主目录分支
7. **停点**：项目有「用户把关门」节点时写明「做到这停下、报告、等指令」

## 姿态要点

- 大波次先让它**复述任务理解 / 输出 plan** 再动手，防跑偏
- 遇阻不钻牛角尖：记 issue、报告、继续其他子任务

## 验收衔接

Claude 亲自跑 done-gate + 逐提交 `git show` 审查；波次收尾必转 [reviewer](reviewer.md) 交叉审。
