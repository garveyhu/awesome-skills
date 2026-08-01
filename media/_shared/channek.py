"""channek — 统一频道解析器（分布式矩阵架构的唯一定位入口）。

所有 media skill 通过它定位「当前频道」并读取**风格卡 `card.json`**（机器单一事实源），
不再各自硬编码 vault 路径 / 上溯查找 / 家目录相对路径三套机制。

★ 卡是唯一真相源：只读 `card.json`（Channek 风格卡 v2）。旧 `card.json` 已彻底退役——
  不做兼容视图、不做双读、不做路径翻译。`ch.get("identity.niche")` 就是读卡里的 `identity.niche`。

★ 零外部依赖（仅 Python 标准库 json）——在 current / mlx-audio / whisper / manim
  任何 venv 下都能 import，不依赖 PyYAML。这是选 JSON 而非 YAML 的关键原因。

点号路径速查（旧 card.json → 新 card.json）：
    channel.slug / channel.name             →  slug / name（顶层）
    channel.niche|audience|persona|slogan    →  identity.<同名>
    channel.pillars|bio|strategy|format      →  identity.<同名>（format 是对象：orientation/persona/captions）
    channel.mind_word                        →  identity.mindWord
    brand.style_lock.image_prompt            →  locks.visualStyle.imagePrompt
    brand.style_lock.negative_prompt         →  locks.visualStyle.negativePrompt
    brand.style_lock.version|seed|sref|backend → locks.visualStyle.<同名>
    brand.ip.*                               →  brand.mascot.*
        brand.ip.i2v_subject                 →  brand.mascot.i2vSubject
        brand.ip.i2v_style                   →  brand.mascot.i2vStyle
        brand.ip.asset_ref                   →  brand.mascot.assetRef
        brand.ip.clip_map                    →  brand.mascot.clipMap
        brand.ip.clips_dir / badge_asset     →  卡 v2 已无此二键；IP 动作库目录改由
                                                layout.cardAssets.brandAssets.root
                                                + brand.mascot.name
                                                + layout.cardAssets.libraries.ipActions 拼出
    brand.sound                              →  locks.motionSound.sound
    brand.code_theme                         →  brand.codeTheme
    secrets_needed                           →  requires.secrets
    brand.tokens.* / voice.* / captions / cover / audio / platforms / publish  →  同名不变

解析优先级（频道）：
    explicit 参数  >  $CHANNEK_CHANNEL  >  从 start/cwd 上溯找 card.json（≤MAX_UP 层）
    >  `_channel/` 容器解析
解析优先级（凭据）：
    $AGENTS_RESOURCES  >  上溯找 _secrets/resources.json  >  $AGENTS_HOME/resources.json
    （**不含**任何家目录硬编码兜底——随卡分发的文件里绝不留指向他人凭据库的路径）

CLI 自检：
    python channek.py                       # 打印解析到的频道
    python channek.py brand.tokens.colors.mint
    python channek.py --channel <dir> identity.niche
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Optional

CARD_FILE = "card.json"  # 风格卡 v2·机器单一事实源（旧 card.json 已退役）
STYLE_DIR = "风格卡"  # 频道可分发区（含 card.json + 创作宪章 + 品牌 + hooks）·两区布局
ENV_CHANNEL = "CHANNEK_CHANNEL"
ENV_SECRETS = "AGENTS_RESOURCES"  # 凭据文件（或其所在目录）
ENV_SECRETS_HOME = "AGENTS_HOME"  # 凭据库根目录（其下 resources.json）
SECRETS_DIR = "_secrets"
SECRETS_FILE = "resources.json"
MAX_UP = 12


class Channel:
    """解析好的风格卡（card.json）+ 频道根。"""

    def __init__(self, root: Path, data: dict):
        self.root = root
        self.data = data or {}

    def get(self, dotted: str, default: Any = None) -> Any:
        """点号路径取值，路径即 card.json 的真实结构：get('brand.tokens.colors.mint')。"""
        cur: Any = self.data
        for key in dotted.split("."):
            if isinstance(cur, dict) and key in cur:
                cur = cur[key]
            else:
                return default
        return cur

    def path(self, rel: str) -> Path:
        """把卡里的相对路径解析成绝对路径（相对频道根）。"""
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
        return self.get("slug")

    @property
    def name(self) -> Optional[str]:
        return self.get("name")

    @property
    def identity(self) -> dict:
        return self.get("identity", {}) or {}

    @property
    def brand(self) -> dict:
        return self.get("brand", {}) or {}

    @property
    def mascot(self) -> dict:
        return self.get("brand.mascot", {}) or {}

    @property
    def ip(self) -> dict:
        """保留的旧 API 名——值同 `.mascot`（卡 v2 里这段叫 brand.mascot）。"""
        return self.mascot

    @property
    def style_lock(self) -> dict:
        return self.get("locks.visualStyle", {}) or {}

    @property
    def sound(self) -> dict:
        return self.get("locks.motionSound.sound", {}) or {}

    @property
    def colors(self) -> dict:
        return self.get("brand.tokens.colors", {}) or {}

    def __repr__(self) -> str:
        return f"<Channel slug={self.slug!r} root={self.root}>"


def _json_in(channel_dir: Path) -> Optional[Path]:
    """某频道目录里的 card.json：优先 `风格卡/card.json`（两区布局）· 兼容根级 `card.json`。"""
    nested = channel_dir / STYLE_DIR / CARD_FILE
    if nested.is_file():
        return nested
    flat = channel_dir / CARD_FILE
    return flat if flat.is_file() else None


def _channel_root(card_file: Path) -> Path:
    """从 card.json 推频道根：在 `风格卡/` 里 → 根=其上层（含两区那层）· 否则=其所在目录。"""
    parent = card_file.parent.resolve()
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
    """按优先级定位风格卡 card.json。explicit/env 可传目录或文件。

    支持「容器层」：一台机器在 _channel/ 下并存多个频道（_channel/<slug>/风格卡/card.json）。
    解析顺序：显式/env > cwd 上溯所在频道树 > _channel 容器解析
    （容器内：.active 文件指定默认 slug > 平铺 _channel/card.json 向后兼容 > 唯一频道自动选）。
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
        if p.is_dir():  # 传目录 → 取其中的 card.json（风格卡/ 或根级）
            j = _json_in(p)
            if j:
                return j
            continue
        if p.is_file():
            return p
    cur = (Path(start).expanduser() if start else Path.cwd()).resolve()
    for _ in range(MAX_UP):
        j = _json_in(cur)  # cwd 已在某频道树内（认 风格卡/card.json 或根级）
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
    """加载当前频道的风格卡。找不到时 required=True 报错、False 返回 None（零回归安全）。"""
    f = find_channel_file(explicit, start)
    if not f:
        if required:
            raise SystemExit(
                f"未解析到频道（{CARD_FILE}）：cd 进某频道目录 / 设 ${ENV_CHANNEL}=.../_channel/<slug> "
                f"/ --channel 指定 / 多频道时建 _channel/.active 写默认 slug"
            )
        return None
    data = json.loads(f.read_text(encoding="utf-8")) or {}
    return Channel(_channel_root(f), data)


