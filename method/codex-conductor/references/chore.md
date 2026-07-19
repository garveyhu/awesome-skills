# chore · 机械杂役

## 何时选

不需要理解代码语义的批量操作：改名、搬文件、格式化、批量替换、依赖版本跑腿、生成样板清单。

不选：需要理解代码再改（→ coder / builder）。

## 旋钮

- `--model spark --effort low`（极速档）
- `--write`；通常前台等（快，不值得后台）

```
Agent(subagent_type: "codex:codex-rescue",
      prompt: "<短指令> --write --model spark --effort low")
```

## 任务书骨架

- 一段短指令：动哪些文件（glob / 清单点名）、做什么变换、**不许碰什么**
- 自查命令：动完跑哪条命令确认没砸（grep 计数 / lint / build）

## 姿态要点

- 边界要硬——只许动点名的文件；宁可拆成多次小 chore，也不给宽泛授权

## 验收衔接

自查命令结果 + `git diff --stat` 扫一眼范围没越界。
