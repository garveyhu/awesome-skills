# ComfyUI 工作流格式 & 如何手写/改写

## 两种 JSON 格式（别搞混）

| 格式 | 长什么样 | 用途 | 谁用 |
|------|---------|------|------|
| **UI / Litegraph 格式** | 有 `nodes`/`links`/坐标/`widgets_values`，可能含 `subgraphs` | 在网页编辑器里保存/导入 | 人在画布上用 |
| **API / prompt 格式** | 扁平 dict：`{"节点id": {"class_type":..., "inputs":{...}}}` | POST 到 `/prompt` 直接执行 | **本 skill 全程用这个** |

官方模板（`comfyui-workflow-templates*`）都是 **UI 格式**，要自动化必须转成 **API 格式**。

## API 格式规则

```jsonc
{
  "1": {                                  // 节点 id（字符串，任意唯一）
    "class_type": "UNETLoader",           // 节点类型，必须与 /object_info 的键一致
    "inputs": {
      "unet_name": "z_image_turbo_bf16.safetensors",  // 常量：直接写值
      "weight_dtype": "default"
    }
  },
  "8": {
    "class_type": "KSampler",
    "inputs": {
      "model": ["4", 0],                  // 连线：[来源节点id, 输出槽序号(从0)]
      "positive": ["5", 0],
      "latent_image": ["7", 0],
      "seed": 42, "steps": 8, "cfg": 1.0,
      "sampler_name": "res_multistep", "scheduler": "simple", "denoise": 1.0
    }
  }
}
```

要点：
- `inputs` 里每个键要么是**常量值**，要么是 `["源节点id", 槽序号]` 的连线。
- 槽序号看 `/object_info/<节点>` 的 `output_name` 顺序（如 `CheckpointLoaderSimple` 输出 `[MODEL, CLIP, VAE]` → MODEL=0, CLIP=1, VAE=2）。
- 必须有一个保存节点（`SaveImage`/`SaveVideo`），否则没有产物可下载。
- 提交时脚本会包成 `{"prompt": 工作流, "client_id": ...}`；`raw` 命令也能直接吃已包好的导出（会自动解包）。

## ComfyUI REST 端点速查（本 skill 用到/可用）

| 端点 | 方法 | 用途 |
|------|------|------|
| `/system_stats` | GET | 设备(Mac 上是 mps)、内存、版本 |
| `/object_info[/{node}]` | GET | 节点 schema（校验工作流的权威来源） |
| `/models/{type}` | GET | 列某类已装模型（checkpoints/loras/vae/diffusion_models/clip…） |
| `/prompt` | POST | 提交工作流 `{"prompt":{...},"client_id":...}`，返回 `prompt_id` + `node_errors` |
| `/history/{id}` | GET | 运行中为空 `{}`，完成后有 `outputs` + `status.completed` |
| `/queue` | GET | 队列积压(`queue_running`/`queue_pending`) |
| `/view?filename=&subfolder=&type=output` | GET | 下载产物 |
| `/upload/image`、`/upload/mask` | POST(multipart) | 上传输入图/遮罩（i2v、inpaint 用） |
| `/interrupt` | POST | 中断当前任务 |
| `/free` | POST | `{"unload_models":true,"free_memory":true}` 释放内存（Mac OOM 缓解） |

> 还有 `ws://127.0.0.1:8188/ws` 推 `progress`/`executed` 事件可做实时进度条，但需 WS 库；本 skill 为纯标准库，默认用 `/history` 轮询。
>
> **提交后必查 `node_errors`**：非空表示工作流在执行前就被校验拒绝（多为模型名拼错/缺输入）。`comfy_api.py` 的 `queue_prompt` 已自动检查并抛错。

## UI 格式 → API 格式 转换 5 条规则（手动改写官方模板时用）

`scripts/build/ui2api.py` 已自动化以下逻辑，手写时也照此：

