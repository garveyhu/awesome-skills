# 可复用图表组件

**纯 CSS/DOM 画的图**——不需要 Excel、Visio、图表库，改数据就是改文本，且和正文字体统一。

需要时把 CSS 和 HTML 一起复制进模板。所有组件都已带 `page-break-inside: avoid`。

---

## 1. 竞争象限图

用于产品定位、方案对比。

```css
.quad { position: relative; height: 58mm; border: .75px solid #d5d5d5; page-break-inside: avoid; }
.quad .ax { position: absolute; background: #d5d5d5; }
.quad .ax.v { left: 50%; top: 5mm; bottom: 5mm; width: .75px; }
.quad .ax.h { top: 50%; left: 5mm; right: 5mm; height: .75px; }
.quad .lb { position: absolute; font-size: 8pt; color: #444; }
.quad .lb.t { top: 2mm; left: 50%; transform: translateX(-50%); }
.quad .lb.b { bottom: 2mm; left: 50%; transform: translateX(-50%); }
.quad .lb.l { left: 2mm; top: 50%; transform: translateY(-50%); }
.quad .lb.r2 { right: 2mm; top: 50%; transform: translateY(-50%); }
.quad .pt { position: absolute; font-size: 8.5pt; color: #444; transform: translate(-50%,-50%); white-space: nowrap; }
.quad .pt.me { border: 1.2px solid #1a1a1a; background: #fff; font-weight: 700; color: #1a1a1a; padding: 1.2mm 3mm; }
```

```html
<figure>
  <div class="quad">
    <div class="ax v"></div><div class="ax h"></div>
    <div class="lb t">纵轴上端</div><div class="lb b">纵轴下端</div>
    <div class="lb l">横轴左端</div><div class="lb r2">横轴右端</div>
    <div class="pt" style="left:30%;top:27%">竞品 A</div>
    <div class="pt me" style="left:71%;top:71%">我们</div>
  </div>
  <figcaption>图 5-1　产品定位象限分析</figcaption>
</figure>
```

**用法要点**：把自己放进一个**空象限**才有说服力；如果四个象限都挤满了，说明这两个维度选错了，换维度。

---

## 2. 柱状图

三五根柱子的趋势对比。超过 8 根就该考虑表格。

```css
.bars { display: flex; align-items: flex-end; gap: 14mm; height: 40mm; padding: 0 12mm; border-bottom: .75px solid #1a1a1a; }
.bar-col { flex: 1; display: flex; flex-direction: column; justify-content: flex-end; height: 100%; }
.bar { width: 100%; background: #d9d9d6; border: .75px solid #444; position: relative; }
.bar.dark { background: #444; }
.bar .v { position: absolute; top: -6.5mm; left: 50%; transform: translateX(-50%); font-family: var(--mono); font-size: 9pt; font-weight: 600; white-space: nowrap; }
.bar-labels { display: flex; gap: 14mm; padding: 2mm 12mm 0; }
.bar-labels span { flex: 1; text-align: center; font-size: 9pt; color: #444; }
```

```html
<figure>
  <div class="bars">
    <div class="bar-col"><div class="bar" style="height:6.2%"><span class="v">18.5 万</span></div></div>
    <div class="bar-col"><div class="bar" style="height:32.5%"><span class="v">97.6 万</span></div></div>
    <div class="bar-col"><div class="bar dark" style="height:100%"><span class="v">300 万</span></div></div>
  </div>
  <div class="bar-labels"><span>第一年</span><span>第二年</span><span>第三年</span></div>
  <figcaption>图 10-1　三年营业收入趋势（单位：元）</figcaption>
</figure>
```

**`height` 百分比 = 该值 / 最大值**。改数据时记得同步改高度，否则图和数字对不上——这是最容易漏的地方。

---

## 3. 时间线

实施计划、里程碑。正式公文里建议改用表格（更规整），提案里用时间线更好看。

```css
.timeline { margin: 4mm 0 5mm; border-left: 2px solid rgba(22,22,22,.22); padding-left: 6mm; }
.tl-item { position: relative; margin-bottom: 4mm; page-break-inside: avoid; }
.tl-item::before {
  content: ""; position: absolute; left: -7.9mm; top: 1.8mm;
  width: 3.6mm; height: 3.6mm; border-radius: 50%;
  background: #fff; border: 2px solid rgba(22,22,22,.22);
}
.tl-item.hot::before { background: var(--accent); border-color: var(--accent); }
.tl-item .when { font-family: var(--mono); font-size: 8pt; font-weight: 700; color: var(--accent); }
.tl-item .note { font-size: 8.2pt; color: #746f66; }
```

```html
<div class="timeline">
  <div class="tl-item hot">
    <div class="when">第 1~3 月 · 阶段名</div>
    <div>主要工作内容</div>
    <div class="note">交付标准：可验证的量化目标</div>
  </div>
</div>
```

`.hot` 标记当前/关键阶段——**一条时间线上最多标两个**，全标等于没标。

---

## 4. 数据块（Stat）

关键指标的视觉锚点。**只用在执行摘要或章节开头**，全文不超过两组。

```css
.stats { display: grid; grid-template-columns: repeat(4,1fr); gap: 3mm; page-break-inside: avoid; }
.stat { background: #fffdf7; border: 1px solid rgba(22,22,22,.13); border-radius: 4px; padding: 4mm 3.5mm; }
.stat .v { font-family: var(--mono); font-size: 21pt; font-weight: 700; line-height: 1.05; letter-spacing: -.04em; font-variant-numeric: tabular-nums; }
.stat .v small { font-size: 10pt; font-weight: 600; margin-left: .5mm; }
.stat .k { margin-top: 1.5mm; font-size: 7.8pt; color: #746f66; line-height: 1.5; }
.stat.accent { border-color: rgba(18,128,92,.35); background: rgba(18,128,92,.10); }
.stat.accent .v { color: var(--accent); }
```

```html
<div class="stats">
  <div class="stat"><div class="v">1.8<small>万亿</small></div><div class="k">市场规模<br>2025 年，同比 +42%</div></div>
  <div class="stat accent"><div class="v">50<small>万</small></div><div class="k">可获得市场</div></div>
</div>
```

四个一排最稳。`.accent` 标出最重要的那一个——**只标一个**。

---

## 5. 长表格跨页时重复表头

超过一页的表格，加上这个让每页都带表头：

```css
thead { display: table-header-group; }
tfoot { display: table-footer-group; }
```

同时把该表的 `page-break-inside: avoid` 去掉（否则它会试图挤进一页，反而在页尾留大片空白）。
