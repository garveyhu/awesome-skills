---
id: blocks/search/style-vault/cmd-k-search-panel
type: block
name: ⌘K 全站搜索面板
description: 玻璃感浮层 modal · ⌘K / `/` 唤起 · 字段加权打分 + 类型 sidebar + 平台 facet + 键盘 ↑↓Enter + localStorage 最近 5 条
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/style-vault/slate-cyan-cool
  - tokens/typography/pairs/style-vault/inter-editorial-display
  - tokens/motion/style-vault/editorial-flow
  - components/tags-badges/style-vault/cyan-dot-meta-pill
preview: /preview/blocks/search/style-vault/cmd-k-search-panel
---

# Cmd-K Search Panel

> Style Vault 的全站搜索浮层 —— "一个面板能找到所有东西"。⌘K 唤起 · 输入即时搜 · 键盘可导航 · 主动关闭 = 清状态新会话；点结果跳转 = 跨导航保留，浏览器后退自动复活

## 视觉特征

```
┌──────────────────────────────────────────────────────┐
│  [⌕]  搜索风格            ⊗  全部 Web iOS Android   │  ← toolbar · `<SearchOutlined>` 20px slate-400
├──────────────────────────────────────────────────────┤
│  最近 · [ blob ] [ cta ] [ editorial ]                │  ← chips · localStorage 持久
├──────────┬───────────────────────────────────────────┤
│ 类型      │ 热门推荐                                   │
│ ● 全部 79 │ ┌─────────────────────────────────────┐   │
│   产品 3  │ │ [mini] ● 设计 · Style Vault         │   │
│   风格 3  │ │        为 AI 编码协作而造的设计...  │   │
│   页面 6  │ ├─────────────────────────────────────┤   │
│   模块 6  │ │ [mini] ● 模块 · 营销  Cool Blob Hero│   │
│ ▸ 组件 5  │ └─────────────────────────────────────┘   │
│   原语 6  │ ─ 模块 · 营销 (4)                          │
│           │   • 冷感漂浮 Hero                         │
│           │   • 渐变 Hero                             │
│           │ ─ 模块 · 展示 (3)                          │
└───────────┴───────────────────────────────────────────┘
```

### 浮层结构（4 层）

1. **遮罩** `fixed inset-0 z-[200]`，`bg-rgba(15,23,42,0.28) + backdrop-blur(1px)` —— 轻遮但不闷，背后页面仍可辨
2. **面板** 居顶 `pt-[12vh]`，`max-h-[680px] w-[min(840px,calc(100vw-48px))]`，`rounded-3xl border border-slate-200`，玻璃白底 `rgba(255,255,255,0.97) + backdrop-blur(24px)`，深柔投影 `0_32px_80px_-20px_rgba(15,23,42,0.5)`
3. **入场** 遮罩 fade（220ms ease）+ 面板 spring overshoot scale `0.96→1` + translateY `-12→0`（320ms `cubic-bezier(0.34,1.56,0.64,1)`）
4. **退场** 直接卸载（`return null`）—— 不做退场动画，避免引入 transition 复杂度

### Toolbar

- `<input>` 17px tracking-tight slate-900，placeholder 仅 `搜索风格`（不放快捷键提示，**避免视觉噪音**）
- 清空按钮 `<×>` 仅 query 非空时出现
- 平台 facet `[全部 · Web · iOS · Android]` rounded-full chip 组 —— **独立于全局 platform context**（搜索是临时探索行为，改全局态会污染浏览状态）

### 最近搜索

- 顶部 `font-mono text-[10px] uppercase tracking-[0.18em] text-slate-400` "最近" 标签
- 后跟 chips：rounded-full + slate-200 描边 + slate-600 文字，hover 收紧到 slate-900
- 持久化 `localStorage['sv-search-recent']`，最多 5 条，新搜索去重前置

### Body 双栏

