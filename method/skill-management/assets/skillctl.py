#!/usr/bin/env python3
"""skillctl —— 多来源 skill 中央管理工具（通用版，随 skill-management 方法论分发）

放置约定： <root>/scripts/skillctl.py ，单一事实源 <root>/registry.yaml
物理结构： <root>/<source>/<category>/<skill>/   —— 来源 → 分类 → skill；分类可多级（如 media/audio），据 SKILL.md 递归识别
  含 .git 的来源目录即「会发布的仓库」，其 .gitignore 由本工具维护（整目录入库，仅挡垃圾）

用法（不带参数 = stats 总览）:
  python3 scripts/skillctl.py               一眼总览：来源/分类/层级分布 + 挂载健康 + 项目级 skill
  python3 scripts/skillctl.py sync          重建：扁平镜像 <root>/skills + 各 mounts 软链 + git 来源的 .gitignore
  python3 scripts/skillctl.py doctor        体检：缺 SKILL.md / registry↔磁盘漂移 / 来源串味 / 孤儿·断链
  python3 scripts/skillctl.py mount [项目]   opt-in：把 tier:project skill 软链进项目 .claude/skills/（默认 sync 不挂）
  python3 scripts/skillctl.py unmount [项目] 撤销上面的项目软链

registry.yaml 需含： mounts(列表) / sources / projects(可选) / categories / skills，详见同目录 registry.example.yaml
"""
import os, re, sys, shutil

ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIRROR = os.path.join(ROOT, "skills")
REG    = os.path.join(ROOT, "registry.yaml")

# tier:project 默认只「声明 + 移出全局」，不挂进项目目录。置 True 后 sync 会顺带挂载；
# 也可随时 `skillctl mount <项目>` 一键挂载（与本开关无关）。
SYNC_AUTOMOUNT_PROJECTS = False

C = dict(grn="\033[32m", red="\033[31m", yel="\033[33m", dim="\033[2m", rst="\033[0m")
def c(s, col): return f"{C[col]}{s}{C['rst']}"


def load_registry():
    txt = open(REG, encoding="utf-8").read()
    mounts, sources, projects, sec = [], [], {}, None
    for ln in txt.splitlines():
        h = re.match(r'^(mounts|sources|projects|categories|skills):', ln)
        if h: sec = h.group(1); continue
        if sec == "mounts":
            m = re.match(r'^\s*-\s*(.+?)\s*(?:#.*)?$', ln)
            if m: mounts.append(os.path.expanduser(m.group(1).strip().strip('"\'')))
        elif sec == "sources":
            m = re.match(r'^\s{2}([A-Za-z0-9_-]+):\s*"', ln)
            if m: sources.append(m.group(1))
        elif sec == "projects":
            m = re.match(r'^\s{2}([A-Za-z0-9_-]+):\s*"([^"]+)"', ln)
            if m: projects[m.group(1)] = os.path.expanduser(m.group(2))
    skills = {}
    for m in re.finditer(
        r'^\s{2}([A-Za-z0-9_-]+):\s*\{source:\s*([A-Za-z0-9_-]+),\s*'
        r'category:\s*([A-Za-z0-9_/-]+),\s*tier:\s*([A-Za-z0-9_-]+)', txt, re.M):
        name, src, cat, tier = m.groups()
        skills[name] = dict(source=src, category=cat, tier=tier, project=None)
    # project: <名> —— tier:project 的归属项目（喂 stats 聚合 + mount 目标选择，见 projects: 段）
    for m in re.finditer(r'^\s{2}([A-Za-z0-9_-]+):\s*\{[^}]*\bproject:\s*([A-Za-z0-9_-]+)', txt, re.M):
        if m.group(1) in skills:
            skills[m.group(1)]["project"] = m.group(2)
    return mounts, sources, projects, skills


def skill_dir(info, name):
    return os.path.join(ROOT, info["source"], info["category"], name)


