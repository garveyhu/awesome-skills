"""产物落盘：决定输出文件名、下载签名地址。与 Flow / 浏览器无关。"""

from __future__ import annotations

import urllib.request
from pathlib import Path


def output_paths(out: str, ids: list[str], default_suffix: str) -> list[Path]:
    """单个产物且 out 带后缀 → 就用 out；否则 out 当前缀或目录，按序号 + id 前 8 位命名。"""
    target = Path(out).expanduser()
    if len(ids) == 1 and target.suffix:
        return [target]
    folder = target.parent if target.suffix else target
    stem = target.stem if target.suffix else "flow"
    suffix = target.suffix or default_suffix
    return [folder / f"{stem}-{i + 1}-{mid[:8]}{suffix}" for i, mid in enumerate(ids)]


def sniff_suffix(data: bytes) -> str | None:
    """按文件头判断真实格式。"""
    if data[:3] == b"\xff\xd8\xff":
        return ".jpg"
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return ".png"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return ".webp"
    if data[4:8] == b"ftyp":
        return ".mp4"
    return None


def download(url: str, dest: Path) -> tuple[Path, int]:
    """下载 Flow 的签名地址（无需 cookie，签名数小时有效），返回 (实际路径, 字节数)。

    Flow 出图固定给 JPEG：扩展名和真实格式对不上时改成真实的，避免 .png 里装 JPEG。
    """
    with urllib.request.urlopen(url, timeout=180) as resp:
        data = resp.read()
    real = sniff_suffix(data)
    alias = {".jpeg": ".jpg"}
    if real and alias.get(dest.suffix.lower(), dest.suffix.lower()) != real:
        dest = dest.with_suffix(real)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return dest, len(data)
