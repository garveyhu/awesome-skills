# 写一个新流程

一个「流程」就是一个目录，里面放两个文件：

```
flows/<你的流程名>/
├── flow.toml   # 元信息：名字、图标、分组、参数、是不是写操作、要哪些密钥
└── flow.py     # 干活的代码：一个 run(page, params, ctx) 函数
```

加流程不用碰内核。你把这两个文件写好，`registry.py` 会自动扫到它，看板自动把它渲染成一张卡片，命令行也能直接跑。你要做的就只有写这俩文件。

---

## 1. 起步：拷一份模板

```bash
# 在 skill 根目录下执行

# 想公开、跟着 skill 进 git，就放 skill 自带的 flows/
cp -r flows/_template flows/<你的流程名>

# 想私有、永远不进 git，就放你自己的运行时目录
cp -r flows/_template ~/.browser-runner/flows/<你的流程名>
```

这两个地方 registry 都会扫，看板和命令行对它们一视同仁。唯一区别是**进不进 git**（文末细说）。

顺带两个规则：目录名以 `_` 或 `.` 开头的会被跳过（所以 `_template` 这种模板不会被当成真流程收进来）；流程的**唯一名字**取 `flow.toml` 里的 `name` 字段，不是目录名——建议两个取成一样的，省得自己搞混。

---

## 2. flow.toml 每个字段讲清楚

```toml
[flow]
name        = "my-flow"           # 唯一名字：命令行 run <这个>、看板卡片认它。不填就用目录名
title       = "流程标题"           # 看板卡片的大标题。不填就用 name
description = "一句话说明干嘛"      # 卡片副标题，也是命令行 list 里那句说明。不填=空
icon        = "search"            # 卡片图标：用图标名，别用 emoji（下面详说）。不填=一个通用图标
group       = "采集"              # 看板里的分组标题，比如 采集 / 发布 / 运营 / 巡检。不填=未分组
write_ops   = false               # 有没有写操作（发布、删除、付款、提交这类）。不填=false
landing_url = ""                  # 起始页：跑之前先自动打开这个网址。留空就停在空白页，由你自己在代码里 goto

# 参数：看板照这个自动生成一个表单；命令行用 -p key=value 传。可以写 0 到 N 个 [[params]]
[[params]]
key      = "keyword"              # 参数名，代码里用 params["keyword"] 取。这个字段必填
label    = "搜索关键词"            # 表单里显示的名字。不填就用 key
type     = "string"               # string / int / float / bool 四选一。写了别的会被当成 string
required = true                   # 缺这个必填参数，命令行和看板会直接报错拒跑。不填=false
default  = ""                     # 没填时用的默认值。不填的话，这个参数就是 None

[[params]]
key   = "limit"
label = "最多条数"
type  = "int"
default = 20

# 要用哪些密钥：这里写的名字，对应 ~/.browser-runner/secrets.toml 里的段名。
# 缺了的话 doctor 和看板会提示你补，但不拦着你跑。完全不用密钥就把这一整段删掉。
[secrets]
needs = ["llm.deepseek"]          # 细节见 reference/secrets.md
```

字段速查：

| 段 | 字段 | 干啥用 | 不填时 |
|----|------|------|------|
| `[flow]` | `name` | 流程的唯一名字 | 用目录名 |
| | `title` | 看板卡片标题 | 用 name |
| | `description` | 副标题 / 说明 | 空 |
| | `icon` | 卡片图标（图标名，不是 emoji） | 一个通用图标 |
| | `group` | 看板分组 | 未分组 |
| | `write_ops` | 是不是写操作（决定要不要 `--yes`、看板要不要标红加确认） | false |
| | `landing_url` | 跑之前先自动打开的起始页 | 空（空白页） |
| `[[params]]` | `key` | 参数名（**必填**） | — |
| | `label` | 表单里显示的名字 | 用 key |
| | `type` | string / int / float / bool | string |
| | `required` | 缺了就拒跑 | false |
| | `default` | 默认值 | 无（取到就是 None） |
| `[secrets]` | `needs` | 依赖的密钥段名列表 | 无 |

**关于 icon**：用图标名，别用 emoji。看板里的图标是一套线条 SVG，emoji 显廉价。现成能用的名字有：`search` `form` `rocket` `publish` `pulse` `globe` `download` `upload` `link` `grid` `eye` `layers` `tag` `gear` `bolt` `camera`。写一个不认识的名字（或者干脆不写），看板就显示一个通用图标兜底，不会报错。图标名的定义在 `dashboard/assets/icons.js`，想加新图标就往那里加。

