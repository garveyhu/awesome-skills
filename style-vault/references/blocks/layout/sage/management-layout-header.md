---
id: blocks/layout/sage/management-layout-header
type: block
name: 管理页头
description: title + 搜索 + filter slot + rightActions 的通用管理后台 header，注入 ConfigProvider 主题色
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/sage/twelve-theme-spectrum
preview: /preview/blocks/layout/sage/management-layout-header
---

# Management Layout Header

> sage 所有管理后台页面的统一 header（UserManagement / RoleManagement / RuleSetManagement / Collections / Spaces 都用）。`ManagementLayout` 是个 wrapper：title + 搜索 input + filter slot + rightActions（通常是"+ 新建"按钮）。整个容器外面有 ConfigProvider 把 antd 默认色注入主题色。

## 视觉特征

- 容器：`p-6` 左右上下 24px padding
- header 行：`mb-4 flex justify-between items-center`
- title：`text-2xl font-bold text-slate-800`
- 右侧：`flex items-center gap-3`
- 搜索 input：`w-[200px] ${themeClasses.borderFocusWithin} ${themeClasses.ringFocusWithin}` + suffix 是 search icon button
- filter slot：用户传入（如 ant Select）
- rightActions slot：通常是 `<Button type="primary" icon={<Plus />}>新建</Button>` (Plus from lucide)
- ConfigProvider 注入：`token: { colorPrimary: themeHex, borderRadius: 8 }` + 各组件 `colorPrimary / colorPrimaryHover / colorPrimaryActive` 全设主题色，`controlOutline: 'transparent'` 去掉 ring，`boxShadow: 'none'`

## 核心代码

```tsx
import { ConfigProvider, Input } from 'antd';
import { Search } from 'lucide-react';
import { THEME_CLASSES, THEME_HEX_COLORS } from '@/core/utils/themeUtils';

export function ManagementLayout({
  title, searchPlaceholder = 'Search…', onSearch, filter, rightActions, children, themeColor = 'gray',
}) {
  const tc = THEME_CLASSES[themeColor];
  const hex = THEME_HEX_COLORS[themeColor];
  const [v, setV] = useState('');

  return (
    <ConfigProvider
      theme={{
        token: { colorPrimary: hex, colorLink: hex, colorLinkHover: hex, borderRadius: 8 },
        components: {
          Button: { colorPrimary: hex, colorPrimaryHover: hex, colorPrimaryActive: hex, controlOutline: 'transparent', boxShadow: 'none', boxShadowSecondary: 'none' },
          Input: { colorPrimary: hex, controlOutline: 'transparent' },
          Select: { colorPrimary: hex, controlOutline: 'transparent' },
          Table: { colorPrimary: hex },
          Tag: { colorPrimary: hex },
          Modal: { colorPrimary: hex },
        },
      }}
    >
      <div className="p-6">
        <div className="mb-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-slate-800">{title}</h1>
          <div className="flex items-center gap-3">
            {filter}
            {onSearch && (
              <Input
                placeholder={searchPlaceholder}
                value={v}
                onChange={e => setV(e.target.value)}
                onPressEnter={() => onSearch(v)}
                className={`w-[200px] ${tc.borderFocusWithin} ${tc.ringFocusWithin}`}
                allowClear
                suffix={<Search size={16} className={`text-gray-400 cursor-pointer ${tc.textHover}`} onClick={() => onSearch(v)} />}
              />
            )}
            {rightActions}
          </div>
        </div>
        {children}
      </div>
    </ConfigProvider>
  );
}
```

## 适配指南

- 调用：`<ManagementLayout title="规则管理" onSearch={...} themeColor={themeColor} rightActions={<Button>新建</Button>}>... <Table /> ...</ManagementLayout>`
- ConfigProvider 必须在 ManagementLayout 内部（不在外面），保证子树所有 antd 组件都拿到主题
- 不要把 children 拆成 `<div className="management-body">` 这种壳——直接交给 children，让业务自己布局

## 反模式

- ❌ 把 search input 用 lucide 直接做 —— Antd Input 有完整的 allowClear / clearIcon 体验，自己造会缺东西
- ❌ 不注入 ConfigProvider —— 表格 / 按钮会回到 antd 默认蓝
