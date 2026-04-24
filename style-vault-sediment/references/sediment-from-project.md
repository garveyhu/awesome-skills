# sediment-from-project · 本地项目提取

**适用触发**：用户给了本地项目路径（绝对路径 / cwd / 相对路径），希望把该项目的风格沉淀到 vault。

**核心能力**：**把已有代码反向归类到六层资产**（token / component / block / page / style / product）。

---

## 输入解析

用户触发语可能是：

- `沉淀 ~/Projects/acme-admin`
- `沉淀当前项目`（→ 读 cwd）
- `沉淀 /abs/path/to/project`
- `把这个 repo 沉淀到 vault`（→ 若 cwd 是 git repo，就用 cwd；否则反问）

**首步**：把路径规范化到绝对路径。若路径不存在 / 不是目录 → 让用户确认。

```bash
PROJECT=$(realpath "<用户给的路径>")
[[ -d "$PROJECT" ]] || { echo "不是目录"; exit 1; }
```

---

## 档位门 · step 0（必做）

进入所有 discovery 前，**先问用户挖掘深度**（见 [depth-tiers.md](depth-tiers.md)）。

```
本次沉淀想要多深？

  1) 精髓级（5–8 条 · 20–30 min）
  2) 基础级（12–18 条 · 1–1.5 h）  ← 默认
  3) 全量级（30–50+ 条 · 3–4 h）

回 1 / 2 / 3（默认 2）。
```

**档位决定后续 discovery 强度**：

| discovery 步骤 | Tier 1 | Tier 2 | Tier 3 |
|---|:---:|:---:|:---:|
| 技术栈识别 | 必 | 必 | 必 |
| Style 推断（主色 + 字体 + 气质） | 必 | 必 | 必 |
| **全路由枚举** | 可选 | 建议 | **必** |
| 组件识别（文件名匹配） | 采样 | 完整 | 完整 |
| **跨文件 className 模式扫描** | 跳过 | 建议 | **必** |
| **表单 / 状态 / 动效清单** | 跳过 | 选做 | **必** |
| 六层反向归类输出沉淀计划 | 必 | 必 | 必 |
| **Tier 3 覆盖率核对表（≥80%）** | — | — | **必** |

档位选完把目标条目区间（Tier 1: 5–8 / Tier 2: 12–18 / Tier 3: 30–50+）记在工作集里，后面 step 2.5 / 3.5 决定是否跑、step 4 review 要卡区间。

---

## 技术栈识别 checklist

逐项扫，把命中结果汇总成**技术栈指纹**：

### package.json

```bash
cat "$PROJECT/package.json" 2>/dev/null | jq '{deps: .dependencies, devDeps: .devDependencies}'
```

关键字段：
- `dependencies.react` → React 项目
- `dependencies.antd` → 含 antd
- `dependencies.@radix-ui/*` 或 `devDependencies.shadcn-ui` → shadcn-radix
- `devDependencies.tailwindcss` → 含 Tailwind
- `devDependencies.vite` → Vite 构建
- `dependencies.next` → Next.js

### Tailwind 配置

```bash
ls "$PROJECT"/tailwind.config.{js,ts,cjs,mjs} 2>/dev/null
```

- 存在 → 含 Tailwind
- **结合 React 存在性决定 stack tag**：
  - React + Tailwind + antd → `react-antd-tailwind`
  - React + Tailwind，无 antd → `react-tailwind`
  - 无 React（纯 HTML + Tailwind） → `html-tailwind`
  - React + shadcn/Radix → `shadcn-radix`

### node_modules 兜底探测（若 package.json 不全）

```bash
[[ -d "$PROJECT/node_modules/antd" ]] && echo "has antd"
[[ -d "$PROJECT/node_modules/@radix-ui" ]] && echo "has radix"
[[ -d "$PROJECT/node_modules/tailwindcss" ]] && echo "has tailwind"
```

### CSS 变量 / design tokens

扫 `:root { ... }` 定义：

```bash
grep -rn ":root" "$PROJECT/src" "$PROJECT/styles" "$PROJECT/app" 2>/dev/null | head -20
```

- 有 `:root` → 抽里面的 CSS 变量作为 tokens 层候选
- 或找 `design-tokens.json` / `theme.ts` / `theme.js` 这种中心化 tokens 文件

### 技术栈指纹输出

汇总成一张表（后面写入 frontmatter 时用）：