- **左 sidebar 168px**（仅类型筛选 · 不放 bucket）：rounded-lg item，active = `bg-slate-900 text-white`，每条带 type-dot 6 色 + mono 计数
- **右 content 1fr**：滚动容器
  - 空 query：4 条热门推荐（横向卡 + mini preview）+ type/bucket 分组
  - 有 query：按 type 分组（折叠 bucket，只看 type）+ cyan 高亮关键词
  - 无结果：mono `No Results` + slate 提示

### 热门推荐（核心装饰区）

每条 `flex items-center gap-3.5` 横向卡：
- 左 `96×64 rounded-lg` mini preview · 手工绘对应 item 的微缩视觉（不用通用 type-letter glyph）
- 右 meta 行（type-dot · 类型 · bucket）+ 名字 14px semibold + 描述 12px line-clamp-1
- hover 浮起（translate-y-0.5 + 多层柔投影 + border 收紧）

mini preview 不用文字头像 / 单色块——而是按 id 手工绘小预览（比如 `cool-blob-hero` 真画两个模糊圆，`dark-pill-cta` 画一个真胶囊按钮）。这套微视觉的字段在面板里**用约 200 行 hand-crafted 函数**承担，权衡：维护成本中等 + 视觉信息密度极高，比泛化 thumbnail 提供 5x 信息量。

## 与同 bucket 区分

`blocks/search/` 桶第一条。后续搜索类条目（搜索结果页 / 联想 dropdown / 全站快搜入口...）都归这桶。

- **vs `blocks/filters/style-vault/sticky-chip-filter-panel`**：那条是常驻 sidebar（4 组 chip toggle，全在视野内）；本条是按需浮层 modal，结构性差异显著
- **vs `components/overlays/style-vault/spring-toast`**：toast 是一过性反馈胶囊（2s 自消）；本条是用户主动召唤、主动关闭的探索界面

## 搜索打分

```ts
function score(item, q) {
  const l = q.toLowerCase();
  let s = 0;
  if (item.name.toLowerCase().includes(l))        s += 5;  // name 命中权重最高
  if (item.description.toLowerCase().includes(l)) s += 2;
  if (item.id.toLowerCase().includes(l))          s += 1;  // 路径段命中（如搜 "blob" 命中 cool-blob-decor）
  const tags = [...item.tags.aesthetic, ...item.tags.mood, ...item.tags.stack];
  if (tags.some(t => t.toLowerCase().includes(l))) s += 1;
  return s;
}
```

不引 Fuse.js —— **substring + 权重**对 < 200 条的小 registry 已足够，且无外部依赖。当 registry > 500 条且需要拼写容错时再升级到 Fuse.js（threshold 0.3，weights 同此）。

## 触发模式（singleton）

`SearchPanel` 用 module-level state + listeners 模拟单例（参考 `Toast.tsx` 同款 pattern），不走 Context：

```ts
let isOpen = false;
// 跨 mount 持久化：用户点结果跳详情后回退能续上
let storedQ = '';
let storedType: TypeFilter = 'all';
let storedPlatform: 'all' | PlatformSel = 'all';
// 标记"因点击结果而临时关闭" · 浏览器 POP 时自动复活面板
let pendingReopen = false;

const listeners = new Set<() => void>();
function emit() { listeners.forEach(l => l()); }

export const searchPanel = {
  open:   () => { isOpen = true;  pendingReopen = false; emit(); },
  close:  () => { isOpen = false; pendingReopen = false; emit(); },  // 主动关 = 清意图
  closeForNavigation: () => {                                          // 临时关 = 保留意图
    isOpen = false; pendingReopen = true; emit();
  },
  toggle: () => { isOpen = !isOpen; if (isOpen) pendingReopen = false; emit(); },
};
```

任何组件 `import { searchPanel } from '...'` 直接 `searchPanel.open()` 即可。**不需要 Context Provider 包裹**，避免树深度增长。

## 跨导航持久化（连续搜索的关键）

