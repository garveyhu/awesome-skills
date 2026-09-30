// flow_page.js — 注入到 flow.google.com 标签页里运行的页面侧客户端。
// 两类能力：
//   1) 只读 RPC（点数 / 模型清单 / 项目 / 进度 / 下载地址）——直接调 batchexecute，不涉及 reCAPTCHA；
//   2) 提交生成（视频 / 图片）——不自己拿 reCAPTCHA（Flow 会把外部调用的令牌标成 extension_hijack_detected
//      并拒绝），而是在页面输入框里设参数、放图、再由浏览器通道真实点击「生成」，让页面走它自己的流程。
// 装到 window.__flowgen，重复注入是幂等的。所有方法返回 JSON 字符串（webbridge evaluate 最稳）。
(() => {
  const VERSION = 10;
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
  const firstLine = el => el.innerText.split('\n')[0].trim();
  const overlayPanes = () => [...document.querySelectorAll('.cdk-overlay-pane')];
  // 只算有内容的弹窗（CDK 会留下空的 pane 容器）
  const openPanes = () => overlayPanes().filter(p => p.childElementCount && p.innerText.trim());
  const UPLOAD_MARK = 'data-flowgen-upload';

  function findButton(root, re) {
    return [...root.querySelectorAll('button')].find(b => re.test(b.innerText.trim()));
  }

  function settingsTrigger() {
    return buttons().find(b => b.hasAttribute('cdkoverlayorigin') && b.hasAttribute('matbutton') && /crop_|x\d/.test(b.innerText));
  }

  function settingsPane() {
    return openPanes().find(p => [...p.querySelectorAll('[role=radio]')].some(r => /videocam/.test(r.innerText)));
  }

  function submitButton() {
    return buttons().find(b => b.innerText.trim() === 'arrow_forward' && b.hasAttribute('cdkoverlayorigin'));
  }

  // 输入框里的「添加素材」；顶栏也有个 add 图标按钮（aria-haspopup="menu" 的下拉菜单），要排除
  function addIngredientButton() {
    return buttons().find(b => b.hasAttribute('maticonbutton') && b.innerText.trim() === 'add'
      && b.hasAttribute('aria-haspopup') && b.getAttribute('aria-haspopup') !== 'menu');
  }

  async function clickRadio(pred, label) {
    const r = radios().find(x => pred(radioText(x)));
    if (!r) throw new Error(`找不到选项：${label}`);
    if (r.getAttribute('aria-checked') !== 'true') { r.click(); await sleep(400); }
  }

  async function ensureDirectMode() {
    // 刚载入的项目页，输入框要过一会儿才渲染出来
    const agentToggle = () => buttons().find(b => b.hasAttribute('aria-pressed') && b.getAttribute('aria-pressed') === 'true');
    for (let i = 0; i < 50 && !settingsTrigger() && !agentToggle(); i++) await sleep(300);
    if (settingsTrigger()) return;
    const toggle = agentToggle();
    if (!toggle) throw new Error('找不到生成设置按钮：Flow 界面可能改版了');
    toggle.click(); // 关掉「智能体」，切到直接生成
    await sleep(800);
    if (!settingsTrigger()) throw new Error('切换到直接生成模式失败');
  }

  async function openSettings() {
    if (settingsPane()) return;
    settingsTrigger().click();
    for (let i = 0; i < 15 && !settingsPane(); i++) await sleep(150);
    if (!settingsPane()) throw new Error('生成设置面板没打开');
  }

  // 模型名按「整行相等」比较：Nano Banana 2 和 Nano Banana 2 Lite 不能互相误判
  async function pickModel(familyName) {
    const dropdown = () => [...settingsPane().querySelectorAll('button')].find(b => /arrow_drop_down/.test(b.innerText));
    if (!dropdown()) throw new Error('找不到模型下拉框');
    if (firstLine(dropdown()) === familyName) return;
    dropdown().click();
    await sleep(700);
    const item = [...document.querySelectorAll('[role=menuitem]')]
      .find(e => e.innerText.split('\n').map(s => s.trim()).includes(familyName));
    if (!item) throw new Error(`模型菜单里没有「${familyName}」`);
    item.click();
    await sleep(900);
    if (firstLine(dropdown()) !== familyName) throw new Error(`没能切换到模型「${familyName}」`);
  }

  function shownCost() {
    const links = [...document.querySelectorAll('a')];
    const link = links.find(a => /\d/.test(a.innerText) && a.closest('.cdk-overlay-container'))
      || links.find(a => /\d+\s*(个点数|credits?)/i.test(a.innerText));
    const m = link && link.innerText.match(/\d+/);
    return m ? Number(m[0]) : null;
  }

  // 依次尝试：设置面板再点一次它的按钮收起（它不认 Escape）→ 点遮罩层 → 点弹窗自带的 close 按钮 → Escape；
  // 每步确认弹窗数真的减少
  async function closeAllOverlays() {
    for (let i = 0; i < 6 && openPanes().length; i++) {
      const before = openPanes().length;
      const backdrop = [...document.querySelectorAll('.cdk-overlay-backdrop')].pop();
      const closeBtn = openPanes().map(p => findButton(p, /^close$/)).find(Boolean);
      if (settingsPane() && settingsTrigger()) settingsTrigger().click();
      else if (backdrop) backdrop.click();
      else if (closeBtn) closeBtn.click();
      else document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
      for (let j = 0; j < 10 && openPanes().length >= before; j++) await sleep(100);
    }
    if (openPanes().length) throw new Error('关不掉页面上的弹窗');
  }

  // ---------- 输入框里的图片：首帧 / 尾帧 / 素材 ----------
  const frameSlots = () => [...document.querySelectorAll('.frame-trigger')];
  const placedChips = () => [...document.querySelectorAll('.ingredient-bar-container button.chip-container')];

  function slotState(slot) {
    const el = frameSlots()[slot];
    if (!el) return 'missing';
    const chip = el.querySelector('button.chip-container');
    if (!chip) return 'empty';
    return chip.getAttribute('aria-busy') === 'true' ? 'busy' : 'filled';
  }

  // 首尾帧和素材都在 ingredient-bar 里，已放图的格子点一下即移除
  async function clearPlaced() {
    for (let i = 0; i < 12; i++) {
      const chip = placedChips()[0];
      if (!chip) return;
      chip.click();
      await sleep(500);
      await closeAllOverlays();
    }
    throw new Error('清不掉输入框里已放的图片');
  }

  function pickerPane() {
    return openPanes().find(p => [...p.querySelectorAll('button')].some(b => /(^|\s)upload(\s|$)/.test(b.innerText)));
  }

  function uploadOpener(target, slot) {
    if (target === 'frame') {
      if (slotState(slot) === 'missing') throw new Error('输入框里没有首尾帧格子：确认是「视频 · 帧」模式');
      return frameSlots()[slot].querySelector('button');
    }
    const add = addIngredientButton();
    if (!add) throw new Error('找不到「添加素材」按钮');
    return add;
  }

  function placedWith(target, slot, mediaId) {
    const chips = target === 'frame'
      ? [frameSlots()[slot]?.querySelector('button.chip-container')].filter(Boolean)
      : placedChips();
    return chips.some(c => c.getAttribute('aria-busy') !== 'true'
      && ((c.querySelector('img') || {}).src || '').includes(mediaId));
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

    // 在输入框里设好参数，返回页面显示的点数供核对。
    // media: video | image；composition（仅视频）: frames=首尾帧 / ingredients=素材
    async configure({ media, composition, familyName, aspect, duration, resolution, count = 1 }) {
      await ensureDirectMode();
      await openSettings();
      await clickRadio(t => t.startsWith(media === 'image' ? 'image' : 'videocam'), media);
      if (media === 'video') {
        await clickRadio(t => t.startsWith(composition === 'ingredients' ? 'chrome_extension' : 'crop_free'), composition);
      }
      await pickModel(familyName);
      await clickRadio(t => t.endsWith(aspect), aspect);
      // 时长选项形如「8 秒 / 8 s」；排除「360p」这类分辨率选项
      if (duration != null && radios().some(r => /^\d+\s*[^\dp]/.test(radioText(r)))) {
        await clickRadio(t => new RegExp(`^${duration}\\s*[^\\dp]`).test(t), `${duration}s`);
      }
      if (resolution && radios().some(r => /^(360p|720p)/.test(radioText(r)))) {
        await clickRadio(t => t.startsWith(resolution), resolution);
      }
      await clickRadio(t => t === `x${count}`, `x${count}`);
      const cost = shownCost();
      const summary = settingsTrigger() && settingsTrigger().innerText.replace(/\s+/g, ' ');
      await closeAllOverlays();
      await clearPlaced(); // 上次残留的图会改变生成模式（文生变图生）
      return JSON.stringify({ cost, summary });
    },

    // 打开图片选择框（target=frame 时是第 slot 格：0 首帧 1 尾帧；target=ingredient 是「添加素材」），
    // 触发「上传」但拦下系统文件对话框，返回隐藏文件输入框的选择器，交给浏览器通道 upload。
    async openUpload({ target, slot = 0 }) {
      let pane = null;
      for (let attempt = 0; attempt < 3 && !pane; attempt++) {
        await closeAllOverlays(); // 有别的弹窗开着时，点按钮只会先把那个弹窗关掉
        uploadOpener(target, slot).click();
        for (let i = 0; i < 25 && !pane; i++) { await sleep(200); pane = pickerPane(); }
      }
      if (!pane) throw new Error('图片选择框没打开');
      document.querySelectorAll(`[${UPLOAD_MARK}]`).forEach(e => e.removeAttribute(UPLOAD_MARK));
      const origClick = HTMLInputElement.prototype.click;
      let input = null;
      HTMLInputElement.prototype.click = function () {
        if (this.type === 'file') { input = this; return; }
        return origClick.call(this);
      };
      try {
        findButton(pane, /(^|\s)upload(\s|$)/).click();
        for (let i = 0; i < 10 && !input; i++) await sleep(200);
      } finally {
        HTMLInputElement.prototype.click = origClick;
      }
      if (!input) throw new Error('没找到上传用的文件输入框');
      input.setAttribute(UPLOAD_MARK, '1');
      return JSON.stringify({ selector: `input[type=file][${UPLOAD_MARK}]` });
    },

    // 文件塞进输入框后：处理使用权确认 → 在列表里按「唯一文件名」找到这张图并点选 → 必要时「添加到提示」
    // → 确认输入框里放的就是它。返回它的 mediaId（从缩略图地址里取），供提交后核对。
    // 注意：选择框会保留上一次选中的旧图，直接点「添加到提示」会加错图，所以必须按文件名点选。
    async finishUpload({ target, slot = 0, agreeRights, fileName }) {
      let mediaId = null;
      for (let i = 0; i < 180; i++) {
        const agree = openPanes().map(p => findButton(p, /^(我同意|I agree|Agree)$/i)).find(Boolean);
        if (agree) {
          if (!agreeRights) throw new Error('RIGHTS_CONFIRM_REQUIRED');
          agree.click();
          await sleep(800);
          continue;
        }
        const pane = pickerPane();
        if (!pane) {
          if (!mediaId) throw new Error('图片选择框提前关闭了');
          if (placedWith(target, slot, mediaId)) return JSON.stringify({ mediaId });
          await sleep(500);
          continue;
        }
        const opt = [...pane.querySelectorAll('button.asset-item[role=option]')]
          .find(b => b.innerText.split('\n').map(s => s.trim()).includes(fileName));
        const src = opt && (opt.querySelector('img') || {}).src;
        const m = src && src.match(/\/image\/([0-9a-f-]{36})/);
        if (m) {
          mediaId = m[1];
          if (opt.getAttribute('aria-selected') !== 'true') {
            opt.click();
          } else {
            const add = findButton(pane, /添加到提示|Add to prompt/i);
            if (add && !add.disabled) add.click();
          }
        }
        await sleep(1000);
      }
      throw new Error(`${fileName} 上传超时（mediaId ${mediaId}）`);
    },

    async closeOverlays() {
      await closeAllOverlays();
      return JSON.stringify({ open: openPanes().length });
    },

    // 「开始生成」按钮的中心坐标：出图模式只认真实点击（isTrusted），由浏览器通道发真实鼠标事件
    async submitPoint() {
      const btn = submitButton();
      if (!btn) throw new Error('找不到「开始生成」按钮');
      if (btn.disabled) throw new Error('「开始生成」不可点：提示词没填进去');
      btn.scrollIntoView({ block: 'nearest' });
      const r = btn.getBoundingClientRect();
      return JSON.stringify({ x: Math.round(r.x + r.width / 2), y: Math.round(r.y + r.height / 2) });
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
