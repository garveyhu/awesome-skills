#!/usr/bin/env python3
"""ComfyUI 自动化 CLI 入口(瘦壳)。

参数与命令逻辑在 cli/app.py;其余按职责分类:
  core/  通信(comfy_api) + 库存发现(inventory)
  build/ 工作流构建/转换(workflows, ui2api, api2ui)
  post/  图像后处理(keyflat, pixelize)
新增脚本放进对应类别目录即可(各目录已在 sys.path 上,直接 import 模块名)。
"""
import os
import sys

_S = os.path.dirname(os.path.abspath(__file__))
for _d in ("core", "build", "post", "cli"):
    _p = os.path.join(_S, _d)
    if _p not in sys.path:
        sys.path.insert(0, _p)

from app import main  # cli/app.py

if __name__ == "__main__":
    main()
