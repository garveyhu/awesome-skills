"""调大模型的小封装 —— OpenAI 兼容接口，纯标准库（urllib），不装第三方。

key 从 skill 自己的 `~/.browser-runner/secrets.toml` 里取。那个文件写成这样：

    [llm.deepseek]
    api_key  = "你的 key"
    base_url = "https://api.deepseek.com"
    model    = "deepseek-chat"

流程里一行就能用：`from llm import chat; text = chat([{"role": "user", "content": "..."}])`。
"""
from __future__ import annotations

import json
import urllib.request

try:
    from . import config
except ImportError:  # 脚本直跑（core 在 sys.path）
    import config


def chat(
    messages: list[dict],
    provider: str = "deepseek",
    model: str | None = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
    timeout: int = 60,
) -> str:
    """调 OpenAI 兼容的 /chat/completions，返回第一条回复文本。

    provider 对应 secrets.toml 里的 `[llm.<provider>]` 段，那段要有 api_key 和 base_url
    （也可以写 model 当默认）。传了 model 参数就用传的。
    """
    cred = config.get_secret(f"llm.{provider}")
    if not cred or "api_key" not in cred:
        raise RuntimeError(
            f"secrets.toml 里没配 [llm.{provider}]（要 api_key 和 base_url）——见 reference/secrets.md。"
        )
    base = (cred.get("base_url") or "https://api.deepseek.com").rstrip("/")
    url = base + ("/chat/completions" if not base.endswith("/chat/completions") else "")
    payload = {
        "model": model or cred.get("model") or "deepseek-chat",
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {cred['api_key']}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]
