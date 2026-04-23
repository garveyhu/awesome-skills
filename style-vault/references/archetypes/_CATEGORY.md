# Archetypes

## 层定义

**页面样板**：一类页面的通用结构。archetype 只管"这种页面通常长什么样"，配色和字体完全可换。

## 二级桶

| 桶 | 说明 |
|---|---|
| `landing` | 落地页 / 首页：hero + feature + CTA |
| `dashboard` | 仪表盘：指标卡 + 图表 + 最近活动 |
| `list-table` | 列表 / 表格页：筛选 + 表格 + 分页 |
| `detail` | 详情页：主体信息 + 相关操作 |
| `form-flow` | 表单流：分步表单、引导填写 |
| `auth` | 登录 / 注册 / 找回密码 |
| `content-reader` | 长文阅读：博客、文档、新闻 |
| `settings` | 设置页：侧栏分组 + 表单 |
| `search-result` | 搜索结果页：筛选 + 命中列表 |
| `checkout` | 结账 / 下单 |
| `empty-error` | 空态 / 错误页 / 404 / 500 |
| `pricing` | 定价页：方案对比表 |

## 与上下层边界

### 往上看（vs vibes）

- archetype 可换色换字，vibe 一整套绑死
- archetype 是"骨架"，vibe 是"骨架+皮肤"

### 往下看（vs composites）

- archetype 覆盖**整个页面**：顶栏 + 内容区 + 侧栏
- composite 只是页面里的**一个块**：一张表、一段表单、一个工具栏
- 判定：如果这东西要单独拎出来放一张页面才成立，归 archetype；如果它是放在页面内的一个"积木"，归 composite

## 命名约定

同 vibes：二级目录 kebab-case；条目既可单文件也可文件夹式。
