# provider 决策表 + capability 元数据

本 skill 不生图，它**按这张表选后端 + 降级**。决策表与 capability 元数据是路由器（`scripts/media_gen.py`）的唯一事实源——改路由行为就改这里 + `scripts/providers.py` 的 `PROVIDERS` 字典（二者同步）。

## provider 决策表（何时走哪个）

| 后端 | 何时是它 | 成本 | 参考图 | 负向词 | 状态 |
|------|----------|------|--------|--------|------|
| **gemini-gen** | **免费快·默认首选**。日常 / 批量低频通用出图，会员额度内免费，内置多账号跳号 | 免费（会员额度） | ✅ | ✗（写进 prompt） | `ready` |
| **codex-image-gen** | 要 **gpt-image-2** 质量、要**参考图锁角色 / 风格一致性**（一致性好于纯文字）；走 Codex 订阅额度 | 订阅额度（不按张计费） | ✅✅（强项） | ✗ | `ready` |
| **comfyui** | 要**本地可控 / 离线 / 特定模型**（Z-Image/FLUX/SDXL…）、要负向词、要批量过夜零边际成本 | 免费（本地算力） | ✅（走 i2i） | ✅ | `ready`（需 ComfyUI 在跑） |
| **dashscope（通义万象）** | 要**直连 API 稳定出图、可控质量、不依赖本地服务/会员额度**——免费/订阅档都不可用时的**有成本但稳的真后端**；账号级 key 已配，异步任务可靠 | 付费 ≈¥0.14/张（turbo） | ✗（t2i 主路；i2i 列可扩展） | ✗（写进 prompt） | `ready`（key 已配·已真测） |
| **browser-gen** | 撞限流要「稳出一张」的**兜底**；Chrome MCP 驱动真实浏览器走 UI 通道，信任分高 | 免费（会员额度） | ✅ | ✗ | `slot·半自动`（需 Chrome MCP，不可纯 CLI 全自动） |
| **ark（字节 Seedream）** | 要 Seedream 付费档质量；OpenAI 兼容同步接口 | 付费（按量） | ✅ | ✗ | `slot·待用户填 ark.api_key` |
| **直连 API 槽位（通用）** | 要其它付费直连模型 | 付费（按量） | ✅ | 视模型 | `slot·需用户配 key` |
| **jimeng / Dreamina** | 云端高质量图 / 视频；**当前账号需 maestro vip** | 付费额度 | ✅ | ✗ | `slot·需权限+付费` |

> 与 Media-Studio `0-内核/能力矩阵.md` 第 3 行、`1-资产库/风格锁/画风锁.md` 的 `backend` 声明同源：默认 `gemini-gen` → `codex-image-gen` → `comfyui` → `dashscope` → `browser-gen` 逐级降级（dashscope 是有成本但稳定的直连 API，排在免费/订阅/本地档之后、半自动兜底之前）。

## 默认降级链

```
gemini-gen → codex-image-gen → comfyui → dashscope → browser-gen(半自动槽位)
  免费快        参考图强项        本地可控    直连API稳出      兜底稳出
                                          ¥0.14/张
```

- `--prefer X`：把 X 提到链首，其余按默认顺序续在后。
- 带 `--ref`：把**不支持 ref** 的后端降权（当前五个都支持 ref，故主要影响未来无 ref 后端）。
- **槽位后端**（browser-gen / 直连 API / jimeng）默认**不进自动链**，除非 `--prefer` 显式点名；点名时仍判定可用性，不可用就给槽位提示而非静默成功。

## capability 元数据（路由依据）

每个后端一份元数据，路由读它做三件事：① 带 ref 时筛 `supports_ref`；② `availability` 探测后端能不能跑（命令在不在 / key 配没配 / 服务在不在）；③ 把 `cost` / `auth` 透出到结果 `meta`。

| 字段 | 含义 |
|------|------|
| `id` | 后端 skill 名 |
| `tier` | `ready`（自动链内可用）/ `slot`（需配置/半自动，默认不进自动链） |
| `invoke` | 路由如何调它（脚本相对路径 + 参数映射，见下「调用映射」） |
| `supports_ref` | 是否吃参考图 |
| `supports_negative` | 是否吃负向词（仅 comfyui） |
| `aspect_param` | 尺寸怎么传：`aspect`(gemini) / `size`(codex) / `wh`(comfyui 拆 --w/--h) |
| `cost` | `free-quota` / `subscription` / `local-free` / `paid` |
| `auth` | 启用前置（cookie / 订阅 / 本地服务 / API key / vip） |
| `availability_probe` | 怎么判它当前可用（见下） |

