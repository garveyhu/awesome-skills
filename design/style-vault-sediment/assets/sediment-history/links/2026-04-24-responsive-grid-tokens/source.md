# 素材溯源 · 响应式 Grid Tokens

## 来源

style-vault 网站自身（vault 仓）的实战演化过程，不是沉淀外部项目。

## 驱动事件

1. **2026-04-24 commit `0ec6b7e`** · 用户指出 `/browse/page` 在 Mac 屏右侧留白，`/browse` 首页硬编码 `PREVIEW_COUNT = 4` 在 4K 屏浪费空间
2. 当时分析了 4 种业界方案（auto-fit+1fr / Tailwind 断点 / JS 感知 slice / container query），给 demo HTML `/tmp/responsive-grid-compare.html`
3. 用户确认 "all 4 schemes are good, better than current"
4. 落实到 vault 仓：
   - 首页用方案 C（useCols + slice）
   - 列表页用方案 A（auto-fit + 1fr）
5. 两种方案解决了各自问题，都跑了一阵子，**两者价值都沉淀下来供未来复用**——本次 sediment

## 关键源文件（vault 仓）

- `frontend/src/hooks/useCols.ts` · useCols hook 实现（commit `0ec6b7e` 首次引入）
- `frontend/src/pages/BrowsePage.tsx:33-55` · fixed-cols-row 实战使用
- `frontend/src/pages/BrowseCategoryPage.tsx:133-138` · auto-fit-fluid 实战使用

## 核心代码摘取

### useCols hook（原样）

```ts
import { useSyncExternalStore } from 'react';

const BREAKPOINTS = [
  { query: '(min-width: 1536px)', cols: 6 },
  { query: '(min-width: 1280px)', cols: 5 },
  { query: '(min-width: 1024px)', cols: 4 },
  { query: '(min-width: 768px)',  cols: 3 },
  { query: '(min-width: 640px)',  cols: 2 },
] as const;

// ... subscribe / getSnapshot / getServerSnapshot
export function useCols(): number { ... }
```

### 两种用法对照

```tsx
// 方案 C · BrowsePage 首页
const cols = useCols();
const preview = items.slice(0, cols);
<div style={{ gridTemplateColumns: `repeat(${cols}, minmax(0, 1fr))` }}>
  {preview.map(...)}
</div>

// 方案 A · BrowseCategoryPage 列表
<div style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))' }}>
  {items.map(...)}
</div>
```

## 识别的技术栈

`react-antd-tailwind`（同 vault 网站的 stack）

## 沉淀 Tier 选择

**Tier 1 · 精髓**——两条 token，因为：
- 两个策略都是独立成立的完整原语（非"辅助性"token）
- 不需要额外 token/component/block 支撑（自足）
- hook 代码（~25 行）作为 token 正文的"核心代码"段存在，不独立沉淀（用户选项 a）

## 本次 discovery 特殊性

此次沉淀**起点非传统 from-project**（不是读某个仓的源码抽象），而是 **vault 网站自身的实战经验提炼**——用户发现两种策略都好用，把它们作为可复用原语留给未来。

**教训回写**：未来 `sediment-from-project.md` 可以补一条"**起点 5 · from-实战提炼**"——不是从零造，也不是从项目照抄，而是从"**多轮使用中涌现的可复用模式**"中提炼。暂不登记，等第 2 次出现同类情况再回写。
