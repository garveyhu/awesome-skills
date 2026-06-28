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
| **gemini-gen** | Generate images via Gemini member accounts (Nano Banana) over browser cookies — multi-account load-balancing with auto-failover on quota |
| **browser-gen** | Drive a logged-in Gemini web session for free image / video generation (Veo video · Nano Banana image) |
| **jimeng** | Jimeng/Dreamina image + video via the cloud API (AK/SK, **no vip needed**): text/image-to-image, P-image edit, inpaint, text/image-to-video, and **motion-mimic — drive a character image with a template video (IP animation made easy)**; CLI fallback |
| **media-gen** | A unified image-gen entry point: one call routes to gemini-gen / comfyui / codex / … by config & availability, with a quota-failover fallback chain, auto-injects style-lock v1, and returns a unified result contract (à la Pixelle's MediaService) |

## Audio

| skill | what it does |
|---|---|
| **voxcpm** | Local text-to-speech / voiceover (VoxCPM2 on Apple MLX) — zero-shot, voice design from a text prompt, and voice cloning; offline, 48kHz, faster-than-realtime on Apple Silicon |

## Methodology

| skill | what it does |
|---|---|
| **skill-management** | My skill-management methodology itself: organize many skills as source → category → skill, driven by a single `registry`, reusable across Claude Code & Codex, with bundled tooling. **Any AI can read it and replicate the whole setup** |
| **self-improving-workflow** | A universal methodology: four reviewer sub-agents for collaborative learning + a single `/run` entrypoint for long-running autonomous execution |
| **memory-palace** | Guide anyone to build a platform-agnostic personal memory system: one Obsidian vault (plain Markdown) that Claude / Codex / Gemini read & write together, so every agent understands *you* over time — memory visible, editable, portable. Subcommands help/init/interview/extract/distill/review/analyze; deterministic zero-dep engine `mp.py`. Distils from Karpathy / OpenClaw / Hermes / open-second-brain / mem0 |
| **loop-harness** | Scaffold + harness for high-quality long-running autonomous iteration loops (optimization / audit / migration / deep grinding). Taskbook + ledger + log file-driven memory, an **external objective verification gate** (report what the script says, not self-judgment), **progress-detection stop/escalate** (not step count), anti-drift memory + multi-agent. Distilled from a real 100-round loop; isomorphic to Ralph loop + BabyAGI + evaluator-optimizer. Runs on top of `/loop` or `/schedule` |

---

## Usage

These skills follow the [Claude Code Agent Skills](https://docs.claude.com/en/docs/claude-code/skills) spec.

```bash
git clone https://github.com/garveyhu/awesome-skills.git

# Symlink the skills you want into Claude Code's skill dir (pick as needed)
ln -s "$PWD/awesome-skills/stack/react-best-practices" ~/.claude/skills/
ln -s "$PWD/awesome-skills/media/image/comfyui"        ~/.claude/skills/
```

Then trigger them in conversation with natural language, or invoke `/<skill-name>` explicitly.

## Shared DNA

- **Single responsibility / extensible / maintainable**: rather split one more layer than cram multiple responsibilities into one file.
- **Anti "AI-slop" aesthetics**: pick one "face" first, freeze the design tokens, build a single signature moment, keep the rest restrained.
- **Convention first**: backend GET + POST with a unified response envelope; frontend atomic styling, strict types.
- **Chinese-first output**: comments, docs and generated content default to Chinese.

> A curated, opinionated collection — only my original skills. Use it, learn from it, and feel free to open an issue.
