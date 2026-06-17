# 架构配方速查

每种生成模型架构的「加载方式 + 关键采样参数」。内置构建器已实现前几种；其余给出要点，便于按 `api-format.md` 手写工作流。所有节点输入名以 `/object_info/<节点>` 实测为准。

## 两种加载范式

| 范式 | 特征 | 加载节点 |
|------|------|---------|
| **Checkpoint（单文件）** | 一个 `.safetensors` 内含 UNet+CLIP+VAE（SD1.5/SDXL/多数融合模型） | `CheckpointLoaderSimple` → 输出 MODEL/CLIP/VAE 三槽 |
| **Split（拆分）** | UNet、文本编码器、VAE 分开放（FLUX/Z-Image/Wan/SD3/Hunyuan…） | `UNETLoader`(diffusion_models) + `CLIPLoader`/`DualCLIPLoader` + `VAELoader` |

> 这就是为什么 split 模型在 `CheckpointLoaderSimple` 的下拉里**看不到**——它们要用 `UNETLoader`。

## CLIPLoader 的 type（split 架构必须选对）

`CLIPLoader.type` 实测枚举：`stable_diffusion, stable_cascade, sd3, stable_audio, mochi, ltxv, pixart, cosmos, lumina2, wan, hidream, chroma, ace, omnigen2, qwen_image, hunyuan_image, flux2, ovis, longcat_image, cogvideox, lens, pixeldit, ideogram4`

| 模型族 | 文本编码器 | CLIP type |
|--------|-----------|-----------|
| Z-Image | qwen_3_4b | `lumina2` |
| Wan 2.x | umt5_xxl | `wan` |
| FLUX | clip_l + t5xxl（双） | `flux`（用 `DualCLIPLoader`） |
| SD3 | clip_l + clip_g + t5 | `sd3` |
| LTXV | t5xxl | `ltxv` |
| HunyuanVideo | llava + clip_l | 见官方模板 |

## 已实现构建器的精确配方

### Z-Image Turbo（t2i，`zimage_t2i`）
- `UNETLoader`(z_image_turbo) → `ModelSamplingAuraFlow` shift=**3**
- `CLIPLoader`(qwen, type=**lumina2**) → `CLIPTextEncode`(正) → `ConditioningZeroOut`(当负向)
- `EmptySD3LatentImage` → `KSampler` steps=**8** / cfg=**1** / sampler=**res_multistep** / scheduler=**simple** / denoise=1
- `VAEDecode`(ae VAE) → `SaveImage`
- Turbo 是蒸馏模型：步数少、cfg=1，**不要**调高 cfg。

### Checkpoint SD/SDXL（t2i，`checkpoint_t2i`）
- `CheckpointLoaderSimple` → CLIP 接两个 `CLIPTextEncode`(正/负)
- `EmptyLatentImage`（注意：SD 系用这个，不是 SD3Latent）→ `KSampler` steps≈20 / cfg≈7 / euler / normal
- SDXL 建议 1024×1024 起；SD1.5 建议 512×512。

### FLUX（t2i，`flux_t2i`）
- `UNETLoader`(flux) + `DualCLIPLoader`(clip_l, t5xxl, type=flux) + `VAELoader`(ae)
- `CLIPTextEncode` → `FluxGuidance` guidance≈3.5（FLUX 用 guidance 而非 cfg；KSampler 的 cfg=1）
- schnell：steps≈4；dev：steps≈20。正负向都接同一条（FLUX 无真负向）。

### Wan 2.2 14B I2V（i2v，`wan22_i2v`）
- **双模型**：high_noise 与 low_noise 各一条 `UNETLoader`，各自挂对应的 `lightx2v_4steps` LoRA(`LoraLoaderModelOnly` strength=1) → `ModelSamplingSD3` shift=**5**
- `CLIPLoader`(umt5, type=**wan**) → 正/负 `CLIPTextEncode`
- `LoadImage` + `WanImageToVideo`(width/height/length=81/batch=1, 接 vae 与起始图) → 输出 positive/negative/latent 三槽
- **两段采样**：`KSamplerAdvanced` 高噪段(add_noise=enable, 0→2步, 保留余噪) → 低噪段(add_noise=disable, 2→4步)，euler/simple/cfg=1
- `VAEDecode` → `CreateVideo` fps=16 → `SaveVideo`
- length 与帧数：81 帧 ≈ 5s @16fps。Mac 上很慢，先降分辨率/帧数试。

## 全架构 → 关键节点链速查（20+）

要手写或改写某架构工作流时，照这张表搭骨架（"CLIP type"指 CLIPLoader/DualCLIPLoader 的 type 字段）。**节点输入名一律以 `/object_info` 实测为准**。

