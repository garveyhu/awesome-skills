# blueprint · 蓝图工程图风

> 米黄牛皮纸 + 黑色细线 + 阴影偏移 + Courier 标签 · 像建筑师工程蓝图

## 视觉 DNA（必须保留）

1. `#f5f1e8` 米黄牛皮纸底 + 全屏 `radial-gradient` 暗角晕染
2. 40px 浅褐色网格底纹（`rgba(160,140,90,.08)`）
3. **黑色 1.5px 细边框**（节点 + 网络区） · 双线效果通过 `inset 3px` 内描边 dashed 实现
4. **阴影偏移**（`box-shadow: 2.5px 2.5px 0 var(--ink)`） — 工程蓝图最关键的"实体感"标识
5. 节点左侧 5px 色条标识类型（svc / mon / sched / mq / db / cross / ext）
6. **Courier New 等宽字体** 标 label / port / 编号 · 中文用 Hiragino Sans GB / PingFang SC
7. 突出节点：双线边框（`0 0 0 5px var(--paper), 0 0 0 7px var(--ink)` 模拟两层）
8. 标签 chip：`background: var(--paper)` + 黑细边 + Courier · 像图纸印章
9. Hero 顶部水平分割线（`border-bottom: 1.5px solid var(--ink)`） · 工程图首页标准头
10. 右上"BLUEPRINT · 年份"旋转 -2° 印章效果

## 完整 Token 表

```css
:root {
  /* 纸张 */
  --paper:   #f5f1e8;   /* 米黄底 */
  --bg-c:    #fefcf7;   /* 节点白底（略带温度） */
  --ink:     #1a1a1a;   /* 主线 / 主文字 */
  --ink2:    #444;
  --ink3:    #777;
  --bdL:     #bbb;      /* 浅辅助线 */

  /* 类型色（hi-* 用于线条 / 高亮，tone-* 用于左侧色条） */
  --hi-blue:    #1d4ed8;
  --hi-orange:  #d97706;
  --hi-purple:  #7e22ce;
  --hi-pink:    #be185d;
  --hi-green:   #15803d;
  --hi-red:     #b91c1c;

  --tone-svc:   #0f766e;  /* 业务执行 */
  --tone-sched: #b45309;  /* 调度 / 反代 */
  --tone-mq:    #9d174d;  /* 消息队列 */
  --tone-db:    #475569;  /* 数据库 / 上游 */
  --tone-mon:   #5b21b6;  /* 监控 / 中央 */
}
```

## 字体栈

```css
font-family: "Hiragino Sans GB", "PingFang SC", system-ui, sans-serif;
```

mono / label / port chip / Hero kicker / 印章：

```css
font-family: "Courier New", "Courier", ui-monospace, monospace;
```

## 节点形状语言

| type | 关键特征 |
|------|----------|
| `node` standard | 白底 · 黑细边 1.5px · 阴影偏移 2.5px · 左侧 5px 色条 · padding-left 56px 给 icon |
| `node.featured` | 双线边框（外 5px paper + 7px ink）· 顶部跳出 `★ XX` Courier 印章 |
| `nv` vertical | 同 standard，但 icon-big 上方 + 标题居中 + port chip 下方 |
| `db-merged` | 大长方形 + 顶部 mono 标题 + 内部 grid 双块（dashed 描边） |
| `aura` plate | 2.5px ink 边 + 5px ink 偏移阴影 + 紫色渐变内填 · 分两段（head + module grid） |
| `ext` external card | 米色填充 + dashed red 边 + 阴影偏移 · 顶部跳出 `EXTERNAL · 外部` 印章 |

通用质感：

```css
.node {
  background: var(--bg-c);
  border: 1.5px solid var(--ink);
  border-radius: 5px;
  box-shadow: 2.5px 2.5px 0 var(--ink);
}
.node::before {                       /* 左侧 5px 色条 */
  content: ''; position: absolute;
  left: 0; top: 0; bottom: 0; width: 5px;
}
.node[data-t="svc"]::before { background: var(--tone-svc); }
/* ... */
```

## 链路语言（SVG）

```css
.lk { fill: none; stroke-linecap: round; stroke-width: 1.8; }
.lk.lp { stroke: var(--hi-blue); }                              /* 业务流 实线 */
.lk.lh { stroke: var(--hi-orange); stroke-dasharray: 6 5; }     /* SDK 推送 虚线 */
.lk.lb { stroke: var(--hi-purple); stroke-dasharray: 4 4; }     /* 反查 / 配置 */
.lk.lm { stroke: var(--hi-pink); stroke-dasharray: 8 5; stroke-width: 2.4; } /* mq-kafka */
.lk.lg { stroke: var(--hi-green); stroke-width: 2.4; }           /* 跨网代理 实线 */
.lk.cross { stroke-width: 2.6; }                                /* 跨网通道 加粗 */
```

