"""解析 Flow 服务端下发的模型清单（RPC HTrJv），按需求挑出具体 modelKey 和点数。

纯函数、无 IO：输入清单 JSON + 用户档位，输出能用的模型。
清单字段位置是抓包实测的（2026-09），Google 改结构时只需改这里。
清单结构：raw[0][4] = 视频模型系列，raw[0][5] = 图片模型系列；每个系列 [显示名, [条目...], 启用?, 系列id]。
"""

from __future__ import annotations

from dataclasses import dataclass

# 用户可读的系列名 → 清单里的系列 id
VIDEO_FAMILIES = {
    "lite": "veo_3_1_lite",
    "fast": "veo_3_1_fast",
    "quality": "veo_3_1_quality",
    "omni": "abra",
}
IMAGE_FAMILIES = {
    "pro": "nano_banana_pro",
    "nb2": "narwhal_display",
    "lite": "harbor_seal",
}

VIDEO_ASPECTS = {"16:9": 2, "9:16": 1}
IMAGE_ASPECTS = ("16:9", "4:3", "1:1", "3:4", "9:16")
RESOLUTIONS = {1: "720p", 2: "1080p", 3: "4k", 4: "360p"}

# 视频生成模式 → 模型需要的输入组合（1=文字 5=首帧图 7=尾帧图 6=参考图 14=视频）
MODES = {
    "t2v": (1,),              # 文生视频
    "i2v": (1, 5),            # 首帧图生视频（「帧」）
    "first_last": (1, 5, 7),  # 首尾帧（「帧」）
    "r2v": (1, 6),            # 参考图生视频（「素材」）
}


@dataclass(frozen=True)
class VideoModel:
    key: str
    family: str
    family_name: str
    cost: int
    duration: int | None
    aspects: tuple[int, ...]
    resolution: str
    inputs: tuple[tuple[int, ...], ...]
    max_refs: int | None  # 素材模式最多几张参考图

    def supports(self, mode: str) -> bool:
        return MODES[mode] in self.inputs


@dataclass(frozen=True)
class ImageModel:
    key: str
    family: str
    family_name: str
    cost: int


def _cost_for_tier(costs, tier: int) -> int | None:
    for entry in costs or []:
        if entry[0] == tier and entry[1] and entry[1][0]:
            return entry[1][0][1]
    return None


def _families(raw, index: int, allowed: dict[str, str]) -> list:
    return [fam for fam in raw[0][index] or [] if len(fam) > 3 and fam[3] in allowed.values()]


def _parse_video(entry, fam, tier: int) -> VideoModel | None:
    cost = _cost_for_tier(entry[4], tier)
    if cost is None:
        return None  # 当前档位不可用
    inputs = tuple(tuple(alt[0]) for alt in (entry[7] or [[]])[0]) if entry[7] else ()
    res_code = entry[-1][0][0] if entry[-1] else 1
    return VideoModel(
        key=entry[0],
        family=fam[3],
        family_name=fam[0],
        cost=cost,
        duration=entry[16],
        aspects=tuple(entry[12][0]) if entry[12] else (),
        resolution=RESOLUTIONS.get(res_code, str(res_code)),
        inputs=inputs,
        max_refs=entry[9] if isinstance(entry[9], int) else None,
    )


def available_models(raw, tier: int) -> list[VideoModel]:
    models = []
    for fam in _families(raw, 4, VIDEO_FAMILIES):
        for entry in fam[1]:
            m = _parse_video(entry, fam, tier)
            if m and any(m.supports(mode) for mode in MODES):
                models.append(m)
    return models


def available_image_models(raw, tier: int) -> list[ImageModel]:
    models = []
    for fam in _families(raw, 5, IMAGE_FAMILIES):
        for entry in fam[1]:
            cost = _cost_for_tier(entry[4], tier)
            if cost is not None:
                models.append(ImageModel(key=entry[0], family=fam[3], family_name=fam[0], cost=cost))
    return models


def pick_model(raw, tier: int, family: str, mode: str, aspect: str,
               duration: int | None, resolution: str) -> VideoModel:
    """在当前档位里挑出满足 系列 / 模式 / 比例 / 分辨率 / 时长 的最便宜视频模型。"""
    family_id = VIDEO_FAMILIES[family]
    aspect_code = VIDEO_ASPECTS[aspect]
    candidates = [
        m for m in available_models(raw, tier)
        if m.family == family_id and m.supports(mode) and aspect_code in m.aspects and m.resolution == resolution
    ]
    if not candidates:
        raise LookupError(f"{family} 在当前档位没有 {aspect} {resolution} 的 {mode} 模型")
    if duration is not None:
        exact = [m for m in candidates if m.duration == duration]
        if not exact:
            options = sorted({m.duration for m in candidates})
            raise LookupError(f"{family} 的 {mode} 不支持 {duration}s，可选 {options}")
        candidates = exact
    return min(candidates, key=lambda m: (m.cost, -(m.duration or 0)))


def pick_image_model(raw, tier: int, family: str) -> ImageModel:
    family_id = IMAGE_FAMILIES[family]
    for m in available_image_models(raw, tier):
        if m.family == family_id:
            return m
    raise LookupError(f"图片模型 {family} 在当前档位不可用")
