---
id: pages/landing/skillhub/skill-community-home
type: page
name: 技能社区首页
description: Hero 流光 → TOP 榜单 → 分类图标导航 → 搜索 → Skill 网格 + 分页
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - blocks/nav/skillhub/glass-pill-navbar
  - blocks/marketing/skillhub/gradient-hero
  - blocks/display/skillhub/leaderboard-row
  - blocks/display/skillhub/skill-card
  - components/tags-badges/skillhub/teal-pill
  - components/avatars-icons/skillhub/letter-avatar
  - tokens/palettes/skillhub/skillhub-teal-mist
  - tokens/typography/pairs/skillhub/inter-jetbrains-duo
  - tokens/motion/skillhub/gentle-flow
preview: /preview/pages/landing/skillhub/skill-community-home
---

# Skill Community Home

> 发现 / 首页双身份页面——顶部是全站 navbar（外），向下依次是 hero、Top 榜单、分类图标导航 + 搜索、全量 skill 网格 + 分页

## 页面骨架

```
┌─ GlassPillNavbar (sticky) ─────────────────────────┐
│                                                    │
│  ┌─ GradientHero ─────────────────────────────────┐│
│  │   H1（流光词） + subtitle                       ││
│  │   [追光 CTA]  [ghost 浏览]                     ││
│  └───────────────────────────────────────────────┘│
│                                                    │
│  ┌─ 榜单 section (max-w-4xl) ────────────────────┐│
│  │   "精选 TOP Skills 榜单"                       ││
│  │   列头 # Skill 分类 数据                        ││
│  │   Top10 LeaderboardRow                          ││
│  └───────────────────────────────────────────────┘│
│                                                    │
│  ┌─ 分类图标导航 (max-w-7xl) ────────────────────┐│
│  │   [全部] [标签1] [标签2] ...                   ││
│  └───────────────────────────────────────────────┘│
│                                                    │
│  ┌─ 搜索表单 (max-w-2xl) ────────────────────────┐│
│  │   [🔍 input .........] [搜索]                   ││
│  └───────────────────────────────────────────────┘│
│                                                    │
│  ┌─ 当前结果头 ──────────────────────────────────┐│
│  │   "全部 Skill" | "分类: xxx"   [N 结果]        ││
│  └───────────────────────────────────────────────┘│
│                                                    │
│  ┌─ SkillCard 网格 3 列 (max-w-7xl) ─────────────┐│
│  │   [Card] [Card] [Card]                          ││
│  │   [Card] [Card] [Card]                          ││
│  │   ...                                           ││
│  │   分页：<  1 2 3 4 ...  >                      ││
│  └───────────────────────────────────────────────┘│
│                                                    │
└────────────────────────────────────────────────────┘
```

## 核心代码

