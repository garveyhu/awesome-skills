---
id: components/avatars-icons/sage/themed-circle-avatar
type: component
name: 主题色头像
description: 圆形白底 + slate-200 描边 + 主题色 lucide 图标 + group-hover 旋转 12°
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [playful]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/sage/twelve-theme-spectrum
preview: /preview/components/avatars-icons/sage/themed-circle-avatar
---

# Themed Circle Avatar

> sage 用户头像不用首字母也不用照片，用 lucide 图标——`getAvatarIcon(avatar)` 从 `AVATARS` map 中查表（user / heart / cat / star / leaf 等几十种）。Hover 时整个图标 12° 旋转，是 sage 唯一的"俏皮"动作。

## 视觉特征

- 容器：`w-8 h-8 rounded-full bg-white border border-slate-200 flex items-center justify-center font-bold transition-transform duration-300`
- 群组：包裹在 `group` 父级，hover 触发 `group-hover:rotate-12`
- 图标：lucide-react，size 16-18，`className={themeClasses.text}` —— 和用户主题色绑定
- 选中态（avatar picker）：`${themeClasses.bg} text-white scale-110 shadow-sm` 
- 未选中：`bg-slate-100 text-slate-500 hover:bg-slate-200 hover:scale-105`
- 大尺寸（侧栏底部用户菜单）：`w-12 h-12 rounded-full ${themeClasses.iconBg}`

## 核心代码

```tsx
import { getAvatarIcon, AVATARS } from '@/core/utils/avatarUtils';
import { THEME_CLASSES } from '@/core/utils/themeUtils';

const UserAvatarIcon = getAvatarIcon(user.avatar);
const tc = THEME_CLASSES[themeColor];

// 默认（侧栏用户位）
<div className="flex items-center gap-3 group">
  <div className="w-8 h-8 rounded-full bg-white border border-slate-200 flex items-center justify-center font-bold transition-transform duration-300 group-hover:rotate-12">
    <UserAvatarIcon size={18} className={tc.text} />
  </div>
  <span className="text-sm font-medium text-slate-700 group-hover:text-slate-900 transition-colors">
    {user.username}
  </span>
</div>

// avatar picker 选中态
<button
  onClick={() => onSelect(name)}
  className={`w-8 h-8 rounded-full flex items-center justify-center transition-all ${
    selected
      ? `${tc.bg} text-white scale-110 shadow-sm`
      : 'bg-slate-100 text-slate-500 hover:bg-slate-200 hover:scale-105'
  }`}
>
  <Icon size={16} />
</button>
```

## 适配指南

- 头像图标按 `avatarUtils` 的 AVATARS map 注册，约 30 种 lucide 图标可选
- `group-hover:rotate-12` 必须配合 `transition-transform duration-300`，否则瞬间瞎转
- 不需要"组合"头像（叠 badge 等）——sage 头像只承担"我是谁"，不挂在线状态

## 反模式

- ❌ 用首字母 avatar —— sage 选 lucide 图标是为了"超过用户名长度限制时仍有视觉锚"
- ❌ rotate-12 用得过多 —— 这个动作只在用户 hover 自己的菜单时出现，过度使用会变 cheap
