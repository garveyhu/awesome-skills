---
id: blocks/nav/style-vault/sticky-platform-topbar
type: block
name: Sticky 平台切换顶栏
description: sticky bg-white/95 backdrop-blur 顶栏 + 视口绝对居中的 platform underline tab + 右侧登录 / 头像
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/style-vault/slate-cyan-cool
  - tokens/typography/pairs/style-vault/inter-editorial-display
  - components/buttons/style-vault/dark-pill-cta
  - components/toggles/style-vault/editorial-underline-tab
preview: /preview/blocks/nav/style-vault/sticky-platform-topbar
---

# Sticky Platform TopBar

> Style Vault 的全站顶栏：sticky 玻璃感 + 视口绝对居中的平台切换 + 右侧账号

## 视觉特征

**容器**：`sticky top-0 z-50 border-b border-slate-100 bg-white/95 backdrop-blur-xl`，高度 72px，padding `px-10`

**三段布局（关键技巧）**：
```
[ Logo + 浏览/产品集 nav ]   [ flex-1 撑开 ]   [ 登录/头像 ]
        ←------- 视口绝对居中的 platform pill（独立绝对定位层） -------→
```

- 左：logo 36×36 + 主导航 `浏览 / 产品集` 文本 nav（13px medium slate-600 → hover slate-900）
- 中：**绝对定位居中**——而不是用 flexbox space-between——`absolute inset-y-0 left-0 right-0 flex justify-center`，pointer-events-none 父 + pointer-events-auto 子 —— 这样 platform pill 永远在视口正中，不被左右内容拉扯
- 右：未登录 → `dark-pill-cta sm` "登录"；已登录 → 头像（带绿色在线指示点） + click 弹大 dropdown

**Logo hover**：`scale-105` 300ms transition

**右侧 dropdown**（已登录态）：
- 卡片 `rounded-2xl border border-slate-200 shadow-[0_20px_48px_-16px_rgba(15,23,42,0.24)]` —— 大尺寸软投影
- 头像区 56×56 大头像 + 名字粗体，整块可点跳 /profile
- 菜单项 `rounded-lg hover:bg-slate-50`

**显示规则**：platform pill 仅在 `/browse*` 和 `/products` 路径出现 —— 其他页面（如 /profile / /item/*）只显 logo + nav + 账号

## 核心代码骨架

```tsx
function shouldShowPlatformPill(pathname: string) {
  if (pathname === '/browse') return true;
  if (pathname.startsWith('/browse/')) return true;
  if (pathname === '/products') return true;
  return false;
}

return (
  <header className="sticky top-0 z-50 border-b border-slate-100 bg-white/95 backdrop-blur-xl">
    <div className="relative flex h-[72px] items-center gap-8 px-10">
      {/* logo + nav */}
      <Link to="/" className="group shrink-0">
        <img src="/logo.svg" className="h-9 w-9 transition-transform duration-300 group-hover:scale-105" />
      </Link>
      <nav className="hidden items-center gap-7 md:flex">
        <Link to="/browse" className="text-[13px] font-medium text-slate-600 hover:text-slate-900">浏览</Link>
        <Link to="/products" className="text-[13px] font-medium text-slate-600 hover:text-slate-900">产品集</Link>
      </nav>

      {/* spacer */}
      <div className="flex-1" />

      {/* CENTER · platform pill 视口绝对居中 */}
      {showPlatformPill && (
        <div className="pointer-events-none absolute inset-y-0 left-0 right-0 hidden items-center justify-center md:flex">
          <div className="pointer-events-auto inline-flex items-baseline gap-7">
            {(['web', 'ios', 'android'] as const).map((p) => (
              <button key={p} className="sv-underline-tab" data-on={platform === p} onClick={() => setPlatform(p)}>
                {p === 'web' ? 'Web' : p === 'ios' ? 'iOS' : 'Android'}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* right · login / avatar */}
      <div className="flex items-center gap-2">
        {user ? <AvatarDropdown /> : <button className="dark-pill-cta-sm">登录</button>}
      </div>
    </div>
  </header>
);
```

## 适配指南

- **必须** `pointer-events-none` 父 + `pointer-events-auto` 子——否则中间 absolute 层会拦下 logo 区点击
- 高度严格 72px——配合 `min-h-[calc(100vh-72px)]` 的 hero / `top-[72px]` 的 sticky CategoryTabs
- 玻璃感来自 `bg-white/95 backdrop-blur-xl`——8% 半透 + 强 blur，hero blob 浮过时既能透出又不糊
- 所有 nav text 13px medium slate-600/900——**不要**升 14px（破坏紧凑感）

## 反模式

- 不要用 `justify-between` 三栏布局——平台切换永远不会刚好在视口中央
- 不要把 sticky 高度撑到 80px+——侵占内容
- 不要去掉 `border-b border-slate-100`——blur 层和内容层之间需要 1px 切割
- 不要在 dropdown 内放分隔线 + 大间距——保持紧凑菜单形态
