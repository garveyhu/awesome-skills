# SpecHub Git 工作流

通过 git worktree 管理多项目规约的检出、阅读、更新、推送。

---

## 仓库路径解析

所有操作都在 SpecHub 仓库内进行。使用前先确定仓库绝对路径：

1. **用户显式指定**：用户本次调用带了路径参数，以用户指定为准。
2. **默认配置**：读取 `~/.agents/path.json` 的 `spechub` 字段。

```bash
SPECHUB=$(jq -r '.spechub' ~/.agents/path.json)
# 或者用户手动指定：
# SPECHUB=/path/to/spechub
```

若读取失败或字段为空，提示用户在 `~/.agents/path.json` 配置 `spechub` 字段，或本次显式指定路径。

下文命令统一使用 `$SPECHUB` 指代仓库根目录。

---

## 识别 SpecHub 仓库

进入 `$SPECHUB` 后通过以下信号确认（至少匹配两项）：

```bash
grep -q '^specs/' "$SPECHUB/.gitignore" 2>/dev/null                    # .gitignore 包含 specs/
ls "$SPECHUB/specs/" 2>/dev/null                                        # specs/ 目录存在
git -C "$SPECHUB" branch -r | grep 'feature/' 2>/dev/null               # 有远程 feature 分支
git -C "$SPECHUB" branch --show-current | grep '^feature/' 2>/dev/null  # 当前在 feature 分支上
```

---

## 操作指南

### 首次配置

```bash
git -C "$SPECHUB" fetch --all
git -C "$SPECHUB" branch -r | grep 'feature/'          # 查看可用项目
git -C "$SPECHUB" worktree add specs/<project> feature/<project>
```

### 首次阅读规约（消费方）

首次对接时，按全量顺序阅读：

1. 拉取最新：`git -C "$SPECHUB/specs/<project>" pull`
2. 按顺序阅读：README → 01-总览 → 02-详细说明，逐模块
3. 每个模块的 README 说明覆盖范围，先看它再深入细节

### 增量阅读更新（消费方）

已完成首轮实现后，后续更新采用增量模式：

1. 拉取：`git -C "$SPECHUB/specs/<project>" pull`
2. **先只读 CHANGELOG.md**（项目根目录和各模块目录下的），从最新条目读到上次处理过的为止
3. 按"消费方需要做什么"和"涉及文件和章节"，只读对应变更部分
4. 完成增量修改

辅助确认变更内容：
```bash
git -C "$SPECHUB/specs/<project>" log --oneline -5
git -C "$SPECHUB/specs/<project>" diff HEAD~1
```

### 更新并推送规约（生产方）

每次更新规约时，必须同步维护 CHANGELOG.md：

```bash
cd "$SPECHUB/specs/<project>"
# 1. 修改规约文档
# 2. 在对应模块和项目根目录的 CHANGELOG.md 添加新条目
# 3. 结构化 commit
git add .
git commit -m "<变更类型>(<模块>): <简述>"
git push
```

推送后提醒用户通知消费方拉取更新。

### 新建项目分支

```bash
cd "$SPECHUB"
git checkout main
git checkout -b feature/<project-name>
rm README.md
printf '.DS_Store\nspecs/\n' > .gitignore   # specs/ 必须忽略，防止 worktree 目录被提交
# 按对应模板创建规约目录和文档
git add .
git commit -m "<project> 规约文档"
git push -u origin feature/<project-name>
git checkout main
```

> **重要：** feature 分支的 `.gitignore` 必须包含 `specs/`。因为本仓库通过 worktree 将其他 feature 分支检出到 `specs/` 目录下，如果不忽略，`git add -A` 会把其他项目的 worktree 目录误提交到当前分支。

如有需要，更新 main 分支 README 中的项目列表。

### 从外部目录同步

当规约源文件在仓库外时：

```bash
rsync -av --include='*.md' --exclude='.*' --exclude='*.zip' --exclude='*.png' \
  <源路径>/ "$SPECHUB/specs/<project>/<模块>/"
```

---

## 常见错误

| 错误 | 后果 | 正确做法 |
|------|------|---------|
| 阅读前不拉取 | AI 基于过期规约实现 | 每次阅读前先 `git pull` |
| 在错误分支提交 | 规约跑到 main 上 | `cd specs/<project>` 并确认分支 |
| 推送后不通知 | 消费方继续用旧文档 | 推送后提醒通知对方 |
| 更新文档不更新 CHANGELOG | 消费方被迫全量重读 | 每次修改必须同步写 CHANGELOG |
| 缺少示例 | AI 猜测格式 | 每个规约项都需要完整示例 |
