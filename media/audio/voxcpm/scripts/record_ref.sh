#!/bin/bash
# record_ref.sh —— 为 voxcpm 声音克隆录一段「干声」参考音（macOS / ffmpeg）
# 用法: record_ref.sh [秒数=12] [输出=~/voice_ref.wav] [设备号]
#   设备号会随设备插拔变动，默认按名字自动定位 MacBook 麦克风（避开虚拟音频设备）；
#   想用别的麦：MIC_NAME="设备名片段" record_ref.sh，或显式传第 3 个参数。
#   首次运行若报权限错误：系统设置 → 隐私与安全性 → 麦克风 → 给当前终端打勾。
# 不用 set -e/pipefail：ffmpeg 列设备总以非零退出、脚本内多处 grep 正常返回非零，会误杀

SEC="${1:-12}"
OUT="${2:-$HOME/voice_ref.wav}"
PREF="${MIC_NAME:-麦克风}"             # 默认匹配任意「…麦克风」，排除 Virtual/Oray
RAW="${OUT%.wav}_raw.wav"

# 只取 avfoundation 的「audio devices」块（音视频各自从 [0] 编号，必须隔离）
AUDIO=$(ffmpeg -hide_banner -f avfoundation -list_devices true -i "" 2>&1 \
        | awk '/AVFoundation audio devices:/{f=1;next} f' \
        | sed -E 's/^\[AVFoundation[^]]*\] //' \
        | grep -E '^\[[0-9]+\]')

echo "== 音频输入设备 =="; printf '%s\n' "$AUDIO"; echo

# 设备号：显式传参优先；否则按名字定位；再不行取第一个非虚拟设备
if [ -n "${3:-}" ]; then
  DEV="$3"
else
  DEV=$(printf '%s\n' "$AUDIO" | grep -F "$PREF" | grep -viE 'virtual|oray' \
        | grep -oE '^\[[0-9]+\]' | head -1 | tr -dc '0-9')
  [ -z "$DEV" ] && DEV=$(printf '%s\n' "$AUDIO" | grep -viE 'virtual|oray' \
        | grep -oE '^\[[0-9]+\]' | head -1 | tr -dc '0-9')
fi
[ -z "${DEV:-}" ] && { echo "✗ 没找到可用麦克风，手动传设备号：record_ref.sh $SEC $OUT <号>"; exit 1; }

DEV_NAME=$(printf '%s\n' "$AUDIO" | grep -E "^\[$DEV\]" | sed -E 's/^\[[0-9]+\] //')
echo "选用设备 [$DEV] $DEV_NAME · 时长 ${SEC}s · 输出 $OUT"
echo "提示：安静房间 · 贴近麦克风 10~20cm · 正常语速念一句完整的话 · 别在空旷/瓷砖房（会录进回响）"
echo
for i in 3 2 1; do printf "  %s...\n" "$i"; sleep 1; done
echo "▶ 开始说话！（${SEC} 秒）"

ffmpeg -hide_banner -loglevel error -f avfoundation -i ":$DEV" \
  -t "$SEC" -ac 1 -ar 48000 -sample_fmt s16 -y "$RAW" || true
if [ ! -s "$RAW" ]; then
  echo "✗ 录音失败 / 空文件——多半是麦克风权限没给"
  echo "  去 系统设置 → 隐私与安全性 → 麦克风，勾选当前终端后重跑"
  exit 1
fi
echo "✓ 原始录音 $RAW"

# 轻清理：高通去低频隆隆 → 掐头尾静音 → 响度归一（无混响/无染色）
ffmpeg -hide_banner -loglevel error -i "$RAW" -af \
"highpass=f=70,silenceremove=start_periods=1:start_silence=0.08:start_threshold=-45dB:detection=peak,areverse,silenceremove=start_periods=1:start_silence=0.08:start_threshold=-45dB:detection=peak,areverse,loudnorm=I=-18:TP=-2:LRA=11" \
  -ar 48000 -ac 1 -y "$OUT"

DUR=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$OUT" 2>/dev/null || echo "?")
echo "✓ 清理后参考音 $OUT  (${DUR}s)"
echo
echo "试听：  afplay \"$RAW\"   |   afplay \"$OUT\""
echo
echo "下一步（把你刚念的原话逐字填进 --ref-text）："
echo "  python3 ~/.claude/skills/voxcpm/scripts/voxcpm_gen.py clone \\"
echo "    --ref-audio \"$OUT\" --ref-text \"你刚才念的那句话\" \\"
echo "    --text \"想让它念的新内容\" --timesteps 20 --out ~/clone_test.wav --play"
