"""provider 抽象 + capability 元数据 + 可用性探测 + 后端调用映射。

单一职责：定义每个生图后端的能力元数据、怎么探测它当前可用、怎么把统一参数
翻译成它认的命令并执行。路由编排在 media_gen.py，这里只回答「这个后端是什么、
能不能跑、怎么跑」。

新增后端 = 在 PROVIDERS 加一条 + 写 _invoke_<id>；不改路由编排。
"""

from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional


# ── 后端 skill 真身 / 软链解析 ──────────────────────────────────────────────
# 优先用 ~/.claude/skills/<skill>（sync 生成的软链），回退到 media/image 同级真身目录。
_CLAUDE_SKILLS = Path.home() / ".claude" / "skills"
_IMAGE_SRC = Path(__file__).resolve().parents[2]  # .../media/image


def resolve_skill_dir(skill: str) -> Optional[Path]:
    """解析某后端 skill 的根目录（软链优先，回退真身）。找不到返 None。"""
    cand = _CLAUDE_SKILLS / skill
    if cand.exists():
        return cand
    cand = _IMAGE_SRC / skill
    if cand.exists():
        return cand
    return None


def _aspect_to_wh(aspect: Optional[str]) -> tuple[int, int]:
    """aspect → comfyui 的 --w/--h（换算表见 reference/providers.md）。"""
    table = {
        "16:9": (1280, 720),
        "9:16": (720, 1280),
        "1:1": (1024, 1024),
        "4:3": (1024, 768),
        "3:4": (768, 1024),
    }
    return table.get((aspect or "").strip(), (1024, 1024))


def _aspect_to_dashscope_size(aspect: Optional[str]) -> str:
    """aspect → 通义万象 `size` 形参（`宽*高`，通义只认固定档位）。

    wanx2.1-t2i 支持 512~1440 区间常见档位；取贴合各 aspect 的官方推荐档。
    """
    table = {
        "16:9": "1280*720",
        "9:16": "720*1280",
        "1:1": "1024*1024",
        "4:3": "1024*768",
        "3:4": "768*1024",
    }
    return table.get((aspect or "").strip(), "1024*1024")


# ── 直连 API key 配置（绝不硬编码：运行时读配置文件）─────────────────────────
# 事实源：Media-Studio/_secrets/media-api-keys.json（从 --out / cwd 上溯找）。
# 也允许环境变量覆盖（MEDIAGEN_KEYS_FILE 指向配置文件）。
def _find_keys_file() -> Optional[Path]:
    env = os.environ.get("MEDIAGEN_KEYS_FILE")
    if env:
        p = Path(env).expanduser()
        return p if p.exists() else None
    starts = [Path.cwd(), _IMAGE_SRC]
    for start in starts:
        cur = start.resolve()
        for _ in range(14):
            cand = cur / "风格卡" / "发布配置" / "media-api-keys.json"
            if cand.exists():
                return cand
            if cur.parent == cur:
                break
            cur = cur.parent
    return None


def load_api_config(vendor: str) -> Optional[dict]:
    """读某直连 API 厂商的配置块（dashscope / ark）。key 只在运行时读，不缓存到磁盘。"""
    f = _find_keys_file()
    if not f:
        return None
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    cfg = data.get(vendor)
    return cfg if isinstance(cfg, dict) else None


# ── 统一调用入参（路由传给后端调用器的东西）──────────────────────────────────
@dataclass
class GenRequest:
    prompt_final: str          # 已拼好 style-lock 的最终提示词
    negative_prompt: str       # style-lock 负向（支持的后端用）
    out_path: Path
    aspect: Optional[str]
    refs: list[Path] = field(default_factory=list)


@dataclass
class InvokeResult:
    status: str                # ok / failed / unavailable / slot
    error: Optional[str] = None
    hint: Optional[str] = None


