# schematic · 现代工程图风

> 浅灰底 + 白色卡片 + 类型色条 + 圆角阴影 · AWS / Lucidchart / draw.io 调性

## 视觉 DNA（必须保留）

1. `#eef2f7` 浅蓝灰底 + 24px 圆点底纹（`radial-gradient` 点阵，`opacity: .4`）
2. 节点白卡 `#ffffff` + 1px 浅边 `#cbd5e1` + 两层柔阴影（`0 1px 2px + 0 2px 8px`）
3. **节点顶部 4px 类型色条** 标识业务角色（svc 蓝 / mon 紫 / sched 橙 / mq 粉 / db 灰 / cross 绿 / ext 红）
4. **icon 在节点左侧 chip 里**：40×40 圆角方块 + 类型色 10% bg + 类型色 stroke icon
5. port chip：mono · 类型色填充 + 类型色 70% 文字（不是黑色）
6. **突出节点**：双层环（外发光 `0 8px 28px` + `0 0 0 2px` 类型色 ring）
7. 网络区 panel：白底 + 顶部 4px 类型色条 + 右上 monospace 角标（badge）
8. Hero 顶部"SCHEMATIC · v2" mono 印章框
9. **企业 IT 现代调性** — 颜色温和饱和度低、留白充足、信息密度中等

## 完整 Token 表

```css
:root {
  /* 基础 */
  --bg:      #eef2f7;
  --paper:   #ffffff;
  --ink:     #1e293b;
  --ink2:    #475569;
  --ink3:    #94a3b8;
  --bd:      #cbd5e1;
  --bdL:     #e2e8f0;

  /* 类型色 + 浅底色（用于 icon chip 背景）*/
  --hi-svc:   #0ea5e9;   --hi-svc-bg:   #e0f2fe;   /* 业务执行 */
  --hi-mon:   #8b5cf6;   --hi-mon-bg:   #ede9fe;   /* 监控 / 中央 */
  --hi-sched: #f59e0b;   --hi-sched-bg: #fef3c7;   /* 调度 / 反代 */
  --hi-mq:    #ec4899;   --hi-mq-bg:    #fce7f3;   /* 消息队列 */
  --hi-db:    #64748b;   --hi-db-bg:    #f1f5f9;   /* 数据库 / 上游 */
  --hi-cross: #10b981;   --hi-cross-bg: #d1fae5;   /* 跨网代理 */
  --hi-ext:   #ef4444;   --hi-ext-bg:   #fee2e2;   /* 外部数据源 */

  /* 链路色 */
  --l-flow:  #0284c7;   /* 业务流 */
  --l-sdk:   #ea580c;   /* SDK 推送 */
  --l-rev:   #9333ea;   /* 反查 / 配置 */
  --l-mq:    #db2777;   /* mq */
  --l-cross: #059669;   /* 跨网代理 */
}
```

## 字体栈

```css
font-family: -apple-system, "PingFang SC", system-ui, sans-serif;
```

mono / port chip / monospace label：

```css
font-family: "SF Mono", ui-monospace, monospace;
```

## 节点形状语言

| type | 关键特征 |
|------|----------|
| `node` standard | 白底 · 10px 圆角 · 1px 边 + 双层阴影 · 顶部 4px 类型色条 · 左侧 icon chip（10px 圆角，类型 bg） |
| `node.featured` | 加 `0 8px 28px` 外发光 + `0 0 0 2px` 类型色环 · 右上 `★ XX` chip 圆角胶囊（类型色填充 + 白字） |
| `nv` vertical | icon-big chip 居中（13px 圆角）+ 标题居中 + port chip 下方 |
| `db-merged` | 大卡 + 左侧 4px 灰色条 + 顶部 SF Mono 标题 + 内部双块（每块 1px 边） |
| `aura` plate | 大卡 + 顶部 4px 紫条 + 双层紫色阴影 + head 横条 + 4 module grid |
| `ext` external card | 红条顶 + 红 icon chip + 浅灰 access chip |

通用质感：

```css
.node {
  background: var(--paper);
  border: 1px solid var(--bdL);
  border-radius: 10px;
  box-shadow:
    0 1px 2px rgba(15,23,42,.05),
    0 2px 8px rgba(15,23,42,.04);
  transition: transform .2s, box-shadow .2s;
}
.node:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(15,23,42,.08);
}
.node[data-t]::before {                   /* 顶部 4px 色条（不是左侧）*/
  content: ''; position: absolute;
  left: 0; top: 0; bottom: 0; width: 4px;
}
```

**icon chip 配色规则**：icon 背景用类型色 `_bg` 浅色变量，icon stroke 用类型色主变量。port chip 同理。

```css
.node[data-t="p"] .ic    { background: var(--hi-svc-bg); }
.node[data-t="p"] .ic svg { color: var(--hi-svc); }
.node[data-t="p"] .p     { background: var(--hi-svc-bg); color: var(--hi-svc); }
```

## 链路语言（SVG）

