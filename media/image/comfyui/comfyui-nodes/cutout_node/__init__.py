"""Cutout —— 前置"模式选择"抠图节点(文件夹包,带 web 扩展按 mode 显隐参数)。
mode 选 auto(RMBG) 或 text(SAM2),内部只跑选中的模型;委托 ComfyUI-RMBG 的 RMBG / SAM2Segment。"""


class Cutout:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "image": ("IMAGE",),
            "mode": (["auto 自动(RMBG)", "text 文字(SAM2)"],),
            "text_prompt": ("STRING", {"default": "the subject", "multiline": True}),
            "rmbg_model": (["RMBG-2.0", "BEN2", "INSPYRENET"], {"default": "RMBG-2.0"}),
            "sensitivity": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.05}),
            "mask_offset": ("INT", {"default": 0, "min": -64, "max": 64}),
            "mask_blur": ("INT", {"default": 0, "min": 0, "max": 64}),
            "refine_foreground": ("BOOLEAN", {"default": False}),
            "sam2_model": (["sam2.1_hiera_tiny", "sam2.1_hiera_small", "sam2.1_hiera_base_plus", "sam2.1_hiera_large"], {"default": "sam2.1_hiera_tiny"}),
            "dino_model": (["GroundingDINO_SwinT_OGC (694MB)", "GroundingDINO_SwinB (938MB)"], {"default": "GroundingDINO_SwinT_OGC (694MB)"}),
            "device": (["CPU", "Auto", "GPU"], {"default": "CPU"}),
            "threshold": ("FLOAT", {"default": 0.3, "min": 0.0, "max": 1.0, "step": 0.05}),
        }}
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    FUNCTION = "go"
    CATEGORY = "image"

    def go(self, image, mode, text_prompt, rmbg_model, sensitivity, mask_offset, mask_blur,
           refine_foreground, sam2_model, dino_model, device, threshold):
        from nodes import NODE_CLASS_MAPPINGS as N
        if mode.startswith("auto"):
            out = N["RMBG"]().process_image(
                image, rmbg_model, sensitivity=sensitivity, process_res=1024,
                mask_blur=mask_blur, mask_offset=mask_offset, invert_output=False,
                refine_foreground=refine_foreground, background="Alpha", background_color="#222222")
        else:
            out = N["SAM2Segment"]().segment_v2(
                image, text_prompt, sam2_model, dino_model, device, threshold=threshold,
                mask_blur=mask_blur, mask_offset=mask_offset, invert_output=False,
                background="Alpha", background_color="#222222")
        return (out[0],)


NODE_CLASS_MAPPINGS = {"Cutout": Cutout}
NODE_DISPLAY_NAME_MAPPINGS = {"Cutout": "Cutout (模式抠图:auto/text)"}
WEB_DIRECTORY = "./web"
