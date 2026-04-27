---
id: blocks/nav/sage/space-switcher-dropdown
type: block
name: 空间切换下拉
description: LayoutGrid icon + Antd Dropdown + 当前空间高亮（注入 selectionColor 背景 + Check 图标）
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/sage/twelve-theme-spectrum
preview: /preview/blocks/nav/sage/space-switcher-dropdown
---

# Space Switcher Dropdown

> sage 是多 workspace 系统，侧栏第二格是空间切换器——LayoutGrid 图标 + 当前空间名（截断 max-w-160）+ ChevronDown。点开 Antd Dropdown：`group` 分组列表 + 选中项注入 `THEME_SELECTION_COLORS[themeColor]` 作背景 + Check icon；如管理员还有 divider + 管理入口。

## 视觉特征

- 触发按钮：`w-full flex items-center justify-between gap-2 px-3 py-2 rounded-lg transition-all duration-200 text-slate-500 hover:bg-[rgb(237,237,237)] border-none ${themeClasses.textHover}`
- 左侧：`<LayoutGrid size={18} />` (slate-500) + `font-semibold text-sm truncate`（loading 时换成 antd Spin 用主题色）
- 右侧：`<ChevronDown size={14} className="text-slate-400 flex-shrink-0" />`
- Dropdown popup：`maxHeight: 400px overflowY: auto backgroundColor: rgb(249, 249, 249)`（手设 inline style 覆盖 antd 默认白底）
- 列表项 label：`flex items-center justify-between w-full min-w-[180px] py-1` + 截断 max-w-160
- 选中项 inline style：`backgroundColor: ${selectionColor} (e.g. #99f6e4 teal-200)`
- 选中项 className：`font-medium`
- 选中右侧 Check：`size={14} className={tc.text}`
- 管理员入口：`type: 'divider'` + `{ key: 'manage-spaces', icon: <Settings size={14} />, label: '管理工作区' }`

## 核心代码

```tsx
import { ConfigProvider, Dropdown } from 'antd';
import { Check, ChevronDown, LayoutGrid, Settings } from 'lucide-react';
import { THEME_CLASSES, THEME_HEX_COLORS, THEME_SELECTION_COLORS } from '@/core/utils/themeUtils';

const tc = THEME_CLASSES[themeColor];
const primaryColor = THEME_HEX_COLORS[themeColor];
const selectionColor = THEME_SELECTION_COLORS[themeColor];

const items = [
  {
    key: 'spaces-group', type: 'group', label: '我的工作区',
    children: spaces.map(space => ({
      key: space.id,
      label: (
        <div className="flex items-center justify-between w-full min-w-[180px] py-1">
          <span className="truncate max-w-[160px]">{space.name}</span>
          {currentSpace?.id === space.id && <Check size={14} className={tc.text} />}
        </div>
      ),
      onClick: () => handleSpaceClick(space.id),
      className: currentSpace?.id === space.id ? 'font-medium' : '',
      style: currentSpace?.id === space.id ? { backgroundColor: selectionColor } : {},
    })),
  },
  ...(isAdmin ? [
    { type: 'divider' as const },
    { key: 'manage', icon: <Settings size={14} />, label: '管理工作区', onClick: () => navigate('/spaces') },
  ] : []),
];

<Dropdown
  menu={{ items, style: { maxHeight: 400, overflowY: 'auto', backgroundColor: 'rgb(249, 249, 249)' } }}
  trigger={['click']}
>
  <button className={`w-full flex items-center justify-between gap-2 px-3 py-2 rounded-lg transition-all duration-200 text-slate-500 hover:bg-[rgb(237,237,237)] border-none ${tc.textHover}`}>
    <div className="flex items-center gap-2 overflow-hidden">
      <LayoutGrid size={18} className="text-slate-500" />
      {loading
        ? <ConfigProvider theme={{ token: { colorPrimary: primaryColor } }}><Spin size="small" /></ConfigProvider>
        : <span className="font-semibold text-sm truncate">{currentSpace?.name || '选择工作区'}</span>}
    </div>
    <ChevronDown size={14} className="text-slate-400 flex-shrink-0" />
  </button>
</Dropdown>
```

## 适配指南

- AntD Dropdown 不支持 group label 自定义，所以 group label 文本走 antd i18n
- 切换空间会触发 `window.location.href = '/chat'` 硬刷新，确保 SpaceContext 重读 storage
- selectionColor 是 200 阶 alpha 色，不会和文字撞色

## 反模式

- ❌ 用 Tailwind 给选中项染色 —— Antd Dropdown 内部不能直接 className 控制 menu item 背景
- ❌ 移除 hardcoded `backgroundColor: 'rgb(249, 249, 249)'` —— Antd 默认白底跟侧栏对不齐
