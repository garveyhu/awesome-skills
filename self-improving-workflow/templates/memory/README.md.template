# Memory layout

Three layers, written by reviewers and `crystallize.sh`. **Do not hand-edit.**

```
.claude/memory/
├── episodic/                ← raw event records (gitignored)
│   └── ep-<date>-<id>.json
├── semantic-patterns.json    ← aggregated by fingerprint (git tracked)
└── working/                  ← session-scope cache (gitignored)
```

Promotion path: `episodic → semantic → .claude/rules/dev-lessons.md`.

Threshold: 3 occurrences with same 2-segment fingerprint AND average confidence ≥ 0.7.
