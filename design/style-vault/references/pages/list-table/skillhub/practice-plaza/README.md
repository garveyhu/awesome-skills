---
id: pages/list-table/skillhub/practice-plaza
type: page
name: 实践广场
description: 紧凑 hero + 排序切换 + 过滤胶囊 + 帖子卡列表 + 榜单侧栏
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - blocks/nav/skillhub/glass-pill-navbar
  - blocks/display/skillhub/leaderboard-row
  - blocks/feedback/skillhub/empty-state
  - components/buttons/skillhub/dark-primary-cta
  - components/avatars-icons/skillhub/letter-avatar
  - components/tags-badges/skillhub/teal-pill
  - tokens/palettes/skillhub/skillhub-teal-mist
preview: /preview/pages/list-table/skillhub/practice-plaza
---

# Practice Plaza

> 社区实践广场。顶部是紧凑 hero（`text-2xl` 标题 + 内联筛选+搜索+发布按钮同行），下面是帖子卡列表（2 列 · 左主帖子 · 右榜单）。

## 页面骨架

```
┌─ GlassPillNavbar ────────────────────────────────────┐
│                                                      │
│  ┌─ 紧凑 Hero (pt-8 pb-4, bg-[#f5f7fa]) ──────────┐  │
│  │  H1 "Skill 经验社区" (text-2xl)                 │  │
│  │  [滤 icon] [🔍 搜索标题] [发布实践]              │  │
│  │  [skill: xxx ×]（active filter chip）            │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  ┌─ 主体 2 列 max-w-5xl (lg: 2fr 1fr) ─────────────┐ │
│  │ 主栏                  │ 侧栏 sticky              │ │
│  │  [排序 toggle]         │ [榜单标题]                │ │
│  │    最新 / 最热         │   (leaderboard-row × 10) │ │
│  │                       │                          │ │
│  │  PostCard 列表:        │                          │ │
│  │   - avatar+nickname   │                          │ │
│  │   - 标题 font-bold     │                          │ │
│  │   - summary 2 行        │                          │ │
│  │   - [相关 skills pill] │                          │ │
│  │   - like + comment    │                          │ │
│  │                       │                          │ │
│  │  Pagination            │                          │ │
│  └──────────────────────┴──────────────────────────┘ │
└──────────────────────────────────────────────────────┘
```

## 核心代码（骨架）

```tsx
export const PracticePlaza = () => {
  const [posts, setPosts] = useState<PracticePost[]>([]);
  const [leaderboard, setLeaderboard] = useState<LeaderboardData | null>(null);
  const [query, setQuery] = useState('');
  const [sort, setSort] = useState<'latest' | 'popular'>('latest');
  const [skillFilter, setSkillFilter] = useState<string | undefined>();

  return (
    <>
      <GlassPillNavbar /* ... */ />

      <div className="min-h-screen bg-[#f5f7fa] font-sans">
        {/* Hero */}
        <section className="pt-8 pb-4">
          <div className="max-w-5xl mx-auto px-4 sm:px-6 text-center">
            <h1 className="text-2xl font-extrabold text-gray-900 mb-4">Skill 经验社区</h1>
            <div className="flex items-center justify-center gap-2 max-w-lg mx-auto">
              <FilterButton active={Boolean(skillFilter)} /* ... */ />
              <div className="flex-1">
                <Input.Search
                  placeholder="搜索标题..."
                  enterButton={<span style={{ color: '#fff' }}>搜索</span>}
                  size="large"
                  style={{ ['--ant-color-primary' as string]: '#1a1a1a' }}
                  onSearch={setQuery}
                  allowClear
                />
              </div>
              <DarkPrimaryCta size="md" icon={<Sparkles size={13} />} shimmer>
                发布实践
              </DarkPrimaryCta>
            </div>
            {skillFilter && (
              <div className="max-w-lg mx-auto mt-2">
                <FilterChip label={`skill: ${skillFilter}`} onClose={() => setSkillFilter(undefined)} />
              </div>
            )}
          </div>
        </section>

        {/* 主体 */}
        <div className="max-w-5xl mx-auto px-4 sm:px-6 pb-6 grid grid-cols-1 lg:grid-cols-[1fr_320px] gap-6">
          <main>
            {/* 排序 toggle */}
            <div className="flex items-center gap-3 mb-4">
              <SortToggle value={sort} onChange={setSort} />
            </div>

            {/* 帖子卡列表 */}
            {posts.length === 0 && !loading ? (
              <EmptyState
                icon={MessageCircle}
                title="还没有实践帖"
                hint="第一个发帖的就是你"
                action={
                  <DarkPrimaryCta size="md" onClick={() => navigate('/practice/create')}>
                    发布第一篇
                  </DarkPrimaryCta>
                }
              />
            ) : (
              <div className="flex flex-col gap-3">
                {posts.map((p, i) => <PostCard key={p.id} post={p} index={i} />)}
              </div>
            )}

            {/* Pagination */}
            <Pagination total={totalPages} current={currentPage} onChange={setCurrentPage} />
          </main>

          <aside className="lg:sticky lg:top-20 lg:self-start">
            <div className="bg-white border border-slate-200/60 rounded-2xl p-4">
              <div className="text-sm font-bold text-slate-900 mb-3">社区榜单</div>
              {leaderboard?.items.map((item, i) => (
                <LeaderboardRow
                  key={item.id}
                  rank={i + 1}
                  name={item.title}
                  summary={item.authorNickname}
                  stats={{ likeCount: item.likesCount }}
                  avatarIndex={i}
                  onClick={() => navigate(`/practice/${item.id}`)}
                />
              ))}
            </div>
          </aside>
        </div>
      </div>
    </>
  );
};
```

