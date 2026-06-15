---
id: pages/chat/chameleon/embed-fullscreen-chat
type: page
name: 嵌入式全屏对话页 / 会话详情气泡
description: /embed/:embedKey 公开对话壳页（widget fullscreen 占满 viewport）+ 可观测域三段式会话详情（身份头 → 聚合 StatBar → 真实对话气泡 + 反向分页）
platforms:
- web
theme: light
tags:
  aesthetic:
  - minimal
  - industrial
  mood:
  - calm
  - serious
  stack:
  - shadcn-radix
uses:
- blocks/chat/chameleon/embed-widget-bubble-shell
- blocks/chat/chameleon/markdown-message-citation
- blocks/chat/chameleon/message-actions-bar
- blocks/display/waveflow/metric-card-quartet
- tokens/palettes/waveflow/warm-paper-ink-blue
preview: /preview/pages/chat/chameleon/embed-fullscreen-chat
---

# Chameleon Embed Fullscreen Chat / Conversation Detail

> 两个同源场景共一条:
> 1. **嵌入式全屏对话壳页** `/embed/:embedKey`——本页只是「壳」：`<div class="h-screen w-screen bg-white">`，动态注入 `/widget.js` 并以 `fullscreen:true` init，widget 自挂 `document.body` 占满 viewport，渲染同一套 widget shell（无浮动气泡、永远 open、无圆角无阴影无 transform）。供业务方 iframe 嵌入或新标签直访，`?euid=` / `?jwt=` 透传身份。缺 key 时居中显「缺少 embed_key」。
> 2. **可观测域会话详情**——三段式（身份头 → 聚合 StatBar → 真实对话气泡），气泡和 playground / widget 同源但用更宽（78%）更大间距（space-y-5）+ 反向分页滚动锚定。本 preview 主要还原第 2 个（视觉信息密度最高的页面）。

## 视觉特征

### 壳页（fullscreen 模式）
- 壳容器：`h-screen w-screen bg-white(#ffffff)`，什么都不渲，widget 自挂 body
- widget fullscreen `.panel.fullscreen`：`position:fixed; inset:0; width/height:100%; max-width/height:none; border-radius:0; box-shadow:none; transform:none`（vs 浮动 panel 的 radius/shadow/translate 全去掉）
- 缺 key：`flex h-screen w-screen items-center justify-center bg-stone-50(#fafaf7) text-[12.5px] text-stone-500「缺少 embed_key」`

### 会话详情（三段式，`space-y-3` 纵向堆叠）
- **三段都是 SectionCard**：`rounded-xl(16px) border border-stone-200/40 bg-paper p-5(20px) shadow-soft`
- **段 1 身份头**（`SectionCard !py-3`，覆盖竖向 padding 为 12px）：
  - 面包屑行：返回 Link `inline-flex gap-1 rounded-md px-1.5 py-1 text-[12.5px] text-stone-500 hover:bg-stone-100 hover:text-stone-800`（`ArrowLeft h-3.5 w-3.5` + 「会话」）→ `/` 灰分隔 → session 标签 `rounded bg-violet-50 px-1.5 py-0.5 font-mono text-[11px] text-violet-600` → 标题 `truncate text-[15px] font-semibold text-stone-900`
  - 元信息行（`mt-2 flex flex-wrap gap-x-4 gap-y-1 text-[11.5px]`）：会话号复制 button `inline-flex gap-1 font-mono text-stone-600 hover:text-blue-600`（`Copy h-3 w-3 opacity-50`，copied→`Check h-3 w-3 text-emerald-500`）+ 创建/最后活跃时间（label `text-stone-400` + 值 `font-mono text-stone-600`）
  - **段 2 聚合 StatBar**（`mt-3`）：6 个 StatItem（应用 mono / 终端用户 mono / 轮次 + sub「N 条消息」/ Token / 成本 / 模型 mono + sub「+N」），StatItem = label `text-[10.5px] text-stone-400` + value `text-[15px] font-semibold tnum`（mono 档 `text-[13px]`），右侧 `border-r border-stone-100 pr-4 mr-4`