# ── 审核降级（共用·借 Pixelle / ai-video-gen moderation_fallback）─────────────
# 生图被内容审核拒同样常见（dashscope 等直连 API）。被拒 → prompt 中性化重写 → 重试一次。
# 与 ai-video-gen/scripts/moderation_fallback.py 同一套逻辑，下沉为生图侧共用能力。
_INSPECTION_MARKERS = (
    "datainspectionfailed",
    "data_inspection_failed",
    "inappropriate content",
    "green net check failed",
    "content inspection",
    "safety inspection",
    "risk control",
    "审核",
    "敏感",
    "违规内容",
)

# 保守词替换（保留画面主题，去触发词）。
_NEUTRALIZE_REPLACEMENTS = {
    "害怕": "平静",
    "恐惧": "沉思",
    "危险": "未知",
    "崩溃": "调整",
    "压迫": "压力",
    "攻击": "互动",
    "血": "红色",
    "死亡": "离别",
    "violence": "calm motion",
    "weapon": "object",
    "blood": "red light",
    "explosion": "bloom",
    "attack": "interaction",
    "death": "fading",
}


def is_content_inspection_error(error_message: Optional[str]) -> bool:
    """True 当错误像内容审核/安全检查拒绝（而非网络/超时/服务端错误）。"""
    msg = (error_message or "").lower()
    return any(marker in msg for marker in _INSPECTION_MARKERS)


def neutralize_prompt(prompt: str) -> tuple[str, bool]:
    """中性化重写：词替换 + 中性、品牌安全包络。返 (neutralized, changed)。

    保留画面主题与风格（出图主体不变），只去掉可能触发审核的暴力/危险/极端表达。
    """
    if not prompt or not prompt.strip():
        return prompt, False
    sanitized = prompt
    for src, dst in _NEUTRALIZE_REPLACEMENTS.items():
        sanitized = sanitized.replace(src, dst)
    enveloped = (
        "A calm, restrained, brand-safe image with peaceful atmosphere, "
        "no violence, no danger, no sensitive content. Theme adapted neutrally: "
        + sanitized
    )
    return enveloped, True


# ── 可用性探测 ──────────────────────────────────────────────────────────────
def _probe_gemini() -> tuple[bool, Optional[str]]:
    d = resolve_skill_dir("gemini-gen")
    if not d or not (d / "scripts" / "gen-image.sh").exists():
        return False, "gemini-gen 脚本不存在"
    # accounts.json 在 skill 根或 ~/.config/gemini-gen/
    if (d / "accounts.json").exists() or (
        Path.home() / ".config" / "gemini-gen" / "accounts.json"
    ).exists():
        return True, None
    return False, "未配置 gemini-gen accounts.json"


def _probe_codex() -> tuple[bool, Optional[str]]:
    d = resolve_skill_dir("codex-image-gen")
    if not d or not (d / "scripts" / "gen-image.sh").exists():
        return False, "codex-image-gen 脚本不存在"
    # codex 登录在脚本内自检；这里只确认脚本在
    return True, None


def _probe_comfyui() -> tuple[bool, Optional[str]]:
    d = resolve_skill_dir("comfyui")
    if not d or not (d / "scripts" / "comfy.py").exists():
        return False, "comfyui 脚本不存在"
    # 探测 127.0.0.1:8188 是否可连
    try:
        with socket.create_connection(("127.0.0.1", 8188), timeout=1.5):
            return True, None
    except OSError:
        return False, "ComfyUI 未在 127.0.0.1:8188 运行（先 ./run.sh）"


def _probe_browser() -> tuple[bool, Optional[str]]:
    # 半自动：CLI 探测不到 MCP 会话，永远记 slot
    return False, None


def _probe_api_direct() -> tuple[bool, Optional[str]]:
    if os.environ.get("MEDIAGEN_API_KEY"):
        return True, None
    return False, "需配置 MEDIAGEN_API_KEY 才能启用直连 API 槽位"


def _probe_dashscope() -> tuple[bool, Optional[str]]:
    cfg = load_api_config("dashscope")
    if not cfg:
        return False, "找不到 media-api-keys.json 或缺 dashscope 块"
    if not (cfg.get("api_key") or "").strip():
        return False, "dashscope.api_key 为空"
    return True, None


