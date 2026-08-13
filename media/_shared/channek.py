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
    brand.tokens.* / captions / cover / platforms  →  同名不变

本机接线值（弃用期收尾后不再入卡·落频道侧车 `.channek/local/`，get() 双轨读侧车 > 卡段）：
    voice.profiles（modelPath/promptWav…） →  .channek/local/voice.json
    publish.profileDir / publish.debugPort →  .channek/local/publish.json
    publish.accounts                        →  config 声明 channek.publish.accounts（逗号文本·读回重组数组）
    audio.bed.floorDb                       →  config 声明 sound.bedFloorDb

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
import tempfile
import os
import sys
from pathlib import Path
from typing import Any, Optional

CARD_FILE = "card.json"  # 风格卡 v2·机器单一事实源（旧 card.json 已退役）
STYLE_DIR = "风格卡"  # 频道可分发区（含 card.json + 创作宪章 + 品牌 + hooks）·两区布局
LOCAL_DIR = ".channek/local"  # 频道侧车（本机接线值·不入卡不随卡·gitignore）
ENV_CHANNEL = "CHANNEK_CHANNEL"
ENV_SECRETS = "AGENTS_RESOURCES"  # 凭据文件（或其所在目录）
ENV_SECRETS_HOME = "AGENTS_HOME"  # 凭据库根目录（其下 resources.json）
SECRETS_DIR = "_secrets"
SECRETS_FILE = "resources.json"
MAX_UP = 12


# 卡已完成「config 自声明」迁移（locks/captions 段退场·audio 合成参数进 pluginSettings），
# 旧点号路径靠这张表续命：skill 不用改一行，get() 先查 config 声明、再落旧段。
_LEGACY_TO_CONFIG = {
    "locks.visualStyle.imagePrompt": "channek.visual.imagePrompt",
    "locks.visualStyle.negativePrompt": "channek.visual.negativePrompt",
    "locks.visualStyle.seed": "channek.visual.seed",
    "locks.visualStyle.sref": "channek.visual.sref",
    "captions.highlight": "channek.captions.highlight",
    "captions.maxLines": "channek.captions.maxLines",
    "captions.wordsPerLine": "channek.captions.wordsPerLine",
    "captions.stroke": "channek.captions.stroke",
    "voice.default": "channek.voice.default",
    "locks.motionSound.sound.vibe": "sound.vibe",
    "locks.motionSound.sound.bgm.enabled": "sound.bgmEnabled",
    "locks.motionSound.sound.bgm.genre": "sound.bgmGenre",
    "locks.motionSound.sound.bgm.noVocals": "sound.bgmNoVocals",
    "locks.motionSound.sound.sfx.palette": "sound.sfxPalette",
    "locks.motionSound.sound.sfx.brightnessCeilingHz": "sound.sfxBrightnessCeilingHz",
    "locks.motionSound.sound.sonicLogo.enabled": "sound.sonicLogoEnabled",
    "locks.motionSound.sound.intro.enabled": "sound.introEnabled",
    "locks.motionSound.sound.intro.file": "sound.introFile",
    "locks.motionSound.sound.intro.source": "sound.introSource",
    "audio.bed.floorDb": "sound.bedFloorDb",
}

# audio 六个合成参数已归「AI 配音」插件的频道级参数段（plugin id 含点号，走不了点号 walk）。
_AUDIO_PLUGIN_ID = "channek.generation-voice-lab"
_AUDIO_KEYS = {"ttsCfg", "ttsTimesteps", "headBreath", "tailBreath", "paceEven", "toneEven"}


def _split_list(raw: Any) -> list:
    """config 七型没有数组——数组判据以逗号文本声明（bgmMood/sfxAvoid），读回时重组。"""
    if isinstance(raw, list):
        return raw
    if isinstance(raw, str) and raw.strip():
        return [item.strip() for item in raw.split(",") if item.strip()]
    return []


def _walk(obj: Any, dotted: str) -> Any:
    """在嵌套 dict 里走点号路径；走不通返回 None（与 get() 的缺席语义一致）。"""
    cur = obj
    for key in dotted.split("."):
        if isinstance(cur, dict) and key in cur:
            cur = cur[key]
        else:
            return None
    return cur


