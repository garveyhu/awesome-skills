---
name: browser-runner
description: >-
  把你在浏览器里重复做的操作写成脚本存下来，随时一键复放。做法是先开一个带调试端口的
  Chrome，脚本连上这个你已经登录好的浏览器（登录状态、指纹都是你本人的，最不容易被平台
  风控），照着脚本替你点、填、抓。每个流程一个目录（flow.toml 写元信息、flow.py 写怎么做），
  加流程不用动内核。还配了个本地网页看板，自动把流程渲染成卡片，填参数、一键跑、看实时输出。
  适合把发布、采集、填表、批量巡检这类反复做的网页操作固定成脚本。触发词：浏览器自动化、
  把某个网页操作写成脚本、自动填表 / 采集 / 发布、Playwright、连上已登录的 Chrome、
  可视化触发自动化。和 claude-in-chrome 互补——那个是让 AI 现场看着页面即兴操作，
  这个是把已经定型的流程固定成不需要 AI 在旁边盯着的脚本。
---

# browser-runner

一句话：把你在浏览器里反复做的事写成脚本存起来，以后一键就能重跑。内核是稳定的，流程你自己往里加，越攒越多。

做法很简单：连上你已经登录好的浏览器，用一套现成的操作函数照着脚本点、填、抓；一个流程一个文件，写操作停在提交前留给你确认。不挑网站，任何重复的网页操作都能这么固定下来。

## 什么时候用它

- 有个网页操作你老是重复做，想固定成脚本：采集、填表、发布、后台巡检、批量下载……
- 想要**每次都一样、能重跑、快**——不靠 AI 现场判断。这也是它和 `claude-in-chrome` 的分工：没做过、探索性的一次性任务，让 AI 现场看着页面即兴操作；已经定型、要反复跑的，写成脚本沉到这里。
- 想要一个网页界面，手动点一下就跑某个流程、填填参数、看它实时输出。

## 三块结构

```
core/        内核，写好了就不用动：起浏览器、连浏览器、一套操作函数、扫流程、配置、调大模型、命令行入口
flows/       你的流程，越加越多：一个流程 = flows/<名字>/ 里放 flow.toml 和 flow.py
dashboard/   本地网页看板：一个标准库写的小服务 + 一个网页
config/       配置模板：把这里的 *.example.toml 复制到 ~/.browser-runner/ 用
```

## 快速上手

先装好全局命令（见下面「装成全局命令」），然后：

```bash
browser-runner            # 直接开看板（会自动在浏览器里打开）
browser-runner doctor     # 体检：浏览器连没连上、缺不缺配置、流程有没有问题
browser-runner list       # 列出所有流程
browser-runner run <流程名> -p 参数名=值 ...   # 跑某个流程
```

**起调试浏览器**（第一次用、或看板显示没连上时）：命令行跑 `bash core/chrome_debug.sh`，或者直接在看板顶上点「起调试 Chrome」按钮。它起的是一个 browser-runner 专用的 Chrome（登录状态单独存在 `~/.browser-runner/profiles/`，和你日常用的 Chrome 隔开、互不打架）。第一次在弹出来的窗口里把要操作的网站登录一遍就行，之后一直记着。看板顶上会实时显示「已连接 / 未连接」。

没装全局命令的话，也能直接用：`bin/browser-runner <参数>`（它自己会找带 playwright 的 python），或者 `<你的 python> core/runner.py <参数>`。

### 装成全局命令

skill 自带一个启动器 `bin/browser-runner`（跟着 skill 走，自己会挑 python）。在你的 shell 配置里包一层就能全局用了。zsh 的话放一个 `~/.zshrc.d/browser-runner.zsh`：

```zsh
# 把下面的路径换成你放 skill 的实际位置
browser-runner() { "$HOME/你放skill的路径/browser-runner/bin/browser-runner" "$@"; }
br() { browser-runner "$@"; }          # 想要短名就留着
```

之后光敲 `browser-runner`（或 `br`）就开看板，带上子命令就跑对应的事。想换 python 用 `BROWSER_RUNNER_PYTHON` 指定（默认先找 skill 自带的 `.venv`，再找 `~/.venvs/current`，最后用 `python3`）。

## 写一个新流程

```bash
cp -r flows/_template flows/<你的流程名>       # 想私有、不进 git，就放 ~/.browser-runner/flows/<名字>
```

1. 改 `flow.toml`：名字、标题、图标、分组、参数、是不是写操作、要不要密钥。
2. 写 `flow.py` 的 `run(page, params, ctx)`：用现成的操作函数干活，产物写进 `ctx.workdir`。
3. `browser-runner list` 自动就收进来了，看板也自动渲染，命令行也能直接跑。**内核一行都不用改。**

现成能用的操作函数（`from primitives import ...`）：`upload_file`（用 CDP 传文件、绕开 50MB 限制）、`safe_fill`（填框）、`click_text`（按文字点）、`wait_idle`（等一下）、`extract_all`（批量抓文本/属性）、`extract_text`（抓一处文本）、`screenshot`（截图）。要调大模型就 `from llm import chat`。写法细节见 `reference/authoring-a-flow.md`。

## 一条铁律：写操作停在提交前

`write_ops = true` 的流程（发布、删除、付款这种）**只填到「提交按钮」前面就停下，绝不自己点提交**——最后这一下留给你本人。命令行上这类流程要加 `--yes` 才放行，看板里要点一下确认。既是安全兜底，也再降一层被平台风控的风险。

## 配置和密钥（都在自己的文件夹里）

这个 skill 自己管配置和密钥，全放在一个专属文件夹 `~/.browser-runner/` 里，不碰任何外部的凭据库。skill 目录本身一个密钥都不写，可以放心开源。

| 东西 | 放哪 |
|------|------|
| 运行配置（端口 / chrome 路径 / profile / 私有流程目录） | `~/.browser-runner/config.toml` |
| 密钥（大模型 key、平台 token） | `~/.browser-runner/secrets.toml` |
| 你自己写的流程 | `~/.browser-runner/flows/` |
| 调试 Chrome 的登录 profile | `~/.browser-runner/profiles/` |
| 每次运行的产物和日志 | `~/.browser-runner/runs/` |

skill 的 `config/` 里放了两个模板：把 `config.example.toml`、`secrets.example.toml` 复制到 `~/.browser-runner/` 下、去掉 `.example`、填上自己的值就行。都不填也能跑，只是用不了要密钥的流程。细节见 `reference/secrets.md`。

## 依赖

- Python 3.11 以上（要用 `tomllib`）+ `playwright`（`pip install playwright` 就够，连的是你系统里的 Chrome，一般不用再 `playwright install`）。
- macOS 的默认路径都内置好了；别的路径在 `~/.browser-runner/config.toml` 里改。

## 调试端口为什么默认 9876

很多调试用的 Chrome、Playwright 默认用 9222，所以这里特意选了个不常用的 9876，这样你同时挂着别的调试浏览器时两边也不打架。要改就在 `~/.browser-runner/config.toml` 里设 `debug_port`。
