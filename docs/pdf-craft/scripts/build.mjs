// HTML → PDF
//   node build.mjs <input.html> [output.pdf] [--no-page-number] [--footer "自定义文字"]
//
// 分页尺寸与边距一律由 HTML 里的 @page 决定（preferCSSPageSize），
// 这样封面能用 @page :first { margin: 0 } 做满页出血。
import path from 'node:path';
import { existsSync } from 'node:fs';
import { resolveChromium } from './_playwright.mjs';

const args = process.argv.slice(2);
const flags = new Set(args.filter(a => a.startsWith('--')));
const positional = args.filter(a => !a.startsWith('--'));

const src = positional[0];
if (!src) {
  console.error('用法: node build.mjs <input.html> [output.pdf] [--no-page-number] [--footer "文字"]');
  process.exit(1);
}
const srcPath = path.resolve(src);
if (!existsSync(srcPath)) {
  console.error(`找不到输入文件: ${srcPath}`);
  process.exit(1);
}
const out = path.resolve(positional[1] ?? srcPath.replace(/\.html?$/i, '.pdf'));

const footerIdx = args.indexOf('--footer');
const footerText = footerIdx >= 0 ? args[footerIdx + 1] : null;
const showPageNumber = !flags.has('--no-page-number');

const chromium = resolveChromium();
const browser = await chromium.launch();
const page = await browser.newPage();

const errors = [];
page.on('pageerror', e => errors.push(String(e)));

await page.goto(`file://${srcPath}`, { waitUntil: 'networkidle' });
// 等字体解析完再截，否则首屏可能落到 fallback 字体
await page.evaluate(() => document.fonts.ready);

const footer = footerText
  ? `<div style="width:100%;padding:0 25mm;font-family:'PingFang SC',sans-serif;font-size:8pt;color:#444;display:flex;justify-content:space-between;">
       <span>${footerText}</span><span class="pageNumber"></span></div>`
  : `<div style="width:100%;padding:0 25mm;font-family:'PingFang SC',sans-serif;font-size:8pt;color:#444;text-align:center;">
       <span>— 第 </span><span class="pageNumber"></span><span> 页 —</span></div>`;

await page.pdf({
  path: out,
  printBackground: true,
  preferCSSPageSize: true,
  displayHeaderFooter: showPageNumber,
  headerTemplate: '<div></div>',
  footerTemplate: showPageNumber ? footer : '<div></div>',
});

await browser.close();

if (errors.length) {
  console.warn('页面报了 JS 错误（不影响静态排版，但值得看一眼）：');
  errors.forEach(e => console.warn('  ' + e));
}
console.log('PDF →', out);
console.log('别忘了跑 lint.mjs 和 preview.mjs 验一遍。');