**关于 landing_url**：跑你的 `run()` 之前，runner 会先用它把页面打开到这个网址。所以你的 `run()` 一拿到 `page`，页面已经在起始页上了。你也可以把它留空、在 `run()` 里自己 `page.goto(...)`——两种都行，选一种就好，别导航两遍。

**关于 type**：runner 会按你写的类型把参数转好再给你——`int` 会把 `"20"` 转成数字 `20`，`bool` 认 `true / 1 / yes / on`（其余都算 false）。所以你在 `run()` 里拿到的 `params["limit"]` 已经是整数了，不用自己再 `int(...)`。

---

## 3. flow.py 的 run(page, params, ctx) 是什么约定

你只要写一个模块级的 `run` 函数，签名是固定的：

```python
def run(page, params, ctx):
    ...
    return {...}   # 一个能转成 JSON 的 dict
```

### 三个入参

| 入参 | 是什么 |
|------|--------|
| `page` | Playwright 的页面对象（Playwright 是控制浏览器的库）。它已经连到你真实登录的那个 Chrome 上了；如果你设了 `landing_url`，页面也已经打开到位。Playwright 的同步 API 都能用：`page.goto` / `page.locator` / `page.keyboard` / `page.get_by_text` 等等 |
| `params` | 校验、填好默认值、转好类型之后的参数 dict。按 `flow.toml` 里的 key 取：`params["keyword"]`、`params["limit"]`（已经是对应类型了） |
| `ctx` | 这次运行的上下文，下面这张表 |

### ctx 里有啥

| 成员 | 类型 | 说明 |
|------|------|------|
| `ctx.params` | dict | 跟 `params` 一样，方便你在函数里随手取 |
| `ctx.workdir` | `Path` | **这次运行专属的目录**（`~/.browser-runner/runs/<名字>-<时间>/`）。你产出的东西都往这里写 |
| `ctx.flow` | dict | 这个流程的元信息（name、title、write_ops、landing_url 等） |
| `ctx.dry_run` | bool | 这次是不是 `--dry-run`（空跑）。写操作要你自己看它、该跳就跳，见下面的铁律 |
| `ctx.log(msg)` | 函数 | 记一行日志。这一行会**同时**打到终端、写进 `run.log`、推给看板实时显示。多用它，别用 `print` |
| `ctx.secret(spec)` | 函数 | 按名字取一段密钥，比如 `ctx.secret("llm.deepseek")`，返回一个 dict（`{api_key, base_url, model}`）或者 `None`。名字对应 `secrets.toml` 里的段名，细节见 `reference/secrets.md` |

### 能直接 import 的现成函数

core 目录已经被 runner 放进了 import 路径，所以下面这些直接 import 就能用：

```python
from primitives import (
    upload_file,   # 给上传框喂一个本地文件
    safe_fill,     # 等元素出现后往里填字（富文本框也兼容）
    click_text,    # 按看得见的文字点
    wait_idle,     # 给页面一点反应时间
    extract_all,   # 抓一批元素的文字或属性
    extract_text,  # 抓单个元素的文字
    screenshot,    # 整页截图
)
from llm import chat   # 要用大模型时（key 从 ~/.browser-runner/secrets.toml 取）
```

这些函数的真实签名（照抄就能用）：

| 函数 | 签名 | 干啥、返回什么 |
|------|------|------------|
| `upload_file` | `upload_file(page, selector, path) -> None` | 给上传框喂本地文件。它走 CDP（Chrome 的调试协议，说白了就是脚本直接指挥浏览器的那条通道），传的是**本地路径**、让浏览器自己去读磁盘，所以**没有 50MB 上限**，上传框藏着也能设。`selector` 是 CSS 选择器，`path` 是本地绝对路径 |
| `safe_fill` | `safe_fill(page, selector, value, timeout=15000, clear=True) -> None` | 等元素出现后往里填字。普通 `fill` 填不进去时（比如富文本编辑框），自动改成一个字一个字敲。`value` 是空的就直接跳过 |
| `click_text` | `click_text(page, text, exact=False, timeout=3000) -> bool` | 按页面上看得见的文字点。**点到了返回 `True`，没点到返回 `False`（不会抛异常）**，方便你据此做备选处理 |
| `wait_idle` | `wait_idle(page, ms=1500) -> None` | 软等一会儿（等异步渲染、等进度条），不是严格等待，从不抛异常 |
| `extract_all` | `extract_all(page, selector, attr=None, limit=50) -> list[str]` | 抓所有匹配的元素：`attr=None` 取文字，否则取那个属性（比如 `href`、`src`）。**自动去掉空的、按 `limit` 截断** |
| `extract_text` | `extract_text(page, selector, timeout=8000) -> str \| None` | 取第一个匹配元素的文字；没有就返回 `None` |
| `screenshot` | `screenshot(page, path, full_page=True) -> None` | 整页截图存到 `path`（一般传 `str(ctx.workdir / "shot.png")`） |
| `chat` | `chat(messages, provider="deepseek", model=None, temperature=0.7, max_tokens=2048, timeout=60) -> str` | 调大模型，返回它回复的第一段文字。`messages` 是 `[{"role":"user","content":"..."}]`。`provider` 对应 `secrets.toml` 里的 `[llm.<provider>]` 段；`model` 不传就用那段里写的 |

