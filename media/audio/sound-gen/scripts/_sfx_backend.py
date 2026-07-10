#!/usr/bin/env python3
"""_sfx_backend.py — 音效生成后端（Stable Audio Open Small）

**必须用 stable-audio-tools 的 venv 跑**（import stable_audio_tools）。
由同目录 soundgen.py 的 sfx/batch 子命令 subprocess 调用，一般不直接手跑。
模型走本地 model_config.json + model.safetensors（HF 被墙·不用 --pretrained-name）。

单条：--prompt "..." --out x.wav
批量：--manifest items.json  （模型只加载一次·循环出多条·省重复加载）
    manifest: JSON 列表，每条 {prompt, duration?, steps?, seed?, out}
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import soundfile as sf
import torch
from einops import rearrange
from stable_audio_tools.inference.generation import generate_diffusion_cond
from stable_audio_tools.models.factory import create_model_from_config
from stable_audio_tools.models.utils import load_ckpt_state_dict


def _default_model_dir() -> str:
    sao = os.environ.get(
        "SOUNDGEN_SAO_DIR",
        os.path.expanduser("~/Coding/Archer/voice-lab/sound-gen/stable-audio-tools"))
    return os.path.join(sao, "models", "stable-audio-open-small")


def load_model(model_dir: str):
    cfg = json.load(open(os.path.join(model_dir, "model_config.json")))
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model = create_model_from_config(cfg)
    model.load_state_dict(load_ckpt_state_dict(os.path.join(model_dir, "model.safetensors")))
    model = model.to(device).float().eval()  # MPS 用 float32：避免 decoder conv1d fp16 卡死
    return model, cfg, device


def gen_one(model, cfg, device, prompt, duration, steps, seed, out) -> None:
    sr, sample_size = cfg["sample_rate"], cfg["sample_size"]
    dur = max(0.5, min(float(duration), sample_size / sr))
    cond = [{"prompt": (prompt or "").strip(), "seconds_start": 0, "seconds_total": dur}]
    kw = {"seed": int(seed)} if seed is not None and int(seed) >= 0 else {}
    with torch.no_grad():
        o = generate_diffusion_cond(
            model, steps=int(steps), cfg_scale=1.0, conditioning=cond,
            sample_size=sample_size, sampler_type="pingpong", device=device, **kw)
    o = rearrange(o, "b d n -> d (b n)").to(torch.float32).cpu()
    o = o / o.abs().max().clamp(min=1e-8) * 0.9
    o = o[:, : int((dur + 0.4) * sr)]  # 裁到内容长度 + 0.4s 尾
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    sf.write(out, o.numpy().T, sr)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt")
    ap.add_argument("--manifest", help="JSON [{prompt, duration?, steps?, seed?, out}, ...]（批量·载一次）")
    ap.add_argument("--duration", type=float, default=2.0)
    ap.add_argument("--steps", type=int, default=8)
    ap.add_argument("--seed", type=int, default=-1)
    ap.add_argument("--model-dir", default=_default_model_dir())
    ap.add_argument("--out")
    a = ap.parse_args()
    if not a.manifest and not (a.prompt and a.out):
        ap.error("需 --prompt + --out（单条）或 --manifest（批量）")

    model, cfg, device = load_model(a.model_dir)

    if a.manifest:
        items = json.load(open(a.manifest, encoding="utf-8"))
        print(f"[sfx-batch] 模型 loaded on {device} · {len(items)} 条待生成", flush=True)
        ok = 0
        for i, it in enumerate(items):
            try:
                gen_one(model, cfg, device, it["prompt"], it.get("duration", 2.0),
                        it.get("steps", 8), it.get("seed", -1), it["out"])
                ok += 1
                print(f"[sfx-batch] {i + 1}/{len(items)} -> {it['out']}", flush=True)
            except Exception as e:  # noqa: BLE001
                print(f"[sfx-batch] {i + 1}/{len(items)} ERROR: {e}", flush=True)
        print(f"DONE {ok}/{len(items)}", flush=True)
        sys.exit(0 if ok == len(items) else 1)
    else:
        gen_one(model, cfg, device, a.prompt, a.duration, a.steps, a.seed, a.out)
        print("OK", a.out)


if __name__ == "__main__":
    main()
