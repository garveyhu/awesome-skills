# Atoms

## 层定义

**原子件**：单个交互元素或展示元素。不能再拆分出独立意义，但自身有明确的交互/视觉特征。

## 二级桶

| 桶 | 说明 |
|---|---|
| `buttons` | 按钮：primary / ghost / text / icon-only / 方型 / 胶囊 |
| `inputs` | 输入框：Text / Textarea / Number / Search / 带前后缀 |
| `selects` | 选择器：Select / Cascader / 日期时间 / 颜色 |
| `toggles` | 开关类：Switch / Checkbox / Radio / SegmentedControl |
| `tags-badges` | 标签徽章：Tag / Chip / Badge / Pill |
| `overlays` | 浮层原子：Tooltip / Popover / Dropdown 触发 |
| `indicators` | 状态指示器：Loading / Spinner / Progress / Dot |
| `avatars-icons` | 头像 / 图标：Avatar / IconButton |
| `typography-atoms` | 文字原子：Heading / Paragraph / Caption / Link |

## 收录边界

- atom 只能引用 primitives，不引用 atoms / composites
- atom 的代码片段必须是**一个**组件，不能是一组
- 跨业务的通用元素才收：某个项目里定制的"导出按钮"不收，它应该是 composite 的一部分

## 命名约定

- 二级目录 kebab-case：`buttons`、`inputs`、`tags-badges`
- 条目文件名 kebab-case：`primary-solid.md`、`ghost-outline.md`