1. **顶层**：UI 有 `nodes[]/links[]/version`；API 是扁平 `{"id字符串":{"class_type","inputs"}}`。
2. **链接**：UI 的 `links` 每项 `[link_id, src_node, src_slot, dst_node, dst_slot, type]` → 目标节点 `inputs["输入名"]=[src_node, src_slot]`。
3. **widget 值**：UI 把"连接输入"和"widget 输入"混在同一 `inputs[]` 数组，widget 项带 `"widget":{"name":..}`；`widgets_values[]` 按 widget 项出现顺序排列，回填到对应输入名。
4. **⚠️ 幽灵 widget `control_after_generate`**：凡带 seed 的节点(KSampler/RandomNoise)，UI 在 seed 后**自动插一个** `control_after_generate`（值如 `"randomize"`），占一个 `widgets_values` 槽。**API 没有这个字段，必须丢弃**——这是 UI↔API 转换最大的坑。
5. **被"转为输入"的 widget**：若某 widget 项的 `link` 非空（被拖成了连线），走链接分支，且**不消耗** `widgets_values` 槽。

**slot 序号**（API 链接 `[id, slot]` 的 slot = 源节点输出下标）：
```
CheckpointLoaderSimple: 0=MODEL 1=CLIP 2=VAE   LoraLoader: 0=MODEL 1=CLIP
UNETLoader:0=MODEL  CLIPLoader/Dual/Triple:0=CLIP  VAELoader:0=VAE
CLIPTextEncode:0=COND  Empty*Latent*:0=LATENT  KSampler:0=LATENT  VAEDecode:0=IMAGE
LoadImage:0=IMAGE 1=MASK  CLIPVisionEncode:0=CLIP_VISION_OUTPUT
WanImageToVideo: 0=positive 1=negative 2=LATENT   ← 多输出节点，接错 slot 是常见 bug
```

局限：`ui2api.py` 不展开 subgraph，不解析 Primitive/Reroute（新式官方模板常用）。遇到会明确报错——这类改用扁平模板或内置构建器。

## 怎么查一个节点的真实输入

```bash
curl -s http://127.0.0.1:8188/object_info/KSampler | python -m json.tool
```

或用本 skill 采集时的小脚本思路：读 `input.required` / `input.optional`，每个值 `[类型, {默认值...}]`；类型是 list 表示枚举（如模型名、sampler 名）。**写工作流前务必核对输入名拼写**，错一个就会被 `/prompt` 以 400 拒绝（错误体会说明缺哪个）。

## 官方模板蓝本路径（本机自带，443+ 个，覆盖几乎所有架构）

```
ComfyUI/.venv/lib/python3.12/site-packages/
├── comfyui_workflow_templates_media_image/templates/   # 图像（含 z_image*, flux*, sdxl* …）
├── comfyui_workflow_templates_media_video/templates/   # 视频（wan2_2*, hunyuan*, ltxv*, mochi* …）
├── comfyui_workflow_templates_media_audio/             # 音频
└── comfyui_workflow_templates_media_other/
```

用法：找到对应架构的 `*.json`（UI 格式）→ 解析它的 `nodes`（含 `subgraphs.nodes`）拿到节点类型与 `widgets_values` → 对照 `/object_info` 把 widgets 映射成 `inputs` 的常量、把 links 映射成 `[id, slot]` → 得到 API 格式 → `raw` 提交。

> 新模板常把核心包进 `subgraph`（节点 type 是一串 UUID）。真实节点在该 JSON 的 `definitions.subgraphs[].nodes` 里，要展开后再转换。本 skill 的内置 Wan/Z-Image 构建器就是这么从子图里还原出来的。

## 改写时的常见坑

- **UI 的 widgets_values 是按 UI 顺序的数组**，要对照 `/object_info` 的 `input_order` 才能知道每个值对应哪个输入名。
- 模型文件名必须是 `/object_info` 枚举里**真实存在**的，否则报错——所以永远先 `discover`。
- 视频保存节点输出键不一定叫 `images`（可能 `gifs`/`videos`），本 skill 的 `collect_outputs` 已做通用遍历，手写 raw 也无需操心下载。
