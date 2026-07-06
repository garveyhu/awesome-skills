# 风格清单

每个风格 = 一整套视觉语言（色板、节点形状、装饰、动效、图例规范）。

每个风格下有 1+ 个 **sample**，分别覆盖该风格典型的"应用形态"（长滚动 deck / 交互拓扑 / 单图聚焦 / 等）。**sample 不是分类**，是该风格的具体实例 — AI 改填时根据上下文内容形态选最贴近的 sample 作脚手架。

详细规范见 `styles/<style>.md`。

---

## dark-techy · 深色技术风

`#0b0f17` 深色底 + 玻璃毛 + 粒子流 + 32px 网格 + iOS 缓动 + 左侧 fixed 图例。
**适合**：系统架构演示、运维拓扑、政务大屏、向上汇报 deck。

**Samples**:

| sample | 形态 | 适合内容 |
|---|---|---|
| `narrative-deck.html` | 长滚动叙事 deck（hero + 痛点 + 蓝图 + 能力 + 时间轴 + YAGNI） | 方案论证、汇报、白皮书 hero |
| `interactive-link-map.html` | 单屏交互拓扑（节点 + SVG 连线 + 抽屉 + 搜索 + hover 联动） | 服务拓扑、依赖排查、运维工具 |
| `topology-poster.html` | 单页 1920×1080 网络架构海报（多网络 zone + 节点 + 弧线 + 跨网通道说明 + 项目端口表 + legend + 暗/亮主题切换 + PNG 导出） | 跨网/多区域系统架构图、政务/企业内网拓扑、面向领导/运维的对账图 |

→ `styles/dark-techy.md`

---

## slate-mono-grid · 深灰极简

`#020617` 深灰底 + JetBrains Mono + 40px 网格 + 6 色语义编码 + 单图聚焦。
**适合**：技术博客插图、API 流程图、AWS/云架构图、文档配图。

**Samples**:

| sample | 形态 | 适合内容 |
|---|---|---|
| `single-figure.html` | 单图聚焦卡（header + 主 SVG 图 + 3 摘要卡 + 元信息） | README 顶图、博客插图、论文配图 |

→ `styles/slate-mono-grid.md`

---

## blueprint · 蓝图工程图风

`#f5f1e8` 米黄牛皮纸 + 黑色细线 + 阴影偏移 + Courier 标签 + 双线边框。像建筑师工程蓝图。
**适合**：内网架构图 / 政务架构图 / 工程师手画感的内部文档 / 黑白复印保真。

**Samples**:

| sample | 形态 | 适合内容 |
|---|---|---|
| `topology-poster.html` | 单页 1920×1080 网络拓扑海报（多网络区 + 节点 + 连线 + 底部跨网通道说明 + legend bar） | 内网架构图、政务架构图、运维布线图、墙贴 / A3 打印 |

→ `styles/blueprint.md`

---

## schematic · 现代工程图风

`#eef2f7` 浅蓝灰底 + 白卡 + 类型色条 + 圆角阴影 + SF Mono 标签。AWS / Lucidchart / draw.io 调性。
**适合**：现代企业架构图 / 技术 wiki 顶图 / 新人 onboarding / 浅色环境长时间观看。

**Samples**:

| sample | 形态 | 适合内容 |
|---|---|---|
| `topology-poster.html` | 单页 1920×1080 网络拓扑海报（多网络区 + 节点 + 连线 + 底部跨网通道说明 + legend bar） | 企业架构图、Confluence 文档顶图、新人 onboarding、内部技术汇报副屏 |

→ `styles/schematic.md`

---

## paper-dossier · 暖纸档案报表

`#f6f7f2` 暖纸底 + 28px 工程网格 + 硬边直角面板 + 6 色语义（tier→tone）+ Avenir/JetBrains Mono + 双色径向晕。像工程评估报告 / 代码审计档案。
**适合**：代码库/领域盘点评估、工作量估算与分工、架构治理报告、模块审计、数据表+图表混排的分析档案；浅色长看、可打印。

**Samples**:

| sample | 形态 | 适合内容 |
|---|---|---|
| `analytics-report.html` | 多区块数据评估报告（sticky pill 导航 + KPI 板 + 泳道图谱 + 占比条/星盘/负载 + 文件夹对照 + 可排序明细表，一份 `domains[]` 驱动） | 领域/代码盘点、工作量估算、模块审计、技术尽调、"一堆条目 × 多维指标 + 占比 + 排序"的分析报告 |

→ `styles/paper-dossier.md`

---

