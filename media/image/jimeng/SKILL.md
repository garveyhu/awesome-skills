---
name: jimeng
description: >-
  Generate images and videos via 即梦 / Dreamina cloud (ByteDance) using the
  local `dreamina` CLI. Use when the user wants 即梦/Dreamina generation, or
  wants cloud media generation as an alternative to local ComfyUI — especially
  for VIDEO (text2video, image2video, multi-frame story video, Seedance 2.0
  flagship), or high-quality cloud images, when local ComfyUI/MPS is too slow.
  Triggers: 即梦, dreamina, 用即梦生成, 云端生图/生视频, 文生视频, 图生视频,
  seedance, 全能参考. Generation consumes account credits (paid) and needs login.
---

# 即梦 / Dreamina 云端生成 skill

通过官方 `dreamina` CLI 调用即梦云端做图片/视频生成。**与本地 ComfyUI 并列**，是另一条媒体生成途径——可自由选择本地 ComfyUI 还是云端即梦。

即梦 = Dreamina 的中文名。用户说"即梦"即指 Dreamina。

## ComfyUI 还是 即梦？——选型决策

| 维度 | 本地 ComfyUI | 云端 即梦/Dreamina |
|------|-------------|-------------------|
| 成本 | 免费（本地算力） | **消耗账号额度（付费）** |
| 文生图 | ✅ 快够用（Z-Image Turbo） | ✅ 质量高、模型多(3.0–5.0) |
| **视频** | ❌ Mac/MPS 极慢，已放弃 | ✅✅ **首选**（text2video / image2video / 多帧故事 / Seedance 2.0） |
| 速度 | 图够快，视频不可用 | 云端快，异步出结果 |
| 控制力 | 高（自定义工作流/LoRA/ControlNet） | 中（按 CLI 暴露的参数） |
| 隐私/离线 | ✅ 全本地 | ❌ 上传云端，需联网+登录 |

**默认策略**（除非用户另有要求）：
- **图片** → 优先本地 ComfyUI（免费、够快）；要更高质量/特定即梦模型时用即梦。
- **视频** → 用即梦（本地已放弃）。
- 用户明确点名"用即梦/用 comfyui"时按其指定走。

> 跨工具流水线很常见：用 ComfyUI（或即梦）出图 → 把图喂给即梦 `image2video`/`multiframe2video` 生成视频。

## 前置条件

- CLI 已装：`~/.local/bin/dreamina`（已在 PATH，直接 `dreamina`）。版本 `dreamina version`。
- **必须登录**（OAuth 设备流，需用户用抖音/即梦账号授权）——见下。
- **⚠️ 账号需 maestro vip 权限**：CLI（`dreamina_cli_beta`）的生成能力**仅对 maestro vip 账号开放**。普通 `standard` 账号登录/查额度正常，但任何生成命令都会被拦：`当前账号没有 dreamina_cli 使用权限: current account is not maestro vip`（不扣额度）。遇到此错就是账号等级不够，需先在即梦侧获取该权限（升级/白名单），非本 skill 可解。生成前可先确认账号具备权限。
- **生成消耗额度**，跑真任务前先 `dreamina user_credit` 看余额，并提醒用户。

## 登录流程（需用户参与）

未登录时任何生成/账号命令都会提示 `未检测到有效登录态`。登录用 OAuth 设备流：

```bash
dreamina login
```

它会打印 `verification_uri` + `user_code` + `device_code`，并等待授权完成。**告诉用户：打开那个 URL、输入 user_code、用抖音 App 授权**。完成后本地保存会话，后续复用。

- 非阻塞式：`dreamina login --headless` 打印授权材料后退出，再 `dreamina login checklogin --device_code=<code> --poll=30` 轮询确认。
- 复用：`dreamina login` 在会话仍有效时直接复用，不会重复要求授权。
- 重登/登出：`dreamina relogin` / `dreamina logout`。

## 核心异步流程（所有生成命令）

生成是**异步**的：submit 拿到 `submit_id`，再查结果。

1. 跑生成命令（如 `dreamina text2video --prompt="..."`）。
2. **判断 submit 成功**：看 `submit_id` 存在 且 `gen_status` 为 `querying` 或 `success`（**别只看 shell 退出码**）。`gen_status=fail` 时读 `fail_reason` 告诉用户具体原因。
3. 若 `querying`：记下 `submit_id`，用 `dreamina query_result --submit_id=<id> --download_dir=<目录>` 查询并把成品下载到本地。
4. 也可加 `--poll=N`（生成命令自带）：submit 后就地轮询最多 N 秒，省一步。
5. `dreamina list_task [--gen_status=success]` 批量回看历史任务。

**产物落地**：`query_result --download_dir=<目录>` 会把结果媒体下载下来；之后用 Read 工具把图/视频路径展示给用户确认。

## 命令速查（详细参数见 reference/commands.md，或随时 `dreamina <子命令> -h`）

| 命令 | 用途 |
|------|------|
| `text2image` | 文生图（模型 3.0–5.0，ratio，1k/2k/4k） |
| `image2image` | 图生图/改图（1–10 张输入，2k/4k） |
| `image_upscale` | 放大（2k 免费，4k/8k 需 VIP） |
| `text2video` | 文生视频（Seedance 2.0 系，4–15s） |
| `image2video` | 单图生视频 |
| `frames2video` | 首尾帧生视频 |
| `multiframe2video` | 多图(2–20)智能多帧故事视频 |
| `multimodal2video` | 旗舰"全能参考"（图+视频+音频混合参考，Seedance 2.0） |
| `query_result` / `list_task` | 查异步结果 / 列历史 |
| `session` | 会话管理（生成命令可 `--session=<id>` 归类） |
| `user_credit` | 查额度 |

## 模型选择规则（别写死）

- 模型版本、ratio、时长、分辨率的**支持组合随命令不同**——用前先 `dreamina <子命令> -h` 核对。
- **Seedance 2.0 系是旗舰视频模型**，质量最好但可能受容量限制、更耗额度。**用户重速度时不要默认上 seedance2.0**，除非明确要最高质量。视频默认 `seedance2.0fast`。

## 重要提醒

- **付费**：每次生成消耗额度，真跑前 `user_credit` 看余额并知会用户；优先小批量、可复核。
- **合规授权**：部分高内容安全风险模型首次用需先在即梦 Web 端授权。若返回 `AigcComplianceConfirmationRequired`，让用户先去网页完成授权再重试。
- **记录**：每个付费任务记下命令/参数/`submit_id`/最终状态，便于追溯。
- 官方精简版 skill 在 `~/.dreamina_cli/dreamina/SKILL.md`，本 skill 是其增强（加了选型决策、落地流程、Mac 上下文）。