def _probe_ark() -> tuple[bool, Optional[str]]:
    cfg = load_api_config("ark")
    if not cfg:
        return False, "找不到 media-api-keys.json 或缺 ark 块"
    if not (cfg.get("api_key") or "").strip():
        return False, "ark.api_key 待用户填（Seedream 槽位预留）"
    return True, None


def _probe_jimeng() -> tuple[bool, Optional[str]]:
    if shutil.which("dreamina"):
        # 命令在，但付费 + 需 vip，默认仍当 slot（需用户显式启用）
        return False, "jimeng/Dreamina 付费且需 maestro vip，默认不自动调"
    return False, "dreamina CLI 未安装"


# ── 后端调用器（把统一入参翻成各后端命令并执行）─────────────────────────────
def _run(cmd: list[str]) -> tuple[int, str]:
    """跑命令，返 (退出码, stdout 尾 + stderr 尾 摘要)。"""
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
    except subprocess.TimeoutExpired:
        return 124, "timeout"
    except FileNotFoundError as e:
        return 127, str(e)
    tail = (p.stdout or "").strip().splitlines()[-3:] + (
        (p.stderr or "").strip().splitlines()[-3:]
    )
    return p.returncode, " | ".join(tail)[-400:]


def _invoke_gemini(req: GenRequest) -> InvokeResult:
    d = resolve_skill_dir("gemini-gen")
    sh = d / "scripts" / "gen-image.sh"
    cmd = ["bash", str(sh), "--prompt", req.prompt_final, "--out", str(req.out_path)]
    if req.aspect:
        cmd += ["--aspect", req.aspect]
    for r in req.refs:
        cmd += ["--ref", str(r)]
    code, msg = _run(cmd)
    if code == 0 and req.out_path.exists():
        return InvokeResult("ok")
    return InvokeResult("failed", error=msg or f"exit {code}")


def _invoke_codex(req: GenRequest) -> InvokeResult:
    d = resolve_skill_dir("codex-image-gen")
    sh = d / "scripts" / "gen-image.sh"
    cmd = ["bash", str(sh), "--prompt", req.prompt_final, "--out", str(req.out_path)]
    if req.aspect:
        cmd += ["--size", req.aspect]
    for r in req.refs:
        cmd += ["--ref", str(r)]
    code, msg = _run(cmd)
    if code == 0 and req.out_path.exists():
        return InvokeResult("ok")
    return InvokeResult("failed", error=msg or f"exit {code}")


def _invoke_comfyui(req: GenRequest) -> InvokeResult:
    d = resolve_skill_dir("comfyui")
    py = d / "scripts" / "comfy.py"
    w, h = _aspect_to_wh(req.aspect)
    # 带 ref → i2i 锁角色；否则 t2i
    if req.refs:
        cmd = [
            sys.executable, str(py), "i2i", str(req.refs[0]), req.prompt_final,
        ]
    else:
        cmd = [
            sys.executable, str(py), "t2i", req.prompt_final, "--w", str(w), "--h", str(h),
        ]
    code, msg = _run(cmd)
    # comfyui 产物落 comfy_outputs；解析其 stdout 找产物再拷到 out_path
    if code == 0:
        produced = _last_png(d / "scripts" / "comfy_outputs")
        if produced:
            req.out_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(produced, req.out_path)
            return InvokeResult("ok")
        return InvokeResult("failed", error="comfyui 退出 0 但未找到产物 png")
    return InvokeResult("failed", error=msg or f"exit {code}")


def _last_png(d: Path) -> Optional[Path]:
    if not d.exists():
        return None
    pngs = sorted(d.glob("**/*.png"), key=lambda p: p.stat().st_mtime, reverse=True)
    return pngs[0] if pngs else None


# ── DashScope 通义万象 直连 API（异步提交 → 轮询 → 下载）─────────────────────
def _http_json(url: str, headers: dict, body: Optional[dict] = None) -> tuple[int, dict]:
    """发一个 JSON 请求（无 body 即 GET），返 (status, 解析后的 dict)。stdlib only。"""
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method="POST" if data else "GET")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            payload = json.loads(e.read().decode("utf-8"))
        except Exception:
            payload = {"message": str(e)}
        return e.code, payload
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return 0, {"message": f"网络错误: {e}"}


