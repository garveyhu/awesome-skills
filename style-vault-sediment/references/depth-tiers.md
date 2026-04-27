# 深度档位 · depth-tiers

沉淀的挖掘粒度由用户选档。**档位在所有 create 分支（from-project / from-web / from-scratch）的第一步都要问**，选完再进本分支自有的 discovery 细节。

---

## 概览

| 档位 | 名称 | 目标条目 | 预估时间 | 使用场景 |
|:---:|---|:---:|:---:|---|
| **1** | 精髓（essence） | **5–8** | 20–30 min | "给别人看 5 样最代表这个站的东西"——最独特视觉点 |
| **2** | 基础（foundation） | **12–18** | 1–1.5 h | 能拿来启动一个同风格新产品的最小设计系统 |
| **3** | 全量（comprehensive） | **30–50+** | 3–4 h | 尽可能 100% 复刻，每条主路由独立 page 条目 |

> 上面是目标区间。**Tier 1 超 10 条要砍**、**Tier 2 超 22 条要砍**、**Tier 3 没有硬上限**（但下限必须达标，见下）。

---

## 问用户的 prompt（路由到具体分支前用）

```
本次沉淀想要多深？

  1) 精髓级（5–8 条 · 20–30 min）
     只提取最代表性的独特视觉点——够"一眼认出这是谁的风格"就行
     典型产物：1 palette + 1 字体 + 1-2 signature 组件/模块 + 1 style + 1 product

  2) 基础级（12–18 条 · 1–1.5 h）  ← 默认
     完整最小设计系统——tokens / 核心组件 / 主要 block / 1-2 代表页面都落盘
     能拿来启动一个同风格新产品

  3) 全量级（30-50+ 条 · 3-4 h）
     尽可能 100% 复刻——每条主路由独立 page 条目 + 表单/状态/动效全扫
     from-web 时请谨慎选这档（没源码无法扫全，实际能出的多半是 Tier 2 的量）

回 1 / 2 / 3（或 "默认"）。
```

**默认值**：用户直接说"沉淀"没选档 → **Tier 2**（最常见需求）。
**校正**：如果用户在范围／预期上明显要极简或极全（例如"就捕一个调色板" / "全部都抽"），应当主动提示对应档位再确认。

---

## Tier 1 · 精髓 · 5–8 条

### 必出

- **1 个 `tokens/palettes/*`** —— 定义性调色板
- **1 个 `tokens/typography/pairs/*`** —— 字体对
- **1 条 signature**（从 block 或 component 中挑最独特的 1-2 条）——"缺了这条就认不出这个站"那种
- **1 条 `styles/*`** —— 把上面聚合
- **1 条 `products/*`** —— 挂 style + refs

### 不出

