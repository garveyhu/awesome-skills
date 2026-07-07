// api.js —— 取数（GET JSON）。POST /api/run 的 SSE 流在 run.js 里手动解析。

async function getJSON(url) {
  const resp = await fetch(url, { headers: { Accept: "application/json" } });
  if (!resp.ok) throw new Error(`${url} → HTTP ${resp.status}`);
  return resp.json();
}

/** GET /api/doctor → { port, flows, missing_secrets:[...] } */
export const getDoctor = () => getJSON("/api/doctor");

/** GET /api/flows → { flows:[{name,title,description,icon,group,write_ops,...,params,needs,source}] } */
export const getFlows = () => getJSON("/api/flows");

/** POST /api/chrome → { ok, port, message } 一键起 browser-runner 专属 profile 的调试 Chrome */
export const launchChrome = () =>
  fetch("/api/chrome", { method: "POST" }).then((r) => r.json());
