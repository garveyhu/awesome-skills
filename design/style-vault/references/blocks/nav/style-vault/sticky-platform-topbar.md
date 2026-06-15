---
id: blocks/nav/style-vault/sticky-platform-topbar
type: block
name: Sticky 平台切换顶栏
description: sticky bg-white/95 backdrop-blur 顶栏 · 浏览/产品集 路径激活下划线 nav + 搜索胶囊触发器 + 视口绝对居中的 platform underline tab + 右侧登录/头像
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
  - blocks/search/style-vault/cmd-k-search-panel
preview: /preview/blocks/nav/style-vault/sticky-platform-topbar
---

# Sticky Platform TopBar

> Style Vault 的全站顶栏：sticky 玻璃感 + 视口绝对居中的平台切换 + 右侧账号

## 视觉特征

**容器**：`sticky top-0 z-50 border-b border-slate-100 bg-white/95 backdrop-blur-xl`，高度 72px，padding `px-10`

**三段布局（关键技巧）**：
```
[ Logo + 浏览/产品集 nav + 搜索胶囊 ]  [ flex-1 撑开 ]  [ 登录/头像 ]
        ←------- 视口绝对居中的 platform pill（独立绝对定位层） -------→
```

- 左：logo 36×36 + 主导航 `浏览 / 产品集` **路径激活下划线 nav**（复用 `sv-underline-tab` 13px 小档，`data-on` 跟随 pathname）+ **搜索胶囊触发**
- 中：**绝对定位居中**——而不是用 flexbox space-between——`absolute inset-y-0 left-0 right-0 flex justify-center`，pointer-events-none 父 + pointer-events-auto 子 —— 这样 platform pill 永远在视口正中，不被左右内容拉扯
- 右：未登录 → `dark-pill-cta sm` "登录"；已登录 → 头像（带绿色在线指示点） + click 弹大 dropdown

### 主导航激活态（关键细节）

`浏览` / `产品集` 不是普通文本 link，是和平台切换、CategoryTabs 共用同一套 `.sv-underline-tab` 视觉语言：

- `data-on={pathname === '/browse' || pathname.startsWith('/browse/')}` 让 `/browse*` 都激活「浏览」
- 同理 `/products` / `/products/*` 激活「产品集」
- 永远有且仅有一个主入口高亮（路径不属于这两个域时两个都不亮，符合"我不在浏览/产品集语义"）

**对称 padding**：`.sv-underline-tab` 自带 `padding-bottom: 10px`（给下划线让位），用在 72px `items-center` 容器里时文字会偏上。配合 `pt-2.5`（10px）对称 padding-top 让文字盒视觉居中：

```tsx
<Link className="sv-underline-tab pt-2.5" data-on={...}>浏览</Link>
```

不加 `pt-2.5` 文字会比相邻搜索胶囊（`h-9` 36px）的几何中心高 5px，肉眼能看出来。

### 搜索胶囊（产品集右）

紧跟 `产品集` link 后，是触发全站搜索浮层的胶囊：

```
[⌕ 搜索风格]   ← rounded-full · h-9 · border-slate-200 · 玻璃白底 · 13px medium slate-500
              ← icon = `<SearchOutlined>` from @ant-design/icons · 14px
              ← hover：border-slate-300 + bg-white + text-slate-900
              ← click：searchPanel.open() · 唤起 cmd-k-search-panel
```

**有意不放快捷键提示**（`⌘K` badge / `Press / to search` 等）—— 视觉噪音，且实际很少用户被这种 hint 教学。快捷键工作但不显示，让 TopBar 保持极简。

icon 用 `<SearchOutlined />`（@ant-design/icons），14px 比 nav 文字稍小一档，不抢视觉。

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
        <Link
          to="/browse"
          className="sv-underline-tab pt-2.5"
          data-on={pathname === '/browse' || pathname.startsWith('/browse/')}
        >
          浏览
        </Link>
        <Link
          to="/products"
          className="sv-underline-tab pt-2.5"
          data-on={pathname === '/products' || pathname.startsWith('/products/')}
        >
          产品集
        </Link>
        <button
          type="button"
          onClick={() => searchPanel.open()}
          aria-label="搜索"
          className="inline-flex h-9 items-center gap-2 rounded-full border border-slate-200 bg-white/60 px-4 text-[13px] font-medium text-slate-500 transition hover:border-slate-300 hover:bg-white hover:text-slate-900"
        >
          <SearchOutlined className="text-[14px]" />
          搜索风格
        </button>
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
- 所有 nav text 13px medium slate-400/900（`.sv-underline-tab` 默认色）——**不要**升 14px（破坏紧凑感）
- 主导航 `pt-2.5` 是必填项，省略后文字会偏上 5px，和搜索胶囊不齐

## 反模式

- 不要用 `justify-between` 三栏布局——平台切换永远不会刚好在视口中央
- 不要把 sticky 高度撑到 80px+——侵占内容
- 不要去掉 `border-b border-slate-100`——blur 层和内容层之间需要 1px 切割
- 不要在 dropdown 内放分隔线 + 大间距——保持紧凑菜单形态