def _relink(dst, target):
    if os.path.islink(dst): os.unlink(dst)
    elif os.path.isdir(dst): shutil.rmtree(dst)
    elif os.path.exists(dst): os.remove(dst)
    os.symlink(target, dst)


def sync():
    mounts, sources, projects, skills = load_registry()
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

    # 4) 项目级 skill（tier: project）——默认只「声明 + 移出全局」（不在 linked，上面各 mount 的 prune 已把它拿掉）；
    #    SYNC_AUTOMOUNT_PROJECTS=True 才顺带挂进各项目目录，否则仅提示。
    proj = [n for n, i in skills.items() if i["tier"] == "project"]
    if SYNC_AUTOMOUNT_PROJECTS:
        mount(projects, skills)
    elif proj:
        print(c(f"· 项目级 skill {len(proj)} 个：仅声明、已移出全局（未挂载）；"
                f"`skillctl mount <项目>` 一键推进项目", "dim"))


def project_skill_dir(projects, pname):
    return os.path.join(projects[pname], ".claude", "skills")


def _project_targets(skills, only=None):
    """tier:project 的 skill 按归属项目分组 → {项目名: [skill,...]}。only 指定时只取该项目。"""
    targets = {}
    for n, i in skills.items():
        if i["tier"] == "project" and i.get("project"):
            targets.setdefault(i["project"], []).append(n)
    return {only: targets.get(only, [])} if only else targets


def mount(projects=None, skills=None, only=None):
    """opt-in：把 tier:project skill 软链进各自项目目录的 .claude/skills/（真身仍在来源目录，单一事实源不破）。
    支持非 git 目录（不卡 git 根）；默认 sync 不调用，需显式 `skillctl mount` 或开 SYNC_AUTOMOUNT_PROJECTS。
    注：Claude 原生从 git 根读 project skill，要让 Claude 自动加载，projects: 路径须指向 git 根。"""
    if skills is None:
        _, _, projects, skills = load_registry()
    targets = _project_targets(skills, only)
    if not any(targets.values()):
        print(c(f"无 tier:project skill{('（项目 ' + only + '）') if only else ''}", "dim")); return
    for pname, names in sorted(targets.items()):
        if pname not in projects:
            print(c(f"✗ 项目 {pname} 未在 registry projects: 声明，跳过 {len(names)} 个", "red")); continue
        base = project_skill_dir(projects, pname)
        os.makedirs(base, exist_ok=True)
        for n in sorted(names):
            _relink(os.path.join(base, n), skill_dir(skills[n], n))
        pruned = []  # 清孤儿：指向本 root 但已不属该项目的旧软链
        for e in os.listdir(base):
            p = os.path.join(base, e)
            if os.path.islink(p) and os.path.abspath(os.readlink(p)).startswith(ROOT) and e not in names:
                os.unlink(p); pruned.append(e)
        print(c(f"✓ mount {pname} → {base}：{len(names)} 个" +
                (f"，prune {len(pruned)}" if pruned else ""), "grn"))


def unmount(projects=None, skills=None, only=None):
    """撤销 mount 建的项目软链（只动指向本 root 的软链，不碰手放的）。"""
    if skills is None:
        _, _, projects, skills = load_registry()
    targets = _project_targets(skills, only)
    for pname in sorted(targets):
        if pname not in projects: continue
        base = project_skill_dir(projects, pname)
        if not os.path.isdir(base): continue
        rm = []
        for e in os.listdir(base):
            p = os.path.join(base, e)
            if os.path.islink(p) and os.path.abspath(os.readlink(p)).startswith(ROOT):
                os.unlink(p); rm.append(e)
        print(c(f"✓ unmount {pname}：移除 {len(rm)} 个软链", "grn"))


