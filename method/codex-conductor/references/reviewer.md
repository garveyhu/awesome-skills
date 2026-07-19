# reviewer · 对抗评审

## 何时选

每个波次收尾必过；合并进主分支前；涉安全边界（权限 / 沙箱 / 注入面）的改动。

## 通道（二选一）

**① 首选 companion 评审通道**（主线程直调，不经 rescue agent）：

```bash
COMPANION=$(ls -d ~/.claude/plugins/cache/openai-codex/codex/*/scripts/codex-companion.mjs | tail -1)
node "$COMPANION" review --base <ref> [--background]          # 常规评审
node "$COMPANION" adversarial-review --base <ref> [焦点文本]   # 对抗评审：专找反例
```

**② 或只读 task**：模型默认档 / `--effort high`，不带 `--write`，姿态写进任务书 = 专找反例、按严重度排序、每条给复现路径。

## 任务书骨架（走 task 时）

1. **评审范围**：分支 / 提交区间 / 文件清单
2. **关注维度**：正确性 / 安全 / 性能 / 契约一致——点名本次重点
3. **产出格式**：按严重度排序的 findings，每条带 file:line + 失败场景 + 修复建议

## 姿态要点

- **永不给写权限**——评审官不动手
- findings 是输入不是判决：Claude 逐条独立核实真伪（防幻觉 finding）再决定修不修
- 评审后**不许自动修**——哪些要修，由用户 / Claude 决策后另派 [builder](builder.md) / [coder](coder.md)

## 验收衔接

每条确认为真的 finding 转成修复任务；确认为假的记录理由，别静默丢弃。
