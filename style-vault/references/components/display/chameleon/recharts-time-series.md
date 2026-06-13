---
id: components/display/chameleon/recharts-time-series
type: component
name: 主题化 recharts 折线时序图
description: recharts 折线时序封装 — 半透明黑网格 + paper 底 tooltip + themeable primary 线色 + 单/双 Y 轴叠加量纲差异指标 + 空态兜底
platforms:
- web
theme: light
tags:
  aesthetic:
  - industrial
  - minimal
  mood:
  - serious
  stack:
  - shadcn-radix
uses:
- tokens/border/waveflow/translucent-stone-system
preview: /preview/components/display/chameleon/recharts-time-series
---

# 主题化 recharts 折线时序图

> Chameleon dashboard / cost / eval 等页面共用的 recharts 折线时序封装（`TimeSeriesChart`），统一了此前各页内联的 `LineChart`。**signature**：① 网格用半透明黑（`rgb(0 0 0 / 6%)`）而非实色——任何背景上都和谐；② tooltip 底色走 `var(--color-paper)` 跟主题；③ 线色由 `series.color` 传入，推荐 `var(--color-primary-600)` 随主题变；④ 双 Y 轴叠加量纲差异大的指标（成本 + token 同图）；⑤ 空态文字兜底。

## 视觉特征

- 空态：`flex items-center justify-center text-sm text-stone-400`（14px 暖灰），默认文案「暂无数据」，撑满给定 `height`
- 容器：`<div style={{ height }}>` 包 `ResponsiveContainer width="100%" height="100%"`，`height` 默认 256
- **CartesianGrid**：`strokeDasharray="3 3"` + `stroke="rgb(0 0 0 / 6%)"`（**半透明黑虚线网格**——关键签名，不用实色 stone）
- **XAxis / YAxis**：`stroke="#999"` + `fontSize={11}`（中灰轴线 + 11px 刻度）
- **双轴**：当任一 series 标 `axis="right"` → 左轴 `yAxisId="left"` + 右轴 `yAxisId="right" orientation="right"`（右轴可单独 `rightTickFormatter`）；不传 axis 时单轴，向后兼容
- **Tooltip**：`contentStyle = { background: 'var(--color-paper)', border: '1px solid rgb(0 0 0 / 10%)', borderRadius: 8, fontSize: 12 }`（paper 底 + 半透明黑边 + 8px 圆角 + 12px 字）
- **Line**：`type="monotone"` + `strokeWidth={2}` + `dot={false}`（平滑单调曲线 / 2px 线宽 / **不画数据点**），`stroke = series.color`（建议 `var(--color-primary-600)`）

## Tokens

局部图表 token：

```json
{
  "chart": {
    "height": 256,
    "grid": { "dash": "3 3", "stroke": "rgb(0 0 0 / 6%)" },
    "axis": { "stroke": "#999999", "fontSize": 11 },
    "tooltip": {
      "background": "var(--color-paper)",
      "border": "1px solid rgb(0 0 0 / 10%)",
      "radius": 8,
      "fontSize": 12
    },
    "line": { "type": "monotone", "strokeWidth": 2, "dot": false, "color": "var(--color-primary-600)" },
    "empty": { "text": "#a8a29e", "fontSize": 14 }
  }
}
```

## 核心代码

```tsx
<ResponsiveContainer width="100%" height="100%">
  <LineChart data={[...data]}>
    <CartesianGrid strokeDasharray="3 3" stroke="rgb(0 0 0 / 6%)" />
    <XAxis dataKey={xKey} tickFormatter={xTickFormatter} stroke="#999" fontSize={11} />
    <YAxis {...(hasRight ? { yAxisId: 'left' } : {})} stroke="#999" fontSize={11} />
    {hasRight && (
      <YAxis yAxisId="right" orientation="right" stroke="#999" fontSize={11} tickFormatter={rightTickFormatter} />
    )}
    <Tooltip contentStyle={{
      background: 'var(--color-paper)', border: '1px solid rgb(0 0 0 / 10%)', borderRadius: 8, fontSize: 12,
    }} />
    {series.map(s => (
      <Line key={s.dataKey}
        {...(hasRight ? { yAxisId: s.axis === 'right' ? 'right' : 'left' } : {})}
        type="monotone" dataKey={s.dataKey} name={s.name}
        stroke={s.color} strokeWidth={2} dot={false} />
    ))}
  </LineChart>
</ResponsiveContainer>

// 空态
if (!data?.length) return (
  <div className="flex items-center justify-center text-sm text-stone-400" style={{ height }}>
    {empty}
  </div>
);
```

## 适配指南

- 线色传 `var(--color-primary-600)` 让图随主题色变；多 series 时其余用 sky/violet/amber 等区分色
- 量纲差异大的指标（调用数千级 + 成本几元级）用双轴：成本 series 标 `axis="right"` + `rightTickFormatter` 格式化货币
- `dot={false}` 是默认——数据点多时画点会糊；点稀疏（<10）想强调可单独开
- 网格 `rgb(0 0 0 / 6%)` 不要换实色——它在暖纸/纯白底上都不抢线，是封装的核心妥协

## 反模式

- ❌ 网格用 `stroke-stone-200` 实色——在暖纸底上偏重，破坏「半透明克制网格」签名
- ❌ tooltip 用 `bg-white` 硬编码——主题切换时与 paper 底脱节，用 `var(--color-paper)`
- ❌ `strokeWidth` 用 1 或 3——全站统一 2px；1 太细 3 太重
- ❌ 量纲差异大却用单轴——小量纲 series 被压成贴底直线，必须 `axis="right"` 分轴
