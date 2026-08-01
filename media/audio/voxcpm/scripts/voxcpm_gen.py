#!/usr/bin/env python3
"""voxcpm_gen —— 本地 TTS 配音（VoxCPM2 on Apple MLX）。

模式：
  say     零样本：纯文本配音（内置音色）
  design  音色设计：用一句文字描述造音色（无需参考音）
  clone   声音克隆：用一段参考音 + 其转写复刻音色
  batch   批量克隆：一份 manifest·模型只载一次·合成多段（省逐段重载 ~3GB 模型·长旁白多幕神器）
  info    打印环境 / 模型路径 / 采样率

设计要点（别乱放 / 跑得动）：
  · 模型走魔搭 ModelScope，落标准缓存 ~/.cache/modelscope（见 ~/.claude/rules/model-download.md）
  · 推理用专用 venv ~/.venvs/mlx-audio（mlx-audio + modelscope），脚本会自动重定向到它
  · 长文本按句切分逐段生成再拼接，适合 5 分钟级旁白
  · 频道音色两型（card.json voice.profiles·engine 字段路由·见 resolve_channel_ref）：
    LoRA 型 voxcpm2-mlx-lora（mlx_model 专属合并模型 + 可选 prompt_wav/prompt_text 提示条）
    与零样本型（ref_wav/ref_text 基座克隆·向后兼容）
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
import shutil
import subprocess
import tempfile
import time
from typing import Optional

import numpy as np
from scipy.io import wavfile

DEFAULT_MODEL = "mlx-community/VoxCPM2-8bit"   # 也可换 -4bit(更小更快) / -bf16(更高质量)
DEFAULT_SR = 48000

# 频道音色 profile 的 engine 路由值（card.json voice.profiles[].engine）
ENGINE_LORA = "voxcpm2-mlx-lora"                    # LoRA 型：音色工作台训 LoRA→合并→转 MLX 的专属模型
ENGINES_ZEROSHOT = ("", "voxcpm-mlx", "voxcpm2-mlx")  # 零样本型：基座 + 参考音克隆（含缺省无 engine）

# RNNoise 模型（speech 专用）——随 skill 一起冻结，arnndn 吃它做去噪
_RNNN = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "assets", "rnnoise", "sh.rnnn")


def load_channel():
    """惰性加载当前频道（channek·零依赖标准库）；找不到/坏了返回 None（零回归安全）。

    走 _shared/channek.py（dev 真身 / vendored 两处都成立）；惰性调用，
    say/design 不付频道解析成本。mlx-audio venv 下也能 import（stdlib json）。
    """
    try:
        import pathlib

        for _anc in pathlib.Path(__file__).resolve().parents:
            cand = _anc / "_shared" / "channek.py"
            if cand.exists():
                if str(cand.parent) not in sys.path:
                    sys.path.insert(0, str(cand.parent))
                break
        import channek

        return channek.load(required=False)
    except Exception:
        return None


def resolve_channel_ref(ch, profile_key, md_tok):
    """从 card.json voice.profiles 解析 (model, ref_audio, ref_text)——按 `engine` 字段路由两型 profile。

    · LoRA 型（engine=voxcpm2-mlx-lora）：音色工作台（voice-lab）训 LoRA → 合并进底座 → 转 MLX 的
      **专属音色模型**。model = `mlx_model`（音色烤进权重·必须是存在的目录，缺/坏直接报错不静默降级
      到基座冒充频道音色）；参考音 = `prompt_wav` + `prompt_text`（可选克隆提示条·把声纹相似度
      0.866→0.889；prompt_text 是**内联转写文本**，也兼容填成文件路径）。
    · 零样本型（无 engine / voxcpm-mlx / voxcpm2-mlx）：`ref_wav`/`ref_text` 指参考音 wav / 转写文件
      （原行为·向后兼容），model=None（用默认基座）。文件 exists() 兜底回 md_tok（voice.md）——
      P3 物理迁移前 channel 相对路径可能还没就位 → 回落旧路径 / 转写，行为=现状（零回归）。
    · 未知 engine：清晰报错（fail-fast·不猜、绝不冒充某频道音色）。

    路径可为绝对路径（音色资产在频道外 = 外部依赖·风格卡分发不自包含）或相对频道根（ch.path 兼容
    两者）。无频道 / 无 profile 时返回 (None, None, None)，由调用方报「需配置音色」。
    """
    if ch is None:
        return None, None, None
    prof = ch.voice_profile(profile_key)
    if not prof:
        return None, None, None

    engine = (prof.get("engine") or "").strip()
    if engine == ENGINE_LORA:
        model = None
        mm = prof.get("mlx_model")
        if mm:
            p = ch.path(os.path.expanduser(mm))
            if not p.is_dir():
                sys.exit(f"card.json voice profile（engine={engine}）的 mlx_model 不是有效目录：{p}\n"
                         "→ 音色为外部依赖：确认音色工作台的合并模型已就位（voices/<名>/mlx-8bit）")
            model = str(p)
        ref_audio = md_tok.get("ref_audio")
        pw = prof.get("prompt_wav")
        if pw:
            p = ch.path(os.path.expanduser(pw))
            ref_audio = str(p) if p.exists() else ref_audio
        ref_text = md_tok.get("ref_text")
        pt = prof.get("prompt_text")
        if pt:
            p = ch.path(os.path.expanduser(pt))
            ref_text = p.read_text(encoding="utf-8").strip() if p.is_file() else pt
        return model, ref_audio, ref_text

    if engine in ENGINES_ZEROSHOT:
        ref_audio = md_tok.get("ref_audio")
        rw = prof.get("ref_wav")
        if rw:
            p = ch.path(rw)
            ref_audio = str(p) if p.exists() else ref_audio
        ref_text = md_tok.get("ref_text")
        rt = prof.get("ref_text")
        if rt:
            p = ch.path(rt)
            ref_text = p.read_text(encoding="utf-8").strip() if p.is_file() else ref_text
        return None, ref_audio, ref_text

    sys.exit(f"card.json voice profile 的 engine 未知：{engine!r}\n"
             f"→ 支持：{ENGINE_LORA}（LoRA 型·mlx_model [+ prompt_wav/prompt_text]）"
             "或缺省/voxcpm-mlx（零样本型·ref_wav/ref_text）")


def resolve_model_path(repo: str) -> str:
    """把 HF 风格 repo id 经魔搭解析成本地路径（幂等，已缓存秒返）；本地目录（如 LoRA 合并模型）原样返回。"""
    repo = os.path.expanduser(repo)
    if os.path.isdir(repo):
        return repo
    from modelscope import snapshot_download
    return snapshot_download(repo)


def load_model(repo: str):
    """加载 mlx-audio TTS 模型（吃本地目录路径）。"""
    # 本地微调/合并出的 VoxCPM（如 voice-lab 的 mlx-8bit）带自定义分词器 tokenization_voxcpm2.py，
    # AutoTokenizer 会要 trust_remote_code。这些自定义码就是 VoxCPM 自带的（安全）→ 非交互下自动放行，
    # 让 skill 既能跑官方基座、也能跑 voice-lab 训出的专属音色模型。
    try:
        import transformers.dynamic_module_utils as _dmu

        _dmu.resolve_trust_remote_code = lambda *a, **k: True  # type: ignore
    except Exception:
        pass
    from mlx_audio.tts.utils import load
    path = resolve_model_path(repo)
    print(f"· 模型 {repo}\n· 路径 {path}", file=sys.stderr)
    return load(path)


def load_voice_token(path: str) -> dict:
    """读 voice.md 音色 token：解析 frontmatter，把 ref_audio/ref_text 的相对路径
    解析成绝对路径 / 读出转写文本。返回 {ref_audio, ref_text, mode}。"""
    p = os.path.abspath(os.path.expanduser(path))
    if os.path.isdir(p):
        p = os.path.join(p, "voice.md")
    base = os.path.dirname(p)
    text = open(p, encoding="utf-8").read()
    m = re.search(r"^---\s*\n(.*?)\n---", text, re.S)
    fm: dict[str, str] = {}
    if m:
        for line in m.group(1).splitlines():
            mm = re.match(r"^([A-Za-z_]+):\s*(.+?)\s*(?:#.*)?$", line)
            if mm:
                fm[mm.group(1)] = mm.group(2).strip()

    def rel(v: Optional[str]) -> Optional[str]:
        return None if not v else (v if os.path.isabs(v) else os.path.join(base, v))

    rt = fm.get("ref_text")
    ref_text = None
    if rt:
        rtp = rel(rt)
        ref_text = open(rtp, encoding="utf-8").read().strip() if rtp and os.path.isfile(rtp) else rt
    return {"ref_audio": rel(fm.get("ref_audio")), "ref_text": ref_text, "mode": fm.get("mode", "clone")}


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


def denoise_segment(audio: np.ndarray, sr: int) -> np.ndarray:
    """每段生成后过一遍去噪（固定步，不是可选）。

    为什么必须有这步：VoxCPM2 的 CFM 扩散是逐段随机的，克隆参考音（本身底噪 -64dB）
    时，有的段干净（-99dB）、有的段带底噪（-54/-60dB），去噪不做就逐幕飘。
    这里用 RNNoise（speech 专用，asset/rnnoise/sh.rnnn）经 ffmpeg arnndn 把每段底噪
    压到 ≤-80dB（实测多到 -inf），同时 RMS / 高频能量基本不动——不闷、不伤音色。
    叠一道 highpass=50 砍次声轰鸣。ffmpeg 不可用或失败则原样返回（不阻断出片）。
    """
    if not (shutil.which("ffmpeg") and os.path.isfile(_RNNN)):
        return audio
    with tempfile.TemporaryDirectory() as td:
        src = os.path.join(td, "in.wav")
        dst = os.path.join(td, "out.wav")
        wavfile.write(src, sr, audio)
        cmd = [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-i", src, "-af", f"highpass=f=50,arnndn=m={_RNNN}", dst,
        ]
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            cleaned_sr, cleaned = wavfile.read(dst)
            out = np.asarray(cleaned).squeeze().astype(np.float32)
            # wavfile 读回若是整型量化，归一回 [-1, 1]
            if np.issubdtype(np.asarray(cleaned).dtype, np.integer):
                out = out / float(np.iinfo(np.asarray(cleaned).dtype).max)
            return out
        except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
            return audio


def edge_fade(a: np.ndarray, sr: int, ms: float = 8.0) -> np.ndarray:
    """给一段波形首尾各加 ms 毫秒升余弦淡入淡出（去咔哒 / declick）。

    为什么必须有这步：VoxCPM 每块可能从「非零采样」骤起 / 骤停；逐块拼接时在块与
    段间静音（np.zeros）交界处形成一条陡沿（阶跃），听感是一声「咔哒 / pop / 切换杂音」。
    首尾磨成 8ms 斜坡后阶跃消失；8ms 远短于一个音节起振，不吃字、不改音色。就地安全。
    """
    n = len(a)
    w = int(sr * ms / 1000.0)
    if w < 2 or n < 2 * w:
        return a
    ramp = np.sin(np.linspace(0.0, np.pi / 2.0, w, dtype=np.float32)) ** 2  # 升余弦 0→1
    out = a.copy()
    out[:w] *= ramp
    out[-w:] *= ramp[::-1]
    return out


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
    denoise: bool = True,
) -> tuple[np.ndarray, int]:
    """合成音频。长文本按句切分逐段生成、（默认）逐段去噪、段间插入静音后拼接。

    返回 (float32 波形, 采样率)。`denoise=True` 是固定步：每段生成后立刻过 RNNoise，
    保证 raw 层底噪稳定 ≤-80dB（解决逐幕去噪不稳）。
    """
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
        if denoise:
            a = denoise_segment(a, sr)
        a = edge_fade(a, sr)  # 每块首尾去咔哒：消块↔静音交界的阶跃 pop（切换杂音）
        audios.append(a)
        total_dur += len(a) / sr
        tag = "" if denoise else " (raw)"
        print(f"  [{i}/{len(segments)}] {len(a)/sr:5.1f}s{tag}  «{seg[:18]}…»", file=sys.stderr)
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


def apply_warmth_eq(path: str, warmth: float) -> None:
    """可选「暖声 EQ」——微调音色**亮度/厚度**（不改基频·声音仍是模型本音）。

    默认关（`--warmth 0`）；声音尽量用模型原生的。要调音色亮度时才开：
      · warmth > 0：加低中频厚度 + 压高频清脆 → 更暖/沉/厚（去「薄荷清脆」）。
      · warmth < 0：反向 → 更亮/脆。
      · 参数按 |warmth| 线性缩放；warmth=1.0 = 下面这套「厚」档，1.5~2 更狠（可能偏闷）。

    配方（warmth=1.0）：低频 +4.5dB@120 · 240Hz +4 · 4kHz -4.5 · 高频 -4.5dB@6500。
    实测：EQ 只塑形、变化温和（改不了基频/性别感）；要「深沉」的大改动靠**换慢/沉的
    参考音**（clone 的 prompt 决定说法），EQ 只做收尾的亮度微调。ffmpeg 不在则跳过。
    """
    if not warmth:
        return
    import shutil
    if not shutil.which("ffmpeg"):
        return
    k = warmth
    af = (f"bass=g={4.5 * k:.2f}:f=120,"
          f"equalizer=f=240:width_type=q:w=1:g={4.0 * k:.2f},"
          f"equalizer=f=4000:width_type=q:w=1.8:g={-4.5 * k:.2f},"
          f"treble=g={-4.5 * k:.2f}:f=6500")
    tmp = path + ".eq.wav"
    try:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-af", af,
                        "-ar", str(DEFAULT_SR), tmp], check=True)
        os.replace(tmp, path)
    except Exception:  # noqa: BLE001
        if os.path.exists(tmp):
            os.remove(tmp)


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


def _resolve_clone_voice(args, *, is_clone: bool):
    """解析 clone 音色 → (ch_model, ref_audio, ref_text)。run(clone) 与 run_batch 共用（不重复逻辑）。

    card.json voice.profiles（engine 路由两型·文件 exists() 兜底）→ voice.md（--voice）。
    只在 clone（需音色·is_clone）或显式 --voice 时介入；say/design 不进来（行为不变·零回归）。
    """
    ref_audio = getattr(args, "ref_audio", None)
    ref_text = getattr(args, "ref_text", None)
    voice = getattr(args, "voice", None)
    profile_key = getattr(args, "voice_profile", None)
    ch_model = None
    if not (ref_audio and ref_text) and (voice or is_clone):
        md_tok = load_voice_token(voice) if voice else {"ref_audio": None, "ref_text": None}
        ch = load_channel()
        ch_model, c_audio, c_text = resolve_channel_ref(ch, profile_key, md_tok)
        ref_audio = ref_audio or c_audio or md_tok.get("ref_audio")
        ref_text = ref_text or c_text or md_tok.get("ref_text")
        if voice:
            print(f"· 音色 token {voice}", file=sys.stderr)
        if ch is not None and ch.voice_profile(profile_key):
            _pk = profile_key or ch.get("voice.default")
            _tag = "·LoRA 合并模型（音色在权重）" if ch_model else ""
            print(f"· 频道音色 card.json voice.profiles[{_pk}]{_tag}", file=sys.stderr)
    return ch_model, ref_audio, ref_text


def run_batch(args) -> None:
    """批量克隆：一份 manifest·模型只载一次·合成多段（省逐段重载 ~3GB 模型）。

    manifest = JSON 数组 `[{text_file|text, out}, ...]`；音色 / 模型 / timesteps / cfg / max-chars
    全段共享（本就是「同一频道音色批量出多幕旁白」的场景·由调用方保证一致）。逐段 try 兜底——
    一段失败不废整批。stdout 只吐**一行 JSON** `{"outputs":[{out,duration,ok[,error]}]}`（逐段状态·
    顺序 == manifest 顺序·上层按段校验/重试）；其余日志全走 stderr。
    """
    import json
    import pathlib

    manifest = json.loads(pathlib.Path(args.manifest).read_text(encoding="utf-8"))
    if not isinstance(manifest, list) or not manifest:
        sys.exit(f"batch manifest 需为非空 JSON 数组：{args.manifest}")

    ch_model, ref_audio, ref_text = _resolve_clone_voice(args, is_clone=True)
    if not ch_model and not (ref_audio and ref_text):
        sys.exit("batch(clone) 需要频道 card.json voice.profiles，或 --voice 指向 voice.md，"
                 "或 --ref-audio + --ref-text")

    model = load_model(args.model or ch_model or DEFAULT_MODEL)   # ★ 只载一次·省 N-1 次重载
    total = len(manifest)
    outputs: list[dict] = []
    for idx, it in enumerate(manifest, 1):
        out_path = it.get("out")
        try:
            txt = it.get("text")
            if not txt and it.get("text_file"):
                txt = pathlib.Path(it["text_file"]).read_text(encoding="utf-8").strip()
            if not txt:
                raise ValueError("manifest 段缺 text / text_file")
            if not out_path:
                raise ValueError("manifest 段缺 out")
            print(f"·· batch [{idx}/{total}] → {out_path}", file=sys.stderr)
            audio, sr = synthesize(
                model, txt,
                ref_audio=ref_audio,
                ref_text=ref_text,
                timesteps=args.timesteps,
                cfg=args.cfg,
                chunk=not args.no_chunk,
                max_chars=args.max_chars,
                denoise=not args.no_denoise,
            )
            save_wav(audio, sr, out_path)
            apply_warmth_eq(out_path, getattr(args, "warmth", 0.0))
            outputs.append({"out": out_path, "duration": round(len(audio) / sr, 3), "ok": True})
        except Exception as e:  # noqa: BLE001 逐段兜底：一段失败不废整批（上层按段重试·保 M-5 硬化语义）
            outputs.append({"out": out_path, "ok": False, "error": str(e)[:200]})
            print(f"·· batch [{idx}/{total}] 失败：{e}", file=sys.stderr)
    print(json.dumps({"outputs": outputs}, ensure_ascii=False))   # stdout：唯一结果行


def run(args) -> None:
    if args.mode == "info":
        ch = load_channel()
        prof = ch.voice_profile() if ch else {}
        sr = prof.get("sample_rate") or DEFAULT_SR  # 频道 voice.default 采样率·兜底 DEFAULT_SR
        eng = (prof.get("engine") or "").strip()
        # 模型解析同 clone：显式 --model > 频道 LoRA 型 profile 的 mlx_model > 默认基座
        model_repo = args.model or (prof.get("mlx_model") if eng == ENGINE_LORA else None) or DEFAULT_MODEL
        print(f"venv      {_VENV_PY}")
        print(f"model     {model_repo}")
        print(f"path      {resolve_model_path(os.path.expanduser(str(model_repo)))}")
        print(f"sr        {sr} Hz")
        if ch is not None:
            print(f"channel   {ch.name}  voice.default={ch.get('voice.default')}  "
                  f"profiles={list((ch.get('voice.profiles') or {}).keys())}")
            if eng:
                print(f"engine    {eng}")
        return

    if args.mode == "batch":
        return run_batch(args)

    text = read_text(args)
    ch_model, ref_audio, ref_text = _resolve_clone_voice(args, is_clone=(args.mode == "clone"))
    # clone 硬闸：零样本型必须有 ref；LoRA 型音色烤进权重·无提示条也能出声（有 prompt 更贴·0.889）
    if args.mode == "clone" and not ch_model and not (ref_audio and ref_text):
        sys.exit("clone 需要 --ref-audio + --ref-text，或 --voice 指向 voice.md，"
                 "或频道 card.json voice.profiles（LoRA 型 mlx_model / 零样本型 ref_wav+ref_text）")
    # 模型优先级：显式 --model > 频道 LoRA 型 profile 的 mlx_model > 默认基座
    model = load_model(args.model or ch_model or DEFAULT_MODEL)
    audio, sr = synthesize(
        model, text,
        instruct=getattr(args, "instruct", None),
        ref_audio=ref_audio,
        ref_text=ref_text,
        timesteps=args.timesteps,
        cfg=args.cfg,
        chunk=not args.no_chunk,
        max_chars=args.max_chars,
        denoise=not args.no_denoise,
    )
    out = save_wav(audio, sr, args.out or default_out(args.mode))
    apply_warmth_eq(out, getattr(args, "warmth", 0.0))  # 可选暖声 EQ·默认 0 不动
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
        sp.add_argument("--model", default=None,
                        help="模型 repo 或本地目录（缺省：clone 下频道 LoRA 型 profile 取 mlx_model·"
                             f"否则 {DEFAULT_MODEL}）")
        sp.add_argument("--timesteps", type=int, default=10, help="CFM 步数：越低越快，7 是快/质量平衡点")
        sp.add_argument("--cfg", type=float, default=2.0, help="无分类器引导强度")
        sp.add_argument("--no-chunk", action="store_true", help="不按句切分（短文本用）")
        sp.add_argument("--max-chars", type=int, default=120, help="分句打包的单段最大字数")
        sp.add_argument("--no-denoise", action="store_true",
                        help="关闭逐段去噪（默认开：RNNoise 把每段底噪压到 ≤-80dB，保 raw 层稳定）")
        sp.add_argument("--warmth", type=float, default=0.0,
                        help="可选暖声 EQ 强度（默认 0=不动·声音用模型本音）：>0 更暖/厚/沉(去薄荷清脆)、"
                             "<0 更亮/脆；1.0=厚档、1.5~2 更狠。只调音色亮度不改基频。要大改「深沉」靠换沉的参考音")
        sp.add_argument("--play", action="store_true", help="生成后 afplay 试听")

    s_say = sub.add_parser("say", help="零样本：内置音色配音")
    common(s_say)

    s_design = sub.add_parser("design", help="音色设计：文字描述造音色")
    common(s_design)
    s_design.add_argument("--instruct", required=True, help="音色描述，如「温柔甜美的年轻女性主播」")

    s_clone = sub.add_parser("clone", help="声音克隆：参考音 + 转写复刻音色")
    common(s_clone)
    s_clone.add_argument("--voice", help="读 voice.md 音色 token 自动取 ref-audio/ref-text（替代手填）")
    s_clone.add_argument("--voice-profile", dest="voice_profile", default=None,
                         help="card.json voice.profiles 的 key（默认取 voice.default）")
    s_clone.add_argument("--ref-audio", dest="ref_audio", help="参考音频 wav（不用 --voice 时必填）")
    s_clone.add_argument("--ref-text", dest="ref_text", help="参考音频逐字转写（不用 --voice 时必填）")

    s_batch = sub.add_parser("batch", help="批量克隆：一份 manifest·模型载一次·合成多段（省重复加载）")
    common(s_batch)
    s_batch.add_argument("--manifest", required=True,
                         help="JSON 数组文件：[{text_file|text, out}, ...]（音色 / 参数全段共享）")
    s_batch.add_argument("--voice", help="读 voice.md 音色 token（同 clone·替代手填 ref）")
    s_batch.add_argument("--voice-profile", dest="voice_profile", default=None,
                         help="card.json voice.profiles 的 key（默认取 voice.default）")
    s_batch.add_argument("--ref-audio", dest="ref_audio", help="参考音频 wav（不用频道音色 / --voice 时）")
    s_batch.add_argument("--ref-text", dest="ref_text", help="参考音频逐字转写")

    s_info = sub.add_parser("info", help="打印环境 / 模型路径")
    s_info.add_argument("--model", default=None)

    return p


if __name__ == "__main__":
    run(build_parser().parse_args())
