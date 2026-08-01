// 解析 Playwright —— 按顺序找几个常见位置，都没有就给出可执行的补救提示。
// 覆盖顺序：PDFCRAFT_PLAYWRIGHT 环境变量 > 当前项目 > 已知本机项目 > 全局 npm root
import { createRequire } from 'node:module';
import { existsSync } from 'node:fs';
import { execSync } from 'node:child_process';
import path from 'node:path';

const CANDIDATES = [
  process.env.PDFCRAFT_PLAYWRIGHT,
  process.cwd(),
  // 本机已装浏览器的项目，作为兜底
  '/Users/links/Coding/Archer/MediaStudio/frontend/app',
].filter(Boolean);

function tryLoad(base) {
  for (const pkg of ['playwright', '@playwright/test']) {
    try {
      const req = createRequire(path.join(base, 'package.json'));
      const mod = req(pkg);
      if (mod?.chromium) return mod.chromium;
    } catch {
      /* 继续找下一个 */
    }
  }
  return null;
}

export function resolveChromium() {
  for (const base of CANDIDATES) {
    if (!existsSync(path.join(base, 'package.json')) && base !== process.cwd()) continue;
    const c = tryLoad(base);
    if (c) return c;
  }
  // 全局安装兜底
  try {
    const root = execSync('npm root -g', { encoding: 'utf8' }).trim();
    const c = tryLoad(path.dirname(root));
    if (c) return c;
  } catch {
    /* ignore */
  }

  console.error(`
找不到 Playwright。任选一种解决：

  1. 在当前项目安装：
       npm i -D playwright && npx playwright install chromium

  2. 指向一份已装好的：
       export PDFCRAFT_PLAYWRIGHT=/path/to/project-with-playwright
`);
  process.exit(1);
}
