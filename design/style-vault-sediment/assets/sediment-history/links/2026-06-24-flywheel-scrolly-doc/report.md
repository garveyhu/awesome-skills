# 沉淀报告 · 飞轮的内部 · 孟菲斯滚动叙事文档站

日期：2026-06-24
模式：create
起点：from-project（/Users/links/Documents/wiki/media-studio · 已公开 cdn.archeruuu.com/pages/media-studio/）
档位：Tier 2 · 基础级（目标 12–18 · 实际 14 条）
作者：links

## 涉及条目（14 条）

| 操作 | 类型 | ID | 名称 | 标签 |
|---|---|---|---|---|
| 新增 | token | tokens/palettes/flywheel/memphis-collision | 孟菲斯撞色板 | brutalist,maximal · playful,energetic,confident |
| 新增 | token | tokens/typography/pairs/flywheel/han-black-grotesk | 思源黑 Black × Grotesk 字体栈 | brutalist,editorial · confident,energetic |
| 新增 | token | tokens/shadow/flywheel/hard-offset-stack | 硬位移阴影体系 | brutalist · confident,playful |
| 新增 | token | tokens/motion/flywheel/reveal-pin-scroll | 进场揭示 + 钉滚动效体系 | brutalist,editorial · energetic,confident |
| 新增 | component | components/display/flywheel/hard-shadow-card | 硬阴影卡 | brutalist · confident,playful |
| 新增 | component | components/typography-atoms/flywheel/kicker-collision-mark | 等宽 kicker + 撞色高亮 mark | brutalist,editorial · confident,energetic |
| 新增 | component | components/indicators/flywheel/scroll-progress-bar | 顶部滚动进度条 | brutalist,minimal · confident |
| 新增 | block | blocks/layout/flywheel/numbered-section-shell | 序号 Section 外壳 | brutalist,editorial · confident,energetic |
| 新增 | block | blocks/nav/flywheel/toc-scroll-rail | 右侧悬浮 TOC 导航 | brutalist,minimal · confident |
| 新增 | block | blocks/marketing/flywheel/scroll-pinned-spine | 钉滚脊梁穿行交互（★signature） | brutalist,editorial · confident,energetic |
| 新增 | block | blocks/display/flywheel/layered-atlas-grid | 分层硬卡网格 | brutalist,bento · confident,playful |
| 新增 | page | pages/landing/flywheel/scrolly-explainer-doc | 滚动叙事单页文档站 | brutalist,editorial · confident,energetic,playful |
| 新增 | style | styles/marketing-brand/memphis-scrolly-doc | 孟菲斯滚动叙事文档站 | brutalist,editorial · confident,energetic,playful |
| 新增 | product | products/media-studio | media-studio | category:content · brutalist,editorial |

> **修订（同会话 · 用户验收后）**：product 改名 `flywheel-inside` → `media-studio`（id+name+preview 同步重命名）；补 `refs.pages/blocks/components/tokens` 全列表（原只 refs.style，导致详情页页面/模块/组件/原语 栏 ·0 全空）；product 封面 preview 从 stat 卡改为**整屏 hero**（min-h-screen 垂直居中 · emo 黑猫 · 孟菲斯几何 · 滚动提示），还原原站样式。

## 元信息来源
- AI 自动填（Y 授权）：全部 14 条
- 用户手填：无
- 用户拍板的判断点：style 归桶 `marketing-brand`、product 分类 `content`、namespace `flywheel`（用户回「确认」默认采纳）

## 分类决策说明
- **aesthetic=brutalist** 主轴：硬位移阴影 + 2.5px 粗黑边 + 扁平撞色 = 新粗野（neo-brutalism）；配 editorial（文档/排版主导）、maximal（撞色）、bento（网格）按条目补
- **mood=playful/energetic/confident**：鲜艳撞色 + emo IP + 超粗大字
- **stack=react-tailwind**：Vite+React+TS+Tailwind v4（无 antd）
- **style→marketing-brand**：滚动叙事 + signature moment + 品牌 hero 是 landing/营销打法，虽内容是文档
- **product→content**：产品是讲解/文档站品类
- **namespace=flywheel**：被 product 关联，按"优先绑产品"；复用靠 style 入口拉起，namespace 不限制复用

## DAG
flywheel-inside → memphis-scrolly-doc → [section-shell, toc-rail, scroll-pinned-spine, atlas-grid, hard-card, kicker-mark, progress-bar] → refs tokens[palette, typography, shadow, motion]

## 校验
- `yarn sync`：✓ synced 310 items（296 + 14），0 错误，refs/preview 路径全合法
- 14 个 preview .tsx：纯 inline 样式 · 无 framer-motion（vault 未装）· tsc 干净 · 黑猫 IP 用 inline SVG（不外链）

## Commit
- 网站仓（style-vault）：`ebdbe05` · `feat(preview): add flywheel 滚动叙事文档站 preview (14 条)`
- skill 仓（~/.agents/skills）：见本次 `feat(style-vault): add flywheel 滚动叙事文档站 (14 条…)`
- **均未 push**

## 下一步
1. `cd /Users/links/Coding/Archer/style-vault/frontend && yarn dev` 肉眼过 14 个 preview（尤其 signature 钉滚脊梁那条 + page 整页）
2. OK 后 `git push` 两仓
3. 发现 preview 差异 → 改对应 `.tsx` 重 sync；发现条目抽象错 → 改 `.md`

---
*由 style-vault-sediment skill 生成 · 来源：from-project*
