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

**注意**：不是每一层都必须建。小项目可能只值得沉淀 1 token + 1 style；大项目可能 6 层全填。由 AI 分析后提建议，用户在步骤 4 review 决定。

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

沉淀计划就绪后，**汇入 [shared-workflow.md 步骤 2](shared-workflow.md#步骤-2--授权-auto-fill)**。

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
