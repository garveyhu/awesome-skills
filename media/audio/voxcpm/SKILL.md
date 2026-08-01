---
name: voxcpm
description: >-
  本地文字转语音 / 配音（VoxCPM2 跑在 Apple MLX 上，离线、可商用 Apache-2.0）。当用户要「配音 / 语音合成 / 文字转语音 / 给视频配旁白 / 念稿 / 做音频 / 声音克隆 / 造一个音色 / text-to-speech / TTS / voice over / narrate」，且未指定其他音频后端时使用。三模式：say 零样本内置音色、design 用文字描述造音色、clone 用参考音克隆音色；支持 30 语言 + 中文多方言、48kHz、长文本按句切分拼接，适合 5 分钟级旁白。是媒体生态里继出图(comfyui/codex/gemini)之后的第一条音频后端。
---

# voxcpm —— 本地配音 / TTS（VoxCPM2 on Apple MLX）

给 Claude 补「音频自由」：在这台 Mac 上离线把文字合成成 48kHz 录音棚级语音，速度快过实时（M3 实测 RTF ≈ 0.4~0.6），能力对标出图生态——文字描述造音色、参考音克隆、长旁白一把出。

> **角色边界**：本 skill = **MLX VoxCPM 运行时**（zero-shot 克隆 / 内置 / 造音色 + media-studio 出片管线的 TTS 引擎）。要给某频道**训练一个稳定的专属音色**（录音 → LoRA 微调 → 合并 → MLX），去 **voice-lab 音色工作台**（`~/Coding/Archer/voice-lab`·管训练与生产模型）。二者分工：voice-lab 产模型、本 skill 管运行——训好的合并模型直接 `clone/say --model <voice-lab>/models/<名>/mlx-8bit` 就能跑（`load_model` 已放行 trust_remote_code·支持加载本地微调/合并模型）。

## 一条命令的三模式

入口 `scripts/voxcpm_gen.py`，**任意 python 调用即可**（脚本会自动重定向到专用 venv `~/.venvs/mlx-audio`，并把模型经魔搭解析好）。stdout 只吐产物 wav 路径，进度走 stderr。

**自动出厂清理**（每段生成后）：① `edge_fade` 首尾去咔哒 ② `denoise` 逐段去底噪（默认开·`--no-denoise` 关·长稿停顿易产音乐噪声时关它、交给出片管线 `tone_even`）。注：不做「段尾毛刺裁剪」——那个会误伤以短字收尾的正常句（把结尾字裁掉）；VoxCPM 的段尾毛刺应在**训练数据端根治**（见 voice-lab `prepare_dataset` 裁 clip 尾），而非推理时补。

```bash
SK=~/.claude/skills/voxcpm/scripts/voxcpm_gen.py   # 或 skill 真身 .../media/audio/voxcpm/scripts/

# ① say —— 零样本，内置音色
python3 "$SK" say --text "大家好，欢迎收看本期视频。" --out out.wav --play

# ② design —— 文字描述造音色（无需参考音，最适合定一个频道音色后大量配音）
python3 "$SK" design --instruct "温柔甜美的年轻女性主播" \
  --text "今天我们聊聊苹果芯片上的本地语音合成。" --out out.wav

# ③ clone —— 参考音 + 逐字转写，复刻音色
python3 "$SK" clone --ref-audio voice.wav --ref-text "参考音频里说的原话" \
  --text "这句话会用参考音色说出来。" --out out.wav

# ③' clone（频道固定音色首选）—— 自动读 _channel/card.json 的 voice.profiles[default]
#     在频道目录内 / 设 $CHANNEK_CHANNEL 即可，连 --voice 都不用；多音色用 --voice-profile <key>。
#     LoRA 型 profile（engine=voxcpm2-mlx-lora）会**自动加载专属合并模型**（mlx_model）+
#     prompt_wav/prompt_text 提示条——出片管线（voicegen）走的就是这条，不必手传 --model
python3 "$SK" clone --text-file script.txt --out narration.wav

# ③'' clone --voice —— 显式指一份 voice.md（card.json 缺失时的兜底）
python3 "$SK" clone --voice path/to/voice.md --text-file script.txt --out narration.wav

# 长旁白：文本入文件，自动按句切分逐段生成再拼接
python3 "$SK" say --text-file script.txt --out narration.wav
```

`info` 子命令打印 venv / 模型路径 / 采样率 / engine（+ 解析到的频道音色 profile）。**音色解析优先级**：显式 `--ref-audio/--ref-text`（及显式 `--model`）> **频道 `_channel/card.json` 的 `voice.profiles[default]`**（经 `_shared/channek.py` 读取，`--voice-profile` 选 key）> `--voice` 指的 voice.md frontmatter。

**频道 profile 两型（`engine` 字段路由·`resolve_channel_ref`）**：

| 型 | engine | 字段 | 行为 |
|----|--------|------|------|
| **LoRA 型（生产推荐）** | `voxcpm2-mlx-lora` | `mlx_model` + 可选 `prompt_wav`/`prompt_text` | `--model` 自动取 `mlx_model`（voice-lab 训 LoRA→合并→转 MLX 的专属音色模型·音色烤进权重·稳定不抽卡）；提示条可选（提声纹相似度 0.866→0.889·`prompt_text` 为内联转写文本，也兼容文件路径）；无提示条也能出声（音色在权重）。`mlx_model` 目录缺失 / engine 未知 → 清晰报错 fail-fast，不静默降级到基座冒充频道音色 |
| 零样本型 | 缺省 / `voxcpm-mlx` | `ref_wav`/`ref_text`（文件路径） | 原行为·基座 + 参考音克隆·向后兼容。相对路径文件若还没就位（P3 物理迁移前）自动回落 voice.md 解析出的旧路径——零回归 |

