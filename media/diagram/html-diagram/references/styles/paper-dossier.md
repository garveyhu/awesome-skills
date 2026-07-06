# paper-dossier · 暖纸档案报表风

> 工程评估报告 / 代码审计 / 领域盘点的调性 · 暖纸底 + 工程网格 + 硬边面板 + 6 色语义 · 浅色长看不累、可打印

## 视觉 DNA（必须保留，不要随便改）

1. `#f6f7f2` 暖纸底 + **28px 工程网格**（双向 1px 线）+ 左上红晕 / 右上蓝晕两团径向 glow
2. **硬边直角**：面板 / 卡片 / 表格一律**无圆角**（`border-radius:0`）——只有 pill 导航、tag、owner 徽章用 `999px` 胶囊。这是本风格的骨架，圆角化会立刻变成普通 SaaS
3. Avenir Next 展示字（重字重 800–850）+ JetBrains Mono 数字/代码/路径 —— **数字全部走 mono**
4. 6 色语义编码（tier → tone），一个 tier 一种颜色，贯穿卡片色条 / 占比条 / 星盘 / 负载条 / 表格
5. 卡片左侧 **5px 实心 tone 色条**（`.domain-card::before`）作层级锚点
6. 软投影 + 半透明白底面板（`rgba(255,255,255,.74)` + `0 18px 42px` 阴影）浮在纸纹上
7. sticky 顶栏 + **胶囊 pill 导航**（active = 黑底白字胶囊 + mono 编号徽章）+ IntersectionObserver 滚动高亮
8. 多区块纵向报告：KPI 板 → 泳道图谱 → 图表（占比条 / 星盘 / 负载）→ 文件夹对照 → 可排序明细表
9. 数据驱动：所有区块由一份 `domains[]` 数组 render，改数据即改图，**不手写 DOM**
10. 纯 CSS + 原生 SVG + 原生 JS，**零 CDN、零构建**，file:// 直接打开

## 完整 Token 表

```css
:root {
  --paper: #f6f7f2;   /* 暖纸底 */
  --ink:   #111314;   /* 主墨色 */
  --muted: #69716d;   /* 弱化文字 */
  --line:  #d9ded7;   /* 分隔线 */

  /* 6 色语义（tier → tone） */
  --red:    #d43f2f;  /* 核心域 core */
  --amber:  #aa6d12;  /* 支撑域 support */
  --blue:   #155f8a;  /* 架构域 architecture */
  --violet: #6f5aa8;  /* 通用域 generic */
  --green:  #237963;  /* 集成域 integration */
  --slate:  #38454d;  /* 地域域 regional */

  --white: #fff;
  --soft:  rgba(255, 255, 255, .76);
  --shadow: 0 18px 42px rgba(25, 38, 44, .11);
  --display: "Avenir Next", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  --sans:    "Avenir Next", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  --mono:    "JetBrains Mono", "SFMono-Regular", "Cascadia Code", monospace;
}
```

`palette` 对象（JS 里 tier → hex 的映射，与上表一致）：

```js
const palette = {
  core: "#d43f2f", support: "#aa6d12", architecture: "#155f8a",
  generic: "#6f5aa8", integration: "#237963", regional: "#38454d"
};
const toneFor = (d) => {
  if (d.tier === "核心域") return palette.core;
  if (d.tier === "通用域") return palette.generic;
  if (d.tier === "集成域") return palette.integration;
  if (d.tier === "地域域") return palette.regional;
  if (d.tier === "架构域") return palette.architecture;
  return palette.support;   // 支撑域兜底
};
```

## 字体栈

- 标题 / 强调：`--display`（Avenir Next，`font-weight: 800~850`，字重要够狠才有报表的"权威感"）
- 正文：`--sans`（同 Avenir Next）
- **所有数字、代码、路径、编码、占比**：`--mono`（JetBrains Mono）—— 这是本风格"工程档案感"的一半

## 背景（暖纸 + 工程网格 + 双色晕）

```css
body {
  background:
    linear-gradient(90deg, rgba(17, 19, 20, .04) 1px, transparent 1px),
    linear-gradient(0deg,  rgba(17, 19, 20, .04) 1px, transparent 1px),
    radial-gradient(circle at 8% 10%,  rgba(212, 63, 47, .12), transparent 34rem),
    radial-gradient(circle at 90% 18%, rgba(21, 95, 138, .13), transparent 32rem),
    var(--paper);
  background-size: 28px 28px, 28px 28px, auto, auto, auto;
}
```

- 网格线用 `rgba(17,19,20,.04)`（极淡），28px 一格 —— 太深会抢内容
- 两团 glow 用页面主色（红 + 蓝）呼应 tone 语义，固定左上 / 右上，不要撒满

## 容器语言（硬边面板）

```css
.panel {
  border: 1px solid rgba(17, 19, 20, .16);
  background: rgba(255, 255, 255, .74);
  box-shadow: var(--shadow);
  /* 注意：无 border-radius —— 硬直角是本风格骨架 */
}
```

section 头统一：

```html
<div class="section-head">
  <h2>五分区架构归属</h2>
  <p>可选的一句话说明（右对齐，muted）</p>
</div>
```

## 组件库（本风格标志组件）

