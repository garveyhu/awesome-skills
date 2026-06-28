#!/usr/bin/env python3
"""mp.py — Memory Palace CLI · 跨平台个人记忆系统的引擎。

工具/数据分离：脚本随 skill 走，记忆数据在 --vault 指定的宫殿目录。
LLM 只负责「抽候选」，打分/去重/晋升门全是确定性规则——记忆永不被模型幻觉污染。

子命令：
  init     从模板脚手架一座新宫殿（五层 + PROTOCOL + 适配 stub + 配置）
  distill  扫本地 agent 会话 + journal → 六维加权打分 → 出候选草稿（绝不改 00-RULES）
  promote  把已审批([x])的候选晋升到目标文件，留痕 DREAMS
  analyze  体检宫殿：重复 / 陈旧 / 低置信 / 缺 frontmatter / 孤儿 → 报告
  link     按 config [links] 重建软链（中央集权·真身在 vault·外部只放软链）

依赖：仅标准库（Python ≥ 3.11，用 tomllib）。
用法：mp.py <子命令> --vault <宫殿路径> [选项]
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from difflib import SequenceMatcher
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = SKILL_ROOT / "assets" / "templates"
CONFIG_EXAMPLE = SKILL_ROOT / "scripts" / "config.example.toml"

PREFIX_TYPE = {"偏好": "preference", "决策": "decision", "纠正": "correction", "观察": "observation"}
REQUIRED_FM = ("title", "type")  # 每条记忆 note 至少要带的 frontmatter 字段


# ───────────────────────── 配置 / 路径 ─────────────────────────
def cfg_path(vault: Path) -> Path:
    p = vault / ".mp" / "config.toml"
    if p.exists():
        return p
    legacy = vault / "_engine" / "config.toml"   # 兼容早期把引擎放 vault 内的形态
    return legacy if legacy.exists() else p


def load_config(vault: Path) -> dict:
    p = cfg_path(vault)
    if not p.exists():
        raise SystemExit(f"[mp] 找不到配置 {p}，先跑 `mp.py init --vault {vault}`")
    with open(p, "rb") as f:
        return tomllib.load(f)


def expand(p: str) -> Path:
    return Path(p).expanduser()


def journal_dir(v: Path) -> Path: return v / "04-FEEDBACK" / "journal"
def candidates_md(v: Path) -> Path: return v / "04-FEEDBACK" / "candidates.md"
def dreams_md(v: Path) -> Path: return v / "04-FEEDBACK" / "DREAMS.md"
def rules_dir(v: Path) -> Path: return v / "00-RULES"


# ───────────────────────── 数据结构 ─────────────────────────
@dataclass
class Signal:
    text: str
    source: str
    date: str
    kind: str = ""


@dataclass
class Candidate:
    statement: str
    ctype: str
    scope: str
    freq: int = 1
    sources: list[str] = field(default_factory=list)
    dates: set[str] = field(default_factory=set)
    score: float = 0.0
    sub: dict[str, float] = field(default_factory=dict)
    action: str = "ADD"
    dest: str = ""
    conf: str = "low"


# ───────────────────────── 捕获信号 ─────────────────────────
def recent_dates(days: int) -> set[str]:
    today = datetime.now().date()
    return {(today - timedelta(days=i)).isoformat() for i in range(days)}


def gather_journal(vault: Path, days: int) -> list[Signal]:
    wanted = recent_dates(days)
    out: list[Signal] = []
    for md in sorted(journal_dir(vault).glob("*.md")):
        if md.stem not in wanted:
            continue
        for line in md.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^\s*-\s*(偏好|决策|纠正|观察)\s*[:：]\s*(.+)$", line)
            if m:
                out.append(Signal(m.group(2).strip(), "journal", md.stem, PREFIX_TYPE[m.group(1)]))
    return out


def _walk_user_text(obj: object) -> list[str]:
    found: list[str] = []

    def to_text(content: object) -> str:
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts = []
            for b in content:
                if isinstance(b, dict) and b.get("type") in (None, "text") and isinstance(b.get("text"), str):
                    parts.append(b["text"])
                elif isinstance(b, str):
                    parts.append(b)
            return "\n".join(parts)
        return ""

    def walk(o: object) -> None:
        if isinstance(o, dict):
            if (o.get("role") or o.get("type")) == "user" and "content" in o:
                t = to_text(o["content"])
                if t.strip():
                    found.append(t.strip())
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(obj)
    return found


def _scan_jsonl(files: list[Path], source: str, day: str, max_turns: int) -> list[Signal]:
    out: list[Signal] = []
    for fp in files:
        turns = 0
        try:
            for line in fp.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                for t in _walk_user_text(obj):
                    out.append(Signal(t[:2000], source, day))
                    turns += 1
                    if turns >= max_turns:
                        break
                if turns >= max_turns:
                    break
        except OSError:
            continue
    return out


def recent_files(roots: list[Path], pattern: str, days: int, limit: int) -> list[Path]:
    cutoff = datetime.now().timestamp() - days * 86400
    cands: list[tuple[float, Path]] = []
    for root in roots:
        if not root.exists():
            continue
        for fp in root.rglob(pattern):
            try:
                mt = fp.stat().st_mtime
            except OSError:
                continue
            if mt >= cutoff:
                cands.append((mt, fp))
    cands.sort(reverse=True)
    return [fp for _, fp in cands[:limit]]


def gather_agents(cfg: dict, days: int, bootstrap: bool = False) -> list[Signal]:
    """扫各 agent 平台的会话日志。bootstrap=全量(忽略天数限制，扫所有历史)。"""
    src = cfg["sources"]
    out: list[Signal] = []
    scan_days = 3650 if bootstrap else days
    limit = src["max_files"] * (20 if bootstrap else 1)
    today = datetime.now().date().isoformat()
    if src.get("include_claude", True):
        root = expand(src.get("claude_projects", "~/.claude/projects"))
        files = recent_files([root], "*.jsonl", scan_days, limit)
        out += _scan_jsonl(files, "claude", today, src["max_user_turns_per_file"])
    if src.get("include_codex", True):
        roots = [expand(p) for p in src.get("codex_sessions", [])]
        files = recent_files(roots, "rollout-*.jsonl", scan_days, limit)
        out += _scan_jsonl(files, "codex", today, src["max_user_turns_per_file"])
    return out


# ───────────────────────── 抽候选 ─────────────────────────
def extract_heuristic(signals: list[Signal]) -> list[Candidate]:
    cands: list[Candidate] = []
    for s in signals:
        if s.source != "journal" or not s.kind or s.kind == "observation":
            continue
        cands.append(Candidate(s.text, s.kind, "global", sources=[s.source], dates={s.date}))
    return cands


CORRECTION_HINT = re.compile(r"(别|不要|不对|不是|应该|改成|讨厌|不喜欢|下次|记住|以后|偏好|永远|千万)")


def _cli_available(cmd: str) -> bool:
    return bool(shutil.which(cmd)) or Path(cmd).exists()


def _run_cli(pcfg: dict, prompt: str, timeout: int) -> str | None:
    cmd = pcfg.get("command", "")
    if not cmd or not _cli_available(cmd):
        return None
    full = [cmd, *pcfg.get("args", [])]
    out_path: Path | None = None
    if pcfg.get("output_file_arg"):
        tf = tempfile.NamedTemporaryFile(suffix=".txt", delete=False)
        tf.close()
        out_path = Path(tf.name)
        full += [pcfg["output_file_arg"], str(out_path)]
    full.append(prompt)
    try:
        r = subprocess.run(full, capture_output=True, text=True, timeout=timeout, stdin=subprocess.DEVNULL)
    except (OSError, subprocess.TimeoutExpired) as e:
        print(f"[mp] {cmd} 调用失败，跳过：{e}", file=sys.stderr)
        if out_path:
            out_path.unlink(missing_ok=True)
        return None
    try:
        if out_path:
            content = out_path.read_text(encoding="utf-8") if out_path.exists() else ""
            return content if content.strip() else None
        return r.stdout if r.returncode == 0 else None
    finally:
        if out_path:
            out_path.unlink(missing_ok=True)


def extract_llm(signals: list[Signal], cfg: dict) -> tuple[list[Candidate], str | None]:
    llm = cfg["llm"]
    picked = [s for s in signals if s.source != "journal" and CORRECTION_HINT.search(s.text)]
    if not picked:
        return [], None
    blob = "\n".join(f"[{s.source} {s.date}] {s.text}" for s in picked)[: llm["max_prompt_chars"]]
    prompt = (
        "你是记忆抽取器。下面是某用户最近和 AI 的对话里、TA 发出的纠正/偏好/决策片段。\n"
        "请抽出**稳定、可复用、关于这个人本身**的记忆候选（忽略一次性的具体任务指令）。\n"
        "只输出一个 JSON 数组，不要任何解释。每项：\n"
        '{"statement":"一句话陈述TA的偏好/决策/纠正","type":"preference|decision|correction|principle",'
        '"scope":"global 或 project:<路径>"}\n抽不出就输出 []。\n\n=== 片段 ===\n' + blob
    )
    provider = llm.get("provider", "")
    order = [provider] + [p for p in llm.get("fallback", []) if p != provider]
    providers = llm.get("providers", {})
    today = datetime.now().date().isoformat()
    for name in order:
        pcfg = providers.get(name)
        if not pcfg:
            continue
        raw = _run_cli(pcfg, prompt, llm["timeout_sec"])
        if not raw:
            continue
        m = re.search(r"\[.*\]", raw, re.DOTALL)
        if not m:
            continue
        try:
            items = json.loads(m.group(0))
        except json.JSONDecodeError:
            continue
        out = [
            Candidate(str(it["statement"]).strip(), str(it.get("type", "preference")),
                      str(it.get("scope", "global")), sources=[f"llm:{name}"], dates={today})
            for it in (items if isinstance(items, list) else [])
            if isinstance(it, dict) and it.get("statement")
        ]
        if out:
            return out, name
    return [], None


# ───────────────────────── 合并 / 打分 / 去重 ─────────────────────────
def norm(a: str) -> str:
    return re.sub(r"\s+", "", a.lower())


def merge(cands: list[Candidate]) -> list[Candidate]:
    merged: list[Candidate] = []
    for c in cands:
        hit = next((m for m in merged if SequenceMatcher(None, norm(c.statement), norm(m.statement)).ratio() >= 0.78), None)
        if hit:
            hit.freq += 1
            hit.sources = list(set(hit.sources + c.sources))
            hit.dates |= c.dates
        else:
            merged.append(c)
    return merged


def load_existing_statements(vault: Path) -> list[str]:
    out: list[str] = []
    rd = rules_dir(vault)
    for md in rd.rglob("*.md"):
        if md.relative_to(rd).parts[0] == "rules":
            continue  # 00-RULES/rules/ 是工程规范文档(软链给各 CLI)，非个人记忆陈述
        for line in md.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip(" -*")
            if 6 <= len(line) <= 200 and not line.startswith(("#", "|", "---", ">", "```")):
                out.append(line)
    return out


def best_sim(stmt: str, corpus: list[str]) -> float:
    s = norm(stmt)
    return max((SequenceMatcher(None, s, norm(c)).ratio() for c in corpus), default=0.0)


def infer_dest(c: Candidate) -> str:
    if c.scope.startswith("project:"):
        name = c.scope.split(":", 1)[1]
        leaf = "feedback.md" if c.ctype in ("correction", "feedback") else "decisions.md"
        return f"01-PROJECTS/{name}/{leaf}"
    if c.ctype == "principle":
        return "00-RULES/_principles/"
    return "00-RULES/preferences.md"


def score_all(cands: list[Candidate], existing: list[str], cfg: dict, days: int) -> None:
    w = cfg["scoring"]
    today = datetime.now().date()
    max_freq = max((c.freq for c in cands), default=1)
    for c in cands:
        rel = best_sim(c.statement, existing)
        freq = min(1.0, c.freq / max(2, max_freq))
        div = min(1.0, len(set(c.sources)) / 3.0)
        newest = max((datetime.fromisoformat(d).date() for d in c.dates), default=today)
        rec = max(0.0, 1.0 - (today - newest).days / max(1, days))
        rich = min(1.0, len(c.statement) / 60.0)
        c.sub = {"relevance": rel, "frequency": freq, "diversity": div, "recency": rec, "consolidation": rel, "richness": rich}
        c.score = round(w["w_relevance"] * rel + w["w_frequency"] * freq + w["w_diversity"] * div
                        + w["w_recency"] * rec + w["w_consolidation"] * rel + w["w_richness"] * rich, 3)
        sim = best_sim(c.statement, existing)
        c.action = "NOOP" if sim >= 0.92 else "UPDATE" if sim >= w["dedupe_similarity"] else "ADD"
        c.conf = "high" if c.score >= 0.66 else "medium" if c.score >= 0.5 else "low"
        c.dest = infer_dest(c)


def gate(cands: list[Candidate], cfg: dict) -> tuple[list[Candidate], list[Candidate]]:
    w = cfg["scoring"]
    passed, deferred = [], []
    for c in cands:
        if c.action == "NOOP":
            deferred.append(c)
            continue
        ok = c.score >= w["promote_threshold"]
        if c.scope == "global" and c.freq < w["min_freq_global"]:
            ok = False
        (passed if ok else deferred).append(c)
    passed.sort(key=lambda x: x.score, reverse=True)
    return passed, deferred


# ───────────────────────── 子命令：distill ─────────────────────────
def cmd_distill(args: argparse.Namespace) -> int:
    vault = Path(args.vault).expanduser().resolve()
    cfg = load_config(vault)
    days = args.days or cfg["sources"]["scan_days"]
    bootstrap = getattr(args, "bootstrap", False)

    signals: list[Signal] = []
    if cfg["sources"].get("include_journal", True):
        signals += gather_journal(vault, days)
    signals += gather_agents(cfg, days, bootstrap=bootstrap)

    cands = extract_heuristic(signals)
    provider = None
    if cfg["llm"]["enabled"] and not args.no_llm:
        llm_cands, provider = extract_llm(signals, cfg)
        cands += llm_cands

    cands = merge(cands)
    score_all(cands, load_existing_statements(vault), cfg, days)
    if bootstrap:
        # 一次性导入：反正你要逐条审批，跳过频次门，把所有非重复候选都呈现出来
        passed = sorted([c for c in cands if c.action != "NOOP"], key=lambda x: x.score, reverse=True)
        deferred = [c for c in cands if c.action == "NOOP"]
    else:
        passed, deferred = gate(cands, cfg)

    stamp = datetime.now().strftime("%Y-%m-%d")
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    nj = sum(s.source == "journal" for s in signals)
    nc = sum(s.source == "claude" for s in signals)
    nx = sum(s.source == "codex" for s in signals)
    summary = (
        f"\n## {ts} · distill{' (bootstrap)' if bootstrap else ''}{' (shadow)' if args.shadow else ''}\n"
        f"- 扫描: journal {nj} 行 / claude {nc} 发言 / codex {nx} 发言（近 {days} 天）\n"
        f"- 候选: {len(cands)} 条（达标 {len(passed)} · 暂缓 {len(deferred)}）· LLM 抽取: {provider or '否'}\n"
        f"- 达标: " + (", ".join(f"「{c.statement[:24]}」{c.score}" for c in passed) or "无") + "\n"
    )
    print(summary)
    if args.shadow:
        _append(dreams_md(vault), summary + "- (shadow，未落盘)\n")
        return 0
    if passed:
        _append(candidates_md(vault), _render_candidates(passed, stamp))
    _append(dreams_md(vault), summary)
    print(f"[mp] {len(passed)} 条候选已写入 candidates.md，待 `mp.py promote` 或 /memory-palace review 审批。")
    return 0


def _render_candidates(passed: list[Candidate], stamp: str) -> str:
    lines = [f"\n### 🟡 {stamp} 蒸馏（{len(passed)} 条待审批）\n"]
    for i, c in enumerate(passed, 1):
        meta = {"id": f"c{stamp.replace('-', '')}-{i:02d}", "action": c.action, "dest": c.dest,
                "type": c.ctype, "scope": c.scope, "freq": c.freq, "score": c.score, "conf": c.conf}
        lines.append(f"- [ ] {c.statement} <!--cand {json.dumps(meta, ensure_ascii=False)} -->")
        lines.append(f"  - 证据: freq={c.freq} · 来源 {', '.join(sorted(set(c.sources)))} · 日期 {', '.join(sorted(c.dates))}")
        lines.append("  - 六维: " + " ".join(f"{k}={v:.2f}" for k, v in c.sub.items()))
    return "\n".join(lines) + "\n"


def _append(path: Path, text: str) -> None:
    path.write_text((path.read_text(encoding="utf-8") if path.exists() else "") + text, encoding="utf-8")


# ───────────────────────── 子命令：promote ─────────────────────────
LINE = re.compile(r"^- \[([ xX])\]\s+(.*?)\s*<!--cand\s+(\{.*?\})\s*-->\s*$")


def slugify(s: str) -> str:
    return (re.sub(r"[^\w一-鿿]+", "-", s).strip("-")[:40]) or "principle"


def _ensure_leaf(path: Path, name: str, dest: str, today: str) -> None:
    proj = dest[len("01-PROJECTS/"):].rsplit("/", 1)[0]
    path.parent.mkdir(parents=True, exist_ok=True)
    if name == "decisions.md":
        head = (f"---\ntitle: {proj} · 决定\ntype: decision\nscope: project:{proj}\nstatus: active\n"
                f"updated: {today}\ntags: [decisions]\n---\n\n# {proj} · 共同决定（Memory）\n\n"
                "| 日期 | 决定 | 为什么 | 状态 |\n|------|------|--------|------|\n")
    else:
        head = (f"---\ntitle: {proj} · 打回\ntype: feedback\nscope: project:{proj}\nstatus: active\n"
                f"updated: {today}\ntags: [feedback]\n---\n\n# {proj} · 我打回的产出（Feedback）\n\n"
                "| 日期 | 现象 | 我要的 | 反哺去向 |\n|------|------|--------|---------|\n")
    path.write_text(head, encoding="utf-8")


def _apply_one(vault: Path, stmt: str, meta: dict, dry: bool) -> str:
    dest, today = meta["dest"], datetime.now().date().isoformat()
    if dest.endswith("/"):
        path = vault / dest / f"{slugify(stmt)}.md"
        body = (f"---\ntitle: {stmt[:40]}\ntype: {meta.get('type','principle')}\nscope: {meta.get('scope','global')}\n"
                f"status: active\nconfidence: {meta.get('conf','medium')}\ncreated: {today}\nupdated: {today}\n"
                f"last_confirmed: {today}\nsource: [蒸馏晋升]\n---\n\n# 原则：{stmt}\n\n"
                f"- 为什么：（蒸馏自反复信号 freq={meta.get('freq')}；补充动机）\n- 怎么应用：\n- 边界 / 例外：\n")
        if not dry:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body, encoding="utf-8")
        return f"新建 {path.relative_to(vault)}"
    path = vault / dest
    name = path.name
    if name == "decisions.md":
        row = f"| {today} | {stmt} | 蒸馏晋升(freq={meta.get('freq')}) | active |\n"
    elif name == "feedback.md":
        row = f"| {today} | {stmt} | | 蒸馏 |\n"
    else:
        row = f"- {stmt}  （{today}·蒸馏 score={meta.get('score')}）\n"
    note = ""
    if not dry:
        if not path.exists():
            if name in ("decisions.md", "feedback.md") and dest.startswith("01-PROJECTS/"):
                _ensure_leaf(path, name, dest, today)
                note = "（新建子项目文件）"
            else:
                return f"⚠️ 目标不存在，跳过：{dest}"
        text = path.read_text(encoding="utf-8")
        if name in ("decisions.md", "feedback.md"):
            text = text.rstrip() + "\n" + row
        else:
            if "## 蒸馏晋升" not in text:
                text = text.rstrip() + "\n\n## 蒸馏晋升\n\n"
            text = text.rstrip() + "\n" + row
        path.write_text(text, encoding="utf-8")
    return f"{'UPDATE' if meta.get('action') == 'UPDATE' else '追加'} → {dest} {note}".rstrip()


def cmd_promote(args: argparse.Namespace) -> int:
    vault = Path(args.vault).expanduser().resolve()
    src = candidates_md(vault).read_text(encoding="utf-8")
    out_lines, results = [], []
    for line in src.splitlines():
        m = LINE.match(line)
        if not m or m.group(1).lower() != "x":
            out_lines.append(line)
            continue
        stmt, meta = m.group(2).strip("* "), json.loads(m.group(3))
        if meta.get("action") == "NOOP":
            out_lines.append(line)
            continue
        results.append(f"{meta.get('id', '?')}: {_apply_one(vault, stmt, meta, args.dry_run)}")
        out_lines.append(line.replace("<!--cand", "✅<!--done"))
    if not results:
        print("[mp] 没有勾选([x])的候选。先在 candidates.md 勾选要晋升的。")
        return 0
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    log = f"\n## {ts} · promote（你审批）\n" + "".join(f"- 晋升 {r}\n" for r in results)
    print(log)
    if args.dry_run:
        print("[dry-run] 未写入。")
        return 0
    candidates_md(vault).write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    _append(dreams_md(vault), log)
    if args.commit:
        try:
            subprocess.run(["git", "-C", str(vault), "add", "-A"], check=True)
            subprocess.run(["git", "-C", str(vault), "commit", "-m", f"feat(memory): 晋升 {len(results)} 条记忆候选"], check=True)
            print("[mp] 已 git 提交。")
        except (OSError, subprocess.CalledProcessError) as e:
            print(f"[mp] git 提交跳过：{e}")
    print(f"[mp] 完成：{len(results)} 条已晋升。")
    return 0


# ───────────────────────── 子命令：init ─────────────────────────
def cmd_init(args: argparse.Namespace) -> int:
    vault = Path(args.vault).expanduser().resolve()
    if not TEMPLATES.exists():
        raise SystemExit(f"[mp] 模板缺失：{TEMPLATES}")
    vault.mkdir(parents=True, exist_ok=True)
    if any(p.name not in (".git",) for p in vault.iterdir()) and not args.force:
        raise SystemExit(f"[mp] {vault} 非空，加 --force 覆盖或换空目录")
    n = 0
    for src in TEMPLATES.rglob("*"):
        rel = src.relative_to(TEMPLATES)
        dst = vault / rel
        if src.is_dir():
            dst.mkdir(parents=True, exist_ok=True)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            n += 1
    (vault / ".mp").mkdir(exist_ok=True)
    shutil.copy2(CONFIG_EXAMPLE, vault / ".mp" / "config.toml")
    journal_dir(vault).mkdir(parents=True, exist_ok=True)
    today = datetime.now().date().isoformat()
    seed = journal_dir(vault) / f"{today}.md"
    if not seed.exists():
        seed.write_text(f"---\ntitle: Journal {today}\ntype: journal\ncreated: {today}\ntags: [journal]\n---\n\n"
                        f"# {today}\n\n> append-only。前缀 `决策:`/`偏好:`/`纠正:`/`观察:` 方便蒸馏。\n", encoding="utf-8")
    print(f"[mp] 已脚手架 {n} 个文件 → {vault}")
    print("     下一步：/memory-palace interview 充实身份，或 /memory-palace extract 从本地 agent 导入。")
    if args.git:
        try:
            subprocess.run(["git", "-C", str(vault), "init", "-q"], check=True)
            print("[mp] 已 git init。")
        except (OSError, subprocess.CalledProcessError) as e:
            print(f"[mp] git init 跳过：{e}")
    return 0


# ───────────────────────── 子命令：analyze ─────────────────────────
def _parse_fm(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    fm = {}
    for line in text[3:end].splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm


def cmd_analyze(args: argparse.Namespace) -> int:
    vault = Path(args.vault).expanduser().resolve()
    stale_days = 180
    today = datetime.now().date()
    notes: list[tuple[Path, dict, str]] = []
    for md in vault.rglob("*.md"):
        rel = md.relative_to(vault)
        if rel.parts[0].startswith(".") or rel.parts[0] in ("00-RULES",) and len(rel.parts) > 1 and rel.parts[1] == "rules":
            continue
        if rel.parts[0] in (".git",):
            continue
        text = md.read_text(encoding="utf-8", errors="ignore")
        notes.append((rel, _parse_fm(text), text))

    issues: dict[str, list[str]] = {"待充实(draft)": [], "缺frontmatter": [], "陈旧(last_confirmed>180d)": [], "低置信": [], "重复嫌疑": [], "孤儿(无人链接)": []}
    # frontmatter / 陈旧 / 低置信（草稿骨架不算腐化，单列）
    for rel, fm, _ in notes:
        if fm.get("status") == "draft":
            issues["待充实(draft)"].append(str(rel))
            continue
        if not fm or any(k not in fm for k in REQUIRED_FM):
            issues["缺frontmatter"].append(str(rel))
        lc = fm.get("last_confirmed", "")
        if re.match(r"\d{4}-\d{2}-\d{2}", lc):
            try:
                if (today - datetime.fromisoformat(lc[:10]).date()).days > stale_days:
                    issues["陈旧(last_confirmed>180d)"].append(f"{rel} ({lc})")
            except ValueError:
                pass
        if fm.get("confidence") == "low":
            issues["低置信"].append(str(rel))
    # 重复嫌疑（标题相似）
    titles = [(rel, fm.get("title", rel.stem)) for rel, fm, _ in notes]
    for i in range(len(titles)):
        for j in range(i + 1, len(titles)):
            if SequenceMatcher(None, norm(titles[i][1]), norm(titles[j][1])).ratio() >= 0.8:
                issues["重复嫌疑"].append(f"{titles[i][0]} ≈ {titles[j][0]}")
    # 孤儿（没有任何 note 用 [[wikilink]] 指向它）
    all_text = "\n".join(t for _, _, t in notes)
    for rel, _, _ in notes:
        stem = rel.stem
        if stem.startswith("_") or stem in ("README", "PROTOCOL", "candidates", "DREAMS"):
            continue
        if f"[[{stem}" not in all_text:
            issues["孤儿(无人链接)"].append(str(rel))

    report = [f"# 记忆宫殿体检 · {vault.name}", f"\n共 {len(notes)} 条 note。\n"]
    for k, v in issues.items():
        report.append(f"\n## {k}（{len(v)}）")
        report.extend(f"- {x}" for x in v[:30]) if v else report.append("- ✅ 无")
        if len(v) > 30:
            report.append(f"- …还有 {len(v) - 30} 条")
    out = "\n".join(report)
    if args.json:
        print(json.dumps({k: v for k, v in issues.items()}, ensure_ascii=False, indent=2))
    else:
        print(out)
    return 0


# ───────────────────────── 子命令：link ─────────────────────────
def cmd_link(args: argparse.Namespace) -> int:
    vault = Path(args.vault).expanduser().resolve()
    cfg = load_config(vault)
    links = cfg.get("links", {})
    if not links:
        print("[mp] config 无 [links] 段，无软链可建。")
        return 0
    for sys_path, rel in links.items():
        sysp = expand(sys_path)
        target = vault / rel
        if not target.exists():
            print(f"  ✗ 真身不存在，跳过：{rel}")
            continue
        if sysp.is_symlink() and sysp.resolve() == target.resolve():
            print(f"  ✓ 已是正确软链：{sysp}")
            continue
        if args.dry_run:
            print(f"  [dry] 将软链 {sysp} → {target}")
            continue
        if sysp.exists() and not sysp.is_symlink():
            bak = sysp.with_name(sysp.name + ".bak-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
            sysp.rename(bak)
            print(f"  备份原物 → {bak}")
        sysp.parent.mkdir(parents=True, exist_ok=True)
        if sysp.is_symlink():
            sysp.unlink()
        sysp.symlink_to(target)
        print(f"  → 软链 {sysp} → {target}")
    return 0


# ───────────────────────── 入口 ─────────────────────────
def main() -> int:
    ap = argparse.ArgumentParser(prog="mp.py", description="Memory Palace CLI")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add_vault(p): p.add_argument("--vault", required=True, help="记忆宫殿目录")

    p = sub.add_parser("init", help="脚手架一座新宫殿")
    add_vault(p); p.add_argument("--git", action="store_true"); p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("distill", help="蒸馏出候选")
    add_vault(p); p.add_argument("--shadow", action="store_true"); p.add_argument("--no-llm", action="store_true")
    p.add_argument("--days", type=int, default=None); p.add_argument("--bootstrap", action="store_true", help="全量扫历史(首次导入)")
    p.set_defaults(func=cmd_distill)

    p = sub.add_parser("promote", help="晋升已审批候选")
    add_vault(p); p.add_argument("--dry-run", action="store_true"); p.add_argument("--commit", action="store_true")
    p.set_defaults(func=cmd_promote)

    p = sub.add_parser("analyze", help="体检宫殿")
    add_vault(p); p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_analyze)

    p = sub.add_parser("link", help="按 config [links] 重建软链")
    add_vault(p); p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_link)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
