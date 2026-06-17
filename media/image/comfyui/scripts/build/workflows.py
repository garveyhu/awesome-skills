"""工作流构建器：把"意图 + 参数 + 选定模型"组装成 ComfyUI API 格式工作流(dict)。

单一职责：只产出 API 格式 JSON（节点 id -> {class_type, inputs}），不提交、不发现。
每个构建器对应一个架构族，节点结构与默认参数均来自官方模板 + /object_info 实测，
保证提交后能真正跑通。模型文件名通过参数传入，不写死——换同族模型即可复用。

API 格式约定：连线用 [来源节点id, 输出槽序号]，常量直接写值。
"""

from __future__ import annotations


class BuildError(RuntimeError):
    """缺少必要模型/参数，无法组装工作流。"""


# ---- 自动选模助手（在库存里按关键词挑一个合适的） -------------------------

def _first(names: list[str], *keywords: str, exclude: tuple[str, ...] = ()) -> str | None:
    for n in names:
        low = n.lower()
        if all(k.lower() in low for k in keywords) and not any(e.lower() in low for e in exclude):
            return n
    return None


def _require(value, msg: str):
    if not value:
        raise BuildError(msg)
    return value


# ==========================================================================
# 文生图：Z-Image Turbo（split 架构，少步快出图）
# 配方来自官方模板 image_z_image_turbo：CLIP=lumina2, AuraFlow shift=3,
# KSampler steps=8 / cfg=1 / res_multistep / simple。
# ==========================================================================

def zimage_t2i(p: dict, inv: dict) -> dict:
    model = p.get("model") or _require(
        _first(inv["diffusion_models"], "z_image"),
        "未找到 z_image 系列扩散模型",
    )
    clip = p.get("clip") or _require(
        # Z-Image 要 qwen_3_4b(2560 维);排除 qwen_2.5_vl_7b(3584 维,char-edit 用),
        # 否则会选错导致 LayerNorm 形状不匹配报错。
        _first(inv["clip"], "qwen_3")
        or _first(inv["clip"], "lumina")
        or _first(inv["clip"], "qwen", exclude=("vl", "2.5", "2_5")),
        "Z-Image 需要 qwen_3_4b / lumina 文本编码器，未找到",
    )
    vae = p.get("vae") or _require(
        _first(inv["vae"], "ae", exclude=("wan",)),
        "Z-Image 需要 ae.safetensors VAE，未找到",
    )
    steps = p.get("steps", 8)
    return {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": model, "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": clip, "type": "lumina2", "device": "default"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": vae}},
        "4": {"class_type": "ModelSamplingAuraFlow", "inputs": {"model": ["1", 0], "shift": p.get("shift", 3.0)}},
        "5": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": p["prompt"]}},
        "6": {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": ["5", 0]}},
        "7": {"class_type": "EmptySD3LatentImage", "inputs": {"width": p.get("width", 1024), "height": p.get("height", 1024), "batch_size": p.get("batch", 1)}},
        "8": {"class_type": "KSampler", "inputs": {
            "model": ["4", 0], "seed": p.get("seed", 0), "steps": steps, "cfg": p.get("cfg", 1.0),
            "sampler_name": p.get("sampler", "res_multistep"), "scheduler": p.get("scheduler", "simple"),
            "positive": ["5", 0], "negative": ["6", 0], "latent_image": ["7", 0], "denoise": 1.0}},
        "9": {"class_type": "VAEDecode", "inputs": {"samples": ["8", 0], "vae": ["3", 0]}},
        "10": {"class_type": "SaveImageClean", "inputs": {"images": ["9", 0], "filename_prefix": p.get("prefix", "zimage")}},
    }


# ==========================================================================
# 文生图：传统 checkpoint（SD1.5 / SDXL / 多数融合模型）
# 单文件 checkpoint 自带 MODEL/CLIP/VAE 三件套。
# ==========================================================================