```
stack: [react-antd-tailwind]
build: vite
css: tailwind + css-variables
```

---

## 全路由枚举 · step 0.5

**Tier 3 必做** · Tier 2 建议做 · Tier 1 可跳过。

### 为什么要做

上一版沉淀漏掉了 skill 详情 / 实践广场 / 实践详情 / 发布 / 消息 / 编辑资料 / 管理概览——根因是抽样式扫描而非全路由枚举。做过这一步后，漏路由会变成**显式缺口**而不是"忘了看"。

### 怎么做

根据路由方案，grep 以下来源之一：

```bash
# React Router (v6+): 从 createBrowserRouter / routes 配置文件找
grep -rhE "path\s*:\s*['\"]" "$PROJECT/src/router" "$PROJECT/src/routes" 2>/dev/null
grep -rhE "<Route\s+path=" "$PROJECT/src" 2>/dev/null

# 按目录约定枚举（react-router-dom v7 动态路由 / 约定式 routes）
find "$PROJECT/src/system" -maxdepth 4 -name "index.tsx" -path "*/pages/*" 2>/dev/null
find "$PROJECT/src/pages" -maxdepth 3 -name "*.tsx" 2>/dev/null

# Next.js App Router
find "$PROJECT/src/app" "$PROJECT/app" -name "page.tsx" -o -name "page.jsx" 2>/dev/null

# Next.js Pages Router
find "$PROJECT/src/pages" "$PROJECT/pages" -maxdepth 4 -name "*.tsx" -o -name "*.jsx" 2>/dev/null
```

### 产物：路由清单表

| Route | File | 职能 | page 条目候选 |
|---|---|---|---|
| `/` → `/discover` | `discovery/home/index.tsx` | 发现 / 首页 | `pages/landing/<slug>` |
| `/skills/:slug` | `skill/pages/detail/index.tsx` | 技能详情 | `pages/detail/<slug>` |
| `/practice` | `practice/pages/index.tsx` | 实践广场 | `pages/list-table/<slug>` 或 `pages/content-reader/<slug>` |
| `/practice/:id` | `practice/pages/detail/index.tsx` | 实践详情 | `pages/detail/<slug>` |
| `/practice/create` | `practice/pages/create/index.tsx` | 发布实践 | `pages/form-flow/<slug>` |
| `/publish` | `skill/pages/publish/index.tsx` | 发布技能 | `pages/form-flow/<slug>` |
| `/messages` | `message/pages/index.tsx` | 消息会话 | `pages/content-reader/<slug>` |
| `/me` | `me/pages/index.tsx` | 个人中心 | `pages/dashboard/<slug>` 或 `pages/detail/<slug>` |
| `/me/edit` | `me/pages/edit/index.tsx` | 编辑资料 | `pages/form-flow/<slug>` |
| `/admin` | `admin/pages/index.tsx` | 管理后台 | `pages/list-table/<slug>` |
| `/login` | `auth/pages/login/index.tsx` | 登录 / 注册 | `pages/auth/<slug>` |

Tier 3 必须给每个主路由至少一条 page 条目候选（覆盖率 ≥ 80%）。如果 2 条路由视觉几乎相同（比如两个不同的详情页），可以合并为 1 条 page 并在正文列出适用场景。

---

## Style 推断 checklist

### 主色

- **从 Tailwind config**：`tailwind.config.js` 的 `theme.extend.colors` / `theme.colors`
- **从 CSS 变量**：`:root { --primary: #xxx; }`
- **从 antd ConfigProvider**：`<ConfigProvider theme={{ token: { colorPrimary: '#xxx' } }}>`

### 字体

- Tailwind config 的 `theme.extend.fontFamily`
- CSS `font-family` 声明
- Google Fonts `<link rel="stylesheet" href="...?family=Inter...">`
- `@font-face` 自定义字体

### 布局密度

目测源码的 padding / margin / font-size 基线：

| 指标 | 紧凑 | 中等 | 疏朗 |
|---|---|---|---|
| 正文 font-size | 13–14 px | 14–15 px | 16+ px |
| 基础 padding | 6–8 px | 10–14 px | 16–24 px |
| 行高 | 1.4 | 1.5 | 1.6+ |

### 气质（aesthetic / mood）

综合配色 + 字体 + 布局推断，对照 taxonomy.json 的 tag_groups：

