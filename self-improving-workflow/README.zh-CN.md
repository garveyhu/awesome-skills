# self-improving-workflow

> 给任意项目装上一套**会自我学习**的项目级 Claude Code 工作流。三档分级：从单人脚本到政府级系统。新老项目都能装，**绝不覆盖**你已有的文件。

> English version: [README.md](README.md)

## 为什么需要这个

每个稍有规模的项目都在重新发明同一套 `.claude/` 配置：`CLAUDE.md`、rules、slash 命令、评审 agent、记忆库。每个团队都在重新踩同样的坑：业务逻辑写完才想起补事件骨架、多 Agent 并行互相覆盖、评审时才发现需求漏了一半。

这个 skill 把那些教训编码成**三档脚手架** + **持续改进闭环**：

- **初始化** — `/init-workflow` 问 4 个问题，按项目规模生成对应的 `.claude/` 结构
- **阶段协议** — `/phase-start` 和 `/phase-review` 给纪律但不重流程
- **自我改进** — `/self-improve` 抓本次会话的教训，**经你确认后**沉淀到团队共享的规则文件
- **非破坏性** — 老项目装它 100% 安全，永远不覆盖已有文件

## 三档对比

| 档位 | 文件数 | 适用 |
|------|--------|------|
| **minimal** | 6 | 单人脚本、临时实验。只装一个 `/self-improve` 按钮沉淀教训 |
| **standard** | 13 | 2-5 人中型业务项目。含阶段协议 + 1 个评审 agent + 编码禁令 |
| **full** | 19 | 团队 / 大型 / 合规级项目。3 个并行评审 agent + 合规预设 |

完整文件清单见 [`references/tier-comparison.md`](references/tier-comparison.md)。

## 快速开始

### 新项目

```
/init-workflow
```

回答 4 个问题 → 装上推荐档位 → 30 秒搞定。

### 老项目（已有 CLAUDE.md 或 .claude/）

```
/init-workflow minimal
```

`minimal` 是最安全的入口。已存在的文件全部跳过，绝不覆盖。你的 `CLAUDE.md` 不动，但会写一个 `.skill-template` 旁置文件供参考。详情见 [`references/existing-project-guide.md`](references/existing-project-guide.md)。

### 沉淀一条教训

```
/self-improve

> Q1：本次会话学到了什么？
> A：跨模块 Autowire 导致循环依赖，本周已发生 3 次

> Q2：类别？(workflow / coding / module / compliance / other)
> A：module

> Q3：是否写进 dev-lessons.md 作为永久规则？(y/n)
> A：y

✓ 已追加到 .claude/rules/dev-lessons.md
```

### 升档

```
/upgrade-workflow standard   # minimal → standard
/upgrade-workflow full       # 任意档位 → full
```

对内容有差异的同名文件，会触发交互提示 `[k]eep / [n]ew / [d]iff / [s]kip`。控制权在你。

## Slash 命令

| 命令 | 档位 | 作用 |
|------|------|------|
| `/init-workflow [tier]` | 全档 | 交互式问答 + 脚手架。自动探测已有文件 |
| `/upgrade-workflow <target>` | 全档 | 升档。冲突时 diff 提示 |
| `/self-improve [scope]` | 全档 | 沉淀本会话教训到 `dev-lessons.md` |
| `/phase-start <name>` | standard+ | 阶段启动协议 |
| `/phase-review <name>` | standard+ | 阶段完成协议（含评审 agent + 自动 `/self-improve`） |
| `/compile-check` | full | 全模块按依赖编译验证 |

## 核心设计原则

1. **Write-once 原则**：永不覆盖。已存在文件跳过，可选写 `.skill-template` 旁置
2. **写规则前必须用户确认**：`/self-improve` 只**提议**，等你 yes/no，才动 `.claude/rules/`
3. **三档分级**：脚本不用为团队仪式买单，团队项目也不用重复发明
4. **老项目零侵入**：检测到 `.gitignore` 冲突时**警告而非破坏性 patch**
5. **`charon-fan/agent-playbook@self-improving-agent` 弱依赖**：装了就用其完整记忆引擎，没装就走 fallback 三问模式
6. **纯 bash 脚本**：零运行时依赖，macOS + Linux 原生

## 目录结构

```
self-improving-workflow/
├── SKILL.md                    # 入口：触发词 + 锚点钩子
├── README.md / README.zh-CN.md # 双语用户文档
├── templates/
│   ├── minimal/                # 4 个模板文件
│   ├── standard/               # +7 个增量文件
│   └── full/                   # +5 个增量文件
├── scripts/
│   ├── init.sh                 # /init-workflow 实际执行
│   ├── upgrade.sh              # /upgrade-workflow 实际执行
│   └── detect.sh               # 项目体征探测
└── references/
    ├── tier-comparison.md      # 功能矩阵
    ├── existing-project-guide.md
    └── compliance-presets.md   # govt / fintech / healthcare / privacy
```

## 文件所有权模型

跟 `cookiecutter` / `yeoman` / `create-react-app eject` 一样：**write-once，用户永久所有**。

- 初始化绝不覆盖已存在文件
- 升档遇冲突 prompt 提示，绝不静默覆盖
- 用户对脚手架文件的修改神圣不可侵犯
- skill 自身的版本管理在 `garveyhu/awesome-skills` 仓库里，不存在每个项目里

## 合规预设

`full` 档为 `domain-compliance.md` 提供 4 个预设：

- **govt（政府/公共部门）** — 审计、隔离、加密、状态机、审批走流程
- **fintech（金融/支付）** — 幂等键、Decimal 算术、不可变日志、双人审核
- **healthcare（医疗）** — PHI 加密、访问日志、紧急破窗访问
- **privacy（个人信息保护）** — GDPR/CCPA/PIPL：数据最小化、访问/删除权、知情同意

由 `/init-workflow` 的 Q3 问题选择。详情见 [`references/compliance-presets.md`](references/compliance-presets.md)。

## 起源故事

来自一个 Java/Spring 政府托育系统（ProCare 扬州智慧托育，153 功能点 / 5 子系统 / 85 表）经历 3 轮阶段返工后的实践沉淀。6 条硬教训：

1. 事件 / 接口骨架必须**在业务逻辑之前**建好，而不是事后补
2. 多 Agent 并行**只在严格模块隔离下能工作**
3. ServiceImpl 改造清单必须**前置列出**，不能靠评审才发现
4. 编译验证必须**每个 Agent 完成后立即跑**，不能积累
5. 阶段评审必须**强制并行**（≥3 角度），不能可选 / 串行
6. 教训必须**当下沉淀**，不能"下次记得"

这个 skill 把这 6 条教训编码成可执行的工作流。

## 贡献

skill 在 [`garveyhu/awesome-skills`](https://github.com/garveyhu/awesome-skills)。欢迎 issue / PR。

skill 在 dogfood 自己：它装在自己的 repo 上。如果你在真实项目里使用时发现问题，用 `/self-improve` 抓下来，作为 PR 反向同步到 `templates/` 或 `references/`。

## License

MIT（继承 `awesome-skills` 仓库）。
