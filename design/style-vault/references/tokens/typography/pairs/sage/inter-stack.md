---
id: tokens/typography/pairs/sage/inter-stack
type: token
name: Inter 单字体栈
description: Inter 本地字体替代 Google Fonts + sans 单字体策略，让中文 fallback 接管 CJK 字
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm]
  stack: [react-antd-tailwind]
uses: []
preview: /preview/tokens/typography/pairs/sage/inter-stack
---

# Sage Inter Stack

> sage 不做 "sans + mono" 双字体——只用 Inter 一种英文字体，CJK 字体由系统 fallback 接管。Inter 文件本地化（`@import url('../fonts/inter.css')`）避开 Google Fonts 外网请求，国内可用且 LCP 稳定。

## Tokens

```json
{
  "fontFamily": {
    "body": "Inter, sans-serif",
    "fallbackChain": "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif"
  },
  "fontImport": "@import url('../fonts/inter.css')",
  "antdInjection": "整站 AntdApp 包裹 + ConfigProvider 不覆盖默认 fontFamily，让 Inter 统一接管",
  "scale": {
    "xs":   "12px (text-xs · meta / footer / tooltip)",
    "sm":   "14px (text-sm · 正文 / form label / 按钮)",
    "base": "16px (text-base · ChatInput 主输入)",
    "lg":   "18px (text-lg · empty state title)",
    "xl":   "20px (text-xl)",
    "2xl":  "24px (text-2xl · 登录页 title / ManagementLayout title)",
    "3xl":  "30px (text-3xl · empty placeholder)"
  },
  "weight": {
    "normal":   400,
    "medium":   500,
    "semibold": 600,
    "bold":     700
  },
  "tracking": {
    "tight":  "-0.01em (h2 / sidebar header)",
    "normal": "0",
    "wider":  "0.05em (text-xs uppercase 小标题)"
  },
  "letterSpacing": {
    "metaCaps": "uppercase tracking-wider text-xs font-semibold text-slate-400 (用于 sidebar 分组、表单 step、command palette 分类标题)"
  }
}
```

## 视觉特征

- 单字体策略让整站气质统一——没有"代码区域用 mono"那种语义切换
- meta 小标题用 `uppercase tracking-wider text-xs`——出现 9 处，是 sage 信息分组的"印章"
- 标题字重最高 `font-bold` (700)，没有 800/900 的"展示字"层级
- 行高靠 Tailwind 默认 1.5，不另设

## 适配指南

- 全局已在 `body { font-family: Inter, sans-serif; }` 注入
- 单字符标识使用 `<UserAvatarIcon />` 而非首字母 avatar——sage 用 lucide 图标做头像视觉锚
- 若需展示代码，inline `<code>` 由 `prose` (markdown) 处理；不在主 UI 使用等宽

## 反模式

- ❌ 引入第二英文字体（mono / display）—— 破坏单字体气质
- ❌ Google Fonts CDN —— 国内环境会拖慢首屏
