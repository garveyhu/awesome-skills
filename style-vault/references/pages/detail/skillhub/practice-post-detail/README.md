---
id: pages/detail/skillhub/practice-post-detail
type: page
name: 实践帖详情页
description: 单栏长文 + 顶部元信息（作者/时间/关联 skill）+ 底部互动 + 评论
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - blocks/nav/skillhub/glass-pill-navbar
  - components/avatars-icons/skillhub/letter-avatar
  - components/buttons/skillhub/dark-primary-cta
  - components/tags-badges/skillhub/teal-pill
  - tokens/typography/pairs/skillhub/inter-jetbrains-duo
preview: /preview/pages/detail/skillhub/practice-post-detail
---

# Practice Post Detail

> 单篇实践帖的阅读页。单列窄正文（`max-w-2xl`）强调"文章"气质，顶部作者卡 + 底部行内互动条（点赞/评论/分享），底下评论分页。

## 页面骨架

```
┌─ GlassPillNavbar ────────────────────────────────────────┐
│                                                          │
│  ┌─ 返回链接 "← 返回社区" ──────────────────────┐          │
│                                                          │
│  ┌─ 文章容器 max-w-2xl mx-auto ─────────────────┐         │
│  │                                               │         │
│  │  ┌─ 元信息 ─────────────────────────────┐    │         │
│  │  │  [avatar] 作者 @links · 更新于 ...    │    │         │
│  │  │  [skill: xxx pill]                    │    │         │
│  │  └─────────────────────────────────────┘    │         │
│  │                                               │         │
│  │  H1 标题 font-extrabold text-3xl              │         │
│  │                                               │         │
│  │  prose markdown 正文（同 skill-detail）       │         │
│  │                                               │         │
│  │  ┌─ 互动条 sticky bottom 或内联 ────────┐     │         │
│  │  │  ♡ 点赞 (N)   ♬ 评论 (M)   分享       │     │         │
│  │  └──────────────────────────────────────┘     │         │
│  │                                               │         │
│  │  [相关 skill 卡片 ×N]                          │         │
│  │                                               │         │
│  │  [评论区]                                      │         │
│  │    发表评论框                                  │         │
│  │    评论 × N + 分页                            │         │
│  │                                               │         │
│  └───────────────────────────────────────────────┘         │
└──────────────────────────────────────────────────────────┘
```

## 核心代码（骨架）

```tsx
export const PracticePostDetail = () => {
  const { id } = useParams();
  const [post, setPost] = useState<PracticePost | null>(null);
  const [isLiked, setIsLiked] = useState(false);

  return (
    <>
      <GlassPillNavbar /* ... */ />

      <div className="max-w-2xl mx-auto px-4 sm:px-6 pt-6 pb-24">
        <Link to="/practice" className="inline-flex items-center gap-1.5 text-sm text-slate-500
                                        hover:text-slate-900 mb-6 transition-colors">
          <ArrowLeft size={16} /> 返回社区
        </Link>

        {/* 元信息 */}
        <div className="flex items-center gap-3 mb-4">
          <LetterAvatar name={post?.authorNickname ?? ''} index={0} size={40} />
          <div>
            <Link to={`/users/${post?.authorId}`}
              className="text-sm font-bold text-slate-900 hover:text-teal-700">
              {post?.authorNickname}
            </Link>
            <div className="text-xs text-slate-400">更新于 {post?.updatedAt}</div>
          </div>
        </div>

        {post?.relatedSkills && (
          <div className="flex gap-1.5 flex-wrap mb-6">
            {post.relatedSkills.map((s) => (
              <Link key={s} to={`/skills/${s}`}>
                <TealPill>{s}</TealPill>
              </Link>
            ))}
          </div>
        )}

        {/* 标题 */}
        <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight leading-tight mb-8">
          {post?.title}
        </h1>

        {/* 正文 */}
        <article className="prose prose-slate max-w-none">
          <ReactMarkdown rehypePlugins={[rehypeRaw]} remarkPlugins={[remarkGfm]}>
            {post?.content ?? ''}
          </ReactMarkdown>
        </article>

        {/* 互动条 */}
        <div className="mt-12 pt-6 border-t border-slate-200
                        flex items-center gap-6 text-sm font-medium text-slate-600">
          <button
            onClick={handleLike}
            className={`inline-flex items-center gap-1.5 transition-colors
                        ${isLiked ? 'text-rose-600' : 'hover:text-slate-900'}`}>
            <Heart size={16} fill={isLiked ? 'currentColor' : 'none'} />
            {post?.likesCount ?? 0}
          </button>
          <span className="inline-flex items-center gap-1.5">
            <MessageCircle size={16} /> {post?.commentsCount ?? 0}
          </span>
          <button className="inline-flex items-center gap-1.5 hover:text-slate-900">
            <Share2 size={16} /> 分享
          </button>
        </div>

        {/* 评论区 */}
        <section className="mt-12">
          <h2 className="text-lg font-bold text-slate-900 mb-4">讨论 · {post?.commentsCount ?? 0}</h2>
          <CommentComposer /* ... */ />
          <CommentList comments={comments} />
          <Pagination /* ... */ />
        </section>
      </div>
    </>
  );
};
```

## 视觉要点

- 单列 `max-w-2xl`（512px）阅读节奏——和 skill-detail 的双栏区分；这里是纯"文章"体验
- 标题 `text-3xl`（不是 text-4xl）—— 帖子层级低于 skill（产品级）
- 元信息（作者 + 时间）放标题上方，不是旁边——强调"谁在什么时候发的"
- 相关 skill pill 单独一行，可点击跳转——和 skill-detail 的 tag 不同（这里是反向链接）
- 互动条用 border-t + 水平排布——文章尾而非 sticky（保持沉浸阅读）
- 点赞 heart 用 `fill={isLiked ? 'currentColor' : 'none'}`——填色 vs 线框二态

## 适配指南

- 正文 max-w 固定 2xl（512px）—— 阅读学推荐 50-75 个字符每行，Inter 14px 在 512px 约 64 字符
- 点赞用 rose（红）不要用 teal——rose 是"心"的语义色，teal 是"工具/品牌"
- 互动条在底部 border-t 分隔，不做 sticky——干扰阅读；真的需要快速点赞放在侧边（但此 style 不需要）
- 评论区与正文之间 `mt-12`——给足阅读完毕的呼吸

## 反模式

- 不要把这页和 skill-detail 做成同样的双栏——帖子就是帖子，不是产品页
- 不要在元信息里堆 "收藏 / 分享 / 举报"——那些放在互动条里；元信息只承载 who + when
- 不要用 text-4xl 标题——会抢首页 hero 的"最大字号"地位
- 不要在正文外框加 border + shadow——prose 裸放，让 markdown 呼吸
