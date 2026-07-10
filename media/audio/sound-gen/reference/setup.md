# sound-gen 后端安装指南（含全部踩坑）

sound-gen 是薄编排层，真正生成靠两个开源项目，各自独立 venv + 模型（共 ~12GB），装在
**voice-lab 声音工作台** `~/Coding/Archer/voice-lab/sound-gen/`（不进 skill body）。
换机器 / 重装照本文备齐；后端目录可用 `SOUNDGEN_ACESTEP_DIR` / `SOUNDGEN_SAO_DIR` 覆盖默认。

机器要求：Apple Silicon Mac（M 系 · MPS/MLX），≥16GB 内存（实测 36GB 从容）。所有模型走**魔搭**下载（HF 被墙）。

---

## A. music 后端 —— ACE-Step 1.5（文生音乐 · MIT · MLX）

```bash
cd ~/Coding/Archer/voice-lab/sound-gen
GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/ace-step/ACE-Step-1.5
cd ACE-Step-1.5

# ① 装依赖 —— ⚠ 别用 `uv sync`（见坑1），用 uv pip install -e .（仅当前平台解析·清华源）
uv venv --python 3.12 .venv
VIRTUAL_ENV="$PWD/.venv" UV_DEFAULT_INDEX=https://pypi.tuna.tsinghua.edu.cn/simple uv pip install -e .

# ② 配 .env（0.6B LM 防 OOM · 魔搭源 · MLX 后端）
cat > .env <<'ENV'
ACESTEP_CONFIG_PATH=acestep-v15-turbo
ACESTEP_LM_MODEL_PATH=acestep-5Hz-lm-0.6B
ACESTEP_DEVICE=auto
ACESTEP_LM_BACKEND=mlx
ACESTEP_DOWNLOAD_SOURCE=modelscope
ENV

# ③ 下模型（魔搭 · 4 组件都要下齐否则完整性检查触发重下·见坑3）
#    turbo(4.8G) + Qwen3-Embedding(1.2G) + vae(0.34G) + 1.7B LM(3.76G) = ~10G
~/.venvs/current/bin/python - <<'PY'
from modelscope import snapshot_download
snapshot_download('ACE-Step/Ace-Step1.5', local_dir='checkpoints',
    allow_patterns=['acestep-v15-turbo/*','Qwen3-Embedding-0.6B/*','vae/*',
                    'acestep-5Hz-lm-1.7B/*','config.json','configuration.json'])
print('DONE')
PY
```

## B. sfx 后端 —— Stable Audio Open Small（文生音效 · 社区许可 · MPS）

```bash
cd ~/Coding/Archer/voice-lab/sound-gen
GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/Stability-AI/stable-audio-tools
cd stable-audio-tools

# ① 装依赖（Python 3.10·requires-python <3.11）+ 修两个坑（见坑5、6）
uv venv --python 3.10 .venv
VIRTUAL_ENV="$PWD/.venv" UV_DEFAULT_INDEX=https://pypi.tuna.tsinghua.edu.cn/simple uv pip install -e .
VIRTUAL_ENV="$PWD/.venv" UV_DEFAULT_INDEX=https://pypi.tuna.tsinghua.edu.cn/simple uv pip install "numpy<2" "pytorch_lightning==2.5.5" soundfile

# ② 下模型（魔搭·只需 model.safetensors + config·1.7G·仓库那 5G 是 3 份重复权重）
~/.venvs/current/bin/python - <<'PY'
from modelscope import snapshot_download
snapshot_download('stabilityai/stable-audio-open-small',
    local_dir='models/stable-audio-open-small',
    allow_patterns=['model.safetensors','model_config.json','LICENSE','README.md','configuration.json'])
print('DONE')
PY
```

装完 `python <skill>/scripts/soundgen.py info` 应四项全 OK。

---

## 踩过的坑（全是这次装踩出来的·别重踩）