- 低饱和 + 等宽字体 + 紧凑密度 → `aesthetic: [industrial]` / `mood: [serious]`
- 低饱和 + 无衬线 + 大留白 → `aesthetic: [minimal]` / `mood: [calm]`
- 暖色 + 圆角 + 手写字体感 → `aesthetic: [organic]` / `mood: [playful]`
- 冷色 + 锐利几何 → `aesthetic: [industrial]` / `mood: [cold]`

**推断不确定时**打断问用户，不要瞎填。

---

## 组件识别

按**文件名 + 默认导出名**匹配：

### 六层候选目录

```bash
# 组件层候选
find "$PROJECT/src/components" -maxdepth 3 -name "*.tsx" -o -name "*.jsx" 2>/dev/null

# 页面层候选
find "$PROJECT/src/pages" "$PROJECT/src/app" "$PROJECT/app" -maxdepth 3 -name "*.tsx" 2>/dev/null

# 布局层（page 骨架）
find "$PROJECT" -name "Layout.tsx" -o -name "Shell.tsx" -o -name "AppShell*.tsx" 2>/dev/null
```

### 常见组件关键字

| 文件/导出名 | 资产候选 |
|---|---|
| `Button*.tsx` / `IconButton.tsx` | `components/buttons/<slug>` |
| `Input.tsx` / `TextField.tsx` / `Select.tsx` | `components/inputs/<slug>` |
| `Badge.tsx` / `Chip.tsx` / `Tag.tsx` | `components/tags/<slug>` |
| `DataTable.tsx` / `Table.tsx` + 复杂逻辑 | `blocks/display/<slug>` |
| `Card.tsx` / `StatCard.tsx` / `MetricCard.tsx` | `blocks/display/<slug>` |
| `Toolbar.tsx` / `FilterBar.tsx` | `blocks/input/<slug>` |
| `Navbar.tsx` / `Sidebar.tsx` | `blocks/nav/<slug>` |
| `Dashboard.tsx` / `Landing.tsx` / `Settings.tsx` | `pages/<bucket>/<slug>` |
| `Shell.tsx` / `AppLayout.tsx` | `pages/shell/<slug>`（页面骨架也是 page） |

---

## 跨文件 className 模式扫描 · step 2.5

**Tier 3 必做** · Tier 2 建议做 · Tier 1 跳过。

### 为什么要做

上一版漏掉了 skillhub "所有按钮 / 输入框统一黑白配色" 这种**负空间一致性**——它不在任何一个组件里，而是分布在十几个文件的 className 组合里。文件级扫描看不到这个，必须做**跨文件出现频次**统计。

### 怎么做

```bash
# 1) 拉出所有 className 字面量
grep -rhoE 'className="[^"]+"' "$PROJECT/src" 2>/dev/null \
  > /tmp/classnames.txt

# 2) 统计重复的原始组合（完全一致的类字符串）
sort /tmp/classnames.txt | uniq -c | sort -rn | head -40

# 3) 针对性搜索候选全局模式
grep -rE 'bg-\[#1a1a1a\]|bg-slate-900|bg-gray-900' "$PROJECT/src" \
  | awk -F: '{print $1}' | sort -u | wc -l    # 统一深色 CTA 出现的独立文件数

grep -rE 'focus:border-[a-z]+-\d+.*focus:ring-' "$PROJECT/src" \
  | awk -F: '{print $1}' | sort -u | wc -l    # 统一 focus 样式

grep -rE 'rounded-(xl|2xl)' "$PROJECT/src" | wc -l    # 软圆角家族

grep -rE 'active:scale-9\d' "$PROJECT/src" | wc -l    # 统一 tap 缩放
```

### 模式阈值

**是全局模式** ⇔ className 组合（或其核心关键字）**同时满足**：
- 出现 ≥ 5 次
- 横跨 ≥ 3 个文件
- 语义上"做同一件事"（都是 CTA 底色 / 都是 focus / 都是 tap 缩放 ...）

### 产物：全局模式清单

| 模式 | 出现次数 | 文件数 | 该沉淀为 |
|---|---|---|---|
| `bg-[#1a1a1a] text-white active:scale-95` | 12 | 8 | `components/buttons/dark-primary-cta` |
| `border-gray-200 focus:border-teal-300 focus:ring-2 focus:ring-teal-100 rounded-xl` | 9 | 6 | `components/inputs/soft-teal-focus` |
| `rounded-2xl border border-gray-200 bg-white hover:border-teal-200 hover:shadow-md` | 7 | 5 | `tokens/radius/soft-card` 或直接进 block |
| `text-xs font-bold uppercase tracking-wider text-gray-400` | 11 | 7 | `tokens/typography/meta-caps`（可选） |

