#!/usr/bin/env python3
"""Gemini 会员号生图 CLI：多账号 cookie 隔离 + 负载均衡 + 撞额度自动跳号。

依赖（由 gen-image.sh 经 uv 注入）：gemini_webapi、browser-cookie3。
账号身份以 Chrome Local State 的 profile→email 映射为准（Gemini 自报邮箱不可靠）。
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import random
import sys
import time
from pathlib import Path

import browser_cookie3 as bc3
from gemini_webapi import GeminiClient
from gemini_webapi.constants import Model

CHROME_BASE = Path.home() / "Library/Application Support/Google/Chrome"
STATE_PATH = Path.home() / ".config/gemini-gen/state.json"
COOLDOWN_SECONDS = 2 * 3600  # 撞 limit 后该号冷却时长，过后自动重试
# pacing：每次出图请求前随机停顿，模拟人手节奏、降低被反自动化限流的概率。
JITTER_MIN, JITTER_MAX = 0.8, 2.5

# 会员账号配置（名字 → 邮箱）从外部文件读，不硬编码进代码、不入 git。
# 查找顺序：skill 目录/accounts.json → ~/.config/gemini-gen/accounts.json。
# 模板见 skill 目录下 accounts.example.json。
SKILL_DIR = Path(__file__).resolve().parent.parent
ACCOUNTS_CANDIDATES = [
    SKILL_DIR / "accounts.json",
    Path.home() / ".config/gemini-gen/accounts.json",
]


def load_members() -> dict[str, str]:
    """读账号配置，返回 名字→邮箱。找不到则报错指向 example。"""
    for p in ACCOUNTS_CANDIDATES:
        if p.exists():
            data = json.loads(p.read_text())
            members = data.get("members", data) if isinstance(data, dict) else {}
            if members:
                return {str(k): str(v) for k, v in members.items()}
    raise SystemExit(
        f"[gemini-gen] 未找到账号配置。请把 {SKILL_DIR / 'accounts.example.json'} "
        f"复制为 {SKILL_DIR / 'accounts.json'}（或 ~/.config/gemini-gen/accounts.json）"
        "并填入你的 Gemini 会员号邮箱。"
    )


LIMIT_MARKERS = ("limit resets", "check your usage", "usage in settings")

# 出图模型：flash=Nano Banana 2(宽额度/快/默认)，pro=Nano Banana Pro(更高质量/额度紧)。
# ⚠️ 不能用默认 UNSPECIFIED——它路由到的图额度桶极小，会误报 "limit resets"。
MODEL_MAP = {
    "flash": Model.BASIC_FLASH,
    "pro": Model.BASIC_PRO,
}


def log(msg: str) -> None:
    print(f"[gemini-gen] {msg}", file=sys.stderr)


# ---------- profile / cookie ----------

def discover_profiles() -> dict[str, Path]:
    """email → profile 目录。读 Chrome Local State 的 info_cache。"""
    local_state = CHROME_BASE / "Local State"
    cache = json.loads(local_state.read_text()).get("profile", {}).get("info_cache", {})
    out: dict[str, Path] = {}
    for prof, meta in cache.items():
        email = (meta.get("user_name") or "").lower()
        if email:
            out[email] = CHROME_BASE / prof
    return out


def cookie_file(profile_dir: Path) -> Path | None:
    for rel in ("Network/Cookies", "Cookies"):
        p = profile_dir / rel
        if p.exists():
            return p
    return None


def read_cookies(profile_dir: Path) -> tuple[str | None, str | None]:
    cf = cookie_file(profile_dir)
    if not cf:
        return None, None
    cj = bc3.chrome(cookie_file=str(cf), domain_name="google.com")
    psid = psidts = None
    for c in cj:
        if c.name == "__Secure-1PSID":
            psid = c.value
        elif c.name == "__Secure-1PSIDTS":
            psidts = c.value
    return psid, psidts


# ---------- 负载状态 ----------

def load_state() -> dict:
    try:
        s = json.loads(STATE_PATH.read_text())
    except Exception:
        s = {}
    s.setdefault("last_used", {})  # account -> epoch（LRU 分摊用）
    s.setdefault("cooldown", {})   # account -> epoch_until（撞限流冷却）
    return s


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2))


def mark_used(state: dict, name: str) -> None:
    state.setdefault("last_used", {})[name] = time.time()
    save_state(state)


def mark_cooldown(state: dict, name: str) -> None:
    state.setdefault("cooldown", {})[name] = time.time() + COOLDOWN_SECONDS
    state.setdefault("last_used", {})[name] = time.time()
    save_state(state)


def pick_order(names: list[str], state: dict) -> list[str]:
    """LRU 优先：最久没用的号排前面，自然分摊请求；冷却中的排队尾兜底（不剔除）。"""
    now = time.time()
    cd = state.get("cooldown", {})
    lu = state.get("last_used", {})
    fresh = sorted([n for n in names if cd.get(n, 0) <= now], key=lambda n: lu.get(n, 0))
    cooling = sorted([n for n in names if cd.get(n, 0) > now], key=lambda n: cd.get(n, 0))
    return fresh + cooling


# ---------- 出图 ----------

def is_quota_exhausted(resp) -> bool:
    if getattr(resp, "images", None):
        return False
    text = (getattr(resp, "text", "") or "").lower()
    return any(m in text for m in LIMIT_MARKERS)


async def generate_with(account: str, profile_dir: Path, prompt: str,
                        refs: list[str], out: Path, model) -> list[str] | None:
    """单账号出图。成功返回保存路径列表；撞额度返回 None；其它异常抛出。"""
    psid, psidts = read_cookies(profile_dir)
    if not psid:
        log(f"{account}: 该 profile 读不到 __Secure-1PSID（是否登录了 gemini？）")
        return None
    client = GeminiClient(psid, psidts)
    await client.init(timeout=60)
    try:
        kwargs = {"model": model}
        if refs:
            kwargs["files"] = refs
        await asyncio.sleep(random.uniform(JITTER_MIN, JITTER_MAX))  # pacing
        resp = await client.generate_content(prompt, **kwargs)
        if is_quota_exhausted(resp):
            log(f"{account}: 额度已用完（limit resets）")
            return None
        if not resp.images:
            log(f"{account}: 未返回图片，文本回应：{(resp.text or '')[:120]}")
            return None
        out.parent.mkdir(parents=True, exist_ok=True)
        imgs = resp.images
        saved: list[str] = []
        for i, img in enumerate(imgs):
            fname = out.name if len(imgs) == 1 else f"{out.stem}_{i}{out.suffix}"
            path = await img.save(path=str(out.parent), filename=fname, verbose=False)
            saved.append(path or str(out.parent / fname))
        return saved
    finally:
        await client.close()


async def run(args) -> int:
    members = load_members()
    profiles = discover_profiles()

    def resolve(name: str) -> Path | None:
        email = members.get(name, name if "@" in name else None)
        if not email:
            return None
        return profiles.get(email.lower())

    out = Path(args.out).expanduser()
    prompt = args.prompt
    if args.aspect:
        prompt = f"{prompt}\n(aspect ratio: {args.aspect})"
    refs = args.ref or []
    model = MODEL_MAP[args.model]

    state = load_state()

    # 指定账号：只用它，不跳号
    if args.account:
        pdir = resolve(args.account)
        if not pdir:
            log(f"找不到账号 {args.account} 的 profile。已知：{list(profiles)}")
            return 2
        saved = await generate_with(args.account, pdir, prompt, refs, out, model)
        if not saved:
            mark_cooldown(state, args.account)
            log(f"{args.account} 出图失败（额度/限流/登录问题）。")
            return 1
        mark_used(state, args.account)
        for p in saved:
            print(p)
        return 0

    # 负载均衡：LRU 分摊 + 跳号
    names = [n for n in members if resolve(n)]
    if not names:
        log("没有任何可用会员号 profile。请确认已为会员号建独立 Chrome profile 并登录 gemini。")
        return 2
    order = pick_order(names, state)
    log(f"负载顺序（LRU）：{order}")
    for name in order:
        pdir = resolve(name)
        try:
            saved = await generate_with(name, pdir, prompt, refs, out, model)
        except Exception as e:  # 网络/解析等异常也跳号
            log(f"{name}: 异常跳号 {type(e).__name__}: {str(e)[:120]}")
            saved = None
        if saved:
            mark_used(state, name)
            log(f"出图账号：{name}")
            for p in saved:
                print(p)
            return 0
        mark_cooldown(state, name)  # 失败（额度/限流）→ 冷却 + 降优先级
    log("所有会员号都出图失败（额度全满 / 被限流 / 登录失效）。稍后再试或检查 profile 登录态。")
    return 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Gemini 会员号生图（多账号负载均衡）")
    ap.add_argument("--prompt", required=True, help="图像描述（越具体越好，中英文均可）")
    ap.add_argument("--out", required=True, help="输出 PNG 路径，父目录自动建；多图自动加 _0/_1")
    ap.add_argument("--account", help="指定账号（accounts.json 里的名字）；不传则全部号负载均衡")
    ap.add_argument("--model", choices=list(MODEL_MAP), default="flash",
                    help="出图模型：flash=Nano Banana 2(默认/宽额度) | pro=Nano Banana Pro(更高质量)")
    ap.add_argument("--aspect", help="宽高比提示，如 16:9 / 1:1 / 9:16（best-effort，写进提示词）")
    ap.add_argument("--ref", action="append", help="参考图路径，可重复（锁角色/风格）")
    args = ap.parse_args()
    return asyncio.run(run(args))


if __name__ == "__main__":
    sys.exit(main())
