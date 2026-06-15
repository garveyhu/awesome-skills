# awesome-skills

**English** · [简体中文](./README.zh-CN.md)

> A curated collection of the Agent Skills and workflows I've honed in real projects — encoding my engineering conventions and creative pipelines into capabilities that agents like [Claude Code](https://claude.com/claude-code) can call directly.

These aren't generic "do-anything assistants." Each skill takes a stance: my tech-stack conventions, my aesthetic bar, my collaboration patterns. Just describe what you need — the skill handles the architecture decisions, boilerplate, conventions, and delivery. Fewer detours, no cutting corners.

---

## Tech-stack scaffolding

| skill | what it does |
|---|---|
| **react-best-practices** | React conventions & scaffolding: yarn + Vite + TS + Antd + Tailwind, with layering / naming / lint suite — init, build and review end to end |
| **fastapi-best-practices** | FastAPI backend conventions: uv + SQLAlchemy + Alembic + loguru + ruff, MVC layering, unified response envelope, GET+POST convention |
| **docker-best-practices** | Containerization standard kit: three-zone layout (images / containers / scripts), multi-image split, multi-arch buildx, registry & offline-tar delivery |
| **website-creator** | Spin up a website / app from scratch: Socratic questioning to 95% requirement certainty, then scaffolds frontend / full-stack |

## Docs & knowledge

| skill | what it does |
|---|---|
| **wiki-creator** | Deep-scan a project into DeepWiki-style multi-file docs (Mermaid, Docsify-ready) |
| **docsify-station-creator** | Turn a `docs/` folder into a full-featured Docsify site (dark mode / full-text search / TOC / Mermaid / optional animation mode) |
| **req-to-ai-spec** | Turn scattered requirements (text / screenshots / legacy code) into structured, AI-friendly specs a coding agent can run with |
| **spechub-best-practices** | Write high-quality handoff specs managed via git worktree — built for AI-to-AI task handoff |
| **notion-chat-archiver** | Summarize an AI conversation and archive it into a personal Notion database (topic / takeaways / tags) |
| **solution-vault** | A personal solution library to replicate proven implementations (OAuth, uploads, payments…) across projects |

## Visualization

| skill | what it does |
|---|---|
| **html-diagram** | Pick a "face" from a style library and render architecture / topology / timeline diagrams as a self-contained single HTML file |

## Design & style

| skill | what it does |
|---|---|
| **style-vault** | A six-tier (product / style / page / block / component / token) personal style library that generates frontends to my aesthetic |
| **style-vault-sediment** | The companion writer: deposit new styles into style-vault, versioned by author |

## Image & video

| skill | what it does |
|---|---|
| **comfyui** | Drive a local ComfyUI from natural language for image / video generation, auto-building workflows; model-agnostic, tuned for Apple Silicon |
| **codex-image-gen** | Generate / edit images via Codex (gpt-image-2), with reference images to lock character & style |
| **browser-gen** | Drive a logged-in Gemini web session for free image / video generation (Veo video · Nano Banana image) |
| **links-illustrations** | Whimsical hand-drawn Chinese article illustrations featuring the "Little Black" character |
| **jimeng** | Jimeng / Dreamina image-generation channel |

## Methodology

| skill | what it does |
|---|---|
| **skill-management** | My skill-management methodology itself: organize many skills as source → category → skill, driven by a single `registry`, reusable across Claude Code & Codex, with bundled tooling. **Any AI can read it and replicate the whole setup** |
| **self-improving-workflow** | A universal methodology: four reviewer sub-agents for collaborative learning + a single `/run` entrypoint for long-running autonomous execution |

---

## Usage

These skills follow the [Claude Code Agent Skills](https://docs.claude.com/en/docs/claude-code/skills) spec.

```bash
git clone https://github.com/garveyhu/awesome-skills.git

# Symlink the skills you want into Claude Code's skill dir (pick as needed)
ln -s "$PWD/awesome-skills/stack/react-best-practices" ~/.claude/skills/
ln -s "$PWD/awesome-skills/media/comfyui"              ~/.claude/skills/
```

Then trigger them in conversation with natural language, or invoke `/<skill-name>` explicitly.

## Shared DNA

- **Single responsibility / extensible / maintainable**: rather split one more layer than cram multiple responsibilities into one file.
- **Anti "AI-slop" aesthetics**: pick one "face" first, freeze the design tokens, build a single signature moment, keep the rest restrained.
- **Convention first**: backend GET + POST with a unified response envelope; frontend atomic styling, strict types.
- **Chinese-first output**: comments, docs and generated content default to Chinese.

> A curated, opinionated collection — only my original skills. Use it, learn from it, and feel free to open an issue.
