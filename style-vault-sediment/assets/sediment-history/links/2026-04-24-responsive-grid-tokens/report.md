# 沉淀报告 · 响应式 Grid 双策略 Token

日期：2026-04-24
模式：create
起点：from-project（源于 style-vault 网站 BrowsePage / BrowseCategoryPage 实战演化）
档位：**Tier 1 · 精髓（2 条 · 落在 5–8 区间下限）**
作者：links

## 涉及条目（2 新增）

| 操作 | 类型 | ID | 名称 | 策略核心 |
|---|---|---|---|---|
| 新增 | token | `tokens/layout/fixed-cols-row` | 断点列数 · 一行快照栅格 | `useCols + slice(0, cols)` · 列数 = 显示数 · 卡宽同屏恒定 |
| 新增 | token | `tokens/layout/auto-fit-fluid` | 弹性自适应栅格 | `auto-fit + minmax(MIN, 1fr)` · 永远填行 · 卡宽随数据量浮动 |

## 元信息来源

- AI 自动填（Y 模式授权）：全部 2 条

## 分类决策说明

### 为什么归 `token` 而不是 `block`
- `gentle-flow` 先例：token 可以涵盖"复合模式"（CSS keyframes + framer-motion + SVG 动画并列沉淀）
- Grid 策略也是"复合模式"——hook 代码 + CSS + 使用约定 + 反模式
- `block` 是具体 UI 块（toolbar-bar），而 Grid 策略是**抽象的布局原语**——token 更贴

### 为什么独立两条而非合并
- 语义差异大：`fixed-cols-row` 核心是"稳定"（卡宽恒定），`auto-fit-fluid` 核心是"填满"（永远无留白）
- 使用场景**互斥**：一行预览 vs 全量列表
- 独立沉淀让未来 `uses` 能精准引用

### 新子桶 `tokens/layout/`
- taxonomy.json 不限制 token 的 sub-bucket（只限制 tags enum），直接建目录即可
- 未来可扩展：`tokens/layout/sticky-header` · `tokens/layout/container-query` 等

## 关键沉淀内容

### `fixed-cols-row`
- 完整 `useCols` hook 代码（React 18 `useSyncExternalStore`）
- Tailwind 断点映射表（base/sm/md/lg/xl/2xl → 1/2/3/4/5/6）
- 用 inline `gridTemplateColumns` 避 Tailwind JIT purge
- 4 条反模式 + 2 个坑（JIT safelist / Context 单例）

### `auto-fit-fluid`
- 纯 CSS 实现（零 JS）
- `auto-fit` vs `auto-fill` 对照表
- 参数调优：minmax 的 X 取值范围（240-380 by 内容类型）
- **少量数据过度拉宽**的反模式 + 用 maxWidth 封顶的解法
- 明确说明 `BrowseCategoryPage` 历史 bug（`minmax(300px, 400px)`）属于反模式

## Commit

- skill 仓：待聚合 commit
- 网站仓：待聚合 commit
- 将推送到 3 个 remote（skills × 2 + vault × 1）

## 下一步

1. `cd ~/Coding/Archer/style-vault/frontend && yarn dev`，访问 `/preview/tokens/layout/fixed-cols-row` 和 `/preview/tokens/layout/auto-fit-fluid` 肉眼过
2. `fixed-cols-row` preview · 拖窗口看断点切换，cols 实时变化
3. `auto-fit-fluid` preview · 切数据量 1/2/3/4/8/16 看卡宽浮动

## 未来补沉淀方向（本次不做）

- Tier 3 全量化时可补：`tokens/layout/container-query` · `tokens/layout/sticky-stack` · `tokens/layout/split-pane` 等常见布局原语
- `useCols` 可独立为 hook 沉淀进 `components/?/use-cols`——但 skillhub 的 hooks 语义不清，本次选 a 选项把 hook 嵌入 token 正文

---
*由 style-vault-sediment skill 生成 · 档位：Tier 1 · 来源：from-project*
