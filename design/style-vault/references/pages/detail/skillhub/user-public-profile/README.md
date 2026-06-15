---
id: pages/detail/skillhub/user-public-profile
type: page
name: 用户公开主页
description: 浏览他人主页——大 hero 头像 + 关注按钮 + 实践列表 + 相关技能
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - blocks/nav/skillhub/glass-pill-navbar
  - components/buttons/skillhub/dark-primary-cta
  - components/avatars-icons/skillhub/letter-avatar
  - components/tags-badges/skillhub/teal-pill
  - tokens/palettes/skillhub/skillhub-teal-mist
preview: /preview/pages/detail/skillhub/user-public-profile
---

# User Public Profile

> 访问 `/users/:id` 看别人的主页。**大 hero 头像**（112×112，居中）+ 昵称 + bio + stats + **关注 / 私信** 操作，下方 tab 切内容。和 `user-home`（我的）的区别：**此页更强调 public-facing 气质**（大头像 + 居中布局 + 关注/私信 CTA）。

## 页面骨架

```
┌─ GlassPillNavbar ─────────────────────────────────────┐
│                                                       │
│  ┌─ Hero 居中容器 max-w-3xl mx-auto pt-12 ─────────┐   │
│  │                                                   │   │
│  │  [大头像 112×112]                                 │   │
│  │                                                   │   │
│  │  [昵称 text-3xl extrabold]                        │   │
│  │  [bio 一段 text-slate-500]                        │   │
│  │                                                   │   │
│  │  [关注 XX] [粉丝 XX] [获赞 XX]（stat inline）     │   │
│  │                                                   │   │
│  │  [关注 / 已关注] [私信]                            │   │
│  │                                                   │   │
│  └──────────────────────────────────────────────────┘   │
│                                                       │
│  ┌─ Tabs max-w-5xl ──────────────────────────────┐    │
│  │  实践（N） · 技能（M）                         │    │
│  │  (列表内容)                                    │    │
│  └──────────────────────────────────────────────┘    │
└───────────────────────────────────────────────────────┘
```

## 核心代码

```tsx
export const UserPublicProfile = () => {
  const { id } = useParams();
  const [user, setUser] = useState<UserPublic | null>(null);
  const [isFollowing, setIsFollowing] = useState(false);

  return (
    <>
      <GlassPillNavbar /* ... */ />

      <div className="max-w-5xl mx-auto px-4 sm:px-6 pb-16">
        {/* Hero */}
        <section className="pt-12 pb-10 text-center">
          <div className="inline-block mb-5">
            {user?.avatarUrl
              ? <img src={user.avatarUrl} className="w-28 h-28 rounded-full object-cover ring-2 ring-slate-100 shadow-sm" />
              : <LetterAvatar name={user?.nickname ?? ''} index={user?.id ?? 0} size={112} />}
          </div>

          <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
            {user?.nickname}
          </h1>

          {user?.bio && (
            <p className="mt-2 text-slate-500 max-w-xl mx-auto leading-relaxed">
              {user.bio}
            </p>
          )}

          <div className="flex items-center justify-center gap-6 mt-4 text-sm">
            <StatInline label="关注" value={user?.followingCount ?? 0} />
            <StatInline label="粉丝" value={user?.followersCount ?? 0} />
            <StatInline label="获赞" value={user?.totalLikes ?? 0} />
          </div>

          {!isCurrentUser && (
            <div className="flex items-center justify-center gap-2 mt-6">
              <DarkPrimaryCta
                size="md"
                icon={isFollowing ? <UserMinus size={14} /> : <UserPlus size={14} />}
                onClick={handleFollow}
                variant={isFollowing ? 'slate' : 'pure'}
              >
                {isFollowing ? '已关注' : '关注'}
              </DarkPrimaryCta>
              <button
                onClick={() => navigate(`/messages?to=${id}`)}
                className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl
                           border border-slate-300 text-sm font-medium text-slate-700
                           hover:border-slate-400 transition-all active:scale-95"
              >
                <MessageSquare size={14} /> 私信
              </button>
            </div>
          )}
        </section>

        {/* Tabs */}
        <Tabs
          centered
          items={[
            { key: 'practices', label: `实践 · ${user?.practiceCount ?? 0}`, children: <UserPractices id={id} /> },
            { key: 'skills',    label: `技能 · ${user?.skillCount ?? 0}`,    children: <UserSkills id={id} /> },
          ]}
        />
      </div>
    </>
  );
};
```

## 视觉要点

- Hero 居中布局（比起 user-home 的横向 user-card）——让"浏览别人"有一种到访感
- 头像 112×112 比 user-home 的 80×80 更大——强调是 "谁"
- 用户头像 `ring-2 ring-slate-100`（不是 teal）——保持视觉克制
- 关注按钮 2 态：
  - 未关注：pure dark `#1a1a1a`（召唤）
  - 已关注：slate-900 `variant="slate"` + 文字 "已关注"（弱化）
- 私信是 ghost——关注是主，私信是次

## 适配指南

- `user-home`（/me）用横向卡；`user-public-profile`（/users/:id）用居中 hero——别混淆两套
- Hero padding `pt-12 pb-10`——够留白，但不浪费空间
- Tabs 居中 `centered`（Antd prop），分页仅 2 个——选项多时可加"点赞的 skill" / "关注的人"等
- 只有当 `id !== currentUserId` 时才显示关注/私信按钮——自己看自己不该有

## 反模式

- 不要在公开主页放"编辑资料"按钮——那是 `/me` 的事
- 不要让 bio 区域没有 max-width——`max-w-xl` 限制让长 bio 不跨到边缘
- 不要用 ring-teal 给头像——抢眼且用错语义
- 不要让"已关注"变成绿色 pill——依然黑底 + 文字切换，保持交互一致