```css
.lk { fill: none; stroke-linecap: round; stroke-width: 2; }
.lk.lp { stroke: var(--l-flow); }                             /* 业务流 实线 */
.lk.lh { stroke: var(--l-sdk);   stroke-dasharray: 6 5; }    /* SDK 推送 */
.lk.lb { stroke: var(--l-rev);   stroke-dasharray: 4 4; }    /* 反查 / 配置 */
.lk.lm { stroke: var(--l-mq);    stroke-dasharray: 8 5; stroke-width: 2.5; }   /* mq */
.lk.lg { stroke: var(--l-cross); stroke-width: 2.6; }                          /* 跨网代理 */
.lk.cross { stroke-width: 2.8; }                                                /* 跨网通道 */
```

**形状偏好**：贝塞尔曲线为主。dark-techy 一样的 `animateMotion` 粒子，但 size 略大（4px）·`drop-shadow(0 0 5px ...)` 中等光晕。

## 装饰元素

### 网络区 panel

```css
.zone {
  background: var(--paper);
  border-radius: 14px;
  border: 1px solid var(--bdL);
  border-top: 4px solid var(--hi-svc);  /* 类型色顶条 */
  box-shadow:
    0 1px 3px rgba(15,23,42,.04),
    0 8px 32px rgba(15,23,42,.06);
}
.zone-label {                            /* mono 名 + 中文双行 */
  font-family: "SF Mono", monospace;
  font-size: 11px; letter-spacing: 2px; font-weight: 700; text-transform: uppercase;
}
.zone .badge {                           /* 右上角小标 */
  font-family: "SF Mono", monospace;
  font-size: 10.5px; letter-spacing: 1.5px;
  padding: 3px 10px; border-radius: 999px;
  background: var(--bg); border: 1px solid var(--bdL);
}
```

### Hero

```css
.head .title { font-size: 30px; font-weight: 700; color: var(--ink); }
.head .kicker { color: var(--hi-svc); letter-spacing: 3px; font-weight: 700; }
.head .ver {                             /* 右上 印章 */
  padding: 4px 12px; background: var(--paper);
  border: 1px solid var(--bd); border-radius: 6px;
  font-family: "SF Mono", monospace; font-size: 11px;
}
```

### 跨网通道说明（channels panel）

底部一条 panel · 左侧 4px 绿色 cross 色条 + 两大类分组（按 `data-side` 区分）。

```css
.channels {
  background: var(--paper);
  border: 1px solid var(--bdL);
  border-left: 4px solid var(--hi-cross);
  border-radius: 12px;
}
.ch {                                    /* 每条通道 */
  background: var(--bg); border-radius: 8px;
  border-left: 3px solid var(--bd);
}
.ch[data-c="g"]  { border-left-color: var(--hi-cross); }
.ch[data-c="lp"] { border-left-color: var(--l-sdk); }
.ch[data-c="lm"] { border-left-color: var(--hi-mq); }
.ch[data-c="lb"] { border-left-color: var(--l-rev); }
```

## 图例（Legend）

底部单行 legend bar，和 blueprint 风格类似（不用 dark-techy 的 fixed 大面板）：

```css
.lgd {
  height: 36px; display: flex; align-items: center; gap: 18px;
  font-size: 11px; color: var(--ink2); font-weight: 600;
}
.lgd .sw { width: 11px; height: 11px; border-radius: 3px; }   /* 无边框，纯色块 */
.lgd .ln { width: 26px; height: 2.5px; border-radius: 999px; }
```

## 动效系统

适度动效（"现代企业图"应该感觉 alive 但不浮夸）：

- 节点 enter：`translateY(8px) → 0` 600ms iOS 缓动 stagger
- 节点 hover：`translateY(-2px)` + 阴影加深
- 连线粒子：`animateMotion` 标准（4px size）
- aura plate：`box-shadow` 紫色脉冲 5.4s
- 不要呼吸 / 不要 glow / 不要网格漂移

`prefers-reduced-motion` 关粒子 + 关 enter + 关 hover transform。

## Sample 选用指引

### `topology-poster.html` — 单页 1920×1080 网络拓扑海报

- 信息架构：hero + 多网络区 + 节点 + SVG 连线 + 底部跨网通道说明（2 大类分组）+ 底部 legend bar
- 固定 1920×1080 设计基准 + `transform: scale()` 全屏适配
- **适合**：现代企业架构图、新人 onboarding 文档、内部 wiki 顶图、技术汇报副屏
- **不适合**：投影大屏（白底反光，远不如 dark-techy）、墙贴打印（白纸打印浪费墨，用 blueprint 更省）

## 适合 / 不适合

✅ 适合：
- 现代企业架构图（AWS / Lucidchart 调性）
- 技术 wiki / Confluence 文档顶图
- 新人 onboarding 教学
- 浅色环境长时间观看（白领标准办公环境）
- 内部技术汇报副屏 / Slack 截图

❌ 不适合：
- 投影大屏（白底反光太亮）
- 墙贴 / A4 打印（白纸成本高，blueprint 米黄背景更省墨）
- 想"科技感"或"暗黑酷炫"（用 dark-techy）
- 信息密度极高的运维 dashboard

## CDN 依赖

零。所有 CSS 内联。SF Mono / -apple-system 系统字体兜底。
