---
name: flow-gen
description: >-
  用 Google Flow（flow.google.com）按 Google AI Pro/Ultra 会员每月送的点数生成视频（Veo 3.1 Lite / Fast / Quality、Omni 1.1 Flash），
  走用户**真实 Chrome 的登录态**（可插拔浏览器通道，默认 kimi-webbridge），不弹新浏览器、不用 API key、不另外花钱。一条命令：设参数 → 页面自己提交 → 轮询 → 下载原片 mp4（带音轨）。
  当用户要「生成视频 / 文生视频 / 用 Flow / 用 Veo / 薅会员点数做视频 / 低成本 AI 视频」时使用。
  与 jimeng（付费 API）、browser-gen（Gemini 网页 Veo，拿不到原片）并列，是会员点数内最省的视频后端。
---

# flow-gen —— Google Flow 会员点数生成视频

用户 Chrome 里已登录的 Pro 号在 Flow 里有月度点数，本 skill 把它变成一条命令。

```bash
S=~/.claude/skills/flow-gen/scripts
~/.venvs/current/bin/python $S/flow_gen.py credits                 # 剩余点数 + 档位（只读，不花点数）
~/.venvs/current/bin/python $S/flow_gen.py models                  # 当前档位能用的文生视频模型 + 单价
~/.venvs/current/bin/python $S/flow_gen.py gen --prompt "..." --out ./shot.mp4 --dry-run   # 只算价不提交
~/.venvs/current/bin/python $S/flow_gen.py gen --prompt "..." --out ./shot.mp4 \
    [--model lite|fast|quality|omni] [--aspect 16:9|9:16] [--duration 8] [--res 720p|360p] [--count 1-4]
```

stdout 输出 JSON（`outputs[].path` 为本地 mp4），进度写 stderr。退出码：0 成功 / 1 没提交（环境或参数问题）/ 2 提交了但有条目失败或超时。

## 前置条件

- 浏览器通道可用。默认 `kimi`：kimi-webbridge daemon + Chrome 扩展（脚本会自动 `start` daemon、从 `kimi-webbridge status` 读端口；stop / restart / upgrade 不自动做，daemon 与扩展版本不一致时提示用户自己跑 `kimi-webbridge upgrade`）。扩展装在哪个 Chrome 个人资料，就用哪个账号——该资料需已登录 Flow 且是 Pro/Ultra。
- 换通道：`--bridge <名>` 或环境变量 `FLOW_GEN_BRIDGE`。
- 第一次运行会在 Chrome 里开一个「Flow 视频生成」标签页组，之后复用；项目 id 记在 `~/.config/flow-gen/state.json`（`--project` 可指定）。

## 选模型与花费（2026-09 实测 PRO 档，实时以 `models` 为准）

| `--model` | 模型 | 点数 / 条 | 说明 |
|---|---|---|---|
| `lite`（默认） | Veo 3.1 - Lite | 10（8s，720p） | 性价比默认 |
| `fast` | Veo 3.1 - Fast | 20（8s） | 质量更好 |
| `quality` | Veo 3.1 - Quality | 100（8s） | 贵，重要镜头才用 |
| `omni` | Omni 1.1 Flash | 4s/6s/8s/10s = 7/10/12/15；`--res 360p` 4/5/6/7 | 可选时长，360p 最省 |

模型、价格、可选时长全部从 Flow 服务端下发的清单实时读取（`catalog.py`），Google 调价或加模型不用改代码。**真跑前把点数告诉用户**；大批量先 `--dry-run`。

## 工作原理（改代码前必读）

| 步骤 | 做法 | 为什么 |
|---|---|---|
| 读点数 / 清单 / 进度 / 下载地址 | 页面里直接调 batchexecute RPC（`nzlxg` / `HTrJv` / `jwpduf` / `as29s`） | 只读接口，不需要人机验证 |
| **提交生成** | 在页面输入框里设好参数、填提示词、点「生成」，用 webbridge 抓 `YhhmEf` 的响应拿 mediaId | 见下方陷阱 |
| 下载 | `flow-content.google/video/...` 签名地址，无需 cookie 直接下 | 签名约 6 小时有效 |

**⚠️ reCAPTCHA 陷阱（别踩）**：Flow 启动时把原版 `grecaptcha.enterprise.execute` 藏进闭包自用，再把公开的那个换成包装——任何外部调用拿到的令牌 action 都被改成 `extension_hijack_detected`，提交会被拒 `PUBLIC_ERROR_UNUSUAL_ACTIVITY`（不扣点数）。所以**不要自己拼提交请求 / 自己取令牌，也不要尝试绕过它**（主动对抗反作弊 = 封号风险），一律让页面自己提交。

提交前有两道校验：页面显示的点数必须等于清单算出的点数，抓到的请求体里必须是预期的 modelKey，否则中止并报错。

## 文件职责

| 文件 | 职责 |
|---|---|
| `scripts/flow_gen.py` | CLI：参数解析、编排、轮询、下载 |
| `scripts/flow_session.py` | 标签页生命周期、注入页面脚本、UI 提交 + 抓包（只经 `BrowserBridge` 接口） |
| `scripts/flow_page.js` | 页面侧：只读 RPC + 输入框操作（按图标名 / aria 定位，不依赖界面语言） |
| `scripts/catalog.py` | 纯函数：解析模型清单，按系列 / 比例 / 时长 / 分辨率 / 档位挑 modelKey 和单价 |
| `scripts/bridges/base.py` | `BrowserBridge` 接口：开标签页 / 跳转 / 执行 JS / 填输入框 / 抓包 |
| `scripts/bridges/kimi.py` | kimi-webbridge 实现（daemon HTTP + 端口发现） |
| `scripts/bridges/__init__.py` | 通道注册表：`get_bridge()`；新通道 = 写一个子类 + 在 `_REGISTRY` 加一行 |

## 完成度（诚实标）

- ✅ 真跑通：`lite` 文生视频 16:9（1280×720，8s，h264+aac，约 1 分钟出片）。
- ✅ 真跑通：`omni` 文生视频 9:16 / 4s / 360p（360×640，带音轨，4 点）。
- ⏳ `fast` / `quality` / `--count>1` 走同一路径，尚未真跑。
- ⏳ 未做：图生视频 / 首尾帧 / 参考图（需要先抓图片上传的 RPC）；Flow 出图（界面显示 0 点数，可作为免费出图后端，待接入）。

## 常见问题

- `Flow 页面没准备好`：Chrome 没开、扩展没连、或该资料没登录 Flow。
- `页面显示 X 点…对不上`：Flow 改版或清单结构变了，先 `models` 看清单，再对照页面设置面板。
- `找不到选项 / 找不到生成设置按钮`：Flow 界面改版，修 `flow_page.js` 里的定位函数。
- 生成失败 `code` 非 3：多为内容安全拦截，换个提示词（避免真人名、版权 IP）。
- 风险：这是非官方自动化，违反 Flow 服务条款，存在账号被限制的可能；低频自用为宜。
