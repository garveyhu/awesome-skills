---
id: pages/auth/acme/auth-cold-split
type: page
name: 冷感 Auth Split
description: 60/40 双栏登录 · 左暗色 brand panel · 右白色 form 仅 email+password+SSO
platforms: [web]
theme: dark
tags:
  aesthetic: [minimal, industrial]
  mood: [cold, serious]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/acme/slate-cyan-ice
  - tokens/typography/pairs/acme/ibm-plex-duo
  - components/buttons/acme/cyan-cta
  - components/buttons/acme/ghost-button
  - components/inputs/acme/mono-input
preview: /preview/pages/auth/acme/auth-cold-split
---

# Auth Cold Split

> ICEOPS / 冷感工业 SaaS 的登录页：左 60% brand panel + 右 40% form。

## 视觉特征

- 整页 split：左 60% 暗色 brand panel `bg-slate-950`，右 40% form `bg-white text-slate-900`
- **左侧 panel**：
  - 顶部 logo（cyan dot + "ICEOPS"）
  - 中部 slogan 大字（Plex Sans 36px medium，3 行最大）："Observability without the noise."
  - 副文案（Plex Sans 14px slate-400）：1-2 行
  - 底部状态条（Plex Mono uppercase 11px）：`v1.4 · cold-industrial-saas`
  - **不**用图、不用插画——纯排版 + 1 个 cyan dot
- **右侧 form**：
  - 标题"Sign in"（Plex Sans 24px slate-900）
  - email + password 输入（白底 + slate-300 border + cyan focus，**不用 mono-input** —— 邮箱不是数字）
  - 主 CTA `<CyanCta>Continue</CyanCta>`
  - 次要 `<GhostButton>Use SSO</GhostButton>`
  - 底部 footer：版权 + privacy / terms 链
- 区别于 SkillHub 的 auth-split：那个是社区暖调（teal accent + 社交登录矩阵 + emoji），本条是企业 B2B（仅 SSO + 邮箱密码、零暖色、零图标装饰）

## 核心代码

```tsx
import { CyanCta } from '../../components/buttons/acme/cyan-cta';
import { GhostButton } from '../../components/buttons/acme/ghost-button';

export default function AuthColdSplitPage() {
  return (
    <div className="h-screen grid" style={{ gridTemplateColumns: '60% 40%' }}>
      {/* left brand panel */}
      <aside className="bg-slate-950 text-slate-100 px-16 py-14 flex flex-col">
        <div className="flex items-center gap-2">
          <span className="w-1.5 h-1.5 rounded-full bg-cyan-400" />
          <span className="font-semibold tracking-wider">ICEOPS</span>
        </div>
        <div className="mt-auto mb-auto max-w-xl">
          <h1 className="font-sans text-[36px] font-medium leading-tight tracking-tight">
            Observability without<br />the noise.
          </h1>
          <p className="mt-5 text-slate-400 text-[15px] leading-relaxed max-w-md">
            冷感留白、无阴影、单一 cyan 高亮色——把注意力还给数据本身。
          </p>
        </div>
        <div className="font-mono text-[11px] uppercase tracking-wider text-slate-500">
          v1.4 · cold-industrial-saas
        </div>
      </aside>

      {/* right form */}
      <main className="bg-white px-12 py-14 flex flex-col">
        <h2 className="font-sans text-[24px] font-semibold text-slate-900">Sign in</h2>
        <p className="mt-1 text-[13px] text-slate-500">Use your work email or company SSO.</p>

        <form className="mt-8 space-y-4">
          <Field label="Email">
            <input type="email" className="w-full h-10 px-3 border border-slate-300 rounded text-slate-900 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500" />
          </Field>
          <Field label="Password">
            <input type="password" className="w-full h-10 px-3 border border-slate-300 rounded text-slate-900 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500" />
          </Field>
          <CyanCta size="lg" className="w-full">Continue</CyanCta>
          <div className="text-center text-[11px] uppercase tracking-wider text-slate-400">— or —</div>
          <GhostButton size="lg" className="w-full">Use SSO</GhostButton>
        </form>

        <footer className="mt-auto pt-8 text-[11px] uppercase tracking-wider text-slate-400 flex justify-between">
          <span>© 2026 Iceops</span>
          <span className="space-x-3">
            <a>Privacy</a>
            <a>Terms</a>
          </span>
        </footer>
      </main>
    </div>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <label className="block">
      <span className="text-[11px] uppercase tracking-wider text-slate-500">{label}</span>
      <div className="mt-1.5">{children}</div>
    </label>
  );
}
```

## 适配指南

- 左右比例固定 60/40；窄屏 < 768 切成上下栈（左 panel 高 240px 折叠成 brand bar）
- 右侧 form 的 input **不要**强行套 mono-input（它是数字字段专用）
- 仅 SSO + email/password；**绝不**加 GitHub / Google / Apple 等社交登录（那是社区产品的语言）

## 反模式

- 不要在左侧 panel 加图 / 渐变 / SVG 装饰
- 不要在 form 上方加品牌 logo（左侧已经有，重复）
- 不要 form 加阴影或圆角容器
