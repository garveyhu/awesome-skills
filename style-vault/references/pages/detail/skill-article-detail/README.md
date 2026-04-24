---
id: pages/detail/skill-article-detail
type: page
name: Skill 技能详情页
description: 长文 markdown 主栏 + 右侧 sticky sidebar（作者 / 操作 / 评分 / 相关）+ 底部评论区
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - blocks/nav/glass-pill-navbar
  - blocks/display/skill-card
  - components/avatars-icons/letter-avatar
  - components/buttons/dark-primary-cta
  - components/tags-badges/teal-pill
  - tokens/palettes/skillhub-teal-mist
  - tokens/typography/pairs/inter-jetbrains-duo
preview: /preview/pages/detail/skill-article-detail
---

# Skill Article Detail

> SkillHub 的一级详情页。核心是 SKILL.md 的 markdown 正文（`prose` 渲染：indigo blockquote / indigo code inline / slate-200 h1 下划线），配右侧 sticky sidebar（作者卡 + 动作 + 评分 + bundle 树 + 相关技能），底部是分页评论。

## 页面骨架

```
┌─ GlassPillNavbar ──────────────────────────────────────────┐
│                                                            │
│  ┌─ 返回链接 "← 返回发现" ─────────────────────────────┐    │
│                                                            │
│  ┌─ 标题大 hero ────────────────────────────────────┐      │
│  │  H1 skill.name   ·   v1.2.0                      │      │
│  │  [分类 pill] [作者] · 更新时间                     │      │
│  │  summary 一段（slate-600）                         │      │
│  └─────────────────────────────────────────────────┘      │
│                                                            │
│  ┌─ 主体 2 列 (lg: 2fr 1fr) ─────────────────────────┐     │
│  │ 主栏 prose markdown     │ 右 sidebar sticky top-4 │     │
│  │   SKILL.md 全文         │   · 作者卡              │     │
│  │   h1 / h2 / h3          │   · Action（点赞/使用）│      │
│  │   代码块 Prism oneLight │   · 评分 1-5 星         │     │
│  │   blockquote indigo     │   · 快速复制 slug       │     │
│  │                         │   · Bundle 文件树       │     │
│  │                         │   · 相关技能 top3       │     │
│  └────────────────────────┴────────────────────────┘      │
│                                                            │
│  ┌─ 评论区 ─────────────────────────────────────────┐      │
│  │  "讨论 N 条"                                      │      │
│  │  [发表评论框 · SoftFormInput textarea]            │      │
│  │  评论条目：头像 + 昵称 + 时间 + 内容               │      │
│  │  Pagination                                        │      │
│  └─────────────────────────────────────────────────┘      │
│                                                            │
│  ┌─ 相关实践链接（水平 list）────────────────────┐          │
│  │  "相关实践"                                      │          │
│  │  [标题卡片 × N]                                  │          │
│  └─────────────────────────────────────────────┘          │
└────────────────────────────────────────────────────────────┘
```

## 核心代码（骨架）

