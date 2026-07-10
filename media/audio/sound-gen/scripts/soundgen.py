#!/usr/bin/env python3
"""soundgen.py — 本地生成 BGM(音乐) + 音效(SFX) 的统一 CLI（编排层）

两个后端各自独立 venv，装在 voice-lab/sound-gen/（见 ../reference/setup.md）：
  music → ACE-Step 1.5（文生音乐 · MIT 可商用 · Apple MLX · 48kHz · 最长 10min）
  sfx   → Stable Audio Open Small（文生音效 · Stability 社区许可 · MPS · ≤11s · 极快）

本脚本用任意 python 跑（如 ~/.venvs/current），按子命令 subprocess 调对应后端 venv。
后端目录可用环境变量覆盖：SOUNDGEN_ACESTEP_DIR / SOUNDGEN_SAO_DIR。

    python soundgen.py music --caption "warm bright electronic underscore, no vocals" --duration 25 --out bgm.wav
    python soundgen.py sfx   --prompt  "clean fast whoosh transition" --duration 2 --out whoosh.wav
    python soundgen.py info
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ACE_DIR = Path(os.environ.get(
    "SOUNDGEN_ACESTEP_DIR",
    os.path.expanduser("~/Coding/Archer/voice-lab/sound-gen/ACE-Step-1.5")))
SAO_DIR = Path(os.environ.get(
    "SOUNDGEN_SAO_DIR",
    os.path.expanduser("~/Coding/Archer/voice-lab/sound-gen/stable-audio-tools")))
ACE_PY = ACE_DIR / ".venv" / "bin" / "python"
SAO_PY = SAO_DIR / ".venv" / "bin" / "python"
SFX_BACKEND = HERE / "_sfx_backend.py"
MUSIC_BACKEND = HERE / "_music_backend.py"


def _fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def cmd_music(a: argparse.Namespace) -> None:
    if not ACE_PY.exists():
        _fail(f"ACE-Step venv 不存在：{ACE_PY}\n  → 见 reference/setup.md 安装后端（或设 SOUNDGEN_ACESTEP_DIR）")
    caption = (a.caption or "").strip()
    if not caption:
        _fail("--caption 不能为空（英文描述效果最好）")
    workdir = Path(tempfile.mkdtemp(prefix="sound-gen_bgm_"))
    toml = workdir / "gen.toml"
    lines = [
        'config_path = "acestep-v15-turbo"',
        'checkpoint_dir = "checkpoints"',
        'thinking = false',
        'instrumental = true',
        f'caption = {json.dumps(caption)}',
        f'duration = {int(a.duration)}',
        'audio_format = "wav"',
        f'save_dir = {json.dumps(str(workdir))}',
        'batch_size = 1',
    ]
    if a.seed is not None and a.seed >= 0:
        lines += [f'seed = {int(a.seed)}', 'use_random_seed = false']
    toml.write_text("\n".join(lines) + "\n", encoding="utf-8")
    env = {**os.environ, "ACESTEP_DOWNLOAD_SOURCE": "modelscope"}
    r = subprocess.run([str(ACE_PY), "cli.py", "-c", str(toml)], cwd=str(ACE_DIR), env=env)
    wavs = sorted(workdir.glob("*.wav"))
    if not wavs:  # 兜底：某些版本 cli.py 落 <ACE_DIR>/output
        pool = sorted((ACE_DIR / "output").glob("*.wav"), key=lambda p: p.stat().st_mtime)
        wavs = pool[-1:] if pool else []
    if r.returncode != 0 or not wavs:
        _fail("BGM 生成失败（见上方后端输出）")
    src = wavs[0]
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        if Path(a.out).resolve() != src.resolve():
            shutil.copy(str(src), a.out)
        print(str(Path(a.out).resolve()))
    else:
        print(str(src))


def cmd_sfx(a: argparse.Namespace) -> None:
    if not SAO_PY.exists():
        _fail(f"stable-audio venv 不存在：{SAO_PY}\n  → 见 reference/setup.md 安装后端（或设 SOUNDGEN_SAO_DIR）")
    prompt = (a.prompt or "").strip()
    if not prompt:
        _fail("--prompt 不能为空（英文描述效果最好）")
    out = a.out or tempfile.mktemp(suffix=".wav")
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    cmd = [str(SAO_PY), str(SFX_BACKEND), "--prompt", prompt,
           "--duration", str(float(a.duration)), "--steps", str(int(a.steps)), "--out", out]
    if a.seed is not None and a.seed >= 0:
        cmd += ["--seed", str(int(a.seed))]
    r = subprocess.run(cmd, cwd=str(SAO_DIR))
    if r.returncode != 0 or not os.path.exists(out):
        _fail("音效生成失败（见上方后端输出）")
    print(str(Path(out).resolve()))


def cmd_batch(a: argparse.Namespace) -> None:
    """批量：一份混合 manifest（每条带 type=music|sfx）·按后端各调一次·模型各只加载一次。

    避免逐条 subprocess 重复加载/卸载模型——音效尤其明显（加载 ~10s ≫ 生成 <1s）。
    """
    try:
        items = json.load(open(a.manifest, encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        _fail(f"读不了 manifest：{e}")
    if not isinstance(items, list) or not items:
        _fail("manifest 需是非空 JSON 列表，每条含 type(music|sfx) + 参数 + out")
    for it in items:
        if not isinstance(it, dict) or "out" not in it:
            _fail(f"每条都要有 out 字段：{it}")
    music = [it for it in items if it.get("type") == "music"]
    sfx = [it for it in items if it.get("type") == "sfx"]
    if not music and not sfx:
        _fail("manifest 里没有 type=music 或 type=sfx 的项")

    workdir = Path(tempfile.mkdtemp(prefix="sound-gen_batch_"))
    rc = 0
    if music:
        if not ACE_PY.exists():
            _fail(f"ACE-Step venv 不存在：{ACE_PY}（见 reference/setup.md）")
        mf = workdir / "music.json"
        mf.write_text(json.dumps(music, ensure_ascii=False), encoding="utf-8")
        env = {**os.environ, "ACESTEP_DOWNLOAD_SOURCE": "modelscope"}
        r = subprocess.run([str(ACE_PY), str(MUSIC_BACKEND), "--manifest", str(mf)],
                           cwd=str(ACE_DIR), env=env)
        rc |= r.returncode
    if sfx:
        if not SAO_PY.exists():
            _fail(f"stable-audio venv 不存在：{SAO_PY}（见 reference/setup.md）")
        sxf = workdir / "sfx.json"
        sxf.write_text(json.dumps(sfx, ensure_ascii=False), encoding="utf-8")
        r = subprocess.run([str(SAO_PY), str(SFX_BACKEND), "--manifest", str(sxf)],
                           cwd=str(SAO_DIR))
        rc |= r.returncode

    print(f"[batch] music={len(music)} sfx={len(sfx)} · 产物：")
    for it in items:
        print(f"  {'OK ' if os.path.exists(it['out']) else '缺 '}{it['out']}")
    sys.exit(0 if rc == 0 else 1)


def cmd_info(a: argparse.Namespace) -> None:
    def mark(ok: bool) -> str:
        return "OK" if ok else "缺"
    ace_ck = ACE_DIR / "checkpoints" / "acestep-v15-turbo" / "model.safetensors"
    sao_ck = SAO_DIR / "models" / "stable-audio-open-small" / "model.safetensors"
    print("sound-gen 后端状态：")
    print(f"  [music] ACE-Step  dir={ACE_DIR}")
    print(f"          venv={mark(ACE_PY.exists())}  turbo模型={mark(ace_ck.exists())}")
    print(f"  [sfx]   Stable Audio Open Small  dir={SAO_DIR}")
    print(f"          venv={mark(SAO_PY.exists())}  模型={mark(sao_ck.exists())}")
    print("  覆盖后端路径：SOUNDGEN_ACESTEP_DIR / SOUNDGEN_SAO_DIR")


def main() -> None:
    p = argparse.ArgumentParser(description="本地生成 BGM(音乐) + 音效(SFX)")
    sub = p.add_subparsers(dest="mode", required=True)

    m = sub.add_parser("music", help="文生 BGM（纯器乐 · ACE-Step）")
    m.add_argument("--caption", required=True, help="音乐英文描述（气质/乐器/情绪/no vocals）")
    m.add_argument("--duration", type=int, default=25, help="时长秒（5–120，默认 25）")
    m.add_argument("--seed", type=int, default=-1, help="随机种子，-1=随机")
    m.add_argument("--out", help="输出 wav 路径（默认临时文件，路径打到 stdout）")
    m.set_defaults(func=cmd_music)

    s = sub.add_parser("sfx", help="文生音效（Stable Audio Open Small）")
    s.add_argument("--prompt", required=True, help="音效英文描述（whoosh/ping/impact…）")
    s.add_argument("--duration", type=float, default=2.0, help="时长秒（≤11，默认 2）")
    s.add_argument("--steps", type=int, default=8, help="采样步数（默认 8）")
    s.add_argument("--seed", type=int, default=-1, help="随机种子，-1=随机")
    s.add_argument("--out", help="输出 wav 路径（默认临时文件，路径打到 stdout）")
    s.set_defaults(func=cmd_sfx)

    b = sub.add_parser("batch", help="批量：混合 manifest（type=music|sfx）·各后端载一次出多条")
    b.add_argument("--manifest", required=True,
                   help='JSON [{"type":"music|sfx", caption/prompt, duration?, seed?, steps?, out}, ...]')
    b.set_defaults(func=cmd_batch)

    i = sub.add_parser("info", help="打印后端 / 模型就绪状态")
    i.set_defaults(func=cmd_info)

    a = p.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