```tsx
import { AnimatePresence, motion } from 'framer-motion';
import { Search, Box, ChevronLeft, ChevronRight } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';
import { GlassPillNavbar }   from '../blocks/nav/GlassPillNavbar';
import { GradientHero }      from '../blocks/marketing/GradientHero';
import { LeaderboardRow }    from '../blocks/display/LeaderboardRow';
import { SkillCard }         from '../blocks/display/SkillCard';

const ITEMS_PER_PAGE = 12;

export const SkillCommunityHome = () => {
  const [skills, setSkills]           = useState<SkillCard[]>([]);
  const [featured, setFeatured]       = useState<SkillCard[]>([]);
  const [tags, setTags]               = useState<TagItem[]>([]);
  const [stats, setStats]             = useState<StatsOverview | null>(null);
  const [search, setSearch]           = useState('');
  const [activeTag, setActiveTag]     = useState<string | null>(null);
  const [page, setPage]               = useState(1);
  const [loading, setLoading]         = useState(true);
  const gridRef = useRef<HTMLDivElement>(null);

  // 1. 初次并发加载
  useEffect(() => {
    Promise.allSettled([fetchSkills(), fetchStats(), fetchFeatured(), fetchTags()])
      .then(/* setState each */);
  }, []);

  const onSearch = (e) => { e.preventDefault(); setActiveTag(null); fetchSkills({ q: search }); };
  const onTag    = (slug) => { setActiveTag(slug); setSearch(''); fetchSkills({ tag: slug }); };
  const scrollToGrid = () => gridRef.current?.scrollIntoView({ behavior: 'smooth' });

  const totalPages = Math.ceil(skills.length / ITEMS_PER_PAGE) || 1;
  const current = skills.slice((page - 1) * ITEMS_PER_PAGE, page * ITEMS_PER_PAGE);

  return (
    <div className="w-full min-h-screen font-sans bg-white">
      {/* 1. Hero */}
      <GradientHero
        prefix="让 AI 技能 "
        flowWord="流动起来"
        subtitle="发现、安装、分享高质量的 AI Skill 技能包"
        primaryLabel="发布 Skill"
        onPrimary={() => navigate('/publish')}
        secondaryLabel="探索全部技能"
        onSecondary={scrollToGrid}
      />

      {/* 2. 榜单 */}
      {featured.length > 0 && (
        <motion.section
          className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 mt-8"
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
        >
          <div className="text-center mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">精选 TOP Skills 榜单</h2>
            <p className="text-gray-500 text-sm">精选最值得安装的 Skills</p>
          </div>
          <div className="rounded-2xl overflow-hidden">
            {/* 列头 */}
            <div className="grid grid-cols-[40px_1fr_100px_180px] md:grid-cols-[40px_1fr_100px_200px]
                            items-center px-4 py-2.5 text-xs font-bold
                            text-gray-400 uppercase tracking-wider">
              <span>#</span><span>Skill</span><span>分类</span>
              <span className="text-right">数据</span>
            </div>
            {featured.slice(0, 10).map((s, i) => (
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
        </motion.section>
      )}

      {/* 3. 分类导航 + 搜索 */}
      <div ref={gridRef} className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-16 scroll-mt-4">
        <div className="text-center mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">探索全部技能</h2>
          <p className="text-gray-500 text-sm">
            {stats ? `收录共 ${stats.totalSkills} 个 Skills` : '快速发现你需要的 AI Skills'}
          </p>
        </div>

        {tags.length > 0 && (
          <div className="flex items-center justify-center gap-4 flex-wrap mb-6">
            <CategoryIconButton active={!activeTag} onClick={() => onTag(null)} icon={<Box size={22} />} label="全部" />
            {tags.map((t) => (
              <CategoryIconButton
                key={t.id}
                active={activeTag === t.slug}
                onClick={() => onTag(t.slug)}
                icon={getTagIcon(t.icon)}
                label={t.name}
              />
            ))}
          </div>
        )}

        <form onSubmit={onSearch} className="max-w-2xl mx-auto mb-8">
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-gray-400">
              <Search size={18} />
            </div>
            <input
              type="text" value={search} onChange={(e) => setSearch(e.target.value)}
              placeholder="搜索名称、标签或描述..."
              className="w-full pl-11 pr-24 py-3 bg-white border border-gray-200 rounded-xl
                         text-gray-900 placeholder:text-gray-400
                         focus:outline-none focus:border-teal-300 focus:ring-2 focus:ring-teal-100
                         transition-all duration-200 text-sm"
            />
            <button type="submit"
              className="absolute inset-y-1.5 right-1.5 px-5
                         bg-teal-500 hover:bg-teal-600 text-white
                         text-sm font-semibold rounded-lg
                         transition-colors duration-200 active:scale-95">
              搜索
            </button>
          </div>
        </form>
      </div>

      {/* 4. 网格 + 分页 */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-24">
        <div className="flex items-center justify-between mb-5">
          <h3 className="text-lg font-bold text-gray-900">
            {activeTag ? `分类: ${tags.find(t => t.slug === activeTag)?.name}` : '全部 Skill'}
          </h3>
          <span className="text-[13px] font-semibold text-gray-500
                           bg-white px-3 py-1 rounded-full border border-gray-200">
            {skills.length} 结果
          </span>
        </div>

        <AnimatePresence mode="wait">
          <motion.div
            key={`${activeTag}-${page}`}
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 mb-10"
          >
            {current.map((s, i) => (
              <SkillCard
                key={s.id}
                name={s.name}
                summary={s.summary}
                version={s.version}
                stats={s.stats}
                avatarIndex={(page - 1) * ITEMS_PER_PAGE + i}
                onClick={() => navigate(`/skills/${s.slug}`)}
              />
            ))}
          </motion.div>
        </AnimatePresence>

        <Pagination total={totalPages} current={page} onChange={setPage} />
      </div>
    </div>
  );
};
```

