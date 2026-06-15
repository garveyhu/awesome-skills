---
id: blocks/layout/style-vault/browser-chrome-frame
type: block
name: 浏览器 Chrome 预览框
description: mac 红黄绿 dot + slate-50 chrome bar + 居中标题 · 内嵌响应式视口预览
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial, skeuomorph]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/style-vault/slate-cyan-cool
  - tokens/typography/pairs/style-vault/inter-editorial-display
preview: /preview/blocks/layout/style-vault/browser-chrome-frame
---

# Browser Chrome Frame

> 详情页右列的预览容器：mac 风浏览器 chrome 包住可调视口（375 / 768 / 1024 / 1440 / full）的真实组件

## 视觉特征

**容器**：`overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm`，外层 16px 圆角

**Chrome 顶栏**：`flex items-center gap-2 border-b border-slate-100 bg-slate-50 px-4 py-2.5`
- 左：mac 红黄绿三圆 `h-3 w-3 rounded-full bg-[#ff5f57] / #febc2e / #28c840`
- 中：当前条目名 `text-[12px] font-medium text-slate-500 truncate`
- 右：`w-16` 占位（保持顶栏对称）

**预览区**：`flex justify-center bg-slate-50 p-4`，内层 `max-w-{viewport}`，`overflow-auto rounded-md border border-slate-200 bg-white`，`maxHeight: 72vh`，`transition: max-width 240ms ease`

**视口选择器**（顶部独立工具条，不在 chrome 内）：

形态走 antd `<Select>` 大尺寸下拉（**不是 inline button group**），关键参数：
- `size="large"` · `style={{ width: 200 }}` · `popupMatchSelectWidth={200}`
- `suffixIcon={null}` —— 去掉默认 chevron，让胶囊视觉更干净
- 5 档 option：375 手机 · 768 平板 · 1024 桌面 · 1440 大屏 · full 全宽
- 每条 option 三段 layout：
  - `h-6 w-6 rounded-md bg-slate-100 text-slate-600` icon 容器（mobile/tablet/desktop/expand 图标）
  - `flex-1 text-[13px] font-medium` 中文标签
  - `text-[11px] text-slate-400` 右对齐 px 值（如 `375 px` / `响应式`）

右侧 `全屏预览` 走 ghost-bordered-cta md 档；最右边 `ml-auto` 是当前视口标记 —— `h-1.5 w-1.5 rounded-full bg-emerald-500` 小绿点 + `text-[12px] text-slate-400` 文字。

## 核心代码骨架

```tsx
const VIEWPORT_OPTIONS = [
  { value: 375,    label: '手机', desc: '375 px' },
  { value: 768,    label: '平板', desc: '768 px' },
  { value: 1024,   label: '桌面', desc: '1024 px' },
  { value: 1440,   label: '大屏', desc: '1440 px' },
  { value: 'full', label: '全宽', desc: '响应式' },
];

return (
  <div className="space-y-4">
    {/* viewport toolbar */}
    <div className="flex items-center gap-3">
      <Select<ViewportKey>
        value={viewport}
        onChange={(v) => setViewport(v)}
        size="large"
        suffixIcon={null}
        popupMatchSelectWidth={200}
        style={{ width: 200 }}
        options={VIEWPORT_OPTIONS.map((v) => ({
          value: v.value,
          label: (
            <div className="flex items-center gap-2">
              <span className="flex h-6 w-6 items-center justify-center rounded-md bg-slate-100 text-slate-600">
                {v.icon}
              </span>
              <span className="flex-1 text-[13px] font-medium">{v.label}</span>
              <span className="text-[11px] text-slate-400">{v.desc}</span>
            </div>
          ),
        }))}
      />
      <button className="ghost-bordered-cta">全屏预览</button>
      <div className="ml-auto flex items-center gap-1 text-[12px] text-slate-400">
        <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
        {currentViewport.label}
      </div>
    </div>

    {/* browser chrome */}
    <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
      <div className="flex items-center gap-2 border-b border-slate-100 bg-slate-50 px-4 py-2.5">
        <div className="flex gap-1.5">
          <div className="h-3 w-3 rounded-full bg-[#ff5f57]" />
          <div className="h-3 w-3 rounded-full bg-[#febc2e]" />
          <div className="h-3 w-3 rounded-full bg-[#28c840]" />
        </div>
        <div className="flex-1 truncate text-center text-[12px] font-medium text-slate-500">{item.name}</div>
        <div className="w-16" />
      </div>
      <div className="flex justify-center bg-slate-50 p-4">
        <div className="overflow-auto rounded-md border border-slate-200 bg-white"
             style={{ maxWidth: viewport === 'full' ? '100%' : `${viewport}px`, width: '100%', maxHeight: '72vh', transition: 'max-width 240ms ease' }}>
          <PreviewComp />
        </div>
      </div>
    </div>
  </div>
);
```

## 适配指南

- **chrome 顶栏一定 `bg-slate-50` 而不是白**——从白卡到白预览之间需要这一档过渡，否则边界消失
- mac 红黄绿用 `#ff5f57 / #febc2e / #28c840` 准色——其它"橘色 / 偏蓝绿"会破坏 mac 文化标识
- 预览区 `p-4` slate-50 背景是为了让窄视口（375/768）有"左右留白"——别去掉
- viewport 切换 transition 仅 max-width，不要做高度动画——内容自然撑开就好
- 不要 chrome 顶栏放真"地址栏 input"——这是预览框不是浏览器

## 反模式

- 不要把 chrome 顶栏圆角拆掉（`rounded-2xl` 整体圆角是质感来源）
- 不要把 mac 三圆放右侧（windows 风）
- 不要给三圆加阴影或点点高光（变 skeuomorph 过头）
- 不要让 chrome 高度 < 36px——按钮区压不住
