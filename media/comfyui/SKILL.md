---
name: comfyui
description: >-
  Drive a local ComfyUI instance to generate images and videos from natural
  language — no manual node wiring. Discovers installed models dynamically and
  auto-builds runnable API-format workflows, then submits/polls/downloads the
  result. Use when the user wants to generate / produce an image or video
  locally, "用 ComfyUI 出图/出视频", text-to-image, image-to-video, run a
  ComfyUI workflow, 文生图, 图生视频, 本地生图, or batch-generate media. Model-
  agnostic (Z-Image, FLUX, SD/SDXL checkpoints, Wan 2.2 video, …); tuned for
  macOS / Apple Silicon (MPS).
---

# ComfyUI 本地生成 skill

驱动**本地 ComfyUI**(Mac/MPS):你说人话,skill 发现模型、跑工作流、取回成品,不用在画布连节点。从单张出图升级成**有注册表、可批量、可复刻、有出厂标准的本地 AIGC 美术生产线**。

## 功能总览

**① 四大生成**(CLI 直接调,跑的就是画布同一份 JSON):

| 命令 | 能力 | 默认工作流 |
|------|------|-----------|
| `t2i "提示词"` | 文生图 | Z-Image Turbo(8步快) |
| `i2i <图> "编辑指令"` | 图生图编辑(改背景/加物/换风格/换色) | Qwen-Image-Edit |
| `i2v <图> "运动描述"` | 图生视频 | Wan 2.2(Mac 慢) |
| `matte <图>` | 抠图(`--text` 文字选取) | RMBG-2.0 / SAM2 |

- **② 工作流管理**(单一真源 `workflows/` + `catalog.json`):`workflows` 列全部 · `install <名>` 按 catalog 从魔搭备齐模型+节点 · 新增网上工作流 = 丢 json + catalog 加一条 · **CLI 与画布同一份**。
- **③ 跑任意工作流**:`raw <json> [--var k=v]`(UI 自动转 API)· `convert` · `api2ui` · `templates`(library 20+ 架构模板)。
- **④ 后处理三段**:`--keyflat`/`--matte` 抠透明 → `--pixelize` 像素化+统一调色板。
- **⑤ 项目资产管线**:`init` 一条命令铺整套(assets 骨架+规约+装工作流+反向软链)· `batch.sh` 照 assets.json **零 LLM 无人值守批量出图**。
- **⑥ 抠图栈**:RMBG-2.0 / SAM2 文字 / 手绘选区三合一 · `setup/setup_matting.sh` 一键复刻。
- **⑦ 出厂标准**:任何画布工作流必走 `reference/workflow-style.md`(命名/分组/Note/布局)+ `groupify.py`。

## 核心理念
- **模型无关**:能干啥由"装了啥模型"动态决定(查 `/object_info`),不写死。
- **API 闭环**:`/prompt`→`/history`→`/view` 全自动,不用点网页。
- **Mac 优先**:纯标准库 CLI 引擎,Apple Silicon/MPS 实测通过。

## 美术资产生产方法论（本 skill 不只是出图，是整套可复刻的资产管线）

一条命令把整套铺进任意项目:`python scripts/comfy.py init <项目路径> --name <名>` → 复制模板(`scripts/comfyui/` 批量入口、`assets/` 结构与 `assets.json`、`docs/` 规约)+ 装 canonical 工作流到 ComfyUI 默认目录 + 建反向软链 + 打印模型清单。别人装完本 skill,一条 `init` 就复刻整套。

**两阶段分工(关键设计):**
- **① Claude 设计期(用 LLM,一次性)**:把项目的**提示词 / 资产结构 / 工作流 / `assets.json` 配置**做好——这步要判断和创意,是 Claude 的价值所在。
- **② 脚本执行期(纯机械,零 LLM)**:`bash scripts/comfyui/batch.sh` 照 `assets.json` 无人值守批量出图——**不调用 Claude、不耗 API、零边际成本**,用户在自己终端过夜跑。
> 即:Claude 把配置弄好是一次性投入;之后无限量出图是纯脚本、免费。**绝不要在 batch 链路里塞任何需要 LLM 的步骤。**

