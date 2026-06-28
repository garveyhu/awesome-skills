---
title: 晋升队列 · 待审批候选
type: candidates
---

# 晋升队列 · 待审批候选

> `mp.py distill` 自动写这里，**不直接改 `00-RULES`**。审批：把要的勾成 `[x]`，跑 `/memory-palace review`（或 `mp.py promote`）落地。
> 留 `[ ]` = 暂缓；想否决就删掉那条（留痕 `DREAMS.md`）。

## 格式（promote 解析约定）

```text
- [ ] <一句话候选> <!--cand {"id":"c1","action":"ADD","dest":"00-RULES/preferences.md","type":"preference","scope":"global","freq":2,"score":0.61,"conf":"high"} -->
  - 证据: <来源 session / journal 日期>
```

- `action`: `ADD` / `UPDATE`(dest 指到具体文件) / `NOOP`(已存在，忽略)
- `dest`: 落点（`00-RULES/…` 跨项目铁律 · `01-PROJECTS/<名>/…` 项目级）
- `freq`: 证据次数（跨项目铁律建议 ≥2 才进 00-RULES）· `score`: 六维分 · `conf`: 置信度

---

## 🟡 待审批（distill 尚未首次运行）

<!-- distill 会把候选追加到这一节下方。 -->
