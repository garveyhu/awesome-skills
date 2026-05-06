# dark-techy · 深色技术风

> Datadog/Grafana/Linear 调性 · 玻璃毛 + 粒子流 + 内发光 · 长时间观看不累

## 视觉 DNA（必须保留，不要随便改）

1. `#0b0f17` 深色底 + 双色径向 glow + 32px 网格底纹
2. CSS 变量驱动的完整 token 系统
3. 玻璃毛节点（`backdrop-filter: blur(8px)` + 6% 白底）
4. **inset 顶光阴影**（`box-shadow: inset 0 1px 0 rgba(255,255,255,0.06)`）—— 提质感关键
5. 节点 5 type × 5 tone 网格（`data-type` × `data-tone` 属性驱动）
6. SVG 贝塞尔连线 + glow filter + 粒子流（`animateMotion`）
7. iOS easing：`cubic-bezier(0.16, 1, 0.3, 1)` 进场、`cubic-bezier(0.32, 0.72, 0, 1)` 抽屉
8. mono 编号 section 头："01 / 现状" + 主标题 + lead
9. `prefers-reduced-motion` + `@supports not (backdrop-filter)` 完整降级
10. **Legend 左侧固定面板**（4 分组：Node tones / Link kinds / Tier / Markers，含 timeline 加 Stage palette） — dark-techy 的"工程文档"调性核心

## 完整 Token 表

```css
:root {
  /* 底层 */
  --bg-base:      #0b0f17;
  --bg-grid:      rgba(255,255,255,0.02);
  --bg-panel:     rgba(255,255,255,0.04);
  --bg-card:      rgba(255,255,255,0.06);
  --border:       rgba(255,255,255,0.08);

  /* 节点 tone（性质语义） */
  --c-primary:    #5eead4;   /* 青绿 · 核心/平台 */
  --c-accent:     #818cf8;   /* 紫蓝 · 中间件/服务 */
  --c-warn:       #fbbf24;   /* 琥珀 · 需关注 */
  --c-danger:     #fb7185;   /* 珊瑚红 · 复杂/易事故 */
  --c-mute:       #94a3b8;   /* 中性灰 · 弱化 */

  /* 链路 tone（关系语义） */
  --l-pull:       #38bdf8;   /* 蓝 · 拉取 */
  --l-push:       #fb923c;   /* 橙 · 推送/异步 */
  --l-bi:         #c084fc;   /* 紫 · 双向 */
  --l-fault:      #ef4444;   /* 红 · 故障传播 */
  --l-mute:       rgba(255,255,255,0.06);

  /* 阶段 tone（时间轴用） */
  --s-prep:       #94a3b8;
  --s-pilot:      #fb7185;
  --s-batch:      #fbbf24;
  --s-mid:        #818cf8;
  --s-final:      #5eead4;

  /* 文字层级 */
  --text-1:       rgba(255,255,255,0.96);
  --text-2:       rgba(255,255,255,0.65);
  --text-3:       rgba(255,255,255,0.4);

  /* 动画曲线 */
  --ease-out:     cubic-bezier(0.16, 1, 0.3, 1);
  --ease-ios:     cubic-bezier(0.32, 0.72, 0, 1);
}
```

## 字体栈

```css
font-family: -apple-system, "PingFang SC", "Microsoft YaHei", system-ui, sans-serif;
```

monospace 局部使用：

```css
font-family: ui-monospace, SFMono-Regular, "JetBrains Mono", monospace;
```

## 节点形状语言（5 type × 5 tone）

`data-type` 决定形状/尺寸/语义，`data-tone` 决定边框色和 dot 状态色。

| type | 尺寸 | 圆角 | 边框 | 背景 | 视觉特征 |
|---|---|---|---|---|---|
| `platform` | 320–360 × 140–150 | 16px | tone × 60% 实线 | tone × 8% 玻璃毛 | 顶部渐变发光条 + 顶光脉冲 |
| `service`  | 240 × 100 | 12px | tone × 40% 实线 | `--bg-card` | 紧凑、冷感 |
| `region`   | 178–200 × 96–120 | 12px | tone × 60% 实线 | tone × 6% | 大字号区名 |
| `table`    | 180–200 × 56–60 | 8px | tone 虚线 (dashed) | `--bg-card` | 圆柱图标可选 |
| `api`      | 160–200 × 40–44 | 999px (胶囊) | `--border` | `--bg-card` | mono 字体 |