**约定(init 模板已固化;换项目/换风格只改内容、不动结构):**
- **反向软链**:`<ComfyUI>/output/projects/<名>` → 项目 `assets/`;`<ComfyUI>/user/default/workflows/projects/<名>` → 项目 `comfy-workflows/`(项目自有的专用工作流;通用工作流走 skill 的 `workflows/`)。产物与工作流直接进项目仓、随 git 共享。
- **结构**:`assets/<类>/`(每类一个文件夹;`README.md` 给人看 + `assets.json` 给脚本读)。
- **管线**:生成(`t2i` / `i2i` / 项目专用工作流 `raw`)→ `--keyflat` 或 `--matte` 抠透明 → `--pixelize` 统一像素+调色板,三段都在 CLI 里串。
- `assets.json` 格式见 `scripts/batch/README.md`。

## 前置条件

ComfyUI 必须在运行。脚本默认连 `http://127.0.0.1:8188`（可用环境变量 `COMFYUI_HOST` 改）。

- 启动：ComfyUI 根目录 `./run.sh`（项目：`/Users/links/Coding/Hub/ComfyUI`）
- 停止：`./stop.sh`
- 先确认活着：`python scripts/comfy.py discover` 连不上会直接提示去 run.sh

## 标准工作流程（Claude 照此执行）

### 1. 永远先 discover

任何生成请求前，先跑一次发现，拿到当前可用能力和模型清单：

```bash
python scripts/comfy.py discover
```

输出会列出 `capabilities`（如 `[t2i] zimage`、`[i2v] wan22`）和各类模型。**用这个结果决定走哪条路、用哪个模型**，不要假设。

### 2. 按意图选命令

> **架构(2026 重构):工作流 JSON 单一真源。** CLI 不再用代码 builder——`t2i/i2i/i2v` 跑的就是
> `workflows/<媒体>/<工作流>.json`(和用户在 ComfyUI 画布用的**同一份**),由 `workflows/catalog.json`
> 注册(每任务一个默认 + 需要的模型/节点)。新增网上工作流:json 丢进 `workflows/image|video/` + catalog 加一条
> → `comfy.py install <名>` 自动备齐模型与节点。`comfy.py workflows` 看全部。

| 用户意图 | 命令 |
|---------|------|
| 文生图 | `python scripts/comfy.py t2i "<提示词>" [--w 1024 --h 1024 --seed N] [--workflow 名]`(跑 catalog 默认 image_z_image_turbo) |
| 图生图编辑 | `python scripts/comfy.py i2i <图片> "<编辑指令,英文佳>" [--workflow 名]`(Qwen-Image-Edit) |
| 图生视频 | `python scripts/comfy.py i2v <图片> "<运动描述>"`(catalog 默认 video_*;Mac 慢) |
| 列出/装工作流依赖 | `comfy.py workflows`(全部) / `comfy.py install <名>`(按 catalog 下它要的模型+节点) |
| 跑任意工作流 | `python scripts/comfy.py raw <工作流.json> [--var k=v]`（UI 自动转 API；自定义工作流走这条） |
| 架构参考模板库 | `workflows/library/`(原 ui_templates,20+ 架构;`raw workflows/library/<名>` 跑) |
| 转格式不执行 | `python scripts/comfy.py convert <ui.json> -o <api.json>`（UI→API） |
| API→UI（画布可开） | `python scripts/build/api2ui.py <api.json> <out_ui.json>`（用 /object_info 还原扁平 litegraph，画布能编辑、`raw` 能跑） |
| 扁平图抠透明（color-key） | `python scripts/post/keyflat.py <in.png> <out.png> [--tol 70] [--bg ff00ff]`（洪水填充抠纯色底；或 `t2i … --keyflat` 生成即抠） |
| 像素化+统一调色板 | `python scripts/post/pixelize.py <in.png> <out.png> [--px 96] [--colors 32]`（插画→真像素;或 `t2i/raw … --pixelize --px N --colors N`,跑在 --keyflat 之后） |
| **给项目铺开整套管线** | `python scripts/comfy.py init <项目路径> --name <项目名>`（复制模板 scripts/comfyui+assets 骨架+规约 → 装 canonical 工作流 → 建反向软链 → 打印模型清单。别人装完 skill 一条命令复刻整套） |
| **批量/过夜生图** | `bash scripts/batch.sh <资产目录> --project <名> --workflows-dir <仓>/comfy-workflows [--variants N] [--only props,ui] [--dry-run]`（读各文件夹 `assets.json` 照计划批量出;详见 `scripts/batch/README.md`） |
| 上传输入图 | `python scripts/comfy.py upload <图片路径>` |
| 释放内存 | `python scripts/comfy.py free`（大任务之间/OOM 时） |

