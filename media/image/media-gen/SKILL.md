---
name: media-gen
description: >-
  通用生图的统一入口（provider 抽象层）——一个调用，底下可插拔路由到多个生图后端
  (gemini-gen / comfyui / codex-image-gen / dashscope 通义万象直连 API / browser-gen / ark 槽位)，上层不用
  关心调的是哪个。当要生图但不想手动挑后端、要一致的统一结果契约、要失败自动降级、
  或在 asset-bridge / produce-pipeline 等编排里程序化出图时使用。Triggers: 统一生图,
  生图路由, 出图但不挑后端, 自动降级出图, media-gen, unified image gen, image provider
  router, generate an image (backend-agnostic)。吃 style-lock v1 保品牌一致，返
  {path, type:"image", backend, meta} 统一结果。借 Pixelle MediaService 抽象思路：
  一个入口按配置/可用性路由 + 统一结果 + capability 元数据。
---

# media-gen —— 统一生图入口（provider 抽象 + 路由 + 降级）

把 `gemini-gen / comfyui / codex-image-gen / dashscope（通义万象直连 API）/ browser-gen / jimeng / ark` 这些**各调各的**生图后端，收敛到**一个统一入口**：上层只说「我要这张图」，由本 skill 按**配置 + 可用性**路由到合适后端、出错自动**降级到下一个**，最后返**统一结果契约**。学 Pixelle-Video 的 `MediaService` 抽象——一个入口按 `source/前缀` 路由到不同 provider，统一返 `MediaResult`，每个 provider 带 capability 元数据。

> **媒体生态定位**：本 skill 是 `media/image` 层的**调度壳**，不重造任何出图能力——底下复用既有五个后端。`asset-bridge`（素材生成环节）、`produce-pipeline`（制片流水线素材阶段）调它，不直接挑后端。要点名某后端时仍可绕过本 skill 直接调那个 skill。

## 何时用

- **要生图，但不想手动挑后端**——交给路由按默认链 + 可用性决定。
- **要统一结果契约**——不管底下走哪个后端，都返一致的 `{path, type, backend, meta}` JSON，方便上游编排消费。
- **要失败自动降级**——一个后端撞额度 / 报错 → 自动跳下一个（`gemini-gen` 本就内置多账号跳号，本 skill 在它之上再做**跨后端**降级）。
- **被 `asset-bridge` / `produce-pipeline` 程序化调用**——它们不该耦合某个具体后端。

> 反例（**不**走本 skill）：用户**点名**「用 ComfyUI 出图 / 用 Gemini 画」→ 直接调那个后端 skill。要手绘小黑配图 → `links-illustrations`。要 HTML 图表 → `html-diagram`。本 skill 只管「通用生图、由我来选后端」。

## 统一接口（一个调用）

入口 `scripts/media_gen.py`，任意 python 调用即可。**stdout 只吐一行统一结果 JSON**，进度 / 决策日志走 stderr。

```bash
MG=~/.claude/skills/media-gen/scripts/media_gen.py   # 或 skill 真身 .../media/image/media-gen/scripts/

# ① 最简：一句提示词 → 走默认降级链，自动拼 style-lock，返统一结果
python3 "$MG" gen --prompt "一条数据流穿过暗场，几何线框，柔和辉光" --out out/hero.png

# ② 带尺寸 + 参考图（锁角色/画风）
python3 "$MG" gen --prompt "同一角色，全身，纯背景" \
  --aspect 16:9 --ref refs/hero.png --out out/hero-run.png

# ③ 指定后端偏好（仍会在该后端失败时按链降级，除非 --no-fallback）
python3 "$MG" gen --prompt "..." --prefer comfyui --out out/x.png

# ③b 点名通义万象直连 API（有成本但稳；key 读 media-api-keys.json，绝不硬编码）
python3 "$MG" gen --prompt "..." --prefer dashscope --aspect 16:9 --out out/x.png

# ④ 关掉 style-lock 注入（默认开；非品牌图才关）
python3 "$MG" gen --prompt "..." --no-style-lock --out out/x.png

# 决策预演（不真生成）：打印路由决策 + 完整降级链 + 各后端可用性
python3 "$MG" gen --prompt "..." --out out/x.png --dry-run

# 能力 / 后端清单
python3 "$MG" providers          # 列各后端 capability + 当前可用性
python3 "$MG" contract           # 打印统一结果契约 schema
```

