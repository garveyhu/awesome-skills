# Tokens · 原语

## 层定义

**设计原语 / 资源**：没有交互形态的值或资源。调色板、字体对、动效曲线、边框、阴影、图标集……Token 只是一串值或一组资源，不带 DOM、不带状态，仅供上层组件引用。

## 二级场景桶

| 桶 | 说明 |
|---|---|
| `palettes` | 调色板：主色、中性、语义色整套 |
| `typography` | 字体体系：字体对、字号阶梯、行高规则 |
| `motion` | 动效：duration / easing 曲线 / 过渡预设 |
| `border` | 边框体系：宽度、样式、圆角阶梯 |
| `shadow` | 阴影层次：sm / md / lg / xl / inner |
| `gradient` | 渐变配方：主背景、装饰块用的渐变组合 |
| `iconography` | 图标集 / 图标风格：描边宽度、尖锐 vs 圆润 |

## 收录边界

**先问一句**：要不要产出新实现？不 → Products；要 → 按粒度 整语言 → 整页 → 整段 → 单件 → 值。

Tokens 位于第五层（「值」）。和相邻层的边界：

- **Tokens ↔ Components**：Component 有交互状态和 DOM；Token 只是值或资源。判定：一段可 `JSON.parse` 的配置 / 一组 SVG → Token；带 hover / focus 的控件 → Component
- Token 不引用任何其他层，只被上层引用
- Token 必须带 `## Tokens` 章节，里面一个可 `JSON.parse` 的代码块——sync 脚本直接喂给网站
- 不要在 Token 里放组件代码；有代码就说明它还不够「原语」

## 命名约定

- 二级目录 kebab-case：`palettes`、`typography`、`motion`
- **三级 namespace 强制**（见 [../README.md · Namespace 子目录](../README.md#namespace-子目录强制)）：
  - 单文件：`tokens/<bucket>/<namespace>/<slug>.md`
  - 多文件：`tokens/<bucket>/<namespace>/<slug>/README.md`，id 取文件夹路径
  - `<namespace>` = product 短名（如 `acme` / `skillhub`）；通用件归 `_shared`
- slug 全程 kebab-case，如 `slate-cyan-ice.md`、`ibm-plex-duo.md`
