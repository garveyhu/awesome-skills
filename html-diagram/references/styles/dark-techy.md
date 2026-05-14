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

**容器规范**（含默认折叠按钮 + < 1400px 自动收缩为窄条）：

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
  transition: width 240ms var(--ease-out), padding 240ms var(--ease-out);
}
.legend.collapsed { width: 36px; padding: 8px 6px; overflow: hidden; }
.legend.collapsed .legend-content { display: none; }
.legend-toggle {
  position: absolute; top: 8px; right: 8px;
  width: 22px; height: 22px;
  display: flex; align-items: center; justify-content: center;
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text-2);
  cursor: pointer;
  font-size: 11px; font-family: inherit;
  transition: background 120ms var(--ease-out);
}
.legend-toggle:hover { background: rgba(255,255,255,0.08); color: var(--text-1); }
.legend.collapsed .legend-toggle { position: static; margin: 0 auto; }
@media (max-width: 1400px) {
  .legend:not(.collapsed) { display: none; }
  .legend.collapsed { display: block; }
}
```

**配套 JS（自调用 IIFE，进 `<script>` 块开头）**：

```js
(function initLegendToggle() {
  const legend = document.getElementById('legend');
  const btn = document.getElementById('legend-toggle');
  if (!legend || !btn) return;
  try {
    if (localStorage.getItem('legend-collapsed') === '1') {
      legend.classList.add('collapsed');
      btn.textContent = '▶';
    }
  } catch (e) {}
  btn.addEventListener('click', () => {
    const collapsed = legend.classList.toggle('collapsed');
    btn.textContent = collapsed ? '▶' : '◀';
    try { localStorage.setItem('legend-collapsed', collapsed ? '1' : '0'); } catch (e) {}
  });
})();
```

### 标准结构（4 个分组，按顺序 · 默认带 toggle 按钮 + content wrapper）

```html
<aside class="legend" id="legend">
  <button class="legend-toggle" id="legend-toggle" aria-label="Toggle legend">◀</button>
  <div class="legend-content">
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
  </div><!-- /.legend-content -->
