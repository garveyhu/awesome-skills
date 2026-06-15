---
id: pages/list-table/skillhub/admin-console
type: page
name: 多域管理后台
description: Tabs 切多个管理域 + 每 Tab 里 toolbar-bar + table 的标准列表页
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - blocks/nav/skillhub/glass-pill-navbar
  - blocks/layout/skillhub/toolbar-bar
  - blocks/display/skillhub/table
  - tokens/palettes/skillhub/skillhub-teal-mist
  - tokens/typography/pairs/skillhub/inter-jetbrains-duo
preview: /preview/pages/list-table/skillhub/admin-console
---

# Admin Console

> 平台管理员用的多域管理台——总览 / 仓库 / 投稿 / 实践 / 评论 / 用户 各一 Tab，切换时在同一骨架里换 table

## 页面骨架

```
┌─ GlassPillNavbar (不 sticky) ──────────────────────┐
│                                                    │
│  ┌─ 页面容器 max-w-7xl px-4 py-6 ────────────────┐│
│  │                                                ││
│  │  ┌─ 总览 6 格 Statistic 卡（顶部一屏） ───────┐│
│  │  │  [仓库数] [技能数] [帖子数] [评论] [用户]  ││
│  │  │  [同步成功数]                               ││
│  │  └───────────────────────────────────────────┘││
│  │                                                ││
│  │  ┌─ Tabs ─────────────────────────────────────┐│
│  │  │  仓库 · 投稿 · 实践 · 评论 · 用户           ││
│  │  │  ──────────                                 ││
│  │  │                                             ││
│  │  │  AdminTableToolbar  [搜索][筛选]  [新建]    ││
│  │  │  ┌─ AdminTable ─────────────────────────┐  ││
│  │  │  │ ... rows ...                         │  ││
│  │  │  │ 分页（共 N 条 · 跳至 X 页）           │  ││
│  │  │  └─────────────────────────────────────┘  ││
│  │  └───────────────────────────────────────────┘││
│  │                                                ││
│  └──────────────────────────────────────────────┘│
└────────────────────────────────────────────────────┘
```

## 权限门

访问前先校验角色（localStorage 或 session 里存的 user.roles 包含 `admin`）；否则 Modal 提示"没有权限访问"并跳回首页。

## 核心代码

```tsx
import { Tabs, Statistic } from 'antd';
import {
  Activity, AreaChart, Database, MessagesSquare, Package, ShieldCheck, Users,
} from 'lucide-react';
import { AdminTableToolbar, AdminTable } from '../blocks/...';
import { GlassPillNavbar } from '../blocks/nav/GlassPillNavbar';

export const AdminConsole = () => {
  const [overview, setOverview] = useState<AdminOverview>(emptyOverview);

  return (
    <>
      <GlassPillNavbar sticky={false} /* ...nav props... */ />

      <div className="max-w-7xl mx-auto px-4 py-6 font-sans">
        {/* 1. 总览 6 格 */}
        <section className="mb-6">
          <h1 className="text-2xl font-extrabold text-slate-900 mb-4">管理后台</h1>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
            <StatCard icon={<Database size={16} />} label="仓库" value={overview.repositoryCount} />
            <StatCard icon={<Package  size={16} />} label="技能" value={overview.skillCount} />
            <StatCard icon={<MessagesSquare size={16} />} label="帖子" value={overview.practicePostCount} />
            <StatCard icon={<Activity size={16} />} label="评论" value={overview.commentCount} />
            <StatCard icon={<Users size={16} />}   label="活跃用户" value={overview.activeUserCount} />
            <StatCard icon={<AreaChart size={16} />} label="同步成功" value={overview.successfulSyncCount} />
          </div>
        </section>

        {/* 2. Tabs 多域 */}
        <Tabs
          items={[
            { key: 'repos',       label: '仓库',     children: <ReposPanel /> },
            { key: 'submissions', label: '技能投稿', children: <SubmissionsPanel /> },
            { key: 'practice',    label: '实践',     children: <PracticePanel /> },
            { key: 'comments',    label: '评论',     children: <CommentsPanel /> },
            { key: 'users',       label: '用户',     children: <UsersPanel /> },
            { key: 'skills',      label: '技能',     children: <SkillsPanel /> },
          ]}
        />
      </div>
    </>
  );
};

const StatCard = ({ icon, label, value }) => (
  <div className="bg-white border border-slate-200 rounded-xl p-4 flex items-center gap-3
                  hover:border-slate-300 transition-colors">
    <div className="w-10 h-10 rounded-lg bg-slate-50 text-slate-600 flex items-center justify-center">
      {icon}
    </div>
    <div>
      <div className="text-xs text-slate-400 font-medium">{label}</div>
      <div className="text-xl font-bold text-slate-900 tabular-nums">{value}</div>
    </div>
  </div>
);
```

