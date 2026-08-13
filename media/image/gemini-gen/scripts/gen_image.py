#!/usr/bin/env python3
"""Gemini 生图 CLI：默认走本机反代服务（antigravity2api-nodejs，proxy 后端），
可选切回 Gemini 网页会员号 cookie 方式（cookie，旧方式）。

两条后端配额池不互通，分别管理：
  proxy  —— 反代账号池（Antigravity/Cloud Code Assist），多账号轮询在反代服务里做，
             凭据读 skill 目录下 proxy_config.json（见 proxy_config.example.json 模板），
             找不到时经 $AGENTS_RESOURCES 读资源中枢的 llm.antigravity2api（只认环境变量，
             不猜任何家目录路径；别人用本 skill 走 proxy_config.json 即可）。
  cookie —— Gemini 网页版会员号（Pro/Advanced 订阅）cookie，凭据配置见本文件下方
             cookie 相关代码 + skill 根目录 accounts.json，多账号 LRU 负载 + 撞额度跳号。

依赖（由 gen-image.sh 经 uv 注入）：gemini_webapi、browser-cookie3（仅 cookie 后端用到，
proxy 后端只用标准库）。
账号身份以 Chrome Local State 的 profile→email 映射为准（Gemini 自报邮箱不可靠）。
"""

from __future__ import annotations

import argparse
import asyncio
import base64
import json
import mimetypes
import os
import random
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

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


def log(msg: str) -> None:
    print(f"[gemini-gen] {msg}", file=sys.stderr)


# ==================== backend: proxy（默认，antigravity2api-nodejs 反代）====================
# 凭据 / 端点优先读 skill 目录下 proxy_config.json（见 load_proxy_config），本机私有的
# $AGENTS_RESOURCES 资源中枢只是没配 proxy_config.json 时的兜底，不是主路径。
# 多账号轮询、撞额度自动跳号都在反代服务里做，脚本这边只是个薄 HTTP 客户端。

DEFAULT_PROXY_IMAGE_MODEL = "gemini-3.1-flash-image"


PROXY_CONFIG_CANDIDATES = [
    SKILL_DIR / "proxy_config.json",
    Path.home() / ".config/gemini-gen/proxy_config.json",
]


def load_proxy_config() -> dict:
    """读反代配置，返回统一字段 {base_url, api_key, default_model}。

    三级发现（**本文件随公开 skill 分发，绝不写死任何家目录路径**）：
      ① 环境变量 GEMINI_PROXY_BASE_URL / GEMINI_PROXY_API_KEY
      ② skill 目录或 ~/.config/gemini-gen 下的 proxy_config.json（XDG 标准位置）
      ③ $AGENTS_RESOURCES 指向的资源中枢 llm.antigravity2api.local
    """
    env_url = os.environ.get("GEMINI_PROXY_BASE_URL")
    env_key = os.environ.get("GEMINI_PROXY_API_KEY")
    if env_url and env_key:
        return {"base_url": env_url, "api_key": env_key,
                "default_model": os.environ.get("GEMINI_PROXY_MODEL",
                                                DEFAULT_PROXY_IMAGE_MODEL)}
    for p in PROXY_CONFIG_CANDIDATES:
        if p.exists():
            cfg = json.loads(p.read_text())
            if cfg.get("base_url") and cfg.get("api_key"):
                return cfg
    local = _from_resource_hub("llm.antigravity2api", "local")
    if local and local.get("base_url") and local.get("api_key"):
        return {
            "base_url": local["base_url"],
            "api_key": local["api_key"],
            "default_model": local.get("default_image_model", DEFAULT_PROXY_IMAGE_MODEL),
        }
    raise SystemExit(
        f"[gemini-gen] 未找到反代配置。三选一：\n"
        f"  · 设 GEMINI_PROXY_BASE_URL / GEMINI_PROXY_API_KEY\n"
        f"  · 把 {SKILL_DIR / 'proxy_config.example.json'} 复制为 "
        f"{SKILL_DIR / 'proxy_config.json'}（或 ~/.config/gemini-gen/proxy_config.json）\n"
        f"  · 设 $AGENTS_RESOURCES 指向资源中枢"
    )


def _from_resource_hub(res_id: str, instance: str) -> dict | None:
    """经 $AGENTS_RESOURCES 读资源中枢的一条凭据；没设或读不到就返回 None。

    只认环境变量——**不猜任何家目录路径**，这样本文件随 skill 公开分发时
    不会指向别人机器上并不存在的私有凭据库。
    """
    hub = os.environ.get("AGENTS_RESOURCES") or os.environ.get("AGENTS_HOME")
    if not hub:
        return None
    base = Path(hub).expanduser()
    if base.is_file():
        base = base.parent
    for cand in (base, base / "resources"):
        # 中枢里一个资源一个目录，位置由索引 registry.json 的 path 给出
        idx = cand / "src" / "registry.json"
        if not idx.is_file():
            continue
        try:
            info = json.loads(idx.read_text("utf-8"))["resources"][res_id]
            return json.loads((cand / "secrets" / info["path"] / "secret.json")
                              .read_text("utf-8")).get(instance)
        except Exception:
            return None
    return None


def check_proxy_alive(base_url: str) -> bool:
    """只判断服务有没有在监听、能不能连上；HTTP 层面报什么状态码都算活（哪怕 401/404），
    真正的鉴权失败留给正式请求去报错，这里不该因为没带 Authorization 就误判成"服务没启动"。
    """
    try:
        urllib.request.urlopen(f"{base_url}/models", timeout=3)
        return True
    except urllib.error.HTTPError:
        return True
    except Exception:
        return False