</aside>
```

含 timeline 的 deck，再加第 5 分组 `<h4>Stage palette</h4>`，列 5 个 stage tone 色块。
**注意 `Stage palette` 也要放在 `.legend-content` 内部**，跟其他 4 组并列；折叠按钮始终在外层 `.legend` 上。

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

dark-techy 当前有三个 sample，都是该风格的真实应用实例。AI 改填时按内容形态选最贴近的：

### `narrative-deck.html` — 长滚动叙事 deck

- 信息架构：hero → 痛点 (pain-card) → 蓝图主图 (panel + 节点 + 连线) → 能力 (feat-card) → 时间轴 (stage-card) → YAGNI (yagni-card)
- 多 section 顺序铺陈，section 头用 mono 编号（"01 / pain"）
- 主图区只有一处，含 panel 三层 + SVG 链路 + 粒子流
- 含全套卡组件 + timeline + 进场动画
- **适合**：方案论证、向上汇报、白皮书 hero、长文 deck
- **不适合**：纯拓扑图（用 interactive-link-map / topology-poster）

### `interactive-link-map.html` — 单屏交互拓扑

- 信息架构：topbar (含搜索) + 左侧 fixed legend + 主拓扑（panel × 3） + 右侧抽屉
- 单屏单页（不滚动）
- **核心交互**：hover 联动（muted/focused/related 三态）、点击抽屉、搜索高亮
- 节点 click 触发抽屉，抽屉显示上下游链路 + 节点详情
- **适合**：服务拓扑、依赖关系图、运维排查工具、故障演练
- **不适合**：方案叙事（用 narrative-deck）

### `topology-poster.html` — 单页 1920×1080 网络架构海报

- 信息架构：head 标题 + 多个 zone 区块（用 `<section class="zone">` 给每个网络/域划框）+ 节点 absolute 定位 + SVG 弧线连接 + 底部 channels 跨网通道说明 + 底部 LEGEND + PROJECTS & PORTS 端口总览
- 单页固定 1920×1080，`.stage` 用 `transform: scale()` 自动适应 viewport（fit 公式：`Math.min(innerWidth/1920, innerHeight/1080)`）
- 节点全部 `position:absolute` 配 inline `style="left:Xpx;top:Ypx;width:Wpx;height:Hpx"`，SVG 端点用绝对坐标对齐节点边框
- 关键组件：
  - `.zone` — 虚线 dashed border + zone-label（mono 大写 + 中文小字）作为网络/域边界
  - `.node` / `.nv` / `.featured` — 横节点 / 竖节点 / 带 ★ 角标的关键节点
  - `.db-merged` — DB 容器，顶部色带 + 内部 split 多个 half 子库
  - `.ext` — 虚线节点表示外部数据源
  - `.aura` — plate-style 多模块汇聚框
  - SVG `<path class="lk ...">` + cubic bezier + marker（`markerUnits=userSpaceOnUse` 固定大小箭头）+ `<animateMotion>` 粒子流
  - 底部 `.channels`（跨网通道 5/4+1 分组卡）+ `.bot-row` 双块（LEGEND 图例 + PROJECTS & PORTS 端口 chip flow）
  - 顶部 `.toolbar` 右上角浮动 button：暗/亮主题切换（`[data-theme]` 双套 token + localStorage）+ PNG 导出（`modern-screenshot@4.7.0`）
- **适合**：跨网/多区域系统架构图、政务/企业内网拓扑、向领导/运维 review 的对账图、A3 打印 / 大屏展示
- **不适合**：单一系统内部模块依赖（用 interactive-link-map）；方案叙事多 section（用 narrative-deck）

### 选 sample 决策

```
上下文是"多网络/多区域 + 静态拓扑展示 + 需 1920×1080 单页"？
  └─ topology-poster
上下文是"单系统内部 + 实体 + 关系网络"，关注 hover/click 交互？
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

---

## 进阶模式（基于实战沉淀）

下面这些模式不是每张图都必须用，但当你的图遇到对应场景时，**抄这套 pattern 比从头设计省 1 小时**。每条都来自真实重构（"政务婴育同步架构图 v2"）的踩坑教训。

### 1. 多 tier 分层 panel · 突出层级关系

**场景**：单 panel 内有明显的层级关系（顶 / 中 / 底；或网关层 → 业务层 → 数据层），平铺会让阅读者误以为"同级"。

**反模式（不要做）**：
```html
<!-- 4 个组件平铺一排，看起来像 4 个独立系统 -->
<section class="panel">
  <div class="node">A</div>
  <div class="node">B</div>
  <div class="node">C</div>
  <div class="node">D</div>
</section>
```

**正解**：用嵌套的 `.tier` 容器表达层级，每个 tier 一个标签 + 一组节点：

```html
<section class="panel">
  <div class="tier" data-tier="bridge">
    <div class="tier-label"><span class="num">01</span><span>桥接层 · 对外暴露</span></div>
    <div class="tier-body">…1 个节点撑满…</div>
  </div>
  <div class="tier" data-tier="biz">
    <div class="tier-label"><span class="num">03</span><span>业务层 · 三件套</span></div>
    <div class="tier-body">…3 个节点平排…</div>
  </div>
  <div class="tier" data-tier="db">
    <div class="tier-label"><span class="num">04</span><span>数据层</span></div>
    <div class="tier-body">…2 个数据库一起…</div>
  </div>
</section>
```

