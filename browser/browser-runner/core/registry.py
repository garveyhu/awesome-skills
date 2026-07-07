"""流程登记表 —— 扫描所有 flow.toml，聚合成清单（看板 + CLI 的单一事实源）。

扫两处：本 skill 内置 `flows/`（可公开示例）+ 你私有 `~/.browser-runner/flows/`（永不入库）。
跳过 `_`/`.` 开头的目录（如 `_template`、`_private`）。
"""
from __future__ import annotations

import json
import tomllib
from pathlib import Path

try:
    from . import config
except ImportError:  # 脚本直跑
    import config

BUILTIN_FLOWS = Path(__file__).resolve().parent.parent / "flows"

_ALLOWED_TYPES = {"string", "int", "float", "bool"}


def _parse_flow(flow_dir: Path, source: str) -> dict | None:
    """解析一个 flow 目录的 flow.toml → 标准清单条目；元信息非法则返 None（跳过·不炸全表）。"""
    toml_path = flow_dir / "flow.toml"
    py_path = flow_dir / "flow.py"
    if not toml_path.exists() or not py_path.exists():
        return None
    try:
        data = tomllib.loads(toml_path.read_text("utf-8"))
    except Exception:  # noqa: BLE001
        return None
    f = data.get("flow", {})
    name = f.get("name") or flow_dir.name
    params = []
    for p in data.get("params", []):
        t = p.get("type", "string")
        params.append({
            "key": p["key"],
            "label": p.get("label", p["key"]),
            "type": t if t in _ALLOWED_TYPES else "string",
            "required": bool(p.get("required", False)),
            "default": p.get("default"),
        })
    return {
        "name": name,
        "title": f.get("title", name),
        "description": f.get("description", ""),
        "icon": f.get("icon", "🧩"),
        "group": f.get("group", "未分组"),
        "write_ops": bool(f.get("write_ops", False)),
        "landing_url": f.get("landing_url", ""),
        "params": params,
        "needs": list(data.get("secrets", {}).get("needs", [])),
        "source": source,
        "dir": str(flow_dir),
    }


def _scan(root: Path, source: str) -> list[dict]:
    if not root.exists():
        return []
    out = []
    for d in sorted(root.iterdir()):
        if not d.is_dir() or d.name.startswith(("_", ".")):
            continue
        entry = _parse_flow(d, source)
        if entry:
            out.append(entry)
    return out


def load_flows() -> list[dict]:
    """内置 + 私有全部流程；同名以私有覆盖内置（你能就地改示例行为）。"""
    builtin = _scan(BUILTIN_FLOWS, "builtin")
    private = _scan(config.private_flows_dir(), "private")
    by_name = {e["name"]: e for e in builtin}
    for e in private:
        by_name[e["name"]] = e
    return sorted(by_name.values(), key=lambda e: (e["group"], e["name"]))


def find_flow(name: str) -> dict | None:
    for e in load_flows():
        if e["name"] == name:
            return e
    return None


if __name__ == "__main__":
    print(json.dumps({"flows": load_flows()}, ensure_ascii=False, indent=2))
