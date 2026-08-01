---
name: codex-image-gen
description: 用 Codex(订阅账号,gpt-image-2)生成或编辑图片,特长是用参考图锁定角色/风格一致性。当用户显式点名用 Codex 出图,或需要参考图锁角色/风格的场景时使用。通过 `codex exec` 调内置 image_gen 出图,产物存为 PNG。通用生图/程序化出图未点名具体后端时,由 `media-gen` 统一路由选后端,不在此抢默认。
---

# Codex 生图

借用本机已登录的 **Codex 订阅账号**,经 `codex exec` 调用其内置 `image_gen` 工具(gpt-image-2)出图。Claude Code 自身无生图能力,这个 skill 就是那座桥:你写好提示词,它出 PNG。

## 何时用

- 用户要为文章 / 文档 / 网页生成插图、配图、封面、图标、Banner、占位图等。
- 用户要基于参考图做角色一致的系列图(给 `--ref`)。
- **未**指定走 ComfyUI / 即梦等其他后端时,这是默认出图后端。

## 怎么用

只调一个脚本(已可执行):

```bash
bash ~/.claude/skills/codex-image-gen/scripts/gen-image.sh \
  --prompt "画面的具体描述" \
  --out "目标路径/名字.png" \
  [--size 16:9] \
  [--ref 参考图1.png] [--ref 参考图2.png] \
  [--dir 工作目录]
```

- 脚本成功后会把最终 PNG 路径打到 stdout;失败退出码非零。
- 产物同时保留在 `~/.codex/generated_images/`,脚本会把它拷到 `--out`。
- 多张图就多次调用,**一次一张**(别让模型把多图拼进一张)。

### 参数要点

| 参数 | 说明 |
|------|------|
| `--prompt` | 必填。越具体越好:主体、风格、构图、背景、配色、留白。英文对模型更稳,中文也支持。 |
| `--out` | 必填。保存路径,父目录自动建。 |
| `--size` | 宽高比 / 尺寸:`16:9`、`1:1`、`1536x1024` 等。不传由模型自定。 |
| `--ref` | 参考图,可重复。**做系列图保持同一角色 / 同一画风时务必带上**,一致性远好于纯文字描述。 |
| `--dir` | codex 工作目录,默认取 `--out` 父目录,一般无需指定。 |

## 写提示词的几条

- 一张图只讲一个主体 / 一个结构,别堆。
- 指明风格(手绘线稿 / 扁平插画 / 3D / 像素 / 水彩…)、背景(纯白 / 透明 / 渐变)、配色、留白。
- 要文字标注就在 prompt 里写清要出现的**短**文字(模型出长文/多字容易错)。
- 透明背景:prompt 里写 "transparent background" 或 "on a solid green background for chroma key"。
- 出图后用 Read 工具看一眼成品,不满意就改 prompt 重生成,或追加 `--ref 上一张` 局部调整。

## 出图必留痕（sidecar 约定 · 260712 素材体系）

**每张进媒体工作流的产物都要留痕**：素材落**分类目录**（内容级 `素材/{真材料,生图,精灵}/`、频道级 `风格卡/素材库/{插画,装置}/`），出图成功后往本类 `_meta/<名>.json` 写 sidecar——新对话/新频道零人工记忆，asset-index 扫描即得（prompt 直接成检索描述符），qc 可 `ls` 对账（每文件 ↔ 一条 sidecar）。

```bash
# 出图后（gen-image.sh / gen-batch.sh 成功落盘后）补一行：
~/.venvs/current/bin/python ~/.claude/skills/codex-image-gen/scripts/write_sidecar.py \
  --out "素材/生图/shot-3.png" --prompt "刚才的完整提示词" --backend codex-image-gen \
  [--aspect 16:9] [--ref shot-3] [--license original] [--washed true]
```

- **`gen-image.sh` 不内嵌此步**——留痕由**调用方/管线**负责（编排素材步时调本 helper 补写）。
- 幂等可重跑：已有 sidecar → 字段覆盖更新、`refs` 去重追加、`created` 保留首次；产物不存在则拒写（不给不存在的东西记账）。
- 后端无关：图/视频/HTML/音频都能记（`--kind` 缺省按扩展名自判），其它出图后端（gemini-gen / comfyui / media-gen 编排）同样可调本工具留痕。