**箭头 marker**：每种 stroke 色对应一个 marker（`<marker><path d="M0 1L9 5L0 9z" fill="..."/></marker>`）。

**形状偏好**：贝塞尔曲线为主；近距离也可直线。**所有线宽 ≥ 1.8px** — 工程图要"线条够粗、不抠细节"。

## 装饰元素

### Hero 头

```html
<div class="head">
  <div>
    <div class="title"><span class="kicker">V2 · CODE</span>主标题</div>
    <div class="sub">副标题 · italic</div>
  </div>
  <div class="stamp">BLUEPRINT · 2026</div>
</div>
```

```css
.head { border-bottom: 1.5px solid var(--ink); padding-bottom: 10px; }
.head .title { font-size: 30px; font-weight: 700; color: var(--ink); }
.head .kicker { font-family: "Courier New", monospace; letter-spacing: 3px; font-weight: 600; }
.head .sub { font-style: italic; color: var(--ink2); }
.head .stamp { border: 1.5px solid var(--ink3); padding: 4px 10px; border-radius: 3px;
               transform: rotate(-2deg); font-family: "Courier New", monospace; }
```

### 网络区（zone）

```css
.zone { border: 1.5px solid var(--ink); border-radius: 6px;
        background: rgba(255,255,255,.35); }
.zone::before {                       /* 内描边：dashed double-line */
  content: ''; position: absolute; inset: 3px;
  border: 1px dashed rgba(0,0,0,.18);
  border-radius: 4px; pointer-events: none;
}
.zone-label {
  position: absolute; top: 10px; left: 18px;
  background: var(--paper); padding: 0 10px;            /* 切进边框 */
  font-family: "Courier New", monospace;
  font-size: 12px; font-weight: 700; letter-spacing: 1.5px;
}
```

### 跨网通道说明（channels panel）

底部一条横排 panel：列出 ① ~ ⑤ 跨网通道，每条按 `dir / desc / why` 三行竖排。**每条左侧加 4px 类型色条**（与节点色条呼应）。

## 图例（Legend）

蓝图风的 legend 设计为**底部单行小条**（不是 dark-techy 的左侧 fixed 大面板）— 工程图阅读者习惯翻到图纸底部找图例：

```html
<div class="lgd">
  <div class="lr"><span class="sw a"></span>监控</div>
  <div class="lr"><span class="sw p"></span>执行器</div>
  ...
  <div class="lr"><span class="ln lp"></span>业务流</div>
  <div class="lr"><span class="ln lm"></span>mq-kafka</div>
</div>
```

```css
.lgd {
  position: absolute; left: 54px; height: 36px;
  display: flex; align-items: center; gap: 16px;
  font-size: 11px; color: var(--ink2); font-weight: 600;
}
.lgd .sw { width: 10px; height: 10px; border-radius: 2px;
           border: 1.4px solid var(--ink); flex: none; }
.lgd .ln { width: 26px; height: 2px; border-radius: 999px; flex: none; }
```

## 动效系统

蓝图风**克制**用动效（"纸张感"不该乱跳）：

- 节点 enter：`translate(-4px, -4px) → translate(0, 0)` 600ms iOS 缓动（模拟"图纸印上去"的对齐感）
- 连线粒子：保留（用 SVG `animateMotion`），但粒子 size 较小、`filter: drop-shadow(0 0 3px ...)` 减小光晕
- 不要呼吸 / 不要 glow scale / 不要网格漂移

`prefers-reduced-motion` 一律关粒子 + 关 enter。

## Sample 选用指引

### `topology-poster.html` — 单页 1920×1080 网络拓扑海报

- 信息架构：hero + 多个网络区横向 + 节点 + SVG 连线 + 底部跨网通道说明 + 底部 legend bar
- 固定 1920×1080 设计基准 + `transform: scale()` 全屏适配
- 含 5 个跨网通道、4 个内网通道、6+ 节点、2 个突出节点
- **适合**：内网架构图、政务架构图、运维布线图、墙贴海报、A3/A4 打印
- **不适合**：长滚动叙事、交互拓扑（用 dark-techy 的相应 sample）

## 适合 / 不适合

✅ 适合：
- 内网架构图 / 政务架构图（需要打印或墙贴）
- 工程师"手画"既视感的内部文档
- 黑白复印保真（仅黑墨+米黄底）
- 给非技术领导看（直观、不刺眼）

❌ 不适合：
- 投影演示（米黄底在投影上偏黄褐，远不如 dark-techy 醒目）
- 暗色环境 / 夜晚长时间观看
- 需要强烈"科技感"或"动态感"
- 信息密度极高的运维 dashboard

## CDN 依赖

零。所有 CSS 内联。Courier New 系统字体兜底。