- 常规 button / input / tag / avatar（除非**极其**独特）
- 页面级条目（pages/*）通常不出；真要出的话只 1 条
- 状态 / 空态 / 表单 等补充条目一律不出
- shadow / motion / radius 等二级 token（除非**就是**该站的招牌）

### 示例（对 skillhub）

1. `tokens/palettes/skillhub/skillhub-teal-mist`
2. `tokens/typography/pairs/skillhub/inter-jetbrains-duo`
3. `components/buttons/skillhub/border-trace-cta`（最独特）
4. `blocks/marketing/skillhub/gradient-hero`（流光 hero）
5. `styles/community-social/skillhub-soft-modernist`
6. `products/skillhub`

**不做**：glass-pill-navbar（虽好但算模式化）、letter-avatar（常见）、teal-pill（常见）、leaderboard-row / skill-card（列表变种）、pages/*（骨架要 Tier 2+ 才出）

---

## Tier 2 · 基础 · 12–18 条

### 必出

- **3–5 个 tokens**：palette / typography（必）+ motion / shadow / radius / spacing 挑 1-3 个标志性的
- **3–5 个 components**：核心 button / input / tag / avatar + 1–2 个 signature
- **3–5 个 blocks**：navbar / hero / 代表性 card / 代表性 row / 代表性 table 选 3-5 种
- **1–3 个 pages**：landing 必出，detail 或 admin 按需补
- **1 个 `styles/*`** + **1 个 `products/*`**

### 推荐补

- 1 条 form 块（如果站点有独特表单样式）
- 1 条 loading / empty 状态条目（只在站点状态表达有辨识度时）

### 不出（和 Tier 3 区分）

- 不做全路由一一对应的 page 条目
- 不做全 state 穷尽
- 不做模式一致性扫描的强制交付（可选做）

### 示例（对 skillhub · 就是本次沉淀的量）

见 `sediment-history/links/2026-04-24-skillhub/report.md`。15 条：4 tokens + 3 components + 4 blocks + 2 pages + 1 style + 1 product。

---

## Tier 3 · 全量 · 30–50+ 条

### 硬下限 checklist

写入阶段前必须完成以下全部项，**有任何一项空缺打断让用户决定**：

- [ ] 全路由枚举完成 → 生成**路由清单表**
- [ ] 跨文件 className 模式扫描完成 → 生成**全局模式清单**（要求至少 3 条 ≥5 次出现且跨 ≥3 文件的模式）
- [ ] 表单系统扫描完成 → 生成**表单清单**
- [ ] 状态系统扫描完成 → 生成**状态清单**（loading / empty / error / success / pulse）
- [ ] 动效目录扫描完成 → 生成**动效清单**（所有 keyframes / framer-motion 模式）
- [ ] **主路由 ≥80% 被沉淀为独立 page 条目**
- [ ] **全局模式 ≥80% 被沉淀为 token 或 component**

### 强制产出的 Discovery 清单

在 step 3 生成写入方案前，AI 必须先贴出 4 张清单让用户过目：

```
=== 路由清单 ===
| Route | File | 职能 | 是否沉淀为独立 page? |
|---|---|---|---|
| / → /discover | discovery/home/index.tsx | 发现 | ✅ pages/landing/skillhub/skill-community-home |
| /skills/:slug | skill/pages/detail/... | 技能详情 | ✅ pages/detail/skillhub/skill-article-detail |
| /practice | practice/pages/index.tsx | 实践广场 | ✅ pages/list-table/skillhub/practice-plaza |
| /practice/:id | practice/pages/detail/... | 实践详情 | ✅ pages/detail/skillhub/practice-post-detail |
| /practice/create | practice/pages/create/... | 发布实践 | ✅ pages/form-flow/skillhub/practice-compose |
| /publish | skill/pages/publish/... | 发布技能 | ✅ pages/form-flow/skillhub/skill-publish-wizard |
| /messages | message/pages/... | 消息会话 | ✅ pages/content-reader/skillhub/im-conversation |
| /me | me/pages/... | 个人中心 | ✅ pages/dashboard/skillhub/user-home |
| /me/edit | me/pages/edit/... | 编辑资料 | ✅ pages/form-flow/skillhub/profile-edit |
| /admin | admin/pages/... | 管理后台 | ✅ pages/list-table/skillhub/admin-console |
| /login | auth/pages/login/... | 登录注册 | ✅ pages/auth/skillhub/auth-split |
| 覆盖率 | | | 11/11 = 100% |

=== 全局模式清单 ===
| 模式 | 出现次数 | 文件数 | 沉淀为 |
|---|---|---|---|
| `bg-[#1a1a1a] text-white ... active:scale-95` | 12 | 8 | components/buttons/skillhub/dark-primary-cta |
| `border-gray-200 focus:border-teal-300 focus:ring-2 focus:ring-teal-100 rounded-xl` | 9 | 6 | components/inputs/skillhub/soft-form-input |
| ...（至少 3 条）

=== 表单清单 ===
| 表单 | 路由 | 字段类型 | 沉淀为 |
|---|---|---|---|
| 登录 / 注册 | /login | email + password + toggle | blocks/form/skillhub/auth-split-form |
| 发布实践 | /practice/create | title + markdown editor + skill picker | blocks/form/skillhub/long-article-compose |
| ...

=== 状态清单 ===
| 状态 | 位置 | 视觉特征 | 沉淀为 |
|---|---|---|---|
| Loading skeleton | 首页技能网格 | h-48 animate-pulse | blocks/feedback/skillhub/skeleton-card |
| Empty | 无搜索结果 | border-dashed + Box icon | blocks/feedback/skillhub/empty-state |
| Error | 加载失败 | bg-rose-50 text-rose-700 | components/indicators/error-banner |
| Pulse dot | systems operational | emerald w-1.5 shadow glow | components/indicators/pulse-dot |

=== 动效清单 ===
| 名称 | 来源文件 | 类型 | 沉淀到 |
|---|---|---|---|
| flow-right 14s | index.less:42 | CSS keyframe | tokens/motion/gentle-flow |
| fadeIn 4px | index.less:49 | CSS keyframe | tokens/motion/gentle-flow |
| whileHover y:-4 | home:463 | framer-motion | tokens/motion/gentle-flow
| BorderTrace ResizeObserver | home:34 | SVG + RO | components/buttons/skillhub/border-trace-cta
| ...
```

### 覆盖率核对表（写入前最后关卡）

```
=== Tier 3 覆盖率核对 ===
✓ 主路由 11/11 → 100% ≥ 80% ✅
✓ 全局模式 5/5 → 100% ≥ 80% ✅
✓ 表单 4/5 → 80% ≥ 80% ✅
✓ 状态 4/4 → 100% ≥ 80% ✅

□ 覆盖率 ≥ 80%，可以继续写入
✖ 覆盖率 < 80%，询问用户：补齐缺口 or 降到 Tier 2？
```

### 不做的事（Tier 3 也不该泛滥到）

- 每条 row / cell 都独立沉淀（合并为一个 blocks/display/* 条目）
- 路由里的 404 / 500 除非样式独特否则不单独出 page 条目
- 完全被 antd 默认样式覆盖的地方（比如没自定义的 Modal）不单独出 component 条目

---

## 档位与 discovery 步骤的绑定

| Discovery 步骤 | Tier 1 | Tier 2 | Tier 3 |
|---|:---:|:---:|:---:|
| 输入解析（realpath 项目路径） | 必 | 必 | 必 |
| 技术栈识别 | 必 | 必 | 必 |
| Style 推断（主色 + 字体 + 气质） | 必 | 必 | 必 |
| **全路由枚举（step 0.5）** | 可选 | 建议 | **必** |
| 组件识别（文件名匹配） | 采样 | 完整 | 完整 |
| **跨文件 className 模式扫描（step 2.5）** | 跳过 | 建议 | **必** |
| **表单 / 状态 / 动效清单（step 3.5）** | 跳过 | 选做 | **必** |
| 六层反向归类输出沉淀计划 | 必 | 必 | 必 |
| **Tier 3 覆盖率核对表** | N/A | N/A | **必**，未达 80% 打断 |

---

## Tier 3 时间预算

粗估（给用户心理预期用）：

- 技术栈识别 + Style 推断：15 min
- 全路由枚举 + 职能标注：30 min
- 跨文件 className 模式扫描：30 min
- 表单/状态/动效清单：30 min
- 生成方案 + 整批 review：30–60 min
- 写入 + sync + 双仓 commit + 报告：60–90 min

**总计 3–4 小时**（实际随项目规模浮动 ±1h）。

---

## 降档 / 升档的触发

沉淀过程中可以**动态调档**：

- Tier 2 → Tier 3：用户在 review 阶段说"还是每条路由都来一个吧" → 回到 step 0 重做路由枚举
- Tier 3 → Tier 2：覆盖率核对卡住 > 20% 缺口且用户不想补 → 砍到 Tier 2 范围
- Tier 1 → Tier 2：用户在 review 看到方案说"再多抽一些" → 补完基础集

调档一定要让用户**明确确认**，不要自己悄悄升/降。
