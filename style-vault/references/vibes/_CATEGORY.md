# Vibes

## 层定义

**整站调性**：覆盖全局的完整形象。一个 vibe 把页面结构、配色、字体三件事绑死在一起，引用后不需要再做任何风格决策。

## 二级桶

| 桶 | 说明 |
|---|---|
| `saas-tool` | SaaS 工具类产品：Notion / Linear / Vercel 风，干净理性 |
| `marketing-brand` | 品牌官网 / 营销落地：Apple / Stripe 风，强视觉叙事 |
| `admin-console` | 管理后台：功能密度大，信息密集型 |
| `content-media` | 内容媒体：Medium / 纽约时报风，阅读优先 |
| `ecommerce-shop` | 电商：图片驱动，强转化 |
| `portfolio-studio` | 作品集 / 工作室：个性强，实验空间大 |
| `community-social` | 社区 / 社交：时间流、feed、互动密集 |
| `experimental` | 实验性 / 艺术向：Awwwards 款，规则之外 |

## 与 archetypes 的边界

- **vibe 把结构+色+字绑死**：引用 `vibes/saas-tool/notion-clean` 直接出来整个风格系统
- **archetype 只管结构**：`archetypes/dashboard/triple-column` 换什么色、什么字不约束
- 判定：如果这条风格脱离了配色就不成立（比如 "dark-academia 书卷气"），归 vibes；如果只是"一种布局样板"，归 archetypes

## 命名约定

- 二级目录 kebab-case：`saas-tool`、`marketing-brand`
- 条目 ID 可以用文件夹式（带 README.md + 多个 token 文件），比如 `vibes/saas-tool/notion-clean/README.md`
- 也可以用单文件：`vibes/saas-tool/notion-clean.md`
- 文件夹式 ID = 文件夹路径，不带 `/README`
