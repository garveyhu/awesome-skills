"""SaveImageClean —— 干净名保存。
- 默认 <prefix>.png 同名覆盖(历史名=磁盘名);mode=increment 递增编号保留多版本。
- 可选 name 输入(接 LoadImageNamed 的图名)→ 存成 <prefix>/<name>.png,用源图名而非写死。
- IS_CHANGED 永远变 → 每次"运行"都真重存(否则 ComfyUI 缓存命中不会重存,递增失效)。"""
import os, glob, re
import numpy as np
from PIL import Image
import folder_paths


class SaveImageClean:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {"images": ("IMAGE",), "filename_prefix": ("STRING", {"default": "out"})},
            "optional": {
                "mode": (["overwrite", "increment"], {"default": "overwrite"}),
                "name": ("STRING", {"default": "", "forceInput": True}),
            },
        }
    RETURN_TYPES = ()
    FUNCTION = "save"
    OUTPUT_NODE = True
    CATEGORY = "image"
    DESCRIPTION = "Clean-name save. overwrite(default)/increment; optional name input uses source image name."

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")     # 永远算"变了" → 每次运行都重存(缓存不会跳过,递增才生效)

    def save(self, images, filename_prefix="out", mode="overwrite", name=""):
        out_dir = folder_paths.get_output_directory()
        results = []
        n = len(images)
        for i in range(n):
            arr = np.clip(255.0 * images[i].cpu().numpy(), 0, 255).astype(np.uint8)
            img = Image.fromarray(arr)
            if name:
                fp = filename_prefix.rstrip("/")
                stem = f"{fp}/{name}" if fp else name
            else:
                stem = filename_prefix
            base = stem + ("" if n == 1 else f"-{i + 1}")
            if mode == "increment":
                nums = [int(m.group(1)) for e in glob.glob(os.path.join(out_dir, base + "_*.png"))
                        if (m := re.search(r"_(\d+)\.png$", e))]
                rel = f"{base}_{(max(nums) + 1) if nums else 1:05d}.png"
            else:
                rel = base + ".png"
            path = os.path.join(out_dir, rel)
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            img.save(path, compress_level=4)
            results.append({"filename": os.path.basename(rel),
                            "subfolder": os.path.dirname(rel), "type": "output"})
        return {"ui": {"images": results}}


NODE_CLASS_MAPPINGS = {"SaveImageClean": SaveImageClean}
NODE_DISPLAY_NAME_MAPPINGS = {"SaveImageClean": "Save Image (clean name)"}
