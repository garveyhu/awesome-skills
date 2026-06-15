# 沉淀报告 · style-vault 自指沉淀

日期：2026-04-27
模式：create
起点：from-project（$PROJECT = /Users/links/Coding/Archer/style-vault · 即 vault 自身）
档位：Tier 2 · 基础级（目标 12–18 · 实际 18 条）
作者：links

## 涉及条目（18 条）

| 操作 | 类型 | ID | 名称 |
|---|---|---|---|
| 新增 | token | tokens/palettes/style-vault/slate-cyan-cool | Slate × Cyan Cool |
| 新增 | token | tokens/typography/pairs/style-vault/inter-editorial-display | Inter Editorial Display |
| 新增 | token | tokens/gradient/style-vault/cool-blob-decor | 冷感漂浮气泡装饰 |
| 新增 | token | tokens/motion/style-vault/editorial-flow | Editorial Flow Motion |
| 新增 | component | components/buttons/style-vault/dark-pill-cta | 深色胶囊主 CTA |
| 新增 | component | components/buttons/style-vault/ghost-bordered-cta | 描边幽灵 CTA |
| 新增 | component | components/tags-badges/style-vault/cyan-dot-meta-pill | Cyan Dot Meta Pill |
| 新增 | component | components/toggles/style-vault/editorial-underline-tab | 编辑式 Tab 下划线 |
| 新增 | block | blocks/marketing/style-vault/cool-blob-hero | 冷感漂浮 Hero |
| 新增 | block | blocks/display/style-vault/preview-thumb-card | 虚拟视口预览缩略卡 |
| 新增 | block | blocks/display/style-vault/floating-cover-row | 浮起作品照行卡 |
| 新增 | block | blocks/layout/style-vault/browser-chrome-frame | 浏览器 Chrome 预览框 |
| 新增 | block | blocks/nav/style-vault/sticky-platform-topbar | Sticky 平台切换顶栏 |
| 新增 | page | pages/landing/style-vault/editorial-cool-landing | 编辑感冷调落地页 |
| 新增 | page | pages/detail/style-vault/sticky-toc-product | Sticky TOC 产品详情页 |
| 新增 | page | pages/list-table/style-vault/category-row-browse | 类目行浏览页 |
| 新增 | style | styles/portfolio-studio/style-vault-cool-editorial | 冷感 Editorial 设计目录站 |
| 新增 | product | products/style-vault | Style Vault · 风格库 |

## 元信息来源

- AI 自动填（用户授权 Y 模式）：全部 18 条
- 用户手改：无

## taxonomy 字典改动

新增 `category.design`（zh "设计" · dot `#6366f1` · order 6）
`products/style-vault.category` = `design`

## 沿途修复（小错记录）

1. **YAML # 注释问题**：style README 的 `description: #fafafa 浅底...` 被 YAML 当作注释。改成 `description: "浅底 #fafafa + ..."` 双引号包裹后通过。
2. **preview tsx import 路径深度**：批量误用 `'../../../../_layout'` 而下层条目（buttons/tags-badges/toggles/blocks/pages/gradient/motion）应该是 `'../../../_layout'`，styles 应是 `'../../_layout'`。批量 sed 修。

均属"一次小错"，未触发教训回写。

## 验证

- ✅ `yarn sync` → 74 items（56 + 18），无报错
- ✅ `yarn vite build` → 通过（仅有同款 INEFFECTIVE_DYNAMIC_IMPORT warning，与 acme/skillhub 一致，pre-existing）

## Commit

- 网站仓：`dd35938` · `feat(preview): add style-vault self-sediment preview (17 tsx)`
- skill 仓：（本次报告落盘后聚合 commit）
- **均未 push**

## 下一步

1. `cd /Users/links/Coding/Archer/style-vault/frontend && yarn dev`
2. 浏览：
   - `/products` → 看产品列表新条目（设计类目 indigo dot）
   - `/products/style-vault` → 看产品详情完整的 17 条聚合
   - `/browse` → 看每类一行里都加了 style-vault 系列条目
   - `/preview/blocks/marketing/style-vault/cool-blob-hero` → 直接看 hero 完整效果（双 blob 漂浮 + fade-up cascade）
   - `/preview/tokens/gradient/style-vault/cool-blob-decor` → 单看气泡装饰
3. OK 后 `git push` 两仓
4. 发现问题 `git reset --soft HEAD~1` 回到工作区

## 关键观察

这是一次"自指沉淀"——vault 网站自己的设计语言被沉淀回 vault 数据库。技术上 VAULT_OK 路径与 PROJECT 路径相同，但 skill 仓与 vault 仓本就是两个独立 git repo（`~/.agents/skills/` vs `/Users/links/Coding/Archer/style-vault/`），双仓 commit 模式无差。

唯一值得提的一点：因为是自己沉淀自己，preview tsx 的"真实组件"和"沉淀条目所描述的真实页面"几乎可以视觉直接对照——给了一次很好的"沉淀准确度"自检机会。

---
*由 style-vault-sediment skill 生成 · 来源：from-project（自指）*
