# 内置工作流模板索引

两类模板：
- 本目录(`workflows/library/`)—— 通用架构 UI 模板(来自 comfyui-workflow-skill,已去 LLM_party)。用 `scripts/comfy.py raw workflows/library/<文件>` 直接跑(自动转 API)，**前提是已装对应模型**（见 `reference/models-catalog.md`）。
- `example_*.json` —— 已是 API 格式、针对当前库存的实例（Z-Image t2i、Wan i2v），可直接 `raw`。

另外 ComfyUI 自带 **443+ 官方模板**（路径见 `reference/api-format.md`），同样能用 `raw` 跑。

## 模板清单

| 模板 | 任务 | 架构 | 说明 |
|------|------|------|------|
| flux-txt2img / -img2img / -lora | t2i/i2i | FLUX | ⭐ custom sampler 链范例 |
| sdxl-txt2img / -img2img / -lora | t2i/i2i | SDXL | 经典基线 |
| sdxl-controlnet | t2i+控制 | SDXL | ControlNetApplyAdvanced 范例 |
| sdxl-inpaint | 局部重绘 | SDXL | VAEEncodeForInpaint 范例 |
| sd3-txt2img | t2i | SD3 | TripleCLIP 范例 |
| sd15-* (txt2img/img2img/lora/controlnet/inpaint) | t2i/i2i | SD1.5 | 偏旧，参考链路 |
| wan22-txt2vid | t2v | Wan2.2 | ⭐ 你已有 Wan |
| wan22-img2vid | i2v | Wan2.2 | ⭐ CLIPVision+WanImageToVideo 完整版 |
| wan22-first-last | i2v(首尾帧) | Wan2.2 | ⭐ 首尾帧插补，分镜利器 |
| wan22-fun-control / -camera | 控制视频 | Wan2.2 | 运动/相机控制 |
| wan22-motion-transfer | 动作迁移 | Wan2.2 | WanVaceToVideo |
| ltxv-txt2vid / -img2vid | t2v/i2v | LTXV | 轻量，Mac 友好候选 |
| hunyuan-video / -i2v | t2v/i2v | HunyuanVideo | 显存需求大 |
| mochi-txt2vid | t2v | Mochi | — |
| cosmos-txt2vid / -img2vid | t2v/i2v | Cosmos | 7B 偏大 |
| upscale-model | 放大 | 通用 | 极简实用 |
| stable-audio | 音频 | StableAudio | VAEDecodeAudio 范例 |
| stable-cascade | t2i | Cascade | 两阶段范例 |
| hunyuan3d-v2 | 图→3D | Hunyuan3D | SaveGLB/VOXEL 范例 |
| combo-flux-t2i-wan22-i2v | 跨架构串联 | FLUX→Wan | ⭐ 生图→图生视频全流程学习样本 |

> 这些模板里的模型文件名是模板作者环境的，多半与你库存不符。`raw` 跑会因 `value_not_in_list` 报错并列出你的真实可选项——把模板里的模型名换成你 `discover` 出的名字即可（或直接用内置构建器 `t2i`/`i2v`，它们自动选模）。
