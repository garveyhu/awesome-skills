# 素材溯源 · SkillHub Tier 3

## 项目路径

- `$PROJECT = ~/Coding/A-complex/ikt/skills/skillhub`
- 技术栈指纹：react 19 + antd 6 + tailwind 4 + vite 8 + framer-motion 12

## Discovery 产物

### 路由清单（12 条全枚举）

| Route | File | 行数 | 沉淀条目 |
|---|---|---|---|
| `/` / `/discover` | `discovery/pages/home/index.tsx` | 546 | `pages/landing/skill-community-home`（Tier 2 已有）|
| `/skills/:author/:skillName` | `skill/pages/detail/index.tsx` | **703** | `pages/detail/skill-article-detail` |
| `/skills/submit` | `skill/pages/publish/index.tsx` | ~600 | `pages/form-flow/skill-publish-wizard` |
| `/practice` | `practice/pages/index.tsx` | 387 | `pages/list-table/practice-plaza` |
| `/practice/:id` | `practice/pages/detail/index.tsx` | 388 | `pages/detail/practice-post-detail` |
| `/practice/create` | `practice/pages/create/index.tsx` | 153 | `pages/form-flow/practice-compose` |
| `/messages` | `message/pages/index.tsx` | ~500 | `pages/content-reader/im-conversation` |
| `/me` | `me/pages/index.tsx` | ~400 | `pages/dashboard/user-home` |
| `/me/edit` | `me/pages/edit/index.tsx` | ~300 | `pages/form-flow/profile-edit` |
| `/admin` (整页) | `admin/pages/index.tsx` | 950+ | `pages/list-table/admin-console`（Tier 2）+ `pages/dashboard/admin-overview`（Tier 3 拆）|
| `/users/:id` | `user/pages/profile/index.tsx` | ~200 | `pages/detail/user-public-profile` |
| `/login` `/register` | `auth/pages/login/index.tsx` | ~180 | `pages/auth/auth-split` |

**覆盖率：13/12 = 108%**（admin 拆了 overview 故超 100%）

### 全局模式扫描产物

```bash
# 命令
grep -rhoE 'bg-\[#1a1a1a\]|bg-\[#2b2b2b\]|bg-slate-900' $PROJECT/frontend/src
# 结果：19 hit 跨 9 文件
```

| 模式 | hit | 文件 | 沉淀为 |
|---|---|---|---|
| `bg-[#1a1a1a]`+`bg-slate-900`+`bg-[#2b2b2b]` | 19 | 9（MainLayout / 登录 / 首页 / 广场 / admin / message / user profile / detail / skill detail）| `components/buttons/dark-primary-cta` |
| `border-slate-300 rounded-xl focus:…primary-500` | 7 | 多（登录表单 / 编辑资料 / 发布）| `components/inputs/soft-form-input` |
| `bg-gradient-to-br from-indigo-500 to-indigo-400 shadow-indigo-500/25` | 4 | 1（admin overview）| `blocks/display/gradient-stat-card` |

### 表单扫描产物

```bash
grep -rlE '<form|onSubmit' $PROJECT/frontend/src
# 结果：3+ 文件
```

| 表单 | 路由 | 字段 | 沉淀为 |
|---|---|---|---|
| 登录 / 注册 | `/login` | email + password + nickname + confirmPassword + mode toggle | `blocks/form/auth-split-form` |
| 编辑资料 | `/me/edit` | nickname + bio + avatar picker + gender + birthday + location | `blocks/form/profile-edit-form` |
| 发布实践 | `/practice/create` | title + markdown + skills picker | 并入 `pages/form-flow/practice-compose` |
| 发布技能 | `/skills/submit` | Git URL / 文件上传 + 预览 + 提交 3 步 | 并入 `pages/form-flow/skill-publish-wizard` |

### 状态清单

| 状态 | 来源 | 视觉 | 沉淀为 |
|---|---|---|---|
| Loading skeleton | `discovery/home/index.tsx:440` | `h-48 animate-pulse bg-white border-gray-100 rounded-2xl` | `blocks/feedback/skeleton-card` |
| Empty | `discovery/home/index.tsx:444` / admin / practice | `border-dashed + Box icon + text-gray-300` | `blocks/feedback/empty-state` |
| Pulse dot (emerald) | `MainLayout.tsx:253` | `w-1.5 h-1.5 bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.8)] animate-pulse` | `components/indicators/pulse-dot` |
| Unread dot (orange) | `MainLayout.tsx:116` | `w-1.5 h-1.5 bg-orange-500` | 并入 `pulse-dot` 变体 |

## 关键源文件行号

### 本次聚焦的新路由

- `skill/pages/detail/index.tsx:1-703` · 整页（sidebar + markdown prose + comments）
- `skill/pages/publish/index.tsx:1-200` · 3 步 wizard（source/preview/done）
- `practice/pages/index.tsx:103-175` · 紧凑 hero + search + 发布按钮
- `practice/pages/index.tsx:177-280` · PostCard 样式
- `practice/pages/detail/index.tsx:1-388` · 单栏 prose
- `practice/pages/create/index.tsx:1-153` · 编辑器
- `message/pages/index.tsx:40-200` · 双列 IM
- `me/pages/index.tsx:1-400` · User 卡 + Tabs
- `me/pages/edit/index.tsx:1-300` · Avatar picker + 字段
- `user/pages/profile/index.tsx:1-200` · 居中 hero
- `auth/pages/login/index.tsx:121-280` · 分屏表单
- `admin/pages/index.tsx:862-950` · 运营概览 stat card + 分布 + 趋势

### 全局模式涉及文件

统一黑底 CTA 的 9 处：
- `core/components/layout/MainLayout.tsx:156` · 登录按钮
- `system/discovery/pages/home/index.tsx:78` · hero BorderTrace
- `system/practice/pages/index.tsx:158` · 发布实践
- `system/practice/pages/index.tsx:132` · 筛选 applySkillFilter
- `system/auth/pages/login/index.tsx` · 登录/注册 submit
- `system/skill/pages/detail/index.tsx` · 使用 skill / 评论
- `system/admin/pages/index.tsx` · 各 action
- `system/message/pages/index.tsx` · 发送
- `system/me/pages/edit/index.tsx` · 保存

## 识别的技术栈

`react-antd-tailwind`（与 Tier 2 沉淀一致）

## Tier 3 Discovery 花的时间

- 路由枚举：~10 min（grep + 目录 find）
- 跨文件模式扫描：~15 min（grep / uniq / 映射）
- 表单 + 状态扫描：~10 min
- 各路由源码通读：~45 min
- 合计 discovery：~80 min，落在 Tier 3 预估（90 min）区间内