### 返回值

`run()` 返回一个能转成 JSON 的 dict。runner 会拿它做两件事：

- 自动包一层 `{"ok": true, ...你的字段}`，写进 `ctx.workdir/result.json`；
- 把这个结果推给看板，跑完显示出来。

返回 `None` 也行（当成空 dict）。返回一个不是 dict 的东西，会被塞进 `{"result": ...}`。**建议永远返回 dict**，把「跑出了啥、停在哪、有没有留给人工补的活」讲清楚。

---

## 4. 几条铁律（必须守）

### ① 写操作流程：填到「提交按钮」前面就停，绝不自己点提交

`write_ops = true` 的流程（发布、删除、付款、任何点下去就收不回来的提交），你把表单填好、把提交按钮滚动到看得见的位置就停手，最后那一下点击**交回给人**。

- 这既是安全兜底（脚本不替你按下收不回来的按钮），也再降低一层被网站判定成机器人的风险。
- 这类流程在命令行上要加 `--yes` 才放行；看板里要勾一下确认框。
- **别在 `run()` 里 `click("提交")`。** 正确做法是把按钮 `scroll_into_view_if_needed()` 滚出来，`ctx.log` 记一句「已填好，停在提交前」，然后返回 `{"stopped_at": "...", "todo": [...]}`。

### ② 出错别硬崩：try/except → 记一句 → 返回里带 todo

选择器失效、元素没出现、网站改版——别让流程直接抛异常崩掉。用 `try/except` 包住，`ctx.log` 记一句人话，返回的 dict 里带一个 `todo` 交给人工补：

```python
try:
    safe_fill(page, SEARCH_BOX, kw)
except Exception as e:
    ctx.log(f"填搜索框失败：{e}")
    return {"error": "搜索框选择器可能改了", "todo": ["核对 SEARCH_BOX 选择器"]}
```

runner 自己也兜了一层：单个流程抛异常，只会记成 `{"ok": false, "error": ...}`，不会把整个 runner 带崩。但你自己处理得越细，返工时越省事。

### ③ 记得看 ctx.dry_run

`--dry-run`（空跑）只是把 `ctx.dry_run` 设成 `True` 传给你，它**不会自动帮你拦住任何动作**。真正会改东西的动作，要你自己判断跳过：

```python
if not ctx.dry_run:
    safe_fill(page, SEARCH_BOX, kw)   # 会改东西的动作，空跑时跳过
```

只读的流程可以不管它（空跑时照抓，正好验证选择器还活着）。

### ④ 产出的东西一律写进 ctx.workdir

JSON、截图、下载的文件……全写进 `ctx.workdir`（这次运行专属的目录）。别往 skill 目录写，也别往当前目录乱写。

---

## 5. 一个完整例子：登录状态下搜关键词 → 抓前 N 条结果的标题和链接

假设你要写这么一个流程：借着你已经登录好的浏览器，在某个站内搜一个词，把前 N 条结果的标题和链接抓下来存成 JSON。这是个**只读**流程（`write_ops=false`）。它演示了 `landing_url` 自动导航、`safe_fill` 搜索、`extract_all` 抓标题和链接、把结果写进 `ctx.workdir`。

> 里面的选择器（`SEARCH_BOX` / `RESULT_TITLE` / `RESULT_LINK`）都是**跟着具体网站走**的，换成你自己的站点时改这几行就行。这里用占位选择器示意结构。

`flows/site-search/flow.toml`：

```toml
[flow]
name        = "site-search"
title       = "站内搜索采集"
description = "登录状态下搜关键词，抓前 N 条结果的标题和链接存 JSON。只读。"
icon        = "search"
group       = "采集"
write_ops   = false
landing_url = "https://你的站点.com/search"   # 跑之前自动打开搜索页

[[params]]
key      = "keyword"
label    = "搜索关键词"
type     = "string"
required = true

[[params]]
key     = "limit"
label   = "最多条数"
type    = "int"
default = 20
```

`flows/site-search/flow.py`：

