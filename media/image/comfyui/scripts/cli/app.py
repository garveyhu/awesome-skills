#!/usr/bin/env python3
"""ComfyUI 自动化 CLI —— 发现库存、生成图片/视频、提交任意工作流。

单一职责：命令行编排层，把 comfy_api(通信) / inventory(发现) / workflows(构建) 串起来。
全程只用标准库；任何 python3 都能跑（推荐用 ComfyUI 自己的 venv 以保持一致）。

环境变量：
  COMFYUI_HOST    默认 http://127.0.0.1:8188
  COMFYUI_OUTPUT  下载产物的本地目录，默认 ./comfy_outputs

示例：
  python comfy.py discover
  python comfy.py t2i "a cinematic photo of a fox in snow" --w 1024 --h 1024
  python comfy.py i2v ./cat.png "the cat slowly turns its head" --length 81
  python comfy.py raw my_api_workflow.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time

from comfy_api import ComfyClient, ComfyError
import inventory as inv_mod
import workflows as wf_mod

OUT_DIR = os.environ.get("COMFYUI_OUTPUT", os.path.join(os.getcwd(), "comfy_outputs"))
# ComfyUI 安装根目录（用于把产物归到它 output/projects/<项目>/ 下，便于汇总查看）
COMFY_HOME = os.environ.get("COMFYUI_HOME", "/Users/links/Coding/Hub/ComfyUI")
# scripts/ 根目录(本文件在 scripts/cli/ 下,上跳一层)
_SCRIPTS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# t2i 在多架构都可用时的优先级（质量/速度权衡）
T2I_PRIORITY = ["zimage", "flux", "checkpoint"]


def _resolve_project(args: argparse.Namespace) -> str | None:
    """每次生成所属的项目名：--project 优先，其次 COMFY_PROJECT 环境变量。"""
    return getattr(args, "project", None) or os.environ.get("COMFY_PROJECT") or None


def _apply_project(args: argparse.Namespace, base_prefix: str) -> str:
    """按项目归档产物。返回带 `projects/<项目>/` 前缀的 SaveImage 前缀（ComfyUI
    原生支持子目录），并把本地下载目录对齐到同一个子目录。

    推荐用法：把 `<ComfyUI>/output/projects/<项目>` 软链到各自代码仓的资源目录
    （如 `<repo>/assets`）。这样 ComfyUI 按前缀写入时会穿过软链**直接落进项目仓**
    （可随 git 提交、便于协作维护），同时在 ComfyUI 输出目录仍能汇总查看各项目。"""
    project = _resolve_project(args)
    if not project:
        return base_prefix
    full = f"projects/{project}/{base_prefix}"
    if getattr(args, "out", None) in (None, OUT_DIR):
        # 落到与原生 SaveImage 相同的子目录（经软链 = 项目仓资源目录），避免重复/错位
        args.out = os.path.join(COMFY_HOME, "output", os.path.dirname(full))
    return full


def _client() -> ComfyClient:
    c = ComfyClient()
    try:
        c.ping()
    except ComfyError:
        sys.exit(
            f"✗ 连不上 ComfyUI ({c.host})。\n"
            f"  先到 ComfyUI 根目录 ./run.sh 启动，再重试。"
        )
    return c


def _tick(elapsed: float) -> None:
    if int(elapsed) % 10 == 0 and elapsed >= 10:
        print(f"  … 生成中 {int(elapsed)}s", flush=True)


def _run(client: ComfyClient, workflow: dict, out_dir: str, timeout: int) -> list[str]:
    """提交 -> 轮询 -> 下载产物，返回本地文件路径列表。"""
    pid = client.queue_prompt(workflow)
    print(f"已提交 prompt {pid}，等待生成（超时 {timeout}s）…", flush=True)
    t0 = time.time()
    entry = client.wait(pid, poll=2.0, timeout=timeout, on_tick=_tick)
    files = client.collect_outputs(entry, out_dir)
    print(f"✓ 完成，用时 {int(time.time() - t0)}s")
    for f in files:
        print(f"  → {f}")
    if not files:
        print("  (未抓到产物文件；可能是工作流没有 Save 节点)")
    return files


# ---- 子命令 ----------------------------------------------------------------

def cmd_discover(args: argparse.Namespace) -> None:
    client = _client()
    inv = inv_mod.discover(client)
    cache = os.path.join(_SCRIPTS, "..", "state", "inventory.json")
    try:
        os.makedirs(os.path.dirname(cache), exist_ok=True)
        with open(cache, "w") as f:
            json.dump(inv, f, ensure_ascii=False, indent=2)
    except OSError:
        pass
    if args.json:
        print(json.dumps(inv, ensure_ascii=False, indent=2))
    else:
        print(inv_mod.format_report(inv))


def _detect_t2i_family(inv: dict, model: str | None) -> str:
    caps = {c["family"]: c for c in inv["capabilities"] if c["task"] == "t2i"}
    if model:
        low = model.lower()
        if "z_image" in low:
            return "zimage"
        if "flux" in low:
            return "flux"
        if model in inv["checkpoints"]:
            return "checkpoint"
    for fam in T2I_PRIORITY:
        if fam in caps:
            return fam
    sys.exit("✗ 当前库存里没有可用的文生图模型。先在 models/ 放底模，或 discover 查看。")


def _maybe_keyflat(args: argparse.Namespace, files: list[str]) -> None:
    """生成后可选用 color-key 抠平底→透明 PNG(扁平 2D 美术专用,见 keyflat.py)。
    神经抠图对扁平像素/插画会失败,这条是扁平道具/UI 拿透明素材的正路。"""
    if not getattr(args, "keyflat", False):
        return
    import subprocess
    script = os.path.join(_SCRIPTS, "post", "keyflat.py")
    for f in files:
        if not f.lower().endswith(".png"):
            continue
        cmd = [sys.executable, script, f, f, "--tol", str(args.key_tol)]
        if args.key_bg:
            cmd += ["--bg", args.key_bg]
        if getattr(args, "key_global", False):
            cmd += ["--global"]
        subprocess.run(cmd, check=False)


def _maybe_pixelize(args: argparse.Namespace, files: list[str]) -> None:
    """生成(并可选抠图)后,把插画风输出像素化 + 可选统一调色板(见 pixelize.py)。
    跑在 keyflat 之后,以保留透明。"""
    if not getattr(args, "pixelize", False):
        return
    import subprocess
    script = os.path.join(_SCRIPTS, "post", "pixelize.py")
    for f in files:
        if not f.lower().endswith(".png"):
            continue
        subprocess.run([sys.executable, script, f, f, "--px", str(args.px),
                        "--colors", str(args.colors)], check=False)


# ---- 工作流注册表(catalog)+ 统一运行 ----------------------------------------
# 统一:CLI 跑的就是 workflows/<分类>/<工作流>.json,和用户在 ComfyUI 画布用的同一份。
_SKILL = os.path.dirname(_SCRIPTS)
_WF_DIR = os.path.join(_SKILL, "workflows")


def _catalog() -> dict:
    try:
        with open(os.path.join(_WF_DIR, "catalog.json")) as f:
            return json.load(f)
    except OSError:
        return {"defaults": {}, "workflows": {}}


def _apply_vars(workflow: dict, vars_dict: dict) -> None:
    """把 <key> 占位符替换成值;若字段==占位符且值为纯数字,按 int/float 注入(尺寸/步数等)。"""
    for k, v in (vars_dict or {}).items():
        if v is None:
            continue
        ph, sv = f"<{k}>", str(v)
        for node in workflow.values():
            if not isinstance(node, dict):
                continue
            for ik, iv in (node.get("inputs", {}) or {}).items():
                if isinstance(iv, str) and ph in iv:
                    if iv == ph and sv.lstrip("-").isdigit():
                        node["inputs"][ik] = int(sv)
                    elif iv == ph and sv.replace(".", "", 1).lstrip("-").isdigit():
                        node["inputs"][ik] = float(sv)
                    else:
                        node["inputs"][ik] = iv.replace(ph, sv)


def _finalize_and_run(client, workflow, args, vars_dict=None):
    """统一收尾:注入 vars → 覆盖 seed → 改写 Save 前缀(项目归档) → 提交 → 抠图/像素化。返回产物。"""
    _apply_vars(workflow, vars_dict)
    if getattr(args, "seed", None) is not None:
        for node in workflow.values():
            ins = node.get("inputs", {}) if isinstance(node, dict) else {}
            for k in ("seed", "noise_seed"):
                if k in ins and not isinstance(ins[k], list):
                    ins[k] = args.seed
    if _resolve_project(args) or getattr(args, "prefix", None):
        full = _apply_project(args, getattr(args, "prefix", None) or "out")
        for node in workflow.values():
            if isinstance(node, dict) and str(node.get("class_type", "")).startswith("Save"):
                ins = node.setdefault("inputs", {})
                if "filename_prefix" in ins:
                    ins["filename_prefix"] = full
                # 显式 --prefix/--project 优先于"按源图名存"(i2i 的 SaveImageClean 接了 name):
                # 去掉 name 输入,让 filename_prefix 决定文件名(否则出动作集时每张都叫源图名)。
                ins.pop("name", None)
                # 显式命名 → 干净名(覆盖),不要 increment 的 _00001 后缀
                if ins.get("mode") == "increment":
                    ins["mode"] = "overwrite"
    files = _run(client, workflow, args.out, args.timeout)
    _maybe_keyflat(args, files)
    files = _maybe_matte(args, files)
    _maybe_pixelize(args, files)
    return files


def _run_task(task: str, vars_dict: dict, args) -> list[str]:
    """跑 catalog 里 task 的默认工作流(--workflow 可指定别的同任务工作流)。"""
    cat = _catalog()
    name = getattr(args, "workflow", None) or cat.get("defaults", {}).get(task)
    wf = cat.get("workflows", {}).get(name or "")
    if not wf:
        sys.exit(f"✗ catalog 里没有 {task} 的默认工作流(或 --workflow {name} 不存在)")
    path = os.path.join(_WF_DIR, wf.get("file", ""))
    if not os.path.isfile(path):
        sys.exit(f"✗ 工作流文件不存在: {path}(用 comfy.py install {name} 备齐?)")
    client = _client()
    try:
        workflow = _load_as_api(client, path)
    except Exception as e:
        sys.exit(f"✗ 读取/转换工作流失败({name}): {e}")
    if getattr(args, "dry_run", False):
        _apply_vars(workflow, vars_dict)
        print(json.dumps(workflow, ensure_ascii=False, indent=2))
        return []
    print(f"工作流: {name}  ({wf.get('note', '')})")
    return _finalize_and_run(client, workflow, args, vars_dict)


def cmd_t2i(args: argparse.Namespace) -> None:
    """文生图:跑 catalog 默认 t2i 工作流(默认 image_z_image_turbo),注入 prompt/尺寸/seed。"""
    _run_task("t2i", {"prompt": args.prompt, "width": args.w, "height": args.h}, args)


def cmd_i2v(args: argparse.Namespace) -> None:
    """图生视频:跑 catalog 默认 i2v 工作流(默认 video_wan2_2_5B_ti2v),注入图+prompt。"""
    server = _client().upload_image(args.image)
    print(f"已上传起始图: {server}")
    print("⚠ Mac/MPS 上视频较慢,请耐心(可能数分钟)。")
    _run_task("i2v", {"image": server, "prompt": args.prompt or ""}, args)


def cmd_i2i(args: argparse.Namespace) -> None:
    """图生图编辑:跑 catalog 默认 i2i 工作流(默认 image_qwen_image_edit_2511),
    上传待编辑图 + 自然语言编辑指令(英文佳)。"""
    server = _client().upload_image(args.image)
    print(f"已上传待编辑图: {server}")
    _run_task("i2i", {"image": server, "prompt": args.prompt}, args)


def _load_as_api(client: ComfyClient, path: str) -> dict:
    """读工作流文件，UI 格式自动转 API 格式，已是 API 格式则透传。"""
    import ui2api
    with open(path) as f:
        wf = json.load(f)
    if "prompt" in wf and isinstance(wf["prompt"], dict):  # 带包装的导出
        wf = wf["prompt"]
    if "nodes" in wf and "links" in wf:  # UI/Litegraph 格式 → 转 API
        valid = {}
        try:
            full = client.object_info()
            for ct, info in full.items():
                ins = info.get("input", {})
                valid[ct] = set((ins.get("required") or {}).keys()) | set((ins.get("optional") or {}).keys())
        except ComfyError:
            valid = None
        wf = ui2api.convert(wf, valid)
        print(f"（已把 UI 格式转为 API 格式，{len(wf)} 个节点）")
    # 容忍自文档字段：剥掉顶层非节点条目（如 "_comment" 字符串），否则 ComfyUI
    # 校验会把它当节点 dict 处理而 500。
    dropped = [k for k, v in wf.items() if not isinstance(v, dict)]
    if dropped:
        wf = {k: v for k, v in wf.items() if isinstance(v, dict)}
        print(f"（已忽略顶层非节点字段：{', '.join(dropped)}）")
    return wf


def cmd_raw(args: argparse.Namespace) -> None:
    client = _client()
    try:
        workflow = _load_as_api(client, args.workflow)
    except Exception as e:
        sys.exit(f"✗ 读取/转换工作流失败: {e}")
    # --var K=V 占位替换(数字自动按 int/float 注入);seed/项目归档/抠图/像素化统一收尾。
    vd = {}
    for kv in (args.var or []):
        if "=" in kv:
            k, v = kv.split("=", 1)
            vd[k] = v
    _finalize_and_run(client, workflow, args, vd)


def cmd_workflows(args: argparse.Namespace) -> None:
    """列出 catalog 注册的工作流(分类/任务/默认/需要的模型与节点)。"""
    cat = _catalog()
    defaults = cat.get("defaults", {})
    print("任务默认工作流:", {t: n for t, n in defaults.items()})
    for name, w in cat.get("workflows", {}).items():
        star = " ★默认" if defaults.get(w.get("task")) == name else ""
        models = ", ".join(m.get("name", "") for m in w.get("models", []))
        print(f"\n● {name}{star}  [{w.get('category')}/{w.get('task')}]  {w.get('note','')}")
        print(f"   文件: workflows/{w.get('file')}")
        if models:
            print(f"   模型: {models}")
        if w.get("nodes"):
            print(f"   节点: {', '.join(w['nodes'])}")


def cmd_install(args: argparse.Namespace) -> None:
    """按 catalog 给某工作流备齐模型(魔搭下载)+ 提示装节点。新增网上工作流后用它备齐依赖。"""
    import subprocess
    cat = _catalog()
    w = cat.get("workflows", {}).get(args.name)
    if not w:
        sys.exit(f"✗ catalog 没有 {args.name};comfy.py workflows 看列表")
    ms = os.path.expanduser("~/.venvs/current/bin/modelscope")
    hub = os.path.expanduser("~/.cache/huggingface/hub")
    for m in w.get("models", []):
        repo = m.get("ms", "")
        dest = m.get("dir", "").replace("HF_CACHE", hub)
        if not dest.startswith("/"):
            dest = os.path.join(COMFY_HOME, dest)
        if not repo or repo.startswith("("):
            print(f"  ⏭  {m['name']}: {repo or '需手动'}")
            continue
        if os.path.isdir(dest) and os.listdir(dest):
            print(f"  ✓ 已有 {m['name']}")
            continue
        print(f"  ↓ {m['name']} ← {repo}")
        os.makedirs(dest, exist_ok=True)
        cmd = [ms, "download", "--model", repo] + (m.get("files") or []) + ["--local_dir", dest]
        subprocess.run(cmd, check=False)
    if w.get("nodes"):
        print(f"  节点: {', '.join(w['nodes'])}")
        print(f"  → 装节点 + 补丁请跑: COMFYUI_HOME={COMFY_HOME} bash {os.path.join(_SKILL, 'scripts/setup/setup_matting.sh')}(抠图)"
              f" 或手动 clone 到 custom_nodes")
    print("✓ 备齐后重启 ComfyUI 生效")


def cmd_convert(args: argparse.Namespace) -> None:
    import ui2api
    client = _client()
    workflow = _load_as_api(client, args.workflow)
    out = json.dumps(workflow, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w") as f:
            f.write(out)
        print(f"✓ 已写出 {args.output}")
    else:
        print(out)


def cmd_templates(args: argparse.Namespace) -> None:
    tdir = os.path.join(_SCRIPTS, "..", "workflows", "library")
    tdir = os.path.abspath(tdir)
    if not os.path.isdir(tdir):
        sys.exit(f"模板目录不存在: {tdir}")
    files = sorted(f for f in os.listdir(tdir) if f.endswith(".json"))
    print(f"内置 UI 模板（{len(files)} 个，位于 {tdir}）：")
    print("用 `raw <路径>` 直接跑（会自动转 API；需先装好对应模型）\n")
    for f in files:
        print(f"  {f}")
    print("\n另：ComfyUI 自带 443+ 官方模板，见 reference/api-format.md 的路径，同样可用 raw 跑。")


def cmd_matte(args: argparse.Namespace) -> None:
    """用抠图模型把单张图抠成透明 PNG(神经抠图,对像素画/插画/照片都行)。

    流程:上传 → RemoveBackground(模型出 mask)→ InvertMask(留主体)→ JoinImageWithAlpha
    → 下载覆盖。比 color-key 稳:不怕封闭区、不怕主体含底色、不挑背景色。
    模型放 ComfyUI/models/background_removal/(默认 BiRefNet.safetensors)。"""
    client = _client()
    inp = os.path.abspath(args.inp)
    name = client.upload_image(inp)
    # 抠图版按**输出名**(带 -cutout 后缀)存,且落到与原图同一子目录——
    # 这样 ComfyUI 历史里名字 = 我们的输出名(不撞原图名、带后缀),能预览、和原图并排。
    out_abs = os.path.abspath(args.out)
    comfy_out = os.path.join(COMFY_HOME, "output")
    if out_abs.startswith(comfy_out + os.sep):
        save_prefix = os.path.splitext(os.path.relpath(out_abs, comfy_out))[0]
    else:
        save_prefix = "_matte/" + os.path.splitext(os.path.basename(out_abs))[0]
    text = getattr(args, "text", None)
    if text:
        # 文字选取(SAM2 + GroundingDINO):打英文名词抠出指定物体,直接出 RGBA
        wf = {
            "1": {"class_type": "LoadImage", "inputs": {"image": name}},
            "2": {"class_type": "SAM2Segment", "inputs": {"image": ["1", 0], "prompt": text,
                  "sam2_model": "sam2.1_hiera_tiny", "dino_model": "GroundingDINO_SwinT_OGC (694MB)",
                  "device": "CPU", "threshold": 0.3, "mask_blur": 0, "mask_offset": 0,
                  "invert_output": False, "background": "Alpha"}},
            "6": {"class_type": "SaveImageClean", "inputs": {"images": ["2", 0], "filename_prefix": save_prefix}},
        }
    # RMBG 系模型(ComfyUI-RMBG 节点,直接出 RGBA + 细化边缘);其余走内置 BiRefNet 链
    elif args.model in ("RMBG-2.0", "BEN2", "BEN", "INSPYRENET"):
        wf = {
            "1": {"class_type": "LoadImage", "inputs": {"image": name}},
            "2": {"class_type": "RMBG", "inputs": {"image": ["1", 0], "model": args.model,
                  "sensitivity": 1.0, "process_res": 1024, "mask_blur": 0, "mask_offset": 0,
                  "invert_output": False, "refine_foreground": True, "background": "Alpha"}},
            "6": {"class_type": "SaveImageClean", "inputs": {"images": ["2", 0], "filename_prefix": save_prefix}},
        }
    else:
        wf = {
            "1": {"class_type": "LoadImage", "inputs": {"image": name}},
            "2": {"class_type": "LoadBackgroundRemovalModel", "inputs": {"bg_removal_name": args.model}},
            "3": {"class_type": "RemoveBackground", "inputs": {"image": ["1", 0], "bg_removal_model": ["2", 0]}},
            "4": {"class_type": "InvertMask", "inputs": {"mask": ["3", 0]}},
            "5": {"class_type": "JoinImageWithAlpha", "inputs": {"image": ["1", 0], "alpha": ["4", 0]}},
            "6": {"class_type": "SaveImageClean", "inputs": {"images": ["5", 0], "filename_prefix": save_prefix}},
        }
    pid = client.queue_prompt(wf)
    entry = client.wait(pid, poll=1.5, timeout=args.timeout)
    import tempfile
    tmp = tempfile.mkdtemp()
    got = client.collect_outputs(entry, tmp)
    if got:
        os.replace(got[0], args.out)
        print(f"✓ 抠图({'text:'+text if text else args.model})→ {args.out}")
    else:
        print("✗ 抠图无产物")


def _maybe_matte(args: argparse.Namespace, files: list[str]) -> list[str]:
    """生成后用抠图模型抠透明,**默认保留原图**,抠图版加后缀(默认 -cutout)。

    开关:--matte 是否抠;--matte-overwrite-original 不保留原图(直接覆盖);
    --matte-mode overwrite(默认,抠图版同名覆盖)/ increment(保留多版本 -2/-3 递增)。
    返回"抠图版(或原图)"路径列表,供后续 pixelize 接着处理。"""
    if not getattr(args, "matte", False):
        return files
    import subprocess
    comfy = os.path.join(_SCRIPTS, "comfy.py")
    model = getattr(args, "matte_model", None) or "BiRefNet.safetensors"
    suffix = getattr(args, "matte_suffix", None) or "-cutout"
    keep = not getattr(args, "matte_overwrite_original", False)
    mode = getattr(args, "matte_mode", None) or "overwrite"
    text = getattr(args, "matte_text", None)             # 设了则走 SAM2 文字选取
    out = []
    for f in files:
        if not f.lower().endswith(".png"):
            out.append(f); continue
        if not keep:
            cutout = f                                   # 不保留原图 → 覆盖
        elif mode == "increment":                        # 保留多版本,递增不覆盖
            base = f[:-4] + suffix; cutout = base + ".png"; k = 2
            while os.path.exists(cutout):
                cutout = f"{base}-{k}.png"; k += 1
        else:                                            # 默认:抠图版同名覆盖,原图保留
            cutout = f[:-4] + suffix + ".png"
        cmd = [sys.executable, comfy, "matte", f, cutout]
        cmd += ["--text", text] if text else ["--model", model]
        subprocess.run(cmd, check=False)
        out.append(cutout if os.path.exists(cutout) else f)
    return out


def cmd_free(args: argparse.Namespace) -> None:
    client = _client()
    client.free()
    print("✓ 已请求释放模型与内存")


def cmd_init(args: argparse.Namespace) -> None:
    """把这套美术资产管线脚手架到一个项目:复制模板 + 建反向软链 + 打印模型清单。

    让任何装了本 skill 的人,一条命令就把"软链习惯 / 项目结构 / assets.json 格式 /
    工作流 / 批量入口 / 治理规约"全铺进自己的项目,复刻整套工作流。"""
    import shutil
    skill_root = os.path.dirname(_SCRIPTS)
    tdir = os.path.join(skill_root, "templates")
    target = os.path.abspath(args.path)
    name = args.name or os.path.basename(target.rstrip("/"))
    # 1) 复制模板(不覆盖已存在文件)
    copied = 0
    for root, _, files in os.walk(tdir):
        rel = os.path.relpath(root, tdir)
        for f in files:
            dst = os.path.join(target, f) if rel == "." else os.path.join(target, rel, f)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if os.path.exists(dst):
                continue
            shutil.copy2(os.path.join(root, f), dst)
            copied += 1
    for s in ("scripts/comfyui/batch.sh", "scripts/comfyui/setup.sh"):
        p = os.path.join(target, s)
        if os.path.exists(p):
            os.chmod(p, 0o755)
    # 2) 反向软链(ComfyUI output/workflows → 项目)。通用工作流集中在 skill(装到 ComfyUI
    #    默认目录,见 2c);comfy-workflows 这层留给**项目独有**的工作流(画布可编辑、随 git)。
    links = []
    pairs = [(os.path.join(COMFY_HOME, "output", "projects", name), os.path.join(target, "assets")),
             (os.path.join(COMFY_HOME, "user", "default", "workflows", "projects", name),
              os.path.join(target, "comfy-workflows"))]
    for link, tgt in pairs:
        os.makedirs(os.path.dirname(link), exist_ok=True)
        try:
            if os.path.islink(link) or os.path.exists(link):
                os.remove(link)
            os.symlink(tgt, link)
            links.append(f"{link} → {tgt}")
        except OSError as e:
            links.append(f"(软链失败 {link}: {e})")
    # 2b) 安装内置自定义节点(SaveImageClean:存干净名,ComfyUI 历史与项目仓命名一致)
    nodes_src = os.path.join(skill_root, "comfyui-nodes")
    cn_dir = os.path.join(COMFY_HOME, "custom_nodes")
    node_msg = ""
    if os.path.isdir(nodes_src) and os.path.isdir(cn_dir):
        for f in os.listdir(nodes_src):
            src = os.path.join(nodes_src, f)
            dst = os.path.join(cn_dir, f)
            try:
                if os.path.isdir(src):                       # 文件夹包(如 cutout_node,含 web 扩展)
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                elif f.endswith(".py"):
                    shutil.copy2(src, dst)
            except OSError:
                pass
        node_msg = (f"  自定义节点 → {cn_dir}(重启 ComfyUI 生效)\n"
                    f"  ⚠ 抠图整套(ComfyUI-RMBG + 模型 + 依赖)另跑:"
                    f"COMFYUI_HOME={COMFY_HOME} bash {os.path.join(skill_root, 'scripts/setup/setup_matting.sh')}")
    # 2c) 装 canonical 工作流到 ComfyUI 默认工作流目录(CLI 与 canvas 共用同一份)
    wf_src = os.path.join(skill_root, "workflows")
    wf_dst = os.path.join(COMFY_HOME, "user", "default", "workflows")
    wf_msg = ""
    if os.path.isdir(wf_src) and os.path.isdir(os.path.join(COMFY_HOME, "user")):
        os.makedirs(wf_dst, exist_ok=True)
        wn = 0
        for media in ("image", "video", "audio", "3d"):
            md = os.path.join(wf_src, media)
            if not os.path.isdir(md):
                continue
            for f in os.listdir(md):
                if f.endswith(".json") and not f.endswith(".api.json"):
                    try:
                        shutil.copy2(os.path.join(md, f), os.path.join(wf_dst, f))
                        wn += 1
                    except OSError:
                        pass
        wf_msg = f"  canonical 工作流 → {wf_dst}({wn} 个;CLI 与画布共用同一份)"
    # 3) 报告 + 模型清单 + 下一步
    print(f"✓ 已脚手架到 {target}(项目名 {name}),新增 {copied} 个文件")
    for l in links:
        print("  软链:", l)
    if node_msg:
        print(node_msg)
    if wf_msg:
        print(wf_msg)
    mf = os.path.join(skill_root, "manifests", "models.json")
    if os.path.exists(mf):
        m = json.load(open(mf))
        print("\n需要的模型(魔搭国内下,放对 models/<dir>/;用到才装):")
        for x in m.get("models", []):
            print(f"  · [{x['dir']}] {x.get('file','')}  ← {x['ms']}  {x.get('size','')}")
        for x in m.get("custom_nodes", []):
            print(f"  · custom_node {x['repo']}({x['why']})")
    print("\n下一步:")
    print("  1) 装上面的模型 + ComfyUI-GGUF 节点(只用 prop-gen/builder 的话 Qwen 那几个可先不装)")
    print("  2) 填 assets/**/assets.json 的提示词")
    print("  3) 预览:bash scripts/comfyui/batch.sh --dry-run")
    print("  4) 出图:bash scripts/comfyui/batch.sh --variants 3")


