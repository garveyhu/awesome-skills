# 模型下载目录（按架构）

用户想新增某架构时，按此清单下到对应 `models/<目录>/`，下完 `discover` 即自动识别。URL 为 HuggingFace `resolve/main` 直链（仓库路径，下载时拼具体文件）。

> 下载命令示例（Mac）：`curl -L -o models/checkpoints/xxx.safetensors "<URL>"`，或用 ComfyUI-Manager / `hf download`。

## 文生图

| 架构 | 目录/文件 | 来源仓库 |
|------|----------|---------|
| SD1.5 | checkpoints/`v1-5-pruned-emaonly.safetensors` | stable-diffusion-v1-5/stable-diffusion-v1-5 |
| SDXL | checkpoints/`sd_xl_base_1.0.safetensors` | stabilityai/stable-diffusion-xl-base-1.0 |
| SD3 | checkpoints/`sd3_medium_incl_clips_t5xxlfp8.safetensors` | stabilityai/stable-diffusion-3-medium |
| **FLUX.1-dev** | diffusion_models/`flux1-dev.safetensors` | black-forest-labs/FLUX.1-dev |
| FLUX 编码器 | text_encoders/`clip_l.safetensors` + `t5xxl_fp16.safetensors` | comfyanonymous/flux_text_encoders |
| FLUX VAE | vae/`ae.safetensors` | black-forest-labs/FLUX.1-dev（你已有，Z-Image 也用它） |
| Stable Cascade | checkpoints/`stage_b.safetensors` + `stage_c.safetensors` | stabilityai/stable-cascade |

## 视频

| 架构 | 目录/文件 | 来源仓库 |
|------|----------|---------|
| Wan 2.2 t2v | diffusion_models/`wan2.2_t2v_14b.safetensors` | Comfy-Org/Wan_2.2_ComfyUI_Repackaged（split_files/...） |
| Wan 2.2 i2v | diffusion_models/`wan2.2_i2v_*`（你已有 high/low_noise 14B） | 同上 |
| Wan 编码器/VAE | text_encoders/`umt5_xxl_*`、clip_vision/`clip_vision_h.safetensors`、vae/`wan_2.1_vae.safetensors` | 同上（i2v 必须配 clip_vision） |
| HunyuanVideo | diffusion_models/`hunyuan_video_t2v_720p_bf16.safetensors` + text_encoders/`llava_llama3_fp16.safetensors` | Comfy-Org/HunyuanVideo_repackaged |
| LTXV（轻量,Mac友好） | diffusion_models/`ltxv_2b_0.9.7_dev_fp8.safetensors` | Lightricks/LTX-Video |
| Mochi | diffusion_models/`mochi_preview_bf16.safetensors` | genmo/mochi-1-preview |
| Cosmos | diffusion_models/`cosmos_*_7b.safetensors` | nvidia/Cosmos-1.0-Diffusion-7B-* |

## 其它

| 类型 | 目录/文件 | 来源 |
|------|----------|------|
| Stable Audio | checkpoints/`stable_audio_open_1.0` | stabilityai/stable-audio-open-1.0 |
| Hunyuan3D | diffusion_models/`hunyuan3d_v2_turbo.safetensors` | Tencent/Hunyuan3D-2 |
| ControlNet SD15 | controlnet/`control_v11p_sd15_canny.safetensors` | lllyasviel/ControlNet-v1-1 |
| ControlNet SDXL | controlnet/`diffusers_xl_canny_full.safetensors` | diffusers/controlnet-canny-sdxl-1.0 |
| 放大 | upscale_models/`RealESRGAN_x4plus.pth`、`4x-UltraSharp` | ai-forever/Real-ESRGAN 等 |

## 选型经验

- **写实静图**：FLUX.1-dev（最好但慢）vs RealVisXL/Juggernaut XL（快，SDXL 系）。
- **放大器**：`4x-UltraSharp`(脸/细节)、`4x-Foolhardy-Remacri`(通用)、`SUPIR`(最好但慢)。
- **Mac 上视频**：优先轻量的 LTXV / Wan 5B 做草稿，14B 出终稿。

> 装好新架构后，若本 skill 没有对应内置构建器，用 `templates` 列出的同架构 UI 模板 + `raw` 直接跑（自动转 API）。