def checkpoint_t2i(p: dict, inv: dict) -> dict:
    model = p.get("model") or _require(
        inv["checkpoints"][0] if inv["checkpoints"] else None,
        "未找到任何 checkpoint 模型",
    )
    neg = p.get("negative", "text, watermark, low quality, worst quality, blurry")
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": model}},
        "2": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["1", 1], "text": p["prompt"]}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["1", 1], "text": neg}},
        "4": {"class_type": "EmptyLatentImage", "inputs": {"width": p.get("width", 1024), "height": p.get("height", 1024), "batch_size": p.get("batch", 1)}},
        "5": {"class_type": "KSampler", "inputs": {
            "model": ["1", 0], "seed": p.get("seed", 0), "steps": p.get("steps", 20), "cfg": p.get("cfg", 7.0),
            "sampler_name": p.get("sampler", "euler"), "scheduler": p.get("scheduler", "normal"),
            "positive": ["2", 0], "negative": ["3", 0], "latent_image": ["4", 0], "denoise": 1.0}},
        "6": {"class_type": "VAEDecode", "inputs": {"samples": ["5", 0], "vae": ["1", 2]}},
        "7": {"class_type": "SaveImageClean", "inputs": {"images": ["6", 0], "filename_prefix": p.get("prefix", "checkpoint")}},
    }


# ==========================================================================
# 文生图：FLUX（split，dev/schnell）。需要 clip_l + t5xxl 双编码器 + ae VAE。
# 注意：此构建器在用户安装了 flux 全套后才能跑；缺件会给出明确报错。
# ==========================================================================

def flux_t2i(p: dict, inv: dict) -> dict:
    model = p.get("model") or _require(_first(inv["diffusion_models"], "flux"), "未找到 flux 扩散模型")
    clip_l = p.get("clip_l") or _require(_first(inv["clip"], "clip_l"), "FLUX 需要 clip_l 编码器")
    t5 = p.get("t5") or _require(_first(inv["clip"], "t5xxl") or _first(inv["clip"], "t5"), "FLUX 需要 t5xxl 编码器")
    vae = p.get("vae") or _require(_first(inv["vae"], "ae", exclude=("wan",)), "FLUX 需要 ae VAE")
    is_schnell = "schnell" in model.lower()
    steps = p.get("steps", 4 if is_schnell else 20)
    return {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": model, "weight_dtype": "default"}},
        "2": {"class_type": "DualCLIPLoader", "inputs": {"clip_name1": clip_l, "clip_name2": t5, "type": "flux"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": vae}},
        "4": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": p["prompt"]}},
        "5": {"class_type": "FluxGuidance", "inputs": {"conditioning": ["4", 0], "guidance": p.get("cfg", 3.5)}},
        "6": {"class_type": "EmptySD3LatentImage", "inputs": {"width": p.get("width", 1024), "height": p.get("height", 1024), "batch_size": p.get("batch", 1)}},
        "7": {"class_type": "KSampler", "inputs": {
            "model": ["1", 0], "seed": p.get("seed", 0), "steps": steps, "cfg": 1.0,
            "sampler_name": p.get("sampler", "euler"), "scheduler": p.get("scheduler", "simple"),
            "positive": ["5", 0], "negative": ["5", 0], "latent_image": ["6", 0], "denoise": 1.0}},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["7", 0], "vae": ["3", 0]}},
        "9": {"class_type": "SaveImageClean", "inputs": {"images": ["8", 0], "filename_prefix": p.get("prefix", "flux")}},
    }


# ==========================================================================
# 图生视频：Wan 2.2 14B I2V（双模型高噪+低噪两段采样 + lightx2v 4步加速 LoRA）
# 配方来自官方模板 video_wan2_2_14B_i2v 的快速路径：
# ModelSamplingSD3 shift=5, KSamplerAdvanced 共4步(高噪0-2 / 低噪2-4), euler/simple, cfg=1。
# ==========================================================================