- **段 3 气泡区**（`SectionCard !p-0`，去内边距）：
  - 滚动容器：`max-h-[calc(100vh-260px)] overflow-y-auto px-5(20px) py-5(20px)`，内 `space-y-5(20px)`
  - 加载更早按钮（顶部，`flex justify-center pb-1`）：`inline-flex gap-1.5 rounded-full border border-stone-200 bg-white px-3 py-1 text-[12px] text-stone-600 hover:border-blue-300 hover:bg-blue-50 hover:text-blue-700`（`Loader2 h-3 w-3 animate-spin` + 「加载更早（已加载 N / total）」）
  - **每条消息**（`group/msg flex flex-col gap-1`，user → `items-end`，assistant → `items-start`）：
    - 元信息行：`flex items-center gap-2 px-1 text-[10.5px] text-stone-400`——角色 `font-medium text-stone-500` + `#seq font-mono` + 时间 `font-mono` + 反馈（`ThumbsUp h-3 w-3 text-emerald-500` / `ThumbsDown h-3 w-3 text-rose-500`）
    - 气泡：`max-w-[78%] rounded-2xl(16px) px-3.5(14px) py-2.5(10px) text-[13px] leading-relaxed`
      - user：`rounded-tr-sm(2px) bg-blue-600(#2563eb) whitespace-pre-wrap text-white`
      - assistant：`rounded-tl-sm(2px) border border-stone-200 bg-white text-stone-800`（Markdown 渲染）
    - 动作行（`flex items-center gap-1.5`，user `flex-row-reverse`）：trace 按钮常显 `rounded-md border border-stone-200 bg-white px-1.5 py-0.5 text-[10.5px] text-stone-500 hover:border-blue-300 hover:bg-blue-50 hover:text-blue-600`（`ListTree h-3.5 w-3.5` + 「trace」）+ MessageActions（hover 才显 `opacity-0 group-hover/msg:opacity-100`）

## 核心代码

```tsx
// 壳页：动态注入 widget.js fullscreen init
useEffect(() => {
  const boot = () => window.ChameleonWidget?.init({
    embedKey, apiBase: window.location.origin, fullscreen: true, externalUserId, jwtToken });
  if (window.ChameleonWidget) boot();
  else { const s = document.createElement('script'); s.src = '/widget.js'; s.async = true; s.onload = boot; document.body.appendChild(s); }
}, [embedKey, externalUserId, jwtToken]);
return <div className="h-screen w-screen bg-white" />;

// 会话详情气泡
<div className={cn('max-w-[78%] rounded-2xl px-3.5 py-2.5 text-[13px] leading-relaxed',
  isUser ? 'rounded-tr-sm bg-blue-600 whitespace-pre-wrap text-white'
         : 'rounded-tl-sm border border-stone-200 bg-white text-stone-800')}>
  {isUser ? msg.content : <Markdown content={msg.content} />}
</div>
```

```tsx
// 反向分页 + 滚动锚定：首屏滚到底，加载更早后保持视口位置
useLayoutEffect(() => {
  const el = scrollRef.current; if (!el || !messages.length) return;
  if (initedSid.current !== sid) { initedSid.current = sid; el.scrollTop = el.scrollHeight; prevHeight.current = el.scrollHeight; return; }
  if (prevHeight.current && el.scrollHeight > prevHeight.current) el.scrollTop += el.scrollHeight - prevHeight.current;
  prevHeight.current = el.scrollHeight;
}, [messages.length, sid]);
```

## 适配指南

- 嵌入页就是个壳——所有视觉走 widget 的 `renderShell + styles.ts`，确保 iframe / script widget 视觉完全一致，唯一区别是 fullscreen（占满 + 不渲气泡 + 永远 open）
- 会话详情用 `space-y-5` + 78% 宽（比 widget 的 88% 窄、比 playground 间距大），气泡 trace 按钮是"溯源"入口（点开 TraceDrawer）
- 反向分页：先取 total（1 行）定位最后一页（最新），`useInfiniteQuery` 从最新页递减加载，滚到顶（`scrollTop <= 48`）触发 `fetchNextPage`，加载后用 scrollHeight 差值保持视口
- 编辑 / 重新生成走 MessageActions（user 可编辑、assistant 可重生）

## 反模式

- ❌ 嵌入页自己写一套对话 UI——必须复用 widget shell（避免 iframe / script 视觉漂移）
- ❌ fullscreen panel 留圆角 / 阴影 / transform——iframe 里会露父容器边
- ❌ 气泡四角全圆——必须保留"贴近一侧"的小直角（user `rounded-tr-sm` / assistant `rounded-tl-sm`）
- ❌ 长会话一次性渲染全部消息——用反向分页 + 滚动锚定
- ❌ trace / 编辑按钮常驻——trace 常显，编辑/重生 hover 才露（`opacity-0 group-hover/msg:opacity-100`）
