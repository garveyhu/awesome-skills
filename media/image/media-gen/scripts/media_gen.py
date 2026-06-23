#!/usr/bin/env python3
"""media-gen —— 统一生图入口（路由 + 降级 + 统一结果）。

单一职责：CLI 解析 → style-lock 注入 → 按配置/可用性构建降级链 → 串行路由到后端
→ 出统一结果 JSON（stdout 一行）。后端能力 / 探测 / 调用在 providers.py，本文件只编排。

用法见 SKILL.md：
    media_gen.py gen --prompt "..." --out out.png [--aspect 16:9] [--ref a.png]
                     [--prefer comfyui] [--no-fallback] [--no-style-lock] [--dry-run]
    media_gen.py providers      # 各后端能力 + 可用性
    media_gen.py contract       # 打印统一结果契约 schema 说明
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

import providers as P


# ── 日志：决策走 stderr，结果走 stdout ──────────────────────────────────────
def log(msg: str) -> None:
    print(f"[media-gen] {msg}", file=sys.stderr)


def emit(result: dict) -> None:
    """统一结果：stdout 只吐一行 JSON。"""
    print(json.dumps(result, ensure_ascii=False))


# ── style-lock 注入 ─────────────────────────────────────────────────────────
def find_style_lock(out_path: Path, explicit: Optional[str]) -> Optional[Path]:
    if explicit:
        p = Path(explicit).expanduser()
        return p if p.exists() else None
    # 从 out 目录逐级上溯找 Media-Studio 的画风锁（style-lock token 真身文件 画风锁.md）
    cur = out_path.resolve().parent
    for _ in range(12):
        cand = cur / "1-资产库" / "风格锁" / "画风锁.md"
        if cand.exists():
            return cand
        if cur.parent == cur:
            break
        cur = cur.parent
    return None


def parse_style_lock(path: Path) -> dict:
    """读 画风锁.md（style-lock token）frontmatter 取 locked_prompt / negative_prompt / version。"""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    fm = text[3:end] if end > 0 else ""
    out: dict[str, str] = {}
    for key in ("locked_prompt", "negative_prompt", "version", "seed", "sref"):
        for line in fm.splitlines():
            s = line.strip()
            if s.startswith(f"{key}:"):
                val = s[len(key) + 1 :].strip()
                if val.startswith('"') and val.endswith('"') and len(val) > 1:
                    val = val[1:-1]
                out[key] = val
                break
    return out


def inject_style_lock(user_prompt: str, sl: dict) -> tuple[str, str]:
    """拼 locked_prompt 到前、negative 以 'avoid:' 追加；返 (prompt_final, negative)."""
    locked = sl.get("locked_prompt", "").strip()
    negative = sl.get("negative_prompt", "").strip()
    parts = []
    if locked:
        parts.append(locked)
    parts.append(user_prompt.strip())
    prompt_final = ", ".join(parts)
    if negative:
        prompt_final = f"{prompt_final}. avoid: {negative}"
    return prompt_final, negative


# ── 降级链构建（prefer + ref-aware 重排）─────────────────────────────────────
def build_chain(prefer: Optional[str], has_ref: bool, no_fallback: bool) -> list[str]:
    chain = list(P.DEFAULT_CHAIN)
    if prefer:
        if prefer not in P.PROVIDERS:
            log(f"未知 --prefer 后端 '{prefer}'，忽略（可选：{list(P.PROVIDERS)}）")
        else:
            # prefer 提到链首；若它是 slot 后端（默认不在链里）也加进来
            chain = [prefer] + [c for c in chain if c != prefer]
    if has_ref:
        # 把不支持 ref 的后端降权到末尾
        chain.sort(key=lambda c: 0 if P.PROVIDERS[c].supports_ref else 1)
    if no_fallback:
        chain = chain[:1]
    return chain


# ── gen 主流程 ──────────────────────────────────────────────────────────────
def cmd_gen(args: argparse.Namespace) -> int:
    out_path = Path(args.out).expanduser()
    refs = [Path(r).expanduser() for r in (args.ref or [])]
    for r in refs:
        if not r.exists():
            log(f"⚠️ 参考图不存在：{r}")

    # 1) style-lock 注入
    sl_version = None
    negative = ""
    prompt_user = args.prompt
    prompt_final = args.prompt
    if not args.no_style_lock:
        sl_path = find_style_lock(out_path, args.style_lock)
        if sl_path:
            sl = parse_style_lock(sl_path)
            prompt_final, negative = inject_style_lock(prompt_user, sl)
            sl_version = sl.get("version") or "v1"
            log(f"style-lock 注入：{sl_path}（{sl_version}）")
        else:
            log("未找到 画风锁.md，跳过注入（非品牌图可忽略）")
    else:
        log("--no-style-lock：跳过 style-lock 注入")

    # 2) 构建降级链
    chain = build_chain(args.prefer, bool(refs), args.no_fallback)
    log(f"降级链：{' → '.join(chain)}")

    meta_base = {
        "prompt_user": prompt_user,
        "prompt_final": prompt_final,
        "negative_prompt": negative or None,
        "aspect": args.aspect,
        "refs": [str(r) for r in refs],
        "style_lock": sl_version,
        "fallback_chain": chain,
    }

    # 3) dry-run：只出决策预演
    if args.dry_run:
        routing = []
        first_avail = True
        for cid in chain:
            prov = P.PROVIDERS[cid]
            ok, reason = prov.probe()
            if prov.tier == "slot":
                decision = "slot (half-auto / 需配置, hint)"
                avail: object = "slot"
            elif ok:
                decision = "would-try (1st)" if first_avail else "fallback"
                first_avail = False
                avail = True
            else:
                decision = f"skip ({reason})"
                avail = False
            routing.append(
                {"backend": cid, "available": avail, "decision": decision}
            )
        emit(
            {
                "ok": True,
                "dry_run": True,
                "type": "image",
                "path": None,
                "meta": {**meta_base, "routing": routing},
            }
        )
        return 0

    # 4) 真路由：串行降级
    out_path.parent.mkdir(parents=True, exist_ok=True)
    req = P.GenRequest(
        prompt_final=prompt_final,
        negative_prompt=negative,
        out_path=out_path,
        aspect=args.aspect,
        refs=refs,
    )
    attempts: list[dict] = []
    for cid in chain:
        prov = P.PROVIDERS[cid]
        # slot 后端：除非被 --prefer 点名仍只给提示
        if prov.tier == "slot":
            res = prov.invoke(req)
            attempts.append({"backend": cid, "status": "slot", "hint": res.hint})
            log(f"slot 后端 {cid}：{res.hint}")
            continue
        ok, reason = prov.probe()
        if not ok:
            attempts.append({"backend": cid, "status": "unavailable", "error": reason})
            log(f"{cid} 不可用：{reason} → 跳过")
            continue
        log(f"→ 尝试后端 {cid} …")
        res = prov.invoke(req)
        if res.status == "ok":
            attempts.append({"backend": cid, "status": "ok"})
            log(f"✅ {cid} 出图成功：{out_path}")
            emit(
                {
                    "ok": True,
                    "type": "image",
                    "path": str(out_path.resolve()),
                    "backend": cid,
                    "meta": {**meta_base, "cost": prov.cost, "attempts": attempts},
                }
            )
            return 0
        attempts.append({"backend": cid, "status": "failed", "error": res.error})
        log(f"❌ {cid} 失败：{res.error} → 降级")

    # 5) 链路耗尽
    emit(
        {
            "ok": False,
            "type": "image",
            "path": None,
            "backend": None,
            "meta": {
                **meta_base,
                "attempts": attempts,
                "error": "所有后端均未出图（unavailable/failed/slot）",
            },
        }
    )
    return 1


def cmd_providers(_: argparse.Namespace) -> int:
    emit({"providers": P.providers_snapshot(), "default_chain": P.DEFAULT_CHAIN})
    return 0


def cmd_contract(_: argparse.Namespace) -> int:
    schema = {
        "ok": "bool — 是否出图成功",
        "type": "image",
        "path": "成品绝对路径；失败为 null",
        "backend": "成功出图的后端 id；失败为 null",
        "meta": {
            "prompt_user": "用户原始 prompt",
            "prompt_final": "拼 style-lock 后真正喂后端的 prompt",
            "negative_prompt": "style-lock 负向词",
            "aspect": "宽高比",
            "refs": "参考图列表",
            "style_lock": "注入的 style-lock 版本或 null",
            "cost": "成功后端成本档",
            "fallback_chain": "实际降级链",
            "attempts": "[{backend,status: ok|failed|unavailable|slot, error?/hint?}]",
        },
    }
    emit(schema)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(prog="media-gen", description="统一生图入口（路由+降级）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("gen", help="生成一张图（路由+降级）")
    g.add_argument("--prompt", required=True)
    g.add_argument("--out", required=True)
    g.add_argument("--aspect")
    g.add_argument("--ref", action="append")
    g.add_argument("--prefer")
    g.add_argument("--no-fallback", action="store_true")
    g.add_argument("--no-style-lock", action="store_true")
    g.add_argument("--style-lock")
    g.add_argument("--dry-run", action="store_true")
    g.set_defaults(func=cmd_gen)

    p = sub.add_parser("providers", help="列各后端能力 + 可用性")
    p.set_defaults(func=cmd_providers)

    c = sub.add_parser("contract", help="打印统一结果契约 schema")
    c.set_defaults(func=cmd_contract)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