## nebula-graph · 深空星云图谱

`#080b12` 深空底 + 3 团 blur 辉光 + 暖珊瑚多色 + canvas 力导向/树布局 + 玻璃 HUD + 右侧抽屉。发光球节点 + 高亮粒子流，可拖拽/缩放/点开抽屉。
**适合**：领域知识图谱、限界上下文图、模块依赖星图、微服务关系网、概念/实体关系的可交互探索。

**Samples**:

| sample | 形态 | 适合内容 |
|---|---|---|
| `knowledge-graph.html` | 自包含交互式知识图谱（全屏 canvas 树↔网双布局 + 图例分层隐藏 + 点节点开抽屉，内联 `window.DOMAIN_GRAPH` 数据） | 领域/上下文知识图谱、依赖星图、关系网络探索、"节点 + 层级 + 归属 + 少量跨组关系"的交互浏览 |

→ `styles/nebula-graph.md`

---

## 裸 `/html-diagram` 输出格式

```
可用风格：

▎ dark-techy · 深色技术风
  深色底 + 玻璃毛 + 粒子流 + 网格底 + 工程感图例
  适合：系统架构演示、运维拓扑、政务大屏、向上汇报 deck

  样例（复制到浏览器查看）：
    file://${SKILL_DIR}/assets/styles/dark-techy/samples/narrative-deck.html
      ↳ 长滚动叙事 deck（方案论证 / 汇报）
    file://${SKILL_DIR}/assets/styles/dark-techy/samples/interactive-link-map.html
      ↳ 单屏交互拓扑（服务拓扑 / 排查）
    file://${SKILL_DIR}/assets/styles/dark-techy/samples/topology-poster.html
      ↳ 单页 1920×1080 跨网架构海报（多 zone / 弧线 / 端口表 / 主题切换 / PNG 导出）

▎ slate-mono-grid · 深灰极简
  #020617 底 / JetBrains Mono / 40px 网格 / 6 色语义编码
  适合：技术博客插图、API 流程图、AWS/云架构图、文档配图

  样例：
    file://${SKILL_DIR}/assets/styles/slate-mono-grid/samples/single-figure.html
      ↳ 单图聚焦卡（README 顶图 / 博客插图）

▎ blueprint · 蓝图工程图风
  #f5f1e8 米黄底 / Courier 标签 / 黑细线 + 双线边框 / 阴影偏移 / 不依赖动画
  适合：内网架构图、政务架构图、工程师手画感文档、墙贴 / A3 打印

  样例：
    file://${SKILL_DIR}/assets/styles/blueprint/samples/topology-poster.html
      ↳ 单页 1920×1080 网络拓扑海报（适合打印）

▎ schematic · 现代工程图风
  #eef2f7 浅灰底 / 白卡 / 类型色条 + 圆角阴影 / SF Mono / AWS-Lucidchart 调性
  适合：现代企业架构图、Confluence 顶图、新人 onboarding、浅色环境观看

  样例：
    file://${SKILL_DIR}/assets/styles/schematic/samples/topology-poster.html
      ↳ 单页 1920×1080 网络拓扑海报（适合浅色环境长看）

▎ paper-dossier · 暖纸档案报表
  #f6f7f2 暖纸底 / 28px 工程网格 / 硬边直角面板 / 6 色语义 / Avenir + JetBrains Mono
  适合：领域/代码盘点评估、工作量估算与分工、架构治理报告、模块审计（浅色长看 / 可打印）

  样例：
    file://${SKILL_DIR}/assets/styles/paper-dossier/samples/analytics-report.html
      ↳ 多区块数据评估报告（KPI 板 + 泳道图谱 + 占比条/星盘/负载 + 可排序表）

▎ nebula-graph · 深空星云图谱
  #080b12 深空底 / 3 团辉光 / 暖珊瑚多色 / canvas 力导向+树布局 / 玻璃 HUD + 抽屉
  适合：领域知识图谱、限界上下文图、模块依赖星图、微服务关系网、关系交互探索

  样例：
    file://${SKILL_DIR}/assets/styles/nebula-graph/samples/knowledge-graph.html
      ↳ 自包含交互式知识图谱（拖拽 / 缩放 / 树↔网切换 / 点节点开抽屉）

用法：
  /html-diagram <style-name> 画一个 xxx
  /html-diagram 画一个 xxx        ← 我会推荐风格让你确认
  /html-diagram                   ← 列出本清单（当前就是）
```

`${SKILL_DIR}` 替换成 SKILL.md 加载时注入的 Base directory 绝对路径。