**Tier 3 要求**：至少产出 3 条全局模式，每条都要在沉淀计划中对应一条 token 或 component 条目。

---

## 表单 / 状态 / 动效清单 · step 3.5

**Tier 3 必做** · Tier 2 选做 · Tier 1 跳过。

### 表单清单

```bash
# 找所有表单
grep -rlE '<form\b|onSubmit=' "$PROJECT/src" 2>/dev/null
```

产出：

| 表单 | 路由 | 字段类型 | 视觉特征 | 沉淀为 |
|---|---|---|---|---|
| 登录 / 注册 | `/login` | email + password + toggle | 分屏 + slate 渐变 logo | `blocks/form/auth-split-form` |
| 发布实践 | `/practice/create` | title + markdown editor + skill picker | 宽正文 + editor 卡片 | `blocks/form/long-article-compose` |
| 发布技能 | `/publish` | file upload + metadata | 拖拽区 + 进度 | `blocks/form/upload-archive` |
| 编辑资料 | `/me/edit` | nickname + avatar + bio | 两列 + avatar picker | `blocks/form/profile-edit` |

### 状态清单

```bash
# loading
grep -rlE 'animate-pulse|<Spin\s|isLoading' "$PROJECT/src" 2>/dev/null

# empty
grep -rlE '<Empty\b|"暂无|"未找到|"还没有' "$PROJECT/src" 2>/dev/null

# error
grep -rlE '"加载失败|bg-rose-|text-rose-|role="alert"' "$PROJECT/src" 2>/dev/null
```

产出：

| 状态 | 位置 | 视觉特征 | 沉淀为 |
|---|---|---|---|
| Loading skeleton | 首页技能网格 | `h-48 animate-pulse rounded-2xl` | `blocks/feedback/skeleton-card` |
| Empty 无搜索结果 | 发现页 | `border-dashed + Box icon` | `blocks/feedback/empty-state` |
| Error 加载失败 | 全局 | `bg-rose-50 text-rose-700 border` | `components/indicators/error-banner` |
| Pulse dot 正常 | footer | emerald + glow shadow + animate-pulse | `components/indicators/pulse-dot` |

### 动效清单

```bash
# CSS keyframes
grep -rnE '@keyframes\s+\w+' "$PROJECT/src" 2>/dev/null

# framer-motion 模式
grep -rnE 'whileHover=|whileTap=|whileInView=|initial=|animate=' "$PROJECT/src" 2>/dev/null | head -40

# Tailwind animate 工具
grep -rhoE 'animate-\[[^\]]+\]|animate-pulse|animate-spin' "$PROJECT/src" 2>/dev/null | sort -u
```

产出：

| 名称 | 来源 | 类型 | 沉淀到 |
|---|---|---|---|
| `flow-right` 14s linear | `index.less:42` | CSS keyframe | `tokens/motion/<slug>` |
| `fadeIn` 4px translateY | `index.less:49` | CSS keyframe | `tokens/motion/<slug>` |
| `shimmer` 骨架 | `index.less:37` | CSS keyframe | `tokens/motion/<slug>` |
| `whileHover y:-4 duration:0.2` | `home:463` | framer-motion | `tokens/motion/<slug>` |
| `whileTap scale:0.97` | `home:76` | framer-motion | `tokens/motion/<slug>` |
| SVG border trace `stroke-dashoffset` | `home:34` | SVG + ResizeObserver | `components/buttons/<slug>` |

---

## 写 page 条目前的硬规矩：**必须通读 JSX**

**惨痛教训**（2026-04-24 · skillhub tier3 第一次交付时犯过）：只读了 `skill/pages/detail/index.tsx` 文件头 150 行（state / hooks / fetching）就开始写沉淀条目，结果把"长文 + sidebar"的刻板印象套上去，漏了 **安装命令条 / SUMMARY box / SKILL.md pill / 元信息矩阵 / timeline 评论 / rounded-3xl compose** 6 处关键结构。用户一截图比对就发现差异很大。

### 硬规矩

