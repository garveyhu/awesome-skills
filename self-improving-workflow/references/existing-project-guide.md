# Adopting on an Existing Project

This skill is **non-destructive** by design. You can run `/init-workflow` on a project that already has CLAUDE.md, `.claude/`, `.gitignore`, etc. without losing any data.

## What Happens On An Existing Project

### Case 1: No `.claude/` directory yet

Same as a brand-new project. Full clean install. Done.

### Case 2: `.claude/` exists with some files

The init script does this for **each template file**:

1. Compute target path (e.g. `.claude/rules/coding-bans.md`)
2. Check if target exists
3. **Exists** → log "skipped" and move on. Never overwrite.
4. **Doesn't exist** → render template variables, write file, log "created".

Result: you get whatever was missing, and nothing of yours is touched.

### Case 3: `.claude/CLAUDE.md` already exists (special case)

CLAUDE.md is the entry file, so the skill **also writes a `.skill-template` companion** alongside your existing one:

```
.claude/CLAUDE.md                  ← your existing file (untouched)
.claude/CLAUDE.md.skill-template   ← reference template from skill
```

You can `diff` them and merge useful sections at your leisure. Or ignore the `.skill-template` if your CLAUDE.md is already perfect.

### Case 4: `.gitignore` has `.claude/` (entire dir ignored)

The init script **detects this and warns** instead of patching:

```
⚠️  WARNING: .gitignore contains '.claude/' which ignores the entire dir.
   This skill assumes .claude/ should be git-tracked (except memory subdirs).
   Manually remove '.claude/' line and add the granular pattern below:

   # Claude — project config tracked, ignore private/temp data
   .claude/settings.local.json
   .claude/memory/episodic/
   .claude/memory/working/
```

You decide whether to remove the broad ignore. The skill won't do it for you (too invasive).

### Case 5: `.gitignore` doesn't have `.claude/` ignored

Init **idempotently appends** the granular ignore pattern (only if not already present):

```
# Claude — project config tracked, ignore private/temp data
.claude/settings.local.json
.claude/memory/episodic/
.claude/memory/working/
```

Re-running init won't duplicate the lines.

## Recommended Workflow For Existing Projects

### Step 1: Backup (optional but cheap)

```bash
cp -r .claude .claude.backup-$(date +%Y%m%d) 2>/dev/null || true
```

### Step 2: Run detection only

```bash
bash ~/.agents/skills/self-improving-workflow/scripts/detect.sh
```

This tells you:
- What's already in `.claude/`
- What tier the skill recommends based on project signals
- No files are changed

### Step 3: Run init with `minimal` first

```
/init-workflow minimal
```

`minimal` is the safest entry point. It only adds 6 files and skips anything that exists. Verify nothing of yours got touched.

### Step 4: Read the `.skill-template` files

If your existing CLAUDE.md got a `.skill-template` companion, read it. Decide whether to:
- Ignore it (your CLAUDE.md is fine)
- Cherry-pick a section into your CLAUDE.md
- Replace your CLAUDE.md wholesale

The skill never makes this choice for you.

### Step 5: Decide on upgrading

If you want phase protocols and review agents, run:

```
/upgrade-workflow standard
```

or jump straight to `/upgrade-workflow full`.

Same write-once rules apply. New tier files that don't exist → created. Existing files → skipped or diff-prompted.

## Migration From Other Workflow Tools

### From hand-written `.claude/`

Just run `/init-workflow minimal`. Your existing files survive. Look at `.skill-template` companions for inspiration.

### From `cookiecutter` / `yeoman` templates

Same as hand-written. The skill doesn't care how your `.claude/` was created, only that the files exist.

### From `charon-fan/agent-playbook@self-improving-agent` standalone

If you already have charon-fan's skill installed and have memories in `~/.agents/skills/self-improving-agent/memory/`, those stay where they are. This skill complements it: charon-fan provides the **memory engine**, this skill provides the **project-level scaffold + slash commands** that drive memory operations.

`/self-improve` will detect charon-fan's skill and delegate to it for the heavy lifting. Without charon-fan installed, `/self-improve` falls back to a 3-prompt manual mode.

## Frequently Asked Questions

**Q: I ran init and don't like some files. Can I delete them?**
A: Yes. Just `rm` them. This skill doesn't track ownership beyond the `.workflow-tier` marker. Re-running init will recreate them (since they no longer exist).

**Q: I edited `coding-bans.md` heavily. Will upgrade overwrite it?**
A: No. Upgrade detects content differences and prompts you with `[k]eep / [n]ew / [d]iff / [s]kip`. You stay in control.

**Q: Can I run init twice with different tiers?**
A: Yes, but use `/upgrade-workflow` instead. Running init twice with different tiers is fine but won't do anything different — it's idempotent and never overwrites.

**Q: How do I downgrade?**
A: Not supported. Manually delete unwanted files. The skill refuses to "downgrade" because it would risk deleting files you've customized.

**Q: My team has a strict policy against AI-generated files. Can the skill annotate files as AI-generated?**
A: All skill-written files have a clear comment block at the top citing the skill. Additionally, all files in `.claude/.skill-template` versions are clearly marked with `.skill-template` suffix.