### 参数

| 参数 | 说明 |
|------|------|
| `--prompt` | 必填。主体 + 构图 + 配色 + 留白，越具体越好。本 skill 会在前面自动拼 style-lock 的 `locked_prompt`（除非 `--no-style-lock`）。 |
| `--out` | 必填。保存路径，父目录自动建。 |
| `--aspect` | 可选。`16:9` / `1:1` / `9:16` 等；按后端转成它认的形参（gemini `--aspect` / codex `--size` / comfyui `--w/--h`）。 |
| `--ref` | 可选，可重复。参考图，做系列图锁角色 / 画风时带上。**注意**：不是所有后端都吃 ref（见 capability 表）；带 ref 时路由会优先选支持 ref 的后端。 |
| `--prefer` | 可选。后端偏好（`gemini-gen`/`comfyui`/`codex-image-gen`/…），把它提到链首；仍会降级，除非 `--no-fallback`。 |
| `--no-fallback` | 可选。只试链首一个后端，失败即失败，不降级。 |
| `--no-style-lock` | 可选。关掉 style-lock 注入（非品牌图才关）。 |
| `--style-lock` | 可选。指定 画风锁.md 路径（默认自动找 Media-Studio `风格卡/风格锁/画风锁.md`）。 |
| `--dry-run` | 可选。只打印路由决策 + 降级链 + 可用性，不真生成。 |

## 路由 + 降级（核心）

本 skill 不自己生图，它**决策走哪个后端**并**串行降级**。完整决策表、capability 元数据、降级链见 [`reference/providers.md`](reference/providers.md)，要点：

1. **默认链（与 Media-Studio 能力矩阵 / style-lock 同源）**：
   `gemini-gen`（免费快·默认）→ `codex-image-gen`（gpt-image-2·参考图锁风格）→ `comfyui`（本地可控·模型无关）→ `dashscope`（通义万象直连 API·可控质量稳定·≈¥0.14/张）→ `browser-gen`（Gemini 网页·兜底稳出）。
2. **`--prefer X`**：把 X 提到链首，其余按默认顺序续在后面。
3. **带 `--ref`**：路由优先选**支持参考图**的后端（gemini-gen / codex-image-gen / comfyui-i2i），把不支持的降权（dashscope t2i 主路不吃 ref，带 ref 时会被降权）。
4. **降级触发**：某后端**不可用**（依赖缺失 / 未配置）→ 跳过不计失败；某后端**真失败**（撞额度 / 报错 / 退出码非零）→ 记一次失败、跳下一个。链路耗尽仍失败 → 返失败结果（**绝不**假装生成）。
5. **直连 API 后端（需 key）**：
   - `dashscope`（通义万象）：key 已配（`media-api-keys.json` 的 `dashscope.api_key`，**运行时读·绝不硬编码**），判定 `ready`、**进默认自动链**——这是有成本但稳定的真后端，免费/订阅/本地档都不可用时兜底出图。已真测：M3 上提交→SUCCEEDED→下载约 5~10s/张。
   - **审核降级（被拒→中性化重写→重试一次）**：生图被内容审核拒同样常见（dashscope 等直连 API 会以 `DataInspectionFailed` / 敏感内容 等标志拒）。`dashscope` 调用内置审核降级（共用逻辑，借 Pixelle / ai-video-gen 的 `moderation_fallback`）：首次被拒 → 判是否审核类错误 → 是则把 prompt **中性化重写**（去暴力/危险/极端表达、保留画面主题与品牌风格）、**重试一次**；中性化后仍失败 → 诚实带「原始 + 重试」两段错误返失败，不静默吞。**非审核类错误**（网络 / 超时 / 服务端 5xx / 下载失败）**不触发**中性化（不掩盖真因），直接返失败让上层降级到下一后端。正常出图链路完全不受影响——只有 `failed` 且审核类才触发。逻辑在 `scripts/providers.py` 的 `is_content_inspection_error` / `neutralize_prompt` + `_invoke_dashscope`，单测 `python3 scripts/providers.py --selfcheck`（不烧 API、不触发真审核）。
