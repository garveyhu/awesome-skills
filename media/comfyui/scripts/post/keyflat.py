#!/usr/bin/env python3
"""把"纯色背景的扁平图"抠成透明 PNG —— 扁平 2D 游戏美术的正确抠图法。

为什么不用神经抠图:BiRefNet/RMBG/BEN 等是给真实照片做显著性分割的,对扁平像素/插画
完全在分布外(实测把主体整个抹掉或抠不掉底)。扁平美术该用 color-key。

两种模式:
- 默认(洪水填充):从四边按背景色容差填充,**只清边缘连通**区域 → 保留被主体轮廓围住
  的内部(内部即使有相近色也不误删)。适合背景色与主体可能撞色的情况。
- `--global`(全局色键):清掉**整张**里所有接近背景色的像素 → **进得了封闭区**
  (如拉弓的弓环白块)。**前提是背景用独特色(纯洋红 #ff00ff)**,主体不含该色才安全。

用法: python keyflat.py <in.png> <out.png> [--tol 90] [--bg ff00ff] [--global]
  --bg 不给则取四角众数色为背景色。
"""
import argparse
from PIL import Image


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inp"); ap.add_argument("out")
    ap.add_argument("--tol", type=int, default=90, help="背景色欧氏容差(0-441)")
    ap.add_argument("--bg", help="背景色 hex,如 ff00ff;默认取四角众数")
    ap.add_argument("--global", dest="globalkey", action="store_true",
                    help="全局色键:清掉所有接近背景色的像素(进得了封闭区);用于纯洋红等独特底色")
    a = ap.parse_args()
    im = Image.open(a.inp).convert("RGBA"); W, H = im.size; px = im.load()
    if a.bg:
        bg = tuple(int(a.bg[i:i+2], 16) for i in (0, 2, 4))
    else:
        corners = [px[0, 0], px[W-1, 0], px[0, H-1], px[W-1, H-1]]
        keys = [(c[0], c[1], c[2]) for c in corners]
        bg = max(set(keys), key=keys.count)
    tol2 = a.tol * a.tol

    def close(p):
        return (p[0]-bg[0])**2 + (p[1]-bg[1])**2 + (p[2]-bg[2])**2 <= tol2

    cleared = 0
    if a.globalkey:                              # 全局:整张清,进得了封闭区
        for y in range(H):
            for x in range(W):
                p = px[x, y]
                if p[3] == 0 or close(p):
                    px[x, y] = (0, 0, 0, 0); cleared += 1
    else:                                        # 洪水填充:只清边缘连通
        seen = bytearray(W * H); stack = []
        for x in range(W): stack += [(x, 0), (x, H-1)]
        for y in range(H): stack += [(0, y), (W-1, y)]
        while stack:
            x, y = stack.pop()
            if x < 0 or y < 0 or x >= W or y >= H: continue
            i = y * W + x
            if seen[i]: continue
            seen[i] = 1
            p = px[x, y]
            if p[3] == 0 or close(p):
                px[x, y] = (0, 0, 0, 0); cleared += 1
                stack += [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    im.save(a.out)
    mode = "全局" if a.globalkey else "洪水填充"
    print(f"✓ {a.out} | 背景色 {bg} 容差 {a.tol} | {mode} | 清除 {cleared*100//(W*H)}%")


if __name__ == "__main__":
    main()
