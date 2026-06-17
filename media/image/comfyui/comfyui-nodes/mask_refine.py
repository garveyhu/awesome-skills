"""MaskRefine —— 抠图掩膜合成器/微调(统一 1=保留/前景 约定)。
配合 ImageToMask(channel=alpha) 把各段 RGBA 取成 1=主体;合成后用 InvertMask 再喂 JoinImageWithAlpha
(Join 是 1=透明,故最后要反一次)。这样 auto/text/paint 的掩膜可任意 max/相减组合,零极性坑。
- keep:  out = max(base, paint)     涂/选的区域 → 并入保留
- erase: out = base * (1 - paint)   涂/选的区域 → 从保留里扣掉
invert_paint:若某来源的 ROI 是反的(0=ROI)则打开。"""
import torch
import torch.nn.functional as F


class MaskRefine:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "base_mask": ("MASK",),
            "paint_mask": ("MASK",),
            "mode": (["keep 补:涂哪留哪", "erase 擦:涂哪去掉"], {"default": "keep 补:涂哪留哪"}),
            "invert_paint": ("BOOLEAN", {"default": False}),
        }}
    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("MASK",)
    FUNCTION = "go"
    CATEGORY = "mask"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")

    def go(self, base_mask, paint_mask, mode, invert_paint=False):
        if base_mask.dim() == 2:
            base_mask = base_mask.unsqueeze(0)
        if paint_mask.dim() == 2:
            paint_mask = paint_mask.unsqueeze(0)
        if paint_mask.shape[-2:] != base_mask.shape[-2:]:
            paint_mask = F.interpolate(paint_mask.unsqueeze(1), size=base_mask.shape[-2:],
                                       mode="nearest").squeeze(1)
        if invert_paint:
            paint_mask = 1.0 - paint_mask
        if mode.startswith("keep"):
            out = torch.maximum(base_mask, paint_mask)      # 1=保留 → 并入
        else:
            out = base_mask * (1.0 - paint_mask)            # 扣掉
        return (out.clamp(0.0, 1.0),)


NODE_CLASS_MAPPINGS = {"MaskRefine": MaskRefine}
NODE_DISPLAY_NAME_MAPPINGS = {"MaskRefine": "Mask Refine (keep/erase 涂抹微调)"}
