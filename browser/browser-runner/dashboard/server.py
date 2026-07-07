"""看板本地服务 —— stdlib http.server，零三方依赖。

  GET  /                → index.html
  GET  /assets/*        → 静态资源
  GET  /api/flows       → registry 清单（前端据此渲染卡片 + 参数表单）
  GET  /api/doctor      → 连通/密钥体检
  POST /api/run         → {flow, params, dry_run, yes}；起 runner.py 子进程·SSE 流式回传输出

前端只是通用渲染器（按 flow.toml 的 params 生成表单），加流程零改前端。
"""
from __future__ import annotations

import json
import mimetypes
import os
import subprocess
import sys
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

DASH_DIR = Path(__file__).resolve().parent
SKILL_DIR = DASH_DIR.parent
CORE_DIR = SKILL_DIR / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

import config  # noqa: E402
import registry  # noqa: E402

RUNNER = CORE_DIR / "runner.py"


def _port_alive(port: int) -> bool:
    """调试端口上有没有活的 Chrome（看板据此显示已连接/未连接）。"""
    try:
        with urllib.request.urlopen(f"http://localhost:{port}/json/version", timeout=1.2) as r:
            return b"webSocketDebuggerUrl" in r.read()
    except Exception:  # noqa: BLE001
        return False


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):  # 静音默认访问日志
        pass

    # ── 工具 ──
    def _json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _static(self, rel: str):
        # 只允许 dashboard/ 内的文件（防目录穿越）
        target = (DASH_DIR / rel).resolve()
        if not str(target).startswith(str(DASH_DIR)) or not target.is_file():
            self.send_error(404)
            return
        ctype = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
        data = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")  # 本地开发工具·永远拿最新前端·免踩旧 JS
        self.end_headers()
        self.wfile.write(data)

    def _doctor(self):
        flows = registry.load_flows()
        missing = sorted({s for f in flows for s in f["needs"] if not config.has_secret(s)})
        return {
            "port": config.debug_port(),
            "flows": len(flows),
            "missing_secrets": missing,
            "chrome_alive": _port_alive(config.debug_port()),
        }

    def _launch_chrome(self):
        """从看板一键起 browser-runner 专属 profile 的调试 Chrome（跑 chrome_debug.sh）。

        显式把解析好的端口/profile/chrome 路径喂进去，确保起的正是稍后 attach 的那个浏览器。
        """
        script = CORE_DIR / "chrome_debug.sh"
        env = {
            **os.environ,
            "BROWSER_RUNNER_DEBUG_PORT": str(config.debug_port()),
            "BROWSER_RUNNER_PROFILE_DIR": str(config.profile_dir()),
            "BROWSER_RUNNER_CHROME_PATH": config.chrome_path(),
        }
        try:
            proc = subprocess.run(["bash", str(script)], capture_output=True,
                                  text=True, timeout=30, env=env)
            msg = ((proc.stdout or "") + (proc.stderr or "")).strip()
            return {"ok": proc.returncode == 0, "port": config.debug_port(), "message": msg[-800:]}
        except subprocess.TimeoutExpired:
            return {"ok": False, "port": config.debug_port(), "message": "chrome_debug.sh 超时（30s 未就绪）"}

    # ── 路由 ──
    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/" or path == "/index.html":
            self._static("index.html")
        elif path.startswith("/assets/"):
            self._static(path.lstrip("/"))
        elif path == "/api/flows":
            self._json({"flows": registry.load_flows()})
        elif path == "/api/doctor":
            self._json(self._doctor())
        else:
            self.send_error(404)

    def do_POST(self):
        path = self.path.split("?", 1)[0]
        if path == "/api/chrome":  # 一键起调试 Chrome
            self._json(self._launch_chrome())
            return
        if path != "/api/run":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length) or b"{}")
        flow = body.get("flow", "")
        params = body.get("params", {})

        cmd = [sys.executable, str(RUNNER), "run", flow,
               "--params-json", json.dumps(params, ensure_ascii=False)]
        if body.get("dry_run"):
            cmd.append("--dry-run")
        if body.get("yes"):
            cmd.append("--yes")

        # SSE：起子进程，逐行把 stdout/stderr 推给前端
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()

        def emit(event: str, data: str):
            try:
                self.wfile.write(f"event: {event}\ndata: {data}\n\n".encode("utf-8"))
                self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError):
                pass

        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                text=True, bufsize=1)
        result = None
        for line in proc.stdout:  # type: ignore[union-attr]
            line = line.rstrip("\n")
            if line.startswith("__RESULT__ "):
                result = line[len("__RESULT__ "):]
                continue
            emit("log", line)
        proc.wait()
        emit("done", result or json.dumps({"ok": proc.returncode == 0}))


def serve(port: int = 8760, open_browser: bool = True) -> int:
    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    url = f"http://localhost:{port}"
    print(f"==> 看板 {url}  （Ctrl-C 停）")
    # 自动在默认浏览器打开看板（BROWSER_RUNNER_NO_OPEN=1 可禁·如无头/测试）
    if open_browser and not os.environ.get("BROWSER_RUNNER_NO_OPEN"):
        import threading
        import webbrowser
        threading.Timer(0.4, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n停。")
    return 0


if __name__ == "__main__":
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 8760
    raise SystemExit(serve(p))
