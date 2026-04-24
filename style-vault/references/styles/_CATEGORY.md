# Styles · 风格

## 层定义

**整套设计语言**：一个 Style 把配色、字体、动效、整体气质绑成一个可引用的「风格」。引用一个 Style 就等于一次性把这套语言的色板、字体对、动效曲线等 Tokens 捆绑带过来，无需再做风格决策。

Style 必须绑定至少一套 Tokens；可以被 Products 直接引用作为整站的设计底座。

## 二级场景桶

| 桶 | 说明 |
|---|---|
| `saas-tool` | SaaS 工具类设计语言：Notion / Linear / Vercel 风，冷静理性 |
| `editorial` | 编辑/杂志向：阅读优先，强排版节奏，衬线大标题常见 |
| `playful` | 活泼俏皮：高饱和配色、手绘感、强品牌叙事 |
| `e-commerce` | 电商向：图片驱动、强转化节奏、价格/促销视觉语言成型 |
| `dashboard` | 后台/控制台：信息密度高，数据可读性优先 |
| `marketing` | 品牌营销：强视觉叙事、大动效，Apple / Stripe 款 |
| `mobile-native` | 移动原生感：iOS / Android 平台气质，触控优先 |
| `game` | 游戏/娱乐向：暗色为主、高对比、装饰性强 |

## 收录边界

**先问一句**：这条内容要不要产出新实现？
- 不产出新实现 → 归 **Products**（只做引用聚合）
- 产出新实现 → 按粒度 **整语言 → 整页 → 整段 → 单件 → 值** 往下走

Styles 位于第一层（「整语言」）。和相邻层的边界：

- **Styles ↔ Products**：Product 是「引用一套 Style + 若干 Pages/Blocks」的聚合视图，不新增实现；Style 是真正定义语言的那一层
- **Styles ↔ Pages**：Style 绑定整套 Tokens + 气质；Page 只描述一个页面的结构，不携带设计语言。判定：如果这条脱离了配色/字体就不成立（如「dark-academia 书卷气」），归 Styles；只是一种布局样板，归 Pages

## 命名约定

- 二级目录 kebab-case：`saas-tool`、`editorial`、`mobile-native`
- 条目单文件：`styles/<bucket>/<slug>.md`
- 条目多文件（配套 cover / tokens 文件）：`styles/<bucket>/<slug>/README.md`，条目 id 为文件夹路径
- slug 全程 kebab-case，一经收录不随意改名
