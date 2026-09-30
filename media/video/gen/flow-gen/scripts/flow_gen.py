#!/usr/bin/env python3
"""flow-gen 命令行：用 Google Flow（Veo 3.1 / Omni Flash）按会员点数生成视频。

    flow_gen.py credits                       # 看剩余点数和档位
    flow_gen.py models                        # 列出当前档位能用的视频模型和点数
    flow_gen.py gen --prompt "..." --out a.mp4 [--model lite|fast|quality|omni]
                   [--aspect 16:9|9:16] [--duration 8] [--res 720p|360p] [--count 1] [--dry-run]

走用户真实 Chrome（可插拔浏览器通道，默认 kimi-webbridge），不弹新浏览器；reCAPTCHA 由 Flow 页面自己现场生成。
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from catalog import FAMILIES, available_models, pick_t2v  # noqa: E402
from flow_session import SESSION, FlowError, FlowSession  # noqa: E402
from bridges import BridgeError, available, get_bridge  # noqa: E402

STATUS_DONE = 3
STATUS_FAILED = {4, 5}


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def cmd_credits(session: FlowSession, _args: argparse.Namespace) -> dict:
    return session.call("credits")


def cmd_models(session: FlowSession, _args: argparse.Namespace) -> list:
    tier = session.call("credits")["tier"]
    raw = session.call("catalog")
    return [
        {"key": m.key, "cost": m.cost, "duration": m.duration, "resolution": m.resolution,
         "aspects": ["16:9" if a == 2 else "9:16" for a in m.aspects]}
        for m in available_models(raw, tier) if m.is_t2v
    ]


def _output_paths(out: str, media_ids: list[str]) -> list[Path]:
    target = Path(out).expanduser()
    if len(media_ids) == 1 and target.suffix:
        return [target]
    folder = target if not target.suffix else target.parent
    stem = target.stem if target.suffix else "flow"
    return [folder / f"{stem}-{i + 1}-{mid[:8]}.mp4" for i, mid in enumerate(media_ids)]


def _download(url: str, dest: Path) -> int:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=120) as resp, open(dest, "wb") as fh:
        data = resp.read()
        fh.write(data)
    return len(data)


def _wait(session: FlowSession, media_ids: list[str], timeout: float, interval: float) -> dict:
    deadline = time.time() + timeout
    results: dict[str, dict] = {}
    while time.time() < deadline:
        pending = [m for m in media_ids if m not in results]
        if not pending:
            break
        for item in session.call("poll", pending)["media"]:
            if item["status"] == STATUS_DONE or item["status"] in STATUS_FAILED:
                results[item["mediaId"]] = item
        done = len(results)
        log(f"… 进度 {done}/{len(media_ids)}")
        if done < len(media_ids):
            time.sleep(interval)
    return results


def cmd_gen(session: FlowSession, args: argparse.Namespace) -> dict:
    account = session.call("credits")
    model = pick_t2v(session.call("catalog"), account["tier"], args.model, args.aspect, args.duration, args.res)
    total = model.cost * args.count
    plan = {"model": model.key, "cost_each": model.cost, "count": args.count, "cost_total": total,
            "credits_before": account["credits"], "project": session.project_id}
    log(f"计划：{model.key} ×{args.count}，共 {total} 点（当前剩 {account['credits']}）")
    if args.dry_run:
        return {"dry_run": True, **plan}
    if account["credits"] < total:
        raise FlowError(f"点数不够：需要 {total}，只剩 {account['credits']}")

    submitted = session.submit_t2v(
        prompt=args.prompt, family_name=model.family_name, model_key=model.key, expected_cost=model.cost,
        aspect=args.aspect, duration=model.duration, resolution=args.res, count=args.count,
    )
    media_ids = submitted["mediaIds"]
    log(f"已提交 {len(media_ids)} 条，剩余点数 {submitted['creditsLeft']}，开始轮询")

    finished = _wait(session, media_ids, args.timeout, args.interval)
    outputs = []
    for media_id, dest in zip(media_ids, _output_paths(args.out, media_ids)):
        item = finished.get(media_id)
        if not item:
            outputs.append({"mediaId": media_id, "status": "timeout"})
            continue
        if item["status"] != STATUS_DONE:
            outputs.append({"mediaId": media_id, "status": "failed", "code": item["status"]})
            continue
        url = session.call("media", media_id)["videoUrl"]
        size = _download(url, dest)
        outputs.append({"mediaId": media_id, "status": "ok", "path": str(dest.resolve()), "bytes": size})
        log(f"✓ {dest}")
    return {**plan, "credits_after": submitted["creditsLeft"], "outputs": outputs}


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Google Flow 视频生成（走真实 Chrome 登录态）")
    p.add_argument("--project", help="Flow 项目 id；默认沿用上次 / 最近的项目")
    p.add_argument("--bridge", choices=available(), help="浏览器通道；默认读 FLOW_GEN_BRIDGE，再默认 kimi")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("credits", help="剩余点数与档位")
    sub.add_parser("models", help="当前档位可用的文生视频模型")
    g = sub.add_parser("gen", help="文生视频")
    g.add_argument("--prompt", required=True)
    g.add_argument("--out", default="./flow.mp4", help="输出 mp4 路径（多条时作为前缀/目录）")
    g.add_argument("--model", choices=sorted(FAMILIES), default="lite")
    g.add_argument("--aspect", choices=["16:9", "9:16"], default="16:9")
    g.add_argument("--duration", type=int, default=8)
    g.add_argument("--res", choices=["720p", "360p"], default="720p")
    g.add_argument("--count", type=int, choices=[1, 2, 3, 4], default=1)
    g.add_argument("--timeout", type=float, default=900)
    g.add_argument("--interval", type=float, default=8)
    g.add_argument("--dry-run", action="store_true", help="只解析模型和点数，不提交")
    return p


def main() -> int:
    args = build_parser().parse_args()
    handlers = {"credits": cmd_credits, "models": cmd_models, "gen": cmd_gen}
    try:
        session = FlowSession(args.project, get_bridge(SESSION, args.bridge)).open()
        result = handlers[args.cmd](session, args)
    except (FlowError, BridgeError, LookupError) as e:
        log(f"✗ {e}")
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if isinstance(result, dict) and any(o.get("status") != "ok" for o in result.get("outputs", [])):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
