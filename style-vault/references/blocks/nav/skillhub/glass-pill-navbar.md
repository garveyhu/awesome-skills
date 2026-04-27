---
id: blocks/nav/skillhub/glass-pill-navbar
type: block
name: 玻璃 Pill 导航栏
description: 玻璃层 + 内嵌白色圆角 pill + 3 列 grid（品牌 / 中心导航 / 鉴权）
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/skillhub/skillhub-teal-mist
  - tokens/shadow/skillhub/ambient-float
preview: /preview/blocks/nav/skillhub/glass-pill-navbar
---

# Glass Pill Navbar

> 顶部导航两层结构：外层毛玻璃（`bg-white/80 backdrop-blur-lg`）横铺全宽，内层白色 2xl 圆角 pill 把品牌 / 中心导航 / 鉴权三个区块 grid 成 3 列

## 视觉特征

- **外层 sticky（仅发现页/首页）** + `z-50` + 垂直 `py-3` + 横向 `px-4 sm:px-6 lg:px-8`
- 外层背景：`bg-white/80 backdrop-blur-lg`（玻璃）
- 内层 pill：`max-w-6xl mx-auto bg-white rounded-2xl shadow-[0_1px_4px_rgba(0,0,0,0.04)] border border-gray-100 px-5`
- pill 内：`grid grid-cols-3 items-center h-14`——三列，等宽，左/中/右三区块用 `justify-self-start/center/end` 自我对齐
- 品牌：favicon 7×7 + 粗体 `SkillHub` 标题，hidden sm:block（小屏仅显示 logo）
- 导航链接：`px-4 py-1.5 rounded-lg text-sm font-medium`
  - 激活：`!bg-[#2b2b2b] !text-white/95`（近黑色胶囊）
  - 默认：`!text-[#666]`
  - hover：`!text-[#1a1a1a] hover:bg-black/5`
- 中心导航 hidden md:flex（移动端走底部 tab bar，不在 header）
- 未读消息红点：`absolute -top-1 -right-1 w-1.5 h-1.5 rounded-full bg-orange-500`
- 鉴权区按钮：登录 `bg-[#1a1a1a] text-white rounded-xl px-4 py-1.5 active:scale-95`

## 核心代码

