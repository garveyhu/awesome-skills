/* DAG 调度动画：start → (llm ∥ kb 并行) → merge(join) → if_else → 选 true
   → answer 执行 / fallback 整体 skip → end。演事件驱动 ready-queue 调度。 */
AnimCore.register('dag-execution', function (stage, host, util) {
  var C = util.colors();
  var S = util.svg;
  var has = !!window.gsap;

  var W = 760, H = 276;
  var svg = S('svg', { viewBox: '0 0 ' + W + ' ' + H, width: '100%' });
  stage.appendChild(svg);

  function text(x, y, str, o) {
    o = o || {};
    var t = S('text', { x: x, y: y, fill: o.fill || C.fg, 'font-size': o.size || 12,
      'font-family': 'ui-sans-serif, system-ui', 'text-anchor': 'middle', 'font-weight': o.weight || 600 });
    t.textContent = str; return t;
  }

  var N = {
    start: { cx: 46, cy: 138, t: 'start' },
    llm:   { cx: 176, cy: 64, t: 'LLM' },
    kb:    { cx: 176, cy: 212, t: 'KB 检索' },
    merge: { cx: 318, cy: 138, t: '聚合' },
    iff:   { cx: 446, cy: 138, t: 'if_else' },
    ans:   { cx: 588, cy: 64, t: 'answer' },
    fb:    { cx: 588, cy: 212, t: 'fallback' },
    end:   { cx: 712, cy: 138, t: 'end' }
  };
  var BW = 92, BH = 40;

  var defs = S('defs');
  var mk = S('marker', { id: 'dag-ar', viewBox: '0 0 10 10', refX: 9, refY: 5, markerWidth: 6, markerHeight: 6, orient: 'auto' });
  mk.appendChild(S('path', { d: 'M0,0 L10,5 L0,10 z', fill: C.mut })); defs.appendChild(mk); svg.appendChild(defs);

  var rects = {};
  function drawNode(k) {
    var n = N[k];
    var r = S('rect', { x: n.cx - BW / 2, y: n.cy - BH / 2, width: BW, height: BH, rx: 10, fill: C.bg, stroke: C.border, 'stroke-width': 1.5 });
    svg.appendChild(r); rects[k] = r;
    svg.appendChild(text(n.cx, n.cy + 4, n.t, { size: 12.5, weight: 700 }));
  }
  var edges = {};
  function drawEdge(id, a, b, lbl) {
    var na = N[a], nb = N[b];
    var x1 = na.cx + BW / 2, y1 = na.cy, x2 = nb.cx - BW / 2, y2 = nb.cy;
    var ln = S('line', { x1: x1, y1: y1, x2: x2, y2: y2, stroke: C.border, 'stroke-width': 1.6, 'marker-end': 'url(#dag-ar)' });
    svg.appendChild(ln); edges[id] = ln;
    if (lbl) svg.appendChild(text((x1 + x2) / 2, (y1 + y2) / 2 - 6, lbl, { size: 10, fill: C.mut }));
  }
  // 先画边后画节点（节点压在上层）
  drawEdge('s_llm', 'start', 'llm');
  drawEdge('s_kb', 'start', 'kb');
  drawEdge('llm_m', 'llm', 'merge');
  drawEdge('kb_m', 'kb', 'merge');
  drawEdge('m_if', 'merge', 'iff');
  drawEdge('if_ans', 'iff', 'ans', 'true');
  drawEdge('if_fb', 'iff', 'fb', 'false');
  drawEdge('ans_e', 'ans', 'end');
  drawEdge('fb_e', 'fb', 'end');
  Object.keys(N).forEach(drawNode);

  var cap = text(W / 2, H - 10, '', { size: 12.5, weight: 600, fill: C.accent });
  svg.appendChild(cap);

  function setNode(k, st) {
    var r = rects[k];
    if (st === 'run') { r.setAttribute('stroke', C.accent); r.setAttribute('stroke-width', 2.5); r.setAttribute('fill', C.bg); r.setAttribute('opacity', 1); }
    else if (st === 'done') { r.setAttribute('stroke', C.accent3); r.setAttribute('stroke-width', 2); r.setAttribute('fill', '#34d39915'); r.setAttribute('opacity', 1); }
    else if (st === 'skip') { r.setAttribute('stroke', C.mut); r.setAttribute('stroke-width', 1.2); r.setAttribute('stroke-dasharray', '4 3'); r.setAttribute('opacity', .45); }
    else { r.setAttribute('stroke', C.border); r.setAttribute('stroke-width', 1.5); r.setAttribute('fill', C.bg); r.setAttribute('opacity', 1); r.removeAttribute('stroke-dasharray'); }
  }
  function setEdge(id, st) {
    var e = edges[id];
    if (st === 'active') { e.setAttribute('stroke', C.accent3); e.setAttribute('stroke-width', 2.2); e.removeAttribute('stroke-dasharray'); e.setAttribute('opacity', 1); }
    else if (st === 'kill') { e.setAttribute('stroke', C.mut); e.setAttribute('stroke-dasharray', '4 3'); e.setAttribute('opacity', .35); }
    else { e.setAttribute('stroke', C.border); e.setAttribute('stroke-width', 1.6); e.removeAttribute('stroke-dasharray'); e.setAttribute('opacity', 1); }
  }

  function reset() {
    Object.keys(N).forEach(function (k) { setNode(k, 'pend'); });
    Object.keys(edges).forEach(function (id) { setEdge(id, 'pend'); });
    cap.textContent = '';
  }

  function play() {
    reset();
    if (!has) { Object.keys(N).forEach(function (k) { setNode(k, k === 'fb' ? 'skip' : 'done'); }); cap.textContent = '并行 + 汇聚 + 条件分支 skip'; return; }
    var tl = gsap.timeline();
    var D = 0.5;
    function run(keys, capt, edgesAfter) {
      tl.call(function () { cap.textContent = capt; keys.forEach(function (k) { setNode(k, 'run'); }); });
      tl.to({}, { duration: D });
      tl.call(function () { keys.forEach(function (k) { setNode(k, 'done'); }); (edgesAfter || []).forEach(function (e) { setEdge(e, 'active'); }); });
      tl.to({}, { duration: 0.25 });
    }
    run(['start'], '① start 入度0 → 入队执行', ['s_llm', 's_kb']);
    run(['llm', 'kb'], '② llm 与 kb 入度归零 → 并行执行（worker pool）', ['llm_m', 'kb_m']);
    run(['merge'], '③ 聚合：两条入边都完成（join 等齐）', ['m_if']);
    // if_else 选 true
    tl.call(function () { cap.textContent = '④ if_else 判定 → 选 true 分支'; setNode('iff', 'run'); });
    tl.to({}, { duration: D });
    tl.call(function () {
      setNode('iff', 'done');
      setEdge('if_ans', 'active');
      setEdge('if_fb', 'kill');     // false 边被 kill
      setNode('fb', 'skip');        // fallback 整体跳过
      setEdge('fb_e', 'kill');      // 沿边传播 skip
    });
    tl.to({}, { duration: 0.3 });
    run(['ans'], '⑤ answer 执行（false 分支被整体 skip）', ['ans_e']);
    run(['end'], '⑥ end：聚合输出', []);
    tl.call(function () { cap.textContent = '✓ 并行 + 汇聚 join + 条件分支 skip 一次跑通'; });
    return tl;
  }

  reset();
  return { play: play, reset: reset };
}, /*__META__*/{ title: "⚙️ DAG 调度：并行分支 + 汇聚 join + 条件分支 skip", caption: "入度归零入队 → 并行节点同时跑 → join 等齐 → if_else 选边、未选分支整体跳过" });
