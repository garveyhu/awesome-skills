---
name: codex-image-gen
description: 用 Codex(订阅账号,gpt-image-2)生成或编辑图片。当用户要求“生成/画/做一张图片、插图、图标、封面、配图、icon、illustration、generate/make/draw an image”,且未指定其他出图后端(comfyui / jimeng 等)时使用。通过 `codex exec` 调内置 image_gen 出图,产物存为 PNG;支持参考图锁定角色/风格一致性。
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

## 成本 & 前置

- **走订阅额度,不按张计费**;每张约 1.5w–3w Codex token(agent token 计入 Codex 用量)。
- 依赖:`~/.codex/auth.json` 已登录(本机已是订阅登录);`codex` 在 PATH(已全局安装),否则脚本自动退回 `npx @openai/codex@latest`。

## 和其它 skill 配合

- **docsify-station-creator / wiki-creator**:生成的图存进文档 `assets/`,需要公网 URL 时按 `~/.claude/rules/cdn-publish.md` 推到 `cdn.archeruuu.com`,markdown 里引用——站点运行时仍只引自托管资源。
- **要带固定 IP 角色出图**:把角色设定写进 prompt + 用 `--ref` 喂角色参考图;后续若要做成专门的「IP 配图 skill」,可在本 skill 之上加一层风格/IP 参考(参考 ian-xiaohei 的 references 结构)。