### 各后端元数据（与 scripts/providers.py 同步）

```yaml
gemini-gen:
  tier: ready
  supports_ref: true
  supports_negative: false        # 负向写进 prompt 描述
  aspect_param: aspect            # --aspect 16:9
  cost: free-quota
  auth: gemini 会员 cookie + accounts.json
  invoke: gemini-gen/scripts/gen-image.sh  (--prompt --out [--aspect] [--ref ...])
  availability_probe: skill 脚本存在 且 accounts.json 存在

codex-image-gen:
  tier: ready
  supports_ref: true              # 强项：参考图锁角色/风格
  supports_negative: false
  aspect_param: size              # --size 16:9
  cost: subscription              # Codex 订阅额度，不按张
  auth: ~/.codex/auth.json 已登录
  invoke: codex-image-gen/scripts/gen-image.sh  (--prompt --out [--size] [--ref ...])
  availability_probe: skill 脚本存在（codex 登录在脚本内自检）

comfyui:
  tier: ready
  supports_ref: true              # 走 i2i 锁角色
  supports_negative: true         # 唯一吃负向词的后端
  aspect_param: wh                # 拆成 --w / --h（由 aspect 换算，见 result-contract）
  cost: local-free
  auth: 本地 ComfyUI 在 127.0.0.1:8188 跑
  invoke: comfyui/scripts/comfy.py t2i "<prompt>" [--w --h]  | i2i <ref> "<prompt>"（带 ref 时）
  availability_probe: comfy.py 存在 且 127.0.0.1:8188 可连（HTTP 探测，连不上记 unavailable）

dashscope (通义万象 / 阿里):
  tier: ready                     # 直连 API，已真测 t2i OK
  model: wanx2.1-t2i-turbo        # 读 media-api-keys.json dashscope.image_model
  supports_ref: false             # t2i 主路不吃 ref；i2i/图像编辑是另一组接口，列可扩展
  supports_negative: false        # 通义 t2i 无独立负向槽；style-lock 负向以 "avoid: …" 拼进 prompt
  aspect_param: size              # "宽*高"（星号）固定档：16:9→1280*720 / 1:1→1024*1024 / 9:16→720*1280 / 4:3→1024*768 / 3:4→768*1024
  cost: paid (≈¥0.14/张 turbo)    # 按张计费，账号级 key
  size_range: 512~1440 各档（turbo 推荐用上述固定档，超范围会被拒）
  n: 1                            # 每次出 1 张（批量由上游多次调）
  auth: media-api-keys.json 的 dashscope.api_key（账号级·绝不硬编码·运行时读配置）
  invoke: >-
    异步两步——
    ① POST {base}/api/v1/services/aigc/text2image/image-synthesis
       header: Authorization: Bearer <key> + X-DashScope-Async: enable
       body: {"model":<image_model>,"input":{"prompt":<prompt_final>},"parameters":{"size":<size>,"n":1}}
       → output.task_id
    ② 轮询 GET {base}/api/v1/tasks/{task_id}（Authorization: Bearer <key>，每 3s，上限 5min）
       → task_status SUCCEEDED 时 output.results[0].url 是图 URL，stdlib urllib 下载到 --out
  availability_probe: media-api-keys.json 可解析 且 dashscope.api_key 非空（从 cwd / skill 目录上溯找配置文件）
  实测: M3 提交→SUCCEEDED→下载约 5~10s/张；1280*720 PNG ~200KB

browser-gen:
  tier: slot                      # 半自动：Chrome MCP 驱动，非纯 CLI
  supports_ref: true
  supports_negative: false
  aspect_param: prompt            # 比例写进自然语言
  cost: free-quota
  auth: Chrome MCP + 已登录 Gemini
  invoke: 无 CLI —— 由 Claude 用 claude-in-chrome 工具按 browser-gen/SKILL.md 流程驱动
  availability_probe: 永远记为 slot（CLI 探测不到 MCP 会话）；给「转 browser-gen 半自动流程」提示

api-direct (Seedream / GPT-Image):
  tier: slot
  supports_ref: true
  cost: paid
  auth: 需用户配 API key（环境变量 MEDIAGEN_API_KEY 或专用配置）
  invoke: 槽位 —— 未配 key 时只给提示，绝不擅自调付费接口
  availability_probe: 检测 key 是否配置；未配 → slot 提示

jimeng (Dreamina):
  tier: slot
  supports_ref: true
  cost: paid
  auth: dreamina CLI 登录 + maestro vip 权限
  invoke: 槽位 —— dreamina text2image（付费，需 vip）；本 skill 不自动调
  availability_probe: dreamina 命令存在 但默认仍记 slot（付费，需用户显式启用）

ark (字节 Seedream / Volcengine):
  tier: slot                      # 槽位预留——ark.api_key 当前为空，待用户补 key
  model: doubao-seedream          # 读 media-api-keys.json ark.image_model
  supports_ref: true
  supports_negative: false
  aspect_param: size              # OpenAI 兼容用 "宽x高"（小写 x），区别于 dashscope 的 "宽*高"
  cost: paid (按量)
  auth: media-api-keys.json 的 ark.api_key（待用户填；base=https://ark.cn-beijing.volces.com/api/v3）
  invoke: >-
    待 key 后落地（OpenAI 兼容·同步，无需轮询）——
    POST {base}/images/generations
    header: Authorization: Bearer <key>
    body: {"model":<image_model>,"prompt":<prompt_final>,"size":"1024x1024","response_format":"url","n":1}
    → data[0].url 下载即得
  availability_probe: ark.api_key 非空才 available；为空记 slot 并给「填 ark.api_key 后接入」提示
  状态: key 空 → slot（诚实标·绝不假装出图）；补 key + 落地真调后把 tier 切 ready
```

