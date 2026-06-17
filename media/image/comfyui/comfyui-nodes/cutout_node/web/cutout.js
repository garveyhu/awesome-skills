import { app } from "/scripts/app.js";

function setVis(node, name, show) {
  const w = node.widgets?.find(x => x.name === name);
  if (!w) return;
  if (w.__t === undefined) { w.__t = w.type; w.__c = w.computeSize; w.__d = w.draw; }
  w.type = show ? w.__t : "hidden";
  w.computeSize = show ? w.__c : (() => [0, -4]);
  w.draw = show ? w.__d : function () {};   // 彻底不画(收住最后一个隐藏控件)
  if (w.element) w.element.style.display = show ? "" : "none";
}

const AUTO = ["rmbg_model", "sensitivity", "refine_foreground"];
const TEXT = ["text_prompt", "sam2_model", "dino_model", "device", "threshold"];

function hook(node) {
  if (!node || node.comfyClass !== "Cutout") return null;
  const modeW = node.widgets?.find(w => w.name === "mode");
  if (!modeW) return null;
  const apply = () => {
    const isAuto = String(modeW.value).startsWith("auto");
    AUTO.forEach(n => setVis(node, n, isAuto));
    TEXT.forEach(n => setVis(node, n, !isAuto));
    const sz = node.computeSize(); sz[0] = Math.max(sz[0], 340);  // 隐藏后保持宽度,标签不截断
    node.setSize(sz);
    app.graph?.setDirtyCanvas(true, true);
  };
  if (!node.__cutoutHooked) {
    node.__cutoutHooked = true;
    const orig = modeW.callback;
    modeW.callback = function () { const r = orig?.apply(this, arguments); apply(); return r; };
  }
  return apply;
}

app.registerExtension({
  name: "Cutout.ModeWidgets",
  nodeCreated(node) { hook(node); },
  afterConfigureGraph() { (app.graph?._nodes || []).forEach(n => { const a = hook(n); if (a) a(); }); },
  setup() { setTimeout(() => (app.graph?._nodes || []).forEach(n => { const a = hook(n); if (a) a(); }), 400); },
});
