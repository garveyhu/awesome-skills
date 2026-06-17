#!/usr/bin/env python3
"""通用 ComfyUI 批量生图引擎 —— 读各资产文件夹下的 assets.json,照计划无人值守出图。

设计:
- **数据与逻辑分离**:每个资产文件夹放一个 `assets.json`(生成内容/提示词/出图配置/
  用哪个工作流/后处理),本脚本只啃 JSON,不内嵌任何项目知识 → 任何项目可复用。
- **容错**:单条超时/报错只记一笔并继续;每条之间 `free` 释放内存。
- **断点续跑(默认)**:按磁盘已有产物数,每条只补到目标变体数 → 中断/崩溃后重跑自动接上,不重出;
  `--no-resume` 强制忽略已有、每条重出 variants 张。
- **多变体**:每条按 variants 出 N 张(不同 seed),早上挑。
- **不自动定稿**:只生成候选,status 不改 done(留给人审)。
- **好看的终端 UI**:边框面板 + 进度条 + 实时秒表 + 成功/失败/跳过统计 + ETA/速率。

每条任务最终翻译成一句 `comfy.py` 调用(t2i builder 或 raw <工作流>);生成/抠图/像素化
都复用 skill 既有能力(--keyflat / --pixelize / --var / --seed)。

assets.json 结构与用法见 scripts/batch/README.md。
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import random
import subprocess
import sys
import tempfile
import time

C = {"g": "\033[32m", "r": "\033[31m", "y": "\033[33m", "b": "\033[36m", "m": "\033[35m",
     "dim": "\033[2m", "bold": "\033[1m", "x": "\033[0m"}
SPIN = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
W = 64  # 面板内宽


def _vlen(s: str) -> int:
    """可见宽度(剥 ANSI,中文算 2 宽)。"""
    import re
    t = re.sub(r"\033\[[0-9;]*m", "", s)
    return sum(2 if ord(ch) > 0x2E7F else 1 for ch in t)


def _pad(s: str, w: int = W) -> str:
    """裁到可见宽度 w(含中文按 2 宽、跳过 ANSI)再右补空格 —— 防止长文本撑破边框。"""
    if _vlen(s) <= w:
        return s + " " * (w - _vlen(s))
    import re
    out, width, i = [], 0, 0
    while i < len(s):
        m = re.match(r"\033\[[0-9;]*m", s[i:])
        if m:
            out.append(m.group()); i += m.end(); continue
        ch = s[i]; cw = 2 if ord(ch) > 0x2E7F else 1
        if width + cw > w - 1:  # 留 1 宽给省略号
            break
        out.append(ch); width += cw; i += 1
    return "".join(out) + "…\033[0m" + " " * max(0, w - width - 1)


def _bar(frac: float, n: int = 30) -> str:
    f = int(frac * n)
    return "█" * f + "░" * (n - f)


class UI:
    def __init__(self, log_path: str):
        self.tty = sys.stdout.isatty()
        self.log = open(log_path, "a")
        self.drawn = 0

    def col(self, k, s):
        return f"{C[k]}{s}{C['x']}" if self.tty else s

    def logline(self, s):
        self.log.write(s + "\n"); self.log.flush()

    def panel(self, title, lines):
        if not self.tty:
            return
        box = ["╭─ " + title + " " + "─" * max(0, W - _vlen(title) - 3) + "╮"]
        for ln in lines:
            box.append("│ " + _pad(ln, W - 2) + " │")
        box.append("╰" + "─" * W + "╯")
        if self.drawn:
            sys.stdout.write(f"\033[{self.drawn}A\033[J")
        sys.stdout.write("\n".join(box) + "\n")
        sys.stdout.flush()
        self.drawn = len(box)

    def close(self):
        self.log.close()


# ---- 配置 ------------------------------------------------------------------
def discover(root):
    out = []
    for p in sorted(glob.glob(os.path.join(root, "**", "assets.json"), recursive=True)):
        try:
            out.append({"path": p, "data": json.load(open(p))})
        except Exception as e:
            print(f"⚠ 跳过坏配置 {p}: {e}")
    return out


def merge(defaults, item):
    cfg = dict(defaults or {})
    cfg.update({k: v for k, v in item.items() if k not in ("name", "status", "prompt", "vars")})
    # vars 也合并:共享值(如参考图 image)放 defaults.vars,逐条值(如动作 prompt)放 item.vars
    cfg["vars"] = {**((defaults or {}).get("vars") or {}), **(item.get("vars") or {})}
    return cfg


def build_prompt(cfg, item):
    parts = [cfg.get("style_prefix"), item.get("prompt"), cfg.get("suffix")]
    return ", ".join(p.strip().strip(",") for p in parts if p)


def normalize_names(root):
    """把残留的 ComfyUI 计数名 `*-vK_NNNNN_.png` 统一归一成干净的 `*-vK.png`。
    覆盖"生成成功但下载步骤报错没改名"等遗留情况,保证续跑命名一致。"""
    import re
    for f in glob.glob(os.path.join(root, "**", "*.png"), recursive=True):
        m = re.match(r"(.*-v\d+)_\d+_\.png$", os.path.basename(f))
        if not m:
            continue
        dst = os.path.join(os.path.dirname(f), m.group(1) + ".png")
        try:
            if os.path.abspath(dst) == os.path.abspath(f):
                continue
            if os.path.exists(dst):     # 已有干净名 → 删多余计数版
                os.remove(f)
            else:
                os.replace(f, dst)
        except OSError:
            pass


def clear_history(host):
    """清空 ComfyUI 历史。产物改名后,历史里 `*_00001_` 的引用会指不到文件、预览失效,
    跑完清掉最干净(真资产都在 assets/ 里,历史只是临时运行日志)。"""
    import urllib.request
    try:
        req = urllib.request.Request(host.rstrip("/") + "/history",
                                     data=b'{"clear": true}',
                                     headers={"Content-Type": "application/json"}, method="POST")
        urllib.request.urlopen(req, timeout=10)
        return True
    except Exception:
        return False


def build_tasks(configs, args):
    tasks, skipped = [], 0
    for c in configs:
        d = c["data"]; cat = d.get("category", "")
        if args.only and not any(o in cat for o in args.only):
            continue
        defaults = d.get("defaults", {}); out_prefix = d.get("out_prefix", cat)
        for item in d.get("items", []):
            status = item.get("status", "todo")
            is_char = item.get("type") == "character" or merge(defaults, item).get("type") == "character"
            if status == "skip" or (is_char and not args.with_chars):
                skipped += 1; continue
            if status == "done" and not args.redo:
                skipped += 1; continue
            cfg = merge(defaults, item)
            target = args.variants if args.variants else int(cfg.get("variants", 1))
            outdir = os.path.join(args.root, out_prefix)
            slots = []                                  # 按"槽位"查缺补缺(每变体固定名 name-vK)
            for v in range(1, target + 1):
                stem = os.path.join(outdir, f"{item['name']}-v{v}")
                exists = glob.glob(stem + "_*.png") or glob.glob(stem + ".png")
                if args.no_resume or args.redo or not exists:
                    slots.append(v)                     # 该槽缺(或强制重出)→ 补
            if not slots:                               # 各槽都在,跳过(续跑命中)
                skipped += 1; continue
            tasks.append({"cat": cat, "name": item["name"], "out_prefix": out_prefix,
                          "cfg": cfg, "item": item, "target": target, "slots": slots})
    return tasks, skipped


_uploaded = {}  # 本地参考图路径 → 已上传的服务端文件名(避免重复上传)


def _resolve_refs(vars_dict, args):
    """把 vars 里指向**本地图片**的值自动上传到 ComfyUI,替换成服务端文件名。
    这样 char-edit 的参考图直接写在 assets.json 里(相对 assets 根或绝对路径),
    一条批量命令自动上传 + 引用,不用手动先 upload。非本地路径的值原样透传。"""
    out = dict(vars_dict or {})
    for k, v in list(out.items()):
        if not isinstance(v, str):
            continue
        cand = v if os.path.isabs(v) else os.path.join(args.root, v)
        if not os.path.isfile(cand):
            continue                              # 不是本地文件 → 当普通字符串/已是服务端名
        if cand in _uploaded:
            out[k] = _uploaded[cand]; continue
        r = subprocess.run([args.python, args.comfy, "upload", cand], capture_output=True, text=True)
        name = (r.stdout.strip().splitlines() or [os.path.basename(cand)])[-1]
        _uploaded[cand] = name; out[k] = name
    return out


def cmd_for(task, slot, args):
    cfg, item = task["cfg"], task["item"]
    # 默认随机 seed:每张变体不同,删了重生成也给一张**新的**(你删它就是想换一张)。
    # 只有显式 --seed-base 时才用确定性种子(可复现实验)。
    seed = (args.seed_base + slot - 1) if args.seed_base is not None else random.randint(1, 2_147_483_646)
    base = [args.python, args.comfy]
    wf = cfg.get("workflow", "t2i")
    if wf == "t2i":
        size = cfg.get("size", [768, 768])
        cmd = base + ["t2i", build_prompt(cfg, item), "--w", str(size[0]), "--h", str(size[1]), "--seed", str(seed)]
    elif wf in ("i2i", "i2v"):
        # 路由到 catalog 任务命令(用 skill 的 canonical 工作流,无需项目放副本)。
        # image 是本地路径(相对 assets 根),i2i/i2v 命令自己上传。
        v = cfg.get("vars") or {}
        img = v.get("image", "")
        if img and not os.path.isabs(img):
            img = os.path.join(args.root, img)
        cmd = base + [wf, img, v.get("prompt", ""), "--seed", str(seed)]
    else:
        path = wf if (os.path.isabs(wf) or wf.endswith(".json")) else os.path.join(args.workflows_dir, f"{wf}.json")
        cmd = base + ["raw", path, "--seed", str(seed)]
        for k, v in _resolve_refs(cfg.get("vars") or {}, args).items():
            cmd += ["--var", f"{k}={v}"]
    # 每变体固定文件名 name-vK → 删某张重跑只补那一槽,文件名也回到那一槽
    cmd += ["--prefix", f"{task['out_prefix']}/{task['name']}-v{slot}", "--timeout", str(args.timeout)]
    if args.project:
        cmd += ["--project", args.project]
    mt = cfg.get("matte")
    if mt:                                       # 神经抠图(模型),复杂主体更稳
        m = mt if isinstance(mt, dict) else {}
        cmd += ["--matte", "--matte-model", m.get("model", "BiRefNet.safetensors")]
        if m.get("text"):                       # 文字选取抠图(英文名词)替代自动抠
            cmd += ["--matte-text", m["text"]]
        if m.get("suffix"):
            cmd += ["--matte-suffix", m["suffix"]]
        if m.get("keep_original") is False:     # 默认保留原图;显式 false 才覆盖
            cmd += ["--matte-overwrite-original"]
        if m.get("mode"):                       # overwrite(默认)/ increment
            cmd += ["--matte-mode", m["mode"]]
    kf = cfg.get("keyflat")
    if kf and not mt:                            # color-key(纯色底快抠);matte 优先
        cmd += ["--keyflat", "--key-tol", str(kf.get("tol", 70))]
        if kf.get("bg"):
            cmd += ["--key-bg", kf["bg"]]
        if kf.get("global"):
            cmd += ["--key-global"]
    px = cfg.get("pixelize")
    if px:
        cmd += ["--pixelize", "--px", str(px.get("px", 96)), "--colors", str(px.get("colors", 0))]
    return cmd


# ---- 主流程 ----------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="通用 ComfyUI 批量生图(读 assets.json)")
    ap.add_argument("root")
    ap.add_argument("--workflows-dir", default="")
    ap.add_argument("--project", default=os.environ.get("COMFY_PROJECT", ""))
    ap.add_argument("--variants", type=int, default=0, help="每条出几张(覆盖配置;0=用配置)")
    ap.add_argument("--only", default="", help="只跑类别含这些子串(逗号分隔)")
    ap.add_argument("--redo", action="store_true")
    ap.add_argument("--with-chars", action="store_true")
    ap.add_argument("--no-resume", action="store_true", help="不续跑:忽略磁盘已有变体,每条都重出 variants 张(默认续跑=接上次进度,只补缺的)")
    ap.add_argument("--seed-base", type=int, default=None,
                    help="固定种子基(可复现:seed=base+槽位);默认随机=每次/重生成都出新图")
    ap.add_argument("--clear-history", action="store_true",
                    help="跑完清空 ComfyUI 历史(默认不清,保持两边一致)")
    ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--python", default=sys.executable)
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--comfy", default=os.path.join(here, "..", "comfy.py"))
    args = ap.parse_args()
    args.only = [s for s in args.only.split(",") if s]

    if not args.dry_run:
        normalize_names(args.root)        # 真跑前先归一遗留的计数名 → 干净 -vK.png
    configs = discover(args.root)
    tasks, skipped = build_tasks(configs, args)
    total = sum(len(t["slots"]) for t in tasks)
    ui = UI(os.path.join(args.root, "batch.log"))

    print(C["bold"] + f"\n🎨 批量生图:{len(tasks)} 条资源 × 变体 = {total} 张  ·  跳过 {skipped} 条(已完成/角色)" + C["x"])
    if args.dry_run:
        for t in tasks:
            partial = len(t["slots"]) < t["target"]
            _hv = f"  (补槽 v{','.join(map(str,t['slots']))} / 共 {t['target']})" if partial else ""
            c = t["cfg"]
            sz = c.get("size", [768, 768])
            tags = [c.get("workflow", "t2i"), f"{sz[0]}x{sz[1]}",
                    "matte" if c.get("matte") else ("keyflat" if c.get("keyflat") else "no-key")]
            if c.get("pixelize"):
                tags.append(f"pixelize px{c['pixelize'].get('px')}/{c['pixelize'].get('colors')}c")
            body = build_prompt(c, t["item"]) if c.get("workflow", "t2i") == "t2i" else str(t["item"].get("vars", {}))
            print(ui.col("y", f"  {t['cat']}/{t['name']}  ×{len(t['slots'])}{_hv}"))
            print(ui.col("dim", f"      [{' · '.join(tags)}]  {body[:88]}"))
        print(ui.col("bold", f"\n[dry-run] 共 {total} 张,未执行。去掉 --dry-run 即开跑。"))
        ui.close(); return

    done = fail = 0
    per_cat = {}
    recent = []
    t0 = time.time()
    for t in tasks:
        per_cat.setdefault(t["cat"], [0, 0])
        tgt = t["target"]
        for slot in t["slots"]:                     # 只补缺的槽位
            cmd = cmd_for(t, slot, args)
            ui.logline(f"[{done+fail+1}/{total}] {t['cat']}/{t['name']} v{slot}")
            tstart = time.time(); rc = None; out = ""
            with tempfile.TemporaryFile(mode="w+") as tf:
                p = subprocess.Popen(cmd, stdout=tf, stderr=subprocess.STDOUT, text=True)
                sp = 0
                while p.poll() is None:
                    el = time.time() - tstart
                    if el > args.timeout + 120:
                        p.kill(); break
                    done_frac = (done + fail) / total if total else 0
                    avg = (time.time() - t0) / max(done + fail, 1)
                    eta = int(avg * (total - done - fail))
                    rate = (done + fail) / max((time.time() - t0) / 60, 0.01)
                    header = ui.col("bold", "🎨 Quiver 资产批量生成")
                    lines = [
                        f"{ui.col('b', _bar(done_frac))}  {int(done_frac*100):>3}%   {done+fail}/{total}",
                        f"{ui.col('g', f'✓ {done} 成功')}   {ui.col('r', f'✗ {fail} 失败')}   {ui.col('dim', f'⏭ {skipped} 跳过')}    ⏱ {int((time.time()-t0))//60}m  剩~{eta//60}m  ({rate:.1f}/分)",
                        "─" * (W - 2),
                        f"{ui.col('y', SPIN[sp % len(SPIN)])} {ui.col('bold', t['cat']+'/'+t['name'])}  变体 {slot}/{tgt}  生成中 {int(el)}s",
                        "─" * (W - 2),
                    ] + recent[-8:]
                    ui.panel(header, lines)
                    time.sleep(0.5); sp += 1
                rc = p.returncode
                tf.seek(0); out = tf.read()
            ok = rc == 0 and "✓ 完成" in out
            dur = int(time.time() - tstart)
            if ok:
                # ComfyUI 必加 _NNNNN_ 计数后缀;去掉它 → 干净的 name-vK.png(每槽唯一名)
                stem = os.path.join(args.root, t["out_prefix"], f"{t['name']}-v{slot}")
                cands = sorted(glob.glob(stem + "_*.png"), key=os.path.getmtime)
                if cands:
                    try:
                        os.replace(cands[-1], stem + ".png")
                    except OSError:
                        pass
                done += 1; per_cat[t["cat"]][0] += 1
                recent.append(ui.col("g", f"✓ {t['cat']}/{t['name']} v{slot}  {dur}s"))
            else:
                fail += 1
                tail = (out.strip().splitlines()[-1] if out.strip() else "超时/无输出")[:40]
                recent.append(ui.col("r", f"✗ {t['cat']}/{t['name']} v{slot} — {tail}"))
                ui.logline(f"    FAIL rc={rc}: {tail}")
            subprocess.run([args.python, args.comfy, "free"], capture_output=True, timeout=60)

    dur = int(time.time() - t0)
    # 收尾汇总面板
    cat_rows = [f"  {ui.col('dim', cat)}: {v[0]} 张" for cat, v in per_cat.items()]
    ui.panel(ui.col("bold", "✅ 批量生成完成"), [
        f"{ui.col('g', f'✓ {done} 成功')}   {ui.col('r', f'✗ {fail} 失败')}   共 {total} 张",
        f"用时 {dur//60}m{dur%60}s   平均 {dur//max(total,1)}s/张",
        "─" * (W - 2),
    ] + cat_rows + [
        "─" * (W - 2),
        ui.col("dim", "候选已落资产库;早上挑选满意的 → 改 assets.json status=done。"),
    ])
    if not ui.tty:
        print(f"完成 done={done} fail={fail} total={total} dur={dur}s")
    ui.logline(f"DONE done={done} fail={fail} total={total} dur={dur}s")
    json.dump({"done": done, "fail": fail, "total": total, "dur": dur, "per_cat": per_cat},
              open(os.path.join(args.root, "batch-progress.json"), "w"), ensure_ascii=False)
    if args.clear_history:                   # 仅显式要求时才清
        if clear_history(os.environ.get("COMFYUI_HOST", "http://127.0.0.1:8188")):
            ui.logline("已清空 ComfyUI 历史")
    ui.close()


if __name__ == "__main__":
    main()