def wan22_i2v(p: dict, inv: dict) -> dict:
    high = p.get("model_high") or _require(_first(inv["diffusion_models"], "wan", "i2v", "high"), "未找到 wan i2v high_noise 模型")
    low = p.get("model_low") or _require(_first(inv["diffusion_models"], "wan", "i2v", "low"), "未找到 wan i2v low_noise 模型")
    lora_high = p.get("lora_high") or _first(inv["loras"], "lightx2v", "high")
    lora_low = p.get("lora_low") or _first(inv["loras"], "lightx2v", "low")
    clip = p.get("clip") or _require(_first(inv["clip"], "umt5") or _first(inv["clip"], "t5"), "Wan 需要 umt5 文本编码器")
    vae = p.get("vae") or _require(_first(inv["vae"], "wan"), "Wan 需要 wan_2.1_vae")
    image = _require(p.get("image"), "i2v 需要起始图片（服务端文件名，先用 upload 上传）")

    neg = p.get("negative", "色调艳丽，过曝，静态，细节模糊不清，最差质量，低质量，JPEG压缩残留，丑陋的，"
                            "残缺的，多余的手指，画得不好的手部，画得不好的脸部，畸形的，毁容的，杂乱的背景")
    total = p.get("steps", 4)
    split = p.get("split", total // 2)  # 高噪段结束 / 低噪段开始的步数
    seed = p.get("seed", 0)
    shift = p.get("shift", 5.0)

    # 高噪模型链：UNET -> (可选 lightx2v LoRA) -> ModelSamplingSD3
    wf: dict = {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": high, "weight_dtype": "default"}},
        "4": {"class_type": "UNETLoader", "inputs": {"unet_name": low, "weight_dtype": "default"}},
        "7": {"class_type": "CLIPLoader", "inputs": {"clip_name": clip, "type": "wan", "device": "default"}},
        "8": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["7", 0], "text": p["prompt"]}},
        "9": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["7", 0], "text": neg}},
        "10": {"class_type": "VAELoader", "inputs": {"vae_name": vae}},
        "11": {"class_type": "LoadImage", "inputs": {"image": image}},
    }
    high_model_src = ["1", 0]
    if lora_high:
        wf["2"] = {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["1", 0], "lora_name": lora_high, "strength_model": 1.0}}
        high_model_src = ["2", 0]
    wf["3"] = {"class_type": "ModelSamplingSD3", "inputs": {"model": high_model_src, "shift": shift}}

    low_model_src = ["4", 0]
    if lora_low:
        wf["5"] = {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["4", 0], "lora_name": lora_low, "strength_model": 1.0}}
        low_model_src = ["5", 0]
    wf["6"] = {"class_type": "ModelSamplingSD3", "inputs": {"model": low_model_src, "shift": shift}}

    wf["12"] = {"class_type": "WanImageToVideo", "inputs": {
        "positive": ["8", 0], "negative": ["9", 0], "vae": ["10", 0],
        "width": p.get("width", 640), "height": p.get("height", 640),
        "length": p.get("length", 81), "batch_size": 1, "start_image": ["11", 0]}}
    # 高噪段：加噪，跑 0..split，保留余噪交给低噪段
    wf["13"] = {"class_type": "KSamplerAdvanced", "inputs": {
        "model": ["3", 0], "add_noise": "enable", "noise_seed": seed, "steps": total, "cfg": p.get("cfg", 1.0),
        "sampler_name": p.get("sampler", "euler"), "scheduler": p.get("scheduler", "simple"),
        "positive": ["12", 0], "negative": ["12", 1], "latent_image": ["12", 2],
        "start_at_step": 0, "end_at_step": split, "return_with_leftover_noise": "enable"}}
    # 低噪段：不加噪，接着跑 split..total
    wf["14"] = {"class_type": "KSamplerAdvanced", "inputs": {
        "model": ["6", 0], "add_noise": "disable", "noise_seed": seed, "steps": total, "cfg": p.get("cfg", 1.0),
        "sampler_name": p.get("sampler", "euler"), "scheduler": p.get("scheduler", "simple"),
        "positive": ["12", 0], "negative": ["12", 1], "latent_image": ["13", 0],
        "start_at_step": split, "end_at_step": total, "return_with_leftover_noise": "disable"}}
    wf["15"] = {"class_type": "VAEDecode", "inputs": {"samples": ["14", 0], "vae": ["10", 0]}}
    wf["16"] = {"class_type": "CreateVideo", "inputs": {"images": ["15", 0], "fps": p.get("fps", 16.0)}}
    wf["17"] = {"class_type": "SaveVideo", "inputs": {"video": ["16", 0], "filename_prefix": p.get("prefix", "video/wan_i2v"), "format": "auto", "codec": "auto"}}
    return wf


# 构建器注册表：inventory.classify() 里的 builder 字段对应这里的键
BUILDERS = {
    "zimage_t2i": zimage_t2i,
    "checkpoint_t2i": checkpoint_t2i,
    "flux_t2i": flux_t2i,
    "wan22_i2v": wan22_i2v,
}