| 组件 | 用途 | 关键特征 |
|---|---|---|
| `.mast` + `.nav a` | sticky 顶栏 + 胶囊 pill 导航 | active = 黑胶囊白字 + mono 编号徽章 `<b>01</b>`；`::before` 伪元素做胶囊背景 |
| `.metric-board` / `.metric` | 顶部 KPI 板（6 格） | `grid-template-areas` 排 label/value/sub；value 走 mono 大字右对齐 |
| `.lanes` / `.lane` / `.domain-card` | 泳道图谱（按 root 分泳道，卡片按 tier 染色） | 卡片 `::before` 5px tone 左色条 + `.bar` 工作量条 + `.brief` mono 摘要 |
| `.share-bar` / `.share-segment` | 100% 横向堆叠占比条 | 每段 `width:pct%` + tone 底色 + `inset` 白右边线分隔；`pct>=3.2` 才显文字 |
| `.share-legend` / `.share-chip` | 占比条图例（7 列 grid） | 色块 + 名称 + mono 百分比 |
| SVG `#radial` 星盘 | 极坐标 sunburst，半径编码工作量 | `arcPath()` 画环扇 + 外移标签 + 引导线 + 中心圆；hover/click → `.selected` 详情 |
| `.owner-board` / `.owner-row` | 负责人负载条 | flex 段按 score 加权（`flex:score`）+ tone 染色 |
| `.folder-map` / `.folder` | 文件夹对照（root → 领域清单） | mono 标题 + `<li>` 编码 + 路径 |
| `table` + `th button` | 可排序明细表 | sticky 表头 + 点击列头升降排序（`data-sort-mark` 显 ↑↓）+ 斑马纹 + hover 高亮 |

### 星盘（radial sunburst）要点

- viewBox `0 0 900 720`，中心 `(450, 350)`，内半径 116，外半径 = `178 + (score/maxScore)*130`（**半径编码工作量**）
- 每个扇区 `arcPath(cx,cy,inner,outer,start,end)` 生成，`fill` 用 `toneFor(d)`
- 标签**外移到 r=338** + 引导线连回扇区，避免遮挡图形；`text-anchor` 按 `cos(mid)` 三态（start/middle/end）
- 底部独立 `.selected` 卡显示当前 hover/click 的领域详情（编码大字 + 名称 + note + path），不在图形上叠字

## 数据契约（改填只动这一段）

sample 的全部内容由一份 `domains[]` 驱动，每项字段：

```js
{
  code:"D01",              // 领域编码（mono 显示）
  id:"account",            // 英文标识
  zh:"账户",               // 中文名
  tier:"核心域",           // 决定 tone：核心域/支撑域/架构域/通用域/集成域/地域域
  root:"modules",          // 决定落哪条泳道：kernel/modules/common/platform/regional
  owner:"team-a",          // 负责人（业务域用 team-x；架构域用"全员涉及"/"全员约束"）
  path:"src/main/java/.../modules/account",
  shortPath:"modules/account",
  files:540, loc:33800, methods:4600, interfaces:150, http:340, mappers:120,
  score:2180.0,            // 工作量分（驱动色条/占比/星盘半径/负载权重）
  note:"账户、组织、门店、主数据与权限。"
}
```

外加两个映射：
- `laneMeta[]` —— 5 条泳道的 root / 标题 / 中文 / 描述（对齐后端目录）
- `columns[]` —— 明细表列定义（key / label / type: text|number）

**改填流程**：把 `domains[]` 换成你的领域数据 → tier 值套上面 6 类之一 → root 值对齐你的目录分区 → 其余渲染逻辑（`renderMetrics/renderLanes/renderWorkloadShare/renderRadial/renderOwners/...`）不用动。

## Sample 选用指引

paper-dossier 当前 1 个 sample：

### `analytics-report.html` — 多区块数据评估报告

- 信息架构：sticky 顶栏 + pill 导航 → KPI 板(6) → 五分区泳道图谱 → 全量可视化(占比条 + 星盘 + 负载) → 文件夹对照 → 可排序明细表 → footer 口径说明
- 单页长滚动，导航锚点 + IntersectionObserver 高亮当前区块
- 数据驱动：一份 `domains[]` 喂满全部 6 个区块，改数据即改图
- **适合**：代码库 / 领域盘点评估、工作量估算与分工、架构治理报告、模块审计、技术尽调、任何"一堆条目 × 多维指标 + 占比 + 排序"的分析报告
- **不适合**：节点连线的拓扑 / 依赖图（用 nebula-graph / dark-techy / schematic）；单张聚焦图（用 slate-mono-grid）；深色大屏演示（用 dark-techy）

### sample 选不到怎么办

如果内容是"一批条目 + 多维数值 + 需要占比/排序/分组"但形态不完全一样（比如只要 KPI 板 + 表格，不要星盘），取 `analytics-report.html` 作 token/组件 base，删掉用不上的区块即可 —— token、配色、硬边骨架、字体栈全部保留不动。

## 适合场景 & 不适合场景

✅ 适合：
- 工程评估 / 代码审计 / 领域盘点 / 工作量估算报告
- 需要浅色环境长时间阅读、需要打印 / A4·A3 出稿的分析文档
- 多维数据表 + 图表混排的"数据档案"
- 想要"冷静、克制、有工程权威感"而非炫技的汇报

❌ 不适合：
- 节点 - 连线的关系 / 拓扑 / 依赖图（本风格没有连线语言）
- 深色大屏 / 沉浸式演示（用 dark-techy）
- 极简单图插图（用 slate-mono-grid）
- 需要动态力导向 / 交互探索（用 nebula-graph）

## 动效与降级

- 本风格**几乎零动画**（只有导航 hover 位移 + `scroll-behavior: smooth`）—— 克制是它的性格
- `@media (prefers-reduced-motion: reduce)` 下关平滑滚动 + 关 transition
- 无 `backdrop-filter` 强依赖（仅 sticky 顶栏用一层 blur，降级为半透明底也不破相）

## CDN 依赖

**无。** 字体走系统栈（Avenir Next / PingFang SC / JetBrains Mono 本地有则用，没有走 fallback），CSS / SVG / JS 全内联，零构建、零外链、file:// 可开。