通用质感（所有 type 公用）：

```css
.node {
  position: relative;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 14px 16px;
  backdrop-filter: blur(8px);
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.06);
  transition: transform 120ms var(--ease-out),
              border-color 120ms var(--ease-out),
              box-shadow 120ms var(--ease-out),
              opacity 180ms ease,
              filter 180ms ease;
  user-select: none;
}

.node:hover {
  transform: translateY(-2px);
  border-color: rgba(255,255,255,0.18);
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.08),
              0 8px 24px rgba(0,0,0,0.4);
}

/* tone 边框 */
.node[data-tone="primary"] { border-color: color-mix(in oklab, var(--c-primary) 60%, transparent); }
.node[data-tone="accent"]  { border-color: color-mix(in oklab, var(--c-accent)  60%, transparent); }
.node[data-tone="warn"]    { border-color: color-mix(in oklab, var(--c-warn)    60%, transparent); }
.node[data-tone="danger"]  { border-color: color-mix(in oklab, var(--c-danger)  60%, transparent); }
.node[data-tone="mute"]    { border-color: var(--border); }

/* dot 状态点 */
.node[data-tone="primary"] .dot { background: var(--c-primary); box-shadow: 0 0 8px var(--c-primary); }
.node[data-tone="accent"]  .dot { background: var(--c-accent);  box-shadow: 0 0 8px var(--c-accent); }
/* ... */
```

节点内部结构标准化为：

```html
<div class="node" data-type="service" data-tone="accent" data-id="...">
  <div class="header">
    <span class="dot"></span>
    <span class="title">标题</span>
  </div>
  <div class="subtitle">副标题（可选）</div>
  <div class="chips">
    <span class="chip">标签1</span>
    <span class="chip">标签2</span>
  </div>
  <div class="lines">
    <div class="line"><span class="k">key</span> value</div>
  </div>
</div>
```

## 链路语言（SVG）

```css
.link-path { fill: none; stroke-linecap: round;
             transition: stroke 200ms ease, opacity 200ms ease, stroke-width 200ms ease; }
.link-pull   { stroke: var(--l-pull);  stroke-width: 1.5; }
.link-push   { stroke: var(--l-push);  stroke-width: 1.5; stroke-dasharray: 6 4; }
.link-bi     { stroke: var(--l-bi);    stroke-width: 2; }
.link-fault  { stroke: var(--l-fault); stroke-width: 2.5;
               filter: drop-shadow(0 0 8px var(--l-fault)); }
.link-mute   { stroke: var(--l-mute);  stroke-width: 1; }
```

**glow filter**（必备 SVG `<defs>`）：

```html
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
  <feGaussianBlur stdDeviation="3" result="blur"/>
  <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
```

**粒子流**（核心高级感）：每条 `flow:particles` 链路上 1–3 个发光粒子：

```html
<circle r="3" fill="var(--l-pull)" filter="url(#glow)">
  <animateMotion dur="3s" repeatCount="indefinite">
    <mpath href="#path-l-xxx"/>
  </animateMotion>
</circle>
```

**形状偏好**：贝塞尔曲线（不要直线）。同层水平浅 S 形、跨层纵向平滑弧线。

## 装饰元素

### 1. 全屏底纹（body）

```css
body {
  background:
    radial-gradient(circle at 30% 20%, rgba(94,234,212,0.04), transparent 50%),
    radial-gradient(circle at 70% 80%, rgba(129,140,248,0.04), transparent 50%),
    var(--bg-base);
}
body::before {
  content: '';
  position: fixed; inset: 0;
  background-image:
    linear-gradient(var(--bg-grid) 1px, transparent 1px),
    linear-gradient(90deg, var(--bg-grid) 1px, transparent 1px);
  background-size: 32px 32px;
  pointer-events: none;
  z-index: 0;
}
```

### 2. Section 头（mono 编号）

```html
<div class="section-title">
  <span class="num">01 / 现状</span>
  <h2>三大痛点</h2>
  <span class="lead">为什么必须重做</span>
</div>
```

