#!/usr/bin/env python3
"""voxcpm_gen —— 本地 TTS 配音（VoxCPM2 on Apple MLX）。

三模式：
  say     零样本：纯文本配音（内置音色）
  design  音色设计：用一句文字描述造音色（无需参考音）
  clone   声音克隆：用一段参考音 + 其转写复刻音色
  info    打印环境 / 模型路径 / 采样率

设计要点（别乱放 / 跑得动）：
  · 模型走魔搭 ModelScope，落标准缓存 ~/.cache/modelscope（见 ~/.claude/rules/model-download.md）
  · 推理用专用 venv ~/.venvs/mlx-audio（mlx-audio + modelscope），脚本会自动重定向到它
  · 长文本按句切分逐段生成再拼接，适合 5 分钟级旁白
"""
import os
import sys

# ---- 重定向到专用 venv（必须在导入重依赖之前）----
# 注意：uv 的多个 venv 共享同一底层 CPython，比 sys.executable 区分不开 venv，
# 必须按 venv 前缀 sys.prefix 判断；再用环境哨兵兜底防重入死循环。
_VENV = os.path.expanduser("~/.venvs/mlx-audio")
_VENV_PY = os.path.join(_VENV, "bin", "python")
if (os.environ.get("_VOXCPM_REEXEC") != "1"
        and os.path.exists(_VENV_PY)
        and os.path.realpath(sys.prefix) != os.path.realpath(_VENV)):
    os.environ["_VOXCPM_REEXEC"] = "1"
    os.execv(_VENV_PY, [_VENV_PY, os.path.abspath(__file__), *sys.argv[1:]])

# 本机 HF 不可达：强制本地优先、镜像兜底，杜绝卡在被墙的 huggingface.co
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")

import argparse
import re
import time
from typing import Optional

import numpy as np
from scipy.io import wavfile

DEFAULT_MODEL = "mlx-community/VoxCPM2-8bit"   # 也可换 -4bit(更小更快) / -bf16(更高质量)
DEFAULT_SR = 48000


def resolve_model_path(repo: str) -> str:
    """把 HF 风格 repo id 经魔搭解析成本地路径（幂等，已缓存秒返）。"""
    if os.path.isdir(repo):
        return repo
    from modelscope import snapshot_download
    return snapshot_download(repo)


def load_model(repo: str):
    """加载 mlx-audio TTS 模型（吃本地目录路径）。"""
    from mlx_audio.tts.utils import load
    path = resolve_model_path(repo)
    print(f"· 模型 {repo}\n· 路径 {path}", file=sys.stderr)
    return load(path)


def split_text(text: str, max_chars: int = 120) -> list[str]:
    """按中英句末标点切分，再贪心打包到 <= max_chars 的块，避免单段过长。"""
    parts = re.split(r"(?<=[。！？!?；;\n])", text)
    chunks: list[str] = []
    cur = ""
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if cur and len(cur) + len(p) > max_chars:
            chunks.append(cur)
            cur = p
        else:
            cur = f"{cur}{p}" if cur else p
    if cur:
        chunks.append(cur)
    return chunks or [text]


def synthesize(
    model,
    text: str,
    *,
    instruct: Optional[str] = None,
    ref_audio: Optional[str] = None,
    ref_text: Optional[str] = None,
    timesteps: int = 10,
    cfg: float = 2.0,
    chunk: bool = True,
    max_chars: int = 120,
    gap_sec: float = 0.25,
) -> tuple[np.ndarray, int]:
    """合成音频。长文本按句切分逐段生成、段间插入静音后拼接。返回 (float32 波形, 采样率)。"""
    segments = split_text(text, max_chars) if chunk else [text]
    audios: list[np.ndarray] = []
    sr = DEFAULT_SR
    total_dur = 0.0
    t0 = time.time()
    for i, seg in enumerate(segments, 1):
        res = next(model.generate(
            seg,
            instruct=instruct,
            ref_audio=ref_audio,
            ref_text=ref_text,
            inference_timesteps=timesteps,
            cfg_value=cfg,
        ))
        sr = int(getattr(res, "sample_rate", DEFAULT_SR) or DEFAULT_SR)
        a = np.asarray(res.audio).squeeze().astype(np.float32)
        audios.append(a)
        total_dur += len(a) / sr
        print(f"  [{i}/{len(segments)}] {len(a)/sr:5.1f}s  «{seg[:18]}…»", file=sys.stderr)
    gen_dt = time.time() - t0

    if len(audios) == 1:
        out = audios[0]
    else:
        gap = np.zeros(int(sr * gap_sec), dtype=np.float32)
        joined = [audios[0]]
        for a in audios[1:]:
            joined.extend((gap, a))
        out = np.concatenate(joined)

    rtf = gen_dt / total_dur if total_dur else 0.0
    print(f"· 生成 {gen_dt:.1f}s / 音频 {total_dur:.1f}s / RTF {rtf:.2f}", file=sys.stderr)
    return out, sr


