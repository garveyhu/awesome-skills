---
name: docsify-station-creator
description: Generate a fully-featured Docsify documentation site from an existing docs/ folder. Use when the user asks to create a documentation site, generate a Docsify site, or turn markdown files into a browsable doc portal. Features include dark/light theme toggle, right-side TOC with scroll highlight, full-text search, Mermaid diagram rendering, code highlighting with copy button, and responsive layout.
---

# Docsify Station Creator

From an existing `docs/` folder with markdown files, generate a complete Docsify documentation site.

## Pre-requisites

Identify project info (ask user if not available from code/context):

1. `{{PROJECT_NAME}}` — project name
2. `{{PROJECT_DESCRIPTION}}` — one-line description
3. `{{PROJECT_ICON}}` — emoji icon (default: `🌊`)

## Workflow

### Step 1: Create directory structure

Under `docs/`:

```
docs/
├── docsify/
│   ├── _sidebar.md
│   └── README.md
└── scripts/
    ├── start-docs.bat
    └── start-docs.sh
```

### Step 2: Scan existing markdown files

Scan `docs/` and subdirectories for all `.md` files. **Exclude**:
- `docs/docsify/`, `docs/scripts/`, `node_modules/`, `.git/`
- `_sidebar.md`, `_navbar.md`, `_coverpage.md`
- `docs/docsify/README.md`

Record the file list for sidebar generation.

### Step 3: Generate sidebar navigation

From the scanned file list:

1. Sort by filename (numeric prefix first if present)
2. Extract title: read first `# heading` from each file; fallback to filename without `.md`
3. Group files:
   - By subdirectory name if files are in subdirectories
   - By numeric prefix pattern (e.g., `01-`, `02-`)
   - Common groups: 入门指南, 核心概念, 使用指南, 开发文档, 其他
4. If fewer than 5 files, use flat list without groups

**Path format**: relative to `docs/` root (where `index.html` lives). No `../` prefix.

Example `_sidebar.md`:

```markdown
- 入门指南
  - [快速开始](01-quick-start.md)
  - [项目简介](02-introduction.md)
- 核心概念
  - [架构设计](03-architecture.md)
```

For files in subdirectories (e.g., `docs/guide/start.md`): link is `guide/start.md`.

Strip numeric prefixes from display names (e.g., `01-quick-start.md` → "快速开始").

### Step 4: Generate files

Generate 5 files using the templates below.

#### 4.1 `docs/index.html`

Copy from [assets/index.html](assets/index.html). Replace all `{{PROJECT_NAME}}`, `{{PROJECT_DESCRIPTION}}`, `{{PROJECT_ICON}}` with actual values.

#### 4.2 `docs/docsify/_sidebar.md`

Use the navigation generated in Step 3.

#### 4.3 `docs/docsify/README.md`

Generate a landing page with:
- Project name as `# heading`
- `{{PROJECT_DESCRIPTION}}` as blockquote
- Feature highlights (adapt to actual project)
- Quick start link pointing to first content file
- Doc navigation guide

#### 4.4 `docs/scripts/start-docs.bat`

Copy from [assets/start-docs.bat](assets/start-docs.bat) verbatim.

#### 4.5 `docs/scripts/start-docs.sh`

Copy from [assets/start-docs.sh](assets/start-docs.sh) verbatim. Set executable: `chmod +x`.

### Step 5: Verify

Confirm to user:
- [ ] Directory structure created (`docsify/`, `scripts/`)
- [ ] All `.md` files scanned with correct paths
- [ ] `index.html` generated with project info substituted
- [ ] `_sidebar.md` contains all content file links
- [ ] `README.md` landing page complete
- [ ] Startup scripts generated

Provide startup instructions:

**Windows**: `./docs/scripts/start-docs.bat`
**Linux/Mac**: `chmod +x docs/scripts/start-docs.sh && ./docs/scripts/start-docs.sh`

Then visit `http://localhost:3000`.

## Customization

For theme color, favicon, code language, or markdown conventions, see [references/customization.md](references/customization.md).