```css
.panel { display: grid; grid-template-columns: 1fr; gap: 22px; padding-top: 48px; }
.tier {
  padding: 14px 16px 16px;
  border-radius: 14px;
  border: 1px dashed rgba(255,255,255,0.10);
  background: rgba(255,255,255,0.012);
  border-left: 3px solid /* 按 tier 染不同色 */;
}
.tier-label { display: flex; align-items: center; gap: 10px;
              font-size: 11.5px; color: var(--text-3); margin-bottom: 10px; }
.tier-label .num { /* mono 编号 chip */ }
.tier-body { display: grid; gap: 14px; grid-template-columns: 1fr; }
.tier[data-tier="biz"] .tier-body { grid-template-columns: repeat(3, 1fr); }
.tier[data-tier="db"]  .tier-body { grid-template-columns: 1fr 1fr; }
```

**配色策略**：每个 tier 的 `border-left` 用一种 tone（紫 / 蓝 / 青 / 灰），形成"自上而下"的色彩降序。

### 2. 复合主节点 · 含内部模块（platform with modules）

**场景**：要表达"一个系统平台，里面有 N 个组件"，**不能**用 N 个 `.node` 平铺（视觉上是 N 个独立系统，破坏层级），要做成**一个突出大节点 + 内部 modules chip 风格**。

**关键**：不要把这种节点跟普通 `.node` 共用 class，否则 `.node[data-type="platform"] { width: 360px }` 会限死宽度。

```html
<div class="aura-node" data-tone="accent">
  <div class="aura-head">
    <span class="aura-title">Aura · 全域监控平台</span>
    <span class="aura-sub">React + FastAPI + 中央数据库</span>
    <span class="aura-pin">★ 中央监控</span>
  </div>
  <div class="aura-modules">
    <div class="aura-mod" data-kind="ui"><span class="ico">◧</span><div class="body">…</div></div>
    <div class="aura-mod" data-kind="service"><span class="ico">⚙</span><div class="body">…</div></div>
    <div class="aura-mod" data-kind="db"><span class="ico">▤</span><div class="body">…</div></div>
    <div class="aura-mod" data-kind="alert"><span class="ico">!</span><div class="body">…</div></div>
  </div>
</div>
```

```css
.aura-node {
  display: block;                  /* 不继承 panel 的 flex */
  width: 100% !important;          /* 强制撑满（防被父 grid/flex 压缩）*/
  max-width: none !important;
  box-sizing: border-box;
  padding: 26px 30px 24px;
  border-radius: 18px;
  background:
    radial-gradient(circle at 12% -20%, rgba(192,132,252,0.18), transparent 55%),
    linear-gradient(135deg, rgba(192,132,252,0.05), rgba(129,140,248,0.04)),
    var(--bg-card);
  border: 1.5px solid color-mix(in oklab, var(--c-accent) 55%, transparent);
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,0.08),
    0 0 36px color-mix(in oklab, var(--c-accent) 14%, transparent);
  animation: aura-breath 5.2s ease-in-out infinite;
}
.aura-modules {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
}
@media (max-width: 1100px) { .aura-modules { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 600px)  { .aura-modules { grid-template-columns: 1fr; } }
.aura-mod {
  min-width: 0;                    /* 允许内容收缩，防字竖排 */
  display: flex; gap: 10px;
  padding: 12px 14px;
  background: rgba(255,255,255,0.02);
  border: 1px solid var(--border);
  border-radius: 10px;
}
.aura-mod .ico {
  flex: none; width: 28px; height: 28px;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  /* 按 data-kind 配 background / color */
}
@keyframes aura-breath {
  0%, 100% { box-shadow: inset 0 1px 0 rgba(255,255,255,0.08),
                          0 0 36px color-mix(in oklab, var(--c-accent) 14%, transparent); }
  50%      { box-shadow: inset 0 1px 0 rgba(255,255,255,0.10),
                          0 0 56px color-mix(in oklab, var(--c-accent) 28%, transparent); }
}
```

**踩坑提醒**：
- 如果 modules 字"竖排成一列字"，99% 是子项 `min-width: 0` 没设，被 grid 强制成极窄列
- 如果整个节点只占父容器 1/3，95% 是父级 `.panel` 的 `display: flex` 没被覆盖；用 `#panel-xxx { display: block !important; }`