1. **`uv sync` 卡死**：ACE-Step 的 pyproject 有 `required-environments`(win/linux/mac 全平台) + 显式 CUDA 索引，`uv sync` 做通用解析要拉 `download.pytorch.org` 元数据（国内卡死·进程 0%CPU 干等）。**改 `uv pip install -e .`——只按当前平台解析，绕开 CUDA 索引**，mac torch 走清华源。

2. **modelscope 多线程下载器偶发卡死**（连接挂住·零字节写入·非网络问题·同期别的下载能成）。**用看门狗 bash 兜**：监控 `du` 字节增长，停滞 ~75s 就 kill 重启（modelscope 断点续传·实测重启从断点续、非从 0）：
   ```bash
   is_done(){ [ "$(stat -f%z checkpoints/acestep-v15-turbo/model.safetensors 2>/dev/null||echo 0)" -gt 4500000000 ]; }
   while ! is_done; do
     python ms_dl.py & PID=$!; last=0;st=0
     while kill -0 $PID 2>/dev/null; do sleep 15; cur=$(du -sk checkpoints|cut -f1)
       [ "$cur" -le "$last" ] && st=$((st+15)) || st=0; last=$cur
       [ $st -ge 75 ] && { kill $PID; pkill -9 -f ms_dl.py; break; }; done; done
   ```

3. **ACE-Step 模型完整性检查硬要 4 组件全有权重**：`MAIN_MODEL_COMPONENTS` = turbo + vae + Qwen3-Embedding-0.6B + **acestep-5Hz-lm-1.7B**。缺任一（哪怕 `thinking=false` 不加载 LM）→ handler 初始化触发**全量重下**。所以 1.7B LM(3.76G) 也得下齐（虽然 sound-gen 用 thinking=false 不真加载它）。

4. **`_can_access_google()` 决定下载源**：连 google:443 通→选 HF（被墙·卡死），不通→魔搭。**这台机器 google 竟连得上→自动走 HF**。且 cli.py 的 ensure_main_model **不读** `ACESTEP_DOWNLOAD_SOURCE` 环境变量。**解法：预先把 4 组件从魔搭下齐 → 完整性检查过 → 根本不触发自动下载**（绕开源探测）。

5. **numpy ABI 冲突**（stable-audio）：`PyWavelets==1.4.1`(pyproject 钉死) 对 numpy1.x 编译，装的却是 numpy2.x → `ValueError: numpy.dtype size changed 96→88`。**装 `numpy<2`(1.26.4)**。

6. **推理路径 import 训练依赖 + 无存盘后端**（stable-audio）：`lora/callbacks.py` import `pytorch_lightning`（在 train extra 里·base 装缺它）→ 补 `pytorch_lightning==2.5.5`；`torchaudio 2.7.1` 无 I/O 后端，`torchaudio.save` 报 "Couldn't find appropriate backend" → 用 `soundfile.write`（`_sfx_backend.py` 已用）。

7. **MPS 用 float32**（stable-audio）：decoder 的 conv1d 在 fp16 下会卡死（`_sfx_backend.py` 已 `.float()`）。生成内部 autocast 报 "device_type cuda" 警告无害。small 版是 rf_denoiser 蒸馏模型 → 用 `sampler_type="pingpong"` + `steps=8` + `cfg_scale=1.0`。

---

## 实测（2026-07-10 · M3 · 36GB）

- **music**：caption→25s 纯器乐，total 20.8s（DiT 8步 7.4s + VAE 7.7s + LM 元数据相 ~4s），48kHz 立体声，真音乐结构（全频段+律动+谐波）。
- **sfx**：whoosh/ping/impact，每个 0.6–1.0s 生成（模型加载另计 ~10s），44.1kHz，真音效（whoosh 是标准扫频涌起-衰落形）。
- 选型依据（为什么这两个·别的为什么否）见 Claude 项目记忆 `audio-gen-stack-selection`：AudioX-Turbo 否(NC+水印+无MPS)、MusicGen/MMAudio/TangoFlux 权重非商用、video-to-audio 暂不做。