| 架构 | Loader 链 | CLIP type | Latent 节点 | 采样建议 | 输出 |
|------|-----------|-----------|------------|---------|------|
| SD1.5 | CheckpointLoaderSimple | — | EmptyLatentImage(512²) | euler_a/dpmpp_2m, karras, 20-30步, cfg7-8 | SaveImage |
| SDXL | CheckpointLoaderSimple | — | EmptyLatentImage(1024²) | dpmpp_2m, karras, cfg7-8 | SaveImage |
| SD3 | UNETLoader+TripleCLIPLoader(clip_l+clip_g+t5)+VAELoader | — | EmptySD3LatentImage | dpmpp_2m/sgm_uniform, 28步, cfg4.5 | SaveImage |
| **FLUX** | UNETLoader+DualCLIPLoader(clip_l+t5xxl)+VAELoader | `flux` | EmptyLatentImage(1024²) | custom sampler: RandomNoise→BasicGuider→KSamplerSelect(euler)→BasicScheduler(simple/beta)→SamplerCustomAdvanced; guidance3.5, 20-28步 | SaveImage |
| **Z-Image** | UNETLoader+CLIPLoader(qwen)+VAELoader | `lumina2` | EmptySD3LatentImage | ModelSamplingAuraFlow shift3 + KSampler res_multistep/simple, 8步, cfg1 | SaveImage |
| **Wan2.2 t2v** | UNETLoader+CLIPLoader(umt5)+VAELoader(wan_2.1_vae) | `wan` | WanImageToVideo(无start_image) | KSampler euler/normal, 25步, cfg6, 832×480×81 | SaveAnimatedWEBP/CreateVideo |
| **Wan2.2 i2v** | 同上 + CLIPVisionLoader+CLIPVisionEncode | `wan` | WanImageToVideo(接clip_vision+start_image) | 见 architectures 上文 Wan 配方 | 同上 |
| Wan 变体 | 同 Wan 基座 | `wan` | WanFirstLastFrameToVideo / WanCameraImageToVideo(+WanCameraEmbedding) / WanVaceToVideo(动作迁移) | — | — |
| HunyuanVideo | UNETLoader+CLIPLoader+VAELoader | (单) | EmptyHunyuanLatentVideo | euler/normal, 30步, cfg6, 848×480 | SaveAnimatedWEBP |
| LTXV | UNETLoader+CLIPLoader+VAELoader | `ltxv` | EmptyLTXVLatentVideo + **LTXVConditioning(frame_rate)** | KSampler | SaveAnimatedWEBP |
| Mochi | UNETLoader+CLIPLoader+VAELoader | (单) | EmptyMochiLatentVideo(length step=6) | KSampler | SaveAnimatedWEBP |
| Cosmos | UNETLoader+CLIPLoader+VAELoader | (单) | EmptyCosmosLatentVideo / CosmosImageToVideoLatent | KSampler | SaveAnimatedWEBP |
| Stable Audio | CheckpointLoaderSimple | — | EmptyLatentAudio + **ConditioningStableAudio(seconds)** | KSampler → **VAEDecodeAudio** | SaveAudio |
| Hunyuan3D v2 | UNETLoader+VAELoader+CLIPVisionLoader | — | EmptyLatentHunyuan3Dv2 + **Hunyuan3Dv2Conditioning** | KSampler → VAEDecodeHunyuan3D(VOXEL)→VoxelToMeshBasic | **SaveGLB** |
| Stable Cascade | CheckpointLoaderSimple ×2(stage_c/b) | — | StableCascade_EmptyLatentImage(出双LATENT) | 两段 KSampler | SaveImage |

多 CLIP loader 备忘：`DualCLIPLoader` type 含 `sdxl/sd3/flux/hunyuan_video/hidream/ltxv`；`TripleCLIPLoader`=SD3；`QuadrupleCLIPLoader`=HiDream。

**采样器全集**（校验白名单）：euler, euler_ancestral, heun, dpm_2, dpmpp_2s_ancestral, dpmpp_sde, dpmpp_2m, dpmpp_2m_sde, dpmpp_3m_sde, ddpm, lcm, deis, ddim, uni_pc, uni_pc_bh2 等。
**调度器**：normal, karras, exponential, sgm_uniform, simple, ddim_uniform, beta。

> 想直接用上面任一架构：`scripts/comfy.py templates` 里有对应 UI 模板，`raw <模板>` 自动转 API 跑（先按 `models-catalog.md` 装好模型）。

## 未实现架构的要点（按需手写）

- **Wan t2v**：同 i2v 但无 `LoadImage`/`start_image`，用 `EmptyHunyuanLatentVideo` 或 Wan 专用空 latent；其余采样同 i2v。
- **HunyuanVideo / LTXV / Mochi / Cosmos**：直接参考 ComfyUI 自带官方模板（见 `api-format.md` 模板路径），它们都有完整示例。
- 通用做法：找到官方 UI 模板 → 对照 `/object_info` 把每个节点转成 API 格式 → `raw` 提交。
