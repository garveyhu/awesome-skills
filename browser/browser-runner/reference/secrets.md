# 配置和密钥怎么管

## 金律：skill 目录里一个密钥都不放

这个 skill 自己的配置和密钥，全放在一个专属文件夹 `~/.browser-runner/` 里，不碰任何外部的凭据库。skill 目录本身连一个密钥都不写，所以可以放心开源。

分工是这样：

| 东西 | 只放哪 | 进 git？ |
|------|--------|---------|
| **密钥**（大模型 API key、平台 token） | `~/.browser-runner/secrets.toml` | 不进 |
| **运行配置**（端口、chrome 路径、profile、私有流程目录） | `~/.browser-runner/config.toml` | 不进 |
| **运行时状态**（每次跑的产物、日志、登录 profile、你的私有流程） | `~/.browser-runner/` 下的 `runs/`、`profiles/`、`flows/` | 不进 |
| 框架代码 + 通用示例流程 | 本 skill | 进 |

skill 的 `config/` 里放了两个模板 `config.example.toml` 和 `secrets.example.toml`。上手就是：把它俩复制到 `~/.browser-runner/`，去掉文件名里的 `.example`，填上你自己的值。两个都不填也能跑，只是用不了要密钥的流程。

```bash
mkdir -p ~/.browser-runner
# 在 skill 根目录下执行
cp config/config.example.toml  ~/.browser-runner/config.toml
cp config/secrets.example.toml ~/.browser-runner/secrets.toml
# 然后编辑这两个文件填值
```

---

## 1. config.toml：运行配置

能配这几个键，全都有兜底默认，不填就走默认，按需覆盖：

| 键 | 默认 | 干啥用 |
|----|------|------|
| `debug_port` | `9876` | Chrome 调试端口。特意选了个不常用的，避开常见的 9222，这样能同时挂着别的调试浏览器、两边不打架 |
| `chrome_path` | macOS 默认路径 | Chrome 可执行文件的路径（换机器、换系统时改） |
| `profile_dir` | `~/.browser-runner/profiles/default` | 专用调试浏览器的登录 profile 目录（跟你日常用的 Chrome 隔离开） |
| `private_flows_dir` | `~/.browser-runner/flows` | 你私有流程放哪（registry 除了扫 skill 自带的流程，也扫这里） |

一份 `~/.browser-runner/config.toml` 的样子：

```toml
debug_port  = 9876
chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
profile_dir = "/Users/你/.browser-runner/profiles/default"
private_flows_dir = "/Users/你/.browser-runner/flows"
```

### 用环境变量临时覆盖

任何一个键都能用环境变量临时盖掉，优先级最高：

```
BROWSER_RUNNER_<键名大写>  >  config.toml  >  内置默认
```

比如临时换个端口跑一下 doctor：

```bash
BROWSER_RUNNER_DEBUG_PORT=9444 browser-runner doctor
```

另外还有一个 `BROWSER_RUNNER_HOME`，能整体换掉运行时根目录（默认就是 `~/.browser-runner`）。

---

## 2. secrets.toml：密钥

格式很简单，一段一套凭据，段名你自己起。大模型的 key 统一放在 `[llm.<名字>]` 这种段里，每段写 `api_key`、`base_url`、`model`：

```toml
# ~/.browser-runner/secrets.toml —— 下面都是占位值，填你自己的真 key

[llm.deepseek]
api_key  = "sk-你的key"
base_url = "https://api.deepseek.com"
model    = "deepseek-chat"

[llm.qwen]
api_key  = "你的key"
base_url = "https://dashscope.aliyun.com/compatible-mode/v1"
model    = "qwen-plus"

# 平台 token 之类照同样的格式加，段名随你起：
[platform.example]
token = "..."
```

几点说明：

