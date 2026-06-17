# 排错库

✅ = Mac/Apple Silicon 上也会遇到。排查第一步永远是看 `comfyui.log`（`tail -f`）。

| 现象 / 报错 | 原因 | 解决 | Mac? |
|------------|------|------|------|
| 连不上服务 | 没启动/端口/防火墙 | `curl /system_stats` 验活；确认 8188；`./run.sh` | ✅ |
| Out of memory / 卡死 | 超出统一内存 | 降分辨率(1024→768, 720p→480p)；batch=1；fp8；tiled VAE 解码节点；`comfy.py free` 清内存；重启清碎片 | ✅（MPS 吃系统内存） |
| `Node type not found: X` | 缺自定义节点 | 用下表 node→package 装包后重启 | ✅ |
| `Required input 'x' not provided` | 有输入没接线 | 检查所有 required 输入都连上 | ✅ |
| `'NoneType' object has no attribute…` | 模型静默加载失败 | 查路径/文件名是否精确；重下(可能损坏)；查内存 | ✅ |
| `SafetensorError: file does not contain key` | 文件对、**加载器用错** | 按模型类型选对 loader（Checkpoint vs UNETLoader vs LoRA vs ControlNet） | ✅ |
| `value_not_in_list: ... not in [...]` | 工作流里模型名在库存里不存在 | 先 `discover` 核对真实文件名，精确到大小写后缀 | ✅ |
| 恰好 1024×1024 出水印状伪影 | 已知 SDXL 怪癖 | 改 **1016×1016 / 1020×1020** | ✅ |
| 队列卡死不动 | 任务挂起 | `comfy.py free`（含 interrupt 思路）；或重启 | ✅ |
| 视频闪烁/抖动 | 缺时间一致性 | FaceDetailer denoise ≤0.3；RIFE 补帧；deflicker；AnimateDiff context overlap ≥4 | ✅ |
| Wan i2v 忽略输入图 | CLIP-vision / VAE 配错 | 用对的 `clip_vision_h` + `wan_2.1_vae` | ✅ |
| `expected scalar type BFloat16` | 精度不一致 | 让链路精度一致(fp16/fp32)；Mac 上注意 fp8 节点兼容性 | ✅ |
| 首次某模型特别慢 | 模型首次载入内存 | 正常，后续会快；别误判为卡死 | ✅ |

## 节点类 → 自定义节点包 速查（解 "Node type not found"）

| 节点类 | 安装包 |
|--------|--------|
| `ApplyInstantID` | ComfyUI_InstantID |
| `IPAdapterUnifiedLoader` | ComfyUI_IPAdapter_plus |
| `FaceDetailer` | ComfyUI-Impact-Pack |
| `ReactorFaceSwap` | ComfyUI-ReActor |
| `AnimateDiffLoaderWithContext` | AnimateDiff-Evolved |
| `VHS_*`（VideoCombine 等） | VideoHelperSuite |
| `ControlNetApply*` / 预处理器 | comfyui_controlnet_aux |
| `UltimateSDUpscale` | ComfyUI_UltimateSDUpscale |
| `RIFE*` | ComfyUI-Frame-Interpolation |

装法：ComfyUI-Manager 里搜包名安装，或 `git clone` 到 `custom_nodes/` 后重启。

## OOM 处理阶梯（Mac 统一内存）

降分辨率 → batch=1 → 切 fp8 模型 → 用 tiled VAE 解码节点 → `comfy.py free`（任务间）→ 重启 ComfyUI 清碎片 → 启动加 `--lowvram`/`--cpu-vae`（透传给 run.sh）。
