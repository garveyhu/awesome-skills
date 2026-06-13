/* CRUD 模板动画：一套「鉴权→校验DTO→业务→ORM→审计→Result」六步模板，
   token 穿过点亮，然后 fan out 到约 30 个 admin 域 —— 读懂一个=读懂全部。 */
AnimCore.register('crud-template', function (stage, host, util) {
  var C = util.colors();
  var S = util.svg;
  var has = !!window.gsap;

  var W = 760, H = 268;
  var svg = S('svg', { viewBox: '0 0 ' + W + ' ' + H, width: '100%' });
  stage.appendChild(svg);

  function text(x, y, str, o) {
    o = o || {};
    var t = S('text', { x: x, y: y, fill: o.fill || C.fg, 'font-size': o.size || 12,
      'font-family': 'ui-sans-serif, system-ui', 'text-anchor': o.anchor || 'middle', 'font-weight': o.weight || 600 });
    t.textContent = str; return t;
  }

  var steps = ['① 鉴权', '② 校验 DTO', '③ 业务', '④ ORM', '⑤ 审计', '⑥ Result'];
  var sub = ['require_permission', '入参/出参分离', 'service 逻辑', '软删/加密', 'before/after', 'Result.ok'];
  var SY = 52, BW = 112, BH = 44;
  var cx = steps.map(function (_, i) { return 64 + i * 126; });
  var rects = [];
  for (var i = 0; i < steps.length - 1; i++) {
    svg.appendChild(S('line', { x1: cx[i] + BW / 2, y1: SY, x2: cx[i + 1] - BW / 2, y2: SY, stroke: C.border, 'stroke-width': 1.4 }));
  }
  steps.forEach(function (s, i) {
    var r = S('rect', { x: cx[i] - BW / 2, y: SY - BH / 2, width: BW, height: BH, rx: 10, fill: C.bg, stroke: C.border, 'stroke-width': 1.5 });
    svg.appendChild(r); rects.push(r);
    svg.appendChild(text(cx[i], SY - 3, s, { size: 12.5, weight: 700 }));
    svg.appendChild(text(cx[i], SY + 13, sub[i], { size: 9, fill: C.mut }));
  });

  var tok = S('circle', { cx: cx[0], cy: SY, r: 7, fill: C.accent, opacity: 0 });
  svg.appendChild(tok);

  svg.appendChild(text(W / 2, 112, '同一套模板，约 30 个 admin 域同构复制：', { size: 12, fill: C.mut }));
  var domains = ['providers', 'models', 'kbs', 'datasets', 'eval-jobs', 'plugins', 'marketplace', 'users', 'roles', 'api-keys', 'graphs', 'tools', 'embed-configs', '…+18'];
  var chips = [];
  var chX = 40, chY = 138, lineH = 32, gap = 10;
  domains.forEach(function (d) {
    var w = d.length * 7.4 + 22;
    if (chX + w > W - 30) { chX = 40; chY += lineH; }
    var g = S('g', {});
    g.appendChild(S('rect', { x: chX, y: chY, width: w, height: 24, rx: 8, fill: C.bg, stroke: C.accent2, 'stroke-width': 1.2 }));
    g.appendChild(text(chX + w / 2, chY + 16, d, { size: 11.5, weight: 600, fill: C.accent2 }));
    g.setAttribute('opacity', 0);
    svg.appendChild(g); chips.push(g);
    chX += w + gap;
  });

  var cap = text(W / 2, H - 8, '', { size: 12.5, weight: 600, fill: C.accent });
  svg.appendChild(cap);

  function reset() {
    if (has) gsap.set(tok, { x: 0, y: 0 });
    tok.setAttribute('cx', cx[0]); tok.setAttribute('opacity', 0);
    rects.forEach(function (r) { r.setAttribute('stroke', C.border); r.setAttribute('stroke-width', 1.5); });
    chips.forEach(function (g) { g.setAttribute('opacity', 0); });
    cap.textContent = '';
  }

  function play() {
    reset();
    if (!has) { rects.forEach(function (r) { r.setAttribute('stroke', C.accent3); }); chips.forEach(function (g) { g.setAttribute('opacity', 1); }); cap.textContent = '一套模板 × 约 30 域'; return; }
    var tl = gsap.timeline();
    tl.to(tok, { opacity: 1, duration: .2 });
    tl.call(function () { cap.textContent = '一次请求穿过六步模板'; });
    steps.forEach(function (s, i) {
      if (i > 0) tl.to(tok, { attr: { cx: cx[i] }, duration: .4, ease: 'power1.inOut' });
      tl.call(function () { rects[i].setAttribute('stroke', C.accent); rects[i].setAttribute('stroke-width', 2.6); });
      tl.to({}, { duration: .14 });
      tl.call(function () { rects[i].setAttribute('stroke', C.accent3); rects[i].setAttribute('stroke-width', 1.8); });
    });
    tl.to(tok, { opacity: 0, duration: .25 });
    tl.call(function () { cap.textContent = '➜ 约 30 个 admin 域同构复制这套模板（读懂一个=读懂全部）'; });
    chips.forEach(function (g) { tl.to(g, { opacity: 1, duration: .12 }, '-=0.04'); });
    return tl;
  }

  reset();
  return { play: play, reset: reset };
}, /*__META__*/{ title: "🧩 一套 CRUD 模板 × 约 30 个 admin 域", caption: "鉴权→校验DTO→业务→ORM→审计→Result 六步模板，providers/models/kbs/datasets… 同构复制" });
