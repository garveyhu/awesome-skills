"""ms_channel — 统一频道解析器（分布式矩阵架构的唯一定位入口）。

所有 media skill 通过它定位「当前频道」并读取 channel.json（机器单一事实源），
不再各自硬编码 vault 路径 / 上溯查找 / 家目录相对路径三套机制。

★ 零外部依赖（仅 Python 标准库 json）——在 current / mlx-audio / whisper / manim
  任何 venv 下都能 import，不依赖 PyYAML。这是选 JSON 而非 YAML 的关键原因。

解析优先级（频道）：
    explicit 参数  >  $MEDIA_STUDIO_CHANNEL  >  从 start/cwd 上溯找 channel.json（≤MAX_UP 层）
解析优先级（凭据）：
    $AGENTS_RESOURCES  >  上溯找 _secrets/resources.json  >  ~/.agents/resources.json

CLI 自检：
    python ms_channel.py                       # 打印解析到的频道
    python ms_channel.py brand.tokens.colors.mint
    python ms_channel.py --channel <dir> channel.name
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Optional

CHANNEL_FILE = "channel.json"
STYLE_DIR = "风格卡"  # 频道可分发区（含 channel.json + 创作宪章 + 品牌 + hooks）·两区布局
ENV_CHANNEL = "MEDIA_STUDIO_CHANNEL"
ENV_SECRETS = "AGENTS_RESOURCES"
SECRETS_DIR = "_secrets"
SECRETS_FILE = "resources.json"
MAX_UP = 12


class Channel:
    """解析好的频道配置 + 频道根。"""

    def __init__(self, root: Path, data: dict):
        self.root = root
        self.data = data or {}

    def get(self, dotted: str, default: Any = None) -> Any:
        """点号路径取值：get('brand.tokens.colors.mint')。"""
        cur: Any = self.data
        for key in dotted.split("."):
            if isinstance(cur, dict) and key in cur:
                cur = cur[key]
            else:
                return default
        return cur

    def path(self, rel: str) -> Path:
        """把 channel.json 里的相对路径解析成绝对路径（相对频道根）。"""
        return (self.root / rel).resolve()

    def style_path(self, rel: str = "") -> Path:
        """频道可分发区（风格卡/）下的绝对路径。两区布局的单一入口——
        画面组件 / BGM音效 / 品牌套件等都在此区，调用方不再散落 `风格卡` / 旧 `0-风格` 字面量。"""
        base = self.root / STYLE_DIR
        return (base / rel).resolve() if rel else base.resolve()

    def voice_profile(self, key: Optional[str] = None) -> dict:
        """取某音色 profile（默认 voice.default）。"""
        profiles = self.get("voice.profiles", {}) or {}
        key = key or self.get("voice.default")
        return profiles.get(key, {}) if key else {}

    @property
    def slug(self) -> Optional[str]:
        return self.get("channel.slug")

    @property
    def name(self) -> Optional[str]:
        return self.get("channel.name")

    @property
    def brand(self) -> dict:
        return self.get("brand", {}) or {}

    @property
    def ip(self) -> dict:
        return self.get("brand.ip", {}) or {}

    @property
    def style_lock(self) -> dict:
        return self.get("brand.style_lock", {}) or {}

    @property
    def colors(self) -> dict:
        return self.get("brand.tokens.colors", {}) or {}

    def __repr__(self) -> str:
        return f"<Channel slug={self.slug!r} root={self.root}>"


def _json_in(channel_dir: Path) -> Optional[Path]:
    """某频道目录里的 channel.json：优先 `风格卡/channel.json`（两区布局）· 兼容根级 `channel.json`。"""
    nested = channel_dir / STYLE_DIR / CHANNEL_FILE
    if nested.is_file():
        return nested
    flat = channel_dir / CHANNEL_FILE
    return flat if flat.is_file() else None


def _channel_root(json_file: Path) -> Path:
    """从 channel.json 文件推频道根：在 `风格卡/` 里 → 根=其上层（含两区那层）· 否则=其所在目录。"""
    parent = json_file.parent.resolve()
    return parent.parent if parent.name == STYLE_DIR else parent


def _upward(start: Path, target: str) -> Optional[Path]:
    cur = start.resolve()
    for _ in range(MAX_UP):
        cand = cur / target
        if cand.exists():
            return cand
        if cur.parent == cur:
            break
        cur = cur.parent
    return None


def find_channel_file(
    explicit: Optional[str] = None, start: Optional[str] = None
) -> Optional[Path]:
    """按优先级定位 channel.json。explicit/env 可传目录或文件。

    支持「容器层」：一台机器在 _channel/ 下并存多个频道（_channel/<slug>/channel.json）。
    解析顺序：显式/env > cwd 上溯所在频道树 > _channel 容器解析
    （容器内：.active 文件指定默认 slug > 平铺 _channel/channel.json 向后兼容 > 唯一频道自动选）。
    多频道且未指定 → None（交 load() 报歧义）。
    """

    def _pick_in_container(container: Path) -> Optional[Path]:
        if not container.is_dir():
            return None
        active = container / ".active"
        if active.is_file():
            cand = _json_in(container / active.read_text(encoding="utf-8").strip())
            if cand:
                return cand
        flat = _json_in(container)  # 平铺单频道（向后兼容）
        if flat:
            return flat
        subs = sorted(d for d in container.iterdir() if d.is_dir() and _json_in(d))
        return _json_in(subs[0]) if len(subs) == 1 else None

    for candidate in (explicit, os.environ.get(ENV_CHANNEL)):
        if not candidate:
            continue
        p = Path(candidate).expanduser()
        if p.is_dir():  # 传目录 → 取其中的 channel.json（风格卡/ 或根级）
            j = _json_in(p)
            if j:
                return j
            continue
        if p.is_file():
            return p
    cur = (Path(start).expanduser() if start else Path.cwd()).resolve()
    for _ in range(MAX_UP):
        j = _json_in(cur)  # cwd 已在某频道树内（认 风格卡/channel.json 或根级）
        if j:
            return j
        hit = _pick_in_container(cur / "_channel")
        if hit:
            return hit
        if cur.parent == cur:
            break
        cur = cur.parent
    return None


def load(
    explicit: Optional[str] = None,
    start: Optional[str] = None,
    required: bool = True,
) -> Optional[Channel]:
    """加载当前频道。找不到时 required=True 报错、False 返回 None（零回归安全）。"""
    f = find_channel_file(explicit, start)
    if not f:
        if required:
            raise SystemExit(
                f"未解析到频道（{CHANNEL_FILE}）：cd 进某频道目录 / 设 ${ENV_CHANNEL}=.../_channel/<slug> "
                f"/ --channel 指定 / 多频道时建 _channel/.active 写默认 slug"
            )
        return None
    data = json.loads(f.read_text(encoding="utf-8")) or {}
    return Channel(_channel_root(f), data)


def find_secrets(start: Optional[str] = None) -> Optional[Path]:
    """定位媒体矩阵凭据文件。带外手工下发、git 永不携带。"""
    env = os.environ.get(ENV_SECRETS)
    if env:
        p = Path(env).expanduser()
        if p.is_file():
            return p
    hit = _upward(
        Path(start).expanduser() if start else Path.cwd(), f"{SECRETS_DIR}/{SECRETS_FILE}"
    )
    if hit and hit.is_file():
        return hit
    fallback = Path.home() / ".agents" / "resources.json"
    return fallback if fallback.is_file() else None


def _main(argv: list) -> int:
    explicit = None
    args = list(argv)
    if args and args[0] == "--channel":
        explicit = args[1]
        args = args[2:]
    ch = load(explicit=explicit, required=False)
    if ch is None:
        print(f"[ms_channel] 未解析到频道（cwd={Path.cwd()}）", file=sys.stderr)
        return 1
    if args and args[0] == "--root":
        print(ch.root)
        return 0
    if args:
        print(ch.get(args[0], "<未定义>"))
        return 0
    print(f"频道:   {ch.name}  (slug={ch.slug})")
    print(f"根:     {ch.root}")
    print(f"赛道:   {ch.get('channel.niche')}")
    print(f"形态:   {ch.get('channel.format')}")
    print(f"主色板: {ch.colors}")
    print(f"IP:     {ch.ip.get('name')}  signature={ch.ip.get('signature')}")
    print(f"音色:   default={ch.get('voice.default')}  profiles={list((ch.get('voice.profiles') or {}).keys())}")
    print(f"凭据:   {find_secrets() or '<未找到·带外下发>'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv[1:]))
