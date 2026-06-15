---
id: pages/detail/skillhub/skill-article-detail
type: page
name: Skill 技能详情页
description: 顶部 breadcrumb + 安装命令条 + SUMMARY box + SKILL.md 文档 + 280px 元信息 sidebar + timeline 评论区
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - components/avatars-icons/skillhub/letter-avatar
  - tokens/palettes/skillhub/skillhub-teal-mist
  - tokens/typography/pairs/skillhub/inter-jetbrains-duo
preview: /preview/pages/detail/skillhub/skill-article-detail
---

# Skill Article Detail

> 这不是一个"技能博客文章"，而是一个**技能发行物页**（类似 npm 或 PyPI 的 package 页）。**核心 CTA 是顶部那条安装命令**（复制即装），其余元素都围绕"确认是否值得安装"展开——SUMMARY + 文档正文 + sidebar 的使用量/下载量/评分/同仓库 Skills。

## 页面骨架

```
┌─ Top Bar (breadcrumb) · border-b slate-100 ─────────────────────────────┐
│  < · skills / iktapp / ai-skills / req-to-ai-spec    (mono 字 slate-400)│
└─────────────────────────────────────────────────────────────────────────┘

┌─ max-w-6xl 2 列 grid (1fr · 280px · gap-12) ─────────────────────────────┐
│                                                                          │
│  主栏                                      │ Sidebar 280px space-y-5     │
│  ─────                                    │ ─────────────────             │
│                                           │                             │
│  H1 text-2xl font-bold                    │ STATS 3 列（使用/下载/评分）│
│  req-to-ai-spec                           │   使用 0  下载 0  评分 - ★★★★★│
│                                           │                             │
│  ┌─ 安装命令条 slate-50 rounded-lg ────┐  │ ─ border-t                   │
│  │ mkdir -p ~/.claude/... && curl ...   │  │ 来源         iktapp         │
│  │                               [📋]    │  │ 作者标识     ai-skills      │
│  └────────────────────────────────────┘  │ 提交者       links          │
│                                           │ 版本         v1.0.0         │
│  ┌─ SUMMARY box slate-50 ──────────────┐ │ 类型         [一方]          │
│  │ SUMMARY                              │ │ 标签                         │
│  │ 将零散的产品需求…转换为 AI 友好规格… │  │ [开发工具][效率提升]        │
│  └────────────────────────────────────┘  │                             │
│                                           │ ─ border-t                   │
│  [SKILL.md]  ← 黑底 pill + border-b      │ [点赞] [标记使用]            │
│                                           │ [下载压缩包] ← 全宽 ghost    │
│  # req-to-ai-spec                         │                             │
│  将零散、模糊的产品需求…                  │ ─ border-t                   │
│                                           │ 文件 (2)                ⌄   │
│  ## 触发条件                              │                             │
│  当用户提到…                              │ ─ border-t                   │
│                                           │ 社区实践        [去广场]     │
│  ## 使用场景                              │ → 帖 1 标题                  │
│  ...                                       │ → 帖 2 标题                  │
│                                           │                             │
│  ## 输入                                  │ ─ border-t                   │
│  \| 输入 \| 必需 \| ... \|                │ 同一仓库                     │
│                                           │ ┌ Docker Best Practices ┐   │
│  ## 工作流                                │ │ Use when containerizing│   │
│  ### 第1步：输入收集                      │ └──────────────────────┘   │
│  ...                                       │ ┌ Docsify Station ─────┐   │
│                                           │ └──────────────────────┘   │
│                                           │ [更多 (N)]                  │
└──────────────────────────────────────────┴─────────────────────────────┘

┌─ 评论区（lg:max-w-[calc(100% - 280px - 3rem)]）mt-12 ───────────────────┐
│  ━ 评论讨论区 (N)     ← 1.5px 蓝色竖条 bg-blue-500 +H2                 │
│                                                                          │
│  │ (border-l-2 slate-100 · pl-4)                                         │
│  ● ┌─ 评论 card rounded-2xl shadow-sm ─────────────────┐                │
│  │ │ avatar + 昵称                         日期（mono）│                │
│  │ │ 内容                                                │                │
│  │ └──────────────────────────────────────────────────┘                │
│  ● ...                                                                   │
│                                                                          │
│  [Pagination]                                                            │
│                                                                          │
│  ┌─ Compose rounded-3xl border p-6 shadow-sm ──────────────────────────┐│
│  │ textarea "这个东西能在什么场景下用？..."                             ││
│  │ "支持 Markdown 语法"            [投递评论]（slate-900）              ││
│  └────────────────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────────────────┘
```

