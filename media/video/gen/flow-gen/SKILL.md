---
name: flow-gen
description: >-
  用 Google Flow（flow.google.com）按 Google AI Pro/Ultra 会员的点数生成视频和图片，走用户**真实 Chrome 的登录态**
  （可插拔浏览器通道，默认 kimi-webbridge），不弹新浏览器、不用 API key、不另外花钱。
  视频（Veo 3.1 Lite / Fast / Quality、Omni 1.1 Flash，原片 mp4 带音轨）支持三种输入：文生视频、「帧」（首帧图生视频 / 首尾帧过渡）、
  「素材」（多张参考图：角色 / 物体 / 场景 → 视频）。图片（Nano Banana Pro / 2 / 2 Lite，PRO 档 0 点）支持文生图和参考图生图。
  当用户要「生成视频 / 文生视频 / 图生视频 / 首尾帧 / 参考图做视频 / 让这张图动起来 / 用 Flow / 用 Veo / 薅会员点数做视频 /
  低成本 AI 视频」，或点名要用 Flow / Nano Banana 免费出图时使用。
  与 jimeng（付费 API）、browser-gen（Gemini 网页 Veo，拿不到原片）并列，是会员点数内最省的视频后端；
  通用出图未点名后端时仍由 media-gen 路由。
---

# flow-gen —— Google Flow 会员点数生成视频 / 图片

用户 Chrome 里已登录的 Pro 号在 Flow 里有月度点数，本 skill 把它变成命令行。

```bash
S=~/.claude/skills/flow-gen/scripts; PY=~/.venvs/current/bin/python
$PY $S/flow_gen.py credits                                   # 剩余点数 + 档位（只读）
$PY $S/flow_gen.py models                                    # 当前档位能用的视频 / 图片模型、单价、支持的模式

# 视频（加 --dry-run 只算价不提交）
$PY $S/flow_gen.py gen --prompt "..." --out shot.mp4                                         # 文生视频
$PY $S/flow_gen.py gen --prompt "..." --start-image a.png --out shot.mp4                     # 帧：首帧图生视频
$PY $S/flow_gen.py gen --prompt "..." --start-image a.png --end-image b.png --out shot.mp4   # 帧：首尾帧过渡
$PY $S/flow_gen.py gen --prompt "..." --ref char.png --ref scene.jpg --out shot.mp4          # 素材：参考图生视频
    # 通用参数：[--model lite|fast|quality|omni] [--aspect 16:9|9:16] [--duration 8] [--res 720p|360p] [--count 1-4]

# 图片（PRO 档 0 点）
$PY $S/flow_gen.py image --prompt "..." --out pic.jpg [--model nb2|pro|lite] [--aspect 16:9|4:3|1:1|3:4|9:16] [--count 1-4]
$PY $S/flow_gen.py image --prompt "..." --ref ref.png --out pic.jpg                          # 参考图生图
```

stdout 输出 JSON（`outputs[].path` 为本地文件），进度写 stderr。退出码：0 成功 / 1 没提交（环境或参数问题）/ 2 提交了但有条目失败或超时。
多条 / 多张时 `--out` 作前缀，文件名带序号和 id。图片固定是 JPEG，`--out` 写成 `.png` 会被自动改成 `.jpg`。

## 三种视频输入怎么选

| 模式 | 参数 | 图片的作用 | 适合 |
|---|---|---|---|
| 文生 | 只给 `--prompt` | — | 从零生成 |
| **帧** | `--start-image` [+ `--end-image`] | 原样当第一帧（和最后一帧） | 让一张图动起来；两张图之间做过渡 |
| **素材** | `--ref` 可多次 | 当「演员 / 道具 / 场景」参考，重新构图 | 固定角色在新场景里演；多元素合成 |

「帧」和「素材」不能同时用。素材数量上限按模型：Veo Lite / Fast 最多 3 张，Omni 最多 7 张；Quality 不支持素材模式。