### 一个 Tab panel 的典型内容（UsersPanel）

```tsx
const UsersPanel = () => {
  const [users, setUsers]     = useState<AdminManagedUser[]>([]);
  const [keyword, setKeyword] = useState('');
  const [roleFilter, setRoleFilter] = useState<string | undefined>();

  const columns: ColumnsType<AdminManagedUser> = [
    {
      title: '用户', dataIndex: 'nickname',
      render: (_, u) => <UserAvatarBadge name={u.nickname} avatarUrl={u.avatarUrl} />,
    },
    { title: '邮箱', dataIndex: 'email' },
    { title: '角色', dataIndex: 'roles',
      render: (roles) => (
        <Space size={4}>
          {roles?.map(r => (
            <Tag key={r} color={r === 'admin' ? 'geekblue' : 'default'}>{r}</Tag>
          ))}
        </Space>
      ),
    },
    { title: '注册时间', dataIndex: 'createdAt' },
    { title: '操作', render: (_, u) => <Button size="small" type="link" onClick={() => openEdit(u)}>编辑角色</Button> },
  ];

  return (
    <>
      <AdminTableToolbar
        searchPlaceholder="搜索昵称 / 邮箱"
        onSearch={setKeyword}
        filters={
          <Select
            size="small" style={{ width: 110 }}
            placeholder="角色" allowClear
            options={[
              { label: '管理员', value: 'admin' },
              { label: '普通用户', value: 'user' },
            ]}
            onChange={setRoleFilter}
          />
        }
      />
      <AdminTable<AdminManagedUser>
        rowKey="id"
        columns={columns}
        dataSource={users.filter(u =>
          (!keyword || u.nickname?.includes(keyword) || u.email?.includes(keyword)) &&
          (!roleFilter || u.roles?.includes(roleFilter))
        )}
      />
    </>
  );
};
```

## 适配指南

- **Tab 切换不触发整页 loading** ——每个 panel 自己拿数据，切过来再 fetch，保持骨架流畅
- 总览 6 格在移动端 `grid-cols-2`、中屏 3、大屏 6——一行 6 个必须 desktop 才开
- 一条管理域里只允许 1 个主 table，多域请拆子 Tab（避免单页 N 个表格一起加载）
- Modal（编辑角色 / 驳回投稿）统一用 Antd Modal，`okText="确认"` / `cancelText="取消"` 中文化，不依赖默认英文
- 审核类操作（通过 / 驳回）按钮色用 Antd 默认 primary/danger，不要改 teal——管理后台里的语义色必须明确

## 反模式

- 不要给 Tab 内的 table 加阴影/圆角容器——`blocks/display/skillhub/table` 的无边框前提就是"裸"
- 不要混用中英文操作按钮——全中文（"编辑 / 驳回 / 通过 / 取消"）
- 不要在同一个 tab 同时展示 2 张 table——用次级筛选器在同一张表切视图
- 不要把 navbar 设 sticky——管理页滚动时 table head sticky 才重要，双 sticky 冲突
