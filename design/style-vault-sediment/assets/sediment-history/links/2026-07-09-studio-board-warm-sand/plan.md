# 沉淀计划 · studio-board 暖砂白玻璃工作台

日期：2026-07-09
作者：links
模式：create
起点：from-project（$PROJECT = /Users/links/Documents/obsidian/Media-Studio/studio-board）
档位：Tier 2 · 基础级（目标 12–18 · 实际 17 条）
技术栈指纹：react-tailwind + vite + css-variables（无组件库·纯自研 UI）

## 目标

把 media-studio 看板 studio-board「首页频道 board + 详情页 workstation」两屏一体的暖砂白玻璃风格，沉淀成一套可复用的最小设计系统（namespace = studio-board）。已同步进记忆宫殿 frontend-aesthetic.md 第 9 张脸「暖砂工作台」。

## 涉及条目（依赖拓扑序 · 17）

tokens（5）
1. tokens/palettes/studio-board/warm-sand-ink
2. tokens/typography/pairs/studio-board/grotesk-han-plex
3. tokens/texture/studio-board/warm-paper-grain
4. tokens/motion/studio-board/liquid-ease
5. tokens/radius/studio-board/soft-sand-scale

components（5）
6. components/display/studio-board/warm-glass-card
7. components/buttons/studio-board/ink-cta
8. components/tags-badges/studio-board/status-badge
9. components/indicators/studio-board/pipeline-status-light
10. components/toggles/studio-board/platform-pills

blocks（3）
11. blocks/nav/studio-board/pipeline-rail
12. blocks/display/studio-board/publish-hero
13. blocks/media/studio-board/work-card

pages（2）
14. pages/dashboard/studio-board/workstation-detail
15. pages/landing/studio-board/channel-board-home

style + product（2）
16. styles/content-media/warm-sand-workbench
17. products/studio-board

## 依赖关系

products/studio-board → warm-sand-workbench → [两 pages + 三 blocks + 五 components + 五 tokens]
pipeline-rail → warm-glass-card + pipeline-status-light + warm-sand-ink + liquid-ease
publish-hero → warm-sand-ink + grotesk-han-plex + soft-sand-scale
work-card → warm-sand-ink + liquid-ease
workstation-detail → warm-glass-card + pipeline-rail + publish-hero + warm-sand-ink + warm-paper-grain
channel-board-home → platform-pills + work-card + warm-sand-ink + grotesk-han-plex + warm-paper-grain
各 component → warm-sand-ink（+ 部分 motion/radius）

## 元信息填写方式

- AI 自动填（Y 模式·用户已授权）：全部 17 条
- 用户手改：无（用户「确认」整批通过）

## 与近邻区分（已写进条目正文）

- styles/warm-sand-workbench 内含「与 waveflow-warm-engineer / flywheel 区分」
- products/studio-board 内含「工具壳 vs 内容脸」定位区分

## 执行状态

☑ 用户已确认 · 写入中