## PostCard

```tsx
const PostCard = ({ post, index }: { post: PracticePost; index: number }) => (
  <Link to={`/practice/${post.id}`}
    className="group bg-white rounded-xl border border-slate-200/60 p-4
               hover:border-teal-200 hover:shadow-sm transition-all">
    <div className="flex items-start gap-3">
      <LetterAvatar name={post.authorNickname} index={index} size={36} />
      <div className="flex-1 min-w-0">
        <div className="flex items-baseline gap-2">
          <span className="text-sm font-bold text-slate-900">{post.authorNickname}</span>
          <span className="text-xs text-slate-400">· {post.createdAt}</span>
        </div>
        <h3 className="text-base font-bold text-slate-900 group-hover:text-teal-700 mt-1">
          {post.title}
        </h3>
        <p className="text-sm text-slate-500 mt-1 line-clamp-2 leading-relaxed">{post.summary}</p>
        {post.relatedSkills && (
          <div className="flex gap-1.5 mt-2 flex-wrap">
            {post.relatedSkills.map((s) => <TealPill key={s}>{s}</TealPill>)}
          </div>
        )}
        <div className="flex items-center gap-4 mt-3 text-xs text-slate-400 font-medium">
          <span className="inline-flex items-center gap-1"><Heart size={12} /> {post.likesCount}</span>
          <span className="inline-flex items-center gap-1"><MessageCircle size={12} /> {post.commentsCount}</span>
        </div>
      </div>
    </div>
  </Link>
);
```

## 适配指南

- Hero 压缩版（text-2xl 而不是 text-6xl）——这是"功能页"而非"品牌页"，发现页才用大 hero
- 搜索 + 发布按钮 + 过滤按钮同行——减少垂直空间浪费
- Antd `Input.Search` 用 CSS 变量 override `--ant-color-primary: #1a1a1a`，按钮会变黑
- 帖子卡用 `rounded-xl` 而不是 `rounded-2xl`——广场内容密度高，小圆角更紧凑
- 榜单侧栏 sticky + `border-slate-200/60`——避免喧宾夺主
- 单列帖子不是网格 —— 广场更像"动态流"而非"商品货架"

## 反模式

- 不要和 skill-community-home 用相同的大 hero ——实践广场是二级页，不是入口页
- 不要把 LeaderboardRow 搬到主栏——主栏是流，侧栏才是榜
- 不要给 PostCard 加 y:-4 浮起——帖子密度大于 skill-card，每条都动会晕
- 不要让发布按钮只是文字链 / ghost——需要黑底 CTA 召唤