### 3. 节点视觉差异化 · 项目 vs 数据库 vs 端口

**场景**：单 panel 里同时有"软件项目"、"数据库"、"对外端口"三类，全部用同一个圆角矩形会看起来"都是一样的盒子"，丢失语义。

**做法**：用 type 触发不同视觉，并加 prefix icon：

```css
/* 项目（service）— 左侧 3px 渐变高亮条 + 渐变背景 */
.node[data-type="service"] {
  background: linear-gradient(90deg, color-mix(in oklab, var(--c-primary) 8%, transparent) 0%, transparent 30%), var(--bg-card);
}
.node[data-type="service"]::after {
  content: ''; position: absolute;
  left: 0; top: 12%; bottom: 12%;
  width: 3px; border-radius: 0 3px 3px 0;
  background: color-mix(in oklab, var(--c-primary) 70%, transparent);
  box-shadow: 0 0 8px color-mix(in oklab, var(--c-primary) 50%, transparent);
}
.node[data-type="service"] .title::before { content: '⚙ '; color: var(--c-primary); font-size: 11px; }

/* 数据库（table）— 圆柱视觉（顶部弧条 + 条纹纹理）*/
.node[data-type="table"] {
  border: 1px solid rgba(148,163,184,0.35);
  background:
    repeating-linear-gradient(0deg,
      rgba(148,163,184,0.04) 0 1px,
      transparent 1px 6px),
    rgba(255,255,255,0.025);
  padding-top: 22px;
}
.node[data-type="table"]::before {
  content: ''; position: absolute;
  top: 0; left: 0; right: 0; height: 14px;
  background: rgba(148,163,184,0.12);
  border-bottom: 1px solid rgba(148,163,184,0.25);
  border-radius: 12px 12px 0 0;
}
.node[data-type="table"]::after {
  content: '▤'; position: absolute;
  top: 6px; left: 12px; font-size: 10px;
  color: var(--c-mute); letter-spacing: 1px;
}

/* API 端口（api）— 不要用胶囊形（容易超框）·
 * 长名字（"WaveBridge · 桥接器"）必须用 service type，胶囊容易溢出。
 * api type 只用于真正的短端口名（"/health"、":8443"）*/
.node[data-type="api"] {
  background: linear-gradient(90deg, rgba(94,234,212,0.06), rgba(56,189,248,0.04)), var(--bg-card);
  border-color: color-mix(in oklab, var(--c-primary) 50%, transparent);
}
```

**踩坑提醒**：长中文标题（含项目名 + 子标题）配 `type="api"` 的胶囊形（`border-radius: 999px`）会溢出 — 这种情况一律用 `service` type。

### 4. 区域分组 · 按业务维度切分（非随机平铺）

**场景**：N 个区域 / 实例平铺成一片网格，看不出分类（"市级 / 区级"、"接入方式 A / B / C"）。

**做法**：在 DATA 里给 region 加 `group` 字段，render 时按 group 切块，每块一个 `.region-group` 容器（彩色左边条 + 块标题）：

```html
<div class="regions-grid">
  <div class="region-group">
    <div class="region-group-label">
      <span class="num">市</span>
      <span>市级 · 1 个</span>
    </div>
    <div class="region-group-body">… nodes …</div>
  </div>
  <div class="region-group">
    <div class="region-group-label"><span class="num">区·接市</span><span>杭州下属区 · 4 个</span></div>
    <div class="region-group-body">… nodes …</div>
  </div>
</div>
```

