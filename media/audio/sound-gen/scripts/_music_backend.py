#!/usr/bin/env python3
"""_music_backend.py — BGM 批量生成后端（ACE-Step · 载一次 · 多 caption 循环）

**必须用 ACE-Step 的 venv 跑**（import acestep）。由同目录 soundgen.py 的 batch 调用。
DiT + LM 各只加载一次，manifest 里多条循环出——省重复加载（单条走 cli.py 每条都重载）。
LM 提质（填满目标时长 / bpm 结构）；LM 初始化失败则退化纯 DiT（thinking=False·仍能出，但长曲可能填不满）。

manifest: JSON 列表，每条 {caption, duration?, seed?, out}。
    python _music_backend.py --manifest items.json
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys

import torch
from acestep.handler import AceStepHandler
from acestep.inference import GenerationConfig, GenerationParams, generate_music
from acestep.llm_inference import LLMHandler


def _device() -> str:
    if torch.backends.mps.is_available():
        return "mps"
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


def _try_init_lm(llm: LLMHandler, device: str, checkpoint_dir: str = "checkpoints") -> bool:
    """尝试初始化 5Hz LM（提质·填满时长）。成功 True，失败 False → 退化纯 DiT。"""
    try:
        models = llm.get_available_5hz_lm_models()
        if not models:
            return False
        lm_path = next((m for m in models if "0.6B" in m), models[0])  # 优先小 LM 省内存
        backend = "mlx" if device == "mps" else ("vllm" if device == "cuda" else "pt")
        llm.initialize(checkpoint_dir=checkpoint_dir, lm_model_path=lm_path,
                       backend=backend, device=device, offload_to_cpu=False, dtype=None)
        return bool(getattr(llm, "llm_initialized", False))
    except Exception as e:  # noqa: BLE001
        print(f"[music-batch] LM 初始化失败，退化纯 DiT：{e}", flush=True)
        return False


def _params(it: dict, thinking: bool) -> GenerationParams:
    kw = dict(task_type="text2music", caption=(it.get("caption") or "").strip(),
              lyrics="[Instrumental]", instrumental=True, thinking=thinking,
              duration=int(it.get("duration", 25)))
    seed = it.get("seed", -1)
    if seed is not None and int(seed) >= 0:
        kw["seed"] = int(seed)
    return GenerationParams(**kw)


def _config(it: dict) -> GenerationConfig:
    kw = dict(batch_size=1, audio_format="wav")
    seed = it.get("seed", -1)
    if seed is not None and int(seed) >= 0:
        kw["use_random_seed"] = False
    return GenerationConfig(**kw)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True, help="JSON [{caption, duration?, seed?, out}, ...]")
    ap.add_argument("--config-path", default="acestep-v15-turbo")
    ap.add_argument("--no-lm", action="store_true", help="强制纯 DiT（不加载 LM·更快·长曲可能填不满）")
    a = ap.parse_args()

    items = json.load(open(a.manifest, encoding="utf-8"))
    if not isinstance(items, list) or not items:
        print("ERROR: manifest 空或非列表", file=sys.stderr)
        sys.exit(1)

    device = _device()
    dit = AceStepHandler()
    llm = LLMHandler()
    try:
        use_fa = dit.is_flash_attention_available(device)
    except Exception:  # noqa: BLE001
        use_fa = False
    dit.initialize_service(project_root=os.getcwd(), config_path=a.config_path,
                           device=device, use_flash_attention=use_fa, compile_model=False,
                           offload_to_cpu=False, offload_dit_to_cpu=False)
    thinking = False if a.no_lm else _try_init_lm(llm, device)
    print(f"[music-batch] DiT loaded on {device} · LM={'on' if thinking else 'off(纯DiT)'} · "
          f"{len(items)} 条待生成", flush=True)

    ok = 0
    for i, it in enumerate(items):
        out = it["out"]
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        save_dir = os.path.dirname(os.path.abspath(out))
        try:
            res = generate_music(dit, llm, _params(it, thinking), _config(it), save_dir=save_dir)
        except Exception as e:  # noqa: BLE001
            print(f"[music-batch] {i + 1}/{len(items)} ERROR: {e}", flush=True)
            continue
        src = res.audios[0].get("path") if getattr(res, "success", False) and res.audios else None
        if src and os.path.exists(src):
            if os.path.abspath(src) != os.path.abspath(out):
                shutil.move(src, out)
            ok += 1
            print(f"[music-batch] {i + 1}/{len(items)} -> {out}", flush=True)
        else:
            print(f"[music-batch] {i + 1}/{len(items)} FAILED: {getattr(res, 'error', 'no audio')}", flush=True)

    print(f"DONE {ok}/{len(items)}", flush=True)
    sys.exit(0 if ok == len(items) else 1)


if __name__ == "__main__":
    main()
