# 素材溯源 · Quiver 夜色像素工作室

## 项目路径

- $PROJECT = ~/Coding/Archer/quiver（feat/game-first 分支）
- 技术栈指纹：React 18 + TypeScript + Vite + Tauri v2 · 纯手写 CSS（无 Tailwind / 无 Antd）· DOM 等距渲染器（已从 Phaser 迁回）· SQLite 持久化

## 关键源文件（逐条溯源）

| 资产 | 主要来源 |
|---|---|
| night-studio 调色板 | `frontend/src/theme/palette.ts` + `frontend/src/styles/global.css`（`:root`） |
| sf-system-duo 字体 | `global.css` `--ui` / `--mono` / `.num` |
| pixel-steps 动效 | `global.css` keyframes（typebob/walkbob/blinkeye/sway/godray/...）+ `hooks/useLedFlicker.ts` + `hooks/useFreezeOnBlur.ts` |
| iso-grid 网格 | `office/iso.ts`（TW/TH/iso/zidx）+ `office/primitives.ts`（SceneBuilder/isoBox/poly） |
| pixel-worker-sprite | `office/Worker.tsx` + `office/workers.ts`（HOODS/shade）+ `global.css` `.worker` |
| lime-go-button | `global.css` `.b-go` / `.pbtn.go` |
| glass-chrome-button | `global.css` `.b-gh` / `.cmd` / `.ico.pause` / `.ico.play` |
| autonomy-pill-badge | `shell/Hud.tsx` + `global.css` `.hud-auto` / `.hud-auto.on` |
| iso-office-world | `office/Office.tsx` + `office/buildScene.ts` + `office/furniture.ts` + `office/rooms.ts` |
| glass-topbar-hud | `shell/Hud.tsx` + `shell/Ctrls.tsx` + `App.tsx`（`.topbar`） |
| command-palette | `shell/CommandPalette.tsx` + `shell/commandRegistry.ts` + `global.css` `.cmdk` |
| world-ambience | `shell/Atmosphere.tsx` + `global.css`（`#sky`/`#budgetTint`/`#rededge`/`#flashfx`/`#vignette`/`#grain`） |
| glass-panel-modal | `global.css` `.panel`/`.worksurf`/`.kv`/`.rev`/`.pbtn` + 各 `shell/*` 面板 |
| office-command-deck | `App.tsx`（根组件编排：stage + topbar + caption + overlays + atmosphere） |

## 设计意图来源（辅助理解，非沉淀对象）

- `docs/redesign-iso-directions.html` —— global.css 与 palette.ts 注明「忠实移植」自此文件的 `:root` 与等距实现
- `docs/art-bible-night-studio.html` / `docs/ui-design.md` —— 美术 bible + UI 北极星方向

## 识别的技术栈标签

`stack: [vanilla-css]`（React 驱动但样式是纯手写 CSS，无 Tailwind；taxonomy 中 vanilla-css 此前 count 0，本批首用）

## 并发情况

沉淀期间 style-vault 仓有另一活跃 chameleon 会话并行写入（详见 report.md「并发会话与 sync 说明」）。本次 quiver 与之零重叠（namespace 隔离），未相互覆盖。