```css
.regions-grid { display: flex; flex-direction: column; gap: 18px; }
.region-group {
  padding: 14px 16px 16px;
  border-radius: 12px;
  border: 1px dashed rgba(255,255,255,0.10);
  background: rgba(255,255,255,0.012);
}
.region-group:nth-child(1) { border-left: 3px solid color-mix(in oklab, var(--c-accent) 50%, transparent); }
.region-group:nth-child(2) { border-left: 3px solid color-mix(in oklab, #38bdf8 50%, transparent); }
.region-group:nth-child(3) { border-left: 3px solid color-mix(in oklab, var(--c-warn) 50%, transparent); }
.region-group-body {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}
@media (max-width: 1100px) { .region-group-body { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 780px)  { .region-group-body { grid-template-columns: repeat(2, 1fr); } }
```

### 5. 反向代理 / 网关 panel · 多行域名分级

**场景**：列出多个域名 / 端点 / 实例，混在一行不可读。

**做法**：用 `.proxy-row` + `.proxy-tag` 分级，每行一个 tag + 该级别的所有 url：

```html
<section class="panel" data-layer="proxy">
  <div class="proxy-title"><span class="dot"></span>● Layer 2 · 反向代理网关 · 公司域名出口</div>
  <div class="proxy-body">
    <div class="proxy-row">
      <span class="proxy-tag tag-city">市级 · 1</span>
      <span class="url">syzh.bridge.iktapp.com</span>
      <span class="proxy-note">善育在杭</span>
    </div>
    <div class="proxy-row">
      <span class="proxy-tag tag-region">区级 · 10</span>
      <span class="url">gs.bridge.iktapp.com</span> ·
      …
    </div>
    <div class="proxy-row proxy-foot">
      <span style="color: var(--text-3)">认证：HMAC + nonce 防重放 · 60s 时间窗</span>
    </div>
  </div>
</section>
```

```css
.proxy-body { font-family: ui-monospace, monospace; font-size: 12px;
              display: flex; flex-direction: column; gap: 8px; }
.proxy-row { display: flex; align-items: center; flex-wrap: wrap; gap: 8px 6px; }
.proxy-row.proxy-foot {
  padding-top: 6px; border-top: 1px dashed rgba(255,255,255,0.06);
  font-family: -apple-system, "PingFang SC", system-ui, sans-serif;
}
.proxy-tag {
  flex: none;
  font-size: 11px; padding: 2px 9px; border-radius: 999px;
  font-family: -apple-system, "PingFang SC", system-ui, sans-serif;
}
.tag-city   { background: rgba(192,132,252,0.10); color: var(--c-accent); border: 1px solid color-mix(in oklab, var(--c-accent) 35%, transparent); }
.tag-region { background: rgba(56,189,248,0.10); color: #38bdf8; border: 1px solid color-mix(in oklab, #38bdf8 35%, transparent); }
.url { color: var(--c-primary); }
.proxy-note { color: var(--text-3); font-size: 11.5px;
              font-family: -apple-system, "PingFang SC", system-ui, sans-serif; }
```

### 6. 可折叠侧栏 Legend

**场景**：左侧 fixed legend 在窄屏遮挡内容、用户想看图时不能临时收起。

**做法**：legend 加一个 toggle 按钮 + `localStorage` 记住状态：

```html
<aside class="legend" id="legend">
  <button class="legend-toggle" id="legend-toggle">◀</button>
  <div class="legend-content">
    <h4>Node tones</h4> …
  </div>
</aside>
```

```css
.legend {
  /* 原 fixed-left 200-224px 样式 */
  transition: width 240ms var(--ease-out), padding 240ms var(--ease-out);
}
.legend.collapsed { width: 36px; padding: 8px 6px; overflow: hidden; }
.legend.collapsed .legend-content { display: none; }
.legend-toggle {
  position: absolute; top: 8px; right: 8px;
  width: 22px; height: 22px;
  display: flex; align-items: center; justify-content: center;
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text-2);
  cursor: pointer;
}
.legend.collapsed .legend-toggle { position: static; margin: 0 auto; }
@media (max-width: 1400px) {
  .legend:not(.collapsed) { display: none; }
  .legend.collapsed { display: block; }
}
```

