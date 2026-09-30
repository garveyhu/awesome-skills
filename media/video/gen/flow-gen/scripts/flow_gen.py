#!/usr/bin/env python3
"""flow-gen 命令行：用 Google Flow 按会员点数生成视频（Veo 3.1 / Omni Flash）和图片（Nano Banana）。

    flow_gen.py credits                                   # 剩余点数和档位
    flow_gen.py models                                    # 当前档位能用的视频 / 图片模型和点数
    flow_gen.py gen   --prompt "..." --out a.mp4 [视频参数]  # 生成视频
    flow_gen.py image --prompt "..." --out a.jpg [图片参数]  # 生成图片（PRO 档 0 点）

视频有三种输入：不给图 = 文生；--start-image [--end-image] = 「帧」（首帧 / 首尾帧）；
--ref 图（可多次）= 「素材」（参考图生视频）。「帧」和「素材」不能同时用。
走用户真实 Chrome（可插拔浏览器通道，默认 kimi-webbridge），不弹新浏览器；reCAPTCHA 由 Flow 页面自己生成。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from bridges import BridgeError, available, get_bridge  # noqa: E402
from catalog import (  # noqa: E402
    IMAGE_ASPECTS, IMAGE_FAMILIES, MODES, VIDEO_FAMILIES,
    available_image_models, available_models, pick_image_model, pick_model,
)
from flow_session import SESSION, FlowError, FlowSession  # noqa: E402
from outputs import download, output_paths  # noqa: E402

STATUS_DONE = 3
STATUS_FAILED = {4, 5}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".heif", ".heic"}


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def check_images(paths: list[str]) -> None:
    for path in paths:
        f = Path(path).expanduser()
        if not f.is_file():
            raise FlowError(f"图片不存在：{path}")
        if f.suffix.lower() not in IMAGE_SUFFIXES:
            raise FlowError(f"Flow 只收 {'/'.join(sorted(IMAGE_SUFFIXES))}：{path}")


def ensure_credits(account: dict, total: int) -> None:
    if account["credits"] < total:
        raise FlowError(f"点数不够：需要 {total}，只剩 {account['credits']}")


# ---------- 子命令 ----------
def cmd_credits(session: FlowSession, _args: argparse.Namespace) -> dict:
    return session.call("credits")


def cmd_models(session: FlowSession, _args: argparse.Namespace) -> dict:
    tier = session.call("credits")["tier"]
    raw = session.call("catalog")
    return {
        "video": [
            {"key": m.key, "modes": [mode for mode in MODES if m.supports(mode)], "cost": m.cost,
             "duration": m.duration, "resolution": m.resolution, "max_refs": m.max_refs,
             "aspects": ["16:9" if a == 2 else "9:16" for a in m.aspects]}
            for m in available_models(raw, tier)
        ],
        "image": [{"key": m.key, "name": m.family_name, "cost": m.cost}
                  for m in available_image_models(raw, tier)],
    }


def resolve_video_mode(args: argparse.Namespace) -> tuple[str, list[str | None], list[str]]:
    """根据给了哪些图推断视频模式，并提前校验图片文件。"""
    if args.end_image and not args.start_image:
        raise FlowError("只给尾帧不行：尾帧必须配合 --start-image")
    if args.ref and args.start_image:
        raise FlowError("「帧」（--start-image/--end-image）和「素材」（--ref）不能同时用")
    frames = [args.start_image, args.end_image]
    check_images([p for p in frames if p] + args.ref)
    if args.ref:
        return "r2v", [None, None], args.ref
    mode = "first_last" if args.end_image else "i2v" if args.start_image else "t2v"
    return mode, frames, []


def _wait_videos(session: FlowSession, media_ids: list[str], timeout: float, interval: float) -> dict:
    deadline = time.time() + timeout
    results: dict[str, dict] = {}
    while time.time() < deadline:
        pending = [m for m in media_ids if m not in results]
        if not pending:
            break
        for item in session.call("poll", pending)["media"]:
            if item["status"] == STATUS_DONE or item["status"] in STATUS_FAILED:
                results[item["mediaId"]] = item
        log(f"… 进度 {len(results)}/{len(media_ids)}")
        if len(results) < len(media_ids):
            time.sleep(interval)
    return results


def cmd_gen(session: FlowSession, args: argparse.Namespace) -> dict:
    mode, frames, refs = resolve_video_mode(args)
    account = session.call("credits")
    model = pick_model(session.call("catalog"), account["tier"], args.model, mode,
                       args.aspect, args.duration, args.res)
    if refs and model.max_refs and len(refs) > model.max_refs:
        raise FlowError(f"{model.family_name} 素材模式最多 {model.max_refs} 张参考图，给了 {len(refs)} 张")
    total = model.cost * args.count
    plan = {"mode": mode, "model": model.key, "cost_each": model.cost, "count": args.count,
            "cost_total": total, "credits_before": account["credits"], "project": session.project_id}
    log(f"计划：{mode} · {model.key} ×{args.count}，共 {total} 点（当前剩 {account['credits']}）")
    if args.dry_run:
        return {"dry_run": True, **plan}
    ensure_credits(account, total)

    submitted = session.submit_video(
        prompt=args.prompt, family_name=model.family_name, model_key=model.key, expected_cost=model.cost,
        aspect=args.aspect, duration=model.duration, resolution=args.res, count=args.count,
        frames=frames, refs=refs, agree_rights=args.agree_rights,
    )
    media_ids = submitted["mediaIds"]
    log(f"已提交 {len(media_ids)} 条，剩余点数 {submitted['creditsLeft']}，开始轮询")

    finished = _wait_videos(session, media_ids, args.timeout, args.interval)
    outputs = []
    for media_id, dest in zip(media_ids, output_paths(args.out, media_ids, ".mp4")):
        item = finished.get(media_id)
        if not item:
            outputs.append({"mediaId": media_id, "status": "timeout"})
        elif item["status"] != STATUS_DONE:
            outputs.append({"mediaId": media_id, "status": "failed", "code": item["status"]})
        else:
            dest, size = download(session.call("media", media_id)["videoUrl"], dest)
            outputs.append({"mediaId": media_id, "status": "ok", "path": str(dest.resolve()), "bytes": size})
            log(f"✓ {dest}")
    return {**plan, "credits_after": submitted["creditsLeft"], "outputs": outputs}


def cmd_image(session: FlowSession, args: argparse.Namespace) -> dict:
    check_images(args.ref)
    account = session.call("credits")
    model = pick_image_model(session.call("catalog"), account["tier"], args.model)
    total = model.cost * args.count
    plan = {"model": model.key, "name": model.family_name, "count": args.count, "cost_total": total,
            "credits_before": account["credits"], "refs": len(args.ref), "project": session.project_id}
    log(f"计划：出图 · {model.family_name} ×{args.count}，共 {total} 点")
    if args.dry_run:
        return {"dry_run": True, **plan}
    ensure_credits(account, total)

    submitted = session.submit_image(
        prompt=args.prompt, family_name=model.family_name, model_key=model.key, expected_cost=model.cost,
        aspect=args.aspect, count=args.count, refs=args.ref, agree_rights=args.agree_rights,
    )
    images = submitted["images"]
    outputs = []
    for img, dest in zip(images, output_paths(args.out, [i["mediaId"] for i in images], ".jpg")):
        dest, size = download(img["url"], dest)
        outputs.append({"mediaId": img["mediaId"], "status": "ok", "path": str(dest.resolve()), "bytes": size})
        log(f"✓ {dest}")
    if len(images) < args.count:
        log(f"⚠ 只出了 {len(images)}/{args.count} 张（其余可能被内容安全拦截）")
    return {**plan, "outputs": outputs}


# ---------- 参数 ----------
def _add_ref_args(p: argparse.ArgumentParser, ref_help: str) -> None:
    p.add_argument("--ref", action="append", default=[], metavar="IMG", help=ref_help)
    p.add_argument("--agree-rights", action="store_true",
                   default=os.environ.get("FLOW_GEN_AGREE_RIGHTS") == "1",
                   help="Flow 弹「图片使用权」确认时自动点同意（= 你声明对图片拥有权利）")
    p.add_argument("--dry-run", action="store_true", help="只解析模型和点数，不提交")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Google Flow 视频 / 图片生成（走真实 Chrome 登录态）")
    p.add_argument("--project", help="Flow 项目 id；默认沿用上次 / 最近的项目")
    p.add_argument("--bridge", choices=available(), help="浏览器通道；默认读 FLOW_GEN_BRIDGE，再默认 kimi")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("credits", help="剩余点数与档位")
    sub.add_parser("models", help="当前档位可用的视频 / 图片模型")

    g = sub.add_parser("gen", help="生成视频：文生 / 帧（首帧、首尾帧）/ 素材（参考图）")
    g.add_argument("--prompt", required=True)
    g.add_argument("--out", default="./flow.mp4", help="输出 mp4 路径（多条时作为前缀/目录）")
    g.add_argument("--model", choices=sorted(VIDEO_FAMILIES), default="lite")
    g.add_argument("--aspect", choices=["16:9", "9:16"], default="16:9")
    g.add_argument("--duration", type=int, default=8)
    g.add_argument("--res", choices=["720p", "360p"], default="720p")
    g.add_argument("--count", type=int, choices=[1, 2, 3, 4], default=1)
    g.add_argument("--start-image", help="首帧图片 →「帧」模式图生视频")
    g.add_argument("--end-image", help="尾帧图片（需同时给 --start-image）→ 首尾帧过渡")
    g.add_argument("--timeout", type=float, default=900)
    g.add_argument("--interval", type=float, default=8)
    _add_ref_args(g, "参考图（可多次）→「素材」模式：角色 / 物体 / 风格参考")

    i = sub.add_parser("image", help="生成图片（Nano Banana，PRO 档 0 点）")
    i.add_argument("--prompt", required=True)
    i.add_argument("--out", default="./flow.jpg", help="输出图片路径（多张时作为前缀/目录）")
    i.add_argument("--model", choices=sorted(IMAGE_FAMILIES), default="nb2",
                   help="pro=Nano Banana Pro  nb2=Nano Banana 2  lite=Nano Banana 2 Lite")
    i.add_argument("--aspect", choices=IMAGE_ASPECTS, default="16:9")
    i.add_argument("--count", type=int, choices=[1, 2, 3, 4], default=1)
    _add_ref_args(i, "参考图（可多次）→ 图生图 / 风格参考")
    return p


def main() -> int:
    args = build_parser().parse_args()
    handlers = {"credits": cmd_credits, "models": cmd_models, "gen": cmd_gen, "image": cmd_image}
    session = None
    try:
        session = FlowSession(args.project, get_bridge(SESSION, args.bridge)).open()
        result = handlers[args.cmd](session, args)
    except (FlowError, BridgeError, LookupError) as e:
        log(f"✗ {e}")
        return 1
    finally:
        if session:
            session.close()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if isinstance(result, dict) and any(o.get("status") != "ok" for o in result.get("outputs", [])):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
