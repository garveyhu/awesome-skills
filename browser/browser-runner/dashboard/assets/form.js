// form.js —— 按 flow.params schema 自动生成表单 + 收集类型化取值。
// 这是「加流程零改前端」的关键：前端是通用渲染器，不认识任何具体流程。

import { tmpl } from "./dom.js";

/** 为一个参数建控件（string→text / int·float→number / bool→checkbox）。 */
function control(p) {
  if (p.type === "bool") {
    const c = document.createElement("input");
    c.type = "checkbox";
    c.className = "input input--check";
    c.checked = p.default === true || p.default === "true";
    c.dataset.key = p.key;
    c.dataset.ptype = "bool";
    return c;
  }
  const i = document.createElement("input");
  i.className = "input";
  const numeric = p.type === "int" || p.type === "float";
  i.type = numeric ? "number" : "text";
  if (p.type === "float") i.step = "any";
  if (p.default != null && p.default !== "") i.value = p.default;
  if (p.required) i.required = true;
  i.placeholder = p.required
    ? "必填"
    : p.default != null && p.default !== ""
    ? String(p.default)
    : "可选";
  i.dataset.key = p.key;
  i.dataset.ptype = p.type;
  return i;
}

/** 把 params 渲染进 fieldsEl。无参数则给一句提示。 */
export function buildFields(fieldsEl, params) {
  fieldsEl.replaceChildren();
  if (!params || !params.length) {
    const hint = document.createElement("p");
    hint.className = "run-hint";
    hint.textContent = "此流程无需参数，直接运行。";
    fieldsEl.append(hint);
    return;
  }
  for (const p of params) {
    const field = tmpl("tmpl-field");
    if (p.type === "bool") field.classList.add("field--bool");
    field.querySelector("[data-label]").textContent = p.label || p.key;
    const req = field.querySelector("[data-req]");
    if (p.required) req.hidden = false;
    field.querySelector("[data-control]").append(control(p));
    fieldsEl.append(field);
  }
}

/** 从表单收集类型化取值。空的可选项省略（让后端填默认 / 校验必填）。 */
export function collect(formEl) {
  const out = {};
  for (const i of formEl.querySelectorAll("[data-key]")) {
    const key = i.dataset.key;
    const t = i.dataset.ptype;
    if (t === "bool") {
      out[key] = i.checked;
      continue;
    }
    const v = i.value.trim();
    if (v === "") continue;
    if (t === "int") out[key] = parseInt(v, 10);
    else if (t === "float") out[key] = parseFloat(v);
    else out[key] = v;
  }
  return out;
}
