"""配置与密钥。

这个 skill 自己管配置和密钥，全放在一个专属文件夹 `~/.browser-runner/` 里，
不依赖任何外部凭据库：

    ~/.browser-runner/
      config.toml     运行配置（端口 / chrome 路径 / profile / 私有流程目录）
      secrets.toml    密钥（大模型 key、平台 token）—— 流程按名取用
      profiles/       调试 Chrome 的专属登录 profile
      flows/          你自己写的流程（不进 git）
      runs/           每次运行的产物和日志

skill 目录本身一个密钥都不写，可以放心开源。
配置读取优先级：环境变量 `BROWSER_RUNNER_<KEY>` > `config.toml` > 内置默认。
"""
from __future__ import annotations

import os
import tomllib
from functools import lru_cache
from pathlib import Path

DEFAULT_PORT = 9876  # 选个不常用的端口，避开常见的 9222，免得和别的调试浏览器撞
DEFAULT_CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def home() -> Path:
    """运行时根目录（所有本地状态的家）。可用 BROWSER_RUNNER_HOME 覆盖。"""
    d = Path(os.environ.get("BROWSER_RUNNER_HOME", Path.home() / ".browser-runner"))
    return d.expanduser()


@lru_cache(maxsize=1)
def _config() -> dict:
    f = home() / "config.toml"
    if f.exists():
        return tomllib.loads(f.read_text("utf-8"))
    return {}


def get(key: str, default=None):
    env = os.environ.get("BROWSER_RUNNER_" + key.upper())
    if env is not None:
        return env
    return _config().get(key, default)


def debug_port() -> int:
    return int(get("debug_port", DEFAULT_PORT))


def chrome_path() -> str:
    return get("chrome_path", DEFAULT_CHROME)


def profile_dir() -> Path:
    return Path(get("profile_dir", home() / "profiles" / "default")).expanduser()


def private_flows_dir() -> Path:
    """你私有流程的家（永不入库）。看板 / registry 除扫 skill 内置 flows 外也扫这里。"""
    return Path(get("private_flows_dir", home() / "flows")).expanduser()


def runs_dir() -> Path:
    d = home() / "runs"
    d.mkdir(parents=True, exist_ok=True)
    return d


# ── 密钥（本 skill 专属 · ~/.browser-runner/secrets.toml）──

def secrets_path() -> Path:
    return home() / "secrets.toml"


@lru_cache(maxsize=1)
def _secrets() -> dict:
    f = secrets_path()
    return tomllib.loads(f.read_text("utf-8")) if f.exists() else {}


def get_secret(spec: str) -> dict | None:
    """按点号名从 secrets.toml 取一段凭据，比如 `llm.deepseek`。取不到返 None。

    secrets.toml 里 `[llm.deepseek]` 这一段，就对应 spec `llm.deepseek`。
    """
    node = _secrets()
    for part in spec.split("."):
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node if isinstance(node, dict) else None


def has_secret(spec: str) -> bool:
    """流程 flow.toml 里 needs 的某项配齐了没（doctor 和看板据此提示）。"""
    return bool(get_secret(spec))
