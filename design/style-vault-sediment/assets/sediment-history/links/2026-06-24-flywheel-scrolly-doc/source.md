# 素材溯源 · 飞轮的内部 · 孟菲斯滚动叙事文档站

## 项目路径
- $PROJECT = /Users/links/Documents/wiki/media-studio
- 已公开发布：https://cdn.archeruuu.com/pages/media-studio/
- 技术栈指纹：react-tailwind（Vite + React 18 + TS strict + Tailwind v4 + framer-motion）· base 相对路径

## 关键源文件
- `src/styles/index.css`：`@theme` 冻结 token（5 色板 + 字体 + 硬阴影 + 点阵/方格纹理 + mark/card 工具类）——色板/字体/阴影 token 三条的来源
- `src/data/workflow.ts`：全站渲染单一事实源（section 数据 + NAV_SECTIONS 锚点表）
- `src/components/Section.tsx`：序号 Section 外壳 → numbered-section-shell
- `src/components/SectionNav.tsx` + `src/hooks/useScrollSpy.ts`：右侧 TOC scroll-spy → toc-scroll-rail
- `src/components/ScrollProgress.tsx`：顶部进度条 → scroll-progress-bar
- `src/sections/Pipeline.tsx`：钉滚脊梁穿行 signature → scroll-pinned-spine
- `src/sections/SkillAtlas.tsx` + `ZoneMap.tsx`：分层硬卡网格 → layered-atlas-grid
- `src/sections/Hero.tsx`：Memphis hero（大字 + emo + 几何）→ page 骨架
- `src/App.tsx`：整页编排 → scrolly-explainer-doc

## 上游事实源（品牌 token）
- media-studio 的 `1-资产库/品牌套件/tokens.dtcg.json`（v2 孟菲斯撞色脸）——本站 CSS token 由它派生

## 识别的技术栈
react-tailwind（无 antd · framer-motion 做进场/钉滚动效）

## 备注
- 这是该项目同一会话内：先建站 → 公开发布 → 再沉淀为可复用模板
- 用户诉求：下次写图文并茂讲解型文档站、不想用 docsify 时复用本风格；撞色脸可换、结构/交互范式是骨架
