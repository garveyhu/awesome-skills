#!/usr/bin/env python3
"""write_sidecar —— 给任意媒体产物写 `_meta/<名>.json` sidecar 留痕（出图必留痕约定的执行小工具）。

素材体系（260712）约定：素材落分类目录（内容级 `素材/{真材料,生图,精灵}/`、频道级
`风格卡/素材库/{插画,装置}/`），每分类自带 `_meta/`——本工具把一次生成的元数据
（prompt / backend / aspect / created / refs…）写到 `<产物同级>/_meta/<stem>.json`，
让新对话 / 新频道零人工记忆、asset-index 扫描即得、qc 可 ls 对账。

用法（后端无关·任何出图/出视频调用方产物落盘后调一下）：
  write_sidecar.py --out 素材/生图/shot-3.png \
      --prompt "a foggy grey cat" --backend codex-image-gen \
      [--aspect 16:9] [--ref shot-3] [--ref 260712-slug] \
      [--kind image|video|html|audio] [--source generated] \
      [--license original] [--washed true|false]

行为：
  · sidecar 落 `<out 父目录>/_meta/<stem>.json`，目录自动建；
  · 已存在 → 合并更新：新字段覆盖旧值、`refs` 去重追加、`created` 保留首次；
  · 纯标准库、幂等；stdout 只打 sidecar 绝对路径（管线可接）。

字段口径与素材步、asset-index skill 的 `_meta/<名>.json` 扫描约定同构。
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

KIND_BY_EXT = {
    ".png": "image", ".jpg": "image", ".jpeg": "image", ".webp": "image",
    ".bmp": "image", ".gif": "image",
    ".mp4": "video", ".mov": "video", ".webm": "video", ".mkv": "video", ".m4v": "video",
    ".html": "html", ".htm": "html",
    ".wav": "audio", ".mp3": "audio", ".m4a": "audio", ".aac": "audio",
    ".flac": "audio", ".ogg": "audio",
}


def _parse_bool(v: str) -> bool:
    if v.lower() in ("true", "1", "yes", "y"):
        return True
    if v.lower() in ("false", "0", "no", "n"):
        return False
    raise argparse.ArgumentTypeError(f"须是 true/false：{v!r}")


def write_sidecar(out: Path, fields: dict, refs: list[str]) -> Path:
    """写/更新 sidecar，返回 sidecar 路径。合并语义：refs 去重追加、created 保留首次。"""
    side = out.parent / "_meta" / f"{out.stem}.json"
    side.parent.mkdir(parents=True, exist_ok=True)
    prev: dict = {}
    if side.is_file():
        try:
            loaded = json.loads(side.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                prev = loaded
        except (json.JSONDecodeError, OSError):
            prev = {}  # 坏 sidecar → 重写（留痕以最新为准）
    record = {**prev, **{k: v for k, v in fields.items() if v is not None}}
    old_refs = prev.get("refs")
    merged = [r for r in old_refs if isinstance(r, str)] if isinstance(old_refs, list) else []
    for r in refs:
        if r not in merged:
            merged.append(r)
    if merged:
        record["refs"] = merged
    record.setdefault("created", dt.datetime.now().isoformat(timespec="seconds"))
    side.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return side


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="给媒体产物写 _meta/<名>.json sidecar 留痕")
    p.add_argument("--out", required=True, help="产物路径（sidecar 落其同级 _meta/）")
    p.add_argument("--prompt", help="生成 prompt（asset-index 检索描述符）")
    p.add_argument("--backend", help="出图后端（codex-image-gen / gemini-gen / …）")
    p.add_argument("--kind", choices=["image", "video", "html", "audio"],
                   help="产物类型；缺省按扩展名自判")
    p.add_argument("--aspect", help="画幅（16:9 / 9:16 / 1:1…）")
    p.add_argument("--source", default="generated",
                   help="来源（generated / real-material / stock…·默认 generated）")
    p.add_argument("--license", help="许可/出处（cc0 / by / screenshot / original…）")
    p.add_argument("--washed", type=_parse_bool,
                   help="AI 生成图是否已过品牌洗味重处理（true/false）")
    p.add_argument("--ref", action="append", default=[], dest="refs",
                   help="被哪镜/哪条内容用（可重复·如 shot-3）")
    args = p.parse_args(argv)

    out = Path(args.out).expanduser().resolve()
    if not out.is_file():
        print(f"[write_sidecar] 产物不存在：{out}（先出图再留痕·不给不存在的东西记账）",
              file=sys.stderr)
        return 1
    kind = args.kind or KIND_BY_EXT.get(out.suffix.lower())
    if kind is None:
        print(f"[write_sidecar] 认不出类型（扩展名 {out.suffix!r}）——用 --kind 显式给",
              file=sys.stderr)
        return 2
    side = write_sidecar(out, {
        "kind": kind, "prompt": args.prompt, "backend": args.backend,
        "aspect": args.aspect, "source": args.source,
        "license": args.license, "washed": args.washed,
    }, args.refs)
    print(side)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
