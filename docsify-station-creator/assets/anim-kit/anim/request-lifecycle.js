/* 请求生命周期动画：一个请求包穿过 调用方→handler鉴权→service编排→provider→LLM，
   每站点亮 + 旁白；LLM 处自动落一条 trace；最后 SSE 逐帧回流到调用方。 */
AnimCore.register('request-lifecycle', function (stage, host, util) {
  var C = util.colors();
  var S = util.svg;
  var has = !!window.gsap;

  var W = 760, H = 300;
  var svg = S('svg', { viewBox: '0 0 ' + W + ' ' + H, width: '100%' });
  stage.appendChild(svg);

  function text(x, y, str, o) {
    o = o || {};
    var t = S('text', { x: x, y: y, fill: o.fill || C.fg, 'font-size': o.size || 12,
      'font-family': 'ui-sans-serif, system-ui', 'text-anchor': o.anchor || 'middle', 'font-weight': o.weight || 400 });
    t.textContent = str; return t;
  }

  var stages = [
    { cx: 88, t: '调用方', s: 'Bearer key' },
    { cx: 240, t: 'handler', s: '鉴权·分支' },
    { cx: 392, t: 'service', s: '编排·派发' },
    { cx: 540, t: 'provider', s: 'local/dify..' },
    { cx: 680, t: 'LLM', s: 'BaseLLM' }
  ];
  var BY = 64, BH = 46, BW = 120;
  var rects = [];
  stages.forEach(function (st) {
    var r = S('rect', { x: st.cx - BW / 2, y: BY, width: BW, height: BH, rx: 11, fill: C.bg, stroke: C.border, 'stroke-width': 1.5 });
    svg.appendChild(r); rects.push(r);
    svg.appendChild(text(st.cx, BY + 20, st.t, { weight: 700, size: 13 }));
    svg.appendChild(text(st.cx, BY + 37, st.s, { fill: C.mut, size: 10.5 }));
  });
  // 连接线
  for (var i = 0; i < stages.length - 1; i++) {
    svg.appendChild(S('line', { x1: stages[i].cx + BW / 2, y1: BY + BH / 2, x2: stages[i + 1].cx - BW / 2, y2: BY + BH / 2, stroke: C.border, 'stroke-width': 1.5 }));
  }

  // call_logs 盒
  var clX = 300, clY = 222, clW = 160, clH = 34;
  var clBox = S('rect', { x: clX, y: clY, width: clW, height: clH, rx: 9, fill: 'none', stroke: C.accent3, 'stroke-width': 1.3, 'stroke-dasharray': '5 4', opacity: .6 });
  svg.appendChild(clBox);
  svg.appendChild(text(clX + clW / 2, clY + 21, 'call_logs（trace）', { fill: C.accent3, size: 11.5, weight: 600 }));

  // 旁白
  var cap = text(W / 2, 132, '', { fill: C.accent, size: 13, weight: 600 });
  svg.appendChild(cap);

  // 请求包
  var pkt = S('circle', { cx: stages[0].cx, cy: BY + BH / 2, r: 7, fill: C.accent, opacity: 0 });
  svg.appendChild(pkt);
  // 落库小点
  var drop = S('circle', { cx: stages[4].cx, cy: BY + BH / 2, r: 5, fill: C.accent3, opacity: 0 });
  svg.appendChild(drop);

  var caps = [
    '① 调用方带 Bearer key 发起 /v1/invoke',
    '② handler：Depends 鉴权 → key 解析成应用身份',
    '③ service：注册表选 provider + 开 trace 作用域',
    '④ provider：按 source 派发（本地 / Dify / 工作流…）',
    '⑤ LLM：astream 出 token，callback 自动落 trace'
  ];

  var retChips = [];
  function reset() {
    if (has) { gsap.set(pkt, { x: 0, y: 0 }); gsap.set(drop, { x: 0, y: 0 }); }
    pkt.setAttribute('cx', stages[0].cx); pkt.setAttribute('cy', BY + BH / 2); pkt.setAttribute('opacity', 0);
    drop.setAttribute('cx', stages[4].cx); drop.setAttribute('cy', BY + BH / 2); drop.setAttribute('opacity', 0);
    cap.textContent = '';
    rects.forEach(function (r) { r.setAttribute('stroke', C.border); r.setAttribute('stroke-width', 1.5); });
    clBox.setAttribute('opacity', .6);
    retChips.forEach(function (c) { if (c.parentNode) c.parentNode.removeChild(c); });
    retChips = [];
  }

  function play() {
    reset();
    if (!has) { cap.textContent = caps[4]; drop.setAttribute('opacity', 1); drop.setAttribute('cy', clY); return; }
    var tl = gsap.timeline();
    tl.to(pkt, { opacity: 1, duration: .2 });
    stages.forEach(function (st, idx) {
      tl.call(function () { cap.textContent = caps[idx]; });
      if (idx > 0) tl.to(pkt, { attr: { cx: st.cx }, duration: .55, ease: 'power1.inOut' });
      tl.call(function () { rects[idx].setAttribute('stroke', C.accent); });
      tl.to(rects[idx], { attr: { 'stroke-width': 3 }, duration: .18, yoyo: true, repeat: 1 });
      tl.call(function () { rects[idx].setAttribute('stroke', idx === stages.length - 1 ? C.accent : C.border); });
    });
    // LLM 落 trace：drop 点下落到 call_logs
    tl.set(drop, { opacity: 1 });
    tl.to(drop, { attr: { cy: clY + clH / 2 }, duration: .5, ease: 'power1.in' });
    tl.to(clBox, { attr: { opacity: 1 }, duration: .2 });
    tl.to(drop, { opacity: 0, duration: .2 });
    // SSE 回流：3 个 delta chip 从 LLM 往调用方走
    tl.call(function () { cap.textContent = '⑥ 流式回流：event:delta 一帧帧推回调用方'; });
    for (var k = 0; k < 3; k++) {
      (function (k) {
        var chip = S('rect', { x: stages[4].cx - 16, y: 100, width: 32, height: 14, rx: 4, fill: C.accent, opacity: 0 });
        svg.appendChild(chip); retChips.push(chip);
        tl.fromTo(chip, { opacity: 0 }, { opacity: .9, duration: .12 }, '+=0.05');
        tl.to(chip, { attr: { x: stages[0].cx - 16 }, duration: .6, ease: 'none' });
        tl.to(chip, { opacity: 0, duration: .15 });
      })(k);
    }
    tl.call(function () { cap.textContent = '✓ 一次 invoke 走完：四层穿透 + 自动埋点 + 流式返回'; });
    tl.to(pkt, { opacity: 0, duration: .3 });
    return tl;
  }

  reset();
  return { play: play, reset: reset };
}, /*__META__*/{ title: "🛰️ 一次 /v1/invoke 的生命周期（请求穿四层）", caption: "鉴权解析身份 → service 编排+选 provider → provider 调 LLM → 自动埋点落 trace → 流式返回" });