```js
function initLegendToggle() {
  const legend = document.getElementById('legend');
  const btn = document.getElementById('legend-toggle');
  if (!legend || !btn) return;
  try {
    if (localStorage.getItem('legend-collapsed') === '1') {
      legend.classList.add('collapsed');
      btn.textContent = '▶';
    }
  } catch (e) {}
  btn.addEventListener('click', () => {
    const collapsed = legend.classList.toggle('collapsed');
    btn.textContent = collapsed ? '▶' : '◀';
    try { localStorage.setItem('legend-collapsed', collapsed ? '1' : '0'); } catch (e) {}
  });
}
```

### 7. 弹性进场 · 突出主节点

**场景**：一个突出的主节点（如 Aura）需要"权重感"，普通的 clip-path 擦出太平淡。

**做法**：用 cubic-bezier 反弹曲线 + scale + blur 过渡：

```css
@keyframes aura-pop {
  0%   { opacity: 0; transform: translateY(14px) scale(0.92); filter: blur(4px); }
  60%  { opacity: 1; transform: translateY(-3px) scale(1.02); filter: blur(0); }
  100% { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }
}
.aura-node.entering { opacity: 0; transform: translateY(14px) scale(0.92); }
.aura-node.enter    { animation: aura-pop 720ms cubic-bezier(0.34, 1.56, 0.64, 1) forwards; }
```

入场错峰：核心主节点（aura）先弹出 → 然后基础设施 + 业务节点常规 stagger。

### 8. 整体居中校验

**反模式**：内容左对齐贴边，右侧大片空白（panel max-width 没生效）

**做法**：
- 顶层 `<div id="app" class="relative max-w-[1600px] mx-auto px-8 py-10">`
- 所有 panel 直接是它的子元素（不要包嵌套 grid 撑出对齐问题）
- Layer 1/2/3 全宽堆叠，Layer 4（区域汇总）单独最下方（不要跟 Layer 3 并排）

### 9. 命名一致性 · 中文 vs 英文混用规则

- **节点 title**：可以中英混杂（`Aura · 全域监控平台` / `WaveBridge · 桥接器`），破折号分隔产品代号 + 中文角色
- **节点 subtitle / description**：纯中文（描述用语言）
- **chip / 标签**：技术栈用英文（`React`、`FastAPI`、`:8443`），中文角色用中文（`双语言`、`异步`）
- **section title**：中文（`新架构全景` / `关键能力`）
- **legend 标题**：英文 UPPERCASE（`Node tones / Link kinds / Tier / Markers`）— 这是 dark-techy 的工程文档调性

避免出现"半中半英奇怪混搭"（`Web Dashboard` 在中文卡里、`Aggregator` 没翻译）—— 业务文档优先用中文（"监控视图 / 聚合服务 / 中央数据库 / 告警引擎"），保留代号用英文。

### 10. ID 稳定性 vs 显示文本

设计 DATA 时分清两类字段：
- `id`：稳定，用于 `link.from / to` 引用，**不轻易改**（改一处要全文搜替换）
- `title / subtitle / label / note`：可随时改，仅影响显示

如果项目改名（如 `wave-bridge` → `WaveBridge`），把改动限制在 `title`，**不要动 `id: "stack-bridge"`**，否则连线会断。

---

## Layer 4 (区域汇总) 在 deck 末尾的呈现规则

如果是"省 / 市 / 区"三级分层架构，**省级通常不属于改造范围**（它是上游数据源），不要把省级也做成 region 节点占据 Layer 4 的网格 — 会让阅读者误以为省级也部署了我们的代码。

正确做法：
- panel-proxy（反代）只列**自己部署 bridge 的层级**（市 + 区，不列省）
- panel-regions（Layer 4）只放**自己部署 stack 的实例**（市 + 10 个区，不放省级）
- 省级"数据源"角色用左侧 hero 文案 / 痛点段落体现，不进架构图主体

---

## topology-poster 专属经验（基于跨网架构图沉淀）