```python
"""登录状态下搜关键词，抓前 N 条结果的标题和链接存 JSON。只读流程。"""
from __future__ import annotations

import json

from primitives import extract_all, safe_fill, wait_idle

# ↓↓↓ 跟着网站走的选择器：换成你自己的站点时只改这三行
SEARCH_BOX   = 'input[name="q"]'          # 搜索框
RESULT_TITLE = "a.result-title"           # 每条结果的标题链接（取文字）
RESULT_LINK  = "a.result-title"           # 每条结果的链接（取 href 属性）


def run(page, params, ctx):
    kw = params["keyword"]
    limit = params["limit"]                # flow.toml 声明了 int，这里已经是整数
    ctx.log(f"搜索「{kw}」，取前 {limit} 条")

    # landing_url 已经把页面带到搜索页了，这里直接填框 + 回车
    try:
        safe_fill(page, SEARCH_BOX, kw)
        page.keyboard.press("Enter")
    except Exception as e:
        ctx.log(f"提交搜索失败：{e}")
        return {"error": "搜索框选择器可能改了", "todo": ["核对 SEARCH_BOX"]}

    wait_idle(page, 1500)  # 等结果渲染出来

    titles = extract_all(page, RESULT_TITLE, attr=None, limit=limit)   # 文字
    links  = extract_all(page, RESULT_LINK, attr="href", limit=limit)  # href 属性
    results = [{"title": t, "link": l} for t, l in zip(titles, links)]
    ctx.log(f"抓到 {len(results)} 条")

    # 产出写进 ctx.workdir（这次运行专属的目录）
    (ctx.workdir / "results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), "utf-8"
    )
    return {"keyword": kw, "count": len(results), "results": results}
```

跑它：

```bash
browser-runner run site-search -p keyword=Playwright -p limit=10
```

（没装全局命令的话，在 skill 目录下用 `<你的 python> core/runner.py run site-search -p ...` 也一样。）

跑完，产出在 `~/.browser-runner/runs/site-search-<时间>/`：`results.json`（抓到的结果）、`run.log`（日志）、`result.json`（返回值包了一层 `ok`）。

### 如果是写操作流程，差在哪

把上面改成「搜到结果后写一条评论并**发布**」这种带写操作的，就该把 `write_ops` 设成 `true`，而且 `run()` 里**只填不点提交**：

```python
if not ctx.dry_run:
    safe_fill(page, COMMENT_BOX, params["comment"])
# 把发布按钮滚到眼前，但绝不点它
page.get_by_text("发布").first.scroll_into_view_if_needed()
ctx.log("评论已填好，停在「发布」前，请人工核对后手动点")
return {"stopped_at": "发布按钮前", "todo": ["人工核对内容后点发布"]}
```

命令行跑这类流程要加 `--yes` 放行（不加就报错拒跑）；看板里要勾确认框。

---

## 6. 测一测

### `--dry-run`：只连上、导航、定位，不动手

```bash
browser-runner run site-search -p keyword=test --dry-run
```

拿来干嘛：网站改版之后跑一遍空跑，流程里会改东西的动作都被 `if not ctx.dry_run` 跳过，只做导航、定位、只读抽取，**快速看看选择器有没有失效**。对写操作流程，空跑还会免掉 `--yes`（反正空跑不会提交）。

### `doctor`：体检依赖、连通、密钥

```bash
browser-runner doctor
```

它检查这几样：playwright 装没装、Chrome 调试端口通不通、扫到了几个流程、各流程 `needs` 里声明的密钥齐不齐。加完流程跑一下，确认元信息合法、密钥到位。

### 另外两个有用的命令

```bash
browser-runner list         # 列出所有流程（含私有的），看看你的新流程有没有被扫到
browser-runner dashboard    # 起看板，在浏览器里手动点着跑、填表单、看实时输出
```

---

## 7. 私有还是公开：流程放哪

| 放哪 | 目录 | 进 git？ | 适合 |
|------|------|---------|------|
| **公开** | skill 自带的 `flows/<名>/` | 会，随 skill 发布 | 通用、能分享、不含隐私逻辑的流程 |
| **私有** | `~/.browser-runner/flows/<名>/` | 不会，永远不入库 | 含你自己站点内部逻辑、跟账号相关、不想外发的流程 |

两处 registry 都扫，看板和命令行一视同仁。**同名的话，私有盖过公开**——你可以在私有目录放一个同名流程，就地改公开示例的行为，而不动 skill 里那个原版。

密钥永远不写进流程文件（skill 目录里一个密钥都没有），全放在 `~/.browser-runner/secrets.toml` 里——细节见 `reference/secrets.md`。
