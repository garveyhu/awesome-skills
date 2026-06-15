# 美术资产管线与规约(项目治理)

> 本文由 comfyui skill 的 `init` 脚手架生成,是本项目美术生产的**方法论权威**。
> 各类资源的具体提示词/状态在 `assets/<类>/` 的 `README.md` + `assets.json`;
> 引擎与命令细节见已安装 skill 的 `SKILL.md` 与 `scripts/batch/README.md`。

## 1. 两阶段分工(核心)
- **① 设计期(Claude / 人,一次性)**:把**提示词 / 结构 / 工作流 / assets.json** 配好——要创意与判断。
- **② 执行期(纯脚本,零 LLM)**:`scripts/comfyui/batch.sh` 照 assets.json 无人值守批量出图,**不调用大模型、零 API 成本**,适合过夜在自己终端跑。
- **绝不在 batch 链路塞需要 LLM 的步骤。**

## 2. 资产在仓里 + ComfyUI 反向软链
- `assets/` 与 `comfy-workflows/` 是项目仓内真实目录,随 git 提交、可协作维护。
- **反向软链**:`<ComfyUI>/output/projects/<项目>` → `assets/`;`<ComfyUI>/user/default/workflows/projects/<项目>` → `comfy-workflows/`。出图与工作流穿过软链直接落进仓。
- 建软链:`bash scripts/comfyui/setup.sh`(`init` 已自动建一次;换机器重建即可)。

## 3. 目录与 assets.json
见 [`assets/README.md`](../assets/README.md):目录约定 + 状态图例 + Style Bible + **assets.json 完整 schema**。

## 4. 管线:生成 → 抠透明 → 像素化
- **生成**:`t2i`(文生图,catalog 默认)/ `i2i`(图生图编辑,Qwen-Image-Edit)/ 项目专用工作流 `raw`。
- **抠透明**:`--keyflat`(纯色底洪水填充 color-key,**扁平美术专用**)或 `--matte`(神经抠图,复杂主体)。⚠️ 别对扁平像素/插画用神经抠图——会整张当前景、抠不掉。
- **像素化 + 统一调色板**:`--pixelize`(降采样到像素网格 + 量化色数,统一全套风格,**美术一致性的最大杠杆**)。
- 三段在 batch / CLI 里自动串(assets.json 的 `keyflat`/`matte`/`pixelize` 控制开关与参数)。

## 5. 工作流(两层)
- **通用工作流**(任何项目都用)在 skill `workflows/<媒体>/` + `catalog.json`:`t2i`=image_z_image_turbo、`i2i`=image_qwen_image_edit_2511、抠图=image_cutout_rmbg2_sam2、`i2v`=video_wan2_2_5B_ti2v。CLI 命令直接调,和画布同一份。
- **项目专用工作流**(只本项目要的固定构图/角色三视图等)放本仓 `comfy-workflows/`,反向软链给 ComfyUI,用 `comfy.py raw <wf>.json --var k=v` 跑。
- 工作流出厂标准(命名/分组/Note/占位/catalog 沉淀)见 skill `reference/workflow-style.md`。
- **所需模型**:skill `comfy.py install <工作流名>` 按 catalog 自动下(国内走魔搭 ModelScope);详单见 `manifests/models.json`。

## 6. 治理(governance)
- **t2i 能做**:场景、道具、UI 纹理、fx、品牌图。
- **角色**:用 `i2i`(图像编辑模型)给一张参考图换姿势/换装/视角/出新角色,不用 ControlNet/不训 LoRA;**逐帧动画级完全一致**可能仍需训角色 LoRA。
- **单一真源**:`assets/<类>/`(随 git,含提示词与 assets.json);运行时目录(如 `frontend/public/`)是"接入后的成品快照"。
- **命名**:kebab-case,描述性;变体加 `-v2`;动画用横向条带、每帧等宽。
- **风格一致 > 单图惊艳**:新资源先对齐 Style Bible;统一靠 `--pixelize` 同网格同调色板。
- **二进制体量**:PNG 多时考虑用 git-lfs 跟踪 `assets/**/*.png`。
