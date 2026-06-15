# awesome-skills

[English](./README.md) · **简体中文**

> 我自己打磨的 Agent Skill 与工作流合集 —— 把在真实项目里反复验证的**工程规约**与**创作流程**，固化成 [Claude Code](https://claude.com/claude-code) 等 agent 可直接调用的能力。

每个 skill 都不是泛泛的「通用助手」，而是带着明确立场：我的技术栈约定、我的审美底线、我的协作范式。描述需求即可，skill 负责架构决策、样板、规范与交付——少走弯路，也不糊弄。

---

## 技术栈脚手架

| skill | 做什么 |
|---|---|
| **react-best-practices** | React 工程规约与脚手架：yarn + Vite + TS + Antd + Tailwind，含分层 / 命名 / lint 全家桶，初始化、开发、评审一条龙 |
| **fastapi-best-practices** | FastAPI 后端规约：uv + SQLAlchemy + Alembic + loguru + ruff，MVC 分层、统一响应封装、GET+POST 约定 |
| **docker-best-practices** | 容器化标准件：三区布局（images / containers / scripts）、多镜像拆分、多架构 buildx、registry 与离线 tar 双投递 |
| **website-creator** | 从零起一个网站 / 应用：苏格拉底式追问到需求 95% 确定，再按前端 / 全栈自动落脚手架 |

## 文档与知识

| skill | 做什么 |
|---|---|
| **wiki-creator** | 深扫项目生成 DeepWiki 式多文件文档（中文 + Mermaid，配 Docsify 直接可读） |
| **docsify-station-creator** | 把 `docs/` 一键变成功能完整的 Docsify 站（暗色 / 全文搜索 / TOC / Mermaid / 可选动画模式） |
| **req-to-ai-spec** | 把零散需求（文字 / 截图 / 旧代码）转成结构化、AI 友好的需求规格，交给编码 agent 直接开干 |
| **spechub-best-practices** | 写高质量交接规约、用 git worktree 管理，专为 AI 之间的任务交接 |
| **notion-chat-archiver** | 把一次 AI 对话总结归档进 Notion 对话录库（带主题 / 要点 / 标签等元数据） |
| **solution-vault** | 个人方案库：把验证过的技术方案（OAuth、文件上传、支付…）跨项目复刻 |

## 可视化

| skill | 做什么 |
|---|---|
| **html-diagram** | 从风格库选「脸」，把架构图 / 链路图 / 时间线渲染成自包含的单文件 HTML |

## 设计与风格

| skill | 做什么 |
|---|---|
| **style-vault** | 六层（产品 / 风格 / 页 / 块 / 组件 / token）个人风格库，按我的审美偏好生成前端 |
| **style-vault-sediment** | 配套写入器：把新风格沉淀进 style-vault，按作者版本化记录 |

## 图像与视频

| skill | 做什么 |
|---|---|
| **comfyui** | 自然语言驱动本地 ComfyUI 出图 / 出视频，自动搭 workflow，模型无关、Apple Silicon 调优 |
| **codex-image-gen** | 用 Codex（gpt-image-2）出图 / 改图，支持参考图锁定角色与风格 |
| **browser-gen** | 驱动已登录的 Gemini 网页免费生图 / 生视频（Veo 视频 · Nano Banana 出图） |
| **links-illustrations** | 「小黑」IP 的怪诞手绘风中文正文配图，给文章 / 文档配图 |
| **jimeng** | 即梦 / Dreamina 出图通道 |

## 方法论

| skill | 做什么 |
|---|---|
| **skill-management** | 我管理 skill 的方法论本身：把大量 skill 按「来源 → 分类 → skill」三级组织、单一 `registry` 驱动、跨 Claude Code 与 Codex 复用，自带工具。**别人的 AI 读完即可复刻同一套** |
| **self-improving-workflow** | 通用方法论：4 个评审子 agent 协同学习 + `/run` 单入口长任务自主执行 |

---

## 用法

这些 skill 遵循 [Claude Code Agent Skills](https://docs.claude.com/en/docs/claude-code/skills) 规范。

```bash
git clone https://github.com/garveyhu/awesome-skills.git

# 把需要的 skill 软链到 Claude Code 的 skill 目录（按需挑，不必全装）
ln -s "$PWD/awesome-skills/stack/react-best-practices" ~/.claude/skills/
ln -s "$PWD/awesome-skills/media/comfyui"              ~/.claude/skills/
```

装好后在对话里用自然语言触发，或 `/<skill-name>` 显式调用。

## 共同底色

- **单一职责 / 高可扩展 / 高可维护**：宁可多拆一层，不把多个职责塞进一个文件。
- **反「AI 味」**：审美产出先定一张「脸」、冻结 design token、只造一个记忆点，其余克制留白。
- **约定优先**：后端 GET + POST、统一响应封装；前端原子化样式、严格类型。
- **中文优先**：注释、文档、产出默认中文。

> 这是一份**精选、带个人立场**的合集——只收录我原创的 skill。欢迎取用、借鉴，也欢迎提 issue 交流。