```tsx
export const SkillArticleDetail = () => {
  const { author, skillName } = useParams();
  const [detail, setDetail] = useState<SkillDetail | null>(null);
  const [viewerState, setViewerState] = useState({ liked: false, downloaded: false, used: false, rating: 0 });

  return (
    <>
      <GlassPillNavbar /* ... */ />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6 pb-24">
        {/* 返回链接 */}
        <button onClick={() => navigate(-1)}
          className="inline-flex items-center gap-1.5 text-sm text-slate-500
                     hover:text-slate-900 mb-6 transition-colors">
          <ChevronLeft size={16} /> 返回发现
        </button>

        {/* 标题 hero */}
        <header className="mb-8">
          <div className="flex items-baseline gap-3 mb-2">
            <h1 className="text-3xl lg:text-4xl font-extrabold text-slate-900 tracking-tight">
              {detail?.name}
            </h1>
            {detail?.version && (
              <span className="text-[13px] font-semibold text-slate-500 bg-slate-50
                               border border-slate-200 px-2 py-0.5 rounded font-mono">
                v{detail.version}
              </span>
            )}
          </div>
          <div className="flex items-center gap-2 flex-wrap mb-4">
            {detail?.tags.map((t) => <TealPill key={t}>{t}</TealPill>)}
            <span className="text-sm text-slate-500">· 作者 @{detail?.authorName} · 更新于 {detail?.updatedAt}</span>
          </div>
          <p className="text-base text-slate-600 leading-relaxed max-w-3xl">
            {detail?.summary}
          </p>
        </header>

        {/* 主体两列 */}
        <div className="grid grid-cols-1 lg:grid-cols-[1fr_320px] gap-10">
          {/* 主栏 */}
          <article className="prose prose-slate max-w-none">
            <ReactMarkdown
              rehypePlugins={[rehypeRaw]}
              remarkPlugins={[remarkGfm]}
              components={{
                code({ inline, className, children, ...props }) {
                  const match = /language-(\w+)/.exec(className || '');
                  return !inline && match
                    ? <SyntaxHighlighter language={match[1]} style={oneLight}>{String(children)}</SyntaxHighlighter>
                    : <code className={className} {...props}>{children}</code>;
                },
                h2({ children }) {
                  const id = slugifyAnchor(extractText(children));
                  return <h2 id={id}>{children}</h2>;
                },
              }}
            >
              {detail?.bodyMarkdown ?? ''}
            </ReactMarkdown>
          </article>

          {/* Sidebar sticky */}
          <aside className="lg:sticky lg:top-20 lg:self-start space-y-4">
            {/* 作者卡 */}
            <SidebarSection>
              <div className="flex items-center gap-3 mb-3">
                <LetterAvatar name={detail?.authorName ?? ''} index={0} size={48} />
                <div>
                  <div className="text-sm font-bold text-slate-900">{detail?.authorName}</div>
                  <div className="text-xs text-slate-500">关注 · 私信</div>
                </div>
              </div>
            </SidebarSection>

            {/* Actions */}
            <SidebarSection>
              <div className="flex flex-col gap-2">
                <DarkPrimaryCta size="md" className="w-full justify-center" icon={<CheckCircle size={14} />}
                  onClick={handleUse}>
                  {viewerState.used ? '已使用' : '使用此 Skill'}
                </DarkPrimaryCta>
                <button onClick={handleLike}
                  className="inline-flex items-center justify-center gap-1.5 px-4 py-2 rounded-xl
                             border border-slate-200 text-sm font-medium text-slate-700
                             hover:border-slate-300 transition-all active:scale-95">
                  <ThumbsUp size={14} /> 点赞 · {detail?.stats.likeCount}
                </button>
              </div>
            </SidebarSection>

            {/* 评分 */}
            <SidebarSection title="评分">
              <StarRater value={viewerState.rating} onRate={handleRate} />
            </SidebarSection>

            {/* 快速复制 slug */}
            <SidebarSection title="Slug">
              <code className="text-xs font-mono text-indigo-800 bg-indigo-50/70 border border-indigo-100
                               rounded px-2 py-1 inline-block">
                {`${author}/${skillName}`}
              </code>
            </SidebarSection>

            {/* Bundle 树 */}
            <SidebarSection title="Bundle">
              <BundleTree files={bundleFiles} open={bundleTreeOpen} onToggle={setBundleTreeOpen} />
            </SidebarSection>

            {/* 相关技能 */}
            <SidebarSection title="相关技能">
              {relatedSkills.slice(0, relatedVisibleCount).map((s, i) => (
                <MiniSkillRow key={s.id} skill={s} index={i} />
              ))}
            </SidebarSection>
          </aside>
        </div>

        {/* 评论区 */}
        <section className="mt-16">
          <h2 className="text-xl font-bold text-slate-900 mb-4">讨论 · {comments.length}</h2>
          <CommentComposer value={commentContent} onChange={setCommentContent} onSubmit={handleComment} />
          <div className="mt-6 space-y-4">
            {paginatedComments.map((c) => <CommentItem key={c.id} comment={c} />)}
          </div>
          <Pagination total={totalPages} current={commentPage} onChange={setCommentPage} />
        </section>

        {/* 相关实践 */}
        {practicePosts.length > 0 && (
          <section className="mt-16">
            <h2 className="text-xl font-bold text-slate-900 mb-4">相关实践</h2>
            <div className="flex gap-3 flex-wrap">
              {practicePosts.map((p) => (
                <Link to={`/practice/${p.id}`} key={p.id}
                  className="text-sm font-medium text-slate-700 hover:text-teal-700
                             bg-white border border-slate-200 hover:border-teal-200
                             px-4 py-2 rounded-xl transition-all">
                  {p.title}
                </Link>
              ))}
            </div>
          </section>
        )}
      </div>
    </>
  );
};

const SidebarSection = ({ title, children }: { title?: string; children: React.ReactNode }) => (
  <div className="bg-white border border-slate-200/60 rounded-2xl p-4">
    {title && <div className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">{title}</div>}
    {children}
  </div>
);
```

## 视觉要点

- 标题 hero `text-3xl lg:text-4xl extrabold tracking-tight`——比 Hero page 的 text-6xl 低一档
- 版本号 pill 用 `font-mono` 背 `bg-slate-50`（不是 teal-50）——版本号是数据不是标签
- Sidebar 宽 320px 固定，主栏自适应；小屏变成 1 列垂直
- Sticky 位置 `top-20`（navbar 高 56 + padding 余量）
- prose 类使用 tailwind-typography 插件 + 自定义 override（index.less `@layer components` 里定义）——详见 `tokens/typography/pairs/inter-jetbrains-duo`
- 评论区 SoftFormInput textarea + 底部 Pagination 复用

## 适配指南

- `prose prose-slate` 是 @tailwindcss/typography 的入口 class，在 index.less 已大量 override；若换品牌，只改 override 不改 class
- 代码块必须用 Prism `oneLight`——和浅底 prose 色对齐；不要用 GitHub dark / Monokai
- Sidebar section 用 `border-slate-200/60`（半透明）比实线弱——让侧栏让位主栏
- 主栏和 sidebar 之间 `gap-10`——不要 gap-16，详情页留白太多读起来累
- 标签 + 版本号 + 作者行要 `flex-wrap`——窄屏下能折行

## 反模式

- 不要给主栏加 border / bg——prose 应该裸在页面上，像长文阅读
- 不要让评论区用 Antd Comment / Avatar——和站点 Inter + slate 字体/色不对齐
- 不要让"使用 Skill" CTA 放在 Hero（比如版本号旁边）——主要 CTA 在 sidebar 里稳定锚点
- 不要把 bundle 树展开默认放出 50+ 条 —— 默认折叠，点击展开