```tsx
import { NavLink, useLocation, useNavigate } from 'react-router-dom';
import { Compass, Sparkles, Upload, MessageSquare, Settings, User } from 'lucide-react';

type NavItem = {
  to: string;
  label: string;
  icon: React.ReactNode;
  badge?: boolean;  // 有红点
  authOnly?: boolean;
  adminOnly?: boolean;
};

interface GlassPillNavbarProps {
  brandName?: string;
  logoSrc?: string;
  items: NavItem[];
  isAuthenticated: boolean;
  isAdmin?: boolean;
  hasUnread?: boolean;
  user?: { nickname?: string; avatarUrl?: string };
  sticky?: boolean;  // 是否随路由开关 sticky
}

const navLinkClass = ({ isActive }: { isActive: boolean }) =>
  `flex items-center gap-1.5 px-4 py-1.5 rounded-lg text-sm font-medium whitespace-nowrap transition-all duration-200 ${
    isActive
      ? '!bg-[#2b2b2b] !text-white/95'
      : '!text-[#666] hover:!text-[#1a1a1a] hover:bg-black/5'
  }`;

export const GlassPillNavbar = ({
  brandName = 'SkillHub',
  logoSrc = '/favicon.svg',
  items,
  isAuthenticated,
  isAdmin = false,
  hasUnread = false,
  user,
  sticky = false,
}: GlassPillNavbarProps) => {
  const navigate = useNavigate();

  return (
    <header
      className={`${sticky ? 'sticky top-0' : ''} z-50 w-full py-3 px-4 sm:px-6 lg:px-8 bg-white/80 backdrop-blur-lg`}
    >
      <div className="max-w-6xl mx-auto bg-white rounded-2xl
                      shadow-[0_1px_4px_rgba(0,0,0,0.04)]
                      border border-gray-100 px-5">
        <div className="grid grid-cols-3 items-center h-14">
          {/* 品牌 */}
          <button
            onClick={() => navigate('/')}
            className="flex items-center gap-2.5 justify-self-start cursor-pointer"
          >
            <img src={logoSrc} alt={brandName} className="w-7 h-7" />
            <span className="font-bold text-base tracking-tight text-[#1a1a1a] hidden sm:block">
              {brandName}
            </span>
          </button>

          {/* 中心导航 */}
          <nav className="hidden md:flex gap-1 justify-self-center">
            {items
              .filter((i) => (!i.authOnly || isAuthenticated) && (!i.adminOnly || isAdmin))
              .map((item) => (
                <NavLink key={item.to} to={item.to} className={navLinkClass}>
                  {({ isActive }) => (
                    <span className="flex items-center gap-1.5">
                      <span className="relative">
                        {item.icon}
                        {item.badge && hasUnread && (
                          <span
                            className={`absolute -top-1 -right-1 w-1.5 h-1.5 rounded-full ${
                              isActive ? 'bg-orange-300' : 'bg-orange-500'
                            }`}
                          />
                        )}
                      </span>
                      {item.label}
                    </span>
                  )}
                </NavLink>
              ))}
          </nav>

          {/* 鉴权区 */}
          <div className="flex items-center gap-3 justify-self-end">
            {isAuthenticated ? (
              <button
                onClick={() => navigate('/me')}
                className="flex items-center gap-2 px-3 py-1.5 rounded-xl
                           hover:bg-black/[0.03] transition-all
                           text-sm font-medium text-[#555] cursor-pointer"
              >
                {user?.avatarUrl
                  ? <img src={user.avatarUrl} className="w-[22px] h-[22px] rounded-full object-cover" />
                  : <div className="w-[22px] h-[22px] rounded-full bg-[#eee] flex items-center justify-center">
                      <User size={13} className="text-[#999]" />
                    </div>
                }
                <span className="hidden sm:block max-w-[100px] truncate">
                  {user?.nickname || '用户'}
                </span>
              </button>
            ) : (
              <NavLink
                to="/login"
                className="flex items-center gap-2 px-4 py-1.5 rounded-xl
                           bg-[#1a1a1a] text-white text-sm font-medium
                           hover:bg-[#333] transition-all active:scale-95"
              >
                <span>登录</span>
              </NavLink>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};
```

## 使用示例

```tsx
<GlassPillNavbar
  brandName="SkillHub"
  items={[
    { to: '/discover', label: '发现', icon: <Compass size={15} /> },
    { to: '/practice', label: '社区', icon: <Sparkles size={15} /> },
    { to: '/publish',  label: '发布', icon: <Upload size={15} />, authOnly: true },
    { to: '/messages', label: '消息', icon: <MessageSquare size={15} />, authOnly: true, badge: true },
    { to: '/admin',    label: '管理', icon: <Settings size={15} />, adminOnly: true },
  ]}
  isAuthenticated={isAuth}
  isAdmin={isAdmin}
  hasUnread={hasUnread}
  user={user}
  sticky={location.pathname === '/' || location.pathname === '/discover'}
/>
```

## 适配指南

- sticky 只在 landing/discover 开；其它页（如 messages）要保证不遮内容时关掉
- pill `max-w-6xl` 可改 `max-w-7xl`，但超过 1280 之后 3 列会变松散——补一个 `gap-24` 或改栅格
- 暗色站把外层 `bg-white/80` → `bg-slate-900/85` + 内层 `bg-slate-900` + border `border-white/10`
- 移动端隐藏中心导航（`hidden md:flex`），配合 `blocks/nav/mobile-tab-bar` 走底部 tab bar
- 未读红点颜色跟随 active 状态变浅（`bg-orange-300` vs `bg-orange-500`），保证黑底胶囊上仍然可见

## 反模式

- 不要给外层加 `border-b`——它已经靠玻璃+阴影分层，再加边线就"厚"了
- 不要让 pill 宽度吃满外层——`max-w-6xl mx-auto` 是关键，制造"浮在中间"的空间感
- 不要把 grid-cols-3 改成 flex justify-between——内容宽度不等时中心导航会偏
- 不要在 active 胶囊里用 teal-500——teal 给内容交互（搜索/分页），nav 激活保留 slate 系