用户的搜索行为是高频连续的：搜 → 点结果 → 看一眼 → 后退继续搜 → 再点。如果每次 panel 关闭都重置 q/type/platform，每次回退都得重新打字 —— 体验断裂。

设计三件事保证连续：

### 1. module-level `storedQ / storedType / storedPlatform`

PanelInner 内部 state 用 module 单例 hydrate 初值，每次 setState 同步写回 module：

```tsx
function PanelInner({ onClose }) {
  const [q, setQ] = useState(storedQ);
  const [type, setType] = useState<TypeFilter>(storedType);
  const [platform, setPlatform] = useState<'all' | PlatformSel>(storedPlatform);

  useEffect(() => { storedQ = q; }, [q]);
  useEffect(() => { storedType = type; }, [type]);
  useEffect(() => { storedPlatform = platform; }, [platform]);
  // ...
}
```

PanelInner unmount 后状态留在 module 闭包里，下次 mount 还能续上。

### 2. `closeForNavigation` 而非 `close`

点击结果项的 `openItem` **不能调 `close()`**（那会清掉 `pendingReopen`）：

```tsx
function openItem(id, ev) {
  if (ev?.metaKey || ev?.ctrlKey) {
    window.open(path, '_blank', 'noopener');  // 新窗口：面板保留
    return;
  }
  searchPanel.closeForNavigation();   // 临时关：保留 q/type/platform + 设 pendingReopen
  nav(path);
}
```

### 3. wrapper 监听 `useNavigationType()`，POP 时自动复活

```tsx
export function SearchPanel() {
  const { key } = useLocation();
  const navType = useNavigationType();

  useEffect(() => {
    if (navType === 'POP' && pendingReopen && !isOpen) {
      searchPanel.open();
    }
  }, [key, navType]);
  // ...
}
```

行为矩阵：

| 操作 | pendingReopen 变化 | 下次 POP 是否复活 |
|---|---|---|
| `open()` (⌘K / 快捷键 / 手动唤起) | 清掉 | 否 |
| `close()` (ESC / 遮罩点击) | 清掉 | 否 |
| `closeForNavigation()` (点结果跳转) | 设 true | **是** |
| ⌘+click 结果（新窗口） | 不变（面板没关） | 维持原状态 |

**关键**：POP 复活只消费一次 `pendingReopen` 就清；用户复活后再 ESC 就回到清状态。

## 全局快捷键

```ts
useEffect(() => {
  const onKey = (e) => {
    if (isOpen) return;  // 打开后由面板自身处理
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault(); searchPanel.open();
    } else if (e.key === '/' && !isInputFocused()) {
      e.preventDefault(); searchPanel.open();
    }
  };
  window.addEventListener('keydown', onKey);
  return () => window.removeEventListener('keydown', onKey);
}, []);
```

`/` 快捷键的 `isInputFocused()` 守卫是必须的 —— 否则用户在任何 input 里打 `/` 都会唤起。

## 键盘导航

面板内部第二个 keydown listener，和外部分开避免互冲：

| 键 | 行为 |
|---|---|
| `↑/↓` | 在 `flatNav[]` 上导航；`flatNav` = popular（仅 type=all 空 query 时）+ 当前 visible items |
| `Enter` | 打开 `flatNav[kbIdx]` 或 `flatNav[0]`（**当前 tab**）· 关闭面板 |
| `⌘/Ctrl+Enter` | 打开 `flatNav[kbIdx]` 在**新窗口**（`window.open(path, '_blank', 'noopener')`）· **保留面板**让用户继续搜 |
| `Esc` | 关闭面板 |

`scrollIntoView({ block: 'nearest' })` 跟随 active row 移动，避免出可视区。

## 路由跳转

- `id.startsWith('products/')` → 路径 `/products/{slug}`
- 其它 → 路径 `/item/{id}`

### 三种打开方式

每条结果（包括热门推荐卡 / query mode 行 / bucket 分组行）都支持：

