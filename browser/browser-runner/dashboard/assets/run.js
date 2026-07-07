// run.js —— 触发一个流程 + 手动解析 POST 的 SSE 流。
// EventSource 只支持 GET，/api/run 是 POST，所以用 fetch() + body.getReader() 逐块读、
// 按空行(\n\n)切事件、解析 event:/data: 行。

import { collect } from "./form.js";
import { renderResult, setStatus } from "./result.js";

/** 解析一个 SSE 事件块（两行：event: x / data: y）。 */
function parseEvent(raw) {
  let event = "message";
  const data = [];
  for (const line of raw.split("\n")) {
    if (line.startsWith("event:")) event = line.slice(6).trim();
    else if (line.startsWith("data:")) data.push(line.slice(5).replace(/^ /, ""));
  }
  return { event, data: data.join("\n") };
}

/** POST /api/run，逐事件回调 onLog / onDone。 */
async function stream(body, { onLog, onDone }) {
  const resp = await fetch("/api/run", {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "text/event-stream" },
    body: JSON.stringify(body),
  });
  if (!resp.ok || !resp.body) throw new Error(`HTTP ${resp.status}`);

  const reader = resp.body.getReader();
  const decoder = new TextDecoder();
  let buf = "";

  const dispatch = (raw) => {
    if (!raw.trim()) return;
    const { event, data } = parseEvent(raw);
    if (event === "done") onDone(data);
    else onLog(data);
  };

  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    buf += decoder.decode(value, { stream: true });
    let idx;
    while ((idx = buf.indexOf("\n\n")) >= 0) {
      dispatch(buf.slice(0, idx));
      buf = buf.slice(idx + 2);
    }
  }
  if (buf) dispatch(buf); // 冲刷残余
}

function appendLog(logEl, line) {
  const atBottom = logEl.scrollHeight - logEl.scrollTop - logEl.clientHeight < 24;
  logEl.append(document.createTextNode(line + "\n"));
  if (atBottom) logEl.scrollTop = logEl.scrollHeight;
}

/** 运行一张卡里的流程。card=<article>，flow=元信息。 */
export async function runFlow(card, flow) {
  const form = card.querySelector("[data-form]");
  if (!form.reportValidity()) return;

  const params = collect(form);
  const dryRun = card.querySelector("[data-dryrun]").checked;

  let yes = false;
  if (flow.write_ops && !dryRun) {
    const ok = window.confirm(
      `「${flow.title || flow.name}」是写操作流程。\n\n` +
        `流程会停在提交按钮前、不会自己点提交，最后一下交回给你。\n\n确认现在运行？`
    );
    if (!ok) return;
    yes = true;
  }

  const btn = card.querySelector("[data-run]");
  const out = card.querySelector("[data-output]");
  const log = card.querySelector("[data-log]");
  const result = card.querySelector("[data-result]");

  out.hidden = false;
  log.textContent = "";
  result.hidden = true;
  result.replaceChildren();
  btn.disabled = true;
  btn.classList.add("is-loading");
  setStatus(card, dryRun ? "运行中 · dry-run" : "运行中", "running");
  out.scrollIntoView({ block: "nearest", behavior: "smooth" });

  const body = { flow: flow.name, params, dry_run: dryRun, yes };

  try {
    await stream(body, {
      onLog: (line) => appendLog(log, line),
      onDone: (raw) => {
        let res;
        try {
          res = JSON.parse(raw);
        } catch {
          res = { ok: false, error: "结果解析失败：" + raw };
        }
        renderResult(result, res, flow);
        setStatus(card, res.ok ? "完成" : "失败", res.ok ? "ok" : "fail");
      },
    });
  } catch (e) {
    appendLog(log, "· 连接中断：" + e.message);
    setStatus(card, "出错", "fail");
  } finally {
    btn.disabled = false;
    btn.classList.remove("is-loading");
  }
}
