# Primitives

## 层定义

**设计原语**：最细粒度的 token。不绑定任何组件，只定义一个维度的值（色、字、间距、圆角等）。

## 二级桶

| 桶 | 说明 |
|---|---|
| `palettes` | 色板：主色、中性色、语义色整套 |
| `typography` | 字体体系（三级：见下） |
| `spacing` | 间距阶梯：4 / 8 / 12 / 16 / 24 ... |
| `radius` | 圆角阶梯：0 / 2 / 4 / 8 / 16 / full |
| `shadow` | 阴影层次：sm / md / lg / xl / inner |
| `motion` | 动效：duration / easing 曲线 |
| `border` | 边框体系：宽度、样式 |
| `gradient` | 渐变配方 |
| `texture` | 纹理 / 底纹：noise / grid / dot |
| `iconography` | 图标风格：描边宽度、尖锐 vs 圆润 |
| `focus-ring` | 聚焦环：ring 宽度、颜色、offset |
| `cursor` | 自定义光标 |

## typography 三级

| 子桶 | 说明 |
|---|---|
| `primitives/typography/fonts` | 单个字体：Inter / Noto Sans SC / Source Serif |
| `primitives/typography/pairs` | 字体对：显示字 + 正文字搭配 |
| `primitives/typography/scales` | 字号阶梯：text-xs ~ text-7xl 的比例 |

## 收录边界

- primitive 不引用任何其他层，只被上层引用
- primitive 必须带 `## Tokens` 章节，里面一个可 `JSON.parse` 的代码块——sync 脚本会直接把它喂给网站
- 不要在 primitive 里放组件代码；有代码就说明不够"原语"

## 命名约定

- 二级目录 kebab-case：`palettes`、`typography`、`focus-ring`
- 条目文件名 kebab-case：`admin-slate.md`、`warm-cream.md`
