"""RefineRefresh —— 透传 IMAGE+MASK,但 IS_CHANGED 永远变 → 强制下游每次"运行"重算。
用于交互微调(MaskEditor 重绘遮罩后,ComfyUI 有时不让 LoadImage 缓存失效):
把它插在 LoadImage 之后,RMBG/MaskComposite 就会每次拿最新涂抹结果重跑。"""


class RefineRefresh:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"image": ("IMAGE",), "mask": ("MASK",)}}
    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("IMAGE", "MASK")
    FUNCTION = "go"
    CATEGORY = "image"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")     # 永远算"变了" → 每次运行强制重算下游(吃当前涂抹/滑块)

    def go(self, image, mask):
        return (image, mask)


NODE_CLASS_MAPPINGS = {"RefineRefresh": RefineRefresh}
NODE_DISPLAY_NAME_MAPPINGS = {"RefineRefresh": "Refine Refresh (force recompute)"}
