#!/bin/bash
# Gemini 会员号生图入口：多账号 cookie 隔离 + 负载均衡 + 撞额度跳号。
# 依赖经 uv 临时注入（首次稍慢、之后走缓存）。把所有参数透传给 gen_image.py。
#
# 用法：
#   bash gen-image.sh --prompt "描述" --out out.png \
#        [--account <账号别名,见 accounts.json>] \
#        [--model flash|pro] [--aspect 16:9] [--ref ref1.png --ref ref2.png]
#
# 不传 --account = 全部号轮询负载，撞 limit 自动跳下一个号。

set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

exec uv run --no-project \
  --with gemini_webapi \
  --with browser-cookie3 \
  python "$DIR/gen_image.py" "$@"
