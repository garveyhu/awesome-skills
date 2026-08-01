// 排版自检 —— 查的全是真实撞过的坑，不是理论上的问题。
//   node lint.mjs <input.html>
//
// 退出码：0 = 干净或仅提示；1 = 有 ERROR
import { readFileSync } from 'node:fs';
import path from 'node:path';

const src = process.argv[2];
if (!src) {
  console.error('用法: node lint.mjs <input.html>');
  process.exit(1);
}
const file = path.resolve(src);
const html = readFileSync(file, 'utf8');
const lines = html.split('\n');

const issues = [];
const add = (level, msg, line = null, hint = '') =>
  issues.push({ level, msg, line, hint });

// ── 1. 中文正文里的英文直引号 ─────────────────────────────
// 只看引号内含中文的成对直引号；HTML 属性值是纯 ASCII，不会误报
const straightQuote = /"[^"<>]*[一-鿿][^"<>]*"/g;
lines.forEach((l, i) => {
  if (straightQuote.test(l)) {
    add('ERROR', '中文正文里用了英文直引号 "', i + 1, '中文排版应为 “ ”');
  }
  straightQuote.lastIndex = 0;
});

// ── 2. 弯引号配对 ────────────────────────────────────────
const openQ = (html.match(/“/g) || []).length;
const closeQ = (html.match(/”/g) || []).length;
if (openQ !== closeQ) {
  add('ERROR', `弯引号数量不配对：“ ×${openQ}  ” ×${closeQ}`, null, '批量替换时最容易错位');
}
lines.forEach((l, i) => {
  const o = (l.match(/“/g) || []).length;
  const c = (l.match(/”/g) || []).length;
  if (o !== c && (o || c)) add('WARN', `本行引号不配对（“×${o} ”×${c}）`, i + 1);
});

// ── 3. justify 用在窄容器（最阴的坑）────────────────────
// 表格/单元格若继承两端对齐，一行后跟不可断开的长 token 时前半行会被拉满
const hasGlobalJustify = /body\s*{[^}]*text-align:\s*justify/s.test(html);
const tableOptsOut = /table\s*{[^}]*text-align:\s*(left|start)/s.test(html);
if (hasGlobalJustify && !tableOptsOut) {
  add(
    'ERROR',
    'body 设了 text-align: justify，但 table 没有改回左对齐',
    null,
    '窄单元格 + 不可断开 token（代码名/英文词）会让字距爆散。加 table { text-align: left; }',
  );
}

// ── 4. 表格跨页 ──────────────────────────────────────────
if (/<table/i.test(html) && !/table\s*{[^}]*page-break-inside:\s*avoid/s.test(html)) {
  add('WARN', '表格未设 page-break-inside: avoid', null, '表格会被撕成两页');
}

// ── 5. 标题孤行 ──────────────────────────────────────────
const headingRules = /h[1-4][^{]*{[^}]*page-break-after:\s*avoid/s.test(html);
if (/<h[23]/i.test(html) && !headingRules) {
  add('WARN', '标题未设 page-break-after: avoid', null, '标题可能孤零零落在页尾');
}

// ── 6. 网络字体 ─────────────────────────────────────────
const remoteFont =
  /@import\s+url\(['"]?https?:/i.test(html) ||
  /<link[^>]+href=["']https?:\/\/[^"']*fonts/i.test(html) ||
  /src:\s*url\(['"]?https?:/i.test(html);
if (remoteFont) {
  add('ERROR', '引用了网络字体', null, '离线渲染必失败且静默 fallback，改用系统字体');
}

// ── 7. @page 是否声明 ───────────────────────────────────
if (!/@page\s*{/.test(html)) {
  add('WARN', '没有声明 @page', null, '纸张尺寸与页边距应由 CSS 定义，配合 preferCSSPageSize');
}

// ── 8. 半角括号夹中文（排版瑕疵）────────────────────────
lines.forEach((l, i) => {
  if (/\([^)<>]*[一-鿿][^)<>]*\)/.test(l) && !/^\s*[/*]/.test(l)) {
    add('INFO', '半角括号里是中文', i + 1, '中文正文一般用全角（）');
  }
});

// ── 输出 ─────────────────────────────────────────────────
const byLevel = l => issues.filter(i => i.level === l);
const E = byLevel('ERROR'), W = byLevel('WARN'), I = byLevel('INFO');

const fmt = arr =>
  arr.forEach(i =>
    console.log(`  ${i.line ? `L${i.line}` : '  -'}  ${i.msg}${i.hint ? `\n        → ${i.hint}` : ''}`),
  );

console.log(`\n排版自检: ${path.basename(file)}`);
if (E.length) { console.log(`\n[ERROR] ${E.length} 项 —— 必须修`); fmt(E); }
if (W.length) { console.log(`\n[WARN] ${W.length} 项 —— 建议修`); fmt(W); }
if (I.length) { console.log(`\n[INFO] ${I.length} 项 —— 看情况`); fmt(I); }
if (!issues.length) console.log('  干净。');

console.log(`
脚本查不了、必须人工确认的：
  · 数字表格内部自洽（分项之和 = 合计，利润 = 收入 − 成本）—— 拿计算器验
  · 中文词有没有被容器切断
  · 封面信息完整、页码正常
  · 跑 preview.mjs 用眼睛看一遍
`);

process.exit(E.length ? 1 : 0);
