// app.js —— 装配：拉 doctor + flows，渲染，事件委托（展开卡 / 提交跑）+ 错峰弹入动效。

import { $, $$ } from "./dom.js";
import { getDoctor, getFlows, launchChrome } from "./api.js";
import { renderDoctor, renderFlows } from "./render.js";
import { runFlow } from "./run.js";

const main = $("#main");
const flowsByName = new Map();

// ── 动效系统：IntersectionObserver 错峰弹入 [data-reveal]（reduced-motion 命中则直接显示） ──
const REDUCED = matchMedia("(prefers-reduced-motion: reduce)").matches;
let revealIO = null;

/** 观测所有 [data-reveal]（含动态渲染出的 group/卡片）；进视口即弹入并停止观测。幂等。 */
function reveal() {
  const els = $$("[data-reveal]");
  if (REDUCED) {
    els.forEach((el) => el.classList.add("in"));
    return;
  }
  if (!revealIO) {
    revealIO = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add("in");
            revealIO.unobserve(e.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -6% 0px" }
    );
  }
  els.forEach((el) => {
    if (!el.classList.contains("in")) revealIO.observe(el);
  });
}

function toggleCard(card) {
  const open = card.classList.toggle("is-open");
  card.querySelector("[data-body]").hidden = !open;
  card.querySelector("[data-role='toggle']").setAttribute("aria-expanded", String(open));
}

function wire() {
  // 点卡头展开/收起
  main.addEventListener("click", (e) => {
    const toggle = e.target.closest("[data-role='toggle']");
    if (toggle && main.contains(toggle)) toggleCard(toggle.closest(".card"));
  });
  // 提交表单 → 跑流程
  main.addEventListener("submit", (e) => {
    const form = e.target.closest("[data-form]");
    if (!form) return;
    e.preventDefault();
    const card = form.closest(".card");
    const flow = flowsByName.get(card.dataset.flow);
    if (flow) runFlow(card, flow);
  });
}

async function refreshDoctor() {
  try {
    renderDoctor(await getDoctor());
  } catch {
    /* 忽略·保留上次状态 */
  }
}

/** 顶栏「起调试 Chrome」按钮 → POST /api/chrome，起完刷新连接状态（连上会自动藏按钮）。 */
function wireChrome() {
  const btn = $("[data-launch-chrome]");
  if (!btn) return;
  const label = $("[data-launch-label]", btn);
  btn.addEventListener("click", async () => {
    const prev = label.textContent;
    btn.disabled = true;
    btn.classList.add("is-loading");
    label.textContent = "启动中… 首次弹窗登录";
    try {
      const r = await launchChrome();
      btn.title = r.message || "";
      if (!r.ok) label.textContent = "未就绪 · 重试";
    } catch (e) {
      btn.title = String(e);
      label.textContent = "启动失败 · 重试";
    }
    await refreshDoctor(); // 连上则本按钮被 renderDoctor 隐藏
    btn.disabled = false;
    btn.classList.remove("is-loading");
    if (!btn.hidden) setTimeout(() => (label.textContent = prev), 2000);
  });
}

async function init() {
  wire();
  wireChrome();
  reveal(); // 海报头静态 [data-reveal] 先弹入
  try {
    const [doctor, data] = await Promise.all([getDoctor(), getFlows()]);
    renderDoctor(doctor);
    const flows = data.flows || [];
    flowsByName.clear();
    for (const f of flows) flowsByName.set(f.name, f);
    renderFlows(main, flows);
    reveal(); // 动态渲染出的 group/卡片再挂观测
  } catch (e) {
    main.setAttribute("aria-busy", "false");
    main.replaceChildren();
    const box = document.createElement("div");
    box.className = "loading";
    box.textContent = "加载失败：" + e.message + " —— 确认看板服务在跑（runner.py dashboard）。";
    main.append(box);
  }
}

init();
