---
mode: create
date: 2026-04-28
author: links
scope: 新增 token + 联动 3 条 page 引用
---

# 沉淀计划 · 滚动状态原语

## 起点

用户在编辑会话中明确指出："滚动条的方案我希望变成设计原语"。
本次沉淀把 ScrollToTop + useInfiniteList 这套 SPA 滚动行为契约固化为 token。

## 落点

`tokens/layout/_shared/scroll-state-system`

- 选 `layout/_shared` bucket：和 `responsive-grid` / `fixed-cols-row` 同源（layout/_shared 已是约定的"行为型 layout 原语"位置）
- `_shared` namespace：机制和品牌无关，任何 SPA 都能直接抄

## 写入条目

### 新增（1 条）

`tokens/layout/_shared/scroll-state-system.md` —— 完整文档：
- 4 场景决策矩阵（A tab 间记忆 / B click 置顶 / C POP 还原 / D 懒加载零位移）
- `## Tokens` JSON 配置（rootMargin / rowsPerPage / rafLockFrames / 重试帧数 / overflowAnchor）
- 核心代码（ScrollToTop + useInfiniteList 全文）
- 使用契约（全局挂载 / 列表 hook / cacheKey 命名规范）
- 反模式（混 content-visibility / 漏 overflow-anchor / cacheKey 撞名 / 用在虚拟列表）
- 沉淀历史（v1 手动按钮 → v2 content-visibility 弃用 → v3 IO sentinel 当前）

### Preview tsx

`frontend/src/preview/tokens/layout/_shared/scroll-state-system.tsx` —— 4 场景对比示意：
- 每场景一张卡：badge 头 + 视口 before/after 示意 + 触发/存储/行为 三行 meta
- 底部 Glue 章节展示 App 顶层挂载 + 列表 hook 调用骨架

### 联动改（3 条 page）

| id | 改动 |
|---|---|
| `pages/list-table/style-vault/category-row-browse` | `uses:` 加 token；二级类别页"滚动行为"小节简化为引用 + 对场景 A/C/D 的映射 |
| `pages/dashboard/style-vault/profile-collections` | `uses:` 加 token；Collections Grid 段落简化为"走 token，详细见 token 条目" |
| `pages/list-table/style-vault/sticky-filter-product-list` | `uses:` 加 token；新增"滚动行为"小节，对场景 B/C 映射，注明数据量小不挂懒加载（场景 D 不适用） |

## 字典验证

- `tokens` 类型 + `layout/_shared` namespace 路径合法（precedent: responsive-grid / fixed-cols-row）
- tags 复用现有合法值：minimal/editorial · calm/confident · react-antd-tailwind
- platforms: [web]（用 history API + IO，web 限定）
- theme: both（无视觉，深浅都适用）

## 用户确认

用户回复"ok" · 整体确认 ✓
