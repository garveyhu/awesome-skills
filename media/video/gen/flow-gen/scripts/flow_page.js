// flow_page.js — 注入到 flow.google.com 标签页里运行的页面侧客户端。
// 两类能力：
//   1) 只读 RPC（点数 / 模型清单 / 项目 / 进度 / 下载地址）——直接调 batchexecute，不涉及 reCAPTCHA；
//   2) 提交生成——不自己拿 reCAPTCHA（Flow 会把外部调用的令牌标成 extension_hijack_detected 并拒绝），
//      而是在页面输入框里设好参数、点「生成」，让页面走它自己的正常流程。
// 装到 window.__flowgen，重复注入是幂等的。所有方法返回 JSON 字符串（webbridge evaluate 最稳）。
(() => {
  const VERSION = 2;
  if (window.__flowgen && window.__flowgen.version === VERSION) return 'ready';

  const BATCH_PATH = '/_/AiSandboxAngularFrontend/data/batchexecute';
  // 抓包实测的 RPC id（Flow 前端 bl=boq_labs-ai-sandbox-frontend_2026092x）
  const RPC = {
    credits: 'nzlxg',      // [] → [credits, tierCode, ...]
    catalog: 'HTrJv',      // [] → 模型清单（含每档点数 / 比例 / 时长）
    projects: 'UpteDb',    // ["projects/*",21,...] → 项目列表
    poll: 'jwpduf',        // [null,null,[[mediaId]]] → 状态
    media: 'as29s',        // [mediaId] → 含签名 mp4 地址
  };

  let reqid = 100000 + Math.floor(Math.random() * 800000);

  const sleep = ms => new Promise(r => setTimeout(r, ms));

  function wiz() {
    const w = window.WIZ_global_data;
    if (!w || !w.SNlM0e) throw new Error('WIZ_global_data 缺失：页面没加载完或没登录');
    return w;
  }

  function parseBatch(text, rpcid) {
    for (const line of text.split('\n')) {
      if (!line.startsWith('[[')) continue;
      let rows;
      try { rows = JSON.parse(line); } catch { continue; }
      for (const row of rows) {
        if (row[0] === 'wrb.fr' && row[1] === rpcid) {
          if (row[2] == null) throw new Error(`${rpcid} 被服务端拒绝: ${JSON.stringify(row).slice(0, 600)}`);
          return JSON.parse(row[2]);
        }
        if (row[0] === 'er') throw new Error(`${rpcid} 出错: ${JSON.stringify(row).slice(0, 600)}`);
      }
    }
    throw new Error(`${rpcid} 响应里没有结果: ${text.slice(0, 400)}`);
  }

  async function rpc(rpcid, payload) {
    const w = wiz();
    reqid += 100000;
    const qs = new URLSearchParams({
      rpcids: rpcid,
      'source-path': location.pathname,
      bl: w.cfb2h,
      'f.sid': w.FdrFJe,
      hl: document.documentElement.lang || 'en',
      _reqid: String(reqid),
      rt: 'c',
    });
    const body = new URLSearchParams({
      'f.req': JSON.stringify([[[rpcid, JSON.stringify(payload), null, 'generic']]]),
      at: w.SNlM0e,
    });
    const resp = await fetch(`${BATCH_PATH}?${qs}`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'x-same-domain': '1',
      },
      body: body.toString() + '&',
    });
    const text = await resp.text();
    if (!resp.ok) throw new Error(`${rpcid} HTTP ${resp.status}: ${text.slice(0, 300)}`);
    return parseBatch(text, rpcid);
  }

  // ---------- 输入框操作（用图标名 / aria 属性定位，不依赖界面语言） ----------
  const buttons = () => [...document.querySelectorAll('button')];
  const radios = () => [...document.querySelectorAll('[role=radio]')];
  const radioText = r => r.innerText.replace(/\s+/g, ' ').trim();

  function settingsTrigger() {
    return buttons().find(b => b.hasAttribute('cdkoverlayorigin') && b.hasAttribute('matbutton') && /crop_|x\d/.test(b.innerText));
  }

  function submitButton() {
    return buttons().find(b => b.innerText.trim() === 'arrow_forward' && b.hasAttribute('cdkoverlayorigin'));
  }

  async function clickRadio(pred, label) {
    const r = radios().find(x => pred(radioText(x)));
    if (!r) throw new Error(`找不到选项：${label}`);
    if (r.getAttribute('aria-checked') !== 'true') { r.click(); await sleep(400); }
  }

  async function ensureDirectMode() {
    if (settingsTrigger()) return;
    const toggle = buttons().find(b => b.hasAttribute('aria-pressed') && b.getAttribute('aria-pressed') === 'true');
    if (!toggle) throw new Error('找不到生成设置按钮：Flow 界面可能改版了');
    toggle.click(); // 关掉「智能体」，切到直接生成
    await sleep(800);
    if (!settingsTrigger()) throw new Error('切换到直接生成模式失败');
  }

  async function openSettings() {
    if (radios().some(r => /videocam/.test(r.innerText))) return;
    settingsTrigger().click();
    await sleep(900);
  }

  async function pickModel(familyName) {
    const current = buttons().find(b => /arrow_drop_down/.test(b.innerText) && b.innerText.includes(familyName));
    if (current) return;
    const dropdown = buttons().find(b => /arrow_drop_down/.test(b.innerText) && /(Veo|Omni)/.test(b.innerText));
    if (!dropdown) throw new Error('找不到视频模型下拉框');
    dropdown.click();
    await sleep(700);
    const item = [...document.querySelectorAll('[role=menuitem]')]
      .find(e => e.innerText.split('\n').map(s => s.trim()).includes(familyName));
    if (!item) throw new Error(`模型菜单里没有「${familyName}」`);
    item.click();
    await sleep(900);
  }

  function shownCost() {
    const links = [...document.querySelectorAll('a')];
    const link = links.find(a => /\d/.test(a.innerText) && a.closest('.cdk-overlay-container'))
      || links.find(a => /\d+\s*(个点数|credits?)/i.test(a.innerText));
    const m = link && link.innerText.match(/\d+/);
    return m ? Number(m[0]) : null;
  }

  function walkStrings(node, pred) {
    if (typeof node === 'string') return pred(node) ? node : null;
    if (Array.isArray(node)) {
      for (const c of node) {
        const hit = walkStrings(c, pred);
        if (hit) return hit;
      }
    }
    return null;
  }

  function summarizeMedia(item) {
    // item = [mediaId, projectId, workflowId, "CAE", null, [ts, prompt, ..., [status], 1, thumbUrl, ..., bytes], ...]
    const meta = item[5] || [];
    return {
      mediaId: item[0],
      projectId: item[1],
      status: meta[8] ? meta[8][0] : null,
      bytes: meta[13] ?? null,
      videoUrl: walkStrings(item, s => s.startsWith('https://flow-content.google/video/')),
    };
  }

  const api = {
    version: VERSION,

    async ready() {
      wiz();
      return JSON.stringify({
        path: location.pathname,
        recaptcha: !!(window.grecaptcha && window.grecaptcha.enterprise),
      });
    },

    async credits() {
      const d = await rpc(RPC.credits, []);
      return JSON.stringify({ credits: d[0], tier: d[1] });
    },

    async catalog() {
      return JSON.stringify(await rpc(RPC.catalog, []));
    },

    async projects() {
      const d = await rpc(RPC.projects, ['projects/*', 21, null, null, null, null, [1]]);
      const list = (d[0] || []).map(p => ({ id: p[0], name: p[1] && p[1][0] }));
      return JSON.stringify(list);
    },

    // 在输入框里设好「视频 · 帧 · 比例 · 模型 · 时长 · 分辨率 · 条数」，返回页面显示的点数供核对。
    async configureVideo({ familyName, aspect, duration, resolution, count = 1 }) {
      await ensureDirectMode();
      await openSettings();
      await clickRadio(t => t.startsWith('videocam'), '视频');
      await clickRadio(t => t.startsWith('crop_free'), '帧');
      await pickModel(familyName);
      await clickRadio(t => t.endsWith(aspect), aspect);
      // 时长选项形如「8 秒 / 8 s」；排除「360p」这类分辨率选项
      if (duration != null && radios().some(r => /^\d+\s*[^\dp]/.test(radioText(r)))) {
        await clickRadio(t => new RegExp(`^${duration}\\s*[^\\dp]`).test(t), `${duration}s`);
      }
      if (radios().some(r => /^(360p|720p)/.test(radioText(r)))) {
        await clickRadio(t => t.startsWith(resolution), resolution);
      }
      await clickRadio(t => t === `x${count}`, `x${count}`);
      const cost = shownCost();
      const summary = settingsTrigger() && settingsTrigger().innerText.replace(/\s+/g, ' ');
      document.body.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
      await sleep(400);
      return JSON.stringify({ cost, summary });
    },

    async clickSubmit() {
      const btn = submitButton();
      if (!btn) throw new Error('找不到「开始生成」按钮');
      if (btn.disabled) throw new Error('「开始生成」不可点：提示词没填进去');
      btn.click();
      return JSON.stringify({ clicked: true });
    },

    async poll(mediaIds) {
      const d = await rpc(RPC.poll, [null, null, mediaIds.map(id => [id])]);
      return JSON.stringify({ creditsLeft: d[1], media: (d[2] || []).map(summarizeMedia) });
    },

    async media(mediaId) {
      return JSON.stringify(summarizeMedia(await rpc(RPC.media, [mediaId])));
    },
  };

  window.__flowgen = api;
  return 'installed';
})();