```css
.section-title { display: flex; align-items: baseline; gap: 12px; margin-bottom: 22px; }
.section-title .num { font-size: 12px; font-family: ui-monospace, SFMono-Regular, monospace;
                      color: var(--c-primary); letter-spacing: 1px; }
.section-title h2  { font-size: 22px; font-weight: 600; margin: 0; color: var(--text-1); }
.section-title .lead { font-size: 13px; color: var(--text-2); margin-left: 4px; }
```

### 3. 容器（panel）

```css
.panel {
  position: relative;
  background: var(--bg-panel);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 16px;
  padding: 24px; padding-top: 48px;
  backdrop-filter: blur(8px);
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
  display: flex; flex-wrap: wrap; gap: 16px;
}
.panel::before {
  content: attr(data-title);
  position: absolute; top: 16px; left: 24px;
  font-size: 14px; font-weight: 500;
  color: var(--text-2); letter-spacing: 0.5px;
}
```

### 4. Hero 主标题

```html
<header class="text-center mb-8 relative">
  <div class="text-xs tracking-widest mb-3"
       style="color: var(--c-primary); opacity: 0.7">
    <项目代号 · 副标题缩写>
  </div>
  <h1 class="text-5xl font-semibold tracking-tight"
      style="color: var(--c-primary); text-shadow: 0 0 28px rgba(94,234,212,0.35)">
    <主标题>
  </h1>
  <p class="mt-4 text-base" style="color: var(--text-2)"><副标题></p>
</header>
```

## Legend（左侧固定图例面板，dark-techy 标志元素之一）

**用途**：dark-techy 风格的拓扑/架构图必备。提供 4 类语义对照表，让阅读者快速理解节点配色 / 链路语义 / 层级关系 / 特殊标记。

**容器规范**：

```css
.legend {
  position: fixed;
  left: 16px; top: 50%;
  transform: translateY(-50%);
  width: 224px;
  background: rgba(15,19,28,0.78);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 16px 16px 14px;
  backdrop-filter: blur(16px);
  box-shadow: 0 8px 32px rgba(0,0,0,0.4);
  z-index: 50;
  font-size: 11px;
  max-height: calc(100vh - 32px);
  overflow-y: auto;
}
```

**< 1400px 自动隐藏**：`@media (max-width: 1400px) { .legend { display: none; } }`

### 标准结构（4 个分组，按顺序）

```html
<aside class="legend">
  <h4>Node tones</h4>           <!-- 1. 5 tone 色彩语义 -->
  <div class="item"><span class="swatch s-primary"></span>primary · 用途</div>
  <div class="item"><span class="swatch s-accent"></span>accent · 用途</div>
  <div class="item"><span class="swatch s-warn"></span>warn · 用途</div>
  <div class="item"><span class="swatch s-danger"></span>danger · 用途 <span class="marker-star">★</span></div>
  <div class="item"><span class="swatch s-mute"></span>mute · 用途</div>

  <h4>Link kinds</h4>           <!-- 2. 链路 kind 视觉样本 -->
  <div class="item"><span class="line-sample line-pull"></span>pull · 拉取语义</div>
  <div class="item"><span class="line-sample line-bi"></span>bi · 双向语义</div>
  <div class="item"><span class="line-sample line-push"></span>push · 推送语义</div>

  <h4>Tier (top → bottom)</h4>  <!-- 3. 层级 stack（用 ↓ 串联） -->
  <div class="tier-stack">
    <div class="tier-item t-primary">Tier 1 · 名称</div>
    <div class="tier-arrow">↓</div>
    <div class="tier-item t-accent">Tier 2 · 名称</div>
    <div class="tier-arrow">↓</div>
    <div class="tier-item t-warn">Tier 3 · 名称</div>
  </div>

  <h4>Markers</h4>              <!-- 4. 特殊标记说明（可选） -->
  <div class="item"><span class="marker-star">★</span>说明文字</div>
</aside>
```

含 timeline 的 deck，再加第 5 分组 `<h4>Stage palette</h4>`，列 5 个 stage tone 色块。

### Swatch / line-sample CSS