Tier 2 / Tier 3 写 page / 复杂 block 条目前，**必须满足以下全部**：

1. **完整读过 `return (` 到文件末尾的 JSX**。不能只读 state/hooks。
2. **识别出至少 3 处"本页独有的视觉结构"**（breadcrumb / install bar / stats grid / timeline / ...），写进 README.md 的"页面骨架"或"视觉要点"节。
3. **列出所有 `className` 里的具体数值**（`rounded-lg` 不是 `rounded-xl` / `w-1.5 h-6 bg-blue-500` 等），而不是写"圆角 / 蓝色竖条"这种模糊描述。
4. **不允许描述"未在源码出现"的元素**（比如不要给 detail 页写"使用此 Skill 黑底 CTA"如果源码里没有）。

### 文件长度分级处理

| 文件行数 | 建议读法 |
|---|---|
| ≤ 200 | 一次全读 |
| 200–500 | 读 state + JSX（分 2 次读）|
| 500–1000 | 读 state（头 100 行）+ JSX 分 2-3 段 |
| > 1000 | 分段 + 优先读最长的 return 块，state 只扫字段名 |

**不允许"读头就开写"**。

### 自检问题（写 page README 前自问）

- [ ] 这个页面第一眼的"主要视觉块"是什么？我在 README 里写到它了吗？
- [ ] 这个页面的"主 CTA"在哪里？不是我凭印象猜的吗？
- [ ] 这个页面有没有"意想不到"的模式（install bar / breadcrumb / timeline / ... ）？
- [ ] 如果用户拿我写的 README 逆向还原出一页，会和真实页差到哪一步？

答不上 → 回去读源码。

---

## 层级反向归类表

把扫到的文件映射到资产层级：

| 源文件路径 | 归到资产 | 说明 |
|---|---|---|
| `tailwind.config.{js,ts}` 的主色 + `:root` CSS vars | `tokens/palettes/<slug>` | 提色板到 token |
| `theme.ts` 的 fontFamily 定义 | `tokens/typography/<slug>` | 字体对到 token |
| `src/components/Button.tsx` | `components/buttons/<slug>` | 单件交互元素 |
| `src/components/DataTable.tsx` | `blocks/display/<slug>` | 多元素组合 |
| `src/components/Toolbar.tsx` | `blocks/input/<slug>` | 交互组合 |
| `src/pages/Landing.tsx` | `pages/landing/<slug>` | 整页 |
| `src/pages/Dashboard.tsx` | `pages/dashboard/<slug>` | 整页 |
| 整个项目视觉主张 | `styles/<bucket>/<slug>` | 风格聚合 |
| 整个项目产品定位 | `products/<slug>` | 产品描述 |

**注意**：不是每一层都必须建。小项目可能只值得沉淀 1 token + 1 style；大项目可能 6 层全填。由 AI 分析后提建议，用户在步骤 4 review 决定。**条目数必须落在档位目标区间内**（Tier 1: 5–8 / Tier 2: 12–18 / Tier 3: 30–50+）。

### refs 关系

沉淀出的条目必须组织成 DAG：

```
products/<slug>
  → refs.style: styles/<bucket>/<slug>

styles/<bucket>/<slug>
  → uses:
    - blocks/display/<slug>
    - components/buttons/<slug>
  → refs.tokens.palette: tokens/palettes/<slug>
  → refs.tokens.typography: tokens/typography/<slug>

blocks/display/<slug>
  → refs.tokens.palette: tokens/palettes/<slug>

components/buttons/<slug>
  → refs.tokens.palette: tokens/palettes/<slug>
```

---

## 输出沉淀计划

把上面的识别结果整理成沉淀计划，按**依赖拓扑序**排列，每条标注**来源文件路径**：

