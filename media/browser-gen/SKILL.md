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

## ⚠️ Token 纪律（第一原则）

**全程不用 `screenshot`**——它是唯一烧 image token 的操作（每张 ~1–1.5k token）。
- 检测 / 等待 / 抓图 / 下载 → 全走 **`javascript_tool`**（纯文本结果）。
- 定位元素 → `find`（自然语言，文本结果）。
- 可信输入（打字 / 回车）→ `computer` 的 `type` / `key` / `left_click`——**这些是廉价文本结果，不烧 token**，只有 `screenshot` 烧。
- 最终图 → 直接 `Read` 磁盘上的 PNG（这一张是交付物，值）。
- `screenshot` 仅在**卡住排障**时用一次，正常流程零截图。

成本对比：旧流程 ~10 次调用含 5–6 张轮询截图；新流程 ~4 次 MCP + 1 次 JS + 1 bash + 1 Read，**零轮询截图**，单图 token 砍 ~80%。

## 核心流程（图片 · 低 token，JS 驱动）

1. `tabs_context_mcp` → `tabs_create_mcp` 新标签页 → `navigate` 到 **登录着的账号** `https://gemini.google.com/u/N/app`。
   - ⚠️ **`/app`(authuser-0)可能是登出态**——主 Chrome 多号混登时 authuser-0 常没登录。先确认该 `/u/N/` 登录了(右上不是「登录」按钮、有账号头像);可一发 JS 读 `[...document.querySelectorAll('[aria-label]')].map(e=>e.getAttribute('aria-label')).filter(a=>a&&a.includes('@'))` 确认是哪个号。
   - **每次新会话用新 chat**,保证页面唯一大图就是这次生成的。
2. `find "message input composer 问问 Gemini"` 拿 composer 的 ref → `computer left_click` ref → `computer type` 提示词。
   - **直接整句提示词走 inline 出图**（消费版 App 自己会出图），不用点「+」→「制作图片」菜单。
   - 输入务必用 `computer type`（可信，Angular 能认）；**别用 JS 设值**（框架可能不认 → 发送空）。
3. `computer key "Meta+Enter"` 发送（或 `find` 发送键再 `computer left_click`）。
4. **等出图，用「短轮询」——别用单发长 await 的 JS**。
   - ⚠️ 坑（实测）：后台标签页 `setTimeout` 被节流，单发 JS 里 `await sleep` 30s 会被拉长，**撞 `javascript_tool` 的 CDP ~45s 超时**而失败。所以**轮询要拆成多发短 JS**（每发秒回，不撞超时）。
   - `computer wait 10`（廉价）给首轮生成时间，再一发**瞬时检查**（秒回）：

     ```js
     (() => {
       const i = [...document.querySelectorAll('img')]
         .filter(x => x.naturalWidth > 200 && x.naturalHeight > 200).pop();
       const t = document.body.innerText;
       return i ? ('IMG ' + i.naturalWidth + 'x' + i.naturalHeight)
         : (/limit|reset|can't create|signed out|went wrong|error/i.test(t) ? 'FAIL' : 'WAIT');
     })()
     ```
   - `WAIT` → `computer wait 6` 再查，重复几次（Nano Banana ~15–30s）；`FAIL` → 该号限流/报错，换号；`IMG WxH` → 进下一步。
5. 出图后**一发下载 JS**（秒回，canvas → `<a download>`）：

   ```js
   (() => {
     const img = [...document.querySelectorAll('img')]
       .filter(x => x.naturalWidth > 200 && x.naturalHeight > 200).pop();
     if (!img) return 'none';
     const c = document.createElement('canvas');
     c.width = img.naturalWidth; c.height = img.naturalHeight;
     c.getContext('2d').drawImage(img, 0, 0);
     let url; try { url = c.toDataURL('image/png'); } catch (e) { return 'TAINTED:' + e; }
     const a = document.createElement('a');
     a.href = url; a.download = 'gemgen.png';
     document.body.appendChild(a); a.click(); a.remove();
     return 'OK ' + c.width + 'x' + c.height;
   })()
   ```
   - `OK WxH` = 已下载到 `~/Downloads/gemgen.png`；`TAINTED:` = 回退 `computer zoom` + `save_to_disk`。
6. `bash`：`mv ~/Downloads/gemgen.png <目标路径>`。
7. 要给用户看就 `Read` 这个 PNG。

提示词写法：Nano Banana / Veo 都吃自然语言整句，描述主体+风格+构图+光照即可；中文英文都行。

## 取产物到磁盘：原理与坑

下载已整合进**核心流程 step 4** 的那段 JS（canvas 自抓 + `<a download>`），这里只讲为什么这么做：

- 生成图是 gemini.google.com **同源 `blob:` `<img>`**，已加载进 DOM。画到 canvas → `toDataURL` 拿 PNG → 自造 `<a download>` data-URL 触发下载，**绕开 Gemini 自带「下载完整尺寸」按钮的手势门控**（那个走 File System Access，automation 点 `isTrusted=false` 必失败；普通 `<a download>` data-URL 不受门控，程序化点击即落盘）。实测 2026-06 跑通 1024×572 原分辨率。
- ⚠️ **别点 Gemini 自带下载按钮**；用 step 4 的 canvas 法。
- 多图：每张换 `download` 文件名分别抓；或每图开新 chat，避免 `.pop()` 抓到旧图。
- 兜底（canvas 被跨源污染，返回 `TAINTED:`）：`computer zoom` + `save_to_disk`（仅屏幕分辨率）。
- **视频**：blob 视频没法 canvas 抓，仍需用户手点下载 / 截帧预览。

## 视频「制作视频」（流程类推，待逐项验证）

与图片同一套机制：`+` → **「制作视频」** → 输入提示 → 发送 → 轮询（更久，1–3 分钟）→ 产物为视频。取视频同样**让用户点下载**拿原文件（视频无法用截图存整段）。首次实跑时注意核对：视频的发送/等待形态、是否有时长/比例选项、下载按钮文案，并据实更新本节与 `reference/gemini-ui.md`。

## Chrome MCP 操作纪律（来自 MCP 规范）

- 先 `tabs_context_mcp`，每个新会话新建标签页，别复用用户标签页。
- **零截图**（见顶部「Token 纪律」）：状态/等待/抓图走 `javascript_tool`，定位走 `find`，输入走 `computer`；`screenshot` 只在排障时用一次。
- 多步 `computer` 动作可用 `browser_batch` 一次发（点+输入+回车），更快更省往返；但**别把 `screenshot` 塞进 batch** 当常规步骤。
- 定位元素优先用 `find`（自然语言）拿 ref，比写死坐标稳。
- **绝不触发 JS alert/confirm/prompt 或原生对话框**——会阻塞后续所有浏览器事件。下载若弹"保存到哪"原生框，automation 够不到，交给用户处理。
- 卡住/连续失败 2–3 次就停下问用户，别死循环。

详细 UI 地图（菜单项、按钮、坐标参考、各类坑）见 `reference/gemini-ui.md`。
