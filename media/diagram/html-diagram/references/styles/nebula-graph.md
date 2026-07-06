# nebula-graph · 深空星云图谱风

> 领域知识图谱 / 依赖星图 / 关系探索的调性 · 深空底 + 珊瑚暖调 + 径向辉光 + canvas 力导向/树布局 · 拖拽 · 缩放 · 点节点开抽屉

## 视觉 DNA（必须保留，不要随便改）

1. `#080b12` 极深空底 + `radial-gradient` 中心晕影 + **3 团 blur(72px) 彩色辉光**（珊瑚 / 薄荷 / 天蓝）—— 不是网格，是星云氛围
2. **暖珊瑚 `#FF7A45` 主强调** + 琥珀/薄荷/天蓝/紫的多色语义（按 tier / 类型给节点上色）—— 这是它区别于冷调 dark-techy 的关键
3. **全屏 `<canvas>` 力导向 / 树状双布局**：节点 = 发光球（径向渐变光晕 + 实心核 + 白描边），核心域带外环，选中带高亮环
4. 链路 = 极细半透明直线，**高亮时跑发光粒子流**（3 颗沿线流动）
5. **玻璃 HUD**（`backdrop-filter: blur(16px)` + 6~9% 白边）：左上标题牌 + 左下图例 dock + 右下工具按钮
6. 右侧 **390px 抽屉面板**（`cubic-bezier(.22,.9,.24,1)` 滑入）：点节点看它的职责 / 子域 / 迁入包 / 地区差异
7. 图例可点击隐藏分层（`.row.off` 半透明 + 节点 `hidden`）
8. 交互：拖拽平移 / 拖节点 / 滚轮缩放 / 点节点聚焦子树 + 开抽屉 / 树↔网布局切换 / 重置 / 重新布局
9. Space Grotesk（展示 + canvas 标签）+ JetBrains Mono（badge / 编号 / 路径）
10. **数据驱动 + 自包含**：一份 `window.DOMAIN_GRAPH` 内联对象喂满整张图，无外部数据文件、无构建

## 完整 Token 表

```css
:root{
  --bg:#080b12; --bg2:#0d1220;
  --panel:rgba(16,21,34,.72); --panel-b:rgba(255,255,255,.09);
  --ink:#EAF0FB; --ink2:#A7B2CC; --ink3:#6C7793; --faint:#4b5570;

  /* 语义色（节点 tier / 类型） */
  --coral:#FF7A45;  --coral-l:#FFA574;   /* 核心域 core / 主强调 */
  --amber:#F3B95F;                        /* 子域 subdomain */
  --mint:#5FD6A0;                         /* 地区差异 regional */
  --blue:#63A2FF;                         /* 外部集成 integration */
  --cream:#F4E9D8;                        /* hub 业务核心 */
  /* 支撑域 support = #F0A868 · 通用域 generic = #B99BFF（在 JS COLORS 里） */

  --mono:'JetBrains Mono',ui-monospace,monospace;
  --disp:'Space Grotesk','PingFang SC','Noto Sans SC',sans-serif;
  --sans:'Space Grotesk','PingFang SC','Hiragino Sans GB','Noto Sans SC',sans-serif;
}
```

JS 侧 `COLORS`（canvas 画节点/连线用的完整色表，与 token 一致，可被 `GRAPH.colors` 覆盖）：

```js
const COLORS = {
  hub:'#F4E9D8',        // 业务核心根节点
  ctx:'#FF7A45',        // 核心域 bounded context
  support:'#F0A868',    // 支撑域
  generic:'#B99BFF',    // 通用能力域
  sub:'#F3B95F',        // 子域
  reg:'#5FD6A0',        // 地区差异
  intg:'#63A2FF',       // 外部集成锚点
  intgitem:'#7E97C9'    // 外部集成条目
};
```

## 字体栈

- 标题 / HUD：`--disp`（Space Grotesk 500~600）
- badge / 编号 / 路径 slug：`--mono`（JetBrains Mono）
- canvas 内节点标签：`600 <px> 'Space Grotesk','PingFang SC','Noto Sans SC'`（带黑色阴影抗底噪）

## 节点语言（canvas 绘制，非 DOM）

节点是画在 `<canvas>` 上的发光球，由 `type` / `tier` 决定颜色与尺寸：

