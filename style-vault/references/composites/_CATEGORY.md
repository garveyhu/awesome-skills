# Composites

## 层定义

**场景块**：一个完整功能块。若干 atoms / primitives 组装起来，能独立解决一个场景需求。

## 二级桶

| 桶 | 说明 |
|---|---|
| `display` | 展示类：表格、列表、卡片网格、数据看板块 |
| `entry` | 录入类：表单、搜索框、文件上传、编辑器 |
| `nav` | 导航类：顶栏、侧栏、面包屑、步骤条、tabs |
| `feedback` | 反馈类：通知、Toast、Modal、Drawer、骨架屏 |
| `layout` | 布局类：工具栏、页头、页脚、两列/三列容器 |
| `editor` | 编辑器类：富文本、代码编辑器、画布 |
| `media` | 媒体类：图片画廊、播放器、视频列表 |
| `social` | 社交类：评论列表、点赞、分享、用户卡 |
| `marketing` | 营销类：Hero、feature grid、CTA 块、testimonial |
| `commerce` | 电商类：商品卡、购物车、SKU 选择、价格块 |

## 收录边界

- composite 原则上只引用 atoms 和 primitives。若两个 composite 存在紧耦合的共享（如共用同一套 Ant Design theme），允许在 `uses:` 里声明对另一 composite 的引用，但必须在正文"引用关系"章节说明理由。长期来看应考虑把共享抽成 primitive 层。
- composite 不带路由，也不覆盖整个页面——那是 archetype
- composite 必带可直接复制的核心代码和示例

## 命名约定

- 二级目录 kebab-case：`display`、`entry`、`nav`
- 条目文件名 kebab-case：`table.md`、`toolbar-bar.md`
