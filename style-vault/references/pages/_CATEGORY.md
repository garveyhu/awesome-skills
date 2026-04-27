# Pages · 页面

## 层定义

**整页样板**：可独立渲染一屏的页面结构。一个 Page 通常由多个 Blocks 拼成，自身只描述「这一类页面通常怎么组织」，不携带设计语言——配色、字体由上层的 Style 决定。

## 二级场景桶

| 桶 | 说明 |
|---|---|
| `landing` | 落地 / 首页：hero + 价值点 + CTA 的综合营销页 |
| `pricing` | 定价页：方案对比表、FAQ、升级引导 |
| `auth` | 登录 / 注册 / 找回密码 / SSO |
| `dashboard` | 仪表盘：指标卡 + 图表 + 最近活动 |
| `list-table` | 列表 / 表格页：筛选 + 表格 + 分页 |
| `detail` | 详情页：主体信息 + 相关操作 + 关联内容 |
| `form-flow` | 表单流：分步表单、向导式引导 |
| `settings` | 设置页：侧栏分组 + 右侧表单 |
| `checkout` | 结账 / 下单 / 支付确认 |
| `content-reader` | 长文阅读：博客、文档、新闻正文页 |
| `search-result` | 搜索结果页：筛选 + 命中列表 |
| `onboarding` | 新手引导：欢迎、引导步骤、首次体验 |
| `profile` | 个人主页 / 用户档案页 |
| `empty-error` | 空态 / 错误 / 404 / 500 |

## 收录边界

**先问一句**：要不要产出新实现？不 → Products；要 → 按粒度 整语言 → 整页 → 整段 → 单件 → 值。

Pages 位于第二层（「整页」）。和相邻层的边界：

- **Pages ↔ Styles**：Page 是骨架，Style 是「骨架+皮肤」。Page 可换色换字也成立；Style 换掉语言就不是它了
- **Pages ↔ Blocks**：Page 覆盖**整屏**（含顶栏、内容区、侧栏）；Block 只是页面里的**一段 section**。判定：如果要单独占据一张屏幕才成立，归 Pages；如果它是页面里可以拼装的积木，归 Blocks

## 命名约定

- 二级目录 kebab-case：`landing`、`list-table`、`empty-error`
- **三级 namespace 强制**（见 [../README.md · Namespace 子目录](../README.md#namespace-子目录强制)）：
  - 单文件：`pages/<bucket>/<namespace>/<slug>.md`
  - 多文件：`pages/<bucket>/<namespace>/<slug>/README.md`，id 取文件夹路径（pages 默认走多文件）
  - `<namespace>` = product 短名（如 `acme` / `skillhub`）；通用件归 `_shared`
- slug 全程 kebab-case