| type | 语义 | 半径 | 颜色 | 特征 |
|---|---|---|---|---|
| `hub` | 业务核心根 | 12 | cream | 树根，最大标签 |
| `ctx` | 核心域 bounded context | `6.5+val*0.42` | coral | 核心域带常亮外环 |
| `generic` | 通用能力域 | `6.5+val*0.42` | violet | 横切复用 |
| `sub` | 子域 | 3.4 | amber | 挂在领域下方，缩放到一定倍数才显标签 |
| `reg` | 地区差异锚点 | 11 | mint | 汇聚所有 region 链路 |
| `intg` | 外部集成锚点 | 11 | blue | 汇聚所有 intg 条目 |
| `intgitem` | 外部集成条目 | 3.2 | 灰蓝 | 三方平台名 |

每个球画三层：径向渐变光晕（`r*3.3`）→ 实心核 → 白描边；核心域 `act` 态加 tone 外环；选中加高亮环。`dim` 态（有选中/hover 时其它节点）降到 30% 透明。

## 链路语言

- 底噪链路：`lineWidth 0.8/scale`，透明度 `0.13`（无选中）/ `0.05`（dim）
- 高亮链路（选中节点的邻接边）：`lineWidth 1.9/scale`，透明度 `0.85`，**跑 3 颗发光粒子流**（`(time*0.5 + p/3) % 1` 沿线插值）
- 链路颜色 `linkCol(l)` 按 type：reg→mint，intg/ext→blue，sub→amber，generic→violet，support→amber-ish，其余→coral
- 树状模式下**隐藏 reg 交叉连线**（`if(treeMode && l.type==='reg') continue`），保持树的清爽

## HUD 三件套（玻璃）

```css
.glass{ background:var(--panel); backdrop-filter:blur(16px) saturate(140%);
        border:1px solid var(--panel-b); border-radius:16px;
        box-shadow:0 20px 60px -30px rgba(0,0,0,.8); }
```

- **左上 `.top`**：标题牌（badge + h1 + sub）+ 右侧一个 glass 胶囊（放返回链接 / 元信息 / 说明）
- **左下 `.dock > .legend`**：图例，每行 `.orb`(色球) + 分层名 + mono 计数；**点击行 toggle 隐藏该层**
- **右下 `.tools`**：`.btn` 工具按钮（树状↔网状 / 重置视图 / 重新布局），active 态珊瑚描边

图例分层与节点色一一对应（core / support / generic / sub / reg / intg）。图例文案与计数由 `hydrateGraphChrome()` 从 `SUMMARY` 注水，**改数据不用手改图例数字**。

## 抽屉面板（右侧 390px）

点节点 → `openPanel(n)` 按 `type` 渲染不同内容：
- `ctx` / `generic`：kind 徽章 + 编号(`idx / 总数`) + 领域名 + `modules/<id>/` slug + 职责描述 + **建议子域列表** + **典型迁入包 chips** + （若 region）地区差异提示卡
- `sub`：子域名 + `modules/<parent>/<slug>/` + MVC 目录说明
- `hub` / `reg` / `intg` / `intgitem`：对应的角色说明

抽屉 `transform: translateX(102%)` → `.open` 归零，`.42s cubic-bezier(.22,.9,.24,1)` 滑入。

## 数据契约（改填只动这一段）

整张图由内联的 `window.DOMAIN_GRAPH` 驱动，无外部依赖：

```js
window.DOMAIN_GRAPH = {
  summary: {
    counts: { core:3, support:6, generic:3, sub:37, reg:4, intg:6 },  // 图例计数
    subtitle: '核心 3 · 支撑 6 · 通用 3 · 演示数据'                     // 标题副行
  },
  colors: { /* 可选：覆盖 COLORS 里任意 key */ },
  ctx: [
    { id:'account', zh:'账户', tier:'core',      // tier: core | support | generic
      val:11,                                    // 节点大小（半径 = 6.5 + val*0.42）
      subs:[['profile','档案'],['org','组织']],  // 子域 [slug, 中文]
      pkgs:['user-center','rbac-core'],          // 典型迁入的旧包（抽屉里显示）
      region:true,                               // 是否连到地区差异锚点
      rtext:'地区差异说明（region=true 时抽屉里显示，可含 <code>）',
      desc:'领域职责描述，可含 <code>xxx</code>' },
    // ... 更多 context
  ],
  intg: ['WeChatPay','Alipay','SF-Express']       // 外部集成条目名
};
```