6. **槽位后端**（默认链外，需用户显式启用）：
   - `browser-gen`：要 Chrome MCP 实时驱动，CLI 不可全自动 → 路由判定为「需人工 / 半自动槽位」，给提示而非静默跳。
   - `ark`（字节 Seedream）：`media-api-keys.json` 的 `ark.api_key` **当前为空**，判定为槽位、给「填 key 后接入」提示（OpenAI 兼容 `/images/generations` 同步接口，slot invoke docstring 已写好接入路径，补 key + 落地真调后切 ready）。
   - 其它直连 API（GPT-Image 付费 · `jimeng`/Dreamina 付费）：**需用户配 key / 权限**。本 skill **绝不**擅自调未授权付费接口——判定为槽位，打印「该后端需配置 X 才能启用」的清晰提示。

## 吃 style-lock v1（品牌一致）

所有生图**默认**自动拼 style-lock：读 `风格卡/风格锁/画风锁.md` 的 frontmatter，把 `locked_prompt` 拼到用户 prompt 前、`negative_prompt` 透传给支持负向的后端（comfyui）。这样跨内容画风不漂移。注入规则、各后端如何吃负向 / seed / sref 见 [`reference/style-lock-injection.md`](reference/style-lock-injection.md)。

- frontmatter 的 `backend: gemini-gen` + 降级链与本 skill 默认链一致（同源），但**本 skill 的 `--prefer` / 可用性**优先于 frontmatter 的静态声明。
- 没传 `--style-lock` 时自动向上找 Media-Studio 的 画风锁.md；找不到则跳过注入并在 stderr 提示（不报错）。

## 统一结果契约（借 Pixelle MediaService）

无论底下走哪个后端，stdout 都吐**一行 JSON**，schema 见 [`reference/result-contract.md`](reference/result-contract.md)：

```json
{
  "ok": true,
  "type": "image",
  "path": "/abs/path/out/hero.png",
  "backend": "gemini-gen",
  "meta": {
    "prompt_final": "<style-lock + 用户 prompt>",
    "aspect": "16:9",
    "refs": ["refs/hero.png"],
    "style_lock": "v1",
    "attempts": [{"backend": "gemini-gen", "status": "ok"}],
    "fallback_chain": ["gemini-gen", "codex-image-gen", "comfyui", "browser-gen"]
  }
}
```

- 失败：`{"ok": false, "type": "image", "path": null, "backend": null, "meta": {"attempts": [...], "error": "..."}}`。
- `attempts` 记录每个试过的后端及其 `status`（`ok` / `failed` / `unavailable` / `slot`），上游可据此知道**到底走了哪个、为什么降级**。

## capability 元数据

每个后端带一份能力元数据（尺寸支持 / 是否吃 ref / 是否吃负向 / 授权与成本 / 可用性探测），是路由决策的依据。全表见 [`reference/providers.md`](reference/providers.md)。路由读它来：① 带 ref 时筛支持 ref 的后端；② 探测后端是否可用（命令在不在、服务起没起、key 配没配）；③ 把成本/授权信息透出到结果 meta，让上游知道这张图花了什么（如 `dashscope` 透出 `cost: paid` ≈¥0.14/张）。直连 API 后端（dashscope/ark）的 key 从 `media-api-keys.json` **运行时读**——`api_key` 为空即判 `unavailable`/`slot`，绝不假装出图。

## 边界与诚实底线

- **本 skill 只路由，不重造生图**——所有像素都由底下后端产，本 skill 负责选 + 降级 + 统一结果。
- **不注册账号、不硬编码 key、不擅自调未授权付费接口**——key **运行时读** `_secrets/media-api-keys.json`，绝不写进脚本/不回显/不入库；`ark` / `jimeng` 等未配 key 或需权限的后端是**槽位**，路由判定为槽位时给清晰提示，**绝不假装生成**。
- **诚实标完成度**：当前真能路由——`gemini-gen` / `codex-image-gen` / `comfyui`（现成可调）+ `dashscope`（通义万象直连 API，**key 已配·已真测 t2i 出真图**·有成本·**带审核降级中性化重试**）；槽位——`browser-gen`（半自动）、`ark`（Seedream，**待用户填 key**）、`jimeng`（付费需 vip）。结果 `attempts` 里如实记每个后端 `ok/failed/unavailable/slot`。审核降级逻辑已写对并单测验证（`providers.py --selfcheck`），**未真触发审核测**（克制·不烧 API）。
- 本地可逆、不 push。
