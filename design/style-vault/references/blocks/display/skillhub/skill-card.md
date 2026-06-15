---
id: blocks/display/skillhub/skill-card
type: block
name: Skill 卡片
description: 字母头像 + 版本胶囊 + 3 项 stats + 底部分隔线 + hover 边框变 teal + y:-4 浮起
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/skillhub/skillhub-teal-mist
  - tokens/shadow/skillhub/ambient-float
  - tokens/motion/skillhub/gentle-flow
  - components/avatars-icons/skillhub/letter-avatar
preview: /preview/blocks/display/skillhub/skill-card
---

# Skill Card

> 列表里的单个技能卡——把"一个 Skill"需要传达的信息（标识 + 描述 + 3 项指标）压到一张卡上；hover 时微微浮起 + 边框变 teal

## 视觉特征

- 容器：`bg-white rounded-2xl p-5 border border-gray-200 flex flex-col`
- 头部：`flex items-start gap-3 mb-3`
  - 左：40×40 `LetterAvatar`
  - 右：标题 `text-sm font-bold text-gray-900 truncate` + 版本号 slate 胶囊
- 描述：`text-gray-500 text-[13px] leading-relaxed line-clamp-2 mb-4 flex-1`
- Stats 行：`flex items-center gap-4 text-xs text-gray-400 font-medium pt-3 border-t border-gray-100`
  - 3 项：点赞 Heart / 使用 Users / 讨论 MessageCircle（`size={12}`）
- Hover 状态：`hover:border-teal-200 hover:shadow-md` + framer-motion `y: -4`
- 标题 hover：`group-hover:text-slate-500`（整张卡 group，标题跟随变色）

## 核心代码

```tsx
import { Heart, Users, MessageCircle } from 'lucide-react';
import { motion } from 'framer-motion';
import { LetterAvatar } from '../components/avatars-icons/LetterAvatar';

interface SkillCardProps {
  name: string;
  summary: string | null;
  version?: string;
  stats?: { likeCount?: number; usedCount?: number; commentCount?: number };
  /** 用于 LetterAvatar 的全局 index（分页切换下保持稳定） */
  avatarIndex: number;
  onClick?: () => void;
}

export const SkillCard = ({
  name, summary, version, stats, avatarIndex, onClick,
}: SkillCardProps) => (
  <motion.div
    whileHover={{ y: -4 }}
    transition={{ duration: 0.2 }}
    onClick={onClick}
    className="group bg-white rounded-2xl p-5 border border-gray-200
               hover:border-teal-200 hover:shadow-md
               transition-all duration-200 cursor-pointer flex flex-col"
  >
    {/* 头部 */}
    <div className="flex items-start gap-3 mb-3">
      <LetterAvatar name={name} index={avatarIndex} />
      <div className="min-w-0 flex-1">
        <h4 className="text-sm font-bold text-gray-900
                       group-hover:text-slate-500 transition-colors truncate">
          {name}
        </h4>
        {version && (
          <span className="text-[10px] font-semibold text-slate-500
                           bg-slate-50 px-1.5 py-0.5 rounded mt-0.5 inline-block">
            v{version}
          </span>
        )}
      </div>
    </div>

    {/* 描述 */}
    <p className="text-gray-500 text-[13px] leading-relaxed line-clamp-2 mb-4 flex-1">
      {summary || '暂无描述。'}
    </p>

    {/* Stats */}
    <div className="flex items-center gap-4 text-xs text-gray-400 font-medium
                    pt-3 border-t border-gray-100">
      <span className="flex items-center gap-1" title="点赞">
        <Heart size={12} /> {stats?.likeCount ?? 0}
      </span>
      <span className="flex items-center gap-1" title="已使用">
        <Users size={12} /> {stats?.usedCount ?? 0}
      </span>
      <span className="flex items-center gap-1" title="讨论">
        <MessageCircle size={12} /> {stats?.commentCount ?? 0}
      </span>
    </div>
  </motion.div>
);
```

## 使用示例

```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
  {skills.map((skill, i) => (
    <SkillCard
      key={skill.id}
      name={skill.name}
      summary={skill.summary}
      version={skill.version}
      stats={skill.stats}
      avatarIndex={(page - 1) * pageSize + i}
      onClick={() => navigate(`/skills/${skill.slug}`)}
    />
  ))}
</div>
```

## 骨架态

```tsx
// 加载中的骨架占位——同尺寸 rounded-2xl + animate-pulse
<div className="h-48 bg-white border border-gray-100 rounded-2xl animate-pulse" />
```

## 适配指南

- `avatarIndex` 必须是 **全局稳定索引**：`(page - 1) * ITEMS_PER_PAGE + i`，保证翻页后头像色不会跳
- 描述用 `line-clamp-2`——保证所有卡等高；没描述就 fallback 一句"暂无描述。"
- stats 3 项是硬约束：多于 3 项就进 tooltip 或挪出卡；少于 3 项保持 3 个图标位即可（数字为 0）
- hover 的 `y: -4` 跟 `hover:shadow-md` 有冲突时，只留 motion（shadow 也会动）—— Tailwind 的 `hover:shadow-md` 只是保险
- 不同层级的 description 改 `text-[13px]` 为 `text-sm` 可以略重——但别超过主标题字重
- 版本号 `v` 前缀不是硬的，但 skillhub 的风格一贯带前缀

## 反模式

- 不要用 `text-gray-900` 作为描述色——会和标题打架
- 不要给卡加背景图/渐变——会和 hero 的流光 CTA 争戏
- 不要 hover 改 scale——只改 y，别把按钮的 scale 逻辑挪过来
- 不要把 stats 改成垂直排列——4 列 grid 到底部分隔线的水平节奏会塌