def cmd_upload(args: argparse.Namespace) -> None:
    client = _client()
    print(client.upload_image(args.image))


def main() -> None:
    ap = argparse.ArgumentParser(prog="comfy", description="ComfyUI 自动化 CLI")
    sub = ap.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("discover", help="发现当前库存与可用能力")
    d.add_argument("--json", action="store_true", help="输出原始 JSON")
    d.set_defaults(func=cmd_discover)

    t = sub.add_parser("t2i", help="文生图")
    t.add_argument("prompt")
    t.add_argument("--workflow", help="指定工作流(默认用 catalog 的 t2i 默认 image_z_image_turbo)")
    t.add_argument("--w", type=int, default=1024, help="宽,默认1024")
    t.add_argument("--h", type=int, default=1024, help="高,默认1024")
    t.add_argument("--seed", type=int)
    t.add_argument("--prefix", help="保存文件名前缀")
    t.add_argument("--project", help="项目名：产物归到 output/projects/<项目>/（亦读 COMFY_PROJECT）")
    t.add_argument("--keyflat", action="store_true", help="生成后 color-key 抠平底→透明 PNG（扁平 2D 美术专用）")
    t.add_argument("--key-bg", help="抠底背景色 hex（默认取四角众数）")
    t.add_argument("--key-tol", type=int, default=70, help="抠底欧氏容差（默认 70）")
    t.add_argument("--key-global", action="store_true", help="全局色键(进得了封闭区,用于纯洋红底)")
    t.add_argument("--matte", action="store_true", help="用抠图模型抠透明(替代 color-key,复杂主体更稳)")
    t.add_argument("--matte-model", default="BiRefNet.safetensors", help="抠图模型名")
    t.add_argument("--matte-text", default=None, help="文字选取抠图(英文名词);设了则走 SAM2 文字抠,替代自动抠")
    t.add_argument("--matte-suffix", default="-cutout", help="抠图版文件名后缀(默认 -cutout)")
    t.add_argument("--matte-overwrite-original", action="store_true", help="不保留原图,抠图直接覆盖")
    t.add_argument("--matte-mode", choices=["overwrite","increment"], default="overwrite", help="抠图版命名:覆盖(默认)或递增保留多版本")
    t.add_argument("--pixelize", action="store_true", help="像素化+可选统一调色板(插画→真像素)")
    t.add_argument("--px", type=int, default=96, help="像素网格(短边像素数)")
    t.add_argument("--colors", type=int, default=0, help="量化色数(0=不量化)")
    t.add_argument("--out", default=OUT_DIR)
    t.add_argument("--timeout", type=int, default=600)
    t.add_argument("--dry-run", action="store_true", help="只打印工作流不提交")
    t.set_defaults(func=cmd_t2i)

    v = sub.add_parser("i2v", help="图生视频(catalog 默认 video_*)")
    v.add_argument("image", help="本地起始图片路径")
    v.add_argument("prompt", nargs="?", default="", help="运动/画面描述(可选)")
    v.add_argument("--workflow", help="指定工作流(默认 catalog i2v)")
    v.add_argument("--seed", type=int)
    v.add_argument("--prefix")
    v.add_argument("--project", help="项目名:产物归 output/projects/<项目>/")
    v.add_argument("--out", default=OUT_DIR)
    v.add_argument("--timeout", type=int, default=3600)
    v.add_argument("--dry-run", action="store_true")
    v.set_defaults(func=cmd_i2v)

    e = sub.add_parser("i2i", help="图生图编辑(catalog 默认 image_qwen_image_edit_2511)")
    e.add_argument("image", help="待编辑图片路径")
    e.add_argument("prompt", help="编辑指令(英文佳,如 change sky to sunset)")
    e.add_argument("--workflow", help="指定工作流(默认 catalog i2i)")
    e.add_argument("--seed", type=int)
    e.add_argument("--prefix")
    e.add_argument("--project")
    e.add_argument("--keyflat", action="store_true", help="生成后 color-key 抠平底→透明(扁平美术)")
    e.add_argument("--key-bg", help="抠底背景色 hex(默认取四角众数)")
    e.add_argument("--key-tol", type=int, default=70)
    e.add_argument("--key-global", action="store_true", help="全局色键(纯洋红底)")
    e.add_argument("--matte", action="store_true", help="神经抠图抠透明(复杂主体)")
    e.add_argument("--matte-model", default="RMBG-2.0", help="抠图模型名(默认 RMBG-2.0)")
    e.add_argument("--matte-text", default=None, help="文字选取抠图(英文名词,如 dress)")
    e.add_argument("--matte-suffix", default="-cutout", help="抠图版文件名后缀")
    e.add_argument("--matte-overwrite-original", action="store_true", help="不保留原图")
    e.add_argument("--matte-mode", choices=["overwrite", "increment"], default="overwrite")
    e.add_argument("--pixelize", action="store_true", help="像素化+统一调色板")
    e.add_argument("--px", type=int, default=96)
    e.add_argument("--colors", type=int, default=0)
    e.add_argument("--out", default=OUT_DIR)
    e.add_argument("--timeout", type=int, default=600)
    e.add_argument("--dry-run", action="store_true")
    e.set_defaults(func=cmd_i2i)

    r = sub.add_parser("raw", help="提交工作流 JSON（UI 格式自动转 API；自定义/项目工作流走这条）")
    r.add_argument("workflow", help="工作流 .json 路径（UI 或 API 格式均可）")
    r.add_argument("--var", action="append", metavar="K=V",
                   help="把工作流里所有 <K> 占位符替换成 V（可多次，如 --var object=\"a wooden barrel\"）")
    r.add_argument("--seed", type=int, help="覆盖工作流里所有 seed/noise_seed（批量出变体用）")
    r.add_argument("--project", help="项目名：改写保存前缀为 projects/<项目>/…，产物归项目资产库")
    r.add_argument("--prefix", help="保存子目录/名（配合 --project，如 props/decor/anvil）")
    r.add_argument("--keyflat", action="store_true", help="生成后 color-key 抠平底→透明 PNG（扁平 2D 美术专用）")
    r.add_argument("--key-bg", help="抠底背景色 hex（默认取四角众数）")
    r.add_argument("--key-tol", type=int, default=70, help="抠底欧氏容差（默认 70）")
    r.add_argument("--key-global", action="store_true", help="全局色键(进得了封闭区,用于纯洋红底)")
    r.add_argument("--matte", action="store_true", help="用抠图模型抠透明(替代 color-key,复杂主体更稳)")
    r.add_argument("--matte-model", default="BiRefNet.safetensors", help="抠图模型名")
    r.add_argument("--matte-text", default=None, help="文字选取抠图(英文名词);设了则走 SAM2 文字抠,替代自动抠")
    r.add_argument("--matte-suffix", default="-cutout", help="抠图版文件名后缀(默认 -cutout)")
    r.add_argument("--matte-overwrite-original", action="store_true", help="不保留原图,抠图直接覆盖")
    r.add_argument("--matte-mode", choices=["overwrite","increment"], default="overwrite", help="抠图版命名:覆盖(默认)或递增保留多版本")
    r.add_argument("--pixelize", action="store_true", help="像素化+可选统一调色板(插画→真像素)")
    r.add_argument("--px", type=int, default=96, help="像素网格(短边像素数)")
    r.add_argument("--colors", type=int, default=0, help="量化色数(0=不量化)")
    r.add_argument("--out", default=OUT_DIR)
    r.add_argument("--timeout", type=int, default=3600)
    r.set_defaults(func=cmd_raw)

    c = sub.add_parser("convert", help="把 UI 格式工作流转成 API 格式（不执行）")
    c.add_argument("workflow")
    c.add_argument("-o", "--output", help="输出路径，缺省打印到 stdout")
    c.set_defaults(func=cmd_convert)

    tp = sub.add_parser("templates", help="列出内置 UI 模板")
    tp.set_defaults(func=cmd_templates)

    u = sub.add_parser("upload", help="上传图片到 ComfyUI input 目录")
    u.add_argument("image")
    u.set_defaults(func=cmd_upload)

    fr = sub.add_parser("free", help="释放模型与内存（大任务之间用）")
    fr.set_defaults(func=cmd_free)

    mt = sub.add_parser("matte", help="用抠图模型把单张图抠成透明(神经抠图,比 color-key 稳)")
    mt.add_argument("inp"); mt.add_argument("out")
    mt.add_argument("--model", default="BiRefNet.safetensors", help="models/background_removal/ 下的抠图模型")
    mt.add_argument("--text", help="文字选取(SAM2+GroundingDINO):打英文名词如 dress/person,抠出该物体")
    mt.add_argument("--timeout", type=int, default=300)
    mt.set_defaults(func=cmd_matte)

    ini = sub.add_parser("init", help="把这套美术管线脚手架到一个项目(复制模板+建反向软链)")
    ini.add_argument("path", help="目标项目根目录")
    ini.add_argument("--name", help="项目名(默认用目录名)")
    ini.set_defaults(func=cmd_init)

    wl = sub.add_parser("workflows", help="列出 catalog 注册的工作流(分类/任务/默认/模型/节点)")
    wl.set_defaults(func=cmd_workflows)

    il = sub.add_parser("install", help="按 catalog 给某工作流备齐模型(魔搭)+ 提示装节点")
    il.add_argument("name", help="catalog 里的工作流名(见 comfy.py workflows)")
    il.set_defaults(func=cmd_install)

    args = ap.parse_args()
    try:
        args.func(args)
    except ComfyError as e:
        sys.exit(f"✗ {e}")


if __name__ == "__main__":
    main()