## 选模型与花费（2026-09 实测 PRO 档，实时以 `models` 为准）

| 视频 `--model` | 模型 | 点数 / 条 | 说明 |
|---|---|---|---|
| `lite`（默认） | Veo 3.1 - Lite | 10（8s，720p） | 性价比默认，三种模式都支持 |
| `fast` | Veo 3.1 - Fast | 20（8s） | 质量更好 |
| `quality` | Veo 3.1 - Quality | 100（8s） | 贵，重要镜头才用；不支持素材 |
| `omni` | Omni 1.1 Flash | 4/6/8/10s = 7/10/12/15；`--res 360p` 4/5/6/7 | 可选时长，360p 最省 |

| 图片 `--model` | 模型 | 点数 |
|---|---|---|
| `nb2`（默认） | Nano Banana 2 | 0 |
| `pro` | Nano Banana Pro | 0 |
| `lite` | Nano Banana 2 Lite | 0 |

模型、价格、时长、素材上限全部从 Flow 服务端下发的清单实时读取（`catalog.py`），Google 调价或加模型不用改代码。**视频真跑前把点数告诉用户**；大批量先 `--dry-run`。

## 前置条件

- 浏览器通道可用。默认 `kimi`：kimi-webbridge daemon + Chrome 扩展（脚本会自动 `start` daemon、从 `kimi-webbridge status` 读端口；stop / restart / upgrade 不自动做，daemon 与扩展版本不一致时提示用户自己跑 `kimi-webbridge upgrade`）。扩展装在哪个 Chrome 个人资料，就用哪个账号——该资料需已登录 Flow 且是 Pro/Ultra。
- 换通道：`--bridge <名>` 或环境变量 `FLOW_GEN_BRIDGE`。
- 第一次运行会在 Chrome 里开一个「Flow 视频生成」标签页组，之后复用（每次开始都会重新载入项目页）；项目 id 记在 `~/.config/flow-gen/state.json`（`--project` 可指定）。运行期间标签页被设成「前台节奏」（焦点模拟），但不会切走用户正在看的页面，结束后还原。
- **上传图片的使用权确认**：Flow 首次上传图片时会弹「此图片的使用权」声明（确认你对图片拥有必要权利）。默认遇到就停下报错、不自动同意；用户确认后加 `--agree-rights`（或设 `FLOW_GEN_AGREE_RIGHTS=1`）。实测该声明同一账号只弹一次。

## 工作原理（改代码前必读）

| 步骤 | 做法 | 为什么 |
|---|---|---|
| 读点数 / 清单 / 进度 / 下载地址 | 页面里直接调 batchexecute RPC（`nzlxg` / `HTrJv` / `jwpduf` / `as29s`） | 只读接口，不需要人机验证 |
| 设参数 | 页面输入框的设置面板：图片/视频 → 帧/素材 → 模型 → 比例 → 时长 → 分辨率 → 条数 | 读回面板显示的点数，和清单算的对不上就不提交 |
| 放图 | 点首/尾帧格子或「+ 添加素材」→ 拦下系统文件对话框 → 通道 `upload` 塞文件 → 按**唯一文件名**点选 → 核对输入框里缩略图的 mediaId | 选择框会保留上次选中的旧图，直接点「添加到提示」会加错图（踩过，白花 10 点） |
| **提交** | 通道对「生成」按钮发**真实鼠标点击**（`click_at`），抓 batchexecute 里「请求体含预期 modelKey」的那条拿结果 | 出图按钮只认真实点击；提交 RPC id 因模式而异（文生 `YhhmEf` / 首帧 `eb1hJf` / 出图 `ogiZ0b`），所以不写死 |
| 下载 | `flow-content.google/{video,image}/...` 签名地址，无需 cookie 直接下 | 签名约 6 小时有效 |