def _download(url: str, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        with urllib.request.urlopen(url, timeout=120) as resp:
            dest.write_bytes(resp.read())
        return dest.exists() and dest.stat().st_size > 0
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def _dashscope_attempt(req: GenRequest, prompt: str, *, key: str, base: str, model: str) -> InvokeResult:
    """通义万象 文生图单次尝试：POST 异步任务 → 轮询 task → 下载结果 url。

    审核失败时 error 带原始审核标志（含 DataInspectionFailed 等），供上层判审核类→中性化重试。
    """
    submit_url = f"{base}/api/v1/services/aigc/text2image/image-synthesis"
    submit_headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable",
    }
    body = {
        "model": model,
        "input": {"prompt": prompt},
        "parameters": {"size": _aspect_to_dashscope_size(req.aspect), "n": 1},
    }
    status, payload = _http_json(submit_url, submit_headers, body)
    task_id = (payload.get("output") or {}).get("task_id")
    if status != 200 or not task_id:
        # 提交即被拒（含同步审核拒绝）：把 code + message 都带出，供审核判定。
        msg = payload.get("message") or payload.get("code") or f"HTTP {status}"
        code = payload.get("code") or ""
        return InvokeResult("failed", error=f"提交失败: {code} {msg}".strip())

    # 轮询（异步任务一般 10~40s 出图）
    poll_url = f"{base}/api/v1/tasks/{task_id}"
    poll_headers = {"Authorization": f"Bearer {key}"}
    deadline = time.time() + 300  # 5min 上限
    while time.time() < deadline:
        time.sleep(3)
        st, pl = _http_json(poll_url, poll_headers)
        out = pl.get("output") or {}
        task_status = out.get("task_status")
        if task_status == "SUCCEEDED":
            results = out.get("results") or []
            img_url = results[0].get("url") if results else None
            if not img_url:
                return InvokeResult("failed", error="SUCCEEDED 但无结果 url")
            if _download(img_url, req.out_path):
                return InvokeResult("ok")
            return InvokeResult("failed", error="结果图下载失败")
        if task_status in ("FAILED", "CANCELED", "UNKNOWN"):
            # 异步任务失败：审核拒绝常落这里（code/message 带 DataInspectionFailed）。
            code = out.get("code") or pl.get("code") or ""
            detail = out.get("message") or pl.get("message") or ""
            return InvokeResult("failed", error=f"任务 {task_status}: {code} {detail}".strip())
        # PENDING / RUNNING → 继续轮询
    return InvokeResult("failed", error="轮询超时（>5min 未 SUCCEEDED）")


def _invoke_dashscope(req: GenRequest) -> InvokeResult:
    """通义万象 文生图（直连 API）+ 审核降级（被拒 → prompt 中性化重写 → 重试一次）。

    带 ref 时通义万象的 t2i-turbo 不吃参考图（i2i/编辑是另一组接口，列为可扩展），
    这里只走 t2i 主路；有 ref 也仅按 prompt 出（路由层已优先支持 ref 的后端）。

    审核降级（共用 moderation 逻辑，借 Pixelle / ai-video-gen）：
      首次被拒 → 判是否审核类错误 → 是则 prompt 中性化重写、重试一次；
      非审核类错误（网络/超时/服务端）直接返失败，不中性化（不掩盖真因）。
      正常出图链路完全不受影响（只有 failed 且审核类才触发）。
    """
    cfg = load_api_config("dashscope")
    if not cfg:
        return InvokeResult("unavailable", error="dashscope 配置缺失")
    key = (cfg.get("api_key") or "").strip()
    base = (cfg.get("base") or "https://dashscope.aliyuncs.com").rstrip("/")
    model = cfg.get("image_model") or "wanx2.1-t2i-turbo"
    if not key:
        return InvokeResult("unavailable", error="dashscope.api_key 为空")

    res = _dashscope_attempt(req, req.prompt_final, key=key, base=base, model=model)
    if res.status != "failed" or not is_content_inspection_error(res.error):
        # 成功，或非审核类失败 → 原样返（不中性化掩盖真因）。
        return res

    # 审核拒绝 → 中性化重写、重试一次。
    neutralized, changed = neutralize_prompt(req.prompt_final)
    if not changed:
        return res
    retry = _dashscope_attempt(req, neutralized, key=key, base=base, model=model)
    if retry.status == "ok":
        return retry
    # 重试仍失败：诚实带原始 + 重试两段错误，不静默吞。
    return InvokeResult(
        "failed",
        error=f"审核拒绝，中性化重试仍失败 | 原始: {res.error} | 重试: {retry.error}",
    )