```css
/* 5 tone swatch */
.legend .swatch { width: 13px; height: 13px; border-radius: 3px; flex: none;
                  border: 1.5px solid rgba(255,255,255,0.12); }
.legend .swatch.s-primary { background: color-mix(in oklab, var(--c-primary) 30%, var(--bg-card)); border-color: var(--c-primary); }
.legend .swatch.s-accent  { background: color-mix(in oklab, var(--c-accent)  30%, var(--bg-card)); border-color: var(--c-accent); }
.legend .swatch.s-warn    { background: color-mix(in oklab, var(--c-warn)    30%, var(--bg-card)); border-color: var(--c-warn); }
.legend .swatch.s-danger  { background: color-mix(in oklab, var(--c-danger)  30%, var(--bg-card)); border-color: var(--c-danger); }
.legend .swatch.s-mute    { background: var(--bg-card); border-color: var(--c-mute); }

/* link-kind 线条样本 */
.legend .line-sample { width: 26px; height: 2px; flex: none; border-radius: 999px; }
.legend .line-sample.line-pull { background: var(--l-pull); }
.legend .line-sample.line-bi   { background: var(--l-bi); }
.legend .line-sample.line-push { background: repeating-linear-gradient(90deg, var(--l-push) 0 4px, transparent 4px 7px); height: 2px; }

/* 层级 stack */
.legend .tier-item { font-size: 11.5px; font-weight: 600; padding: 3px 0; letter-spacing: 0.3px; }
.legend .tier-item.t-primary { color: var(--c-primary); }
.legend .tier-item.t-accent  { color: var(--c-accent); }
.legend .tier-item.t-warn    { color: var(--c-warn); }
.legend .tier-arrow { text-align: center; font-size: 12px; color: var(--text-3); line-height: 1; margin: 2px 0; }

/* 标记说明 */
.legend .marker-star { display: inline-block; width: 13px; flex: none;
                       font-size: 13px; color: var(--c-warn);
                       text-shadow: 0 0 6px var(--c-warn); text-align: center; }
```

### 设计要点

- **图例标题统一格式**：英文 UPPERCASE 风（`Node tones / Link kinds / Tier / Markers / Stage palette`）；item 文字可中英混杂
- **tone 用途必须具体**：不要写"主色调"，要写"platform / source"等结构化语义
- **tier 颜色与对应 tone 一致**：第 1 层 `t-primary` 配青绿，第 2 层 `t-accent` 配紫蓝，第 3 层 `t-warn` 配琥珀
- **省略原则**：仅 1 个 type 的图（如 single-figure 风的 dark-techy 实例）可省略 Tier 和 Markers，但 Node tones + Link kinds 必有
- **不在中部分散**：图例永远 fixed-left，不要在 hero 下方或 section 间放。这是 dark-techy 的视觉惯性

## 卡组件库（按需选用）

narrative-deck sample 会用到，interactive-link-map 不必。

| 卡 | 用途 | 关键样式 |
|---|---|---|
| `pain-card` | 痛点卡 | danger 色调玻璃 + badge + 列表小红点 |
| `feat-card` | 能力/特性卡 | tone 顶部 icon-bar |
| `stage-card` | 时间轴阶段卡 | 顶部 marker 圆点 + 渐变 connecting 线 |
| `yagni-card` | "不做什么"卡 | 虚线边框 + 灰调 |

详细 CSS 见 sample HTML（`assets/styles/dark-techy/samples/narrative-deck.html`）。

## Sample 选用指引

dark-techy 当前有两个 sample，都是该风格的真实应用实例。AI 改填时按内容形态选最贴近的：

### `narrative-deck.html` — 长滚动叙事 deck

- 信息架构：hero → 痛点 (pain-card) → 蓝图主图 (panel + 节点 + 连线) → 能力 (feat-card) → 时间轴 (stage-card) → YAGNI (yagni-card)
- 多 section 顺序铺陈，section 头用 mono 编号（"01 / pain"）
- 主图区只有一处，含 panel 三层 + SVG 链路 + 粒子流
- 含全套卡组件 + timeline + 进场动画
- **适合**：方案论证、向上汇报、白皮书 hero、长文 deck
- **不适合**：纯拓扑图（用 interactive-link-map）

### `interactive-link-map.html` — 单屏交互拓扑

