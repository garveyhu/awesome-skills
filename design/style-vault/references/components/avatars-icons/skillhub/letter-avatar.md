---
id: components/avatars-icons/skillhub/letter-avatar
type: component
name: 12 色柔和字母头像
description: 基于 index 的 12 色柔和轮转底色 + 白色粗体首字母的圆形头像
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/skillhub/skillhub-teal-mist
preview: /preview/components/avatars-icons/skillhub/letter-avatar
---

# Letter Avatar

> 没有真实头像时的 fallback——靠 12 色柔和调色板 + 白色粗体首字母形成可辨识但不抢眼的视觉标识

## 视觉特征

- 圆形（`rounded-full`），默认 40×40（`w-10 h-10`）
- 首字母：白色 / 粗体（`font-bold`）/ 16px（`text-base`）
- 背景色从 12 色轮盘按 index 取：`AVATAR_COLORS[index % 12]`
- 不允许被压缩：`shrink-0`
- 居中对齐：`flex items-center justify-center`

## 核心代码

```tsx
const AVATAR_COLORS = [
  '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
  '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9',
  '#F8C471', '#82E0AA',
];

type LetterAvatarProps = {
  name: string;
  index: number;
  size?: number;           // 默认 40
};

const LetterAvatar = ({ name, index, size = 40 }: LetterAvatarProps) => {
  const letter = (name || '?').charAt(0).toUpperCase();
  const bg = AVATAR_COLORS[index % AVATAR_COLORS.length];
  return (
    <div
      className="rounded-full flex items-center justify-center
                 text-white font-bold shrink-0"
      style={{ backgroundColor: bg, width: size, height: size, fontSize: size * 0.4 }}
    >
      {letter}
    </div>
  );
};
```

## 变体

### 小号（表格内 24×24）

```tsx
<LetterAvatar name={user.name} index={idx} size={24} />
```

小号下 `fontSize` 自动按 0.4 倍缩到 ~10px，仍可辨识。

### 与真实头像互斥的 fallback 组合

```tsx
{avatarUrl
  ? <img src={avatarUrl} className="w-10 h-10 rounded-full object-cover shrink-0" />
  : <LetterAvatar name={user.nickname} index={idx} />}
```

## 适配指南

- `index` 最稳定的取值来源是**列表的 global index**（`(page - 1) * pageSize + i`），这样分页切换时同一条数据的头像色不会变
- 不要用 `user.id % 12` 做 index——id 可能不连续，色分布会集中到某几色
- 12 色是经过配色调优的"柔和但可辨识"集，替换要整组替换，不要只改 1-2 色
- 配大号（48-56）时把 `font-bold` 升 `font-extrabold`，字形更稳

## 反模式

- 不要把 index 替换成 `Math.random()`——同一用户每次渲染会变色
- 不要给头像加 border——12 色已经自带边界
- 不要用 `object-cover` 配字母头像（那是给图片的）
- 不要做 hover 变色——它不是交互元素
