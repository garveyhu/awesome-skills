# 视频管线要点

## 帧数 / 时长（Wan @16fps）

帧数必须是 **(4 的倍数)+1**：

| 时长 | 帧数 |
|------|------|
| 1s | 17 |
| 3s | 49 |
| 5s | 81（默认） |
| 10s | 161 |

`comfy.py i2v ... --length 49` 调时长。Mac 上先用 480×480 / 49 帧试，跑通再放大。

## Wan 2.2 独有：首尾帧控制

生成两张一致的关键帧（首帧 + 尾帧），用 `WanFirstLastFrameToVideo` 让 Wan 在中间插补运动——做分镜/转场很强。对应模板 `workflows/library/wan22-first-last.json`。

## i2v 组件纪律（容易静默出错）

Wan i2v 必须配齐：`UNETLoader`(扩散模型) + `umt5` 文本编码器 + **专用 `clip_vision_h`** + **专用 `wan_2.1_vae`**。任一配错，结果会**忽略你的输入图**而不报错。本 skill 内置 `wan22_i2v` 构建器已接对（注意官方完整 i2v 还会接 CLIPVision，本 skill 当前走 lightx2v 快速双采样路径；要 CLIPVision 版用 `wan22-img2vid.json` 模板）。

## 后处理链（需对应自定义节点）

`帧 → RIFE 补帧(2×/4×, rife47/rife49) → 每帧 FaceDetailer(denoise 0.3–0.4 保时间一致) → deflicker → 色彩校正 → VHS Video Combine`。

## FFmpeg 拼接 / 转场（Mac 原生，纯命令行）

ComfyUI 出的是片段，最终拼接交给 ffmpeg（`brew install ffmpeg`）。

**拼接前先验证**（避免 "Non-monotonous DTS" 失败）：用 `ffprobe` 比对各片段的 width/height/fps/codec 是否一致。

- **同编码/同分辨率/同帧率** → concat demuxer + `-c copy`（瞬间、无损）：
  ```bash
  printf "file '%s'\n" clip1.mp4 clip2.mp4 > list.txt
  ffmpeg -f concat -safe 0 -i list.txt -c copy out.mp4
  ```
- **混合输入 / 要转场** → 重编码：`xfade` 滤镜（`fade`/`wipeleft`/`slideright`/`circlecrop`/`fadeblack`），
  输出参数：`-c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -movflags +faststart`
- **音频**：`acrossfade=d=1` 交叉淡入；`amix` 叠加配乐；`-shortest` 裁到音轨长度。
- **对口型微调时序**：`ffmpeg -i video.mp4 -itsoffset 0.1 -i audio.wav -c:v copy -c:a aac out.mp4`（±offset 平移）。

**画质档位**：h264 `crf 18`(视觉无损) / `23`(更小)；h265 `crf 20 ≈ h264 18`。