## 调用映射（路由怎么把统一参数翻给各后端）

| 统一参数 | gemini-gen | codex-image-gen | comfyui | dashscope（通义万象） |
|----------|-----------|-----------------|---------|----------------------|
| `--prompt`（已拼 style-lock） | `--prompt` | `--prompt` | 位置参数 `"<prompt>"` | body `input.prompt` |
| `--out` | `--out` | `--out` | 产物落 comfy_outputs，路由拷到 `--out` | 轮询拿 url，urllib 下载到 `--out` |
| `--aspect 16:9` | `--aspect 16:9` | `--size 16:9` | 换算成 `--w 1280 --h 720` | `parameters.size`=`1280*720`（星号档） |
| `--ref a.png`（首张） | `--ref a.png`（可多） | `--ref a.png`（可多） | `i2i a.png "<prompt>"` | t2i 主路不吃 ref（i2i 可扩展） |
| `negative_prompt`（来自 style-lock） | 拼进 prompt | 拼进 prompt | comfyui 工作流负向槽（脚本暂拼进 prompt，TODO 走 --neg） | 拼进 prompt 尾「avoid: …」 |

aspect → wh 换算表（comfyui）：`16:9→1280x720` · `1:1→1024x1024` · `9:16→720x1280` · `4:3→1024x768` · `3:4→768x1024`（默认 1024x1024）。
aspect → size 换算表（dashscope，星号分隔）：`16:9→1280*720` · `1:1→1024*1024` · `9:16→720*1280` · `4:3→1024*768` · `3:4→768*1024`（默认 1024*1024）。

## 直连 API key 配置（绝不硬编码）

dashscope / ark 的 key **运行时读** `Media-Studio/1-资产库/发布配置/media-api-keys.json`（从 cwd / skill 目录逐级上溯找；也可用环境变量 `MEDIAGEN_KEYS_FILE` 指定）——**绝不写进脚本、不回显、不入库**。结构：

```jsonc
{
  "dashscope": { "api_key": "sk-...", "base": "https://dashscope.aliyuncs.com", "image_model": "wanx2.1-t2i-turbo" },
  "ark":       { "api_key": "",        "base": "https://ark.cn-beijing.volces.com/api/v3", "image_model": "doubao-seedream" }
}
```

`load_api_config("dashscope"|"ark")` 返对应块；`api_key` 为空即判 `unavailable`/`slot`，绝不假装出图。

## 失败 vs 不可用（降级语义）

- **unavailable**（依赖缺失：脚本不在 / 服务没起 / key 没配）→ **跳过，不计失败**，`attempts` 记 `status:"unavailable"`，继续下一个。
- **slot**（半自动 / 付费需显式启用）→ 不自动跑，`attempts` 记 `status:"slot"` + 提示，继续下一个（除非被 `--prefer` 点名，仍只给提示）。
- **failed**（真跑了但退出码非零 / 撞额度 / 报错）→ 记 `status:"failed"` + stderr 摘要，继续下一个。
- 链路耗尽全没出图 → 顶层 `ok:false`，**绝不假装生成**。
