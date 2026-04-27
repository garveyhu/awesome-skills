# lessons-loopback · 教训回写

Skill 可以**自己修自己**——每次沉淀出错（用户指出差异大 / AI 通读源码后发现之前抽象错了），把**错误模式**（不是具体错误）抽象成**硬规矩**，回写到对应 workflow 文件，后续执行会自动遵守。

Skill 越用越准。

---

## 什么时候触发

**必触发**（任一满足 → 进入回写流程）：

- 用户在 review 阶段拒绝，并给出明确原因
- 用户在写入后指出"差异大"、"风格不对"、"漏了 xxx"、"跟真实站差太多"
- 用户要求重写某条已沉淀条目
- AI 自己在通读源码或用户截图后，发现之前抽象错了

**不触发**：用户只做细节微调（"把名字改成 xxx"、"圆角从 xl 改到 2xl"）——这是小错不是模式错，改条目即可。

---

## 区分"一次小错"vs"模式错"

**只有"模式错"才回写**。判定：

| 维度 | 一次小错 | 模式错（回写） |
|---|---|---|
| 本质 | 具体条目的具体字段错了 | workflow 本身缺 discovery 步骤 / 缺硬规矩 |
| 复现 | 不会反复出现 | 如不回写，下次换个场景还会犯 |
| 修复 | 改该条目即可 | 改 workflow 文件 |
| 涉及面 | 1 条条目 | 可能影响未来所有沉淀 |

**举例**：

❌ **不回写**（一次小错）
- skill-card 圆角写成 rounded-xl，真实是 rounded-2xl
- teal-pill 字号写成 text-xs，真实是 text-[11px]
- user-home 头像色取了 index 5，真实是 index 0
- 等等——**改条目即可**

✅ **回写**（模式错）
- 写 page 条目只读了文件头 150 行（state/hooks）就开始写，没通读 JSX 渲染 →
  **回写到 `sediment-from-project.md`**："写 page 前必须通读 JSX + 文件长度分级读法"
- Tier 2 沉淀 skillhub 漏 10/12 主路由，没做路由覆盖率检查 →
  **回写到 `depth-tiers.md`**："Tier 3 硬下限 checklist · 主路由 ≥80%"
- from-web 时只靠 URL 拉 HTML 没要用户贴截图，出来的沉淀主色错了 →
  **回写到 `sediment-from-web.md`**："URL + 截图二者有一即可，单 URL 不足以判定视觉"

---

## 回写 3 步

### 第 1 步 · 抽象问题

用**一句话**陈述"我为什么会犯这个错"（不是"我犯了什么错"）：

- ❌ "我把 skill-article-detail 的 install 命令条漏了"
- ✅ "我写 page 条目时没通读 JSX 渲染部分，只看了 state/hooks 就开始抽象"

抽象粒度：要能推广到"下次遇到同类情况不会再犯"。

### 第 2 步 · 定位所属 workflow 文件

| 错误性质 | 回写位置 |
|---|---|
| 起点发现（扫项目 / 解析 URL / 对齐对话）| `sediment-from-project.md` / `sediment-from-web.md` / `sediment-from-scratch.md` |
| 档位选择 / 覆盖率 / 条目数 | `depth-tiers.md` |
| Plan / review / 写入 / commit / 报告 | `shared-workflow.md` |
| 跨所有 workflow 的共通原则 | `SKILL.md` 共享原则 |
| 只是单一错误的历史记录 | 本文件（lessons 清单）|

**先搜再加**——用 grep 确认现有文件里没有同义规则，避免重复：

```bash
grep -rn "关键词" ~/.agents/skills/style-vault-sediment/{SKILL.md,references/*.md}
```

### 第 3 步 · 写硬规矩 + 自检

**硬规矩必须满足**：

- 用"必须 / 不允许 / 一律 / 绝不"强制语气
- 给具体可操作的动作（不是抽象建议）
- 附 2-5 条**自检问题**让 AI 在执行前自问

**模板**：

```markdown
## <小节标题> · 必做

**惨痛教训**（<YYYY-MM-DD> · <场景>）：<一句话错误模式>

### 硬规矩

<2-5 条"必须 / 不允许"句式>

1. **必须** xxx
2. **不允许** yyy
3. ...

### 自检问题（执行前自问）

- [ ] 问题 1
- [ ] 问题 2
- [ ] ...

答不上 → 回去补。
```

---

## 反污染规则（回写时必须遵守）

