#!/usr/bin/env bash
# gen-batch.sh —— 并发批量出图：扫描 jobs 目录，每个 job 并发调 gen-image.sh。
#
# 每个 job 文件：文件名(去 .txt) = 输出图基名，文件内容 = 完整提示词。
#   jobs/01-topic.txt  ->  <outdir>/01-topic.png
#
# 用法：
#   gen-batch.sh --jobs <目录> --outdir <目录> [--concurrency 3] [--ref 定妆图] [--size 16:9] [--dir 工作目录]
#
# 设计：
#   - prompt 走文件传入，免命令行转义与长度限制；
#   - 每个 job 输出独立路径，主路径(codex 直接存到 --out)并发安全；
#   - 用 FIFO 信号量做滚动并发，兼容 macOS 自带 bash 3.2（无 wait -n）。
#
# 注意：Codex 订阅有服务端速率限制。--concurrency 先从 3 起；遇到报错/限流降到 1-2，
#       失败的 job 单独重跑即可（已成功的图不受影响）。系列图保持同一角色：所有 job 带同一张 --ref。
set -uo pipefail

JOBS=""; OUTDIR=""; CONC=3; REF=""; SIZE=""; WDIR=""
while [ $# -gt 0 ]; do
  case "$1" in
    --jobs)        JOBS="${2:-}"; shift 2;;
    --outdir)      OUTDIR="${2:-}"; shift 2;;
    --concurrency) CONC="${2:-3}"; shift 2;;
    --ref)         REF="${2:-}"; shift 2;;
    --size)        SIZE="${2:-}"; shift 2;;
    --dir)         WDIR="${2:-}"; shift 2;;
    -h|--help)     grep '^#' "$0" | sed 's/^#\{1,\} \{0,1\}//'; exit 0;;
    *) echo "未知参数: $1" >&2; exit 2;;
  esac
done

[ -n "$JOBS" ] && [ -d "$JOBS" ] || { echo "缺少有效 --jobs 目录" >&2; exit 2; }
[ -n "$OUTDIR" ] || { echo "缺少 --outdir" >&2; exit 2; }
mkdir -p "$OUTDIR"

GEN="$(cd "$(dirname "$0")" && pwd)/gen-image.sh"
[ -x "$GEN" ] || { echo "找不到 gen-image.sh: $GEN" >&2; exit 1; }

shopt -s nullglob
jobs=( "$JOBS"/*.txt )
[ "${#jobs[@]}" -gt 0 ] || { echo "$JOBS 下没有 .txt job 文件" >&2; exit 2; }

echo "[gen-batch] ${#jobs[@]} 个任务，并发度 $CONC → $OUTDIR" >&2

# FIFO 信号量：放 CONC 个令牌，每启动一个任务取一个、结束归还一个 —— 始终最多 CONC 个并发
fifo="$(mktemp -u)"; mkfifo "$fifo"; exec 9<>"$fifo"; rm -f "$fifo"
for ((i=0; i<CONC; i++)); do printf '\n' >&9; done

for job in "${jobs[@]}"; do
  read -u 9
  {
    name="$(basename "$job" .txt)"
    args=( --prompt "$(cat "$job")" --out "$OUTDIR/$name.png" )
    [ -n "$REF" ]  && args+=( --ref "$REF" )
    [ -n "$SIZE" ] && args+=( --size "$SIZE" )
    [ -n "$WDIR" ] && args+=( --dir "$WDIR" )
    if bash "$GEN" "${args[@]}" >/dev/null 2>&1; then
      echo "✓ $name"
    else
      echo "✗ $name（失败，可单独重跑）"
    fi
    printf '\n' >&9
  } &
done
wait
echo "[gen-batch] 全部结束" >&2