def stats():
    mounts, sources, projects, skills = load_registry()
    if not skills: print("registry 为空"); return
    by_src, by_cat = {}, {}
    by_tier = {"core": 0, "extra": 0, "project": 0, "parked": 0}
    by_proj = {}
    for i in skills.values():
        by_src[i["source"]] = by_src.get(i["source"], 0) + 1
        by_cat[i["category"]] = by_cat.get(i["category"], 0) + 1
        by_tier[i["tier"]] = by_tier.get(i["tier"], 0) + 1
        if i.get("project"):
            by_proj[i["project"]] = by_proj.get(i["project"], 0) + 1

    def bar(n, mx, w=22):
        f = round(n / mx * w) if mx else 0
        return c("█" * f, "grn") + c("░" * (w - f), "dim")

    print("\n" + c("━━━ Skill 生态总览 " + "━" * 30, "grn"))
    print(f"  {len(skills)} skill · {len(sources)} 来源 · {len(by_cat)} 分类 · "
          f"core {by_tier['core']} / extra {by_tier['extra']} / "
          f"project {by_tier['project']} / parked {by_tier['parked']}")
    print(c("\n  来源", "dim")); mxs = max(by_src.values())
    for s in sources:
        n = by_src.get(s, 0)
        tag = "会 push" if os.path.isdir(os.path.join(ROOT, s, ".git")) else "本地"
        print(f"    {s:<12}{n:>3}  {bar(n, mxs)}  {c(tag, 'dim')}")
    print(c("\n  分类（按 skill 数）", "dim")); mxc = max(by_cat.values())
    for k in sorted(by_cat, key=lambda x: (-by_cat[x], x)):
        print(f"    {k:<14}{by_cat[k]:>3}  {bar(by_cat[k], mxc)}")
    # 项目级 skill（tier:project）按归属项目聚合 + 挂载状态
    if by_proj:
        print(c("\n  项目级 skill（tier:project · 已移出全局，默认仅声明）", "dim"))
        for p in sorted(by_proj, key=lambda x: (-by_proj[x], x)):
            base = project_skill_dir(projects, p) if p in projects else ""
            mounted = 0
            if base and os.path.isdir(base):
                mounted = sum(1 for e in os.listdir(base)
                              if os.path.islink(os.path.join(base, e))
                              and os.path.abspath(os.readlink(os.path.join(base, e))).startswith(ROOT))
            decl = "已声明路径" if p in projects else c("未声明路径", "yel")
            ms = c(f"已挂载 {mounted}/{by_proj[p]}", "grn") if mounted else c("仅声明·未挂载", "dim")
            print(f"    {p:<14}{by_proj[p]:>3}  {decl} · {ms}")
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
    mounts, sources, projects, skills = load_registry()
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
    # tier:project：必须带 project 字段且已在 projects: 声明；且不该残留在任一全局 mount
    for n, i in skills.items():
        if i["tier"] != "project": continue
        if not i.get("project"): problems.append(f"tier:project 缺 project 字段: {n}")
        elif i["project"] not in projects: problems.append(f"project 未在 projects: 声明: {n} → {i['project']}")
        for mnt in mounts:
            if os.path.islink(os.path.join(mnt, n)):
                problems.append(f"tier:project 仍残留全局挂载 {mnt}（跑 sync 清理）: {n}")
    print(c(f"\ndoctor {len(skills)} skill / {len(sources)} 来源 / {len(mounts)} 挂载", "dim"))
    if not problems: print(c("✓ 全部通过，无漂移", "grn")); return 0
    print(c(f"✗ {len(problems)} 处问题：", "red"))
    for p in problems: print("   - " + p)
    return 1


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "stats"
    arg = sys.argv[2] if len(sys.argv) > 2 else None
    if cmd == "sync": sync()
    elif cmd == "doctor": sys.exit(doctor())
    elif cmd == "stats": stats()
    elif cmd == "mount": mount(only=arg)
    elif cmd == "unmount": unmount(only=arg)
    else: print(__doc__); sys.exit(2)


if __name__ == "__main__":
    main()
