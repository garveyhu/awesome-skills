// 按打印媒体渲染并分段截图 —— PDF 本身没法直接看，用这个代替。
//   node preview.mjs <input.html> [张数=5] [--el ".selector"]
//
// --el 只截某个元素（验单个表格/图表时用，比翻整页快）
import path from 'node:path';
import { existsSync } from 'node:fs';
import { resolveChromium } from './_playwright.mjs';

const args = process.argv.slice(2);
const src = args[0];
if (!src) {
  console.error('用法: node preview.mjs <input.html> [张数] [--el ".selector"]');
  process.exit(1);
}
const srcPath = path.resolve(src);
if (!existsSync(srcPath)) {
  console.error(`找不到输入文件: ${srcPath}`);
  process.exit(1);
}

const elIdx = args.indexOf('--el');
const selector = elIdx >= 0 ? args[elIdx + 1] : null;
const shots = Number(args[1] && !args[1].startsWith('--') ? args[1] : 5);
const outDir = path.dirname(srcPath);

const A4_W = 794; // 210mm @96dpi
const chromium = resolveChromium();
const browser = await chromium.launch();
const page = await browser.newPage({
  viewport: { width: A4_W, height: 1123 },
  deviceScaleFactor: 2,
});
await page.emulateMedia({ media: 'print' });
await page.goto(`file://${srcPath}`, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);

if (selector) {
  const out = path.join(outDir, 'preview-el.png');
  await page.locator(selector).first().screenshot({ path: out });
  console.log('元素截图 →', out);
} else {
  // @page 的边距在截图里不生效，手动补上才能看到真实行宽
  await page.addStyleTag({ content: 'body > *:not(.cover){padding-left:16mm;padding-right:16mm;}' });
  const total = await page.evaluate(() => document.body.scrollHeight);
  const step = Math.ceil(total / shots);
  for (let i = 0; i < shots; i++) {
    await page.evaluate(y => window.scrollTo(0, y), i * step);
    await page.screenshot({ path: path.join(outDir, `preview-${i + 1}.png`) });
  }
  console.log(`总高 ${total}px，出图 ${shots} 张 → ${outDir}/preview-*.png`);
}

await browser.close();
console.log('用 Read 工具逐张看完后删掉：rm -f preview-*.png');