def image_to_data_url(path: str) -> str:
    p = Path(path).expanduser()
    mime = mimetypes.guess_type(p.name)[0] or "image/png"
    b64 = base64.b64encode(p.read_bytes()).decode()
    return f"data:{mime};base64,{b64}"


def generate_via_proxy(prompt: str, refs: list[str], out: Path, model: str,
                       size: str) -> list[str]:
    cfg = load_proxy_config()
    base_url = cfg["base_url"].rstrip("/")
    api_key = cfg["api_key"]

    if not check_proxy_alive(base_url):
        raise SystemExit(
            f"[gemini-gen] 反代服务未运行（{base_url}）。请先 `app run antigravity2api` 再重试。"
        )

    full_model = model if (size == "1K" or model.endswith(size)) else f"{model}-{size}"
    content: list[dict] = [{"type": "text", "text": prompt}]
    for r in refs:
        content.append({"type": "image_url", "image_url": {"url": image_to_data_url(r)}})

    body = json.dumps({
        "model": full_model,
        "messages": [{"role": "user", "content": content}],
        "stream": False,
    }).encode()

    last_err = ""
    result = None
    for attempt in range(2):  # 撞到刚被反代标坏的账号时，重试一次通常会换到健康账号
        req = urllib.request.Request(
            f"{base_url}/chat/completions",
            data=body,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read())
            break
        except urllib.error.HTTPError as e:
            last_err = e.read().decode(errors="replace")[:300]
            log(f"反代请求失败（第 {attempt + 1} 次）：{e.code} {last_err}")
        except Exception as e:
            last_err = str(e)
            log(f"反代请求异常（第 {attempt + 1} 次）：{last_err[:300]}")
    if result is None:
        raise SystemExit(f"[gemini-gen] 反代出图失败：{last_err}")

    reply_text = result["choices"][0]["message"]["content"]
    urls = re.findall(r"!\[image\]\((.*?)\)", reply_text)
    if not urls:
        raise SystemExit(f"[gemini-gen] 反代未返回图片，模型回应：{reply_text[:200]}")

    out.parent.mkdir(parents=True, exist_ok=True)
    saved: list[str] = []
    for i, url in enumerate(urls):
        fname = out.name if len(urls) == 1 else f"{out.stem}_{i}{out.suffix}"
        dest = out.parent / fname
        with urllib.request.urlopen(url, timeout=60) as r:
            dest.write_bytes(r.read())
        saved.append(str(dest))
    return saved


def run_proxy(args) -> int:
    out = Path(args.out).expanduser()
    prompt = args.prompt
    if args.aspect:
        prompt = f"{prompt}\n(aspect ratio: {args.aspect})"
    refs = args.ref or []
    cfg = load_proxy_config()
    model = args.proxy_model or cfg.get("default_model", DEFAULT_PROXY_IMAGE_MODEL)

    saved = generate_via_proxy(prompt, refs, out, model, args.size)
    log(f"出图模型：{model}（size={args.size}）")
    for p in saved:
        print(p)
    return 0


# ==================== backend: cookie（旧方式，Gemini 网页会员号）====================
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
    import browser_cookie3 as bc3

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
    from gemini_webapi import GeminiClient

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


async def run_cookie(args) -> int:
    from gemini_webapi.constants import Model

    model_map = {"flash": Model.BASIC_FLASH, "pro": Model.BASIC_PRO}

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
    model = model_map[args.model]

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
    ap = argparse.ArgumentParser(description="Gemini 生图（默认反代 proxy 后端，可选 cookie 会员号后端）")
    ap.add_argument("--backend", choices=["proxy", "cookie"], default="proxy",
                    help="出图后端：proxy=本机 antigravity2api-nodejs 反代（默认，Antigravity 账号池配额，"
                         "免 Chrome profile）| cookie=Gemini 网页会员号 cookie（旧方式，网页订阅配额，"
                         "两者配额池不通用）")
    ap.add_argument("--prompt", required=True, help="图像描述（越具体越好，中英文均可）")
    ap.add_argument("--out", required=True, help="输出图片路径，父目录自动建；多图自动加 _0/_1")
    ap.add_argument("--ref", action="append", help="参考图路径，可重复（锁角色/风格；两个后端都支持）")
    ap.add_argument("--aspect", help="宽高比提示，如 16:9 / 1:1 / 9:16（两个后端都是 best-effort，写进提示词）")
    # cookie 后端专用
    ap.add_argument("--account", help="[cookie 后端] 指定账号（accounts.json 里的名字）；不传则全部号负载均衡")
    ap.add_argument("--model", choices=["flash", "pro"], default="flash",
                    help="[cookie 后端] 出图模型：flash=Nano Banana 2(默认/宽额度) | pro=Nano Banana Pro(更高质量)")
    # proxy 后端专用
    ap.add_argument("--proxy-model", dest="proxy_model",
                    help="[proxy 后端] 反代模型名，默认读 proxy_config.json 的 default_model"
                         f"（缺省 {DEFAULT_PROXY_IMAGE_MODEL}）")
    ap.add_argument("--size", choices=["1K", "2K", "4K"], default="1K",
                    help="[proxy 后端] 出图分辨率档位，默认 1K")
    args = ap.parse_args()

    if args.backend == "proxy":
        return run_proxy(args)
    return asyncio.run(run_cookie(args))


if __name__ == "__main__":
    sys.exit(main())