def _invoke_slot(req: GenRequest, hint: str) -> InvokeResult:
    """槽位后端：不真跑，给清晰提示。绝不假装生成。"""
    return InvokeResult("slot", hint=hint)


# ── PROVIDERS 注册表（与 reference/providers.md 同步）────────────────────────
@dataclass
class Provider:
    id: str
    tier: str                  # ready / slot
    supports_ref: bool
    supports_negative: bool
    aspect_param: str          # aspect / size / wh / prompt
    cost: str
    auth: str
    probe: Callable[[], tuple[bool, Optional[str]]]
    invoke: Callable[[GenRequest], InvokeResult]


def _browser_invoke(req: GenRequest) -> InvokeResult:
    return _invoke_slot(
        req,
        "browser-gen 是半自动槽位：要 Claude 用 claude-in-chrome 工具按 "
        "browser-gen/SKILL.md 流程驱动 Gemini 网页出图，CLI 无法全自动。",
    )


def _api_direct_invoke(req: GenRequest) -> InvokeResult:
    return _invoke_slot(
        req,
        "直连 API（Seedream/GPT-Image）需用户配 MEDIAGEN_API_KEY；本 skill 绝不擅自调付费接口。",
    )


def _jimeng_invoke(req: GenRequest) -> InvokeResult:
    return _invoke_slot(
        req,
        "jimeng/Dreamina 付费且需 maestro vip 权限；用 `dreamina text2image` 由用户显式启用，本 skill 不自动调。",
    )


def _ark_invoke(req: GenRequest) -> InvokeResult:
    """ARK 字节 Seedream 槽位：key 配好则可接入，未配则给提示。

    接入说明（待用户补 ark.api_key 后实现真调）：
      POST {base}/images/generations（OpenAI 兼容），header `Authorization: Bearer <key>`，
      body {"model": image_model(doubao-seedream), "prompt": ..., "size": "1024x1024",
            "response_format": "url", "n": 1} → data[0].url 下载即得（同步返回，无需轮询）。
    与 dashscope 不同：ARK 是 OpenAI 兼容同步接口、size 用 `宽x高`（小写 x）。
    """
    ok, reason = _probe_ark()
    if not ok:
        return _invoke_slot(
            req,
            f"ARK 字节 Seedream 槽位：{reason}。填 media-api-keys.json 的 ark.api_key "
            "后即可接入（OpenAI 兼容 /images/generations 同步接口，见 _ark_invoke docstring）。",
        )
    # key 已配但真调实现待补（用户补 key 后落地）——诚实标 slot，绝不假装生成。
    return _invoke_slot(
        req,
        "ARK key 已配但 Seedream 真调路径待落地（OpenAI 兼容 /images/generations）；"
        "本 skill 暂判为 slot，不假装出图。补完调用后将其 tier 切 ready。",
    )