- `base_url` 走的是 **OpenAI 兼容**接口（也就是能收 `/chat/completions` 请求的那种）。deepseek、通义 dashscope 的兼容模式、自建网关都符合。
- 段名随你加：`llm.deepseek`、`llm.qwen`、`platform.bilibili` 都行。流程 `flow.toml` 里 `needs` 写的名字，和这里的段名对上就行。
- 平台 token 这类，流程里用 `ctx.secret("platform.example")` 取，返回的就是那一段的 dict。

### 流程里怎么用

最常见的是调大模型，一行就够：

```python
from llm import chat
text = chat([{"role": "user", "content": "把这段话总结成一句话：..."}])
```

`chat` 的签名和解析规则：

```python
chat(messages, provider="deepseek", model=None,
     temperature=0.7, max_tokens=2048, timeout=60) -> str
```

- 它去 `secrets.toml` 里读 `[llm.<provider>]` 那一段，拿 `api_key` 和 `base_url`（还有可选的 `model`）。
- `model` 传了就用传的，没传就用那段里写的，都没有就兜底 `deepseek-chat`。
- `base_url` 没配就兜底 `https://api.deepseek.com`，会自动补上 `/chat/completions`。
- 要是缺 `[llm.<provider>]` 段、或者段里没 `api_key`，会抛错，提示你来看这份文档。
- 返回的是**第一段回复的纯文字**。

换个 provider 就是换个参数：

```python
chat(msgs, provider="qwen")                       # 用 [llm.qwen]
chat(msgs, provider="newapi", model="gpt-4o")     # 用 [llm.newapi]，模型换成 gpt-4o
```

`llm.py` 只用 Python 标准库（`urllib`）发请求，不装任何第三方。

要拿别的密钥（不是大模型的），用 `ctx.secret(名字)`：

```python
cred = ctx.secret("platform.example")   # 返回 {"token": "..."} 或者 None
```

它就一个参数——一个点号连起来的段名。取不到返回 `None`。

---

## 3. needs 和「亮不亮灯」的对应关系

流程在 `flow.toml` 里声明自己要哪些密钥：

```toml
[secrets]
needs = ["llm.deepseek"]
```

`needs` 里每一项，就是一个 `secrets.toml` 的段名。`doctor` 和看板会照着去 `secrets.toml` 里看这段在不在、有没有内容：

- 配齐了：不吭声。
- 缺了：**提示你补一下**（但不拦着你跑）。真跑到用这个 key 的那一步，才会因为缺失报错。

判断规则就是按点号一层层往里找：`llm.deepseek` 就是看 `[llm.deepseek]` 这段在不在、是不是一段有内容的配置。对得上就算齐。

不用任何密钥的流程，把整个 `[secrets]` 段删掉就行。

---

## 4. 两层 gitignore，密钥不会溜进 git

其实真正的密钥根本就**不在 skill 目录里**（在 `~/.browser-runner/secrets.toml`），运行时状态也不在（在 `~/.browser-runner/`）——所以哪怕 gitignore 漏挡，也不会把密钥带进 git。下面这两层只是再多加一道保险。

**第一层，skill 自带的 `.gitignore`。** skill 根目录有一份自己的 `.gitignore`，跟着 skill 走，clone 到哪都生效（git 原生就认这种嵌套的 .gitignore）。它挡的是本 skill 特有的运行时垃圾，外加防手滑：

```
runs/
flows/_private/
*.local.toml
.runtime/
**/secrets.toml
**/config.toml
```

最后两行是防止有人手滑，把真的 `secrets.toml` / `config.toml` 放进了 skill 目录——真放进去了也会被挡下。这份 `.gitignore` 是 skill 自己的一部分，skillctl 只管根 `links/.gitignore`，不碰它。

**第二层，`links/` 仓库根的 `.gitignore`。** skill 所在的 `links/` 仓库根那份 `.gitignore` 已经全局挡掉了一批敏感和垃圾文件，本 skill 白蹭：

```
.DS_Store
__pycache__/
accounts.json
*.local.json / *.local.yaml
.env
```

---

## 快速自检

```bash
browser-runner doctor     # 看密钥齐不齐、端口通不通、流程合不合法
```