**⚠️ reCAPTCHA 陷阱（别踩）**：Flow 启动时把原版 `grecaptcha.enterprise.execute` 藏进闭包自用，再把公开的那个换成包装——任何外部调用拿到的令牌 action 都被改成 `extension_hijack_detected`，提交会被拒 `PUBLIC_ERROR_UNUSUAL_ACTIVITY`（不扣点数）。所以**不要自己拼提交请求 / 自己取令牌，也不要尝试绕过它**（主动对抗反作弊 = 封号风险），一律让页面自己提交。

**其他踩过的坑**：
- 后台标签页的定时器会被 Chrome 节流到 1 次/秒甚至 1 次/分钟，页面脚本里的等待会拖成几分钟 → 运行期间开焦点模拟（`set_foreground`）。
- 设置面板不认 Escape，要再点一次设置按钮收起；弹窗没关干净时点别的按钮只会先关弹窗。
- 顶栏和输入框各有一个 `add` 图标按钮，「添加素材」要排除顶栏那个（`aria-haspopup="menu"`）。
- 出图响应里的条目长度不固定，图片地址按前缀搜，不按固定下标取。

## 文件职责

| 文件 | 职责 |
|---|---|
| `scripts/flow_gen.py` | CLI：参数解析、模式推断、编排、轮询 |
| `scripts/flow_session.py` | 标签页生命周期、注入页面脚本、设参数 / 放图 / 真实点击提交 / 抓包取结果（只经 `BrowserBridge` 接口） |
| `scripts/flow_page.js` | 页面侧：只读 RPC + 输入框操作（按图标名 / aria 定位，不依赖界面语言） |
| `scripts/catalog.py` | 纯函数：解析模型清单，挑视频 / 图片模型的 modelKey、单价、素材上限 |
| `scripts/outputs.py` | 输出文件命名、下载、按文件头纠正扩展名 |
| `scripts/bridges/base.py` | `BrowserBridge` 接口：开标签页 / 前台节奏 / 跳转 / 执行 JS / 真实点击 / 填输入框 / 上传文件 / 抓包 |
| `scripts/bridges/kimi.py` | kimi-webbridge 实现（daemon HTTP + 端口发现 + CDP） |
| `scripts/bridges/__init__.py` | 通道注册表：`get_bridge()`；新通道 = 写一个子类 + 在 `_REGISTRY` 加一行 |

## 完成度（诚实标，2026-09-30）

- ✅ 文生视频：`lite` 16:9（1280×720）、`omni` 9:16 4s 360p、`omni` 16:9 4s 360p。
- ✅ 帧：首帧图生视频 `lite` 9:16（720×1280，首帧与原图一致）；首尾帧 `lite` 16:9（首尾帧都与原图一致）。
- ✅ 素材：`lite` 2 张参考图（角色 + 场景）合成，16:9。
- ✅ 出图：`nb2` 16:9、1:1 ×2；参考图生图 1:1（角色细节保留）。
- ⏳ `fast` / `quality` 视频、视频 `--count>1`、`pro` / `lite` 出图、图片放大（2K 对 PRO 免费）尚未真跑 / 未接入。
- ⏳ 素材里的「角色 / 虚拟形象 / 语音」等 Flow 内建资产还不能选，只支持上传本地图片。

## 常见问题

- `Flow 页面没准备好`：Chrome 没开、扩展没连、或该资料没登录 Flow。
- `页面显示 X 点…对不上`：Flow 改版或清单结构变了，先 `models` 看清单，再对照页面设置面板。
- `找不到选项 / 找不到生成设置按钮 / 图片选择框没打开`：Flow 界面改版，修 `flow_page.js` 里的定位函数。
- `Flow 要求确认「你对上传图片拥有必要权利」`：跟用户确认后加 `--agree-rights`。
- 视频生成失败 `code` 非 3 / 出图张数少于 `--count`：多为内容安全拦截，换个提示词（避免真人名、版权 IP）。
- 风险：这是非官方自动化，违反 Flow 服务条款，存在账号被限制的可能；低频自用为宜。
