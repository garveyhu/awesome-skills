#!/usr/bin/env python3
"""skillctl —— 多来源 skill 中央管理工具（通用版，随 skill-management 方法论分发）

放置约定： <root>/scripts/skillctl.py ，单一事实源 <root>/registry.yaml
物理结构： <root>/<source>/<category>/<skill>/   —— 来源 → 分类 → skill；分类可多级（如 media/audio），据 SKILL.md 递归识别
  含 .git 的来源目录即「会发布的仓库」，其 .gitignore 由本工具维护（整目录入库，仅挡垃圾）

用法（不带参数 = stats 总览）:
  python3 scripts/skillctl.py             一眼总览：来源/分类/层级分布 + 挂载健康
  python3 scripts/skillctl.py sync        重建：扁平镜像 <root>/skills + 各 mounts 软链 + git 来源的 .gitignore
  python3 scripts/skillctl.py doctor      体检：缺 SKILL.md / registry↔磁盘漂移 / 来源串味 / 孤儿·断链

registry.yaml 需含： mounts(列表) / sources / categories / skills，详见同目录 registry.example.yaml
"""
import os, re, sys, shutil

ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIRROR = os.path.join(ROOT, "skills")
REG    = os.path.join(ROOT, "registry.yaml")

C = dict(grn="\033[32m", red="\033[31m", yel="\033[33m", dim="\033[2m", rst="\033[0m")
def c(s, col): return f"{C[col]}{s}{C['rst']}"


def load_registry():
    txt = open(REG, encoding="utf-8").read()
    mounts, sources, sec = [], [], None
    for ln in txt.splitlines():
        h = re.match(r'^(mounts|sources|categories|skills):', ln)
        if h: sec = h.group(1); continue
        if sec == "mounts":
            m = re.match(r'^\s*-\s*(.+?)\s*(?:#.*)?$', ln)
            if m: mounts.append(os.path.expanduser(m.group(1).strip().strip('"\'')))
        elif sec == "sources":
            m = re.match(r'^\s{2}([A-Za-z0-9_-]+):\s*"', ln)
            if m: sources.append(m.group(1))
    skills = {}
    for m in re.finditer(
        r'^\s{2}([A-Za-z0-9_-]+):\s*\{source:\s*([A-Za-z0-9_-]+),\s*'
        r'category:\s*([A-Za-z0-9_/-]+),\s*tier:\s*([A-Za-z0-9_-]+)', txt, re.M):
        name, src, cat, tier = m.groups()
        skills[name] = dict(source=src, category=cat, tier=tier)
    return mounts, sources, skills


def skill_dir(info, name):
    return os.path.join(ROOT, info["source"], info["category"], name)


def _relink(dst, target):
    if os.path.islink(dst): os.unlink(dst)
    elif os.path.isdir(dst): shutil.rmtree(dst)
    elif os.path.exists(dst): os.remove(dst)
    os.symlink(target, dst)


def sync():
    mounts, sources, skills = load_registry()
    core   = {n: i for n, i in skills.items() if i["tier"] == "core"}
    linked = {n: i for n, i in skills.items() if i["tier"] in ("core", "extra")}

    # 1) 扁平镜像（仅 core，相对软链，全量重建）
    if os.path.islink(MIRROR): os.unlink(MIRROR)
    if os.path.isdir(MIRROR): shutil.rmtree(MIRROR)
    os.makedirs(MIRROR)
    for n, i in sorted(core.items()):
        os.symlink(os.path.relpath(skill_dir(i, n), MIRROR), os.path.join(MIRROR, n))
    print(c(f"✓ 扁平镜像 {MIRROR}：{len(core)} 个 core", "grn"))

    # 2) 各 agent 挂载点（core+extra；prune 指向本 root 但已不该在的软链）
    for mnt in mounts:
        os.makedirs(mnt, exist_ok=True)
        made = 0
        for n, i in sorted(linked.items()):
            _relink(os.path.join(mnt, n), skill_dir(i, n)); made += 1
        pruned = []
        for e in os.listdir(mnt):
            p = os.path.join(mnt, e)
            if os.path.islink(p) and os.path.abspath(os.readlink(p)).startswith(ROOT) and e not in linked:
                os.unlink(p); pruned.append(e)
        print(c(f"✓ 挂载 {mnt}：建/更新 {made}，prune {len(pruned)}", "grn"))

    # 3) 含 .git 的来源目录写简化 .gitignore
    for src in sources:
        d = os.path.join(ROOT, src)
        if os.path.isdir(os.path.join(d, ".git")):
            open(os.path.join(d, ".gitignore"), "w", encoding="utf-8").write(
                f"# {src} —— 自动生成 by skillctl；整目录入库，仅忽略垃圾\n"
                "*.skill\n**/.DS_Store\n**/__pycache__/\n")
            print(c(f"✓ {src}/.gitignore 已写", "grn"))