- `t2i`/`i2i`/`i2v` 跑的是 catalog 里该任务的默认工作流(JSON,和画布同一份);`--workflow <名>` 可指定同任务的其它工作流。
- 想先看工作流不执行：加 `--dry-run`。
- 写提示词前看 `reference/prompt-engineering.md`——不同架构写法差异很大（FLUX/Z-Image 低 cfg、自然语言、别堆质量词；视频要动作优先）。
- 产物默认下载到 `./comfy_outputs`（或 `COMFYUI_OUTPUT` 指定目录），同时 ComfyUI 自己也会存到它的 `output/`。
- **按项目归档**:在项目里生成始终带 `--project <名>`(或 `COMFY_PROJECT`),产物落 `output/projects/<名>/`;`init` 已把它反向软链到项目仓 `assets/`,出图直接进仓随 git(手动建链见 art-pipeline.md)。ComfyUI 根目录默认 `/Users/links/Coding/Hub/ComfyUI`,可 `COMFYUI_HOME` 改。
- **通用工作流 vs 项目专用工作流(两层):**
  - **通用**(t2i/i2i/i2v/抠图等任何项目都用)→ 进 skill `workflows/<媒体>/` + `catalog.json`,CLI 命令直接调,所有项目共享。
  - **项目专用**(只有本项目要的固定构图/角色三视图等)→ 存项目仓 `<repo>/comfy-workflows/`,反向软链 `ln -sfn <repo>/comfy-workflows <ComfyUI>/user/default/workflows/projects/<项目>`,用 `comfy.py raw <wf>.json --var k=v --project <项目> --prefix <类>/<名>` 跑。
  - **选择逻辑**:能复用→通用(catalog);只此项目→项目仓 + `raw`。
- 生成完后**用 Read 工具把产出的 png 读出来给用户看**，确认效果。
- **批量/过夜任务交给用户在自己终端跑,Claude 不要自己在 CLI 里执行**:这类任务耗时长、要看实时进度 UI、要可中断——用户自己的终端观测性和控制权更好。Claude 的职责是:① 把 `assets.json` 计划和提示词写好;② 用 `--dry-run` 验证命令正确;③ **给出可直接粘贴的完整命令**并引导用户在自己终端执行。
- 报错先查 `reference/troubleshooting.md`。

### 3. 遇到 catalog 没有的架构/场景怎么办(新增工作流的标准流程)

catalog 默认覆盖:Z-Image(t2i)、Qwen-Image-Edit(i2i)、RMBG/SAM2(抠图)、Wan 2.2(i2v)。
要加新场景(网上搜的工作流、其它架构 HunyuanVideo/LTXV/SD3/Flux…),**优先级从高到低**:

