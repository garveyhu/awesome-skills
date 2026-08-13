# 素材溯源 · Chameleon

## 项目路径
- $PROJECT = ~/Coding/Archer/Chameleon/frontend（主前端）+ frontend/embed（嵌入式 widget）
- 技术栈指纹：react19 + TypeScript + Vite + **Tailwind v4（CSS-first @theme，无 tailwind.config）** + **Radix UI（shadcn 范式）** + class-variance-authority + lucide-react + @xyflow/react + recharts + @uiw/react-codemirror + react-hook-form + zod + zustand + @tanstack/react-query + react-router-dom v7
- stack tag：shadcn-radix（**注意：旧记忆里的 antd 已不存在**）

## 关键源文件（按域）
- 设计 token：src/assets/styles/index.css（@theme 默认 blue+暖白 + 全部 keyframes/工具类）、theme.css（8 primary × 4 neutral × 3 anim 切换 + NeonLoader 锥形霓虹）
- 路由：src/router/index.tsx（import.meta.glob 动态发现 src/system/*/routes.ts，26 模块）
- 原子件：src/core/components/ui/*（24）、common/*（20）、chat/*、form/*、table/*、layout/*、command/*
- 工作流画布：src/system/graphs/* + src/core/stores/workflow/*（xyflow）
- 各业务域：src/system/{dashboard,traces,call_logs,eval_jobs,kbs,datasets,playground,conversations,marketplace,agents,models,providers,settings,...}/

## 与 waveflow 的关系（本次核心判断）
Chameleon 与 vault 已有的 `waveflow`（products/waveflow，数据调度台）是**同一套暖白工程师设计系统的两个产品**——index.css 注释直写"暖白基底（waveflow 风格）"，token 值逐一相同。故采用**智能去重**：通用地基 23 条 cross-namespace ref 复用 waveflow，只为 Chameleon 独有/分叉的 AI 编排面新建 74 条 chameleon/*。

## 视觉 1:1 参照
真实 Chameleon 前端运行在 localhost:6006（验收时停在工作流画布编辑器页），对照截图核验了 node-palette / graph-node-card / neon-loader / product 总览板，结构+配色+图标逐一吻合。

## 识别的技术栈
shadcn-radix