def save_wav(audio: np.ndarray, sr: int, out: str) -> str:
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    wavfile.write(out, sr, audio)
    return out


def default_out(mode: str) -> str:
    stamp = time.strftime("%Y%m%d-%H%M%S")
    return os.path.join("voxcpm_outputs", f"{mode}-{stamp}.wav")


def read_text(args) -> str:
    if args.text_file:
        with open(args.text_file, encoding="utf-8") as f:
            return f.read().strip()
    if args.text:
        return args.text
    sys.exit("需要 --text 或 --text-file")


def run(args) -> None:
    if args.mode == "info":
        print(f"venv      {_VENV_PY}")
        print(f"model     {args.model}")
        print(f"path      {resolve_model_path(args.model)}")
        print(f"sr        {DEFAULT_SR} Hz")
        return

    text = read_text(args)
    model = load_model(args.model)
    audio, sr = synthesize(
        model, text,
        instruct=getattr(args, "instruct", None),
        ref_audio=getattr(args, "ref_audio", None),
        ref_text=getattr(args, "ref_text", None),
        timesteps=args.timesteps,
        cfg=args.cfg,
        chunk=not args.no_chunk,
        max_chars=args.max_chars,
    )
    out = save_wav(audio, sr, args.out or default_out(args.mode))
    print(out)  # stdout 只吐产物路径，方便上层取用
    if args.play:
        os.system(f'afplay "{out}"')


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="VoxCPM2 本地配音（Apple MLX）")
    sub = p.add_subparsers(dest="mode", required=True)

    def common(sp):
        sp.add_argument("--text", help="要合成的文本")
        sp.add_argument("--text-file", help="从文件读文本（长旁白用这个）")
        sp.add_argument("--out", help="输出 wav 路径（默认 voxcpm_outputs/<mode>-<时间>.wav）")
        sp.add_argument("--model", default=DEFAULT_MODEL, help="模型 repo（默认 VoxCPM2-8bit）")
        sp.add_argument("--timesteps", type=int, default=10, help="CFM 步数：越低越快，7 是快/质量平衡点")
        sp.add_argument("--cfg", type=float, default=2.0, help="无分类器引导强度")
        sp.add_argument("--no-chunk", action="store_true", help="不按句切分（短文本用）")
        sp.add_argument("--max-chars", type=int, default=120, help="分句打包的单段最大字数")
        sp.add_argument("--play", action="store_true", help="生成后 afplay 试听")

    s_say = sub.add_parser("say", help="零样本：内置音色配音")
    common(s_say)

    s_design = sub.add_parser("design", help="音色设计：文字描述造音色")
    common(s_design)
    s_design.add_argument("--instruct", required=True, help="音色描述，如「温柔甜美的年轻女性主播」")

    s_clone = sub.add_parser("clone", help="声音克隆：参考音 + 转写复刻音色")
    common(s_clone)
    s_clone.add_argument("--ref-audio", required=True, dest="ref_audio", help="参考音频 wav")
    s_clone.add_argument("--ref-text", required=True, dest="ref_text", help="参考音频的逐字转写")

    s_info = sub.add_parser("info", help="打印环境 / 模型路径")
    s_info.add_argument("--model", default=DEFAULT_MODEL)

    return p


if __name__ == "__main__":
    run(build_parser().parse_args())
