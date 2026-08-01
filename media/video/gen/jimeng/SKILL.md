---
name: jimeng
description: >-
  即梦 / Dreamina（字节）图像 + 视频生成。**优先用 API**——AK/SK 直连火山 visual API（封装在
  `scripts/jimeng_api.py`），**不需要 maestro vip**（区别于 dreamina CLI，CLI 普通账号被拦）。能力栈:
  绘图（文生图 4.0 主力 / 2.1 手绘温度 / 图生图 3.0 智能参考）、P图（4.6 改背景改图 / inpaint 局部重绘消除笔）、
  视频（3.0Pro 文生/图生视频 1080P）、**动作模仿（角色图 + 模板视频 → 驱动角色按动作/表情/口型动起来，IP 动画神器）**。
  CLI（`dreamina`）作备选（需 maestro vip + 登录）。Triggers: 即梦, dreamina, 用即梦生成, 云端生图/生视频,
  文生图, 图生图, P图/改图, 局部重绘/消除, 文生视频, 图生视频, 动作模仿, 让图/IP 动起来, IP 动画, seedream, seedance,
  全能参考。通用生图无指定后端时 `media-gen` 路由;点名即梦/要它的视频·P图·动作模仿时直调本 skill。
---

# 即梦 / Dreamina 生成 skill（API 优先）

即梦 = Dreamina 中文名。两条通路,**默认走 API**:

| | **① API（火山 visual·首选）** | ② CLI（`dreamina`·备选） |
|---|---|---|
| 鉴权 | AK/SK 签名(`resources.json` 已存),**不需要 vip** | OAuth 登录 + **必须 maestro vip**(普通账号被拦) |
| 依赖 | 零(自写 V4 签名,标准库) | 装 CLI + 登录态 |
| 覆盖 | 绘图/P图/局部重绘/视频/动作模仿(见下) | 更全(放大/多帧故事/全能参考/多模态) |
| 何时用 | **默认**——账号没 vip 也能跑 | 账号有 vip 且要 CLI 独有能力时 |

> 火山 API 的 AK/SK 在 `~/.agents/resources.json` 的 `media_generation.volcengine.personal`（脚本自动读）。**生成消耗额度(付费)**,真跑前知会用户。

## ① API 用法（`scripts/jimeng_api.py`）

统一入口,一个脚本跑所有能力。`python scripts/jimeng_api.py --model <model> ...`

| model | 能力 | 关键参数 |
|---|---|---|
| **`t2i-4.0`** | 文生图 4.0(主力·4K·干净矢量风) | `--prompt --out [--width 2048 --height 2048]` |
| `t2i-2.1` | 文生图 2.1(手绘软萌温度好,质量一般) | `--prompt --out` |
| `i2i-3.0` | 图生图 3.0 智能参考(**喂基准图保一致,做变体/表情首选**) | `--prompt --ref base.png [--scale 0.45]` |
| `edit-4.6` | 4.6 Seedream P图(改背景/重绘整体) | `--prompt --img-urls https://图` |
| `inpaint` | 局部重绘 / 消除笔(消除场景 prompt 传"删除") | `--prompt --img-urls "原图URL,maskURL"` |
| `video-1080p` | **文生视频** 1080P(0.63元/秒·性价比) | `--prompt --out o.mp4 [--frames 121=5s\|241=10s --aspect 16:9]` |
| `video-3.0pro` | 文生+**图生视频** 1080P(1元/秒) | 同上;图生加 `--ref first.png`(720P 0.28元最省但 req_key 待确认) |
| **`actor`** | **动作模仿 2.0**(角色图+模板视频→驱动角色动·**IP 动画神器**) | `--img-urls https://角色图 --video-url https://模板视频 --out o.mp4` |
| `actor-m1` | 动作模仿 1.0(备选) | 同上 |
| `upscale` | **智能超清放大**→4K/8K | `--ref low.png --out hi.png [--resolution 4k\|8k --scale 50]` |

**输入图怎么传**:
- `t2i`/`i2i`/视频首帧 → 本地图 `--ref x.png`(脚本自动转 base64)。
- `edit-4.6`/`inpaint`/`actor` → **公网 URL** `--img-urls https://...`(火山只收 URL)。本地图先传公网:用个人 CDN(`~/.claude/rules/cdn-publish.md`)或火山 TOS,拿到 URL 再喂。

**坑(脚本已处理/需注意)**:
- prompt **禁版权 IP 名**(吉卜力/魔女宅急便/吉吉…)→ `50413 文本风控`,改纯特征描述。
- `50400` = 该 req_key 账号没开通(去火山控制台开)；`50200` = req_key 名错；`50500/50429` = 可重试(脚本轮询自动重试)。
- 异步 model(4.0/4.6/inpaint/视频/actor)走 submit→轮询,脚本内置。同步(2.1/3.0)直接返回。
- req_key 实测:`jimeng_high_aes_general_v21_L`(2.1) · `jimeng_i2i_v30`(3.0) · `jimeng_t2i_v40`(4.0) · `jimeng_seedream46_cvtob`(4.6) · `jimeng_image2image_dream_inpaint`(inpaint) · `jimeng_ti2v_v30_pro`(视频3.0Pro) · `jimeng_dreamactor_m20_gen_video`(动作模仿2.0)。

**官方 SDK(可选替代自写签名)**:`pip install volcengine` → `VisualService().set_ak/sk()` + `.cv_sync2async_submit_task(form)`。本 skill 默认用自写 V4 签名(零依赖、已验证),要换 SDK 时按官方示例改。

### 🎬 IP 动画方案(动作模仿)

频道 IP(读 `card.json` 的 `brand.ip`·如某个手绘吉祥物)要在视频里动起来,**最省的路子就是 `actor`**:把 IP 定妆图 + 一段动作模板视频(招手/点头/比心)喂进去 → 直接驱动该 IP 做同款动作,保手绘质感、不用拆骨骼。比 Live2D/Rive 轻太多。

## ② CLI 备选（`dreamina`·需 maestro vip）

账号有 maestro vip 时可用 CLI(能力更全:`image_upscale` 放大 / `multiframe2video` 多帧故事 / `multimodal2video` 全能参考 / `seedance2.0` 旗舰视频)。登录、异步流程、命令速查见 `reference/commands.md`。**普通账号会被拦** `current account is not maestro vip`——此时回 API。

## 重要提醒

- **付费**:每次生成消耗额度,优先小批量、可复核;真跑前知会用户。
- **合规**:返回 `AigcComplianceConfirmationRequired` → 先去即梦 Web 端授权该模型再重试。
- **记录**:付费任务记下 model/参数/task_id/状态,便于追溯。