1. **找现成**:`workflows/library/` 有 20+ 架构 UI 模板 → 先 `raw workflows/library/<名>` 验证(自动转 API;模型名不符会报 `value_not_in_list` 列出真实可选项)。`reference/architectures.md` 有节点链速查。
2. **官方模板**:ComfyUI 自带 443+ 模板(路径见 `reference/api-format.md`),同样 `raw` 跑。
3. **手写**:照 `reference/api-format.md` 的格式 + slot 表 + UI→API 5 规则 + `/object_info/<节点>` 手写。
4. **沉淀成 catalog(关键,让它变成一等工作流):**
   - 工作流做成**分组版**(见 `reference/workflow-style.md`:命名 `<媒体>_<模型>`、彩色分组、Note、`<prompt>`/`<image>` 占位)→ 放 `workflows/<媒体>/`;
   - `workflows/catalog.json` 加一条(category/task/file/vars/models 含魔搭下载信息/nodes/note);
   - 用户 `comfy.py install <名>` 自动备齐模型与节点。
   - 这样它就能被 CLI(`--workflow <名>`)、`workflows`/`install`、`init` 统一管理。**不再往 `scripts/build/workflows.py` 加代码 builder(已弃用)。**

### 缺模型时

用户想要某架构但没装模型 → `discover` 会显示当前没有该能力 → 按 `reference/models-catalog.md` 给出下载目录与 HuggingFace 来源，下到对应 `models/<目录>/` 后重新 `discover` 即自动识别。

## 脚本结构（单一职责拆分）

```
scripts/
├── comfy.py            # CLI 入口（瘦壳：把 core/build/post/cli 加到 sys.path → 调 cli/app）
├── cli/
│   └── app.py          # 参数（argparse）+ 命令逻辑（cmd_t2i/i2i/i2v/raw/workflows/install/… + catalog 编排 + 后处理）
├── core/               # 基础设施
│   ├── comfy_api.py    #   纯 ComfyUI HTTP 客户端（提交/轮询/上传/下载/object_info/free/queue）
│   └── inventory.py    #   库存发现 + 架构归类（discover 用；只回答"装了啥、能干啥"）
├── build/              # 工作流构建/转换
│   ├── ui2api.py       #   UI/Litegraph → API（CLI 跑 JSON 工作流时自动转）
│   ├── api2ui.py       #   API → UI/litegraph（画布可开，拓扑分层布局）
│   ├── groupify.py     #   给工作流加彩色分组框 + Note（出厂标准，见 workflow-style.md）
│   └── workflows.py    #   [已弃用] 旧代码 builder，CLI 不再用，保留供参考
├── post/               # 图像后处理（可扩展类别：新后处理器丢这里）
│   ├── keyflat.py      #   纯色底 color-key 抠透明（扁平美术）
│   └── pixelize.py     #   像素化 + 统一调色板
├── batch/              # 批量生图引擎(纯机械,零 LLM)
│   ├── run.py          #   读 assets.json → 逐条调 comfy.py → 容错/续跑/丰富终端 UI
│   └── README.md       #   assets.json 格式 + 用法
├── setup/setup_matting.sh  # 抠图整套一键复刻(节点+模型+依赖+补丁)
└── batch.sh            # 批量入口(skill 侧;项目侧用 templates 里的瘦壳版)
# scripts/ = 引擎(运行时,不进用户项目)。各类目录都在 sys.path 上,新增脚本放对类别即可。
workflows/          # ★ 工作流单一真源(CLI 与画布共用同一份)
├── catalog.json    #   注册表:每工作流→分类/任务/默认/文件/需要的模型+节点/CLI注入占位
├── image/          #   图像工作流(t2i / i2i 编辑 / 抠图 / 以后 upscale、inpaint…)
├── video/          #   视频工作流(i2v / 以后 t2v…)  (audio/、3d/ 同理按需新建)
└── library/        #   通用架构参考模板(原 ui_templates,20+;raw 跑,非默认)
templates/          # ★ 项目脚手架(comfy.py init 复制进用户项目)
├── scripts/comfyui/{batch.sh(瘦壳调引擎), setup.sh(建软链)}
├── comfy-workflows/ # 项目专用工作流空槽(只 README;通用工作流走 skill workflows/)
├── assets/         # 标准目录骨架 + 各级 README + 示例 assets.json + Style Bible
└── docs/art-pipeline.md   # 治理规约
comfyui-nodes/      # skill 内置自定义节点(init 装进 ComfyUI/custom_nodes)
manifests/models.json  # 模型详单 + 魔搭来源(人读;机器下载走 catalog 的 install)
reference/          # 架构配方 / 提示词 / 排错 / 模型目录 / 视频 / API 格式 / 工作流出厂标准 / Mac
state/inventory.json     # 最近一次 discover 的缓存
```