### CategoryIconButton（内联子件）

```tsx
const CategoryIconButton = ({ active, onClick, icon, label }) => (
  <button
    onClick={onClick}
    className={`flex flex-col items-center gap-1.5 px-3 py-2 rounded-xl transition-all duration-200 ${
      active ? 'text-teal-700' : 'text-gray-400 hover:text-gray-600 hover:bg-gray-50'
    }`}
  >
    <div className={`w-12 h-12 rounded-2xl flex items-center justify-center transition-all duration-200 ${
      active ? 'bg-teal-500 text-white shadow-sm shadow-teal-500/20' : 'bg-gray-100 text-gray-400'
    }`}>
      {icon}
    </div>
    <span className="text-xs font-semibold">{label}</span>
  </button>
);
```

### Pagination（分页控件）

```tsx
const Pagination = ({ total, current, onChange }) => (
  <div className="flex items-center justify-center gap-2 mt-6">
    <button
      disabled={current === 1}
      onClick={() => onChange(current - 1)}
      className="p-2.5 rounded-xl text-gray-500 hover:bg-white hover:shadow-md
                 disabled:opacity-30 transition-all"
    >
      <ChevronLeft size={18} />
    </button>
    <div className="flex items-center gap-1">
      {Array.from({ length: total }, (_, i) => i + 1).map((p) => (
        <button key={p} onClick={() => onChange(p)}
          className={`w-9 h-9 rounded-xl text-[13px] font-bold transition-all ${
            current === p
              ? 'bg-teal-600 text-white shadow-md'
              : 'text-gray-500 hover:bg-white hover:shadow-sm'
          }`}>
          {p}
        </button>
      ))}
    </div>
    <button
      disabled={current === total}
      onClick={() => onChange(current + 1)}
      className="p-2.5 rounded-xl text-gray-500 hover:bg-white hover:shadow-md
                 disabled:opacity-30 transition-all"
    >
      <ChevronRight size={18} />
    </button>
  </div>
);
```

## 适配指南

- 容器层级：navbar 全宽 sticky → hero 全宽 → 榜单 `max-w-4xl`（不要 7xl，5xl 以上的列宽让榜单太散）→ 搜索 `max-w-2xl`（input 居中）→ 网格 `max-w-7xl`（3 列正合适）
- Hero 和榜单之间 `mt-8` 是紧凑，想更呼吸给 `mt-12`
- 搜索和网格之间 `mb-8` 留呼吸；scroll-mt-4 确保点"探索"按钮时滚到网格不卡在 sticky navbar 后面
- 并发加载 4 API：`skills / stats / featured / tags`。三方之一挂掉不影响其它渲染（`Promise.allSettled`）
- `activeTag + page` 组合 key 在 AnimatePresence 切换时触发 fade——注意 key 变化才触发，所以单搜索不改 activeTag 时可以额外加 `search` 进 key

## 反模式

- 不要在 hero 和榜单之间插第二个 motion section——会让用户以为"内容开始了"然后又打断
- 不要把 featured 的 10 条放在 skill 网格之前以外的位置（比如 sidebar）——榜单就是二次强调，该留在 hero 下第一位
- 不要让分类图标导航超过 8 项——超过就该折叠成下拉