## 核心视觉要点（挨个对齐源码）

### 1. Top bar breadcrumb
```tsx
<div className="border-b border-slate-100">
  <div className="max-w-6xl mx-auto px-6 lg:px-8">
    <div className="flex items-center gap-3 py-3">
      <button onClick={() => navigate(-1)} className="text-slate-400 hover:text-slate-700 transition-colors">
        <ChevronLeft size={16} />
      </button>
      <div className="flex items-center gap-1.5 text-xs text-slate-400 font-mono">
        <span>skills</span>
        <span className="text-slate-300">/</span>
        <span className="text-slate-500">{source}</span>
        <span className="text-slate-300">/</span>
        <span className="text-slate-500">{author}</span>
        <span className="text-slate-300">/</span>
        <span className="text-slate-600">{skillName}</span>
      </div>
    </div>
  </div>
</div>
```

- 返回按钮只有 chevron，不带文字
- 分隔符 `/` 用 slate-300（很淡）
- 最后一段用 slate-600（轻微强调当前位置）
- 全部 `font-mono text-xs`

### 2. 安装命令条（核心 CTA）
```tsx
<div className="mt-3 flex items-start gap-2 bg-slate-50 rounded-lg border border-slate-200/60 px-3 py-2">
  <code className="flex-1 text-xs font-mono text-slate-600 break-all leading-relaxed">
    mkdir -p ~/.claude/skills/{source}-{author}-{skillName} && curl -sL {origin}/api/skills/{slug}/download | tar -xz -C ~/.claude/skills/{source}-{author}-{skillName}/
  </code>
  <button className="shrink-0 mt-0.5 text-slate-400 hover:text-slate-700">
    <Copy size={13} />
  </button>
  {copied && <span className="text-[10px] text-emerald-500 font-medium shrink-0">已复制</span>}
</div>
```

**关键**：
- 这条**紧跟在 H1 下面**，是页面的第一 CTA
- `rounded-lg` 不是 `rounded-xl`——小圆角更贴命令行气质
- `bg-slate-50` 极轻底，**不是**暗底黑字那种 terminal 风
- 复制成功反馈 `text-emerald-500` 内联文字"已复制"，不是 toast
- `break-all` 保证长 URL 可以断行而不是溢出

### 3. SUMMARY box
```tsx
<div className="mt-4 mb-6 bg-slate-50 rounded-lg border border-slate-200/60 px-4 py-3">
  <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1.5">SUMMARY</div>
  <p className="text-sm text-slate-600 leading-relaxed">{summary}</p>
</div>
```

- 和安装命令条**同系列**（都是 slate-50 + rounded-lg + border-slate-200/60）——形成"发行物元信息区"
- Label 是 `text-[10px]` **极小 uppercase**
- 正文 `text-sm text-slate-600`

### 4. SKILL.md 文档标签
```tsx
<div className="flex items-center gap-1 mb-6 border-b border-slate-100 pb-3">
  <span className="px-3 py-1.5 text-xs font-medium rounded-md bg-slate-900 text-white">
    SKILL.md
  </span>
</div>
```

- 一个黑底小 pill + 下方横线 border-b——像"文档开始"的分隔符
- 预留给未来多 tab（references / examples / CHANGELOG）

### 5. Prose 正文关键 override
```tsx
// ReactMarkdown components 里的定制
h1: border-b border-slate-200 pb-3
h2: border-b border-slate-100 pb-2
blockquote: border-l-4 border-indigo-300 bg-indigo-50/50 pl-4 py-2 not-italic
inline code: bg-slate-100 text-slate-800 px-1.5 py-0.5 rounded font-mono text-sm
pre (带 language): 白底 border + 顶部语言 ribbon 条（bg-slate-100 uppercase language name） + SyntaxHighlighter oneLight
pre (无 language): bg-slate-50 rounded-lg border px-4 py-3
table: wrap with overflow-x-auto
```

**关键**：代码块有"语言条"——`bg-slate-100 text-slate-500 text-xs font-mono uppercase`，这是 prose 独有的装饰。

