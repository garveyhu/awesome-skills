#!/usr/bin/env python3
"""把插画风输出"像素化"成规整像素画 + 可选统一调色板(美术一致性的关键)。

Z-Image 出的是高分辨率插画、不是规整像素格。本步:① 降采样到固定像素网格(色块规整)
再最近邻放回(硬像素块);② 可选量化到 N 色,统一整套资产用色。全程保留 alpha。

用法: python pixelize.py <in.png> <out.png> [--px 96] [--colors 32]
  --px     像素网格:目标短边像素数(越小越"颗粒")
  --colors 量化色数(0=不量化)
"""
import argparse
from PIL import Image

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inp"); ap.add_argument("out")
    ap.add_argument("--px", type=int, default=96, help="像素网格(目标短边像素数)")
    ap.add_argument("--colors", type=int, default=0, help="量化色数,0=不量化")
    a = ap.parse_args()
    im = Image.open(a.inp).convert("RGBA"); W, H = im.size
    rgb = im.convert("RGB"); alpha = im.split()[3]
    if W <= H:
        tw, th = a.px, max(1, round(H * a.px / W))
    else:
        tw, th = max(1, round(W * a.px / H)), a.px
    small = rgb.resize((tw, th), Image.BILINEAR)            # 平滑降采样取色块
    smalla = alpha.resize((tw, th), Image.NEAREST)          # alpha 硬边
    if a.colors > 0:
        small = small.quantize(colors=a.colors, method=Image.MEDIANCUT,
                               dither=Image.Dither.NONE).convert("RGB")
    big = small.resize((W, H), Image.NEAREST)               # 最近邻放回 → 硬像素块
    biga = smalla.resize((W, H), Image.NEAREST)
    out = big.convert("RGBA"); out.putalpha(biga)
    out.save(a.out)
    print(f"✓ {a.out} | 网格 {tw}x{th}" + (f" | 量化 {a.colors} 色" if a.colors else ""))

if __name__ == "__main__":
    main()
