# Blocks · 模块

## 层定义

**可复用 section**：页面里的一整个模块——Hero / Pricing 表 / FAQ / 工具栏…… 小于 Page，大于 Component。一个 Block 通常由若干 Components + Tokens 组装，能独立解决某个场景需求，可直接嵌入一个 Page。

## 二级场景桶

| 桶 | 说明 |
|---|---|
| `hero` | 页面顶部第一屏的视觉叙事 |
| `cta` | 引导行动模块：按钮 + 文案组合 |
| `feature-grid` | 功能点网格：多列图+文的卖点陈列 |
| `pricing-table` | 定价方案对比表 |
| `testimonials` | 客户口碑 / 评价展示 |
| `faq` | 常见问题折叠列表 |
| `logo-wall` | 客户 Logo 墙 / 合作伙伴展示 |
| `stats` | 数据指标陈列 |
| `timeline` | 时间线 / 里程碑展示 |
| `nav` | 顶部导航栏 / 侧栏导航 |
| `footer` | 页脚 |
| `toolbar` | 操作工具栏：筛选 / 批量操作 / 视图切换 |
| `tabs` | 标签页容器 section |
| `breadcrumb` | 面包屑导航 |
| `form` | 表单段落：登录表单、设置表单 |
| `filters` | 筛选条 / 多条件过滤块 |
| `search` | 搜索入口 + 联想 / 结果面板 |
| `card-grid` | 卡片网格：作品、文章、商品瀑布 |
| `list` | 列表 section：带 header / footer 的条目列表 |
| `table` | 数据表格 section |
| `gallery` | 图片 / 媒体画廊 |
| `media-player` | 视频 / 音频播放器 section |
| `notification` | 通知 / Toast / 消息面板 |
| `banner` | 顶栏 / 公告条 / 促销横幅 |
| `modal-content` | 弹层内容骨架（表单、确认、向导等） |

## 收录边界

**先问一句**：要不要产出新实现？不 → Products；要 → 按粒度 整语言 → 整页 → 整段 → 单件 → 值。

Blocks 位于第三层（「整段」）。和相邻层的边界：

- **Blocks ↔ Pages**：Block 是一段 section，不覆盖整屏，不带路由；Page 是整页，通常由多个 Blocks 拼出来
- **Blocks ↔ Components**：Block 是「一整段」，通常含若干 Components；Component 是「一件」单一原子。判定：如果它里面天然包含多种类型的交互件（按钮 + 输入 + 列表），归 Blocks；如果只是单一交互件，归 Components
- Block 原则上只引用 Components 和 Tokens。若两个 Block 紧耦合共享了结构，允许在 `uses:` 里声明对另一 Block 的引用，但必须在正文「引用关系」章节说明理由

## 命名约定

- 二级目录 kebab-case：`hero`、`pricing-table`、`modal-content`
- **三级 namespace 强制**（见 [../README.md · Namespace 子目录](../README.md#namespace-子目录强制)）：
  - 单文件：`blocks/<bucket>/<namespace>/<slug>.md`
  - 多文件：`blocks/<bucket>/<namespace>/<slug>/README.md`，id 取文件夹路径
  - `<namespace>` = product 短名（如 `acme` / `skillhub`）；通用件归 `_shared`
- slug 全程 kebab-case
