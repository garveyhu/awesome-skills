---
name: gemini-gen
description: 用 Gemini 出图,默认走本机反代服务(antigravity2api-nodejs,Antigravity 账号池,支持参考图 + 分辨率档位),可选切回 Gemini 网页会员号(Nano Banana)cookie 方式、多账号负载均衡 + 撞额度自动跳号;支持并发批量出图(job 文件 + FIFO 信号量,系列图/整套资产一次出)。当用户要用 Gemini / Nano Banana / Antigravity 出图、"用 gemini 画图"、想薅 Gemini 订阅或 Antigravity 账号的免费图额度、要在多个账号之间轮着出图分摊额度、或要一次批量出一组图时使用。两条后端配额池互不相通。产物存图片文件,两条后端都支持参考图(风格迁移/图生图)。是继 codex-image-gen / comfyui / jimeng / browser-gen 之后的又一条出图后端。通用生图/程序化出图未点名具体后端时,由 `media-gen` 统一路由选后端;用户显式点名 Gemini/Nano Banana/Antigravity(或要薅免费额度/多账号轮换/批量出图)时仍直调本 skill。
---

# Gemini 出图(反代 + 会员号 cookie 双后端)

两条互相独立的免费/订阅内出图路径,配额池不通用,按场景选:

| 后端 | 走的通道 | 配额池 | 多账号 | 需要什么 |
|------|---------|--------|--------|---------|
| **proxy(默认)** | 本机反代服务 [antigravity2api-nodejs](https://github.com/liuw1535/antigravity2api-nodejs) → Antigravity/Gemini Cloud Code Assist | Antigravity 账号自己的额度池(跟 Gemini 网页会员号是两回事) | 反代服务自己做 round-robin + 撞额度自动禁用,本 skill 不用管 | 反代服务跑起来(`app run antigravity2api`)+ `proxy_config.json` |
| **cookie(备选,`--backend cookie`)** | 逆向 web API([`gemini-webapi`](https://github.com/HanaokaYuzu/Gemini-API))读浏览器 cookie | Gemini 网页会员号(Pro/Advanced 订阅)自己的额度池 | 本 skill 做 LRU 负载 + 冷却跳号 | 独立 Chrome profile 登录会员号 + `accounts.json` |

> 出图后端选择:本地可控批量 → `comfyui`;订阅 gpt-image → `codex-image-gen`;Gemini/Antigravity → 本 skill;要 Veo 视频 → `browser-gen`。

## 何时用

- 用户点名要 **Gemini / Nano Banana / Antigravity** 出图。
- 想**薅免费图额度**,而不是走付费 API / 本地算力。
- 有**多个账号**,想轮着用分摊每日图额度。
- 想用**参考图做风格迁移 / 图生图**(两条后端都支持,已现场验证效果稳定)。

## 怎么用

单脚本调用(已可执行,依赖经 uv 自动注入,首次稍慢):

```bash
bash ~/.claude/skills/gemini-gen/scripts/gen-image.sh \
  --prompt "画面的具体描述" \
  --out "目标路径/名字.png" \
  [--backend proxy|cookie]        # 默认 proxy \
  [--ref 参考图1.png] [--ref 参考图2.png] \
  [--aspect 16:9] \
  # proxy 后端专用：
  [--proxy-model gemini-3.1-flash-image] [--size 1K|2K|4K] \
  # cookie 后端专用：
  [--account <账号别名>] [--model flash|pro]
```

- 成功后把最终图片路径打到 **stdout**;失败退出码非零,过程信息走 stderr。
- 多张图就多次调用。

### 通用参数

| 参数 | 说明 |
|------|------|
| `--backend` | 可选。`proxy`(默认,见上表)/ `cookie`(旧方式)。 |
| `--prompt` | 必填。主体 + 风格 + 构图 + 背景 + 配色 + 留白,越具体越好;中英文均可,英文更稳。 |
| `--out` | 必填。保存路径,父目录自动建;一次返回多图时自动加 `_0` / `_1`。 |
| `--ref` | 可选,可重复。参考图,**做系列图锁角色 / 画风时务必带**——两条后端都是原生图生图/风格参考,不是简单文字转述。 |
| `--aspect` | 可选。宽高比提示 `16:9` / `1:1` / `9:16` 等(**两条后端都是 best-effort**,写进提示词而非结构化参数,模型遵循度尚可但不保证精确)。 |

### proxy 后端参数

| 参数 | 说明 |
|------|------|
| `--proxy-model` | 可选。反代模型名,默认读 `proxy_config.json` 的 `default_model`(缺省 `gemini-3.1-flash-image`)。可用模型列表见反代的 `GET /v1/models`。 |
| `--size` | 可选。`1K`(默认)/ `2K` / `4K`,通过给模型名加后缀实现,不是所有模型都支持高档位。 |

### cookie 后端参数

| 参数 | 说明 |
|------|------|
| `--account` | 可选。**指定某个会员号**(不跳号);不传则负载均衡。 |
| `--model` | 可选。`flash`(默认,Nano Banana 2,额度宽/快) / `pro`(Nano Banana Pro,更高质量但额度紧)。 |

> ⚠️ **cookie 后端模型坑(已踩平)**:`gemini-webapi` 的默认模型(UNSPECIFIED)会路由到一个图额度极小的桶,几张就报 "limit resets" **假性满额**——但账号其实没满(手动在网页用 Flash 能出)。本 skill 已强制走 `flash`/`pro`,**绝不**用默认模型。

## 批量出图(并发,多张时用这个)

要一次出很多张(系列配图、整套资产)时,**不要串行一张张等**——`gen-image.sh` 是单图工具(一次一张),并发交给批量入口 `scripts/gen-batch.sh`(设计仿照 `codex-image-gen` skill 的同名脚本):

1. 为每张图写一个 job 文件:**文件名(去 `.txt`)= 输出图基名,内容 = 完整提示词**。
   `jobs/01-topic.txt` → 出 `01-topic.png`。
2. 跑:

```bash
bash ~/.claude/skills/gemini-gen/scripts/gen-batch.sh \
  --jobs <jobs目录> --outdir <输出目录> \
  [--concurrency 3] \
  [--backend proxy|cookie] [--ref 定妆图.png] [--aspect 16:9] \
  # proxy 后端可再加：[--proxy-model 模型名] [--size 1K|2K|4K]
  # cookie 后端可再加：[--account 账号别名] [--model flash|pro]
```

- prompt 走文件传入,免命令行转义与长度限制;每个 job 输出独立路径,并发安全;用 FIFO 信号量滚动并发,兼容 macOS 自带 bash 3.2。
- 单个 job 失败只打印 `✗`,不影响其它 job;失败的单独重跑对应 job 文件即可。
- 系列图保持同一角色 / 风格:所有 job 都带同一张 `--ref` 定妆图。

> ⚠️ **两个后端的并发上限不是一回事,别用同一个数字**:
> - **proxy 后端(默认)**:多账号轮询在反代服务里做,`--concurrency` 先从 3 起,观察反代日志 / 管理台账号状态顶不顶得住,顶不住就降;某个 job 撞到坏账号是它自己的进程失败,不连累其它 job。
> - **cookie 后端**:Google 有独立反自动化限流,`gen_image.py` 的 pacing(请求前随机停顿)+ 撞额度冷却是按"单进程顺序请求"设计的,并发跑会削弱这层节奏控制;而且多进程共写 `state.json` 没加锁,并发下 LRU 游标可能互相覆盖(最坏是负载没那么均匀,不会崩,但更容易撞限流)。cookie 后端 `--concurrency` 建议压到 **1-2**。

## proxy 后端配置(默认路径,私密,不入 git)

反代地址/key 抽到 **`proxy_config.json`**(skill 根目录),格式见 `proxy_config.example.json`。该文件已被 `.gitignore` 挡住、**不进仓库**。

**首次使用 / 别人拿到 skill**:
1. 部署 [antigravity2api-nodejs](https://github.com/liuw1535/antigravity2api-nodejs):`git clone` → `npm install` → `npm run login`(走 Google OAuth,可反复登多个账号)→ `npm start`(默认端口 8045)。
2. `cp proxy_config.example.json proxy_config.json`(或放 `~/.config/gemini-gen/proxy_config.json`,二者择一,前者优先),填入 `base_url`(如 `http://localhost:8045/v1`)和反代 `.env` 里配的 `API_KEY`。
3. 出图前确保反代服务在跑;本机用 `app` 项目管理器的可以 `app run antigravity2api`,没有这套管理器就直接进反代目录 `npm start`。
4. 多账号 / 撞额度自动禁用都在反代服务自己的管理台里管(默认 `http://localhost:8045`,登录 `.env` 里配的 `ADMIN_USERNAME`/`ADMIN_PASSWORD`),本 skill 不重复实现。

**找不到 `proxy_config.json` 时的兜底**:会尝试读本机 `~/.agents/resources.json` 的 `llm.antigravity2api.local`(仅我自己机器上有这个私有凭据库,其他人用本 skill 应该走上面的 `proxy_config.json`,不依赖这个)。

## cookie 后端配置(备选,私密,不入 git)

账号信息抽到 **`accounts.json`**(skill 根目录),格式 `{"members": {"别名": "邮箱", ...}}`。该文件已被 `.gitignore` 挡住、**不进仓库**;仓库里只带模板 `accounts.example.json`。

**首次使用 / 别人拿到 skill**:
1. `cp accounts.example.json accounts.json`(或放 `~/.config/gemini-gen/accounts.json`,二者择一,前者优先)。
2. 填入自己的 Gemini 会员号:`别名 → 该号登录邮箱`。
3. **每个会员号要有独立 Chrome profile(只登它一个号)**——一个 profile 的 cookie 罐只存得下一个 `__Secure-1PSID`(authuser=0),多号混登只能薅到最早那个。
4. 在每个 profile 里打开一次 `gemini.google.com` 确认登录态。

- 账号 → profile 映射靠 Chrome `Local State` 的 email 自动反查;**账号身份以此为准**(Gemini 自报邮箱不可靠,会瞎编)。
- 负载状态(游标 + 冷却)存在 `~/.config/gemini-gen/state.json`。

## 限流与兜底(cookie 后端,重要)

- 这条 cookie 通道有 Google **独立的反自动化限流**,跟手动 UI 通道是两套配额。**低频偶尔出图没问题**;短时间高频(几分钟连发十次)会被软限流,典型回应是 "limit resets" 或 "Are you signed in? ...can't create"。脚本已加 **pacing(请求前随机停顿)+ LRU 分摊 + 撞限流自动跳号冷却** 来压低触线概率,但不能根治——脚本无法把自己伪装成"有人在操作的活浏览器"。
- **被限流时的兜底:回退到 [`browser-gen`] skill**(Chrome MCP 驱动真实浏览器走 UI 通道)。UI 通道信任分高、基本不受这条限流影响;手动能画、它就能画。代价是慢、要开 Chrome、取原图需手点下载。proxy 后端不受这条限流影响(走的是 Antigravity API 通道,不是网页 UI 逆向)。
- 经验法则:**proxy 后端够用就优先用它;cookie 后端撞限流或要"稳出一张" → browser-gen。**

## 边界与坑

- **proxy 后端**:依赖第三方开源反代([liuw1535/antigravity2api-nodejs](https://github.com/liuw1535/antigravity2api-nodejs)),该项目处理好了 Antigravity 官方 API 的 projectId 兜底 + thoughtSignature 透传等坑(自己手搓反代很容易在这两处翻车);出图分辨率档位靠模型名后缀 `-2K`/`-4K`,没有结构化的 `aspectRatio` 参数。
- **cookie 后端**:逆向 web API + cookie,属 Google ToS 灰区;cookie 长期有效(`__Secure-1PSID` 寿命长,`__Secure-1PSIDTS` 运行时自动刷新),但账号在浏览器登出 / 改密会失效;出的是 Nano Banana 图(消费版 web),不保证拿到 4K 原图档位。
- 两条后端额度都是**按账号每日**算的;多号合起来也有上限,撞满了等刷新或再加号。
- **绝不**把任何账号的 cookie / PSID / API key / 真实邮箱写进会提交的文件(SKILL.md / example / 代码)或公开仓库。
