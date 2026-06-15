# dreamina CLI 命令参考

源自 `dreamina <子命令> -h`（CLI v1.4.5，2026-06）。**约束随版本变，存疑时以实时 `-h` 为准。** 所有生成命令异步：返回 `submit_id` + `gen_status`，用 `query_result` 取结果。所有生成命令都支持 `--poll=N`（submit 后就地轮询最多 N 秒）和 `--session=<id>`。

## 账号 / 会话 / 查询

```bash
dreamina user_credit                      # 查额度（生成前先看）
dreamina login [--headless]               # OAuth 设备流登录
dreamina login checklogin --device_code=<code> --poll=30
dreamina relogin | logout
dreamina query_result --submit_id=<id> [--download_dir=<目录>]   # 查异步结果并下载
dreamina list_task [--gen_status=success] [--gen_task_type=...] [--limit=20] [--offset=0] [--submit_id=...]
dreamina session create ["名称"] | list [-n 100] | search "名" | rename <id> "名" | delete <id>
```
- session 0 是默认会话，不能改名/删除；删除会话会把历史安全移回默认会话。

## 图像

### text2image —— 文生图
```bash
dreamina text2image --prompt="a cat portrait" --ratio=1:1 --resolution_type=2k [--model_version=4.6]
```
- `model_version`: 3.0, 3.1, 4.0, 4.1, 4.5, 4.6, 4.7, 5.0（省略用默认）
- `ratio`: 21:9, 16:9, 3:2, 4:3, 1:1, 3:4, 2:3, 9:16
- `resolution_type`: 3.0/3.1 → 1k 或 2k；4.0/4.1/4.5/4.6/4.7/5.0 → 2k 或 4k

### image2image —— 图生图 / 改图
```bash
dreamina image2image --images ./a.png,./b.png --prompt="turn into watercolor" [--ratio=1:1 --resolution_type=2k --model_version=5.0]
```
- 输入 **1–10 张**本地图（`--images` 逗号分隔）；`model_version`: 4.0–5.0；`resolution_type`: 2k 或 4k（**不支持 1k**）。

### image_upscale —— 放大
```bash
dreamina image_upscale --image=./input.png --resolution_type=4k
```
- `resolution_type`: 2k（免费）/ 4k / 8k（4k、8k 需 VIP）。

## 视频（本地放弃后的主力）

### text2video —— 文生视频
```bash
dreamina text2video --prompt="a cat running" --duration=5 [--ratio=16:9 --video_resolution=720p --model_version=seedance2.0fast]
```
- `model_version`: seedance2.0, seedance2.0fast(默认), seedance2.0_vip, seedance2.0fast_vip
- `ratio`: 1:1, 3:4, 16:9, 4:3, 9:16, 21:9；`duration`: 4–15s(默认5)
- `video_resolution`: seedance2.0_vip → 720p 或 1080p；其余 → 720p

### image2video —— 单图生视频
```bash
dreamina image2video --image=./first.png --prompt="camera push in" [--duration=5 --video_resolution=720p --model_version=3.5pro]
```
- 基础用法只需 `--image` + `--prompt`；高级控制可设 `--duration/--video_resolution/--model_version`（要成组给合法组合）。
- `model_version`: 3.0, 3.0fast, 3.0pro, 3.5pro, seedance2.0 系；时长范围按模型：3.0系 3–10、3.5pro 4–12、seedance2.0系 4–15。
- ratio 由输入图推断，不在此命令设。

### frames2video —— 首尾帧生视频
```bash
dreamina frames2video --first=./start.png --last=./end.png --prompt="season changes" [--duration=5 --model_version=seedance2.0fast]
```
- `model_version`: 3.0, 3.5pro, seedance2.0 系；时长：3.0 → 3–10，3.5pro → 4–12，seedance2.0 系 → 4–15。ratio 由首帧推断。

### multiframe2video —— 多图智能多帧故事视频
```bash
# 恰好 2 张：用 --prompt + 可选 --duration
dreamina multiframe2video --images ./a.png,./b.png --prompt="character turns around" [--duration=3]
# 3+ 张：每段转场一条 --transition-prompt（N 张给 N-1 条）
dreamina multiframe2video --images ./a.png,./b.png,./c.png \
  --transition-prompt="turn from A to B" --transition-prompt="turn from B to C" \
  [--transition-duration=3 --transition-duration=3]
```
- 输入 2–20 张；N 张 → N-1 段转场；每段时长 [0.5, 8]s，总时长 ≥2。ratio 由首图推断。**不支持** model_version / video_resolution 覆盖。

### multimodal2video —— 旗舰"全能参考"（图+视频+音频）
```bash
dreamina multimodal2video --image ./input.png [--video ./ref.mp4] [--audio ./music.mp3] \
  --prompt="turn into a cinematic shot" --model_version=seedance2.0fast --duration=5 [--ratio=16:9 --video_resolution=720p]
```
- 输入任意组合 `--image`(≤9) / `--video`(≤3) / `--audio`(≤3，音频 2–15s)，至少一个图或视频；本地文件自动上传。
- `model_version`: seedance2.0 系；`duration`: 4–15s。Web 端对应"全能参考"（旧名 ref2video），是当前最强视频模式。

## 通用判定与排错

- **submit 成功** = 有 `submit_id` 且 `gen_status ∈ {querying, success}`；别只看退出码。
- `gen_status=fail` → 看 `fail_reason`。
- `AigcComplianceConfirmationRequired` → 先去即梦 Web 端完成该模型的授权确认，再重试。
- 跑测试扫描时把结果存成机器可读格式，便于后续用 `submit_id` 批量 `query_result`。