## 参考文档

- `reference/workflow-style.md` — **★ 画布工作流出厂标准(强制):命名/分组/Note/布局/catalog 沉淀流程。建任何工作流前必读。**
- `workflows/catalog.json` — 工作流注册表(单一真源):新增工作流照它的字段加一条
- `reference/architectures.md` — 两种加载范式 + 20+ 架构节点链速查 + CLIP type / 采样配方
- `reference/prompt-engineering.md` — 按架构的提示词写法、负向积木、画质问题解法
- `reference/troubleshooting.md` — Mac 相关排错表 + 节点→自定义包 速查 + OOM 阶梯
- `reference/models-catalog.md` — 各架构模型下载目录与 HuggingFace 来源、选型经验
- `reference/video-pipeline.md` — 帧数/时长、Wan 首尾帧、FFmpeg 拼接转场、对口型
- `reference/lora-training.md` — LoRA 数据集/打标/步数要点（方法论）
- `reference/api-format.md` — API vs UI 格式、REST 端点表、UI→API 5 规则、slot 表
- `reference/web-integration.md` — 把文生图接入 Web 应用（FastAPI 后端代理 + React 调用、安全清单）
- `reference/mac-notes.md` — MPS 性能预期、fp8、内存、run.sh/stop.sh

## 实测基线（macOS / MPS）

- Z-Image Turbo 文生图 1024×1024 / 8 步：首次约 **270–280s**（含模型加载），二次更快（模型已驻留）。
- Wan 2.2 14B i2v 视频在 Mac 上**显著慢于 CUDA**，请提前告知用户并给足 timeout（默认 3600s）。

## 抠图(Mac 本地神经抠图 + 文字/选区,2026 新增)

不止 color-key——集成 **ComfyUI-RMBG**(RMBG-2.0/BEN2/SAM2/GroundingDINO)做神经抠图。

**一键复刻整套**(另一台机/另一个人):
```bash
COMFYUI_HOME=~/Coding/Hub/ComfyUI bash scripts/setup/setup_matting.sh
```
装节点 + 依赖(含 transformers 降 4.49)+ 魔搭下模型 + GroundingDINO 补丁 + run.sh 离线 + skill 5 个自定义节点。详单见 `manifests/models.json` 的 `matting` 段。

**用法**:画布开 `image_cutout_rmbg2_sam2`(Cutout 节点 auto/text 选模式 + MaskRefine 手绘微调);CLI `comfy.py matte`;t2i/raw 加 `--matte [--matte-text dress]`;批量 assets.json `"matte": {"model":"RMBG-2.0"}` 或 `{"text":"dress"}`。
**Mac 注意**:文字 device 用 CPU;SAM3 需 triton(CUDA)不可用;GroundingDINO 提示词必须英文。

## 角色动作集(图生图编辑锁角色,2026 新增)

用 `i2i`(image_qwen_image_edit_2511,Qwen-Image-Edit)从**一张定妆参考图**锁住同一角色出整套动作——不用 ControlNet、不训 LoRA,Mac 上实测同角色 idle/walk/run/jump/attack 一致性好(~150s/张)。

- **单张**:`comfy.py i2i <参考图> "the same character running, full body, plain bg, keep identical design" --project <项目> --prefix characters/hero/run`(`--prefix` 优先于源图名,出干净的动作名)。
- **整套(零 LLM 过夜)**:assets.json 里参考图放 `defaults.vars.image`、每个动作一条 item 的 `vars.prompt` → `batch.sh assets/characters --project <项目>`。模板见 `templates/assets/characters/assets.json`。
- 提示词英文佳,强调 "the same character / keep identical design and outfit",动作别太复杂。
- 想要**多角度转身图**(单图多视角):可加 Qwen-Image-Edit 转身/多角度 LoRA(`tarn59/character_turnaround_sheet...`,触发词 `Character turnaround sheet`);逐帧动画走 i2v(Wan,Mac 慢)。
