#!/usr/bin/env python3
"""
把 docsify 站点编译成【单文件】offline.html —— 双击用浏览器(file://)即可打开，无需本地服务器。

策略（配合「共享库托管在 github」的架构）：
  - 内联本项目自己的东西：所有 .md（window.__MD__ + XHR/fetch 拦截，后缀匹配兼容 file://），
    以及本地相对资源（Animated 模式的 assets/anim* 等）—— 这样单个文件就够，不必带 assets 目录。
  - 共享第三方库（https://cdn.archeruuu.com/libs/... docsify/mermaid/gsap/prism…）保持引用，
    不内联 —— 文件小、且跨文档站共享缓存。
  - 不引用任何第三方 CDN、不内联巨型库。

产物：docs/docsify/offline.html。双击打开即可（需联网以从 github 取共享库；本项目内容/动画已内联）。

用法（脚本在 docs/docsify/scripts/ 下）：
  python3 docs/docsify/scripts/build-offline.py
"""
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))   # docs/
DOCSIFY_DIR = os.path.join(DOCS_ROOT, "docsify")                    # index.html 所在
TEMPLATE = os.path.join(DOCSIFY_DIR, "index.html")
OUTPUT = os.path.join(DOCSIFY_DIR, "offline.html")
SKIP_DIRS = {".git", "node_modules", ".github", ".idea"}

SHIM = r"""
(function () {
  var MD = window.__MD__ || {};
  function keyOf(url) {
    var p;
    try { p = new URL(url, document.baseURI).pathname; }
    catch (e) { p = String(url).split('?')[0].split('#')[0]; if (p[0] !== '/') p = '/' + p; }
    try { p = decodeURIComponent(p); } catch (e) {}
    return p;
  }
  function lookup(url) {
    var k = keyOf(url);
    if (Object.prototype.hasOwnProperty.call(MD, k)) return MD[k];
    var bestKey = null;
    for (var key in MD) {
      if (key.length <= k.length && k.slice(k.length - key.length) === key) {
        if (bestKey === null || key.length > bestKey.length) bestKey = key;
      }
    }
    return bestKey === null ? undefined : MD[bestKey];
  }
  var RealXHR = window.XMLHttpRequest;
  window.XMLHttpRequest = function () {
    var xhr = new RealXHR(), _url, _async = true;
    var _open = xhr.open, _send = xhr.send;
    xhr.open = function (m, u, a) { _url = u; _async = (a !== false); try { return _open.apply(xhr, arguments); } catch (e) {} };
    xhr.send = function () {
      var t = lookup(_url);
      if (t !== undefined) {
        try { Object.defineProperty(xhr, 'readyState', { configurable: true, get: function () { return 4; } }); } catch (e) {}
        try { Object.defineProperty(xhr, 'status', { configurable: true, get: function () { return 200; } }); } catch (e) {}
        try { Object.defineProperty(xhr, 'responseText', { configurable: true, get: function () { return t; } }); } catch (e) {}
        try { Object.defineProperty(xhr, 'response', { configurable: true, get: function () { return t; } }); } catch (e) {}
        setTimeout(function () {
          if (typeof xhr.onreadystatechange === 'function') xhr.onreadystatechange();
          if (typeof xhr.onload === 'function') xhr.onload();
          try { xhr.dispatchEvent(new Event('load')); } catch (e) {}
        }, 0);
        return;
      }
      return _send.apply(xhr, arguments);
    };
    return xhr;
  };
  var realFetch = window.fetch ? window.fetch.bind(window) : null;
  window.fetch = function (input, init) {
    var u = (typeof input === 'string') ? input : (input && input.url);
    var t = lookup(u || '');
    if (t !== undefined) {
      return Promise.resolve(new Response(t, { status: 200, headers: { 'Content-Type': 'text/markdown; charset=utf-8' } }));
    }
    return realFetch ? realFetch(input, init) : Promise.reject(new Error('offline miss'));
  };
})();
"""


def collect_markdown(root):
    md = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.lower().endswith(".md"):
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, root).replace(os.sep, "/")
                md["/" + rel] = open(full, "r", encoding="utf-8").read()
    return md


def is_remote(u):
    return u.startswith("http://") or u.startswith("https://") or u.startswith("//")


def read_local(href):
    return open(os.path.normpath(os.path.join(DOCSIFY_DIR, href.split("?")[0])), "r", encoding="utf-8").read()


def _comment_spans(html):
    return [(m.start(), m.end()) for m in re.finditer(r"<!--.*?-->", html, re.S)]


def _skippable(url, pos, spans):
    # 占位符（如 assets/anim/<name>.js）或注释内的引用——静默跳过，不当作真引用
    if "<" in url or ">" in url:
        return True
    return any(s <= pos < e for s, e in spans)


def inline_local_scripts(html):
    spans = _comment_spans(html)

    def repl(m):
        url = m.group(1)
        if is_remote(url) or _skippable(url, m.start(), spans):
            return m.group(0)  # 共享库（github）/ 注释内 / 占位符：保持原样
        try:
            return "<script>\n" + read_local(url) + "\n</script>"
        except Exception as e:
            print("  [跳过 script] %s (%s)" % (url, e)); return m.group(0)
    return re.sub(r'<script\s+src="([^"]+)"\s*></script>', repl, html)


def inline_local_styles(html):
    spans = _comment_spans(html)

    def repl(m):
        url = m.group(1)
        if url.startswith("data:") or is_remote(url) or _skippable(url, m.start(), spans):
            return m.group(0)  # data: / github 共享样式 / 注释内：保持原样
        try:
            return "<style>\n" + read_local(url) + "\n</style>"
        except Exception as e:
            print("  [跳过 style] %s (%s)" % (url, e)); return m.group(0)
    return re.sub(r'<link\s+rel="stylesheet"\s+href="([^"]+)"\s*/?>', repl, html)


def main():
    if not os.path.exists(TEMPLATE):
        sys.exit("找不到模板：%s" % TEMPLATE)
    html = open(TEMPLATE, "r", encoding="utf-8").read()

    # 1) 内联 md（趁 docsify 还是 <script src> 时定位注入点，确保拦截先于 docsify 执行）
    md = collect_markdown(DOCS_ROOT)
    data = json.dumps(md, ensure_ascii=False).replace("</", "<\\/")
    inject = "<script>\nwindow.__MD__ = %s;\n%s\n</script>\n" % (data, SHIM)
    pos = html.find("docsify.min.js")
    if pos == -1:
        pos = html.find("docsify@4")
    if pos == -1:
        sys.exit("找不到 docsify 核心脚本，无法定位注入点")
    tag_start = html.rfind("<script", 0, pos)
    html = html[:tag_start] + inject + html[tag_start:]

    # 2) 仅内联本地资源（动画等）；github 共享库保持引用
    html = inline_local_scripts(html)
    html = inline_local_styles(html)

    open(OUTPUT, "w", encoding="utf-8").write(html)
    print("内联 %d 个 markdown + 本地资源" % len(md))
    print("产物：%s（%.0f KB）" % (OUTPUT, os.path.getsize(OUTPUT) / 1024))
    print("双击用浏览器打开即可（需联网以从 github 取共享库；本项目内容/动画已内联，只请求 cdn.archeruuu.com）。")


if __name__ == "__main__":
    main()
