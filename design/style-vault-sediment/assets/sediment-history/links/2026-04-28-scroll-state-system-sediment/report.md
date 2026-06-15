# 沉淀报告 · 滚动状态原语

日期：2026-04-28
模式：create（新 token + 3 条 page 联动改）
起点：用户在编辑会话中明确诉求"沉淀为设计原语"
作者：links

## 写入了什么

### 新条目 · `tokens/layout/_shared/scroll-state-system`

文档 9 个章节：
1. **4 场景决策矩阵** —— A tab 间记忆 / B click 置顶 / C POP 还原 / D 懒加载零位移 + "为什么需要双 Map"原理性解释
2. **`## Tokens` JSON** —— 9 个可调值（rootMargin / rowsPerPage / rafLockFrames / minPageSize / 钉顶帧数 / 还原帧数 / 容错 / history / overflowAnchor）配表说明
3. **核心代码 · ScrollToTop** —— 全文（含 byKey + byPath 双 Map / capture 滚动监听 / POP 优先级 / 30 帧钉顶 / 60 帧重试）
4. **核心代码 · useInfiniteList** —— 全文（含模块顶层 Map / cacheKey 切换重置 / items clamp / rAF double 锁 / sentinel callback ref）
5. **使用契约** —— 全局挂载 + 列表 hook 调用骨架 + cacheKey 命名规范表
6. **反模式** —— 8 条（混 content-visibility / 手动翻页 / 漏 overflow-anchor / POP 副作用 / 不设 cacheKey / cacheKey 撞名 / scrollRestoration 留默认 / 用在虚拟列表）
7. **沉淀历史** —— v1 手动按钮 → v2 content-visibility 弃用 → v3 IO sentinel 当前
8. **命名出处** —— "原语"含义引申（约定 + 行为契约）

### Preview tsx

`frontend/src/preview/tokens/layout/_shared/scroll-state-system.tsx`：
- 2x2 grid 4 场景卡 · 每场景含 before/after 视口示意 + 三行 meta
- 底部 Glue 章节：App 顶层挂载 + 列表 hook 调用骨架代码块

### 联动 3 条 page

| id | uses 加 | 正文改 |
|---|---|---|
| `pages/list-table/style-vault/category-row-browse` | `tokens/layout/_shared/scroll-state-system` | "二级类别页懒加载"完整章节简化为引用 + 场景 A/C/D 映射表 |
| `pages/dashboard/style-vault/profile-collections` | 同上 | "Collections Grid"懒加载段落简化为"走 token" |
| `pages/list-table/style-vault/sticky-filter-product-list` | 同上 | 新增"滚动行为"小节，场景 B/C 映射；说明数据量小不挂懒加载 |

### registry.json

`yarn sync` 跑完，132 → **133** items（+1 新 token）。

## Commit

- skill 仓：`refactor(style-vault): sediment scroll-state-system as design primitive`
- 网站仓：`feat(preview): add scroll-state-system token preview + sync registry`
- **均未 push**

## 下一步

1. `cd frontend && yarn dev` 走一遍 `/preview/tokens/layout/_shared/scroll-state-system` 看 4 场景示意图是否清晰
2. 进 `/browse/style` 滚一段 → 切 `/browse/page` → 切回 `/browse/style` 看是否还原（场景 A）
3. `/products` 点产品 → 浏览器后退 → 看是否还原（场景 B + C）
4. OK 后 `git push`（双仓）

---
*由 style-vault-sediment skill 生成 · 模式：create · 单条 token + 联动 3 条*
