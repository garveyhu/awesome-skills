---
name: sound-gen
description: >-
  本地生成背景音乐(BGM) + 音效(SFX)——一句文字描述直接合成，离线、免费、可商用。当用户/agent 要「配 BGM / 背景音乐 / 配乐 / 底床 / 氛围乐 / 生成音效 / whoosh / ping / 转场音 / 出场音 / 打击音 / sonic logo / text-to-music / text-to-sfx / background music / sound effect / generate BGM」，且未指定其他音频后端时使用。两个子命令：music(文生纯器乐·ACE-Step 1.5·MIT·Apple MLX·48kHz·最长10min·M3 约与实时同速) / sfx(文生短音效·Stable Audio Open Small·Stability 社区许可·≤11s·8步蒸馏·每个<1s 极快)。是媒体生态 media/audio 层继 voxcpm(人声 TTS)之后的第二条音频后端——**voxcpm 管人声、sound-gen 管音乐+音效**。产物喂进 video-polish(音效落点/BGM ducking) 与 produce-pipeline 的音频设计层。区别 stock-sourcing(下现成 CC0)：本 skill 是「生成」不是「下载」，防同质化、要什么造什么。
---

# sound-gen —— 本地生成 BGM(音乐) + 音效(SFX)

给 Claude 补「声音生成自由」：在这台 Mac 上离线、免费、可商用地用文字造背景音乐和音效。和出图(comfyui/jimeng)、配音(voxcpm) 三足，补齐音频的「生成」这条路。

> **角色边界（重要·仿 voxcpm↔voice-lab 分工）**：本 skill = **BGM/SFX 生成运行时**（薄编排层）。重后端——两个开源项目的 clone / venv / 模型（共 ~12GB）——装在 **voice-lab 声音工作台**（`~/Coding/Archer/voice-lab/sound-gen/`），**不进 skill body**（跟 voxcpm 的模型不进 skill 同理）。本 skill 的脚本只 subprocess 调它们各自的 venv。首次用先按 [`reference/setup.md`](reference/setup.md) 装好后端（含全部踩坑）。后端目录可用 `SOUNDGEN_ACESTEP_DIR` / `SOUNDGEN_SAO_DIR` 覆盖。

## 两个能力

| 子命令 | 干什么 | 后端 | 授权 | 速度(M3) | 时长 |
|--------|--------|------|------|----------|------|
| **music** | 文字→纯器乐 BGM | ACE-Step 1.5（MLX 原生） | MIT · 可商用 | ~25s 音乐 20s 出 | 5–600s |
| **sfx** | 文字→短音效 | Stable Audio Open Small（MPS） | Stability 社区许可(年营收<$1M 免费商用·产出归你) | 每个 <1s | ≤11s |

两者都**离线、零 API 成本、训练数据出处干净可商用**。

## 用法

```bash
PY=~/.venvs/current/bin/python                        # 编排层用任意 python
SK=~/.claude/skills/sound-gen/scripts/soundgen.py      # 或真身 .../media/audio/sound-gen/scripts/soundgen.py

# ① BGM 底床（英文描述效果最好·贴频道气质·务必 no vocals）
$PY "$SK" music --caption "warm bright minimal electronic underscore, gentle plucked synth, soft airy pads, subtle steady pulse, optimistic yet restrained, no vocals" --duration 25 --out bgm.wav

# ② 音效（whoosh/ping/impact/riser/sonic logo…）
$PY "$SK" sfx --prompt "clean fast whoosh transition swoosh, airy movement, no music" --duration 2 --out whoosh.wav
$PY "$SK" sfx --prompt "soft UI notification ping, single bright bell blip" --duration 1.5 --out ping.wav

# ③ 批量（一份混合 manifest·各后端模型只加载一次·避免逐条重复加载/卸载·音效尤其明显）
$PY "$SK" batch --manifest items.json
#   items.json = [{"type":"music","caption":"...","duration":20,"seed":1,"out":"bgm.wav"},
#                 {"type":"sfx","prompt":"whoosh transition","duration":2,"out":"whoosh.wav"}, ...]

# ④ 看后端就绪状态
$PY "$SK" info
```

