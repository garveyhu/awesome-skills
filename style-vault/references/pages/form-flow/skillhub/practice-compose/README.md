---
id: pages/form-flow/skillhub/practice-compose
type: page
name: 实践帖发布编辑器
description: 大标题输入 + 关联 skill 多选 + Markdown 编辑器 + 预览切换 + 发布 CTA
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - blocks/nav/skillhub/glass-pill-navbar
  - components/buttons/skillhub/dark-primary-cta
  - components/inputs/skillhub/soft-form-input
  - components/tags-badges/skillhub/teal-pill
  - tokens/typography/pairs/skillhub/inter-jetbrains-duo
preview: /preview/pages/form-flow/skillhub/practice-compose
---

# Practice Compose

> 发布实践帖的长文编辑器。顶部是无边框大标题输入（直接像 Notion 顶部），中部是关联 skill 多选 + Markdown 编辑器（`@uiw/react-md-editor`），顶部 sticky 操作条放"保存草稿 / 预览 / 发布"。

## 页面骨架

```
┌─ GlassPillNavbar ──────────────────────────────────────┐
│                                                        │
│  ┌─ Sticky top 栏 (编辑态) ──────────────────────┐      │
│  │  ← 返回  |  草稿已保存 · 10秒前  |  [预览] [发布]│      │
│  └──────────────────────────────────────────────┘      │
│                                                        │
│  ┌─ 编辑容器 max-w-3xl mx-auto ─────────────────┐      │
│  │  [大标题输入·无边框 text-3xl extrabold]       │      │
│  │                                               │      │
│  │  [关联 skills: 输入/选择，带 pill 展示选中]    │      │
│  │                                               │      │
│  │  [MDEditor 全宽 · 工具栏 + 内容]               │      │
│  │    - live preview 开关                        │      │
│  │    - 高度 400-600px                           │      │
│  └───────────────────────────────────────────────┘      │
│                                                        │
│  （预览模式时，以 prose 渲染，保留标题 + skills）       │
└────────────────────────────────────────────────────────┘
```

## 核心代码（骨架）

```tsx
import MDEditor from '@uiw/react-md-editor';

type Mode = 'edit' | 'preview';

export const PracticeCompose = () => {
  const [mode, setMode] = useState<Mode>('edit');
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [selectedSkills, setSelectedSkills] = useState<string[]>([]);
  const [skillInput, setSkillInput] = useState('');
  const [savedAt, setSavedAt] = useState<Date | null>(null);

  // 自动保存草稿（每 10s）
  useEffect(() => {
    const id = setInterval(() => {
      if (title || content) {
        saveDraft({ title, content, skills: selectedSkills });
        setSavedAt(new Date());
      }
    }, 10000);
    return () => clearInterval(id);
  }, [title, content, selectedSkills]);

  return (
    <>
      <GlassPillNavbar /* ... */ />

      {/* Sticky 操作栏 */}
      <div className="sticky top-0 z-40 bg-white/85 backdrop-blur-lg border-b border-slate-200/60">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 py-3 flex items-center justify-between">
          <Link to="/practice" className="inline-flex items-center gap-1.5 text-sm text-slate-500
                                          hover:text-slate-900 transition-colors">
            <ArrowLeft size={16} /> 返回
          </Link>
          <div className="text-xs text-slate-400 font-medium">
            {savedAt ? `草稿已保存 · ${timeAgo(savedAt)}` : '未保存'}
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setMode(mode === 'edit' ? 'preview' : 'edit')}
              className="px-4 py-1.5 rounded-xl border border-slate-200 text-sm font-medium
                         text-slate-700 hover:border-slate-300 transition-all">
              {mode === 'edit' ? '预览' : '返回编辑'}
            </button>
            <DarkPrimaryCta size="sm" icon={<Send size={13} />}
              onClick={handlePublish}
              disabled={!title || !content}>
              发布
            </DarkPrimaryCta>
          </div>
        </div>
      </div>

      <div className="max-w-3xl mx-auto px-4 sm:px-6 py-8">
        {mode === 'edit' ? (
          <>
            {/* 大标题输入 */}
            <input
              placeholder="输入标题..."
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              maxLength={80}
              className="w-full text-3xl font-extrabold text-slate-900 tracking-tight
                         border-0 outline-none bg-transparent placeholder:text-slate-300
                         mb-6 font-sans"
            />

            {/* 关联 skills */}
            <div className="mb-6">
              <div className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
                关联 Skill
              </div>
              <div className="flex items-center flex-wrap gap-2 mb-2">
                {selectedSkills.map((s) => (
                  <TealPill key={s} /* closable */>{s}</TealPill>
                ))}
              </div>
              <input
                placeholder="输入 skill slug 按 Enter 添加"
                value={skillInput}
                onChange={(e) => setSkillInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && skillInput.trim()) {
                    setSelectedSkills([...selectedSkills, skillInput.trim()]);
                    setSkillInput('');
                  }
                }}
                className="w-full bg-white border border-slate-200 rounded-lg
                           px-3 py-2 text-sm
                           focus:border-slate-400 focus:ring-2 focus:ring-slate-200
                           outline-none transition-all"
              />
            </div>

            {/* Markdown 编辑器 */}
            <div data-color-mode="light">
              <MDEditor
                value={content}
                onChange={(v) => setContent(v ?? '')}
                height={500}
                preview="edit"
                hideToolbar={false}
                textareaProps={{ placeholder: '在这里写下你的实践心得...' }}
              />
            </div>
          </>
        ) : (
          /* 预览模式 */
          <article className="prose prose-slate max-w-none">
            <h1>{title || '（无标题）'}</h1>
            <div className="flex gap-1.5 flex-wrap not-prose mb-6">
              {selectedSkills.map((s) => <TealPill key={s}>{s}</TealPill>)}
            </div>
            <ReactMarkdown rehypePlugins={[rehypeRaw]} remarkPlugins={[remarkGfm]}>
              {content}
            </ReactMarkdown>
          </article>
        )}
      </div>
    </>
  );
};
```

## 适配指南

- 标题输入**不加 border + placeholder 用 text-slate-300 淡灰**——像 Notion 的无边界标题编辑
- MDEditor 设 `data-color-mode="light"` 强制浅色（避免系统 dark 打破整体）
- 关联 skill 用"输入 + Enter 添加 + TealPill 展示"三件套，比下拉搜索选择更轻量
- 草稿自动保存 10s 一次——提示条文字 `text-xs text-slate-400`，低调但看得见
- 编辑/预览切换用 `mode` 状态，共用同一个容器——切换时不要"新开一页"

## 反模式

- 不要让标题输入保留 border——编辑器气质一下子变成"表单"
- 不要把关联 skill 放在底部（发布前才选）——先声明关联有助于用户组织内容
- 不要用 Antd Form 包所有字段——标题 + markdown + skills 分别是自定义 input，Form 的 label 会打乱版式
- 不要给 MDEditor 外层加 shadow / rounded-2xl——编辑器自带工具栏边框，多一层包会显得拥挤