```
沉淀计划：
  目标：把 acme-admin 的冷工业风沉淀到 vault
  起点：from-project ($PROJECT = ~/Projects/acme-admin)
  技术栈指纹：react-antd-tailwind + vite + css-variables

  新增条目（依赖拓扑序）：
    1. tokens/palettes/acme-cold-steel
       来源：tailwind.config.ts:14-32 + src/styles/tokens.css:1-40

    2. tokens/typography/acme-mono-pair
       来源：tailwind.config.ts:34-48 + src/styles/tokens.css:42-55

    3. components/buttons/acme-ghost-btn
       来源：src/components/Button.tsx

    4. blocks/display/acme-metric-card
       来源：src/components/MetricCard.tsx

    5. blocks/input/acme-toolbar
       来源：src/components/Toolbar.tsx

    6. styles/saas-tool/acme-cold-industrial
       来源：整个项目的视觉聚合

    7. products/acme-admin
       来源：整个项目定位 + README.md

  依赖关系：
    acme-admin → acme-cold-industrial →
      [acme-metric-card, acme-toolbar, acme-ghost-btn, acme-cold-steel, acme-mono-pair]
    acme-metric-card → acme-cold-steel
    acme-toolbar → acme-cold-steel
    acme-ghost-btn → acme-cold-steel
    acme-cold-industrial → acme-cold-steel + acme-mono-pair

  来源溯源：
    项目根：~/Projects/acme-admin
    关键文件：tailwind.config.ts, src/components/*.tsx, src/styles/tokens.css
```

---

## 汇入共享主流程

沉淀计划就绪后：

- **Tier 1 / 2** → 直接汇入 [shared-workflow.md 步骤 2](shared-workflow.md#步骤-2--授权-auto-fill)
- **Tier 3** → 汇入前先完成**覆盖率核对表**（见 [depth-tiers.md#Tier-3-硬下限-checklist](depth-tiers.md)）：
  - 主路由 / 全局模式 / 表单 / 状态 覆盖率都 ≥ 80% 才可继续
  - 未达标 → 打断让用户决策：补齐缺口 / 降到 Tier 2 / 手动放行

接下来的 8 步（授权 auto-fill → 生成完整方案 → 整批 review → path.json 分叉 → 逐条写入 → 双仓 commit → 沉淀报告）**由 shared-workflow 统一处理**，本分支不再参与。

落盘 `source.md` 时，填入：

```markdown
# 素材溯源 · <主题>

## 项目路径
- $PROJECT = ~/Projects/acme-admin
- 技术栈指纹：react-antd-tailwind + vite + css-variables

## 关键源文件
- tailwind.config.ts（第 14-48 行：color + fontFamily）
- src/styles/tokens.css（第 1-55 行：CSS variables）
- src/components/Button.tsx（20 行，基础按钮）
- src/components/MetricCard.tsx（80 行，数据卡片）
- src/components/Toolbar.tsx（60 行，过滤工具栏）

## 识别的技术栈
react-antd-tailwind
```

---

## 典型流程示例

假场景：用户说 `沉淀 ~/Projects/acme-admin`。

**1. 输入解析**

```bash
PROJECT=/Users/links/Projects/acme-admin
```

**2. 技术栈识别**

```bash
jq '.dependencies' "$PROJECT/package.json"
# → react@18, antd@5, react-router-dom@6

ls "$PROJECT"/tailwind.config.* 
# → tailwind.config.ts 存在

# 结论：stack = react-antd-tailwind, build = vite
```

**3. Style 推断**

打开 `tailwind.config.ts`：
```ts
colors: {
  primary: '#0EA5E9',       // 冷蓝
  slate: { ... },           // 冷灰
},
fontFamily: {
  sans: ['Inter', ...],
  mono: ['IBM Plex Mono', ...],
},
```

推断：
- 主色：冷蓝 + 冷灰
- 字体：Inter + IBM Plex Mono
- 布局密度：看 `src/components/DataTable.tsx` 的 padding = `px-3 py-2` → 紧凑
- aesthetic: [industrial], mood: [serious, cold]

**4. 组件识别**

```bash
ls $PROJECT/src/components/
# Button.tsx, DataTable.tsx, MetricCard.tsx, Toolbar.tsx, Sidebar.tsx, ...
```

匹配：
- `Button.tsx` → `components/buttons/acme-ghost-btn`
- `MetricCard.tsx` → `blocks/display/acme-metric-card`
- `Toolbar.tsx` → `blocks/input/acme-toolbar`
- `Sidebar.tsx` → `blocks/nav/acme-sidebar`

**5. 输出沉淀计划**

如前节示例。贴给用户确认入口识别是否完整，允许用户：
- 删掉觉得不值得沉淀的条目（如 "组件太普通，不沉 button"）
- 新增漏掉的条目（如 "还有一个 EmptyState 也想沉"）

**6. 汇入 shared-workflow**

用户确认后调 [shared-workflow.md 步骤 2](shared-workflow.md#步骤-2--授权-auto-fill)。