def find_secrets(start: Optional[str] = None) -> Optional[Path]:
    """定位媒体矩阵凭据文件。带外手工下发、git 永不携带。

    只认环境变量与频道树内的 `_secrets/`——**没有家目录硬编码兜底**，因为随卡分发的文件里
    绝不能留指向他人凭据库的路径。要走机器级共享凭据库就显式设 $AGENTS_RESOURCES
    （文件或其所在目录）或 $AGENTS_HOME（其下 resources.json）。
    都找不到返回 None，调用方自行降级——绝不抛。
    """
    env = os.environ.get(ENV_SECRETS)
    if env:
        p = Path(env).expanduser()
        if p.is_dir():
            p = p / SECRETS_FILE
        if p.is_file():
            return p
    hit = _upward(
        Path(start).expanduser() if start else Path.cwd(), f"{SECRETS_DIR}/{SECRETS_FILE}"
    )
    if hit and hit.is_file():
        return hit
    home = os.environ.get(ENV_SECRETS_HOME)
    if home:
        p = Path(home).expanduser() / SECRETS_FILE
        if p.is_file():
            return p
    return None


def _main(argv: list) -> int:
    explicit = None
    args = list(argv)
    if args and args[0] == "--channel":
        explicit = args[1]
        args = args[2:]
    ch = load(explicit=explicit, required=False)
    if ch is None:
        print(f"[channek] 未解析到频道（cwd={Path.cwd()}）", file=sys.stderr)
        return 1
    if args and args[0] == "--root":
        print(ch.root)
        return 0
    if args:
        print(ch.get(args[0], "<未定义>"))
        return 0
    print(f"频道:   {ch.name}  (slug={ch.slug})")
    print(f"根:     {ch.root}")
    print(f"卡:     {ch.get('schema')} v{ch.get('formatVersion')}  face={ch.get('face')}")
    print(f"赛道:   {ch.get('identity.niche')}")
    print(f"形态:   {ch.get('identity.format')}")
    print(f"主色板: {ch.colors}")
    print(f"IP:     {ch.mascot.get('name')}  signature={ch.mascot.get('signature')}")
    print(f"音色:   default={ch.get('voice.default')}  profiles={list((ch.get('voice.profiles') or {}).keys())}")
    print(f"凭据:   {find_secrets() or '<未找到·带外下发>'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv[1:]))
