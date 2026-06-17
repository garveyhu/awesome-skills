---
name: voxcpm
description: >-
  本地文字转语音 / 配音（VoxCPM2 跑在 Apple MLX 上，离线、可商用 Apache-2.0）。当用户要「配音 / 语音合成 / 文字转语音 / 给视频配旁白 / 念稿 / 做音频 / 声音克隆 / 造一个音色 / text-to-speech / TTS / voice over / narrate」，且未指定其他音频后端时使用。三模式：say 零样本内置音色、design 用文字描述造音色、clone 用参考音克隆音色；支持 30 语言 + 中文多方言、48kHz、长文本按句切分拼接，适合 5 分钟级旁白。是媒体生态里继出图(comfyui/codex/gemini)之后的第一条音频后端。
---

# voxcpm —— 本地配音 / TTS（VoxCPM2 on Apple MLX）

给 Claude 补「音频自由」：在这台 Mac 上离线把文字合成成 48kHz 录音棚级语音，速度快过实时（M3 实测 RTF ≈ 0.4~0.6），能力对标出图生态——文字描述造音色、参考音克隆、长旁白一把出。

## 一条命令的三模式

入口 `scripts/voxcpm_gen.py`，**任意 python 调用即可**（脚本会自动重定向到专用 venv `~/.venvs/mlx-audio`，并把模型经魔搭解析好）。stdout 只吐产物 wav 路径，进度走 stderr。

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

# 长旁白：文本入文件，自动按句切分逐段生成再拼接
python3 "$SK" say --text-file script.txt --out narration.wav
```

`info` 子命令打印 venv / 模型路径 / 采样率。

## 关键参数

| 参数 | 默认 | 说明 |
|------|------|------|
| `--timesteps` | 10 | CFM 扩散步数。**越低越快**；7 是速度/质量平衡点；要更快可降到 5 |
| `--cfg` | 2.0 | 无分类器引导强度，越高越贴指令、可能越僵 |
| `--model` | `mlx-community/VoxCPM2-8bit` | 可换 `-4bit`（更小更快）/ `-bf16`（更高质量） |
| `--max-chars` | 120 | 长文本分句打包的单段上限 |
| `--no-chunk` | 关 | 短文本不切分 |
| `--play` | 关 | 生成后 `afplay` 试听 |

## 速度与选型（重要）

- **say / design 是快路**（RTF ≈ 0.4~0.5）：5 分钟旁白约 2~3 分钟出。**做自媒体批量配音优先用 design 定个音色 + 长文本切分。**
- **clone 偏慢**（RTF ≈ 3）：每次都要编码参考音；只在必须复刻特定嗓音时用，长稿会成倍变慢。
- 想要中文方言（粤语 / 四川话 / 东北话等）或调情感语速：写进 `--instruct` 描述里（design 模式）。

## 模型管理（别乱放）

- 模型 `mlx-community/VoxCPM2-8bit`（3.0GB）走**魔搭 ModelScope**下载，落标准缓存 `~/.cache/modelscope`——脚本里固定用 `snapshot_download`，幂等、按 repo id 引用，不硬编码路径。换模型只改 `--model`。
- 推理环境是专用 venv `~/.venvs/mlx-audio`（装了 `mlx-audio` + `modelscope`），不污染日常 `current`。
- 下载渠道为什么不走 HF：本机 huggingface.co 不可达、hf-mirror 对该 repo 会 308 跳回被墙 origin。完整规约见 `~/.claude/rules/model-download.md`。

## 兜底：高质量 PyTorch 路线

需要更高保真、或 MLX 版异常时，可退回原版 VoxCPM2（PyTorch）在 `/Users/links/Coding/Hub/VoxCPM`（模型已在 `pretrained_models/VoxCPM2`，4.6GB）。**但慢得多**（MPS RTF ≈ 11，降噪器还卡 CPU），仅作高质量兜底，不做日常批量。

## 排错

- `ModuleNotFoundError: mlx_audio`：说明没跑在专用 venv 里。脚本靠 `sys.prefix` 判重定向；若你手动指定了别的 venv，直接用 `~/.venvs/mlx-audio/bin/python` 调。
- **不要用 `voxcpm` 这个命令本身**（原项目的 shim 会用 `pkg_resources.requires` 误报 torchcodec 缺失而秒退）——本 skill 完全绕开它，直接调 mlx-audio。
- 下载卡住 / 报 “not on huggingface.co”：确认走的是魔搭而非 HF（脚本已设 `HF_HUB_OFFLINE=1`）。

更多：音色描述写法、方言、长稿编排见 `reference/voice-design.md`。
