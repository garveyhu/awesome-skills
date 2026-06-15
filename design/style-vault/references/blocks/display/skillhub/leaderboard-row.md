---
id: blocks/display/skillhub/leaderboard-row
type: block
name: 榜单行
description: 4 列网格榜单行——#秩 / 名称+描述 / 分类 pill / stats；Top3 用红黄蓝高亮
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/skillhub/skillhub-teal-mist
  - tokens/motion/skillhub/gentle-flow
  - components/avatars-icons/skillhub/letter-avatar
  - components/tags-badges/skillhub/teal-pill
preview: /preview/blocks/display/skillhub/leaderboard-row
---

# Leaderboard Row

> 首页"精选 TOP Skills 榜单"的单行——4 列 grid 把 #秩 / 名称+简介 / 分类 / 指标 对齐；Top3 的 # 用红黄蓝，4 名及后用 slate-300

## 视觉特征

- Grid：`grid grid-cols-[40px_1fr_100px_180px] md:grid-cols-[40px_1fr_100px_200px]`
  - col 1（40px）：# 秩
  - col 2（1fr）：名称 + 描述 + 头像
  - col 3（100px）：分类 pill
  - col 4（180/200px）：3 项 stats 右对齐
- 行内 padding `px-4 py-3`；行间 `border-b border-gray-50 last:border-b-0`
- Hover：`hover:bg-slate-50/60`（非常轻的 zebra）+ `cursor-pointer`
- 秩号：`text-lg font-extrabold`，前 3 名用 `RANK_COLORS = ['#FF6B6B', '#F7DC6F', '#45B7D1']`，4+ 名 `#cbd5e1`
- 头像 + 名字：`flex items-center gap-3 min-w-0 pr-4`
- 标题 hover：`group-hover:text-slate-500`
- Stats：`flex items-center gap-4 justify-end text-xs text-gray-400 font-medium`

## 列头

```tsx
<div className="grid grid-cols-[40px_1fr_100px_180px] md:grid-cols-[40px_1fr_100px_200px]
                items-center px-4 py-2.5 text-xs font-bold
                text-gray-400 uppercase tracking-wider">
  <span>#</span>
  <span>Skill</span>
  <span>分类</span>
  <span className="text-right">数据</span>
</div>
```

## 核心代码

```tsx
import { Heart, Users, Star } from 'lucide-react';
import { motion } from 'framer-motion';
import { LetterAvatar } from '../components/avatars-icons/LetterAvatar';

const RANK_COLORS = ['#FF6B6B', '#F7DC6F', '#45B7D1'];

interface LeaderboardRowProps {
  rank: number;               // 1-based
  name: string;
  summary?: string | null;
  category?: string | null;
  stats?: { likeCount?: number; usedCount?: number; ratingAverage?: number };
  onClick?: () => void;
  avatarIndex: number;
}

export const LeaderboardRow = ({
  rank, name, summary, category, stats, onClick, avatarIndex,
}: LeaderboardRowProps) => {
  const idx = rank - 1;
  const rankColor = idx < 3 ? RANK_COLORS[idx] : '#cbd5e1';

  return (
    <motion.div
      onClick={onClick}
      className="grid grid-cols-[40px_1fr_100px_180px] md:grid-cols-[40px_1fr_100px_200px]
                 items-center px-4 py-3 hover:bg-slate-50/60
                 transition-colors duration-200 cursor-pointer
                 border-b border-gray-50 last:border-b-0 group"
      initial={{ opacity: 0 }}
      whileInView={{ opacity: 1 }}
      viewport={{ once: true }}
      transition={{ duration: 0.2, delay: idx * 0.02 }}
    >
      {/* rank */}
      <span className="text-lg font-extrabold" style={{ color: rankColor }}>
        {rank}
      </span>

      {/* name + desc */}
      <div className="flex items-center gap-3 min-w-0 pr-4">
        <LetterAvatar name={name} index={avatarIndex} />
        <div className="min-w-0">
          <h4 className="text-sm font-bold text-gray-900
                         group-hover:text-slate-500 transition-colors truncate">
            {name}
          </h4>
          <p className="text-xs text-gray-400 truncate mt-0.5">
            {summary || '暂无描述'}
          </p>
        </div>
      </div>

      {/* category */}
      <div className="flex items-center">
        {category && (
          <span className="inline-block text-[11px] font-semibold
                           px-2.5 py-0.5 rounded-full
                           bg-teal-50 text-teal-600 border border-teal-100
                           truncate max-w-[110px]">
            {category}
          </span>
        )}
      </div>

      {/* stats */}
      <div className="flex items-center gap-4 justify-end text-xs text-gray-400 font-medium">
        <span className="flex items-center gap-1" title="点赞">
          <Heart size={13} /> {stats?.likeCount ?? 0}
        </span>
        <span className="flex items-center gap-1" title="已使用">
          <Users size={13} /> {stats?.usedCount ?? 0}
        </span>
        <span className="flex items-center gap-1" title="评分">
          <Star size={13} />
          {stats?.ratingAverage ? stats.ratingAverage.toFixed(1) : '-'}
        </span>
      </div>
    </motion.div>
  );
};
```

## 容器用法

```tsx
<div className="rounded-2xl overflow-hidden">
  {/* 列头 */}
  <div className="grid grid-cols-[40px_1fr_100px_180px] md:grid-cols-[40px_1fr_100px_200px]
                  items-center px-4 py-2.5 text-xs font-bold
                  text-gray-400 uppercase tracking-wider">
    <span>#</span><span>Skill</span><span>分类</span>
    <span className="text-right">数据</span>
  </div>

  {/* 行 */}
  {skills.slice(0, 10).map((s, i) => (
    <LeaderboardRow
      key={s.id}
      rank={i + 1}
      name={s.name}
      summary={s.summary}
      category={s.tags[0]}
      stats={s.stats}
      avatarIndex={i}
      onClick={() => navigate(`/skills/${s.slug}`)}
    />
  ))}
</div>
```

## 适配指南

- 4 列宽度（40 / 1fr / 100 / 180-200）是经过 desktop / tablet 调优的；宽度可等比放大但不要打破 "fixed-fluid-fixed-fixed" 的骨架
- 4 名及后用 slate-300 的 # 色，不要换成黑色——"看得见但不抢戏"
- 列头永远 uppercase tracking-wider，和表格（`blocks/display/skillhub/table`）保持一致的"meta"气质
- Top 10 是 sweet spot——11 行起视觉密度会被 stats 列压垮，建议改成 `blocks/display/skillhub/skill-card` 网格
- 列 2 的 `min-w-0` 是必须的——否则 truncate 不生效（flex 子项默认 `min-width: auto`）

## 反模式

- 不要把分类 pill 的色改成紫/橙——会和 Top3 的红黄蓝抢视觉权
- 不要让 stats 左对齐——榜单右端需要"数字对齐"感，不对齐=失衡
- 不要加 row divider 之外的列 divider——竖线会让这张榜单变成 spreadsheet
- 不要给每行加 shadow——榜单是"一体"的，不是卡片堆