class Channel:
    """解析好的风格卡（card.json）+ 频道根。"""

    def __init__(self, root: Path, data: dict):
        self.root = root
        self.data = data or {}
        # config 声明拍平成 {key: value}（有值才收；fileRef 的值就是卡内相对路径）
        self._config: dict = {}
        for section in (self.data.get("config") or {}).get("sections", []) or []:
            for field in section.get("fields", []) or []:
                if "value" in field and field.get("value") is not None:
                    self._config[field["key"]] = field["value"]
        self._sidecars: dict = {}

    def _sidecar(self, name: str) -> dict:
        """频道侧车（`.channek/local/<name>`）——本机接线值的家。缺失 / 坏 JSON 一律空 dict。"""
        if name not in self._sidecars:
            data: Any = {}
            path = self.root / LOCAL_DIR / name
            try:
                if path.is_file():
                    data = json.loads(path.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001 —— 侧车是可选增强，坏了退回卡段，绝不炸调用方
                data = {}
            self._sidecars[name] = data if isinstance(data, dict) else {}
        return self._sidecars[name]

    def get(self, dotted: str, default: Any = None) -> Any:
        """点号路径取值。解析序：config 声明（直接键 / 旧路径映射）> 侧车 > 旧段原位 > default。

        旧 skill 写的 `locks.visualStyle.imagePrompt` 与新写法 `channek.visual.imagePrompt`
        读到的是同一个声明值；数组判据（bgm.mood / sfx.avoid / bgm.bpm / publish.accounts）
        由映射层重组；本机接线（voice.profiles / publish.profileDir·debugPort）读频道侧车。
        """
        if dotted in self._config:
            return self._config[dotted]
        mapped = _LEGACY_TO_CONFIG.get(dotted)
        if mapped is not None and mapped in self._config:
            return self._config[mapped]
        if dotted == "voice.profiles" or dotted.startswith("voice.profiles."):
            hit = _walk(self._sidecar("voice.json"), dotted.split(".", 1)[1])
            if hit is not None:
                return hit
        if dotted == "publish":
            merged = dict(_walk(self.data, "publish") or {})
            accounts = _split_list(self._config.get("channek.publish.accounts"))
            if accounts:
                merged["accounts"] = accounts
            merged.update(self._sidecar("publish.json"))
            if merged:
                return merged
        elif dotted.startswith("publish."):
            hit = _walk(self._sidecar("publish.json"), dotted.split(".", 1)[1])
            if hit is not None:
                return hit
            if dotted == "publish.accounts":
                accounts = _split_list(self._config.get("channek.publish.accounts"))
                if accounts:
                    return accounts
        if dotted == "locks.motionSound.sound.bgm.mood":
            mood = _split_list(self._config.get("sound.bgmMood"))
            if mood:
                return mood
        if dotted == "locks.motionSound.sound.sfx.avoid":
            avoid = _split_list(self._config.get("sound.sfxAvoid"))
            if avoid:
                return avoid
        if dotted == "locks.motionSound.sound.bgm.bpm":
            low, high = self._config.get("sound.bgmBpmMin"), self._config.get("sound.bgmBpmMax")
            if low is not None and high is not None:
                return [low, high]
        if dotted.startswith("audio."):
            key = dotted.split(".", 1)[1]
            if key in _AUDIO_KEYS:
                plugin = (self.data.get("pluginSettings") or {}).get(_AUDIO_PLUGIN_ID) or {}
                if key in plugin:
                    return plugin[key]
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
        """取某音色 profile（默认 voice.default）。接线键住频道侧车 voice.json > 卡段兜底。

        **弃用中**：本机接线已迁 app 的能力目录（见 `capability()`），侧车 voice.json 已退役。
        这个方法留给还没迁的调用方兜底，读不到就返回空 dict。
        """
        key = key or self.get("voice.default")
        if not key:
            return {}
        profiles = self.get("voice.profiles", {}) or {}
        return profiles.get(key, {}) if isinstance(profiles, dict) else {}

    def capability(self, capability_id: str, prefer: Optional[str] = None) -> dict:
        """取一条**可以直接照着调**的能力绑定。

        这是 skill 与插件之间唯一的耦合面：app 在装插件 / 改设置 / 开频道时把三层配置合并、
        provider 选路、路径解析全算完，物化成一个 JSON；这里只是把答案读出来。于是 skill
        既不认识插件、也不认识配置分层，更不需要 app 在跑。

        返回形如 `{"providerId", "invoke", "params", "offline", ...}`；没有可用候选返回 {}。
        `invoke.args` 里只剩调用期占位符（`{{input.*}}` / `{{outputDir}}` / `{{runId}}`
        / `{{tmpDir}}`），由调用方自己替。

        频道目录优先、机器级兜底：后者缺频道个性（音色 / 画风 / 尺寸），所以走到兜底时
        **必须如实报告**——静默降级会产出「看起来对但不是这个频道」的东西。
        """
        catalog = self._read_json(self.root / ".channek" / "local" / "capabilities.json")
        source = "channel"
        if not catalog:
            catalog = self._read_json(Path.home() / ".channek" / "capabilities.json")
            source = "machine-fallback"
        entry = (catalog.get("capabilities") or {}).get(capability_id) or {}
        candidates = entry.get("candidates") or []
        if prefer:
            candidates = sorted(candidates, key=lambda c: c.get("providerId") != prefer)
        if not candidates:
            return {}
        return {**candidates[0], "catalog": source}

    def invoke_capability(
        self,
        capability_id: str,
        inputs: Optional[dict] = None,
        out_dir: Optional[Path] = None,
        prefer: Optional[str] = None,
        run_id: Optional[str] = None,
    ) -> dict:
        """调用一条能力，返回 `{"ok", "path", "backend", "catalog", "attempts"}`。

        这是 skill 迁移的落点：原来每个 skill 各写一遍「后端在哪、venv 是哪个、参数怎么拼」，
        现在只说「我要 channek.tts，正文是这个」。**怎么调**由插件声明、由 app 物化进能力目录。

        候选链按序试，**回退不掩盖失败**：每个候选为什么没用上都记在 `attempts` 里——
        否则用户会以为自己点名的那家在跑。
        """
        import subprocess
        import time
        import urllib.request

        inputs = inputs or {}
        out_dir = Path(out_dir or self.root / ".channek" / "local" / "out")
        out_dir.mkdir(parents=True, exist_ok=True)
        run_id = run_id or f"{capability_id.split('.')[-1]}-{int(time.time() * 1000)}"
        tmp_dir = Path(tempfile.mkdtemp(prefix="channek-cap-"))

        catalog = self._read_json(self.root / ".channek" / "local" / "capabilities.json")
        source = "channel"
        if not catalog:
            catalog = self._read_json(Path.home() / ".channek" / "capabilities.json")
            source = "machine-fallback"
        entry = (catalog.get("capabilities") or {}).get(capability_id) or {}
        candidates = list(entry.get("candidates") or [])
        if prefer:
            candidates.sort(key=lambda c: c.get("providerId") != prefer)
        if not candidates:
            miss = entry.get("unavailable") or []
            hint = miss[0].get("hint") if miss else "先在 app 里装一个提供这条能力的插件"
            return {"ok": False, "catalog": source, "attempts": miss,
                    "error": f"没有可用的 {capability_id}：{hint}"}

        def fill(value: str) -> str:
            out = value.replace("{{outputDir}}", str(out_dir))
            out = out.replace("{{runId}}", run_id).replace("{{tmpDir}}", str(tmp_dir))
            for key, val in inputs.items():
                # `@file` 修饰：大载荷落临时文件再传路径——三千字的稿子上 argv 会撞 ARG_MAX，
                # 而撞不撞取决于稿子长度，那种「大部分时候能跑」的故障最难查。
                token = "{{input.%s@file}}" % key
                if token in out:
                    holder = tmp_dir / f"{key}.txt"
                    holder.write_text(str(val), encoding="utf-8")
                    out = out.replace(token, str(holder))
                out = out.replace("{{input.%s}}" % key, str(val))
            return out

        attempts = []
        for binding in candidates:
            invoke = binding.get("invoke") or {}
            provider = binding.get("providerId", "?")
            try:
                if invoke.get("kind") == "command":
                    args = [fill(str(a)) for a in invoke.get("args") or []]
                    proc = subprocess.run(
                        [fill(str(invoke.get("program")))] + args,
                        capture_output=True, text=True,
                        timeout=(invoke.get("timeoutMs") or 600000) / 1000,
                    )
                    payload = {}
                    for line in reversed((proc.stdout or "").strip().splitlines()):
                        try:
                            payload = json.loads(line)
                            break
                        except Exception:
                            continue
                    # 成功要两条同时成立：退出码 0 **且** 末行 JSON ok——只看退出码会把
                    # 「打印了错误但退 0」当成功，只看 JSON 会把「进程被 kill」当没发生。
                    if proc.returncode == 0 and payload.get("ok") is not False:
                        path = payload.get("path")
                        if not path:
                            # 不打印 JSON 的后端（voxcpm 这类通用 CLI 就是）走 `files-in-outdir`：
                            # 产物路径本来就由 args 里的 `--out` 指定，去 outputDir 里认最新的那个。
                            glob = (invoke.get("result") or {}).get("glob") or "*"
                            made = sorted(out_dir.glob(glob), key=lambda f: f.stat().st_mtime)
                            path = str(made[-1]) if made else None
                        return {"ok": True, "path": path, "backend": provider,
                                "catalog": source, "attempts": attempts, "meta": payload}
                    attempts.append({"backend": provider, "status": "failed",
                                     "error": (proc.stderr or proc.stdout or "")[-400:]})
                    continue
                if invoke.get("kind") == "http":
                    body = json.dumps(
                        {k: fill(str(v)) for k, v in (invoke.get("body") or {}).get("template", {}).items()}
                    ).encode()
                    request = urllib.request.Request(
                        fill(str(invoke.get("url"))), data=body, method=invoke.get("method", "POST"),
                        headers=invoke.get("headers") or {"Content-Type": "application/json"},
                    )
                    with urllib.request.urlopen(request, timeout=(invoke.get("timeoutMs") or 120000) / 1000) as resp:
                        blob = resp.read()
                    target = Path(fill(str((invoke.get("result") or {}).get("saveAs") or out_dir / f"{run_id}.bin")))
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(blob)
                    return {"ok": True, "path": str(target), "backend": provider,
                            "catalog": source, "attempts": attempts}
                attempts.append({"backend": provider, "status": "unavailable",
                                 "error": "这条 provider 需要 app 打开着（module 形态）"})
            except Exception as exc:
                attempts.append({"backend": provider, "status": "failed", "error": str(exc)})
        return {"ok": False, "catalog": source, "attempts": attempts,
                "error": f"{capability_id} 的候选都没跑通"}

    @staticmethod
    def _read_json(path: Path) -> dict:
        """读一份 JSON；缺失 / 坏形状一律返回空 dict，绝不炸调用方。"""
        try:
            with open(path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}

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
        """画风锁四参——从 config 声明（channek.visual.*）重组；老卡落回 locks 段。"""
        lock = {
            key: self._config[f"channek.visual.{key}"]
            for key in ("imagePrompt", "negativePrompt", "seed", "sref")
            if f"channek.visual.{key}" in self._config
        }
        return lock or (self.get("locks.visualStyle", {}) or {})

    @property
    def sound(self) -> dict:
        """声场口味——从 config 扁平声明（sound.*）重组成旧嵌套形状；老卡落回 locks 段。"""
        cfg = self._config
        if "sound.vibe" not in cfg:
            return self.get("locks.motionSound.sound", {}) or {}
        bgm = {
            "enabled": cfg.get("sound.bgmEnabled"),
            "genre": cfg.get("sound.bgmGenre"),
            "mood": _split_list(cfg.get("sound.bgmMood")),
            "noVocals": cfg.get("sound.bgmNoVocals"),
        }
        if cfg.get("sound.bgmBpmMin") is not None and cfg.get("sound.bgmBpmMax") is not None:
            bgm["bpm"] = [cfg["sound.bgmBpmMin"], cfg["sound.bgmBpmMax"]]
        return {
            "vibe": cfg.get("sound.vibe"),
            "bgm": {k: v for k, v in bgm.items() if v is not None},
            "sfx": {
                k: v
                for k, v in {
                    "palette": cfg.get("sound.sfxPalette"),
                    "brightnessCeilingHz": cfg.get("sound.sfxBrightnessCeilingHz"),
                    "avoid": _split_list(cfg.get("sound.sfxAvoid")) or None,
                }.items()
                if v is not None
            },
            "sonicLogo": {"enabled": cfg.get("sound.sonicLogoEnabled")},
            "intro": {
                k: v
                for k, v in {
                    "enabled": cfg.get("sound.introEnabled"),
                    "file": cfg.get("sound.introFile"),
                    "source": cfg.get("sound.introSource"),
                }.items()
                if v is not None
            },
        }

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


def load_secret(res_id: str, instance: Optional[str] = None,
                start: Optional[str] = None) -> Optional[dict]:
    """按资源 id 取一份凭据 —— `load_secret("media_generation.volcengine", "personal")`。

    两种凭据源，都**不含家目录硬编码**（随卡/随 skill 分发时绝不指向他人凭据库）：
      ① 资源中枢（$AGENTS_RESOURCES 指向的目录，其下 secrets/<资源>.json）
      ② 频道树内 `_secrets/resources.json`（带外下发的老结构，按 category→provider→variant）
    都找不到返回 None，调用方自行降级——绝不抛。
    """
    env = os.environ.get(ENV_SECRETS) or os.environ.get(ENV_SECRETS_HOME)
    if env:
        base = Path(env).expanduser()
        if base.is_file():
            base = base.parent
        for cand in (base, base / "resources"):
            # 中枢里一个资源一个目录，位置由索引 registry.json 的 path 给出
            idx = cand / "src" / "registry.json"
            if not idx.is_file():
                continue
            try:
                info = json.loads(idx.read_text("utf-8"))["resources"][res_id]
                f = cand / "secrets" / info["path"] / "secret.json"
                data = json.loads(f.read_text("utf-8"))
            except (KeyError, OSError, json.JSONDecodeError):
                break
            if instance is None:
                instance = next(iter(data), None)
            return data.get(instance) if instance else None

    hit = find_secrets(start)
    if hit and hit.is_file():
        node: Any = json.loads(hit.read_text("utf-8"))
        for part in res_id.split("."):
            if not isinstance(node, dict) or part not in node:
                return None
            node = node[part]
        if isinstance(node, dict):
            if instance and instance in node:
                return node[instance]
            sub = [v for k, v in node.items()
                   if isinstance(v, dict) and not k.startswith("_")]
            return sub[0] if sub else node
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
    # `caps` / `invoke` 让**非 Python 的 skill**（bash / node / 任何语言）也能用能力目录：
    # 一条命令进去，一行 JSON 出来。Python skill 直接 import 本模块即可，不必绕这一层。
    if args and args[0] == "caps":
        catalog = ch._read_json(ch.root / ".channek" / "local" / "capabilities.json") or \
            ch._read_json(Path.home() / ".channek" / "capabilities.json")
        for cap, entry in sorted((catalog.get("capabilities") or {}).items()):
            names = [c.get("providerId") for c in entry.get("candidates") or []]
            mark = "" if entry.get("offline") else "  (需 app 打开着)"
            print(f"{cap:24} {', '.join(names) or '<无可用 provider>'}{mark}")
        return 0
    if args and args[0] == "invoke":
        if len(args) < 2:
            print("用法: channek.py invoke <能力id> [键=值 ...] [--out 目录]", file=sys.stderr)
            return 2
        rest, out_dir, inputs = args[2:], None, {}
        while rest:
            token = rest.pop(0)
            if token == "--out":
                out_dir = rest.pop(0) if rest else None
            elif "=" in token:
                key, _, value = token.partition("=")
                inputs[key] = value
        result = ch.invoke_capability(args[1], inputs, out_dir=out_dir)
        # 末行一行紧凑 JSON——与 skill 生态既有的结果契约一致，调用方 tail -1 即可。
        print(json.dumps(result, ensure_ascii=False))
        return 0 if result.get("ok") else 1
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
