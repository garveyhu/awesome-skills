# init — 搭建基础架构

目标：为新用户脚手架一座可用的空宫殿，并把各 AI 工具接上它。

## 步骤

1. **定位置**：问用户宫殿建哪（默认建议 `~/Documents/obsidian/MemoryPalace`，作为独立 Obsidian vault）。确认是空目录或可新建。

2. **脚手架**：
   ```bash
   <SKILL_DIR>/scripts/mp.py init --vault <用户选的路径> --git
   ```
   （`--git` 可选；它会拷五层模板 + PROTOCOL + README + `.mp/config.toml` + 首个 journal。）

3. **接上各 AI 工具**（适配 stub，**改用户全局配置前先征得同意**，逐个确认）：
   - Claude Code：把 `<SKILL_DIR>/assets/stubs/claude-section.md` 的内容（把 `<VAULT>` 换成真实绝对路径）**追加到** `~/.claude/CLAUDE.md` 顶部。
   - Codex：同理把 `assets/stubs/AGENTS.md` 追加到 `~/.codex/AGENTS.md`。
   - Gemini/其它：`assets/stubs/GEMINI.md` 追加到对应入口文件。
   - 要点：stub 只是 5 行指针，指向 `<VAULT>/PROTOCOL.md`；换工具只改这一处。

4. **配 LLM provider**：看 `<VAULT>/.mp/config.toml` 的 `[llm]`，问用户本机装了哪些 CLI（claude/codex/gemini/agy），把 `provider` 设成额度宽、可用的那个，`fallback` 填其余。`mp.py distill --vault <路径> --shadow --no-llm` 先验证脚手架能跑。

5. **建议备份**：装 Obsidian Git 插件或自建 git 仓库（记忆要有历史、可回滚）。提醒：**绝不把密钥写进 vault**。

6. **收尾**：告诉用户下一步——`/memory-palace interview`（从零问出身份）或 `/memory-palace extract`（从已有 agent 配置导入）。

## 纪律
- 改用户全局配置（CLAUDE.md/AGENTS.md）前必须确认。
- 不替用户填身份内容——那是 interview/extract 的事。
