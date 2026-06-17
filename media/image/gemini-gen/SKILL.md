---
name: gemini-gen
description: 用 Gemini 会员号(Nano Banana)生成图片,多账号 cookie 隔离 + 负载均衡 + 撞额度自动跳号。当用户要用 Gemini / Nano Banana 出图、"用 gemini 会员画图"、想薅 Gemini Pro/Advanced 订阅免费图额度、或要在多个 Gemini 会员号之间轮着出图分摊额度时使用。经逆向的 Gemini web API(gemini-webapi)走浏览器 cookie,不用 API key、不用浏览器自动化;产物存 PNG,支持参考图。是继 codex-image-gen / comfyui / jimeng / browser-gen 之后的又一条出图后端。
---

# Gemini 会员号生图(多账号负载均衡)

借用本机 Chrome 里已登录的 **Gemini 会员号**(Pro/Advanced),经逆向 web API([`gemini-webapi`](https://github.com/HanaokaYuzu/Gemini-API))读浏览器 cookie 出图(**Nano Banana**),会员额度内免费。相比 `browser-gen` 走浏览器点界面,这条是**纯 cookie + API,不开浏览器自动化**,更快更稳。

## 何时用

- 用户点名要 **Gemini / Nano Banana** 出图,或"用 gemini 会员画图"。
- 想**薅 Gemini 订阅的免费图额度**,而不是走付费 API / 本地算力。
- 有**多个 Gemini 会员号**,想轮着用分摊每日图额度(本 skill 核心卖点)。
- 单账号额度撞墙时想**自动切到下一个号**继续出。

> 出图后端选择:本地可控批量 → `comfyui`;订阅 gpt-image → `codex-image-gen`;Gemini 会员号 → 本 skill;要 Veo 视频 → `browser-gen`。

## 怎么用

单脚本调用(已可执行,依赖经 uv 自动注入,首次稍慢):

```bash
bash ~/.claude/skills/gemini-gen/scripts/gen-image.sh \
  --prompt "画面的具体描述" \
  --out "目标路径/名字.png" \
  [--account <账号别名>] \
  [--aspect 16:9] \
  [--ref 参考图1.png] [--ref 参考图2.png]
```

- 账号别名来自 `accounts.json`(见下「账号配置」),`--account` 取其中的 key。
- 成功后把最终 PNG 路径打到 **stdout**;失败退出码非零,过程信息走 stderr。
- **不传 `--account` = 全部号轮询负载**:按游标轮转,撞到 "limit resets" 自动跳下一个号,出图成功的号记游标、撞墙的号进冷却(默认 2h)。
- 多张图就多次调用(负载会自动把请求摊到不同号上)。

### 参数

| 参数 | 说明 |
|------|------|
| `--prompt` | 必填。主体 + 风格 + 构图 + 背景 + 配色 + 留白,越具体越好;中英文均可,英文更稳。 |
| `--out` | 必填。保存路径,父目录自动建;一次返回多图时自动加 `_0` / `_1`。 |
| `--account` | 可选。**指定某个会员号**(不跳号);不传则负载均衡。 |
| `--model` | 可选。`flash`(默认,Nano Banana 2,额度宽/快) / `pro`(Nano Banana Pro,更高质量但额度紧)。 |
| `--aspect` | 可选。宽高比提示 `16:9` / `1:1` / `9:16` 等(best-effort,写进提示词)。 |
| `--ref` | 可选,可重复。参考图,**做系列图锁角色 / 画风时务必带**。 |

> ⚠️ **模型坑(已踩平)**:`gemini-webapi` 的默认模型(UNSPECIFIED)会路由到一个图额度极小的桶,几张就报 "limit resets" **假性满额**——但账号其实没满(手动在网页用 Flash 能出)。本 skill 已强制走 `flash`/`pro`,**绝不**用默认模型。

## 账号配置(私密,不入 git)

账号信息抽到 **`accounts.json`**(skill 根目录),格式 `{"members": {"别名": "邮箱", ...}}`。该文件已被 `.gitignore` 挡住、**不进仓库**;仓库里只带模板 `accounts.example.json`。

**首次使用 / 别人拿到 skill**:
1. `cp accounts.example.json accounts.json`(或放 `~/.config/gemini-gen/accounts.json`,二者择一,前者优先)。
2. 填入自己的 Gemini 会员号:`别名 → 该号登录邮箱`。
3. **每个会员号要有独立 Chrome profile(只登它一个号)**——一个 profile 的 cookie 罐只存得下一个 `__Secure-1PSID`(authuser=0),多号混登只能薅到最早那个。
4. 在每个 profile 里打开一次 `gemini.google.com` 确认登录态。

- 账号 → profile 映射靠 Chrome `Local State` 的 email 自动反查;**账号身份以此为准**(Gemini 自报邮箱不可靠,会瞎编)。
- 负载状态(游标 + 冷却)存在 `~/.config/gemini-gen/state.json`。

## 限流与兜底(重要)

- 这条 cookie 通道有 Google **独立的反自动化限流**,跟手动 UI 通道是两套配额。**低频偶尔出图没问题**;短时间高频(几分钟连发十次)会被软限流,典型回应是 "limit resets" 或 "Are you signed in? ...can't create"。脚本已加 **pacing(请求前随机停顿)+ LRU 分摊 + 撞限流自动跳号冷却** 来压低触线概率,但不能根治——脚本无法把自己伪装成"有人在操作的活浏览器"。
- **被限流时的兜底:回退到 [`browser-gen`] skill**(Chrome MCP 驱动真实浏览器走 UI 通道)。UI 通道信任分高、基本不受这条限流影响;手动能画、它就能画。代价是慢、要开 Chrome、取原图需手点下载。
- 经验法则:**日常 / 批量低频 → 本 skill(快);本 skill 撞限流或要"稳出一张" → browser-gen。**

## 边界与坑

- **逆向 web API + cookie**,属 Google ToS 灰区;cookie 长期有效(`__Secure-1PSID` 寿命长,`__Secure-1PSIDTS` 运行时自动刷新),但账号在浏览器登出 / 改密会失效。
- 额度是**按账号每日**算的;多号合起来也有上限,撞满了等刷新或再加号。
- 出的是 Nano Banana 图(消费版 web),不保证拿到 4K 原图档位;要极致分辨率走付费 API。
- **绝不**把任何号的 cookie / PSID / 真实邮箱写进会提交的文件(SKILL.md / example / 代码)或公开仓库。