| 触发 | 行为 |
|---|---|
| 普通 `click` / `Enter` | 当前 tab `nav(path)` · 关闭面板 |
| `⌘/Ctrl + click` / `⌘/Ctrl + Enter` | 新 tab `window.open(path, '_blank', 'noopener')` · **不关面板** |
| **中键 click**（鼠标） | 视同 `⌘+click` —— 新 tab 打开 · 不关面板（`onAuxClick` + `e.button === 1`）|

**关键**：⌘+click 不关闭面板的设计是有意的 —— 用户用 ⌘+click 通常是"快速预览多个"行为，关闭再打开会打断节奏。

跳转前 `pushRecent(q)` 把当前 query 写进 localStorage —— 只有"成功打开了某条"才记录，**避免乱搜也污染历史**。`⌘+click` 也算"打开"，照样写入历史。

### 实现要点

```tsx
function openItem(id: string, ev?: { metaKey?: boolean; ctrlKey?: boolean }) {
  const path = id.startsWith('products/')
    ? `/products/${id.replace(/^products\//, '')}`
    : `/item/${id}`;
  if (ev?.metaKey || ev?.ctrlKey) {
    window.open(path, '_blank', 'noopener');
    return;  // 保留面板
  }
  searchPanel.closeForNavigation();  // 临时关 · 保留 q/type/platform · 设 pendingReopen
  nav(path);
}

// 行 button
<button
  onClick={(e) => onOpen(id, e)}
  onAuxClick={(e) => {
    if (e.button === 1) {
      e.preventDefault();
      onOpen(id, { metaKey: true });
    }
  }}
>...</button>
```

`onAuxClick` 中 `e.preventDefault()` 是必须的——否则浏览器在某些场景下会把中键 click 当成"打开链接"的默认行为，但对 `<button>` 没意义，反而会导致页面滚动 / 手势触发。

`window.open` 第三参数 `noopener` 防止 `window.opener` 引用，是基本安全实践。

## 适配指南

- **module-level state 的副作用**：Fast Refresh 在开发热更时可能让 `isOpen` 旧值不一致。生产无影响。如果需要绝对一致，迁移到 Context
- **数据源切换**：搜索源是 `useRegistry().items`。换成网络请求时把 `useMemo` 改成 `useEffect + useState`，加 loading / error 态
- **键盘范围**：所有键盘 listener 注册在 `window` 上，关闭后 cleanup —— 不影响其它页面键盘行为
- **i18n**：所有 label / placeholder 已抽到代码内，未来切英文时统一在 `taxonomy.ts` 加 `en` 字段（**不要**在组件里 inline 翻译）

## 反模式

- 不要把面板做成抽屉（`right-0` slide-in）—— 浮层中心化是搜索的语义身份
- 不要在 placeholder 里塞快捷键提示（如 `搜索 ⌘K`）—— 视觉噪音；快捷键工作但不显示
- 不要让面板顶部 `top-0` 贴顶 —— `pt-[12vh]` 留白让"打开了一个东西"的语义出来
- 不要把"清除"按钮和"清除最近搜索"耦合 —— 用户清当前 query 不应该影响历史
- 不要在 query 模式还展现 bucket 分组 —— 命中条目可能跨 bucket，按 type 分组更清晰
- 不要展现"X 条结果"counter 在面板顶部 —— 信息已分布在 sidebar 计数和分组 header，重复
- 不要把搜索面板的 platform facet 联动到 TopBar 全局 platform —— 搜索是临时态，改全局会让用户找不回原来的浏览上下文
- 不要给"最近"chips 加 close icon —— 历史是被动累积的，主动管理过细让面板变工具箱
- 不要在 `openItem` 里直接调 `onClose()`（=> `searchPanel.close()`）—— 那会清掉 `pendingReopen`，浏览器后退就续不上 q/type/platform。必须走 `closeForNavigation()`