## 批量出图（并发，多张时用这个）

要一次出很多张（系列配图、整套资产）时，**不要串行一张张等**——`gen-image.sh` 是单图工具（一次一张），并发交给批量入口 `scripts/gen-batch.sh`：

1. 为每张图写一个 job 文件：**文件名（去 `.txt`）= 输出图基名，内容 = 完整提示词**。
   `jobs/01-topic.txt` → 出 `01-topic.png`。
2. 跑：

```bash
bash ~/.claude/skills/codex-image-gen/scripts/gen-batch.sh \
  --jobs <jobs目录> --outdir <输出目录> \
  [--concurrency 3] [--ref 定妆图.png] [--size 16:9]
```

- prompt 走文件传入，免命令行转义与长度限制；每个 job 输出独立路径，主路径并发安全；用 FIFO 信号量滚动并发，兼容 macOS 自带 bash 3.2。
- **`--concurrency` 先从 3 起**：Codex 订阅有服务端速率限制，开太高可能整批被限流。遇报错就降到 1-2，失败的 job 单独重跑即可（已成功的不受影响）。
- 系列图保持同一角色：所有 job 都带同一张 `--ref` 定妆图。

## 按层生成（分层素材协议·喂 video-master 分层镜）

给 `layered-parallax`（分层视差）/ `layered-reveal`（测绘揭示）出素材时，**不生成一张整图再拆，而是源头按层生**——生图无限额度下这是零分割误差、零补洞、风格零漂移的路线：

1. **style anchor**：写一段风格锁（画风 / 色板 / 质感 / 禁用元素），**贴在每个 prompt 顶部**锁全组一致；有频道画风锁就从它生成。
2. **布局参考图**：先出一张完整构图（只用来定各元素位置关系，不进成片）。
3. **背景板**（`bg.png`·不透明）：单独一张，"background only, no subject, low contrast"。
4. **逐元素出层**（每元素一张·全画布同尺寸）：主体 / 配角 / 道具各一张，**纯 chroma 平底**——prompt 写 `isolated subject on a solid pure green background (#00FF00), no shadows, no reflections, positioned at <布局参考里的位置>`；绿色主体换品红底 `#FF00FF`。**Codex 内置 image_gen 不支持透明背景**（请求透明会存成不透明 RGB），chroma 底是官方 imagegen skill 的标准解法。系列层全部 `--ref` 布局参考图（或前一层）锁风格与相对位置。
5. **去底**：`~/.venvs/current/bin/python ~/.claude/skills/codex-image-gen/scripts/strip_chroma.py in.png out.png`（key 自动取边框中位色；`--key green|magenta|#RRGGBB` 可显式指定）。自带 despill 去溢色 + 收边 1px；stderr 报 `kept_ratio` 异常时肉眼核。
6. **从一张定稿图衍生层**（备路）：已有整图必须拆时，用 codex 编辑模式出两张——"remove the subject, keep only the background" + "keep only the subject, on solid green background"，风格零漂移。

产物命名约定：`bg.png` + `layer-<序号>-<语义名>.png`（如 `layer-1-figure.png`），全画布同尺寸（元素位置烘焙在图内），直接进引擎 `public/images/<内容>/` 喂 scenes payload。

## 成本 & 前置

- **走订阅额度,不按张计费**;每张约 1.5w–3w Codex token(agent token 计入 Codex 用量)。
- 依赖:`~/.codex/auth.json` 已登录(本机已是订阅登录);`codex` 在 PATH(已全局安装),否则脚本自动退回 `npx @openai/codex@latest`。

## 和其它 skill 配合

- **docsify-station-creator / wiki-creator**:生成的图存进文档 `assets/`,需要公网 URL 时按你自己的 CDN 规约推到公网 CDN,markdown 里引用——站点运行时仍只引自托管资源。
- **要带固定 IP 角色出图**:把角色设定写进 prompt + 用 `--ref` 喂角色参考图;后续若要做成专门的「IP 配图 skill」,可在本 skill 之上加一层风格/IP 参考(参考 ian-xiaohei 的 references 结构)。
