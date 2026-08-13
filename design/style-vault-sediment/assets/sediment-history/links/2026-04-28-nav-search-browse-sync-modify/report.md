# 沉淀报告 · 同步 nav / search / browse 三类变更

日期：2026-04-28
模式：modify（多条目联动）
起点：用户在编辑会话中完成网站代码后要求同步
作者：links

## 改了什么

本次沉淀同步 6 条 skill 条目 + 3 处 preview tsx + 1 处 registry.json（sync 输出）。

### A · `blocks/nav/style-vault/sticky-platform-topbar.md`
- 描述追加"路径激活下划线 nav"
- "三段布局"小节里改写主导航描述（复用 `sv-underline-tab` 13px + `data-on` 跟随 pathname）
- **新增章节"主导航激活态"**：解释 `data-on` pathname 匹配规则、永远只一个激活、`pt-2.5` 对称 padding 让 `items-center` 容器视觉居中
- 核心代码骨架：`<Link>` 改成带 `sv-underline-tab pt-2.5` + `data-on={pathname...}`
- 适配指南补"`pt-2.5` 是必填项"

### B · `components/toggles/style-vault/editorial-underline-tab.md`
- 用法档位补充：13px 小档新增 TopBar 主导航场景；16px 大档加上"总览"
- **新增小节"`items-center` 容器对称居中"**：解释 `pt-2.5` / `pt-3.5` 抵消自带 padding-bottom

### C · `blocks/search/style-vault/cmd-k-search-panel.md`
- 头部 quote 改写：主动关闭 = 清状态新会话；点结果跳转 = 跨导航保留
- "触发模式 (singleton)"代码块：补充 `storedQ/storedType/storedPlatform/pendingReopen` module-level state；补 `closeForNavigation` 方法
- **新增章节"跨导航持久化（连续搜索的关键）"**：三件事 + 行为矩阵
- "实现要点 openItem"：用 `searchPanel.closeForNavigation()` 替代 `onClose()`
- 反模式补一条：不要在 `openItem` 里直接调 `close()`

### D · `pages/list-table/style-vault/category-row-browse/README.md`
- "Sticky 双层导航"：5 tab 改 6 tab（+ 总览），永远有锚点；fallback `'all'` 描述
- **新增章节"二级类别页（/browse/:type）的懒加载"**：完整 IO sentinel 代码 + 设计动机 + 为什么不用 `content-visibility: auto`
- 反模式删掉"不要 BrowsePage 总览也激活某个 tab"，改成"必须激活总览，不留死角"；补两条二级页相关反模式

### E · `pages/dashboard/style-vault/profile-collections/README.md`
- "Collections Grid"加 `FavGrid` 子组件代码 + `cacheKey: profile:fav:${type}` 跨 tab 保留进度
- 说明：收藏数较少时不触发，体验和原来全量渲染一致

### F · `blocks/display/style-vault/preview-thumb-card.md`
- 核心代码骨架的预览容器加 `inert` 属性
- **新增章节"防焦点劫持"**：解释 autoFocus 导致 scroll-into-view → 整页跳的机制；说明独立 preview 路由不在 inert 树里所以 autoFocus 还能用
- 适配指南 + 反模式补一条：禁用 `tabIndex={-1}` 替代 `inert`

### Preview tsx 同步

- `frontend/src/preview/blocks/nav/style-vault/sticky-platform-topbar.tsx`
  - 抽出 `NavTab` 组件，演示"浏览"激活下划线 + 对称 padding
- `frontend/src/preview/pages/list-table/style-vault/category-row-browse.tsx`
  - `TABS` 数组前面加"总览"
  - 默认 active "总览"
- `frontend/src/preview/blocks/display/style-vault/preview-thumb-card.tsx`
  - 预览容器加 `aria-hidden inert`

### registry.json 同步

`yarn sync` 跑完，132 条 items 同步到 `frontend/src/data/registry.json`（taxonomy 也复制一份）。

## Commit

- skill 仓：将在 `Co-Authored-By` 之前 commit · message `refactor(style-vault): sync nav/search/browse changes`
- 网站仓：将一并 commit · message `refactor(nav,search,browse): polish active state, search persistence, lazy load`
- **均未 push**

## 下一步

1. `cd ~/Coding/Archer/style-vault/frontend && yarn dev` 实际跑一下：
   - `/browse` 验证「总览」高亮、`/browse/style` 切换激活、连续懒加载稳定
   - `⌘K` 搜 → 点结果 → 浏览器后退 → 面板带原 query 复活
   - 收藏 tab 切换间翻页位置保留
2. OK 后 `git push`（双仓）
3. 发现问题 `git reset --soft HEAD~1` 回到工作区

---
*由 style-vault-sediment skill 生成 · 模式：modify*
