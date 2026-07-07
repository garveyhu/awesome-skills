// render.js —— 顶栏 doctor 状态（三色芯片 + 连接态 + launch 显隐）+ 分组流程卡。
// 图标：不再把 flow.icon 当文本渲染，改用命名 SVG 库 iconSvg(flow.icon)（零 emoji）。

import { $, tmpl, fill, elem } from "./dom.js";
import { buildFields } from "./form.js";
import { iconSvg } from "./icons.js";

// 卡片图标 tile 背景色按 index 轮转 pop 色板。
const PALETTE = ["blue", "coral", "violet", "lime", "cyan"];

/** doctor → 海报头三色芯片 + 连接状态 + 缺密钥黄条 + launch 按钮显隐。 */
export function renderDoctor(d) {
  $("[data-flowcount]").textContent = d.flows ?? "–";
  $("[data-port]").textContent = d.port ?? "–";

  // 调试 Chrome 连通状态：连上 → 连接芯片亮 lime·点脉冲·藏 launch；没连上 → 白底·灰点·露 launch
  const alive = !!d.chrome_alive;
  const conn = $("[data-conn]");
  if (conn) conn.textContent = alive ? "已连接" : "未连接";
  const connChip = $(".chip--conn");
  if (connChip) connChip.classList.toggle("is-alive", alive);
  const launch = $("[data-launch-chrome]");
  if (launch) launch.hidden = alive;

  const bar = $("#secrets-bar");
  const missing = d.missing_secrets || [];
  if (missing.length) {
    $("[data-missing]").textContent = missing.join("、");
    bar.hidden = false;
  } else {
    bar.hidden = true;
  }
}

function tag(text, kind) {
  return elem("span", `tag tag--${kind}`, text);
}

/** 单张流程卡。dataset.flow 存名字，运行时按名回查 flow 对象。idx 决定图标 tile 配色轮转。 */
function card(flow, idx) {
  const el = tmpl("tmpl-card");
  el.dataset.flow = flow.name;

  const icon = el.querySelector("[data-icon]");
  icon.classList.add("ic-" + PALETTE[idx % PALETTE.length]);
  icon.innerHTML = iconSvg(flow.icon); // 命名 SVG，非 flow.icon 文本（防 emoji / 防注入）

  fill(el, {
    title: flow.title || flow.name,
    desc: flow.description || "",
  });

  const badges = el.querySelector("[data-badges]");
  if (flow.write_ops) badges.append(tag("写操作", "write"));
  if (flow.source === "private") badges.append(tag("私有", "priv"));

  buildFields(el.querySelector("[data-fields]"), flow.params);

  const hint = el.querySelector("[data-runhint]");
  if (flow.write_ops) {
    hint.textContent = "写操作 · 会停在提交前，需二次确认";
    hint.classList.add("run-hint--write");
  }
  return el;
}

/** 按 group 分组渲染。空清单 → 空状态。给 group/卡片挂 data-reveal + --i 供错峰弹入。 */
export function renderFlows(main, flows) {
  main.replaceChildren();
  main.setAttribute("aria-busy", "false");

  if (!flows || !flows.length) {
    main.append(tmpl("tmpl-empty"));
    return;
  }

  const groups = new Map();
  for (const f of flows) {
    const g = f.group || "未分组";
    if (!groups.has(g)) groups.set(g, []);
    groups.get(g).push(f);
  }

  let idx = 0; // 全局卡片序号（跨组）→ 图标配色轮转
  let gi = 0; // group 序号 → 组标题错峰
  for (const [name, items] of groups) {
    const sec = tmpl("tmpl-group");
    sec.dataset.reveal = "";
    sec.style.setProperty("--i", String(gi++));
    fill(sec, { group: name, count: `${items.length}` });
    const grid = sec.querySelector("[data-grid]");
    let ci = 0; // 组内卡片序号 → 组内错峰
    for (const f of items) {
      const c = card(f, idx++);
      c.dataset.reveal = "";
      c.style.setProperty("--i", String(ci++));
      grid.append(c);
    }
    main.append(sec);
  }
}
