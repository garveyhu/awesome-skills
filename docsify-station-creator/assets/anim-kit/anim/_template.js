/* ============================================================
   动画模板 —— 复制本文件改成 <名字>.js，写一个新动画。
   命名 kebab-case，与 markdown 里 data-anim="<名字>" 一致。
   ============================================================

   契约：
   - 调 AnimCore.register(name, factory, meta)
   - factory(stage, host, util) 在容器内构建画面，返回 { play, reset }
       · stage : 放内容的 DOM 容器（已加好内边距）
       · host  : 外层 .anim 元素
       · util  : { colors(), svg(tag, attrs) }
           - colors() → 当前主题色 { bg, fg, soft, mut, border, accent, accent2, accent3, warn, danger }
           - svg(tag, attrs) → 创建 SVG 元素
   - meta : { title, caption } —— 标题与底部说明（markdown 里不用再写）
   - 框架行为：滚动进视口自动 play()；右上角「↻ 重播」自动 reset()+play()
   - 取色一律用 util.colors()（勿硬编码），暗/亮才一致
   - 动画引擎用页面已加载的 GSAP（window.gsap）；务必判空，无 gsap 时给静态终态兜底

   markdown 里只写：  <div class="anim" data-anim="my-anim"></div>
   ============================================================ */
AnimCore.register('my-anim', function (stage, host, util) {
  var C = util.colors();
  var S = util.svg;
  var has = !!window.gsap;

  // —— 画静态骨架（坐标用 viewBox，宽度 100% 自适应）——
  var W = 760, H = 240;
  var svg = S('svg', { viewBox: '0 0 ' + W + ' ' + H, width: '100%' });
  stage.appendChild(svg);

  function text(x, y, str, o) {
    o = o || {};
    var t = S('text', { x: x, y: y, fill: o.fill || C.fg, 'font-size': o.size || 13,
      'font-family': 'ui-sans-serif, system-ui', 'text-anchor': o.anchor || 'middle', 'font-weight': o.weight || 600 });
    t.textContent = str; return t;
  }

  var box = S('rect', { x: 300, y: 90, width: 160, height: 56, rx: 12, fill: C.bg, stroke: C.border, 'stroke-width': 1.6 });
  svg.appendChild(box);
  var label = text(380, 124, '示例', { weight: 700 });
  svg.appendChild(label);
  var cap = text(W / 2, H - 12, '', { size: 12.5, weight: 600, fill: C.accent });
  svg.appendChild(cap);

  function reset() {
    box.setAttribute('stroke', C.border);
    box.setAttribute('stroke-width', 1.6);
    cap.textContent = '';
  }

  function play() {
    reset();
    if (!has) { box.setAttribute('stroke', C.accent3); cap.textContent = '（无 gsap：静态终态）'; return; }
    var tl = gsap.timeline();
    tl.call(function () { cap.textContent = '① 第一步…'; box.setAttribute('stroke', C.accent); });
    tl.to(box, { attr: { 'stroke-width': 3 }, duration: .25, yoyo: true, repeat: 1 });
    tl.call(function () { box.setAttribute('stroke', C.accent3); cap.textContent = '✓ 完成'; });
    return tl;
  }

  reset();
  return { play: play, reset: reset };
}, /*meta*/{ title: '我的动画标题', caption: '一句话说明这个动画在讲什么' });
