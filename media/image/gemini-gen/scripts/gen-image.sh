#!/bin/bash
# Gemini 生图入口：默认走本机反代（proxy 后端），可选 --backend cookie 切回旧的
# Gemini 网页会员号 cookie 方式。依赖经 uv 临时注入；cookie 后端才需要 gemini_webapi /
# browser-cookie3，proxy 后端只用标准库，默认路径不装那两个重依赖。
#
# 用法：
#   bash gen-image.sh --prompt "描述" --out out.png \
#        [--backend proxy|cookie]（默认 proxy） \
#        [--ref ref1.png --ref ref2.png] [--aspect 16:9] \
#        # proxy 后端专用：
#        [--proxy-model gemini-3.1-flash-image] [--size 1K|2K|4K] \
#        # cookie 后端专用：
#        [--account <账号别名,见 accounts.json>] [--model flash|pro]
#
# proxy 后端：配置见 proxy_config.example.json（复制为 proxy_config.json 填自己的反代地址/key）。
# cookie 后端：不传 --account = 全部号轮询负载，撞 limit 自动跳下一个号。

set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

needs_cookie_deps=0
prev=""
for arg in "$@"; do
  if [[ "$prev" == "--backend" && "$arg" == "cookie" ]] || [[ "$arg" == "--backend=cookie" ]]; then
    needs_cookie_deps=1
  fi
  prev="$arg"
done

if [[ "$needs_cookie_deps" == "1" ]]; then
  exec uv run --no-project \
    --with gemini_webapi \
    --with browser-cookie3 \
    python "$DIR/gen_image.py" "$@"
else
  exec uv run --no-project \
    python "$DIR/gen_image.py" "$@"
fi
