# 素材溯源 · studio-board 暖砂白玻璃工作台

## 项目路径

- $PROJECT = ~/Documents/obsidian/Media-Studio/studio-board
- 前端子包 = studio-board/web
- 技术栈指纹：react-tailwind + vite + css-variables（React 18 + Vite 5 + TS + Tailwind 3.4 + react-router v6·无组件库）

## 关键源文件（token 真值来源）

- `web/src/styles/tokens.css`（真值核心）
  - `:root`（首页 board 暖色系）：bg #f6f2e8 / surface #fffdf7 / text #161616 / success #12805c / focus #2557d6；圆角 8 基准；shadow-panel 0 18px 50px rgba(#161616,9%)；字体 IBM Plex Condensed / IBM Plex Sans / JetBrains Mono；ease cubic-bezier(0.2,0.8,0.2,1)
  - `:root[data-page='workstation']`（详情页暖砂白玻璃系）：bg #f0eeea / surface #fffdfa / text #2a2620 / success #5b8c5a(苔绿) / warning #c8891f(金) / risk #c25a3a(陶土) / focus #2a2620(暖近黑 CTA)；glass rgba(255,253,248,0.74) / glass-brd rgba(255,255,255,0.82) / leak rgba(255,255,255,0.95)；shadow-md/lg 暖棕基 rgba(74,54,20,·)；glass-inset inset 0 1px 0 rgba(255,255,255,0.7)；ambient 金光弥散 + grain 0.05；圆角 16 基准(7/10/12/16/20/22)；字体 Space Grotesk / PingFang SC；ease cubic-bezier(0.16,1,0.3,1)
  - `:root[data-page='workstation'][data-theme='dark']`（冷 slate 暗态）：bg #14161b / surface #1e222b / text #eceef2 / success #3fbe86 / warning #e2a850 / risk #e5686a / focus #3a4150；玻璃转不透明面·去 backdrop-filter
- `web/src/styles/base.css`（.studio-glass 玻璃卡 + body::after feTurbulence 颗粒 + 首页网格底 + studio-* keyframes/motion）
- `web/tailwind.config.js`（把 CSS 变量映射成 Tailwind theme：colors/fontFamily/borderRadius）
- 组件源：`web/src/components/ui/{Button,Badge,StatusDot,Panel}.tsx`
- 详情页源：`web/src/pages/workstation/{WorkstationPage,components/{WorkbenchShell,PipelineRail,LaneGroup,StepNode,StatusLight,PublishHero}}.tsx`
- 首页源：`web/src/pages/board/{index,TopBar,components/{WorkCard,Cover}, homes/BilibiliHome}.tsx`

## 识别的技术栈

react-tailwind（stack tag）；token 由 CSS 变量驱动、Tailwind theme 映射

## 视觉参照

- 用户提供两张截图：详情页 workstation（三栏白玻璃·管线/主台/发布备料）+ 首页频道 board（奶油网格·头像左下·作品网格）
- 频道实例 = 飞轮日记（黑猫 IP）——preview 里作代表性还原，但沉淀的是**工具壳视觉语言**（namespace=studio-board），非频道内容品牌（那是 flywheel namespace）
