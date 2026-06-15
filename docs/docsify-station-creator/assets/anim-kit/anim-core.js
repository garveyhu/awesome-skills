/* ============================================================
   AnimCore —— 动画挂载框架
   用法（markdown 内，极简单标签）：
     <div class="anim" data-anim="ioc-injection"></div>
   动画模块（一动画一文件，自带 title/caption）：
     AnimCore.register('ioc-injection',
       function (stage, host, util) { ...; return { play, reset }; },
       { title: 'IoC 依赖倒置注入', caption: '实线=import 依赖（向下）·虚线=运行时调用（向上不 import）' });
   （markdown 里若仍写 data-title / data-caption 则覆盖 JS 里的，向后兼容）
   ============================================================ */
window.AnimCore = (function () {
  var registry = {};

  function register(name, factory, meta) { registry[name] = { factory: factory, meta: meta || {} }; }

  // 读取当前主题色（从 body 读：CSS 变量会从 :root 继承，且兼容 body.dark / html[data-theme] 两种主题约定）
  function colors() {
    var s = getComputedStyle(document.body || document.documentElement);
    function v(n, d) { var x = s.getPropertyValue(n).trim(); return x || d; }
    return {
      bg: v('--bg-card', '#131a2b'),
      fg: v('--fg', '#e6ecff'),
      soft: v('--fg-soft', '#aab4d4'),
      mut: v('--fg-mut', '#6c7795'),
      border: v('--border', '#1f2940'),
      accent: v('--accent', '#5ed1ff'),
      accent2: v('--accent2', '#a78bfa'),
      accent3: v('--accent3', '#34d399'),
      warn: v('--warn', '#fbbf24'),
      danger: v('--danger', '#fb7185')
    };
  }

  function svgEl(tag, attrs) {
    var e = document.createElementNS('http://www.w3.org/2000/svg', tag);
    if (attrs) for (var k in attrs) e.setAttribute(k, attrs[k]);
    return e;
  }

  function mountAll() {
    var list = document.querySelectorAll('.anim[data-anim]');
    Array.prototype.forEach.call(list, function (el) {
      if (el.__mounted) return;
      el.__mounted = true;
      var name = el.getAttribute('data-anim');
      var entry = registry[name];
      var factory = entry && entry.factory;
      var meta = (entry && entry.meta) || {};

      // 标题 / 说明：优先 markdown 的 data-*，否则取动画 JS 自带的 meta
      var title = el.getAttribute('data-title') || meta.title;
      var caption = el.getAttribute('data-caption') || meta.caption;
      if (caption) el.setAttribute('data-caption', caption); // 供 .anim::after 显示
      if (title) {
        var t = document.createElement('div');
        t.className = 'anim-title';
        t.textContent = title;
        el.appendChild(t);
      }
      // 舞台
      var stage = document.createElement('div');
      stage.className = 'anim-stage';
      stage.style.padding = '8px 10px 10px';
      el.appendChild(stage);

      if (!factory) {
        stage.innerHTML = '<div style="padding:24px;color:var(--fg-mut)">⏳ 动画「' + name + '」排期中（见 BUILD-PLAN 动画清单）</div>';
        return;
      }

      // 工具栏（重播）
      var bar = document.createElement('div');
      bar.className = 'anim-toolbar';
      var replay = document.createElement('button');
      replay.className = 'anim-btn';
      replay.textContent = '↻';
      replay.title = '重播';
      bar.appendChild(replay);
      el.appendChild(bar);

      var api = {};
      try {
        api = factory(stage, el, { colors: colors, svg: svgEl }) || {};
      } catch (e) {
        console.error('[anim]', name, e);
        stage.innerHTML = '<div style="padding:20px;color:var(--danger)">动画出错：' + e.message + '</div>';
        return;
      }

      replay.addEventListener('click', function () {
        if (api.reset) api.reset();
        if (api.play) api.play();
      });

      var played = false;
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting && !played) {
            played = true;
            if (api.play) api.play();
          }
        });
      }, { threshold: 0.3 });
      io.observe(el);
    });
  }

  return { register: register, mountAll: mountAll, colors: colors, svg: svgEl };
})();
