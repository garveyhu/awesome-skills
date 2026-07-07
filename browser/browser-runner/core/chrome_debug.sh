#!/bin/bash
# 以「远程调试端口」启动一个有头 Chrome，供 browser-runner 的 Playwright attach。
# 专用 profile（登录持久·不碰你日常 Chrome）；首次在窗口里登录目标站一次即可。
#
# 用法：  chrome_debug.sh [端口，默认 9333] [--url=<落地页>]
#   端口 / profile / chrome 路径 默认取自 ~/.browser-runner/config.toml，也可命令行覆盖。
#
# 兼容 macOS 自带 bash 3.2（不用数组 / set -u；变量一律 ${VAR} 明确边界，避 UTF-8 坑）。
set -o pipefail

PORT="${BROWSER_RUNNER_DEBUG_PORT:-9876}"
PROFILE_DIR="${BROWSER_RUNNER_PROFILE_DIR:-${HOME}/.browser-runner/profiles/default}"
CHROME="${BROWSER_RUNNER_CHROME_PATH:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
LANDING_URL=""
for a in "$@"; do
  case "$a" in
    --url=*) LANDING_URL="${a#*=}" ;;
    --profile-dir=*) PROFILE_DIR="${a#*=}" ;;
    [0-9]*) PORT="$a" ;;
  esac
done
case "${PROFILE_DIR}" in "~/"*) PROFILE_DIR="${HOME}/${PROFILE_DIR#~/}" ;; esac

if [ ! -x "${CHROME}" ]; then echo "找不到 Chrome: ${CHROME}（在 ~/.browser-runner/config.toml 设 chrome_path）"; exit 1; fi
mkdir -p "${PROFILE_DIR}"

echo "==> 专用 profile 启动 · 端口 ${PORT} · profile=${PROFILE_DIR}"
echo "    首次请在弹出窗口里登录你要自动化的站点（登录持久·只此一次）。"
nohup "${CHROME}" --remote-debugging-port="${PORT}" --user-data-dir="${PROFILE_DIR}" \
  --no-first-run --no-default-browser-check ${LANDING_URL:+"${LANDING_URL}"} >/dev/null 2>&1 &
disown 2>/dev/null || true

printf "    waiting for debug port"
i=0
while [ "${i}" -lt 15 ]; do
  if curl -s --max-time 1 "http://127.0.0.1:${PORT}/json/version" | grep -q webSocketDebuggerUrl; then
    printf "\nOK: 调试端口 %s 就绪，browser-runner 可 attach。\n" "${PORT}"
    exit 0
  fi
  printf "."
  sleep 1; i=$((i + 1))
done
printf "\nWARN: 端口 %s 15s 内未就绪。\n" "${PORT}"
exit 1
