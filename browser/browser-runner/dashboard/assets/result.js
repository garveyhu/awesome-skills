// result.js —— 把 done 事件的结果 JSON 漂亮展示（v3 扁平：kvv 大数字 + items 列表）+ 输出状态灯。

import { elem } from "./dom.js";

const RESERVED = ["ok", "count", "items", "todo", "error", "stopped_at"];

/** 设置输出面板的状态灯：running / ok / fail（run.js 调，CSS 按 data-kind 上色）。 */
export function setStatus(card, text, kind) {
  const s = card.querySelector("[data-status]");
  s.textContent = text;
  s.dataset.kind = kind;
}

function asText(v) {
  return typeof v === "object" ? JSON.stringify(v) : String(v);
}

function pad(i) {
  return String(i).padStart(2, "0");
}

/** 标量 → 大数字块：kvk 小标签 + kvv 超重描边大字。 */
function kvblock(k, v) {
  const b = elem("div", "kvblock");
  b.append(elem("div", "kvk", k), elem("div", "kvv mono", v));
  return b;
}

/** 数组 → 编号列表框（采集结果 / 待人工补）。 */
function itemsBox(arr, head, cap, todo) {
  const box = elem("div", todo ? "items items--todo" : "items");
  const h = elem("div", "items__head");
  h.append(elem("span", "items__t", head), elem("span", "items__c", `${arr.length} 条`));
  box.append(h);
  arr.slice(0, cap).forEach((it, i) => {
    const row = elem("div", "itm", asText(it));
    row.dataset.i = pad(i + 1);
    box.append(row);
  });
  if (arr.length > cap) {
    box.append(elem("div", "itm itm--more", `… 另有 ${arr.length - cap} 条，见原始结果`));
  }
  return box;
}

function failBlock(msg) {
  const b = elem("div", "rfail");
  b.append(elem("div", "rfail__t", "失败"));
  if (msg) b.append(elem("div", "rfail__m", msg));
  return b;
}

function okBlock() {
  const b = elem("div", "rok");
  b.append(elem("div", "rok__t", "完成"), elem("div", "rok__m", "流程已成功执行。"));
  return b;
}

function rawDetails(res) {
  const d = elem("details", "raw");
  d.append(elem("summary", null, "原始结果 JSON"));
  d.append(elem("pre", null, JSON.stringify(res, null, 2)));
  return d;
}

/** 渲染结果。box=[data-result]，res=结果 JSON，flow=流程元信息（判断写操作）。 */
export function renderResult(box, res, flow) {
  box.replaceChildren();
  box.hidden = false;

  if (!res || res.ok === false || res.error) {
    box.append(failBlock(res && res.error ? String(res.error) : "流程未成功完成"));
    if (res) box.append(rawDetails(res));
    return;
  }

  const data = elem("div", "result__data");

  // 标量摘要（count / stopped_at / url / selector …）
  if (typeof res.count === "number") data.append(kvblock("count", String(res.count)));
  if (res.stopped_at) {
    data.append(kvblock(flow && flow.write_ops ? "stopped·写" : "stopped_at", String(res.stopped_at)));
  }
  for (const [k, v] of Object.entries(res)) {
    if (RESERVED.includes(k) || v == null || typeof v === "object") continue;
    data.append(kvblock(k, asText(v)));
  }

  if (Array.isArray(res.items) && res.items.length) {
    data.append(itemsBox(res.items, "采集结果", 60, false));
  }
  if (!data.children.length) data.append(okBlock());
  box.append(data);

  if (Array.isArray(res.todo) && res.todo.length) {
    box.append(itemsBox(res.todo, "待人工补", 100, true));
  }
  box.append(rawDetails(res));
}