`topology-poster.html` 是 dark-techy 风格在"单页 1920×1080 网络架构海报"形态下的完整实例。下面是这套形态独有的规则与踩坑：

### A. 整体布局：固定 1920×1080 + scale 自适应

- `.stage` 设 `width:1920px;height:1080px;transform-origin:center center`，所有节点用 absolute + inline `style="left:X;top:Y;width:W;height:H"` 精确摆位
- viewport 自适应通过 `transform: scale(k)` 实现，`k = Math.min(innerWidth/1920, innerHeight/1080)`，绑定 resize/load 事件
- 不要让节点用相对布局或 flex 排版，**架构图位置就是设计**，相对布局会让 SVG 端点对不齐

### B. 网络/域分组用 `<section class="zone">`

- 每个网络（如政务网 / 卫生网 / 公司内网）一个 `.zone`，虚线 dashed border + zone-label（mono UPPERCASE + 中文小字）
- zone 与节点同层（absolute），节点摆在 zone 视觉框内但 DOM 上不嵌套（避免坐标系混乱）
- zone 颜色编码：每个 zone 用一个 brand color (`--c1/--c2/--cm` 等) 作 border + label color，节点不染色（节点按 type 染色）

### C. 节点形状语言扩展

`.node` (横节点) + `.nv` (竖节点，120 宽全高站列，适合"采集器/桥接器"这种独占一列的关键件) + `.featured` (带 ★ 角标关键节点) + `.db-merged` (DB 容器，顶部色带 + 内部 split 多 half) + `.ext` (虚线节点表示外部数据源) + `.aura` (plate 多模块汇聚框)

**关键 trick**：
- `.node{display:flex;flex-direction:column;justify-content:center}` 让内容垂直居中，避免上下大空白
- 节点 height 必须**贴合内容**而非给固定值留白 — height 多 30+px 视觉上松垮
- `.nv` 是独占一列的"采集器/桥接器"型节点，**内容贴顶 `justify-content:flex-start`** 而非居中（否则一列内容居中导致大块空白）
- `.featured .star` 用 `position:absolute;top:-9px;left:12px;z-index:2` 浮在节点上方外（不挤 row1），node 必须 `overflow:visible`
- 不要在 row1 里塞太多内容（icon + name + chip 已饱和），**节点宽度不够时**先减小 padding-left / icon size / chip font，再考虑加宽
- logo 全部 base64 inline data URI（不依赖外部文件，方便分享）；用 `sips -Z 96` 缩到 96px 再 base64，单 logo ~10KB

### D. SVG 连线：必须严格对齐节点边框

- 所有 `<path class="lk ...">` 端点坐标必须**精确落在节点 border 上**（不是中心，不在节点内）
- 给每条 path 加 inline `fill="none"`（CSS 类 `.lk{fill:none}` 在某些导出库里会被忽略，cubic bezier 会被当作 filled 渲染成黑色色块）
- Cubic bezier `M x1 y1 C cx1 cy1 cx2 cy2 x2 y2` — **末端 tangent** = `(x2 - cx2, y2 - cy2)`，决定箭头方向；想让箭头水平指右就让 `cx2 < x2 且 cy2 == y2`；想斜上指就让 `cy2 > y2 略 cx2 < x2`
- 弧度由 `cx1 / cy1` 控制，让 control1 落在起点附近横向延伸（避免变成直线）

### E. Marker（箭头）固定大小

```html
<marker id="mp" viewBox="0 0 10 10" refX="10" refY="5"
        markerWidth="12" markerHeight="12"
        markerUnits="userSpaceOnUse" orient="auto">
  <path d="M0 0 L10 5 L0 10z" fill="var(--lp)"/>
</marker>
```

