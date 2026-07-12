#!/usr/bin/env python3
"""chroma 底去透明：按层出图协议的去底工具。

Codex 内置 image_gen 不支持透明背景（请求透明会存成不透明 RGB）——官方 imagegen skill
的标准解法是「生成到纯 chroma 底再 key 掉」。本脚本就是那一步：吃一张 chroma 底 PNG，
出一张收好边的透明 PNG，喂 video-master 的分层镜（layered-parallax / layered-reveal）。

用法：
    ~/.venvs/current/bin/python strip_chroma.py in.png out.png [--key auto|green|magenta|#RRGGBB]
                                                [--soft 60] [--hard 24] [--erode 1]

判据（插画硬边风格 · 平底 chroma）：
  - key 色 auto = 取四边 12px 边框像素的中位色（分层素材背景必为 chroma 平底，边框即 key）。
  - alpha 由「像素到 key 色的欧氏距离」软映射：dist<=hard 全透明、dist>=soft 全不透明、中间线性。
  - despill：半透明边缘把 key 通道压到 max(其余两通道)（去绿/品红溢色描边）。
  - erode：3×3 最小值滤一遍 alpha（收边 1px·吃掉 chroma 侵染的最外圈）。
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image

KEY_PRESETS = {"green": (0, 255, 0), "magenta": (255, 0, 255)}


def parse_key(spec: str, img: np.ndarray) -> tuple[int, int, int]:
    """解析 key 色：auto=边框中位色 / 预设名 / #RRGGBB。"""
    if spec in KEY_PRESETS:
        return KEY_PRESETS[spec]
    if spec.startswith("#") and len(spec) == 7:
        return tuple(int(spec[i : i + 2], 16) for i in (1, 3, 5))  # type: ignore[return-value]
    # auto：四边 12px 边框的中位色（分层素材的背景必为 chroma 平底）
    b = 12
    border = np.concatenate(
        [
            img[:b].reshape(-1, 3),
            img[-b:].reshape(-1, 3),
            img[:, :b].reshape(-1, 3),
            img[:, -b:].reshape(-1, 3),
        ]
    )
    return tuple(int(v) for v in np.median(border, axis=0))  # type: ignore[return-value]


def strip(in_path: Path, out_path: Path, key_spec: str, soft: float, hard: float, erode: int) -> dict:
    rgb = np.asarray(Image.open(in_path).convert("RGB"), dtype=np.float32)
    key = parse_key(key_spec, rgb)

    # alpha：到 key 色距离的软映射（hard 内全透明 → soft 外全不透明）
    dist = np.sqrt(((rgb - np.array(key, dtype=np.float32)) ** 2).sum(axis=-1))
    alpha = np.clip((dist - hard) / max(soft - hard, 1e-6), 0.0, 1.0)

    # despill：把 key 主通道压到其余两通道的最大值（去溢色）。
    # **无条件**作用于全图——抗锯齿的实心笔画（alpha 已到 1）同样吃了 key 溢染
    # （黑线在绿底上出成墨绿），只处理半透明区会漏掉它们；中性色内容压 key 通道无副作用。
    dominant = int(np.argmax(key))
    others = [c for c in range(3) if c != dominant]
    if key[dominant] >= 128:  # key 是亮色通道主导（green/magenta 都是）
        cap = np.maximum(rgb[..., others[0]], rgb[..., others[1]])
        rgb[..., dominant] = np.minimum(rgb[..., dominant], cap)
        # magenta 是双通道主导（R+B）：再压次主导通道
        sorted_key = sorted(range(3), key=lambda c: key[c], reverse=True)
        if key[sorted_key[1]] >= 128:
            second = sorted_key[1]
            rest = [c for c in range(3) if c != second]
            cap2 = np.maximum(rgb[..., rest[0]], rgb[..., rest[1]])
            rgb[..., second] = np.minimum(rgb[..., second], cap2)

    # erode：3×3 min 滤 alpha 收边（吃掉最外圈 chroma 侵染），迭代 erode 次
    for _ in range(max(0, erode)):
        p = np.pad(alpha, 1, mode="edge")
        alpha = np.minimum.reduce(
            [p[i : i + alpha.shape[0], j : j + alpha.shape[1]] for i in range(3) for j in range(3)]
        )

    rgba = np.dstack([rgb.clip(0, 255).astype(np.uint8), (alpha * 255).astype(np.uint8)])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(rgba, "RGBA").save(out_path)
    kept = float((alpha > 0.5).mean())
    return {"key": key, "kept_ratio": round(kept, 4)}


def main() -> int:
    ap = argparse.ArgumentParser(description="chroma 底去透明（按层出图协议）")
    ap.add_argument("input", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("--key", default="auto", help="auto | green | magenta | #RRGGBB（默认 auto=边框中位色）")
    ap.add_argument("--soft", type=float, default=60.0, help="全不透明距离阈（默认 60）")
    ap.add_argument("--hard", type=float, default=24.0, help="全透明距离阈（默认 24）")
    ap.add_argument("--erode", type=int, default=1, help="收边迭代次数（默认 1·0 关闭）")
    args = ap.parse_args()

    info = strip(args.input, args.output, args.key, args.soft, args.hard, args.erode)
    # kept_ratio 哨兵：<1% 或 >99% 说明 key 判错（整图被扣光 / 根本没扣掉），报警不静默
    if info["kept_ratio"] < 0.01 or info["kept_ratio"] > 0.99:
        print(f"[warn] kept_ratio={info['kept_ratio']}（key={info['key']}）——疑 key 判错，肉眼核 {args.output}", file=sys.stderr)
    print(f"{args.output}  key={info['key']} kept={info['kept_ratio']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
