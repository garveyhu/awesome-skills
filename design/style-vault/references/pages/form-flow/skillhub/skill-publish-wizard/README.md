---
id: pages/form-flow/skillhub/skill-publish-wizard
type: page
name: 技能发布向导
description: 3 步向导（添加来源 → 预览确认 → 完成）· 拖拽 / URL / 归档上传 · 实时校验
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
  - tokens/palettes/skillhub/skillhub-teal-mist
  - tokens/motion/skillhub/gentle-flow
preview: /preview/pages/form-flow/skillhub/skill-publish-wizard
---

# Skill Publish Wizard

> 发布新技能的 3 步向导。步骤条顶部横向展示（1·2·3 数字+文字），每步在同一个白卡里切内容，动效 `AnimatePresence` 左右滑入。

## 页面骨架

```
┌─ GlassPillNavbar ───────────────────────────────────────┐
│                                                         │
│  ┌─ 返回 "← 返回我的" ─────────────────────────────┐     │
│                                                         │
│  ┌─ 向导容器 max-w-3xl mx-auto ───────────────────┐     │
│  │  步骤条：                                       │     │
│  │    [① 添加来源] ──── [② 预览确认] ──── [③ 完成] │     │
│  │                                                 │     │
│  │  白卡 rounded-2xl border p-8（当前步骤内容）:   │     │
│  │                                                 │     │
│  │  Step 1: Git / 归档 两 tab                      │     │
│  │    [Git 仓库] [压缩包]                          │     │
│  │    ─────────                                     │     │
│  │    Git: URL input + branch input                │     │
│  │    归档: 拖拽区（border-dashed + icon + hint）  │     │
│  │                                                 │     │
│  │  Step 2: 预览 SKILL.md 解析结果                 │     │
│  │    name / summary / version / tags （字段卡）   │     │
│  │    文件树折叠                                    │     │
│  │                                                 │     │
│  │  Step 3: 完成态                                  │     │
│  │    大 CheckCircle + "已提交审核" + CTA          │     │
│  │                                                 │     │
│  │  底部：[上一步]  [下一步 / 提交]                 │     │
│  └────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────┘
```

## 核心代码（骨架）

```tsx
type Step = 'source' | 'preview' | 'done';
type SourceTab = 'git' | 'archive';

const STEPS: { key: Step; label: string; num: number }[] = [
  { key: 'source',  label: '添加来源',   num: 1 },
  { key: 'preview', label: '预览确认',   num: 2 },
  { key: 'done',    label: '完成',       num: 3 },
];

export const SkillPublishWizard = () => {
  const [step, setStep] = useState<Step>('source');
  const [sourceTab, setSourceTab] = useState<SourceTab>('git');
  const [gitUrl, setGitUrl] = useState('');
  const [branch, setBranch] = useState('main');
  const [file, setFile] = useState<File | null>(null);
  const [parsing, setParsing] = useState(false);
  const [parseResult, setParseResult] = useState<ParsedSkill | null>(null);

  return (
    <>
      <GlassPillNavbar /* ... */ />

      <div className="max-w-3xl mx-auto px-4 sm:px-6 pt-6 pb-16">
        <Link to="/me" className="inline-flex items-center gap-1.5 text-sm text-slate-500
                                  hover:text-slate-900 mb-6 transition-colors">
          <ArrowLeft size={16} /> 返回我的
        </Link>

        {/* 步骤条 */}
        <StepBar steps={STEPS} current={step} />

        {/* 步骤容器 */}
        <div className="bg-white border border-slate-200/60 rounded-2xl p-8 mt-6">
          <AnimatePresence mode="wait">
            {step === 'source'  && <SourceStep  /* props */ />}
            {step === 'preview' && <PreviewStep /* props */ />}
            {step === 'done'    && <DoneStep    /* props */ />}
          </AnimatePresence>
        </div>

        {/* 底部操作 */}
        <div className="flex items-center justify-between mt-6">
          <button
            onClick={() => stepBack(step, setStep)}
            disabled={step === 'source'}
            className="px-4 py-2 text-sm font-medium rounded-xl text-slate-600
                       hover:text-slate-900 disabled:opacity-40
                       disabled:cursor-not-allowed transition-all">
            上一步
          </button>
          <DarkPrimaryCta size="md" onClick={() => stepForward(...)}>
            {step === 'preview' ? '提交审核' : '下一步'}
          </DarkPrimaryCta>
        </div>
      </div>
    </>
  );
};
```

## 步骤条子件

```tsx
const StepBar = ({ steps, current }: { steps: typeof STEPS; current: Step }) => {
  const idx = steps.findIndex((s) => s.key === current);
  return (
    <div className="flex items-center gap-2">
      {steps.map((s, i) => {
        const done = i < idx;
        const active = i === idx;
        return (
          <React.Fragment key={s.key}>
            <div className={`flex items-center gap-2.5
                            ${active ? 'text-slate-900' : done ? 'text-teal-600' : 'text-slate-400'}`}>
              <div className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold
                               ${active ? 'bg-slate-900 text-white'
                                 : done ? 'bg-teal-500 text-white' : 'bg-slate-100 text-slate-400'}`}>
                {done ? <Check size={12} /> : s.num}
              </div>
              <span className="text-sm font-medium">{s.label}</span>
            </div>
            {i < steps.length - 1 && (
              <div className={`flex-1 h-px ${done ? 'bg-teal-500' : 'bg-slate-200'}`} />
            )}
          </React.Fragment>
        );
      })}
    </div>
  );
};
```

## Source step 的拖拽区

```tsx
<div className={`rounded-2xl border-2 border-dashed transition-all ${
  dragging ? 'border-teal-400 bg-teal-50/50' : 'border-slate-300 hover:border-slate-400'
}`}
  onDragEnter={() => setDragging(true)}
  onDragLeave={() => setDragging(false)}
  onDrop={handleDrop}
>
  <div className="p-12 text-center">
    <UploadCloud className="w-12 h-12 text-slate-400 mx-auto mb-3" />
    <div className="text-sm font-semibold text-slate-900">拖拽文件到此处</div>
    <div className="text-xs text-slate-500 mt-1">支持 .zip / .tar.gz，≤ 50MB</div>
    <label className="mt-4 inline-block">
      <input type="file" accept=".zip,.tar.gz" className="hidden" onChange={handleFile} />
      <span className="px-4 py-2 rounded-xl border border-slate-300 text-sm font-medium
                       text-slate-700 hover:border-slate-400 cursor-pointer transition-all">
        或选择文件
      </span>
    </label>
  </div>
</div>
```

## 适配指南

- 3 步 wizard 是本 style 的"发布"骨架；换产品也可以是 2 步 / 4 步，但每步字段控制 ≤ 6 个
- 步骤条要区分 done / active / pending 三态——done 用 teal-500 表示"已通过"，active 用 slate-900 表示"当前"
- 拖拽区用 `border-dashed`，默认 slate-300，dragover 时 teal-400 + bg-teal-50/50 轻染
- 大块白卡 `p-8` 而非 `p-6`——发布页字段少但字段权重高，大 padding 显出"重要"
- 底部按钮 "上一步" 是弱化 text-only，"下一步 / 提交" 是 DarkPrimaryCta——层级分明

## 反模式

- 不要在步骤条下方立刻接字段——中间必须有 `mt-6` 呼吸
- 不要把文件上传和 URL 输入放同个表单——用 Tab 切分
- 不要让 Step 完成态显示 Confetti / 花哨动画——本 style 克制，CheckCircle + 1 行文字就够
- 不要把"提交审核"按钮变绿/变红——统一黑底 CTA；语义靠文字表达