1. **不允许把"具体错误"写成"教训"**——污染 skill 体积，降低有效信号
2. **不允许在同一个 workflow 里加同义规则**——先 grep 确认
3. **不允许用"温馨提示 / 建议 / 尽量"语气**——AI 会直接忽略；**必须"必须 / 不允许"**强制语气
4. **不允许抽象到无法执行**——"写代码要仔细"这种不算规矩，"写 page 前必须 Read 整个 JSX 到文件末"才算
5. **不允许跳过本文件的清单登记**——回写完要在"已回写教训清单"append 一行，否则追溯不到

---

## 已回写教训清单（append-only）

| 日期 | 错误模式 | 回写位置 | 相关 sediment |
|---|---|---|---|
| 2026-04-24 | 第一次 skillhub 沉淀只按 Tier 2 硬推 15 条，没做全路由枚举就收工，漏 10/12 主路由 | [depth-tiers.md · Tier 3 硬下限 checklist](depth-tiers.md) | 2026-04-24-skillhub / tier3 |
| 2026-04-24 | 写 skill-article-detail 条目时只读文件头 150 行（state/hooks），没通读 JSX 渲染，凭印象套了"长文 + sidebar"模板，漏掉安装命令条/SUMMARY box/SKILL.md pill/timeline 评论 6 处核心结构 | [sediment-from-project.md · 写 page 条目前的硬规矩](sediment-from-project.md) | 2026-04-24-skillhub-tier3 + 后续修正 |
| 2026-04-24 | 虽然上一条规矩已生效，但还是连续 4 页（publish/IM/me/edit）重蹈覆辙——说明读 JSX 的强制不够靠前 | 同上（规矩本身够，但 AI 执行时没自检，增加"每次写 page 前先答 4 问"自检 checkbox）| 2026-04-24 用户指出 4 页差异 |
| 2026-04-24 | 写 preview tsx 时用 Antd `<Button type="primary">` 没覆盖 `colorPrimary`，直接出 `#1677ff` 默认蓝；用 `<Tag color="blue">` / hardcoded `bg-blue-50` / `text-blue-500`——这些都是"用了 antd/tailwind 默认色没对齐被沉淀站的主色覆盖"的同一类错 | [见下方"preview 写 antd 组件的硬规矩"节](#preview-写-antd-组件的硬规矩必做) | 2026-04-24 用户指出 user-public-profile / profile-edit-form / admin table & toolbar 有大量默认蓝 |
| 2026-04-24 | 写 user-public-profile 时加了 tabs + 2 列内容，真实页是纯 profile header 无 tabs——凭印象套了"用户主页 = header + tabs"的刻板印象 | 并入上面"通读 JSX"规矩——**每个 page 源码的 return 块必须从头读到尾，不允许脑补存在本无的结构** | 2026-04-24 同上 |
| 2026-04-24 | 写 `blocks/form/profile-edit-form` 时被"form"这个名字带偏，直接写成"头像 + input 字段 + 保存按钮"的长表单，真实 skillhub `/me/edit` 是 **iOS 列表点击模式**（每行点击弹独立 modal，没保存按钮）| [见下方"block/page 命名不能带偏抽象"节](#blockpage-命名不能带偏抽象必做) | 2026-04-24 用户指出 profile-edit-form 不对 |
| 2026-04-24 | preview 组件在卡片缩略图里**反复 mount** 时，任何"mount 时的异步动画"都会被反复触发放大可见——具体表现两类：(a) `scrollIntoView({smooth})` / framer-motion `initial→animate` / CSS `transition from→to` 等进场动画；(b) macOS overlay scrollbar 在程序化 `scrollTop = N` 时系统级"淡入再淡出"动画。用户切分类时整屏卡片反复闪 | [见下方"preview 组件是静态快照 · 禁止 mount 时异步动画"节](#preview-组件是静态快照--禁止-mount-时异步动画必做) | 2026-04-24 用户连续指出 StyleCard scale 闪、IM 滚动条抖动、macOS overlay 滚动条渐隐 |
| 2026-04-24 | `useSyncExternalStore` 的 `getSnapshot` 返回**每次新构造的对象** `{ cols, label }` → React `Object.is` 比较每次都不等 → 判定 store 变了触发 rerender → 再 call snapshot 又得新对象 → **无限循环 Maximum update depth / 页面白屏**。错因是想一次性从 hook 返回多个值，没意识到新对象引用每次都变 | [见下方"useSyncExternalStore snapshot 必须返回原语或稳定引用"节](#usesyncexternalstore-snapshot-必须返回原语或稳定引用必做) | 2026-04-24 用户报白屏 · `fixed-cols-row.tsx` preview |
| 2026-04-27 | 旧 flat slug `<bucket>/<base-name>` 在多 product 共存下必撞——同语义的 cyan-cta（acme） / dark-primary-cta（skillhub）抢 buttons/ 命名位，AI 消费时无从区分。**根因是 base-name 没绑风格世界**| 已通过 namespace 机制（路径中间一级 `<namespace>/`）解决 · 不再回写新规则；本条仅作历史记录 | 2026-04-27 acme rebuild |
| 2026-04-27 | review 后期才发现新增的 cyan-cta / status-pulse 跟已有 dark-primary-cta / pulse-dot 视觉/语义重叠——差点引入冗余条目。**根因是生成 frontmatter 前没扫同 bucket 已存在条目** | [shared-workflow.md · 步骤 3.b 重名 grep](shared-workflow.md#3b--重名-grep必做--写-frontmatter-之前) | 2026-04-27 acme rebuild |
| 2026-04-27 | skill 仓 commit 用 `git add -A` 把无关的循环 symlink `wiki-creator/wiki-creator` 拉进 commit，事后单独打 chore commit 修。**根因是 skill 仓多 skill 共存时 -A 会污染** | [shared-workflow.md · 精确 add 硬规矩](shared-workflow.md#精确-add-硬规矩必做--skill--vault-两仓都遵守) | 2026-04-27 acme rebuild |
| 2026-04-27 | sage tier3 沉淀的 38 条 preview .tsx 全部用 emoji（👤🛡⚙💾📦🧩📊🐬🐘等）替代源码使用的 lucide-react 图标。**根因是 preview 里"省事用 emoji"被默认接受**——但 icon 选型本身是风格的一部分，emoji 跟线性矢量是两种视觉语言，整套风格立刻变味 | [sediment-from-project.md · preview 写 icon 的硬规矩](sediment-from-project.md#preview-写-icon-的硬规矩用源码同款-icon-库禁用-emoji-替代必做) | 2026-04-27-sage |
| 2026-04-27 | sage tier3 preview 的 padding / borderRadius / fontSize / shadow / 颜色 hex 大量"凭印象差不多"——和 skill .md 里写的"视觉特征"具体数值脱节，整套气质漂移。**根因是没把 skill .md 的"视觉特征"放进工作集就直接写 preview** | [sediment-from-project.md · preview 必须深度还原源码具体数值](sediment-from-project.md#preview-必须深度还原源码具体数值必做) | 2026-04-27-sage |

---

## preview 写 antd 组件的硬规矩（必做）

**惨痛教训**（2026-04-24）：写预览时直接用了 Antd / tailwind 默认颜色 → 最终 preview 里到处是 `#1677ff`（antd 默认 primary 蓝）、`bg-blue-50/50`（默认选中行蓝）、`<Tag color="blue">` 等，完全违背被沉淀站"slate + teal"的主色。**用户一眼看出"默认色的廉价感"**。

### 硬规矩

1. **preview 里用 Antd 组件必须包一层 `<ConfigProvider theme={{ token: { colorPrimary: '<被沉淀站主色>' } }}>`**。不允许裸用 `type="primary"`——会直接渲染 antd 默认蓝 `#1677ff`
2. **不允许用 `<Tag color="blue">` / `"purple"` / `"geekblue"` 等 antd 预设色名**——这些都是预设的调色，和被沉淀站无关。要么 `color="default"` + 自定义 className，要么用具体 hex
3. **不允许硬编码 tailwind 的 `bg-blue-*` / `text-blue-*` / `text-indigo-500`**（除非被沉淀站本身用了这个色——先在源码里 grep 确认）
4. **preview 调色表必须从被沉淀站的"主色 tokens"取值**，不能从 antd 默认色 / tailwind 默认色 / lucide 图标随手填的色里找
5. **写 antd 表格的 `ant-table-row-selected` 背景时先查源码**——skillhub 真实用 `bg-slate-100/60`（不是 antd 默认的 `bg-blue-50`），很多网站也会覆盖

### 自检问题（写 preview 前自问）

- [ ] 这个 preview 里每一个"蓝色"都有源码依据吗？（源码里能 grep 到对应的类）
- [ ] 用了 Antd Button/Input/Select 的 `type="primary"` 时，有 ConfigProvider 包着吗？
- [ ] 用 Tag 的 `color=` 时，这个色是被沉淀站真用了的，还是 antd 预设？
- [ ] Modal / Popover 里的"确定"按钮用了 hardcoded `#1677ff` 吗？（违规）

任一答不上 → 去源码 grep 确认该色是否合法。

---

## block/page 命名不能带偏抽象（必做）

**惨痛教训**（2026-04-24）：写 `blocks/form/profile-edit-form` 时因为命名里有 "form"，直接套了"标准长表单 + 保存按钮"的刻板印象，而真实 skillhub 的"编辑资料"**根本不是 form 范式**——是 iOS 设置列表点击模式（每行点击弹独立 modal，没保存按钮）。**命名和实际形态脱钩**的情况下如果只看名字写实现，结果必然错。

### 硬规矩

1. **不允许根据 id 里的关键词（"form" / "card" / "list" / "modal" / "hero" / "sidebar" ...）推断实现形态**——id 是归类 slug，不是实现规范
2. **必须先看源码 JSX 确认真实形态**：是 form？是列表？是 grid？是 modal stack？真实用的是什么交互模式？
3. **如果真实形态和命名暗示不一致，必须在 MD 开头用一句话说清差异**：
   > "名字叫 form，但**本质不是传统表单**——skillhub 真实用的是 iOS 列表点击模式。如果你想做传统长表单 + 保存按钮那种形态，这个 block 不是；那种该另开一个 block。"
4. **已有条目发现命名被带偏后**：**不重命名**（保持 id 稳定），但 MD 必须显式标注真实形态 + 反例提醒

### 自检问题（写 block/page 前自问）

- [ ] 我根据 id 的哪些关键词做了"这是 xxx 形态"的推断？真实源码支持吗？
- [ ] 源码里这个交互的**顶级容器元素**是什么？（`<form>` / `<div divide-y>` / `<Modal>` / `<Tabs>` / ...）
- [ ] 这个页/块有没有明显的"保存" / "提交" / "确定"按钮？位置在哪？（form 通常底部或顶部右；列表式通常没有）
- [ ] 真实交互是一次性输入全字段 submit，还是点一行改一字段？

任一答错 → 停下来重读源码，别被 id 名字带偏。

---

## preview 组件是静态快照 · 禁止 mount 时异步动画（必做）

**惨痛教训**（2026-04-24 · 连续 3 轮用户指正）：preview 组件在 vault 网站里会被 StyleCard 缩放成卡片缩略图。卡片在切分类/筛选/滚动时**反复 mount**，任何"mount 时触发的异步动画"都会在卡片里反复播放 → 用户看到整屏闪烁。

具体表现（同一类错的不同症状）：

1. **StyleCard 初始 scale 硬编码 0.28** · useEffect 在 paint 后才纠正 → 每次卡片 mount 都先按 0.28 画一帧再跳到正确 scale
2. **IM preview `scrollIntoView({ behavior: 'smooth' })`** · 300ms 平滑滚动动画 → 卡片 mount 时播放，切分类时整屏滚动条乱动
3. **macOS overlay scrollbar** · 程序化 `el.scrollTop = el.scrollHeight` 触发系统级"淡入淡出"动画 → 用户在缩略卡里看到滚动条闪一下
4. **潜在同类**：framer-motion `initial + animate` 的进场动画（opacity 0→1 / translateY 20→0）同理；CSS `transition` 配合 mount 时 state 切换同理

### 硬规矩

1. **preview 组件必须是"静态快照"** · 渲染完立即稳定 · **不允许 mount 时触发任何 > 0ms 的动画**
2. **测量类副作用（scale / 容器尺寸 / 首帧滚动位置）必须用 `useLayoutEffect` + 初始同步测量** · paint 前完成，不产生"首帧错误→第二帧正确"的闪烁
3. **首次进入滚动到底 / 到指定位置，用 `el.scrollTop = N` 或 `el.scrollLeft = N`**，**禁止** `scrollIntoView({ behavior: 'smooth' })` · smooth 必然动画
4. **preview 里的 overflow 容器必须隐藏滚动条** · 因为 pointer-events-none 下用户无法滚，但程序化 setScroll 会触发 macOS overlay scrollbar 的系统动画。用以下 CSS 三重保险：
   ```css
   .xxx::-webkit-scrollbar { display: none; width: 0; height: 0; }
   .xxx { scrollbar-width: none; -ms-overflow-style: none; }
   ```
5. **framer-motion 在 preview 里要么换 `animate` 直接到终态（省 `initial`），要么完全去掉**——mount-time 进场动画在缩略卡上下文没意义
6. **CSS `transition` 里不允许 mount-state 切换触发** · 例：别在 mount 后 setState 改 className 来触发 from→to 的 transition

### 自检问题（写 preview 前自问）

- [ ] 这个 preview 里有 `scrollIntoView` / `element.animate` / `requestAnimationFrame` / `setTimeout` 吗？任一有 → 可疑
- [ ] 这个 preview 用了 `useEffect` 做首次测量 / 定位 / 滚动吗？应改 `useLayoutEffect` + 初始同步值
- [ ] 这个 preview 用 framer-motion 的 `initial` 属性吗？mount 时会播放 → 缩略卡里是噪音，去掉
- [ ] 这个 preview 有 `overflow-auto` / `overflow-y: auto` 容器吗？没隐藏滚动条 → 切分类时用户会看到滚动条闪烁
- [ ] 这个 preview 的初始 state 里有"需要测量后修正的值"吗（如 scale / container size）？初始给 `null` 不渲染，`useLayoutEffect` 填完再渲染

任一命中 → 改。缩略卡里的静态感是硬底线，preview 是给 vault 网站做"一眼看风格"用的，不是功能演示。

---

## useSyncExternalStore snapshot 必须返回原语或稳定引用（必做）

**惨痛教训**（2026-04-24 · 前端白屏 · `fixed-cols-row.tsx` preview）：想一次性从 `useCols` hook 返回多个值 `{ cols, label }`，直接让 `getSnapshot` 构造新对象返回：

```ts
function snapshot() {
  for (const bp of BREAKPOINTS) {
    if (window.matchMedia(bp.query).matches) return { cols: bp.cols, label: bp.label };
  }
  return { cols: 1, label: 'base' };
}
```

每次调用产生**新对象引用**。React 内部用 `Object.is(prev, next)` 判定"store 变了没"——新对象 `!==` 旧的 → 每次 rerender 后都认为变了 → 又调 `getSnapshot` → 又得新对象 → **infinite loop**，浏览器控制台报：

> The result of getSnapshot should be cached to avoid an infinite loop
> Uncaught Error: Maximum update depth exceeded.

整个 BrowseCategoryPage 白屏。

### 硬规矩

1. **`getSnapshot` 必须返回原语（number / string / boolean）或稳定引用（module-level 常量 / cached object / Map 取值）**
2. **绝不允许 `getSnapshot` 内 `return { ... }` 或 `return [...]` 新建对象/数组**
3. **需要多字段返回时**：
   - 选项 a · 返回原语，派生值在 hook 外层算：
     ```ts
     function useColsState() {
       const cols = useSyncExternalStore(subscribe, getSnapshot, () => 4);
       return { cols, label: LABEL_MAP[cols] };  // 每次 rerender 新对象，但 cols 变才 rerender
     }
     ```
   - 选项 b · 用 module-level Map 缓存：
     ```ts
     const CACHE = new Map<number, { cols: number; label: string }>();
     function getSnapshot() {
       const cols = computeCols();
       if (!CACHE.has(cols)) CACHE.set(cols, { cols, label: LABEL_MAP[cols] });
       return CACHE.get(cols)!;  // 同 cols → 同引用
     }
     ```
4. **`getServerSnapshot` 也必须返回原语或 module-level 常量**，不是每次新建

### 自检问题（写 useSyncExternalStore 前自问）

- [ ] 我的 `getSnapshot` 里有 `return { ... }` 或 `return [...]` 吗？**必定无限循环**
- [ ] 我的 `getSnapshot` 返回的是 number / string / boolean 之一吗？是 → 安全
- [ ] 如果要返回对象，是否用 module-level 常量或 Map 缓存保证同输入 → 同引用？
- [ ] `getServerSnapshot` 是否也满足上述条件？

任一答"不是" → 改。这个坑非常隐蔽（HMR 里可能没事，build 后才炸），测试覆盖必须包括首屏加载 + 多次状态切换。

---

## 元提示（给 AI 的元规则）

1. 当用户说"差太多" / "差异大" / "不对" / "跟真实的不一样" 时，**第一反应不是"我改条目"**，而是**先问自己**："这是一次小错还是模式错？"——如果疑似模式错，进入本流程
2. 回写教训**就是沉淀的一部分**，同 commit 提交（message 前缀：`docs(skill): 沉淀教训 · <简短>`）
3. 本文件的清单增长代表 skill 在变强。**不允许删清单**（即使教训过时也只标注"已失效"，不删）
