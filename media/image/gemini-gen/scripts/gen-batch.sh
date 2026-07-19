#!/usr/bin/env bash
# gen-batch.sh —— 并发批量出图：扫描 jobs 目录，每个 job 并发调 gen-image.sh。
#
# 每个 job 文件：文件名（去 .txt）= 输出图基名，文件内容 = 完整提示词。
#   jobs/01-topic.txt  ->  <outdir>/01-topic.png
#
# 用法：
#   gen-batch.sh --jobs <目录> --outdir <目录> [--concurrency 3] \
#     [--backend proxy|cookie] [--ref 定妆图] [--aspect 16:9] \
#     [--proxy-model 模型名] [--size 1K|2K|4K] \
#     [--account 账号别名] [--model flash|pro]
#
# 参数透传给 gen-image.sh（见其 --help）；--backend/--ref/--aspect 等对整批 job 生效。
#
# 设计：
#   - prompt 走文件传入，免命令行转义与长度限制；
#   - 每个 job 输出独立路径，并发安全；
#   - 用 FIFO 信号量做滚动并发，兼容 macOS 自带 bash 3.2（无 wait -n）。
#
# 并发建议（两个后端限流特性不同，别用同一个数字）：
#   - proxy 后端（默认）：多账号轮询在反代服务里做，--concurrency 先从 3 起，观察反代日志 /
#     管理台账号状态顶不顶得住，顶不住就降；某个 job 撞到坏账号不影响其它 job（各自独立进程）。
#   - cookie 后端：Google 有独立反自动化限流，gen_image.py 自带 pacing（请求前随机停顿）+
#     撞额度冷却，但那是按「单进程顺序请求」设计的——并发跑会削弱这层节奏控制，且多进程
#     共写 state.json 没加锁，并发下 LRU 游标可能互相覆盖（最坏只是负载没那么均匀，不会崩，
#     但更容易被限流）。cookie 后端 --concurrency 建议压到 1-2。
#
# 失败的 job 会打印 ✗ 但不影响其它 job；重跑整批时已成功的图不受影响（幂等靠你自己再跑一次
# 对应的 job 文件，脚本不做「跳过已存在」的判断——需要的话在外层自己按输出文件是否存在过滤）。
set -uo pipefail

JOBS=""; OUTDIR=""; CONC=3
BACKEND=""; REF=""; ASPECT=""
PROXY_MODEL=""; SIZE=""
ACCOUNT=""; MODEL=""
while [ $# -gt 0 ]; do
  case "$1" in
    --jobs)         JOBS="${2:-}"; shift 2;;
    --outdir)       OUTDIR="${2:-}"; shift 2;;
    --concurrency)  CONC="${2:-3}"; shift 2;;
    --backend)      BACKEND="${2:-}"; shift 2;;
    --ref)          REF="${2:-}"; shift 2;;
    --aspect)       ASPECT="${2:-}"; shift 2;;
    --proxy-model)  PROXY_MODEL="${2:-}"; shift 2;;
    --size)         SIZE="${2:-}"; shift 2;;
    --account)      ACCOUNT="${2:-}"; shift 2;;
    --model)        MODEL="${2:-}"; shift 2;;
    -h|--help)      grep '^#' "$0" | sed 's/^#\{1,\} \{0,1\}//'; exit 0;;
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

echo "[gen-batch] ${#jobs[@]} 个任务，后端 ${BACKEND:-proxy}，并发度 $CONC → $OUTDIR" >&2

# FIFO 信号量：放 CONC 个令牌，每启动一个任务取一个、结束归还一个 —— 始终最多 CONC 个并发
fifo="$(mktemp -u)"; mkfifo "$fifo"; exec 9<>"$fifo"; rm -f "$fifo"
for ((i=0; i<CONC; i++)); do printf '\n' >&9; done

for job in "${jobs[@]}"; do
  read -u 9
  {
    name="$(basename "$job" .txt)"
    args=( --prompt "$(cat "$job")" --out "$OUTDIR/$name.png" )
    [ -n "$BACKEND" ]     && args+=( --backend "$BACKEND" )
    [ -n "$REF" ]         && args+=( --ref "$REF" )
    [ -n "$ASPECT" ]      && args+=( --aspect "$ASPECT" )
    [ -n "$PROXY_MODEL" ] && args+=( --proxy-model "$PROXY_MODEL" )
    [ -n "$SIZE" ]        && args+=( --size "$SIZE" )
    [ -n "$ACCOUNT" ]     && args+=( --account "$ACCOUNT" )
    [ -n "$MODEL" ]       && args+=( --model "$MODEL" )
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
