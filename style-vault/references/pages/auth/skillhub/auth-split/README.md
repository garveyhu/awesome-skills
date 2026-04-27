---
id: pages/auth/skillhub/auth-split
type: page
name: 登录注册分屏
description: 左表单 / 右视觉（slate 渐变 + slogan）的经典双栏登录页
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - blocks/form/skillhub/auth-split-form
  - tokens/palettes/skillhub/skillhub-teal-mist
  - tokens/typography/pairs/skillhub/inter-jetbrains-duo
preview: /preview/pages/auth/skillhub/auth-split
---

# Auth Split

> `/login` + `/register` 共用一个页面。左半是 `blocks/form/skillhub/auth-split-form`，右半（仅 lg+ 屏）是 slate-900→950 渐变的 visual panel + slogan。

## 页面骨架

```
┌──────────────────────────────┬─────────────────────────┐
│  左 1/2（小屏：占满）         │  右 1/2（仅 lg+ 显示）  │
│  ────────────────────         │  ────────────────       │
│                              │                         │
│  垂直居中：                   │  slate-900→950 渐变底    │
│   [logo + 标题]               │                         │
│   [mode 切换 pill]            │  Slogan                 │
│   [字段组]                    │  "让 AI 技能流动起来"    │
│   [提交按钮]                  │                         │
│   [Google 登录]               │  (可选装饰: 流光 / 网格) │
│                              │                         │
└──────────────────────────────┴─────────────────────────┘
```

## 核心代码

```tsx
export const AuthSplitPage = () => {
  return (
    <div className="min-h-screen bg-slate-50 flex font-sans">
      {/* 左：表单 */}
      <div className="flex-1 flex flex-col justify-center py-12 px-4 sm:px-6
                      lg:flex-none lg:px-20 xl:px-24 w-full lg:w-1/2">
        <AuthSplitForm />
      </div>

      {/* 右：视觉面板（仅 lg+） */}
      <div className="hidden lg:flex lg:flex-1 relative overflow-hidden
                      bg-gradient-to-br from-slate-900 to-slate-950
                      items-center justify-center text-white">
        <div className="max-w-md px-12 text-center relative z-10">
          <div className="text-xs uppercase tracking-[0.2em] text-white/50 mb-3">
            Visual Panel
          </div>
          <h2 className="text-4xl font-extrabold leading-tight tracking-tight">
            让 AI 技能{' '}
            <span className="bg-[length:300%_100%] bg-clip-text text-transparent
                             animate-[flow-right_14s_linear_infinite]"
                  style={{
                    backgroundImage:
                      'linear-gradient(90deg, #5eead4, #67e8f9, #7dd3fc, #f9a8d4, #5eead4, #67e8f9, #7dd3fc, #f9a8d4, #5eead4)',
                  }}>
              流动起来
            </span>
          </h2>
          <p className="mt-4 text-white/60 leading-relaxed">
            发现、安装、分享高质量的 AI Skill 技能包
          </p>
        </div>

        {/* 可选装饰：细网格背景 */}
        <div className="absolute inset-0 opacity-10" style={{
          backgroundImage: `linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px),
                            linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)`,
          backgroundSize: '40px 40px',
        }} />
      </div>
    </div>
  );
};
```

## 视觉要点

- 左右 50/50，但小屏隐藏右侧，左侧自动占满
- 左侧 padding `lg:px-20 xl:px-24`——大屏时左右留白大
- 右侧渐变底用 slate-900→950（同 logo 方块色）保持一致感
- Slogan 的流动词沿用 `flow-right` 14s，但色系换为浅系（teal-300 / cyan-300 / sky-300 / rose-300）——因为底已经是深色
- 右侧网格底纹 `opacity-10`——几乎看不见但赋予质感
- 右下可装饰 `BorderTrace`的缩小版 / 品牌字母水印——但不建议第一版就上，留意 hero 不宜多动效

## 适配指南

- lg 断点以下右侧完全隐藏——不要做 5:3 / 6:4 的妥协，会两边都不对
- bg-slate-50 作为页面兜底（表单区背景）——不要用纯白，灰色背景让白卡（form 区）更突出
- 若要支持多语言：slogan 要能换行和伸缩，`max-w-md` 保证
- Google 登录按钮（或其它 OAuth）固定放在密码表单下方 + `border-t` 分隔

## 反模式

- 不要让右侧视觉面板占大于 55%——左侧表单体验优先
- 不要把右侧做成视频背景 / 连环轮播——注意力会从登录流程上拽走
- 不要让表单顶到页面顶部——`justify-center` 让它垂直居中才舒服
- 不要用 Antd `<Card>` 包表单——它会加多余 border + padding，和极简气质冲突
