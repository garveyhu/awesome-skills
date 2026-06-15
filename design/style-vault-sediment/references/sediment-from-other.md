# sediment-from-other · 兜底路由

**适用触发**：用户说 "4) 其他 / 不确定"，或者描述里同时混了多种起点线索（"项目 + 参考网站"），或者什么都没说清。

**核心能力**：**反问 2–3 个是/否问题**识别真实起点，路由到 from-project / from-web / from-scratch 之一；或给混合场景的手工合并建议。

---

## 反问逻辑

按顺序三问，任一个 Y 就路由。都 N 就降级。

### 问 1 · 有没有源码 / 项目路径？

```
你有本地项目路径或源码仓库可以让我直接扫吗？
  Y） 路径是 <...>
  N） 没有
```

- Y → 路由到 [sediment-from-project.md](sediment-from-project.md)，让用户给路径

### 问 2 · 有没有 URL / 截图 / 设计稿？

```
有可以参考的 URL、截图或设计稿（Figma / Dribbble / 一张图）吗？
  Y） <URL 或路径>
  N） 没有
```

- Y → 路由到 [sediment-from-web.md](sediment-from-web.md)，让用户提供素材

### 问 3 · 只有想法 / 描述？

```
你心里有一个风格想法（像 xxx 那样 / 冷感 / 暖感），希望对着聊出来吗？
  Y） 我来描述
  N） 啥都没有
```

- Y → 路由到 [sediment-from-scratch.md](sediment-from-scratch.md)

### 都说 N（三问都否）

无法推进，直接终止：

```
暂时没有可以入手的起点。推进沉淀需要至少一种入口：
  - 源码项目路径
  - URL / 截图 / 设计稿
  - 一个具体的风格想法

有其中之一再叫我。
```

**不强行推进**、**不瞎猜**。

---

## 混合场景

用户给的东西**跨多个起点**时，按下面指引合并——**主路径还是走其中一个**，其它作辅助。

### 项目 + 参考网站

**场景**：用户说"沉淀 `~/Projects/acme-admin`，但主色想改成 Linear 的那个冷蓝"。

**处理**：

1. **主路径走 [from-project](sediment-from-project.md)**：扫项目结构、识别组件、反向归类。
2. **参考网站作"色板来源"**：在 from-project 的"Style 推断"步骤**强制插入 Linear 的色板抽取**（走一小步 [from-web](sediment-from-web.md) 的视觉分析，只取 color tokens）。
3. **沉淀计划里的 token 条目标注来源**：
   ```
   tokens/palettes/acme-linear-blue
     来源混合：
       - 项目 tailwind.config.ts（提取结构）
       - https://linear.app（主色替换）
   ```
4. `source.md` 同时记录项目路径 + 参考 URL。
5. 其它层（block / style / product）按 from-project 正常走。

**给用户的 prompt**：

```
理解为混合场景：
  - 骨架从项目 ~/Projects/acme-admin 来
  - 主色从 Linear 来
  
我按这个拼。如果希望更大范围参考 Linear（比如字体也换），告诉我要替换哪几个 token。
```

### 多个参考网站融合

**场景**：用户给 3 个 Dribbble shot / 2 个站点 URL，想"融合"成自己的风格。

**处理**：

1. **挑主样本**：让用户指定一个作"视觉主真相源"（见 [from-web 常见降级 · 多页面混合](sediment-from-web.md#多页面混合多个-shot--多个-url)）。
2. **其它素材的角色**：
   - 色板参考
   - 字体参考
   - 某个 block 的视觉参考（"表格照那张图"）
3. **主路径走 [from-web](sediment-from-web.md)**，主样本作为视觉真相；辅助素材的作用在 `source.md` 明写：

```
主样本：https://linear.app（整体视觉主真相）
辅助 1：https://stripe.com（辅色参考：强调橙 #F59E0B）
辅助 2：/tmp/dashboard-ref.png（表格 density 参考）
```

### 项目 + 从零

**场景**：用户有项目骨架但希望"大部分重写"。

**处理**：按用户要保留 vs 重写的比例决定：

- 保留 ≥50% → 走 [from-project](sediment-from-project.md)，重写部分当 modify 式覆写
- 保留 <50% → 走 [from-scratch](sediment-from-scratch.md)，项目只作为"参考 context"（不直接抽条目）

**问用户**：

```
你想从项目里保留多少？
  A) 保留项目骨架，只改色 / 字体 → 走 from-project
  B) 基本推倒重做，项目只当灵感 → 走 from-scratch，告诉我一句话描述风格
  C) 我也说不清 → 先走 from-project 扒完，到 shared-workflow 步骤 4 再一起 review 决定删哪些
```

### URL + 从零

**场景**：用户给个 URL 但又说"不要完全照它"。

**处理**：走 [from-web](sediment-from-web.md)，视觉分析当基线。在步骤 3 生成写入方案时，AI 主动加入"我按 URL 视觉推出 A+B+C，你是不是想改其中某个？"（如：主色保留，但字体从 Inter 换成衬线）。

---

## 无法归类 / 其它疑似场景

### 用户只说了个产品类型，没说风格

**例**："沉淀一个 dashboard"

**处理**：反问澄清。dashboard 是资产类别（block/page），不是风格来源。

```
dashboard 是你要沉淀的"东西"，不是"风格来源"。我需要知道：
  - 这个 dashboard 要做成什么风格？
  - 有参考对象吗？（项目 / URL / 截图 / 类比 Notion-like）
  
告诉我风格来源再推进。
```

### 用户给了一段 CSS / 一段 tokens JSON

**例**："沉淀这段 `--primary: #xxx; --font: Inter; ...`"

**处理**：视作 [from-web](sediment-from-web.md) 的"粘贴 HTML"变体——没有视觉图，只有 tokens。可以直接出 `tokens/palettes/<slug>` + `tokens/typography/<slug>`，但**其它层需要用户再给更多信息**（视觉 / 产品类型）。

### 用户想沉淀"当前正在做的东西"但说不清在哪

**处理**：

```
"当前正在做的"可能是：
  A) 某个本地项目（给路径）
  B) 在聊天里写过的一段代码（贴一下）
  C) 心里一个想法还没落地（走 from-scratch）

是哪一种？
```

---

## 不汇入共享主流程

本分支的使命**只是路由**，不直接产沉淀计划。识别完起点后交给对应分支：

- 路由到 [sediment-from-project](sediment-from-project.md)
- 路由到 [sediment-from-web](sediment-from-web.md)
- 路由到 [sediment-from-scratch](sediment-from-scratch.md)

**汇入共享主流程是下游分支的责任**，不是本分支。

---

## 典型流程示例

**场景 A**：用户说 "沉淀一下"（没任何上下文）。

AI 走：
1. 问 1 → 用户说"没项目"
2. 问 2 → 用户说"有张截图"
3. 路由到 [from-web](sediment-from-web.md)

---

**场景 B**：用户说 "沉淀 ~/proj + 参考 Linear 的色"。

AI 识别：混合场景 · 项目 + 参考网站。
→ 套"项目 + 参考网站"指引：主路径 from-project，Linear 作色板来源。

---

**场景 C**：用户说 "沉淀这个"（指什么不清楚）。

AI 反问：

```
"这个"指哪个？
  - 当前在聊的某段代码？
  - 某个项目路径？
  - 某个 URL？
  - 心里的一个风格想法？
```

拿到澄清后路由。
