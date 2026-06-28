<!-- [English](README.md) · [中文](README.zh-CN.md) -->

# 🧠 Memory Palace

> A platform-agnostic personal memory system. One local Obsidian vault (plain Markdown) that
> Claude Code / Codex / Gemini / any CLI **read and write together** — so every AI agent
> understands *you* better over time. Your memory is **visible, editable, portable** — never
> locked in a vendor's black box.

This skill guides anyone to build, fill, and maintain their own memory palace. The vault is your
private data; this skill is the generic tool (zero personal data).

## Subcommands

| Command | What it does |
|---------|--------------|
| `/memory-palace help` | Open the concept explainer (self-contained HTML) + menu |
| `/memory-palace init` | Scaffold an empty palace (5 layers + protocol) and wire up your AI tools |
| `/memory-palace interview` | A deep, probing interview that turns *who you are* into memory |
| `/memory-palace extract` | Import existing memory from your local Claude/Codex rules & sessions |
| `/memory-palace distill` | Distil recent sessions into candidate memories (the flywheel) |
| `/memory-palace review` | Approve candidates → promote into the palace (you decide) |
| `/memory-palace analyze` | Audit the palace → actionable cleanup suggestions |

## The 5 layers

`00-RULES` identity & ironclad rules (you-approved) · `01-PROJECTS` per-project decisions+feedback
(nestable) · `02-SOURCES` clippings · `03-MAPS` diagrams · `04-FEEDBACK` the flywheel
(journal → candidates → DREAMS).

## How it learns (the flywheel)

Corrections/decisions/preferences land in `04-FEEDBACK/journal/` → `mp.py distill` scans your local
agent sessions, **scores candidates with 6 weighted signals**, and drafts them (never touching
`00-RULES`) → you approve via `review` → every agent reads `00-RULES` + greps the vault next time.
**Fix once, all tools stop repeating the mistake.**

Core principle: the LLM only *extracts candidates*; scoring, dedup and the promotion gate are
**deterministic** — your memory is never polluted by model hallucination.

## Engine: `scripts/mp.py`

A zero-dependency CLI (Python ≥ 3.11) — also usable standalone:
`mp.py <init|distill|promote|analyze|link> --vault <path>`.

## Credits

Builds on Karpathy's "Obsidian as a shared AI brain", OpenClaw's Dreaming distillation,
Hermes' extraction-pass & skill-as-memory, open-second-brain's no-LLM-in-the-core deterministic
promotion, and mem0's ADD/UPDATE/NOOP write-back. See `assets/explainer.html`.