def stats():
    mounts, sources, skills = load_registry()
    if not skills: print("registry 为空"); return
    by_src, by_cat, by_tier = {}, {}, {"core": 0, "extra": 0, "parked": 0}
    for i in skills.values():
        by_src[i["source"]] = by_src.get(i["source"], 0) + 1
        by_cat[i["category"]] = by_cat.get(i["category"], 0) + 1
        by_tier[i["tier"]] = by_tier.get(i["tier"], 0) + 1

    def bar(n, mx, w=22):
        f = round(n / mx * w) if mx else 0
        return c("█" * f, "grn") + c("░" * (w - f), "dim")

    print("\n" + c("━━━ Skill 生态总览 " + "━" * 30, "grn"))
    print(f"  {len(skills)} skill · {len(sources)} 来源 · {len(by_cat)} 分类 · "
          f"core {by_tier['core']} / extra {by_tier['extra']} / parked {by_tier['parked']}")
    print(c("\n  来源", "dim")); mxs = max(by_src.values())
    for s in sources:
        n = by_src.get(s, 0)
        tag = "会 push" if os.path.isdir(os.path.join(ROOT, s, ".git")) else "本地"
        print(f"    {s:<12}{n:>3}  {bar(n, mxs)}  {c(tag, 'dim')}")
    print(c("\n  分类（按 skill 数）", "dim")); mxc = max(by_cat.values())
    for k in sorted(by_cat, key=lambda x: (-by_cat[x], x)):
        print(f"    {k:<14}{by_cat[k]:>3}  {bar(by_cat[k], mxc)}")
    print(c("\n  挂载 & 健康", "dim"))
    mir = len(os.listdir(MIRROR)) if os.path.isdir(MIRROR) else 0
    print(f"    扁平镜像 skills/        {mir:>3} core")
    linked = {n for n, i in skills.items() if i["tier"] in ("core", "extra")}
    for mnt in mounts:
        managed, foreign = 0, []
        if os.path.isdir(mnt):
            for e in sorted(os.listdir(mnt)):
                if e == ".DS_Store": continue
                p = os.path.join(mnt, e)
                if os.path.islink(p) and os.path.abspath(os.readlink(p)).startswith(ROOT): managed += 1
                elif os.path.islink(p) or os.path.isdir(p): foreign.append(e)
        fz = c("✓", "grn") if not foreign else c(f"⚠ foreign: {', '.join(foreign)}", "yel")
        print(f"    {os.path.basename(mnt.rstrip('/')):<14} 受管 {managed:>3}  {fz}")
    parked = [n for n, i in skills.items() if i["tier"] == "parked"]
    if parked: print(f"    parked 仅留存          {len(parked):>3}  {c('· ' + ', '.join(parked), 'dim')}")
    print()


def doctor():
    mounts, sources, skills = load_registry()
    problems = []
    SKIP = {".git", ".gitignore", "README.md", "CATALOG.md", ".DS_Store"}
    for n, i in skills.items():
        d = skill_dir(i, n)
        if not os.path.isdir(d): problems.append(f"缺真身: {i['source']}/{i['category']}/{n}")
        elif not os.path.isfile(os.path.join(d, "SKILL.md")): problems.append(f"缺 SKILL.md: {n}")
    # 磁盘→registry：递归找含 SKILL.md 的目录=skill，category=相对来源去末段（支持任意深度，如 media/audio）
    for src in sources:
        sd = os.path.join(ROOT, src)
        if not os.path.isdir(sd): continue
        for root, dirs, files in os.walk(sd):
            dirs[:] = [d for d in dirs if d not in SKIP and not d.startswith(".")]
            if "SKILL.md" not in files: continue
            rel = os.path.relpath(root, sd)
            parts = rel.split(os.sep)
            s, cat = parts[-1], "/".join(parts[:-1])
            if s not in skills: problems.append(f"未登记: {src}/{rel}")
            elif skills[s]["source"] != src: problems.append(f"来源串味: {s} 在 {src} 但 registry={skills[s]['source']}")
            elif skills[s]["category"] != cat: problems.append(f"分类不一致: {s} 磁盘={cat} registry={skills[s]['category']}")
            dirs[:] = []  # 命中 skill 后不再深入其内部
    core = {n for n, i in skills.items() if i["tier"] == "core"}
    mir = set(os.listdir(MIRROR)) if os.path.isdir(MIRROR) else set()
    for n in core - mir: problems.append(f"镜像缺 core: {n}")
    for n in mir - core: problems.append(f"镜像多出: {n}")
    linked = {n for n, i in skills.items() if i["tier"] in ("core", "extra")}
    for mnt in mounts:
        for n in linked:
            p = os.path.join(mnt, n)
            if not os.path.islink(p): problems.append(f"{mnt} 缺软链: {n}")
            elif not os.path.exists(p): problems.append(f"{mnt} 断链: {n}")
    print(c(f"\ndoctor {len(skills)} skill / {len(sources)} 来源 / {len(mounts)} 挂载", "dim"))
    if not problems: print(c("✓ 全部通过，无漂移", "grn")); return 0
    print(c(f"✗ {len(problems)} 处问题：", "red"))
    for p in problems: print("   - " + p)
    return 1


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "stats"
    if cmd == "sync": sync()
    elif cmd == "doctor": sys.exit(doctor())
    elif cmd == "stats": stats()
    else: print(__doc__); sys.exit(2)


if __name__ == "__main__":
    main()
