---
id: tokens/layout/auto-fit-fluid
type: token
name: 弹性自适应栅格
description: auto-fit + minmax(min, 1fr) · 永远填行 · 卡宽随数据量与容器宽度浮动
platforms: [web]
theme: both
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses: []
preview: /preview/tokens/layout/auto-fit-fluid
---

# Auto-Fit Fluid

> "弹性填行"栅格策略。`grid-template-columns: repeat(auto-fit, minmax(MIN, 1fr))`——卡片宽度在 `MIN` 下限和容器宽度 `1fr` 之间自动伸缩，**永远无右侧留白**。

## 适用场景

- **全量列表页**：数据量不确定，希望总是填满
- **搜索结果页**：结果数会变动
- **浏览 / 分类 tab 下的长列表**
- 任何"**展示全部数据**"的场景

## 不适用

- "只展一行"的场景 → 用 [fixed-cols-row](./fixed-cols-row.md)
- 需要卡宽在同一屏下恒定（品牌一致性）的预览场景
- 卡片内需要固定 aspect ratio 或精确像素尺寸的场景

## 行为

### 列数公式

```
cols = floor((container_width + gap) / (min_card_width + gap))
```

### 数据量影响（auto-fit 特性）

- **数据量 ≥ cols**：网格有 cols 列，每列等宽 = `(container - (cols-1)*gap) / cols`
- **数据量 < cols**：多余空列**折叠为 0 宽**，已有卡片拉伸分享剩余空间 → **卡片变宽**
- 对比：`auto-fill` 会保留空列，不折叠 → 右侧会留白

## 核心代码

```tsx
<div
  className="grid gap-4"
  style={{
    gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
  }}
>
  {items.map((item) => <Card key={item.id} item={item} />)}
</div>
```

## 参数调优

### `minmax(X, 1fr)` 里的 X 选取

- **X = 卡片最小可读宽度**（内容能正常展示不挤压的下限）
- 推荐值：
  - 文字/元信息卡：`240-280px`
  - 带预览图卡：`280-320px`
  - 大块信息卡（含标题 + 描述 + 标签 + 图）：`320-380px`
- **太小**：断点分得太细，窄屏下一行塞太多，内容挤压
- **太大**：断点粗，宽屏下列数少、每卡过宽

### gap 选取

- 桌面网格：`16-24px`（Tailwind `gap-4 / gap-5 / gap-6`）
- 移动：`12-16px`

### 防止"少量数据过度拉宽"

当数据只有 1-3 条时，auto-fit 会让每卡拉得很宽（吃掉整个容器）。解法：

```tsx
<div
  className="grid gap-4 mx-auto"
  style={{
    gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
    // 容器最大宽度 = N * 最大卡宽 + (N-1) * gap，N = 期望的最多列数
    maxWidth: 'calc(380px * 5 + 1rem * 4)',  // 最多 5 列 × 380px
  }}
>
  {items.map(...)}
</div>
```

`maxWidth` 封顶后，容器本身不会无限拉宽，少量数据时卡片也不会过度拉宽。

## 关键要点

1. **`auto-fit` 而不是 `auto-fill`**——前者折叠空列消除留白；后者保留空列会留白
2. **`minmax(X, 1fr)` 的 1fr 是必须的**——若用 `minmax(X, X)` 变成固定宽，数据量少时右侧会留白
3. **不用 JS**——纯 CSS 实现，比 useCols 方案简单
4. **响应屏宽是"阶梯式"**——每过一个 X 宽度就多/少一列，而不是平滑过渡

## 反模式

- ❌ 用 `repeat(auto-fill, minmax(X, MAX))`（MAX 是硬 px 上限）——MAX 存在就会导致右侧留白（本仓的 `BrowseCategoryPage` 历史 bug：`minmax(300px, 400px)` 在 Mac 屏宽下留白 80-120px）
- ❌ 对"一行展示"场景用 auto-fit——数据量 ≥ cols 时会换行，破坏"一行"语义
- ❌ 不给 maxWidth 封顶——少量数据时卡片拉得极宽破坏阅读
- ❌ 用 `1fr` 做 min（`minmax(1fr, 1fr)`）——等价于 `1fr`，失去 min 下限保护，窄屏卡片会被压到 100px 以下

## 对照：auto-fit vs auto-fill

| | auto-fit | auto-fill |
|---|---|---|
| 数据少时 | 空列折叠，现有卡片拉宽 | 空列保留，右侧留白 |
| 数据多时 | 新增行 | 新增行 |
| 想消除右侧留白 | ✅ | ❌ |
| 想保持卡宽稳定 | ❌（少数据时变宽）| ✅ |

**本 token 选 auto-fit**——核心诉求是"消除右侧留白"。

## 命名出处

"弹性填行"——Flex 的精神用在 Grid 上：有多少容器宽就填多少，不留白、不硬截断。
