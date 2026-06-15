---
name: browser-gen
description: >-
  Generate images and videos for free by driving the user's already-logged-in
  Gemini (gemini.google.com) Pro account through the Chrome MCP browser tools
  (claude-in-chrome). Use when the user wants browser-gen, 用 Gemini 生图/生视频,
  浏览器生成图片/视频, free image/video generation via Gemini web, Veo video,
  Nano Banana image — a third media-generation route alongside local ComfyUI
  and 即梦/Dreamina. Especially useful for VIDEO (Gemini Veo「制作视频」) since
  local Mac video is too slow and the 即梦 CLI is gated behind maestro vip.
---

# browser-gen —— 用浏览器驱动 Gemini 免费生图/生视频

通过 Chrome MCP（`claude-in-chrome`）操作用户**已登录的 Gemini Pro 账号**（gemini.google.com）来生成图片和视频。会员额度内**免费**，是继本地 ComfyUI、即梦 CLI 之后的第三条媒体生成途径。

## 在三条途径里的定位

| 途径 | 成本 | 图 | 视频 | 何时用 |
|------|------|----|------|--------|
| 本地 ComfyUI | 免费 | ✅ 快 | ❌ Mac 太慢 | 离线、可控、批量图 |
| 即梦/Dreamina CLI | 付费额度 | ✅ | ✅ | **当前账号无 maestro vip，暂不可用** |
| **本 skill（Gemini web）** | 会员额度内免费 | ✅ Nano Banana 2 | ✅ Veo「制作视频」 | **视频首选**；要免费/高质量图也行 |

> 图模型：**Nano Banana 2**。视频：**Veo（菜单叫「制作视频」）**。账号：用户 Chrome 已登录的 Gemini **Pro**（Jiawei Hu）。

## 前置条件

- Chrome MCP 工具可用（`mcp__claude-in-chrome__*`，需先 ToolSearch 加载）。
- 用户的 Chrome 已登录 Gemini（会话复用，无需再登录）。
- **会话开始先调 `tabs_context_mcp`**；按规范**新建一个标签页**给本任务，不要复用用户现有标签页。

## 核心流程（图片，已实测跑通）

1. `tabs_context_mcp` → `tabs_create_mcp` 建新标签页 → `navigate` 到 `https://gemini.google.com/app`（沿用登录态）。
2. 点输入框左侧 **「+」(上传和工具)** → 弹出工具菜单。
3. 菜单里点 **「制作图片」**（视频则点 **「制作视频」**）。进入对应创作视图，输入框出现「图片」/「视频」芯片。
4. **点底部输入框**（占位符「描述你的图片」），**再输入提示词**。
   - ⚠️ 坑：首次点输入区可能触发视图切换（出现风格模板墙），切换瞬间输入的文字会丢——**等视图稳定后，对准底部 composer 再输入**。
5. 点**发送**（蓝色 ↑ 箭头，composer 右下；或回车）。
6. **等待 + 轮询截图**：图片 Nano Banana 2 约 15–30s；视频 Veo 约 **1–3 分钟**。用 `computer wait` + `screenshot` 轮询，看到产物渲染完成为止。
7. 产物渲染在对话流里。**取文件见下。**

提示词写法：Nano Banana / Veo 都吃自然语言整句，描述主体+风格+构图+光照即可；中文英文都行。

## 取产物到磁盘（重要，有坑）

**默认：让用户手动点下载拿原图。**

- 用 `find` 定位按钮 **「下载完整尺寸的图片」**，把图/视频在视图里就位，然后**提示用户亲手点一下那个下载按钮**（落到 Chrome 默认下载目录，通常 `~/Downloads`，原分辨率）。
- ⚠️ **不要让自动化去点下载按钮**：扩展派发的点击 `isTrusted=false`、缺「用户激活」手势，Gemini 的下载（走 File System Access / 手势门控）会被 Chrome 判**失败**；用户亲手点才是可信手势，才成功。这是实测结论。
- **快速预览/自动落地**（非原图）：用 `computer` 的 `screenshot`/`zoom` 配 `save_to_disk: true` 截取图片区域存到可访问路径——只有屏幕分辨率，视频也只能截帧。要原图仍走用户手动下载。

## 视频「制作视频」（流程类推，待逐项验证）

与图片同一套机制：`+` → **「制作视频」** → 输入提示 → 发送 → 轮询（更久，1–3 分钟）→ 产物为视频。取视频同样**让用户点下载**拿原文件（视频无法用截图存整段）。首次实跑时注意核对：视频的发送/等待形态、是否有时长/比例选项、下载按钮文案，并据实更新本节与 `reference/gemini-ui.md`。

## Chrome MCP 操作纪律（来自 MCP 规范）

- 先 `tabs_context_mcp`，每个新会话新建标签页，别复用用户标签页。
- 多步操作用 `browser_batch` 一次发（点+输入+截图），更快。
- 定位元素优先用 `find`（自然语言）拿 ref，比写死坐标稳。
- **绝不触发 JS alert/confirm/prompt 或原生对话框**——会阻塞后续所有浏览器事件。下载若弹"保存到哪"原生框，automation 够不到，交给用户处理。
- 卡住/连续失败 2–3 次就停下问用户，别死循环。

详细 UI 地图（菜单项、按钮、坐标参考、各类坑）见 `reference/gemini-ui.md`。