- 信息架构：topbar (含搜索) + 左侧 fixed legend + 主拓扑（panel × 3） + 右侧抽屉
- 单屏单页（不滚动）
- **核心交互**：hover 联动（muted/focused/related 三态）、点击抽屉、搜索高亮
- 节点 click 触发抽屉，抽屉显示上下游链路 + 节点详情
- **适合**：服务拓扑、依赖关系图、运维排查工具、故障演练
- **不适合**：方案叙事（用 narrative-deck）

### 选 sample 决策

```
上下文是"实体 + 关系网络"，关注节点间连接？
  └─ interactive-link-map
上下文是"方案论证 / 多章节叙事"，含痛点/蓝图/路径/边界？
  └─ narrative-deck
两者都不像？先反问用户内容形态，再选
```

## 交互行为（按 sample 启用）

| 行为 | 触发 | 视觉 | 适用 sample |
|---|---|---|---|
| Hover 联动 | mouseenter | 节点抬起 + 关联链路高亮 + 其它褪色 | interactive-link-map |
| 抽屉 | click 节点 | 480px 右侧抽屉滑入（300ms iOS 曲线） | interactive-link-map |
| 搜索 | 顶部 input | 不匹配 opacity 0.2 + blur(2px)；匹配金脉冲 | interactive-link-map |
| 故障演练 | 右键 | 节点变红 + 下游链路 fault + 抽屉显示影响 | interactive-link-map（可选） |
| 平滑滚动 | section 内锚点 | `scroll-behavior: smooth` | narrative-deck |

通用 hover muted/focused 系统：

```css
.node.muted   { opacity: 0.18; filter: saturate(0.3); }
.node.focused { border-color: rgba(255,255,255,0.6) !important; }
.node.related { border-color: rgba(255,255,255,0.35); }
.link-path.muted       { stroke: var(--l-mute); stroke-width: 1; }
.link-path.highlighted { stroke-width: 2.5; filter: drop-shadow(0 0 6px currentColor); }
```

## 动效系统

### 进场（一次性，~2.5s 一气呵成）

```
0.0s  body 淡入
0.3s  hero stagger
0.7s  panel/section 顺序淡入
1.9s  节点 stagger（30ms 错峰），用 clip-path: inset(0 100% 0 0) 擦出
2.2s  连线 stroke-dasharray 0→100% 绘出
2.7s  粒子启动
```

```css
@keyframes node-enter {
  from { opacity: 0; clip-path: inset(0 100% 0 0); }
  to   { opacity: 1; clip-path: inset(0 0 0 0); }
}
@keyframes link-draw {
  from { stroke-dashoffset: var(--len); }
  to   { stroke-dashoffset: 0; }
}
```

### 持续（页面静止时也活）

| 动效 | 频率 | 关 CSS |
|---|---|---|
| 粒子流 | 3s 周期 | `<animateMotion>` |
| 节点呼吸 | 4s 周期 | `top-bar-pulse` 关键帧 |
| 网格漂移 | 1px / 2s | `background-position` 动画 |
| dot 脉冲 | 2s 周期 | `dot-pulse` 关键帧 |

### 降级

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 1ms !important;
    transition-duration: 1ms !important;
  }
  .particle, [class*="animate"] { display: none; }
}
@supports not (backdrop-filter: blur(8px)) {
  .panel, .node, .pain-card, .feat-card, .stage-card { backdrop-filter: none; }
}
```

性能模式（手动 toggle 或自动检测 `navigator.hardwareConcurrency < 4`）：关粒子、关呼吸、关网格漂移。

## 适合场景 & 不适合场景

✅ 适合：
- 系统架构演示（向上汇报 / 客户演示 / 政务大屏）
- 服务拓扑、数据同步链路
- 长时间观看（暗色不刺眼）
- 想要"工程感 + 高级感"的内部文档 hero
- 故障可视化、运维 dashboard 草稿

❌ 不适合：
- 需要打印的图表（暗色油墨成本高）
- 想要轻量、文档插图风格的（用 slate-mono-grid）
- 需要明色环境投影演示
- 极简、紧凑、单图聚焦的场景（用 slate-mono-grid 风格）

## CDN 依赖

```html
<script src="https://cdn.tailwindcss.com"></script>
```

仅此一项。其它 CSS 全部内联。零构建链。