⚠ 音色字段可指向**频道外绝对路径**（如 voice-lab 工作台）= 外部依赖：风格卡打包分发时音色不自包含。

## 关键参数

| 参数 | 默认 | 说明 |
|------|------|------|
| `--timesteps` | 10 | CFM 扩散步数。**越低越快**；7 是速度/质量平衡点；要更快可降到 5 |
| `--cfg` | 2.0 | 无分类器引导强度，越高越贴指令、可能越僵 |
| `--model` | 频道 LoRA 型 profile 的 `mlx_model` → 否则 `mlx-community/VoxCPM2-8bit` | 可显式传 repo id 或本地目录覆盖；基座可换 `-4bit`（更小更快）/ `-bf16`（更高质量） |
| `--max-chars` | 120 | 长文本分句打包的单段上限 |
| `--no-chunk` | 关 | 短文本不切分 |
| `--no-denoise` | 关 | 关闭逐段去噪（默认开，见下「去噪是固定步」）|
| `--play` | 关 | 生成后 `afplay` 试听 |

## 去噪是固定步（raw 层稳定铁律）

**每段生成后都过一遍 RNNoise 去噪，默认开，不是可选项。** VoxCPM2 的 CFM 扩散逐段随机，克隆 v2 参考音（本身底噪 ≈ -64dB）时会逐幕飘——同一参考音、同一参数，有的段干净（-99dB）、有的段带底噪（-54/-60dB）。去噪不做就翻车。

- **怎么修的**：`synthesize()` 里每段生成后立刻调 `denoise_segment()`，经 ffmpeg `highpass=f=50,arnndn=m=assets/rnnoise/sh.rnnn`（RNNoise speech 专用模型）压底噪，再拼接。highpass 砍次声轰鸣，arnndn 做 VAD 门控去噪。
- **验收标准**：每段 **raw 底噪 ≤ -80dB**（实测多到 -inf）。校验：`ffmpeg -i seg.wav -af astats=metadata=1 -f null - 2>&1 | grep "Noise floor dB"`。
- **不伤音色**：RMS 与 4kHz+ 高频能量去噪前后差 < 0.05dB（实测），不闷、不截语音、时长不变。
- **逃生口**：`--no-denoise` 关掉（会退回逐幕不稳的 raw 行为，仅调试用）。ffmpeg 缺失或去噪失败时自动原样返回，不阻断出片。

## 速度与选型（重要）

- **say / design 是快路**（RTF ≈ 0.4~0.5）：5 分钟旁白约 2~3 分钟出。**做自媒体批量配音优先用 design 定个音色 + 长文本切分。**
- **零样本 clone 偏慢**（RTF ≈ 3）：每次都要编码参考音；只在必须复刻特定嗓音时用，长稿会成倍变慢。**频道 LoRA 型 profile 的 clone 不受此累**（音色在权重·提示条编码开销小·RTF ≈ 0.5-0.9，生产出片走这条）。
- 想要中文方言（粤语 / 四川话 / 东北话等）或调情感语速：写进 `--instruct` 描述里（design 模式）。

## 模型管理（别乱放）

- 模型 `mlx-community/VoxCPM2-8bit`（3.0GB）走**魔搭 ModelScope**下载，落标准缓存 `~/.cache/modelscope`——脚本里固定用 `snapshot_download`，幂等、按 repo id 引用，不硬编码路径。换模型只改 `--model`。
- 推理环境是专用 venv `~/.venvs/mlx-audio`（装了 `mlx-audio` + `modelscope`），不污染日常 `current`。
- 下载渠道为什么不走 HF：本机 huggingface.co 不可达、hf-mirror 对该 repo 会 308 跳回被墙 origin。完整规约见 `~/.claude/rules/model-download.md`。

## 兜底：高质量 PyTorch 路线

需要更高保真、或 MLX 版异常时，可退回原版 VoxCPM2（PyTorch）在 `$VOXCPM_HOME`（默认 `~/Coding/Hub/VoxCPM`，模型在其 `pretrained_models/VoxCPM2`，4.6GB）。**但慢得多**（MPS RTF ≈ 11，降噪器还卡 CPU），仅作高质量兜底，不做日常批量。

## 排错

- `ModuleNotFoundError: mlx_audio`：说明没跑在专用 venv 里。脚本靠 `sys.prefix` 判重定向；若你手动指定了别的 venv，直接用 `~/.venvs/mlx-audio/bin/python` 调。
- **不要用 `voxcpm` 这个命令本身**（原项目的 shim 会用 `pkg_resources.requires` 误报 torchcodec 缺失而秒退）——本 skill 完全绕开它，直接调 mlx-audio。
- 下载卡住 / 报 “not on huggingface.co”：确认走的是魔搭而非 HF（脚本已设 `HF_HUB_OFFLINE=1`）。

更多：音色描述写法、方言、长稿编排见 `reference/voice-design.md`。
