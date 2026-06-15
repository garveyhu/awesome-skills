# Components · 组件

## 层定义

**单一可复用的交互原子**：一个 Component 是一件独立的交互/展示元素——Button / Input / Tag / Modal 触发器等。它有明确的交互形态，但不能再拆分出独立意义。

## 二级场景桶

| 桶 | 说明 |
|---|---|
| `buttons` | 按钮：primary / ghost / text / icon-only / 方型 / 胶囊 |
| `inputs` | 输入框：Text / Textarea / Number / Search / 带前后缀 |
| `selects` | 选择器：Select / Cascader / Combobox |
| `toggles` | 开关类：Switch / Checkbox / Radio / SegmentedControl |
| `pickers` | 选取器：日期 / 时间 / 颜色 / 文件 |
| `tags-badges` | 标签徽章：Tag / Chip / Badge / Pill |
| `avatars-icons` | 头像 / 图标：Avatar / IconButton / 圆形头像组 |
| `indicators` | 状态指示器：Loading / Spinner / Progress / Dot |
| `overlays` | 浮层触发：Tooltip / Popover / Dropdown / Menu 触发 |
| `typography-atoms` | 文字原子：Heading / Paragraph / Caption / Link |

## 收录边界

**先问一句**：要不要产出新实现？不 → Products；要 → 按粒度 整语言 → 整页 → 整段 → 单件 → 值。

Components 位于第四层（「单件」）。和相邻层的边界：

- **Components ↔ Blocks**：Component 只是一件；Block 是含多件 Component 的一段 section。判定：如果拎出来就是孤零零一件控件，归 Components；如果它要和其他控件协作才能解释清楚，归 Blocks
- **Components ↔ Tokens**：Component 有交互形态（hover / focus / disabled）；Token 只是值。判定：有状态 / 有 DOM → Component；只是一串值 / 一组颜色 → Token
- Component 只能引用 Tokens，不引用其他 Components 或 Blocks
- Component 的代码片段必须是**一个**组件，不能是一组
- 跨业务的通用控件才收；某个项目里一次性的定制（如「导出按钮」），那是 Block 的一部分

## 命名约定

- 二级目录 kebab-case：`buttons`、`inputs`、`tags-badges`
- **三级 namespace 强制**（见 [../README.md · Namespace 子目录](../README.md#namespace-子目录强制)）：
  - 单文件：`components/<bucket>/<namespace>/<slug>.md`
  - 多文件：`components/<bucket>/<namespace>/<slug>/README.md`，id 取文件夹路径
  - `<namespace>` = product 短名（如 `acme` / `skillhub`）；通用件归 `_shared`
- slug 全程 kebab-case，如 `ghost-button.md`、`segmented-control.md`