### 6. Sidebar stats 3 列
```tsx
<div className="flex items-start gap-5">
  <div>
    <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">使用人数</div>
    <div className="text-xl font-extrabold text-slate-900">{usedCount}</div>
  </div>
  {/* 下载量同 */}
  <div>
    <div className="text-[10px] ...">评分</div>
    <div className="flex items-center gap-1.5">
      <span className="text-xl font-extrabold text-slate-900">{avg > 0 ? avg.toFixed(1) : '-'}</span>
      <div className="flex items-center gap-0.5">
        {[1,2,3,4,5].map(n => (
          <button className={`p-0.5 transition-all hover:scale-110 ${
            rating >= n ? 'text-slate-900' : 'text-slate-300 hover:text-slate-500'
          }`}>
            <Star size={11} fill={rating >= n ? 'currentColor' : 'none'} />
          </button>
        ))}
      </div>
    </div>
  </div>
</div>
```

- 3 个指标横排 `gap-5`
- **星星尺寸只 11px**——很小，不抢
- 已评分的星 `text-slate-900`（黑填色，不是金色）；未评的 slate-300
- hover 星放大 `scale-110`

### 7. Sidebar 元信息矩阵
```tsx
<div className="border-t border-slate-100 pt-4 space-y-3">
  {/* 行式 label : value */}
  <div className="flex items-center justify-between">
    <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">来源</span>
    <span className="text-xs font-mono text-slate-600">{source}</span>
  </div>
  {/* ... 作者标识 / 提交者 / 版本 */}

  {/* 类型 特殊 pill */}
  <div className="flex items-center justify-between">
    <span className="text-[10px] ...">类型</span>
    <span className={`text-[10px] font-semibold px-1.5 py-0.5 rounded ${
      originType === 'first_party' ? 'bg-indigo-100 text-indigo-600' : 'bg-amber-100 text-amber-600'
    }`}>
      {originType === 'first_party' ? '一方' : '三方'}
    </span>
  </div>

  {/* 标签 占整行 */}
  <div>
    <span className="text-[10px] ... block mb-1.5">标签</span>
    <div className="flex flex-wrap gap-1">
      {tags.map(t => (
        <span className="px-1.5 py-0.5 rounded bg-slate-100 text-slate-500 text-[10px] font-medium">
          {t}
        </span>
      ))}
    </div>
  </div>
</div>
```

**关键**：
- 元信息 value 用 **font-mono**（来源 / 作者标识 / 版本 走 mono，提交者是人名走 font-medium）
- 类型 pill 小巧 `text-[10px] px-1.5 py-0.5`——不是 teal-pill 的 rounded-full 胶囊，是 rounded（4px）方块 pill
- 标签 pill 用 **slate-100/slate-500**——**不是 teal！** 因为 sidebar 已经有很多信息，teal 会抢；这里用中性 slate 收住

### 8. Actions（点赞 + 标记使用 + 下载）
```tsx
<div className="border-t border-slate-100 pt-4 space-y-2">
  <div className="grid grid-cols-2 gap-2">
    <button className={`flex items-center justify-center gap-1.5 py-2 rounded-lg text-xs font-medium transition-all ${
      liked ? 'bg-slate-900 text-white border border-slate-900' : 'bg-slate-50 text-slate-600 hover:bg-slate-100 border border-slate-200/60'
    }`}>
      <ThumbsUp size={13} className={liked ? 'fill-current' : ''} />
      {liked ? '已点赞' : '点赞'}
    </button>
    <button>...{used ? '在用' : '标记使用'}</button>
  </div>
  <button className="w-full ... bg-slate-50 ..."><Download size={13} /> 下载压缩包</button>
</div>
```

**关键**：
- **全部都是 ghost 态**（`bg-slate-50` + border），**不是** dark CTA——因为安装命令条在主栏已经是"主 CTA"，sidebar 的这些是次级操作
- 激活态（已点赞 / 在用）才变 `bg-slate-900` 填色
- "下载压缩包"也 ghost——它的对标是"点赞"级别，不是主 CTA（主 CTA 是命令条）

### 9. 文件 / 社区实践 / 同一仓库 section 体系

三个 section 都是 `border-t border-slate-100 pt-4` 分段。

