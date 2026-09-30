"""解析 Flow 服务端下发的模型清单（RPC HTTrJv），按需求挑出具体 modelKey 和点数。

纯函数、无 IO：输入清单 JSON + 用户档位，输出能用的模型。
清单字段位置是抓包实测的（2026-09），Google 改结构时只需改这里。
"""

from __future__ import annotations

from dataclasses import dataclass

# 用户可读的系列名 → 清单里的系列 id
FAMILIES = {
    "lite": "veo_3_1_lite",
    "fast": "veo_3_1_fast",
    "quality": "veo_3_1_quality",
    "omni": "abra",
}

ASPECTS = {"16:9": 2, "9:16": 1}
RESOLUTIONS = {1: "720p", 2: "1080p", 3: "4k", 4: "360p"}

INPUT_TEXT = 1  # 输入能力编码：1=文字 5=首帧图 7=尾帧图 6=参考图 14=视频


@dataclass(frozen=True)
class Model:
    key: str
    family: str
    family_name: str
    cost: int
    duration: int | None
    aspects: tuple[int, ...]
    resolution: str
    inputs: tuple[tuple[int, ...], ...]

    @property
    def is_t2v(self) -> bool:
        return (INPUT_TEXT,) in self.inputs


def _family_list(raw) -> list:
    return raw[0][4]


def _cost_for_tier(costs, tier: int) -> int | None:
    for entry in costs or []:
        if entry[0] == tier and entry[1] and entry[1][0]:
            return entry[1][0][1]
    return None


def _parse_entry(entry, family_id: str, family_name: str, tier: int) -> Model | None:
    cost = _cost_for_tier(entry[4], tier)
    if cost is None:
        return None  # 当前档位不可用
    inputs = tuple(tuple(alt[0]) for alt in (entry[7] or [[]])[0]) if entry[7] else ()
    res_code = entry[-1][0][0] if entry[-1] else 1
    return Model(
        key=entry[0],
        family=family_id,
        family_name=family_name,
        cost=cost,
        duration=entry[16],
        aspects=tuple(entry[12][0]) if entry[12] else (),
        resolution=RESOLUTIONS.get(res_code, str(res_code)),
        inputs=inputs,
    )


def available_models(raw, tier: int) -> list[Model]:
    models = []
    for fam in _family_list(raw):
        family_id = fam[3] if len(fam) > 3 else None
        if family_id not in FAMILIES.values():
            continue
        for entry in fam[1]:
            m = _parse_entry(entry, family_id, fam[0], tier)
            if m:
                models.append(m)
    return models


def pick_t2v(raw, tier: int, family: str, aspect: str, duration: int | None, resolution: str) -> Model:
    family_id = FAMILIES[family]
    aspect_code = ASPECTS[aspect]
    candidates = [
        m for m in available_models(raw, tier)
        if m.family == family_id and m.is_t2v and aspect_code in m.aspects and m.resolution == resolution
    ]
    if not candidates:
        raise LookupError(f"{family} 在当前档位没有 {aspect} {resolution} 的文生视频模型")
    if duration is not None:
        exact = [m for m in candidates if m.duration == duration]
        if not exact:
            options = sorted({m.duration for m in candidates})
            raise LookupError(f"{family} 不支持 {duration}s，可选 {options}")
        candidates = exact
    return min(candidates, key=lambda m: (m.cost, -(m.duration or 0)))