- `--out` 省略则落临时文件，**最后一行 stdout 打印 wav 绝对路径**（编排/管线取它）。
- `--seed <n>` 固定复现；缺省随机。
- 后端 subprocess 的进度/日志直通终端（不吞），失败时 stdout 上方就是后端报错。

### 写好 caption / prompt（决定成败）
- **BGM**：给「气质 + 乐器 + 情绪 + 律动 + no vocals」，别写歌名/艺人。贴频道脸——明亮活力用 `warm/bright/upbeat minimal electronic`、暗场用 `dark ambient/cinematic`。基调参考 video-polish 的「选曲基调」（无人声·不抢解说·有专业骨）。
- **SFX**：给「动作 + 质感 + no music」，短促具体——`whoosh transition` / `UI notification ping` / `deep impact boom` / `riser build up` / `sparkle chime`。

## 与生态协作（在管线哪一环）

- **喂 [`video-polish`](../../video/edit/video-polish/SKILL.md)**：它管「音效落点 + BGM ducking + mux」，本 skill 管「生成那些音效/BGM 素材」。以前 video-polish 靠 `gen_placeholder.sh` 程序化合成(震荡器·土)或 stock 下载；现在 BGM/SFX 可**按内容生成**。video-polish 的 sonic logo / whoosh / ping / sting / riser 落点素材，都可由本 skill 产。
- **喂 produce-pipeline 音频设计层**：每条片按内容生成专属 BGM 底床 + 关键节点音效，不再撞同几首 CC0。
- **和 [`voxcpm`](../voxcpm/SKILL.md) 分工**：voxcpm=人声旁白(TTS)，sound-gen=音乐+音效。一条片的声音 = voxcpm 旁白 + sound-gen 底床/音效（+ video-polish 混音）。
- **和 [`stock-sourcing`](../stock-sourcing/SKILL.md) 分工**：stock=下现成 CC0（要「真」实录），sound-gen=生成（防同质化·要什么造什么）。默认生成，要真实录音质感才走 stock。

## 完成度（诚实标）

- ✅ **两条链在 M3 上真跑验证过**：music 出 25s 纯器乐(48kHz·总 20.8s)；sfx 出 whoosh/ping/impact(每个 <1s)。见 setup.md「实测」。
- ✅ **batch 批量模式（已实现·真跑验证）**：`batch --manifest` 按 type 分 music/sfx，**各后端模型只加载一次**再循环出多条，省逐条重复加载/卸载——音效尤其明显（10 条批量 ~20s vs 逐条 ~110s）。music 批量走 `_music_backend.py`（DiT+LM 载一次·**LM 保时长填满**，LM 初始化失败自动退化纯 DiT）、sfx 批量走 `_sfx_backend.py --manifest`。单条 `music`/`sfx` 仍走各自单发路径（music 单条=cli.py·LM 版）。实测 2 BGM+3 SFX 一把出、BGM 精确填满 15s。
- 🟡 **单发 subprocess 每次加载模型**（和 voxcpm 的 MLX 路径同款·music 单条 ~20–40s、sfx 单条 ~10s）——要连出多条走 `batch` 省加载。
- 🟡 **video-to-audio(喂画面生成配乐)不做**：最好的 MMAudio/AudioX 全非商用、且我们画面是抽象图解拟音价值低。走 text-to-music/sfx 更可控可商用（选型详见项目记忆 audio-gen-stack-selection）。
- ⚠ 后端不在 skill body——换机器/重装照 [`reference/setup.md`](reference/setup.md) 备齐 ~12GB 后端再用。

深档：后端安装 + 全部踩坑见 [`reference/setup.md`](reference/setup.md)。
