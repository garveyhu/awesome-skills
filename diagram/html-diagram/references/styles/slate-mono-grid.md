# slate-mono-grid · 深灰极简单图

> 参考 [Cocoon-AI / architecture-diagram-generator](https://github.com/Cocoon-AI/architecture-diagram-generator)。
> JetBrains Mono 字体 + 40px 网格 + 6 色语义编码 · 文档配图调性。

## 视觉 DNA（必须保留）

1. `#020617` 深灰底 + 40px 网格图案（贯穿全页）
2. **JetBrains Mono** 全文（含中文回退）—— 强烈"工程化"调性
3. 6 色语义编码（每色对应一类组件，**严格一对一**）
4. SVG 主图占绝对主体（~70% 视口面积），DOM 卡片只做摘要
5. 视觉层级极简：标题 + 主图 + 3 张摘要卡 + 元信息脚注
6. 节点圆角不大（4–8px）、阴影克制，不用玻璃毛
7. 箭头 + 标签清晰可读，不依赖动画

## 完整 Token 表

```css
:root {
  --bg-base:      #020617;
  --bg-grid:      rgba(148, 163, 184, 0.06);  /* 网格线 */
  --bg-card:      rgba(15, 23, 42, 0.6);
  --border:       rgba(148, 163, 184, 0.15);
  --border-soft:  rgba(148, 163, 184, 0.08);

  /* 6 色语义编码（严格对应组件类型） */
  --c-frontend:   #06b6d4;   /* cyan · 前端组件 */
  --c-backend:    #10b981;   /* emerald · 后端服务 */
  --c-database:   #8b5cf6;   /* violet · 数据库 */
  --c-cloud:      #f59e0b;   /* amber · 云服务 */
  --c-security:   #f43f5e;   /* rose · 安全组件 */
  --c-external:   #94a3b8;   /* slate · 外部系统/客户端 */

  /* 文字 */
  --text-1:       #e2e8f0;   /* slate-200 */
  --text-2:       #94a3b8;   /* slate-400 */
  --text-3:       #64748b;   /* slate-500 */

  /* 状态 */
  --status-ok:    #10b981;
  --status-warn:  #f59e0b;
  --status-err:   #f43f5e;
}
```

## 字体栈

```css
font-family: "JetBrains Mono", ui-monospace, SFMono-Regular, "Cascadia Code",
             "PingFang SC", monospace;
```

通过 Google Fonts 引入：

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
```

## 6 色语义编码（核心规则）

每个组件**只能**属于以下 6 类之一，颜色严格对应。新建图前先做"组件分类"映射：

| 组件类型 | CSS 变量 | 颜色 | 典型组件 |
|---|---|---|---|
| 前端 | `--c-frontend` | `#06b6d4` cyan | Web App、SPA、Mobile UI、CDN edge |
| 后端 | `--c-backend` | `#10b981` emerald | API server、microservice、worker、Lambda |
| 数据 | `--c-database` | `#8b5cf6` violet | Postgres、MongoDB、Redis、S3 bucket |
| 云服务 | `--c-cloud` | `#f59e0b` amber | AWS API Gateway、SQS、EventBridge、K8s |
| 安全 | `--c-security` | `#f43f5e` rose | Auth、IAM、WAF、KMS |
| 外部 | `--c-external` | `#94a3b8` slate | 第三方 API、用户、客户端、SaaS provider |

如果某组件实在不属于以上 6 类（罕见），用 `--c-external` 兜底。

## 节点形状语言

不像 dark-techy 多 type，slate-mono-grid 节点形状统一、靠**色彩 + 标签**区分：

```css
.node {
  fill: var(--bg-card);
  stroke: var(--c-backend);          /* 按组件类型替换 */
  stroke-width: 1.5;
  rx: 6;                             /* 圆角小 */
}
.node-label {
  font-family: "JetBrains Mono", monospace;
  font-size: 13px;
  fill: var(--text-1);
  font-weight: 500;
}
.node-sublabel {
  font-size: 10px;
  fill: var(--text-2);
  letter-spacing: 0.5px;
  text-transform: uppercase;
}
```

节点尺寸标准：宽 140–180px、高 56–72px。同图内尺寸保持一致。

## 装饰元素

### 1. 全页网格底（核心）

```css
body {
  background-color: var(--bg-base);
  background-image:
    linear-gradient(var(--bg-grid) 1px, transparent 1px),
    linear-gradient(90deg, var(--bg-grid) 1px, transparent 1px);
  background-size: 40px 40px;
}
```

注意 grid 是 40px（不是 dark-techy 的 32px），更"工程图"感。

### 2. 头部

```html
<header>
  <div class="meta-tag">SYSTEM ARCHITECTURE / v1.0</div>
  <h1>主标题</h1>
  <div class="status-bar">
    <span class="status-dot status-ok"></span>
    <span>STATUS: OPERATIONAL</span>
    <span class="separator">·</span>
    <span>UPDATED 2026-05-06</span>
  </div>
</header>
```

```css
.meta-tag {
  font-size: 11px;
  color: var(--c-frontend);
  letter-spacing: 2px;
  margin-bottom: 8px;
}
h1 {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-1);
  letter-spacing: -0.5px;
}
.status-bar {
  display: flex; align-items: center; gap: 8px;
  font-size: 11px;
  color: var(--text-2);
  letter-spacing: 1px;
  margin-top: 12px;
}
.status-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--status-ok);
  box-shadow: 0 0 8px currentColor;
  animation: status-pulse 2s ease-in-out infinite;
}
```

### 3. 摘要小卡（3 张固定）

主图下方排 3 张说明卡，固定结构：

```html
<div class="summary-grid">
  <div class="summary-card">
    <div class="card-label">REQUEST FLOW</div>
    <div class="card-value">5 stages</div>
    <div class="card-desc">Client → CDN → API GW → Service → DB</div>
  </div>
  <div class="summary-card">
    <div class="card-label">COMPONENTS</div>
    <div class="card-value">12 nodes</div>
    <div class="card-desc">3 frontend · 5 backend · 4 data</div>
  </div>
  <div class="summary-card">
    <div class="card-label">LATENCY</div>
    <div class="card-value">~120ms p99</div>
    <div class="card-desc">Edge to first byte</div>
  </div>
</div>
```

```css
.summary-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.summary-card {
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 20px;
  background: var(--bg-card);
}
.card-label {
  font-size: 10px; letter-spacing: 1.5px;
  color: var(--text-3);
}
.card-value {
  font-size: 22px; font-weight: 700;
  color: var(--text-1);
  margin-top: 6px;
}
.card-desc {
  font-size: 11px;
  color: var(--text-2);
  margin-top: 8px;
}
```

### 4. 页脚（元信息）

```html
<footer>
  <div class="separator-line"></div>
  <div class="footer-meta">
    <span>GENERATED 2026-05-06</span>
    <span>·</span>
    <span>HTML-DIAGRAM / SLATE-MONO-GRID</span>
    <span>·</span>
    <span>SINGLE-FILE</span>
  </div>
</footer>
```

## 主 SVG 图规范

### viewBox

宽 1000–1100、高根据节点布局自适应（典型 600–800）。**不要响应式缩放**——保持工程图的"实尺寸"感。

```html
<svg viewBox="0 0 1100 700" width="100%" style="max-width: 1100px; display: block; margin: 0 auto;">
```

### 箭头标记

```html
<defs>
  <marker id="arrow-frontend" viewBox="0 0 10 10" refX="9" refY="5"
          markerWidth="8" markerHeight="8" orient="auto">
    <path d="M0,0 L10,5 L0,10 Z" fill="var(--c-frontend)"/>
  </marker>
  <!-- 每个色一个 marker -->
</defs>
```

### 连线

```css
.flow-line {
  stroke-width: 1.5;
  fill: none;
  stroke-dasharray: 4 4;            /* 默认虚线表示数据流 */
}
.flow-line.solid { stroke-dasharray: none; }   /* 实线表示同步调用 */
```

颜色用源端组件类型色。

### 节点分层

布局原则：**左→右**或**上→下**单向数据流，不要双向交叉。同层组件水平对齐。

## Sample 选用指引

slate-mono-grid 当前只有 1 个 sample：

### `single-figure.html` — 单图聚焦卡

- 信息架构：header (meta-tag + 主标题 + 状态栏) → 主 SVG 图 → 3 张摘要卡 → footer 元信息
- 单页短篇，节点 5–15、连线 6–18
- 静态展示，仅 status dot 脉冲一种动效
- **适合**：README 顶图、博客插图、AWS/云架构图、API 流程图、论文配图

如果上下文形态超出 single-figure 的范围（例如要做长篇方案 deck 或交互拓扑），先反问用户：

> slate-mono-grid 当前只有「单图聚焦卡」一种形态，更适合静态文档配图。你的内容更像方案论证 / 交互拓扑，要不要换 dark-techy 的 narrative-deck / interactive-link-map？

不要在 slate-mono-grid 风下硬塞长滚动 deck（会丢失该风格的"工程图"调性），除非用户明确要求该风格的 deck 形态、并接受需要现做（参照 SKILL.md 的"sample 选不到怎么办"流程）。

## 适合场景 & 不适合场景

✅ 适合：
- 技术博客插图（README、文档、文章配图）
- AWS / GCP / Azure 云架构图
- API 调用流程图、服务调用链
- 单一概念可视化（"X 是怎么工作的"）
- 论文、白皮书配图（可截图）

❌ 不适合：
- 节点 > 20 的复杂拓扑（用 dark-techy 的 interactive-link-map）
- 需要叙事 + 多 section 的方案文档（用 dark-techy 的 narrative-deck）
- 需要交互（hover 联动、抽屉、搜索）
- 演示场景（slate-mono-grid 偏静态、低动效，没有视觉冲击）

## 与 dark-techy 的差异速查

| 维度 | dark-techy | slate-mono-grid |
|---|---|---|
| 底色 | `#0b0f17` | `#020617` |
| 网格 | 32px、半透白 | 40px、半透 slate |
| 字体 | PingFang/system | JetBrains Mono 全文 |
| 颜色语义 | 5 tone × 5 type 矩阵 | 6 类 1 对 1 |
| 节点风格 | 玻璃毛 + inset 顶光 | 描边矩形 + 实色背景 |
| 动效 | 进场 + 持续 + 交互三层 | 仅 status dot 脉冲 |
| 主体 | DOM 节点为主 + SVG 连线层 | SVG 主图为主 + DOM 摘要 |
| 篇幅 | 1200–2000 行 | 400–800 行 |