```tsx
// 文件折叠
<button className="w-full flex items-center justify-between mb-2">
  <span className="text-[10px] ... tracking-wider">文件 ({count})</span>
  <ChevronDown className={`transition-transform ${open ? 'rotate-180' : ''}`} />
</button>

// 社区实践 label + "去广场" link 右对齐
<div className="flex items-center justify-between mb-2">
  <span className="text-[10px] ...">社区实践</span>
  <Link className="text-[10px] font-medium text-primary-600 hover:underline">去广场</Link>
</div>

// 同一仓库 skill card 小号
<Link className="block p-3 rounded-xl border border-slate-100
                 hover:border-slate-300 hover:shadow-sm transition-all group">
  <h4 className="text-xs font-bold text-slate-900 group-hover:text-primary-600 truncate">
    {name}
  </h4>
  <p className="text-[11px] text-slate-500 line-clamp-1">{summary}</p>
</Link>
```

- "同一仓库"里的小 skill card `rounded-xl p-3`——和主栏 SkillCard 尺寸 / 圆角区分
- 标题 `text-xs font-bold`（超小），summary `text-[11px]` + `line-clamp-1`
- 底部 "更多 (N)" 按钮用 `bg-slate-50` ghost

### 10. 评论区（不在 sidebar 列内）
```tsx
<div className="lg:max-w-[calc(100%-280px-3rem)] mt-12">
  <h2 className="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2">
    <span className="w-1.5 h-6 rounded-full bg-blue-500"></span>
    评论讨论区 (N)
  </h2>

  <div className="space-y-6 pl-4 border-l-2 border-slate-100">
    {comments.map(c => (
      <div className="relative">
        <div className="absolute -left-[25px] top-0 w-3 h-3 rounded-full bg-slate-200 border-4 border-white" />
        <div className="bg-white rounded-2xl border border-slate-100 p-5 shadow-sm">
          {/* avatar + nickname + 日期（mono 右对齐） + 正文 */}
        </div>
      </div>
    ))}
  </div>

  {/* Compose */}
  <div className="bg-white rounded-3xl border border-slate-200 p-6 mt-8 shadow-sm">
    <textarea className="bg-slate-50 border rounded-xl p-4 min-h-[100px]" />
    <div className="flex justify-between items-center">
      <span className="text-xs text-slate-400">支持 Markdown 语法</span>
      <button className="bg-slate-900 text-white rounded-lg">投递评论</button>
    </div>
  </div>
</div>
```

**关键**：
- 标题左侧 **蓝色竖条 bg-blue-500 w-1.5 h-6 rounded-full**——整站为数不多的"视觉强调竖条"
- 评论列表是**timeline 样式**：左边 border-l-2 + 每条评论 -left-[25px] 外挂小点
- Compose 用 `rounded-3xl`（24px）比普通 card `rounded-2xl` 更大，强调"留言"仪式感
- 评论区宽度 `calc(100% - 280px - 3rem)` —— 不占 sidebar 的位置

## 适配指南

- 这不是 blog 文章页而是"发行物 landing"——**install 命令条必须是页面第一 CTA**，删不得
- Sidebar 按钮统一 ghost 不是 dark-primary-cta——因为主 CTA 已经是命令条
- 元信息 value 的 mono / 非 mono 分工：机器标识走 mono（源 / slug / 版本），人名走非 mono
- 标签在 sidebar 里用 slate-100/500**刻意弱化**——不抢 "使用 / 下载 / 评分" 的视觉重量
- 评论 timeline 小点要 `border-4 border-white`——白色描边让小点从 border-l 线上"浮出"
- 大屏主栏 + sidebar 并列；小屏 sidebar `hidden lg:block`——隐藏不降级简版

## 反模式

- 不要把安装命令块做成 terminal 黑底绿字——slate-50 浅底 mono 字是本 style 的基调
- 不要把"使用此 Skill"作为主 CTA 按钮（我之前这么干过，错了）——主 CTA 就是命令条
- 不要把 sidebar 元信息用 meta 大字号——保持 `text-[10px]` / `text-xs` 的信息密度
- 不要用 `border-l-4 border-blue`（那是 callout 风）——评论区左竖条是 **bg-blue-500 w-1.5 h-6 rounded-full**，不是 border
- 不要把标签改回 teal pill——在 sidebar 语境里 teal 抢戏