PROVIDERS: dict[str, Provider] = {
    "gemini-gen": Provider(
        "gemini-gen", "ready", True, False, "aspect", "free-quota",
        "gemini 会员 cookie + accounts.json", _probe_gemini, _invoke_gemini,
    ),
    "codex-image-gen": Provider(
        "codex-image-gen", "ready", True, False, "size", "subscription",
        "~/.codex/auth.json 已登录", _probe_codex, _invoke_codex,
    ),
    "comfyui": Provider(
        "comfyui", "ready", True, True, "wh", "local-free",
        "本地 ComfyUI 127.0.0.1:8188", _probe_comfyui, _invoke_comfyui,
    ),
    "dashscope": Provider(
        "dashscope", "ready", False, False, "size", "paid",
        "media-api-keys.json dashscope.api_key（通义万象·账号级）",
        _probe_dashscope, _invoke_dashscope,
    ),
    "browser-gen": Provider(
        "browser-gen", "slot", True, False, "prompt", "free-quota",
        "Chrome MCP + 已登录 Gemini", _probe_browser, _browser_invoke,
    ),
    "api-direct": Provider(
        "api-direct", "slot", True, False, "size", "paid",
        "需用户配 API key", _probe_api_direct, _api_direct_invoke,
    ),
    "jimeng": Provider(
        "jimeng", "slot", True, False, "size", "paid",
        "dreamina CLI 登录 + maestro vip", _probe_jimeng, _jimeng_invoke,
    ),
    "ark": Provider(
        "ark", "slot", True, False, "size", "paid",
        "media-api-keys.json ark.api_key（字节 Seedream·待用户填）",
        _probe_ark, _ark_invoke,
    ),
}

# 默认自动降级链（slot 后端不进自动链，除非 --prefer 点名）
# dashscope 排在免费/订阅档之后、兜底之前：可控质量、稳定的直连 API（有成本，故不抢首位）。
DEFAULT_CHAIN = ["gemini-gen", "codex-image-gen", "comfyui", "dashscope", "browser-gen"]


def providers_snapshot() -> list[dict]:
    """各后端 capability + 当前可用性快照（providers 子命令用）。"""
    out = []
    for pid, p in PROVIDERS.items():
        ok, reason = p.probe()
        out.append(
            {
                "id": pid,
                "tier": p.tier,
                "supports_ref": p.supports_ref,
                "supports_negative": p.supports_negative,
                "aspect_param": p.aspect_param,
                "cost": p.cost,
                "auth": p.auth,
                "available": ok,
                "availability_reason": reason,
            }
        )
    return out


def _selfcheck_moderation() -> int:
    """单测：审核降级判定 + 中性化（不触发真审核·不烧 API）。"""
    print("== media-gen moderation_fallback selfcheck (#14) ==")
    failures = 0
    # 1) 审核类错误判定
    cases = [
        ("任务 FAILED: DataInspectionFailed input blocked", True),
        ("提交失败: data_inspection_failed 敏感内容", True),
        ("green net check failed", True),
        ("内容审核未通过", True),
        ("轮询超时（>5min 未 SUCCEEDED）", False),
        ("提交失败: HTTP 500 internal server error", False),
        ("结果图下载失败", False),
        ("", False),
        (None, False),
    ]
    for msg, expected in cases:
        got = is_content_inspection_error(msg)
        ok = got == expected
        failures += 0 if ok else 1
        print(f"  detect {'OK ' if ok else 'FAIL'}: {str(msg)[:46]!r:48s} → {got} (want {expected})")
    # 2) 中性化保留主题、去触发词
    p = "数据流像血一样崩溃，暗色背景，几何线框"
    neutral, changed = neutralize_prompt(p)
    assert changed, "中性化应改写"
    assert "血" not in neutral and "崩溃" not in neutral, "触发词未去除"
    assert "几何线框" in neutral, "画面主题丢失"
    print(f"  neutralize OK: -> {neutral[:80]}...")
    # 3) 空 prompt 不崩
    n2, c2 = neutralize_prompt("")
    assert not c2 and n2 == "", "空 prompt 应原样返"
    print("  empty-prompt OK")
    print("FAIL" if failures else "PASS")
    return failures


if __name__ == "__main__":
    import sys
    if "--selfcheck" in sys.argv:
        sys.exit(1 if _selfcheck_moderation() else 0)
    print(json.dumps(providers_snapshot(), ensure_ascii=False, indent=2))
