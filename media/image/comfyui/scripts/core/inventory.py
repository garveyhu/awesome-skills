"""库存发现：查询运行中的 ComfyUI 当前能加载哪些模型，并归类到生成能力。

单一职责：只回答"现在装了什么、能干什么"，不构建工作流、不提交任务。
所有清单都来自 /object_info 的真实枚举（服务端实际能加载的才会出现），
因此是动态的——你以后新下任何模型，这里自动反映，不写死。
"""

from __future__ import annotations

from comfy_api import ComfyClient


def _enum(client: ComfyClient, node: str, field: str, group: str = "required") -> list[str]:
    """取某节点某输入的枚举候选（拿不到就返回空，保持容错）。"""
    try:
        spec = client.object_info(node)[node]["input"][group][field][0]
        return [x for x in spec if isinstance(x, str)] if isinstance(spec, list) else []
    except Exception:
        return []


def discover(client: ComfyClient) -> dict:
    """返回结构化库存：各类模型清单 + 推断出的生成能力 capabilities。"""
    inv = {
        "checkpoints": _enum(client, "CheckpointLoaderSimple", "ckpt_name"),
        "diffusion_models": _enum(client, "UNETLoader", "unet_name"),
        "vae": _enum(client, "VAELoader", "vae_name"),
        "clip": _enum(client, "CLIPLoader", "clip_name"),
        "clip_types": _enum(client, "CLIPLoader", "type"),
        "loras": _enum(client, "LoraLoaderModelOnly", "lora_name"),
        "upscale_models": _enum(client, "UpscaleModelLoader", "model_name"),
        "controlnet": _enum(client, "ControlNetLoader", "control_net_name"),
    }
    try:
        stats = client.ping().get("system", {})
        inv["system"] = {
            "os": stats.get("os"),
            "ram_total_gb": round(stats.get("ram_total", 0) / 1024**3, 1),
            "comfyui_version": stats.get("comfyui_version"),
            "python": stats.get("python_version", "").split()[0],
        }
    except Exception:
        inv["system"] = {}
    inv["capabilities"] = classify(inv)
    return inv


def _pick(names: list[str], *keywords: str) -> list[str]:
    """挑出文件名里包含全部关键词的模型（大小写不敏感）。"""
    out = []
    for n in names:
        low = n.lower()
        if all(k.lower() in low for k in keywords):
            out.append(n)
    return out


def classify(inv: dict) -> list[dict]:
    """把原始模型清单推断成"能做什么"。新增架构在这里加一条规则即可。

    每条能力含：task(t2i/i2v/t2v/...)、family(架构族)、builder(对应 workflows.py 的构建器)、
    models(可用主模型)。这是连接"发现"与"构建"的唯一映射点。
    """
    caps: list[dict] = []
    ckpts = inv["checkpoints"]
    dm = inv["diffusion_models"]

    if ckpts:
        caps.append({"task": "t2i", "family": "checkpoint", "builder": "checkpoint_t2i", "models": ckpts})

    z = _pick(dm, "z_image")
    if z:
        caps.append({"task": "t2i", "family": "zimage", "builder": "zimage_t2i", "models": z})

    flux = _pick(dm, "flux")
    if flux:
        caps.append({"task": "t2i", "family": "flux", "builder": "flux_t2i", "models": flux})

    wan_i2v = _pick(dm, "wan", "i2v")
    if wan_i2v:
        caps.append({"task": "i2v", "family": "wan22", "builder": "wan22_i2v", "models": wan_i2v})

    wan_t2v = _pick(dm, "wan", "t2v")
    if wan_t2v:
        caps.append({"task": "t2v", "family": "wan22", "builder": "wan22_t2v", "models": wan_t2v})

    return caps


def format_report(inv: dict) -> str:
    """人类可读的库存报告（给用户看 / 给 Claude 决策用）。"""
    lines = ["# ComfyUI 库存报告", ""]
    sys = inv.get("system", {})
    if sys:
        lines.append(
            f"运行环境: {sys.get('os')} · ComfyUI {sys.get('comfyui_version')} · "
            f"Python {sys.get('python')} · RAM {sys.get('ram_total_gb')}GB"
        )
        lines.append("")
    lines.append("## 当前可做（capabilities）")
    if inv["capabilities"]:
        for c in inv["capabilities"]:
            lines.append(f"- [{c['task']}] {c['family']}  →  {', '.join(c['models'])}")
    else:
        lines.append("- （未发现可用主模型，先去 models/ 下放模型）")
    lines.append("")
    for key, title in [
        ("checkpoints", "Checkpoints"),
        ("diffusion_models", "Diffusion models (split)"),
        ("clip", "CLIP / 文本编码器"),
        ("vae", "VAE"),
        ("loras", "LoRA"),
        ("controlnet", "ControlNet"),
        ("upscale_models", "放大模型"),
    ]:
        vals = inv.get(key) or []
        if vals:
            lines.append(f"## {title}")
            lines.extend(f"- {v}" for v in vals)
            lines.append("")
    return "\n".join(lines)
