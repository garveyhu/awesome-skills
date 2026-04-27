---
id: pages/pricing/acme/saas-cold-pricing
type: page
name: 冷感 SaaS 定价页
description: 工具型 SaaS 定价对比 · 3 档方案 + feature matrix + FAQ
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
preview: /preview/pages/pricing/acme/saas-cold-pricing
---

# Cold SaaS Pricing

> 工具型 SaaS 的定价页：3 档卡片 + 完整 feature matrix + 简短 FAQ。

## 视觉特征

自上而下：

1. **Hero**（py-20）：标题 "Pricing · pay for what you observe"（48px Plex Sans medium）+ 副文 + 月/年切换 segmented control
2. **3 档方案卡**（grid-cols-3, gap-px）：
   - **Starter** (Free)：低层订阅自助
   - **Team** ($99/mo)：中间档加 cyan-400 1px border + cyan caption "Recommended"
   - **Enterprise** (Contact)：定制
   - 每卡：plan name + price (Plex Mono 36px) + period + 5-7 行 feature 列表（✓ 前缀，slate-300）+ 主 CTA (cyan-cta / ghost-button)
3. **Feature matrix**（完整对比表）：
   - 行 = feature（30+ 项），列 = 三档
   - cell 内容：`✓` / `–` / mono 数字（如 "10k req/mo"）
   - 类目用 sticky section header（slate-800 底）
4. **FAQ**（4-6 折叠条）：每条 caret + 标题，展开后 paragraph

## 反模式

- 不要给中间档（Team）填实色 cyan 背景——破坏冷感；只 1px border
- 不要价格闪烁动画
- 不要写"立省 30%！"等促销文字（B2B 工具 SaaS 的口吻不是 D2C）
