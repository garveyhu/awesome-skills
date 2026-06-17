# macOS / Apple Silicon 注意事项

本机：macOS (darwin)，Apple Silicon，统一内存（实测 ~36GB 可用给 ComfyUI 报告）。ComfyUI 走 **MPS** 后端，不是 CUDA。

## 性能预期（重要：先给用户打预防针）

- MPS 比同级 NVIDIA 显卡**慢很多**，且没有 xformers / flash-attn 加速。
- 实测 Z-Image Turbo 1024×1024 / 8 步：**首次 ~270–280s**（含把模型从磁盘加载进内存），同一模型第二次起会快（模型驻留）。
- Wan 2.2 14B fp8 视频：官方模板标注在 RTX4090 + 4步LoRA 约 71–97s；**Mac 上会成倍慢**，可能数分钟到十几分钟。先用小分辨率（如 480×480）、少帧（length 33/49）试水，再放大。
- 调用脚本时 timeout 给足：t2i 默认 600s，i2v/raw 默认 3600s，必要时 `--timeout` 调大。

## 内存而非显存

统一内存架构下没有独立显存。fp8 量化模型（如 wan fp8_scaled）能省内存。若 OOM/卡死：
- 降分辨率、降 batch、降视频帧数
- ComfyUI 启动可加 `--lowvram` / `--cpu-vae` 等参数（透传给 `./run.sh`，它原样传给 main.py）

## 启停（项目自带脚本）

ComfyUI 根目录 `/Users/links/Coding/Hub/ComfyUI`：

```bash
./run.sh            # 后台启动，监听 127.0.0.1:8188，日志 comfyui.log，pid 存 .comfyui.pid
./run.sh --port 8200    # 额外参数原样透传给 main.py
./stop.sh           # 停止
tail -f comfyui.log # 看实时日志（排查报错最有用）
```

它用项目内独立 `.venv`，不污染全局 Python。脚本调用建议用同一个解释器：`/Users/links/Coding/Hub/ComfyUI/.venv/bin/python`。

## 跑本 skill 脚本

脚本零三方依赖（纯标准库），任意 python3 都行。固定用法：

```bash
cd /Users/links/Coding/Hub/ComfyUI            # 任意目录都行，这里只是习惯
.venv/bin/python /Users/links/Coding/Hub/ComfyUI/skills/comfyui/scripts/comfy.py discover
```

环境变量：
- `COMFYUI_HOST`（默认 `http://127.0.0.1:8188`）——远程/换端口时改
- `COMFYUI_OUTPUT`（默认 `./comfy_outputs`）——产物本地下载目录

## 常见报错

| 现象 | 原因 / 处理 |
|------|------------|
| `连不上 ComfyUI` | 没启动 → `./run.sh`；或端口/host 不对 → 设 `COMFYUI_HOST` |
| `POST /prompt 被拒绝 (400)` | 工作流里模型名拼错或节点输入名错 → 先 `discover` 核对模型名，用 `/object_info` 核对输入名 |
| 生成很久不返回 | MPS 本来就慢；看 `comfyui.log` 是否在跑；调大 `--timeout` |
| 视频没产物 | 确认工作流有 `SaveVideo` 节点；`collect_outputs` 会遍历所有输出键，正常不会漏 |
| 第一次某模型特别慢 | 模型首次加载进内存的开销，属正常，后续会快 |
