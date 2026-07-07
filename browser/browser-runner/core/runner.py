"""browser-runner CLI —— 沉淀层的统一入口。

  browser-runner list                      列出所有流程
  browser-runner run <flow> -p k=v ...      跑一个流程（--dry-run 只连不动作 / --yes 放行写操作）
  browser-runner run <flow> --params-json '{...}'   参数走 JSON（看板/程序化调用用）
  browser-runner doctor                    体检：浏览器连通 + 密钥齐不齐 + 流程元信息合法
  browser-runner dashboard [--port N]       起可视化看板

设计：内核稳定，一个流程 = flows/<name>/{flow.toml 元信息, flow.py 实现 run()}。
加流程不改本文件。写操作流程默认停在提交前，且需 --yes 放行。
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

CORE_DIR = Path(__file__).resolve().parent
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))  # 让 flow.py 能 `from primitives import ...`

import config  # noqa: E402
import registry  # noqa: E402


@dataclass
class RunContext:
    """交给 flow.run(page, params, ctx) 的上下文。"""

    params: dict
    workdir: Path
    flow: dict
    dry_run: bool = False
    log: Callable[[str], None] = field(default=lambda m: None)

    def secret(self, spec: str):
        return config.get_secret(spec)


# ── 参数强转 ──

def _coerce(value: Any, typ: str):
    if value is None:
        return None
    if typ == "int":
        return int(value)
    if typ == "float":
        return float(value)
    if typ == "bool":
        return value in (True, "true", "1", "yes", "on") if isinstance(value, str) else bool(value)
    return str(value)


def build_params(flow: dict, raw: dict) -> dict:
    """按 flow.toml 的 params schema 校验 + 填默认 + 强转类型。缺必填则抛。"""
    out = {}
    for p in flow["params"]:
        key, typ = p["key"], p["type"]
        if key in raw and raw[key] not in (None, ""):
            out[key] = _coerce(raw[key], typ)
        elif p.get("default") is not None:
            out[key] = _coerce(p["default"], typ)
        elif p.get("required"):
            raise ValueError(f"缺必填参数：{key}（{p.get('label', key)}）")
        else:
            out[key] = None
    return out


# ── 加载 flow 模块 ──

def _load_flow_module(flow_dir: Path):
    py = Path(flow_dir) / "flow.py"
    mod_name = f"_flow_{Path(flow_dir).name}".replace("-", "_")
    spec = importlib.util.spec_from_file_location(mod_name, py)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    if not hasattr(mod, "run"):
        raise RuntimeError(f"{py} 缺 run(page, params, ctx) 函数")
    return mod


# ── 子命令 ──

def cmd_list(_args) -> int:
    flows = registry.load_flows()
    if not flows:
        print("（还没有流程。cp -r flows/_template flows/<name> 开一个。）")
        return 0
    group = None
    for f in flows:
        if f["group"] != group:
            group = f["group"]
            print(f"\n【{group}】")
        tag = " ✍️写" if f["write_ops"] else ""
        src = "" if f["source"] == "builtin" else " ·私有"
        print(f"  {f['icon']} {f['name']}{tag}{src} — {f['description']}")
    print()
    return 0


def cmd_run(args) -> int:
    flow = registry.find_flow(args.flow)
    if not flow:
        sys.stderr.write(f"❌ 没有流程 `{args.flow}`（`browser-runner list` 看有哪些）\n")
        return 2

    raw = json.loads(args.params_json) if args.params_json else {}
    for kv in args.p or []:
        k, _, v = kv.partition("=")
        raw[k] = v
    try:
        params = build_params(flow, raw)
    except ValueError as e:
        sys.stderr.write(f"❌ {e}\n")
        return 2

    if flow["write_ops"] and not args.yes and not args.dry_run:
        sys.stderr.write("⚠️ 写操作流程需 --yes 放行（或在看板里勾确认）。流程仍会停在提交前。\n")
        return 3

    ts = datetime.now().strftime("%y%m%d-%H%M%S")
    workdir = config.runs_dir() / f"{flow['name']}-{ts}"
    workdir.mkdir(parents=True, exist_ok=True)
    logf = (workdir / "run.log").open("a", encoding="utf-8")

    def log(msg: str) -> None:
        line = f"· {msg}"
        print(line, flush=True)  # 实时流给看板 SSE
        logf.write(line + "\n")
        logf.flush()

    log(f"流程 {flow['name']} · dry_run={args.dry_run} · 产物 {workdir}")
    try:
        from attach import connect, default_context, open_page
    except ImportError:
        sys.stderr.write("❌ 缺 playwright：pip install playwright（见 SKILL.md）\n")
        return 1

    try:
        pw, browser = connect()
    except RuntimeError as e:
        sys.stderr.write(f"❌ {e}\n")
        return 1

    ctx = RunContext(params=params, workdir=workdir, flow=flow, dry_run=args.dry_run, log=log)
    result: dict = {"ok": False}
    try:
        page = open_page(default_context(browser), flow.get("landing_url") or "")
        mod = _load_flow_module(flow["dir"])
        out = mod.run(page, params, ctx) or {}
        result = {"ok": True, **(out if isinstance(out, dict) else {"result": out})}
        log("完成 ✅")
    except Exception as e:  # noqa: BLE001 — 单个流程失败不该带崩 runner
        result = {"ok": False, "error": str(e)}
        log(f"失败 ❌ {e}")
    finally:
        browser.close()  # 只断 CDP，不关你的 Chrome
        pw.stop()
        logf.close()

    (workdir / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), "utf-8")
    print("__RESULT__ " + json.dumps(result, ensure_ascii=False), flush=True)  # 看板据此收尾
    return 0 if result.get("ok") else 1


def _port_alive(port: int) -> bool:
    try:
        with urllib.request.urlopen(f"http://localhost:{port}/json/version", timeout=1.5) as r:
            return b"webSocketDebuggerUrl" in r.read()
    except Exception:  # noqa: BLE001
        return False


def cmd_doctor(_args) -> int:
    ok = True
    print("browser-runner doctor")
    try:
        import playwright  # noqa: F401
        print("  ✅ playwright 已装")
    except ImportError:
        print("  ❌ playwright 未装（pip install playwright）")
        ok = False

    port = config.debug_port()
    if _port_alive(port):
        print(f"  ✅ Chrome 调试端口 {port} 通")
    else:
        print(f"  ⚠️ Chrome 调试端口 {port} 不通 —— bash core/chrome_debug.sh 起浏览器")

    flows = registry.load_flows()
    print(f"  · 流程 {len(flows)} 个")
    missing = set()
    for f in flows:
        for spec in f["needs"]:
            if not config.has_secret(spec):
                missing.add(spec)
    if missing:
        print(f"  · secrets.toml 里还没配：{', '.join(sorted(missing))}")
    else:
        print("  ✅ 各流程所需密钥齐（或无需密钥）")
    return 0 if ok else 1


def cmd_dashboard(args) -> int:
    dash_dir = CORE_DIR.parent / "dashboard"
    sys.path.insert(0, str(dash_dir))
    import server  # type: ignore
    return server.serve(args.port)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="browser-runner", description="沉淀 & 复放浏览器自动化流程")
    # 子命令非必填：裸跑（无参数）默认开看板（见文末）
    sub = ap.add_subparsers(dest="cmd", required=False)

    sub.add_parser("list", help="列出所有流程").set_defaults(func=cmd_list)

    pr = sub.add_parser("run", help="跑一个流程")
    pr.add_argument("flow")
    pr.add_argument("-p", action="append", metavar="key=value", help="参数（可多次）")
    pr.add_argument("--params-json", help="参数 JSON（看板/程序化用）")
    pr.add_argument("--dry-run", action="store_true", help="只连+导航+定位，不动作")
    pr.add_argument("--yes", action="store_true", help="放行写操作流程")
    pr.set_defaults(func=cmd_run)

    sub.add_parser("doctor", help="体检依赖/连通/密钥").set_defaults(func=cmd_doctor)

    pd = sub.add_parser("dashboard", help="起可视化看板")
    pd.add_argument("--port", type=int, default=8760)
    pd.set_defaults(func=cmd_dashboard)

    args = ap.parse_args(argv)
    if not getattr(args, "func", None):  # 裸跑 → 开看板
        return cmd_dashboard(argparse.Namespace(port=8760))
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
