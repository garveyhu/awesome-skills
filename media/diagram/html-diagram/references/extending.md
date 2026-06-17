# 扩展手册

加新风格、加新 sample、删 sample。

## 加新风格

1. 在 `references/styles/` 加 `<new-style>.md`，参考 `dark-techy.md` 的结构：
   - 视觉 DNA（必须保留的特征清单）
   - 完整 token 表（CSS 变量）
   - 字体栈
   - 节点形状语言
   - 链路语言
   - 装饰元素
   - **图例（Legend）规范**（dark-techy 必有；其他风格视情况）
   - 卡组件库（如有）
   - 动效系统
   - **Sample 选用指引**（描述该风格下每个 sample 适合什么内容）
   - 适合 / 不适合场景
   - CDN 依赖

2. 在 `references/styles.md` 新增一节 + sample 表格。

3. 在 `assets/styles/<new-style>/samples/` 至少做 1 个 sample（覆盖该风格最自然的应用形态）。

4. sample 必须是**真实成品级别**，不要占位骨架 —— sample 同时是浏览器看的预览，丑了用户不会选这个风格。

## 加新 sample（同风格下加新形态）

某风格已有 sample，但出现新的"应用形态"（比如 dark-techy 已有 narrative-deck + interactive-link-map，想加 dashboard 形态）：

1. 在该风格下加 `assets/styles/<style>/samples/<new-form>.html`
2. 完整继承该风格的 token / 装饰 / 图例 / 动效（**不能换底色 / 换字体 / 换 token**）
3. 在 `references/styles/<style>.md` 的 "Sample 选用指引" section 加一段：sample 名 + 形态描述 + 适合什么内容
4. 在 `references/styles.md` 该风格的 Samples 表格加一行

## 删 sample

如果某 sample 长期不被用、或与另一 sample 重复度高：

1. 删 `assets/styles/<style>/samples/<obsolete>.html`
2. 同步删 `references/styles.md` 和 `references/styles/<style>.md` 的相关条目

## 命名规则

### 风格命名

- 短横线分词
- 第一段 = 主色调或情绪（dark / light / slate / cream / neon）
- 第二段 = 视觉特征（techy / mono-grid / editorial / brutalist / glassy）
- 例：`dark-techy` / `slate-mono-grid` / `cream-editorial` / `neon-brutalist`

### Sample 命名

- 短横线分词
- 描述形态/容器，不描述内容
- 例：`narrative-deck` / `interactive-link-map` / `single-figure` / `dashboard` / `poster` / `timeline-board`
- ❌ 不要：`my-sample-v2.html` / `dark-techy-narrative.html`（路径里已有风格名，无需重复）

## 视觉验证清单

新 sample 写完后过一遍：

- [ ] Chrome 100+ / Safari 16+ / Firefox 100+ 都能正常渲染
- [ ] `prefers-reduced-motion` 下所有动画停止
- [ ] `@supports not (backdrop-filter)` 下不破相
- [ ] 缩到 1280 px / 800 px 布局不裂
- [ ] file:// 协议直接打开能看（不依赖 http server）
- [ ] 单文件，可邮件附件分发
- [ ] 没有外链 JS（除 CDN 必备）
- [ ] 图例（如风格 spec 要求）齐全且分组完整

## 维护原则

- **YAGNI**：不要预先把可能形态填满。等真触发到某种新形态需求再补 sample
- **真实成品**：sample 必须漂亮，丑了 skill 系统会被低估
- **风格是顶层**：风格之间应有清晰的视觉 DNA 差异，不要做和已有风格 90% 相似的变种
- **sample 不是分类**：sample 只是该风格的不同应用实例，不要把 sample 命名当作"种类"提升到分类层
