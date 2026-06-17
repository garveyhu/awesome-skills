# 提示词工程（按架构区分）

不同架构的提示词写法**完全不同**，把 SDXL 的习惯带到 FLUX/Z-Image/视频上会明显掉效果。核心对照：

| 架构 | CFG | 质量堆词? | 风格写法 | 负向提示 |
|------|-----|----------|---------|---------|
| **FLUX / Z-Image**(DiT 类) | **3.5–4**（Z-Image Turbo=1） | **不要**——"masterpiece, 8k uhd"反而**伤**画质 | 自然语言整句，50–100 词 | 极简：`blurry, low quality, distorted, deformed, watermark, text` |
| **SDXL** | 7–9 | **要**，且放最前 | 质量词 + 权重语法 `(term:1.3)` | 长、激进 |
| **SD1.5** | 7–8 | 必须 | 标签式，较短(30–80词) | 标准 |
| **Wan 视频** | 5–7 | 极少 | **简洁、动作优先**，20–50 词 | `static, frozen, jerky motion, flickering, distorted face, glitch` |

> **Z-Image 是 DiT/flow 类模型，按 FLUX 套路写**：自然语言、低 CFG、别堆质量词、负向精简。Turbo 版 cfg=1 不要调高。

## 可复用提示词结构

- **SDXL**：`{质量词}, {触发词}, {主体}, {细节}, {场景}, {风格}`
- **FLUX / Z-Image**：`{主体描述}, {场景}, {光照}, {镜头/风格}`
- **Wan(i2v/t2v)**：`{主体}, {动作/运动}, {场景}, {质量}` —— **描述运动，不只是外观**
  例：`young woman with auburn hair, talking naturally with gentle hand gestures, seated at a desk, soft studio lighting, high quality`

## 负向提示积木

- 通用(SDXL/SD1.5)：`(worst quality:1.4), (low quality:1.4), blurry, deformed, bad anatomy, bad hands, extra fingers, fused fingers, text, watermark, signature, jpeg artifacts`
- 写实加料：`3d render, cartoon, anime, illustration, painting, cgi, plastic skin, smooth skin, airbrushed, doll, mannequin, oversaturated`
- **视频专用**：`static, frozen, jerky motion, distorted face, glitch, artifacts, flickering, jittery, unnatural movement`
- FLUX/Z-Image：负向尽量短，过长反而干扰。

## 关键词速查

- **情绪**：happy→`warm smile, bright eyes`；serious→`focused gaze, neutral mouth`；confident→`direct eye contact, slight smirk, chin up`；thoughtful→`looking away, contemplative gaze`
- **光照**：studio→`softbox, key light`；natural→`golden hour, window light`；dramatic→`chiaroscuro, rim lighting, high contrast`；cinematic→`anamorphic, color grading, atmospheric`

## 常见画质问题 → 提示词层面的解法

- **塑料/过度光滑皮肤**：从负向里**删掉** "smooth skin"；正向加 `detailed skin texture, skin pores`；必要时 skin LoRA 0.2–0.4 或 FaceDetailer denoise 0.3–0.4。
- **过饱和**：降 CFG；负向加 `oversaturated`。
- **颜色发灰/发白**：确认 VAE 接对了；换 scheduler。
- **模糊**：步数提到 25–30；分辨率匹配架构（SD1.5=512, SDXL/FLUX/Z-Image=1024）。
