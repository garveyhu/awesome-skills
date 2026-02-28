# Awesome Skills

A collection of AI agent skills for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) and other AI coding assistants.

## Skills

### react-best-practices

React project initialization, development guidance, and code review based on `yarn + Vite + TypeScript + React + Ant Design + Tailwind CSS` stack.

**Features:**

- **Init** — Scaffold a React project with full linting toolchain (ESLint, Prettier, Stylelint, Commitlint, Husky, ls-lint, lint-staged)
- **Guide** — Add pages, components, modules, API services following conventions
- **Review** — Check project structure and code against best practices

Includes 9 config templates and 7 source code templates ready to copy.

Supports two project scales: simple (single-module) and complex (multi-module with dynamic route discovery).

### wiki-creator

Deep-scan a project codebase and generate structured, DeepWiki-style multi-file Markdown documentation.

**Features:**

- Thorough 4-phase workflow: Deep Scan → Plan Structure → Generate Docs → Review
- Scans entry files, follows import chains, reads actual source code
- Flexibly generates 4–10 docs based on project characteristics (not a fixed template)
- Mermaid diagrams with render-safe styling (includes a style guide with color schemes and syntax checklist)
- Chinese output, compatible with Docsify display

**Pairs with** `docsify-station-creator` to turn generated docs into a browsable site.

### docsify-station-creator

Generate a fully-featured Docsify documentation site from an existing `docs/` folder.

**Features:**

- Dark/light theme toggle
- Right-side table of contents with scroll highlight and collapse
- Full-text search
- Mermaid diagram rendering with Panzoom click-to-zoom
- Code syntax highlighting (16 languages) with copy button
- Responsive layout
- Cross-platform startup scripts (Windows `.bat` + Unix `.sh`)

## Installation

### Claude Code

```bash
claude skill add --from <skill-folder>
```

Or manually copy/symlink the skill folder to `~/.claude/skills/`.

### Manual

Copy the desired skill folder into your AI assistant's skill directory. Each skill is self-contained — just the folder and its contents.

## Usage

Once installed, skills are triggered automatically when relevant. Examples:

```
# Triggers react-best-practices
"Create a new React project for a dashboard app"

# Triggers wiki-creator
"Generate documentation for this project"

# Triggers docsify-station-creator
"Create a Docsify site from the docs folder"
```

## License

MIT
