---
id: blocks/nav/acme/saas-cold-topbar
type: block
name: 冷感 SaaS 顶栏
description: 56px 暗色顶栏 · 左 logo+breadcrumb · 中 ⌘K 命令面板入口 · 右 status pill+avatar
platforms: [web]
theme: dark
tags:
  aesthetic: [minimal, industrial]
  mood: [cold, serious]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/acme/slate-cyan-ice
  - tokens/typography/pairs/acme/ibm-plex-duo
  - components/indicators/acme/status-pulse
preview: /preview/blocks/nav/acme/saas-cold-topbar
---

# Cold SaaS Topbar

> ICEOPS / 监控型 SaaS 的全局顶栏：信息密度、零装饰、状态可见。

## 视觉特征

- 高度严格 56px；暗底 `#0f172a`；底边 1px `#1e293b`
- **左侧（240px）**：Logo（cyan dot + 大写品牌字）+ "/" 分隔 + breadcrumb（Plex Mono uppercase 11px）
- **中部弹性**：⌘K 命令面板触发器，伪输入框（占位 `Search incidents…`），左侧 search icon、右侧 `⌘K` kbd
- **右侧 Auto**：`<StatusPulse status="healthy" label="All systems operational" />` + 圆形 avatar（cyan 描边）
- 不要任何装饰：无 logo 阴影、无 hover bg 变化、无下拉箭头

**与 blocks/layout/skillhub/toolbar-bar 区分**：那条是表格上方的工具栏（搜索 + 筛选 + 新建按钮，跟着表格滚动），属页面内 section；本条是**全局**导航顶栏，跨页面 sticky。

## 核心代码

```tsx
import { StatusPulse } from '../../components/indicators/acme/status-pulse';

export function ColdSaasTopbar({
  brand = 'ICEOPS',
  breadcrumb = ['Monitoring', 'production'],
}: {
  brand?: string;
  breadcrumb?: string[];
}) {
  return (
    <header className="sticky top-0 z-40 h-14 bg-slate-950 border-b border-slate-800">
      <div className="h-full px-6 flex items-center gap-6">
        {/* brand + breadcrumb */}
        <div className="flex items-center gap-4 min-w-0">
          <div className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 rounded-full bg-cyan-400" />
            <span className="font-semibold tracking-wider text-slate-100">{brand}</span>
          </div>
          <span className="text-slate-700">/</span>
          <nav className="flex items-center gap-2 font-mono text-[11px] uppercase tracking-wider text-slate-400 truncate">
            {breadcrumb.map((seg, i) => (
              <span key={i} className="flex items-center gap-2">
                {i > 0 && <span className="text-slate-700">›</span>}
                <span className={i === breadcrumb.length - 1 ? 'text-slate-200' : ''}>{seg}</span>
              </span>
            ))}
          </nav>
        </div>

        {/* command palette */}
        <button className="flex-1 max-w-xl h-8 px-3 flex items-center gap-3 bg-slate-900 border border-slate-800 rounded text-[12px] text-slate-500 hover:border-slate-700 transition-colors duration-150 ease-out">
          <SearchIcon />
          <span className="flex-1 text-left">Search incidents, services, runbooks…</span>
          <kbd className="font-mono text-[10px] tracking-wider px-1.5 py-0.5 bg-slate-800 text-slate-400 rounded">
            ⌘K
          </kbd>
        </button>

        {/* right status + avatar */}
        <div className="flex items-center gap-4 ml-auto">
          <StatusPulse status="healthy" label="All systems operational" />
          <div className="w-8 h-8 rounded-full bg-slate-800 ring-1 ring-cyan-500/40" />
        </div>
      </div>
    </header>
  );
}

function SearchIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <circle cx="11" cy="11" r="7" /><path d="m20 20-3.5-3.5" />
    </svg>
  );
}
```

## 适配指南

- 永远 `sticky top-0`；上层页面 `pt-14` 让出
- 移动端 < 768px 把 breadcrumb 隐藏，仅留 brand + 漏斗 icon
- 命令面板触发器是**伪 input**（实际是按钮）—— 真正的输入交给 `cmdk` 弹层处理
- avatar ring 用 `cyan-500/40`（半透明），不要全实色——避免抢主品牌视觉

## 反模式

- 不要给 topbar 加阴影 / 渐变底
- 不要在 topbar 放 primary CTA（如"+ 新建"）—— 那应该在内容区上方
- 不要把 logo 做成图片（除非已是品牌标准）；纯文字 + cyan dot 是冷感 SaaS 的标志
