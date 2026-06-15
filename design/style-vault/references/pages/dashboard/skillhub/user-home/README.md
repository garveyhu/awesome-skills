---
id: pages/dashboard/skillhub/user-home
type: page
name: 用户中心主页
description: 顶部用户卡 + 操作区 + Tabs（我的技能 / 实践 / 点赞 / 收藏 / 投稿记录 / 关注）
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - blocks/nav/skillhub/glass-pill-navbar
  - blocks/display/skillhub/skill-card
  - blocks/feedback/skillhub/empty-state
  - components/buttons/skillhub/dark-primary-cta
  - components/avatars-icons/skillhub/letter-avatar
  - tokens/palettes/skillhub/skillhub-teal-mist
preview: /preview/pages/dashboard/skillhub/user-home
---

# User Home

> 当前登录用户的"我的"页面。顶部一张高对比 user-card（大头像 + 昵称 + stats + 操作），下面多 tab 切内容（我的技能 / 我的实践 / 我的点赞 / 我的投稿 / 关注）。

## 页面骨架

```
┌─ GlassPillNavbar ────────────────────────────────────────┐
│                                                          │
│  ┌─ User 卡片 max-w-5xl ─────────────────────────────┐    │
│  │ [大头像 80×80] [昵称] [bio]                       │    │
│  │ [关注 N] [粉丝 M] [点赞 K]                         │    │
│  │ [编辑资料] [退出登录]                               │    │
│  └──────────────────────────────────────────────────┘    │
│                                                          │
│  ┌─ Tabs max-w-5xl ──────────────────────────────────┐   │
│  │  我的技能 · 我的实践 · 点赞 · 投稿 · 关注            │   │
│  │  ──────                                            │   │
│  │  (当前 tab 的列表 / 网格)                            │   │
│  │   - 点赞的技能：3-col 网格（SkillCard）              │   │
│  │   - 我的实践：帖子卡列表                              │   │
│  │   - 投稿记录：带状态 tag 的列表                      │   │
│  │   - 关注：user 头像网格                              │   │
│  └──────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘
```

## User 卡片

```tsx
const UserCard = ({ profile, stats, onEdit, onLogout }) => (
  <section className="bg-white rounded-2xl border border-slate-200/60 p-6 mb-6">
    <div className="flex items-start gap-5">
      {/* 头像 */}
      <div className="shrink-0">
        {profile.avatarUrl
          ? <img src={profile.avatarUrl} className="w-20 h-20 rounded-full object-cover ring-2 ring-slate-100" />
          : <LetterAvatar name={profile.nickname} index={profile.id} size={80} />}
      </div>

      {/* 信息 */}
      <div className="flex-1 min-w-0">
        <div className="flex items-baseline gap-3">
          <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight">
            {profile.nickname}
          </h1>
          {profile.isAdmin && (
            <TealPill>管理员</TealPill>
          )}
        </div>
        {profile.bio && (
          <p className="mt-1 text-sm text-slate-500 leading-relaxed">{profile.bio}</p>
        )}
        <div className="flex items-center gap-5 mt-3 text-sm">
          <StatInline label="关注" value={stats.followingCount} />
          <StatInline label="粉丝" value={stats.followersCount} />
          <StatInline label="获赞" value={stats.totalLikes} />
        </div>
      </div>

      {/* 操作 */}
      <div className="flex flex-col gap-2 shrink-0">
        <DarkPrimaryCta size="sm" icon={<EditOutlined />} onClick={onEdit}>
          编辑资料
        </DarkPrimaryCta>
        <button onClick={onLogout}
          className="inline-flex items-center justify-center gap-1.5 px-4 py-1.5 rounded-xl
                     border border-slate-200 text-sm font-medium text-slate-600
                     hover:border-slate-300 hover:text-slate-900 transition-all">
          <LogoutOutlined /> 退出登录
        </button>
      </div>
    </div>
  </section>
);

const StatInline = ({ label, value }: { label: string; value: number }) => (
  <div>
    <span className="text-sm font-bold text-slate-900 tabular-nums">{value}</span>
    <span className="text-sm text-slate-500 ml-1">{label}</span>
  </div>
);
```

## Tabs

```tsx
<Tabs
  items={[
    { key: 'skills',      label: '我的技能',   children: <MySkillsList /> },
    { key: 'practices',   label: '我的实践',   children: <MyPracticesList /> },
    { key: 'liked',       label: '点赞',      children: <LikedSkillsGrid /> },
    { key: 'submissions', label: '投稿记录', children: <SubmissionHistory /> },
    { key: 'following',   label: '关注',      children: <FollowingGrid /> },
  ]}
  className="[&_.ant-tabs-nav]:px-0"
/>
```

## 投稿记录（示范带状态 tag 的列表）

```tsx
const SubmissionItem = ({ item }: { item: SkillSubmissionItem }) => {
  const statusCls: Record<string, string> = {
    pending:   'bg-amber-50 text-amber-700 border-amber-200',
    approved:  'bg-emerald-50 text-emerald-700 border-emerald-200',
    rejected:  'bg-rose-50 text-rose-700 border-rose-200',
    reviewing: 'bg-blue-50 text-blue-700 border-blue-200',
  };
  const statusLabel: Record<string, string> = {
    pending: '待审核', approved: '已通过', rejected: '已拒绝', reviewing: '审核中',
  };
  return (
    <div className="flex items-center justify-between py-3 border-b border-slate-100 last:border-b-0">
      <div className="min-w-0 flex-1">
        <div className="text-sm font-bold text-slate-900 truncate">{item.skillName}</div>
        <div className="text-xs text-slate-500 mt-0.5">{item.submittedAt}</div>
      </div>
      <span className={`text-[11px] font-semibold px-2.5 py-0.5 rounded-full border
                        ${statusCls[item.status]}`}>
        {statusLabel[item.status]}
      </span>
    </div>
  );
};
```

## 适配指南

- User 卡片用 `bg-white border rounded-2xl`——和首页发现的卡是同一层级
- 3 个 stat inline 用 `text-sm` 不要大字号——这是次要信息，不是 profile 公开页（那个大字号留给 user-public-profile）
- Tab panel 内容高度**不固定**——让各 tab 的内容自己撑；空态用 EmptyState
- Tab 下方空一行呼吸后再放内容——`[&_.ant-tabs-nav]:mb-4`
- 退出登录按钮用 ghost（border 非 dark）——危险度中等，不给它 primary 地位

## 反模式

- 不要把"我的"做成全屏 Dashboard（多个 widget）——和 admin overview 分界模糊
- 不要用 Antd `<Descriptions>` 做用户信息——Inline stats 更紧凑更贴本 style
- 不要把 Tabs 用 antd 默认 underline ink bar + 默认间距——已在 index.less 改 slate-900 ink bar，不要再 override
- 不要把投稿记录的状态 tag 用 teal——这里语义色必须明确（绿=通过 / 黄=等 / 红=拒）
