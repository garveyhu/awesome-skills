"""LoadImageNamed —— 官方 LoadImage 之上多输出"图名"(裸文件名,无扩展名),
接到 SaveImageClean 的 name 口,保存时用源图名;文件夹由 SaveImageClean.filename_prefix 决定。"""
import os
from nodes import LoadImage


class LoadImageNamed(LoadImage):
    RETURN_TYPES = LoadImage.RETURN_TYPES + ("STRING",)
    RETURN_NAMES = ("IMAGE", "MASK", "name")
    FUNCTION = "load_named"
    CATEGORY = "image"

    def load_named(self, image, **kw):
        img, mask = self.load_image(image)
        return (img, mask, os.path.splitext(os.path.basename(image))[0])


NODE_CLASS_MAPPINGS = {"LoadImageNamed": LoadImageNamed}
NODE_DISPLAY_NAME_MAPPINGS = {"LoadImageNamed": "Load Image (with name)"}