图的其余部分（hub / reg / intg 锚点、构图、物理、树布局、渲染、交互、抽屉）**全部自动从这份数据生成，不用改**。

- `id` 是稳定锚（构图 / 连线引用），改名要全文替换；`zh` / `desc` 等只影响显示，随便改
- 想加核心域就往 `ctx` 里加 `tier:'core'` 项并更新 `summary.counts.core`；计数错了图例数字会不准（但不影响图渲染）

## Sample 选用指引

nebula-graph 当前 1 个 sample：

### `knowledge-graph.html` — 自包含交互式知识图谱

- 全屏 canvas 力导向 / 树状双布局，玻璃 HUD（标题 / 图例 / 工具）+ 右侧抽屉
- 内联 `window.DOMAIN_GRAPH` 演示数据（虚构 Orbit 中台的 12 个领域 + 37 子域 + 6 外部集成），改填即替换那份对象
- **核心交互**：拖拽平移 / 拖节点定住 / 滚轮缩放 / 点节点聚焦子树 + 开抽屉 / 树↔网切换 / 重置 / 重新布局 / 图例点击隐藏分层
- **适合**：领域 / 限界上下文知识图谱、模块依赖星图、微服务关系网、概念 / 实体关系探索、"一堆节点 + 层级 + 归属 + 少量跨组关系"的可交互浏览
- **不适合**：静态可打印架构图（用 blueprint / schematic）；精确的网络拓扑对账海报（用 dark-techy 的 topology-poster）；多维数据报表（用 paper-dossier）；单张聚焦图（用 slate-mono-grid）

### sample 选不到怎么办

如果关系是"节点 + 边"但不是"根 → 领域 → 子域"这种层级树（比如纯扁平的服务依赖网），保留 canvas 引擎 / 物理 / HUD / 抽屉 / 配色不动，改 `构图` 段：把 `CTX/INTG` 换成你的节点 - 边模型，`L(s,t,type)` 加你的关系边即可 —— 视觉 DNA 全保留。

## 交互行为

| 行为 | 触发 | 效果 |
|---|---|---|
| 平移 | 拖空白 | 移动相机（`cam.x/y`） |
| 拖节点 | 拖节点 | 定住该节点（`pin`）+ 局部 reheat |
| 缩放 | 滚轮 | 以光标为锚缩放（0.3~5×） |
| 选中 | 点节点 | 高亮邻接 + 聚焦子树 + 开抽屉；树模式下展开子域 |
| 取消 | 点空白 / 关抽屉 | 复位视图 |
| 布局切换 | 树状↔网状按钮 | 树 = 分层 lerp 到固定位；网 = 力导向 reheat |
| 隐藏分层 | 点图例行 | 该 tier 节点 `hidden` |

## 动效与降级

- 持续动效：canvas requestAnimationFrame 循环（物理松弛 + 相机缓动 + 高亮粒子流）
- **`prefers-reduced-motion`**：`const REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches`，为真时**关掉高亮链路的粒子流**（`if(on && !REDUCED)`）；核心交互（拖拽 / 缩放 / 布局）保留 —— 那是可视化本身，不是装饰
- 树状布局 lerp 系数 0.16，约 <1s 收敛到位，不会长时间抖动
- 无 `backdrop-filter` 时 HUD 降级为半透明底，不破相

## 与 dark-techy 的区别（避免选错）

两者都是深色，但 DNA 不同：

| | nebula-graph | dark-techy |
|---|---|---|
| 底纹 | 星云辉光（3 团 blur glow）| 32px 工程网格 |
| 强调色 | 暖珊瑚多色 | 冷青蓝 |
| 渲染 | canvas 力导向 / 树布局 | DOM/SVG 静态节点 + 贝塞尔连线 |
| 布局 | 物理自动 / 可拖拽 | 手工摆位 / absolute |
| 适合 | 关系探索、知识图谱、"让我拖着看" | 拓扑对账、架构海报、方案 deck |

**要交互探索一堆节点关系 → nebula-graph；要精确对账的静态架构图 → dark-techy。**

## CDN 依赖

```html
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:...&family=JetBrains+Mono:...&display=swap" rel="stylesheet" />
```

仅 Google Fonts（带本地 fallback，断网 / file:// 也能看，只是字体回退）。canvas 引擎 / 物理 / 交互全部原生 JS 内联，**零库、零构建**。
