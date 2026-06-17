#!/usr/bin/env bash
# 一键复刻"Mac 本地神经抠图 + 文字/选区抠图"整套(在另一台/另一个人的 ComfyUI 上重建)。
# 幂等:已装的跳过。全程走国内源(ghproxy / 清华 pypi / 魔搭)。
#
#   COMFYUI_HOME=~/Coding/Hub/ComfyUI bash scripts/setup/setup_matting.sh
#
# 做的事:① 装 ComfyUI-RMBG 节点 ② 装 Python 依赖(含 transformers 降级)
#         ③ 魔搭下模型(RMBG-2.0/SAM2/GroundingDINO/BiRefNet/bert)④ 打 GroundingDINO 补丁
#         ⑤ run.sh 设离线环境 ⑥ 装 skill 内置 5 个自定义节点
set -uo pipefail
SKILL="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
COMFY="${COMFYUI_HOME:-$HOME/Coding/Hub/ComfyUI}"
VENV="$COMFY/.venv"
PIPI="https://pypi.tuna.tsinghua.edu.cn/simple"
GH="https://ghproxy.net/https://github.com"
MS="$(command -v modelscope || echo "$HOME/.venvs/current/bin/modelscope")"
[[ -d "$COMFY" ]] || { echo "✗ ComfyUI 不在 $COMFY,用 COMFYUI_HOME 指定"; exit 1; }
[[ -x "$VENV/bin/python" ]] || { echo "✗ ComfyUI venv 不在 $VENV(需 uv venv 建好)"; exit 1; }
cd "$COMFY"
say(){ echo -e "\n=== $* ==="; }

say "1/6 ComfyUI-RMBG 节点(集成 RMBG-2.0/BEN2/INSPYRENET/SAM2/GroundingDINO/Florence2)"
if [[ -d custom_nodes/ComfyUI-RMBG ]]; then echo "已存在,跳过"; else
  git clone --depth 1 "$GH/1038lab/ComfyUI-RMBG.git" custom_nodes/ComfyUI-RMBG && echo "✓ 克隆完成"
fi

say "2/6 Python 依赖(uv pip + 清华源;不装 onnxruntime-gpu;transformers 降 4.49 兼容 GroundingDINO/Florence2)"
VIRTUAL_ENV="$VENV" uv pip install -i "$PIPI" \
  huggingface-hub transparent-background segment-anything opencv-python onnxruntime protobuf \
  hydra-core omegaconf iopath ftfy typing_extensions groundingdino-py modelscope \
  "transformers==4.49.0" 2>&1 | tail -3

say "3/6 魔搭下模型(国内带宽)"
dl(){ # repo  local_dir  files...
  local repo="$1" dir="$2"; shift 2
  if [[ -f "$dir/.done" ]]; then echo "  ✓ $repo 已下"; return; fi
  mkdir -p "$dir"; "$MS" download --model "$repo" "$@" --local_dir "$dir" 2>&1 | tail -1 && touch "$dir/.done"
}
dl briaai/RMBG-2.0           models/RMBG/RMBG-2.0   config.json model.safetensors birefnet.py BiRefNet_config.py
dl 1038lab/sam2             models/sam2            sam2.1_hiera_tiny.safetensors
dl 1038lab/GroundingDINO    models/grounding-dino  groundingdino_swint_ogc.safetensors GroundingDINO_SwinT_OGC.cfg.py
# BiRefNet(内置 RemoveBackground 节点用,可选):
[[ -f models/background_removal/BiRefNet.safetensors ]] || echo "  (可选)BiRefNet 未下,内置 matte 用;RMBG-2.0 已够"
# bert-base-uncased → HF 离线缓存(GroundingDINO 文本编码器必需)
BERT="$HOME/.cache/huggingface/hub/models--bert-base-uncased"
if [[ -d "$BERT/snapshots" ]]; then echo "  ✓ bert 已在缓存"; else
  mkdir -p "$BERT/snapshots/msdl0001" "$BERT/refs"; echo msdl0001 > "$BERT/refs/main"
  "$MS" download --model google-bert/bert-base-uncased config.json model.safetensors tokenizer.json tokenizer_config.json vocab.txt --local_dir "$BERT/snapshots/msdl0001" 2>&1 | tail -1
fi

say "4/6 补丁:GroundingDINO 兼容 transformers>=5 的 get_head_mask(若装了新版 transformers)"
BW="$VENV/lib/python3.12/site-packages/groundingdino/models/GroundingDINO/bertwarper.py"
if [[ -f "$BW" ]] && grep -q "self.get_head_mask = bert_model.get_head_mask" "$BW"; then
  "$VENV/bin/python" - "$BW" <<'PY'
import sys; f=sys.argv[1]; s=open(f).read()
s=s.replace("        self.get_head_mask = bert_model.get_head_mask",
"        self.get_head_mask = getattr(bert_model, 'get_head_mask', lambda head_mask, num_hidden_layers, is_attention_chunked=False: [None] * num_hidden_layers)")
open(f,"w").write(s); print("  ✓ 补丁已打")
PY
else echo "  跳过(已打或 4.x 不需要)"; fi

say "5/6 run.sh 设离线环境(只用本地缓存,不偷连国际 HF)"
RUN="$COMFY/run.sh"
if [[ -f "$RUN" ]] && ! grep -q HF_HUB_OFFLINE "$RUN"; then
  # 在 nohup 启动前插入 export
  /usr/bin/sed -i '' 's#^nohup #export HF_ENDPOINT="${HF_ENDPOINT:-https://hf-mirror.com}"\nexport HF_HUB_OFFLINE="${HF_HUB_OFFLINE:-1}"\nexport TRANSFORMERS_OFFLINE="${TRANSFORMERS_OFFLINE:-1}"\nnohup #' "$RUN" 2>/dev/null \
    && echo "  ✓ run.sh 加了离线 env" || echo "  ⚠ run.sh 自动改失败,请手动加 export HF_HUB_OFFLINE=1 等"
else echo "  跳过(已设或无 run.sh)"; fi

say "6/6 安装 skill 内置自定义节点(Cutout/MaskRefine/RefineRefresh/LoadImageNamed/SaveImageClean)"
if [[ -d "$SKILL/comfyui-nodes" ]]; then
  /bin/cp -R "$SKILL/comfyui-nodes/." "$COMFY/custom_nodes/" && echo "  ✓ 已复制到 custom_nodes/"
fi

echo -e "\n✅ 完成。重启 ComfyUI(./stop.sh && ./run.sh)生效。"
echo "   验证:画布打开 cutout 工作流;CLI 见 comfy.py matte --help。"
