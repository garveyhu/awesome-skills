---
name: wiki-creator
description: Deep-scan a project and generate structured, DeepWiki-style multi-file Markdown documentation under docs/. Use when the user asks to generate project documentation, create a wiki, write project docs, generate a docs folder, or produce a documentation set for a codebase. Output is Chinese, uses Mermaid diagrams, and is compatible with Docsify display via the docsify-station-creator skill.
---

# Wiki Creator

Deep-scan a project codebase and generate structured multi-file Markdown documentation under `docs/`. Output narrative flows top-down: concept → design → implementation → extension. All content in Chinese. Use Mermaid for all diagrams.

## Workflow

### Phase 1: Deep Scan

**This phase is critical. Do not skip or rush it.**

Read [references/scan-checklist.md](references/scan-checklist.md) and execute a thorough project scan:

1. **Global survey**: List all top-level files and directories. Read `package.json` / `pyproject.toml` / `go.mod` / `pom.xml` etc. to identify tech stack and dependencies.
2. **Entry tracing**: Find and read main entry files. Follow import chains to map core module dependencies.
3. **Architecture mapping**: Identify the project's structural pattern (MVC / MVVM / DDD / microservices / monolith / plugin-based, etc.) by reading key directories and files.
4. **Deep read**: For each major module (routing, models, services, controllers, state management, etc.), read representative source files to understand actual implementation — not just directory names.
5. **Config & infra**: Scan config files, Dockerfiles, CI/CD pipelines, environment variables.
6. **Existing docs**: Check for README, CHANGELOG, existing docs/, ADRs, OpenAPI specs.

**Output of this phase**: A mental model of the project covering: purpose, tech stack, architecture pattern, module structure, data flow, external integrations, and deployment approach.

### Phase 2: Plan Document Structure

Based on scan results, determine which document types are relevant. Read [references/doc-templates.md](references/doc-templates.md) for content requirements of each type.

**Selection rules**:

| Project characteristic | Include these doc types |
|---|---|
| Any project | 项目概览, 代码结构 |
| Has clear module boundaries | 系统架构 |
| Has business logic / workflows | 数据流与核心逻辑 |
| Exposes API endpoints | API 与接口 |
| Uses database / ORM | 数据模型与持久化 |
| Has Docker / CI/CD | 配置与部署 |
| Accepts contributions | 开发指南 |
| Has frontend code | 前端架构 |
| Has auth / security | 安全与认证 |
| Has test suite | 测试策略 |
| Has caching / perf design | 性能与优化 |

**File naming**: Two-digit prefix + descriptive kebab-case name. Example:

```
docs/
├── 01-overview.md
├── 02-architecture.md
├── 03-codebase-structure.md
├── 04-core-logic.md
├── 05-api-reference.md
└── 06-deployment.md
```

Number of files is flexible (typically 4–10). Choose based on project complexity. Do NOT force-create docs for aspects the project doesn't have.

Present the planned structure to the user for confirmation before proceeding to Phase 3.

### Phase 3: Generate Documentation

For each planned document file:

1. **Re-read relevant source files** — do not write from memory of Phase 1 alone. Go back and read the actual code to ensure accuracy.
2. **Write content** following the templates in [references/doc-templates.md](references/doc-templates.md).
3. **Include Mermaid diagrams** — read [references/mermaid-style-guide.md](references/mermaid-style-guide.md) and follow its rules strictly. Use `classDef` + `:::` for styling, proper node shapes, and the provided color schemes. Every doc should have at least one diagram where applicable. After writing each diagram, run the quick check list at the end of the style guide to avoid render failures.
4. **Maintain narrative continuity** — each file should start with a brief context sentence linking it to the previous topic.

**Writing rules**:

- Pure Markdown only. No HTML.
- No navigation links ("下一篇", "返回目录") — Docsify handles navigation.
- Each file uses exactly one `# heading` as page title.
- Use `##` / `###` / `####` for sections.
- Code examples must specify language for syntax highlighting.
- Tables for structured data (API params, config items, etc.).
- Content must be **accurate** — sourced from actual code, not generic boilerplate. If unsure about something, re-read the source.

### Phase 4: Review

After generating all files:

1. Verify every file references actual project code, not placeholder examples.
2. Verify Mermaid syntax against [references/mermaid-style-guide.md](references/mermaid-style-guide.md) checklist — no `radius`, `font-size`, `%%{init}%%`, no `note` in flowcharts, no unsupported CSS properties.
3. Verify file naming is sequential and consistent.
4. List generated files to the user with a one-line summary of each.

## Pairing with Docsify

After wiki generation, suggest the user invoke `docsify-station-creator` to create the Docsify site shell that displays these docs.