- `markerUnits="userSpaceOnUse"` 让箭头**大小恒定**（默认 strokeWidth 模式会让不同粗细的线条箭头大小不一）
- `refX=10` 让箭头尖正好在 path endpoint
- `<path class="lk" stroke-linecap="butt">` 而非 round —— round cap 会让 stroke 末端延伸 stroke-width/2 超出 endpoint，导致箭头后面"漏一截线"
- 粒子流 `<animateMotion>` 配 `<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.88;1">` 让粒子在终点前淡出，不会从箭头后露出

### F. Line label（线条说明）紧贴线条 + 一列对齐

- label 是 SVG `<text class="lbl">` 不是 HTML — 跟着 SVG 坐标系
- 多条平行/分叉线条的 label **x 坐标一列对齐**（如全部 x=540 紧贴 ETLFlow 节点右边），y 各贴自己线条起点上方 5-10px
- `.lbl.h{fill:var(--lh)}` 等定义让 label 颜色跟线条颜色一致（用户能看出"这个 label 属于哪根线"）
- label 不要遮挡节点 — 放在节点边框外侧 + 线条贴附位置

### G. 底部三段式说明

1. **CROSS-NET CHANNELS**（跨网通道说明）：top:730 单行 5 列 grid，按通道分组（4 类政务⟷卫生 + 1 类卫生⟷内网），每个 channel card 用对应线条颜色边框
2. **LEGEND**（图例）：节点色块一行 + 线条样式一行，分两行清晰区分
3. **PROJECTS & PORTS**（项目端口总览）：按网络分组（gov-net / health-net / corp-net）流式 chip 排列，每组前置 gtag 色标 + name/port 用 `<b>name</b><i>:port</i>` chip，避免方块边框呆板

### H. 主题切换：`[data-theme]` 双套 token

```css
:root, [data-theme="dark"] { --bg:#0a0e16; --c1:#5eead4; --t1:rgba(255,255,255,.96); ... }
[data-theme="light"]       { --bg:#f4f6fb; --c1:#0d9488; --t1:rgba(15,23,42,.92);   ... }
```

- 所有颜色用 CSS variable，不硬编码 hex
- 顶部 toolbar 加 `<button id="btnTheme">` 切换 `body[data-theme]`，`localStorage` 持久化用户选择
- 避免 `color-mix(in oklab, ...)` 用 hardcoded percent — html2canvas 不支持，但 modern-screenshot 支持

### I. PNG 导出：用 modern-screenshot@4.7.0

```html
<script src="https://cdn.jsdelivr.net/npm/modern-screenshot@4.7.0/dist/index.min.js"></script>
```

- UMD global = `window.modernScreenshot`
- CDN 入口实际是 `dist/index.min.js`，**不是 `dist/index.umd.js`**（jsdelivr 上 `index.umd.js` 404）
- html-to-image / html2canvas 都有 SVG / color-mix 兼容问题；modern-screenshot 4.x 用 SVG foreignObject + 浏览器原生渲染，兼容现代 CSS（`color-mix(in oklab, ...)` ✓）
- 调用：`modernScreenshot.domToPng(stage, { width:1920, height:1080, scale:2, backgroundColor, style:{ transform:'none' } })`
- 已知 limit：`.featured .star` (top:-9 浮在节点外的 ★ 角标) 在 PNG 中**可能被裁掉顶部** — 视为 trade-off 接受，或者让用户截图 viewport 本身

### J. 设计 checklist（每次画完过一遍）

- [ ] 所有节点 width/height 贴合内容，节点内无大块上下空白
- [ ] 所有 SVG path 端点精确在节点 border 上
- [ ] 所有 marker 用 `markerUnits=userSpaceOnUse` 大小一致
- [ ] 所有 path 加 inline `fill="none"`
- [ ] 所有 label 紧贴线条 + 同色 fill
- [ ] 节点之间留够 gap 给箭头 + label（至少 30px）
- [ ] 弧线 control point 让弧度可见而不变直线
- [ ] 跨网通道 / 端口表 / legend 三段式底部说明齐全
- [ ] 主题切换 + PNG 导出按钮齐全
- [ ] logo base64 inline（不依赖外部文件）
