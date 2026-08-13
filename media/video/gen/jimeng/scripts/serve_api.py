#!/usr/bin/env python3
"""jimeng/scripts/serve_api.py — 把即梦包成 BYO 出图端点。

**为什么需要它**：即梦是 AK/SK 直连火山 visual API 的 CLI，而消费方（Channek 的
`channek.jimeng` provider、或任何 BYO 出图设置）发的是一段**归一化 JSON**：

    POST /image
    {"prompt": "...", "negative": "...", "width": 1024, "height": 1024, "model": "t2i-4.0"}
    → 200, Content-Type: image/png, body = PNG 字节

本服务就是那层翻译：收归一化请求 → 调 `jimeng_api.py` → 回图片字节。
**凭据不进请求也不进日志**——它由 `jimeng_api.py` 自己按三级发现读（环境变量 / _secrets / $AGENTS_RESOURCES）。

⚠️ 每次调用都是**真实付费**的云端出图，别拿它做压测。

跑：
    ~/.venvs/current/bin/python scripts/serve_api.py --port 8811
自检：
    curl -s localhost:8811/health
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
JIMENG_CLI = HERE / "jimeng_api.py"
PYTHON = os.environ.get("JIMENG_PYTHON", os.path.expanduser("~/.venvs/current/bin/python"))

DEFAULT_MODEL = "t2i-4.0"
DEFAULT_SIZE = 1024
# 即梦不吃独立的 negative 字段，只有一段 prompt。拼进去比默默丢掉诚实——
# 丢掉的话画风锁里的负向词会静默失效，而那正是「换个后端画风就漂」的根源。
NEGATIVE_PREFIX = "避免出现："


class Handler(BaseHTTPRequestHandler):
    timeout_seconds = 300

    def _json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path.rstrip("/") == "/health":
            self._json(200, {"ok": True, "cli": str(JIMENG_CLI), "exists": JIMENG_CLI.exists()})
        else:
            self._json(404, {"error": f"未知路径 {self.path}"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path.rstrip("/") != "/image":
            self._json(404, {"error": f"未知路径 {self.path}"})
            return
        try:
            length = int(self.headers.get("Content-Length") or 0)
            payload = json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, json.JSONDecodeError) as error:
            self._json(400, {"error": f"请求体不是合法 JSON：{error}"})
            return

        prompt = (payload.get("prompt") or "").strip()
        if not prompt:
            self._json(400, {"error": "prompt 不能为空"})
            return
        negative = (payload.get("negative") or "").strip()
        if negative:
            prompt = f"{prompt}。{NEGATIVE_PREFIX}{negative}"

        out = tempfile.mktemp(suffix=".png")
        cmd = [
            PYTHON, str(JIMENG_CLI),
            "--model", str(payload.get("model") or DEFAULT_MODEL),
            "--prompt", prompt,
            "--width", str(int(payload.get("width") or DEFAULT_SIZE)),
            "--height", str(int(payload.get("height") or DEFAULT_SIZE)),
            "--out", out,
        ]
        if payload.get("aspect"):
            cmd += ["--aspect", str(payload["aspect"])]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=self.timeout_seconds)
        if result.returncode != 0 or not os.path.exists(out):
            detail = (result.stderr or result.stdout or "")[-600:] or "无输出"
            self._json(502, {"error": f"即梦出图失败：{detail}"})
            return

        try:
            image = Path(out).read_bytes()
        finally:
            Path(out).unlink(missing_ok=True)

        self.send_response(200)
        self.send_header("Content-Type", "image/png")
        self.send_header("Content-Length", str(len(image)))
        self.end_headers()
        self.wfile.write(image)

    def log_message(self, fmt: str, *args) -> None:
        print(f"[jimeng] {fmt % args}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="即梦的 BYO 出图 HTTP 端点")
    parser.add_argument("--port", type=int, default=8811)
    parser.add_argument("--host", type=str, default="127.0.0.1")
    args = parser.parse_args()

    if not JIMENG_CLI.exists():
        sys.exit(f"找不到 {JIMENG_CLI}")
    print(f"[jimeng] POST http://{args.host}:{args.port}/image", flush=True)
    ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
