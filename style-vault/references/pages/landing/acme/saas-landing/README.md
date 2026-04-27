---
id: pages/landing/acme/saas-landing
type: page
name: SaaS 落地页
description: 标准 SaaS 落地页骨架：Hero / Feature Grid / Pricing / CTA
platforms: [web]
theme: both
tags:
  aesthetic: [minimal]
  mood: [serious]
  stack: [react-antd-tailwind, html-tailwind]
preview: /preview/pages/landing/acme/saas-landing
---

# SaaS Landing

> SaaS 营销落地页骨架，仅定义结构与留白节奏，色字由 style 注入

## 视觉特征

五个 section 上下堆叠：
1. Hero（大字标题 + 两行副文 + CTA 对）
2. Logo 墙（灰度 logo 排列）
3. Feature Grid 3×2
4. Pricing（3 档）
5. CTA Banner（大字 + 单 CTA）

## 核心代码

（略——preview.tsx 里有真实实现）

## 适配指南

- 色/字通过 CSS 变量 `--font-sans` / `--color-accent` 注入，不在 page 里 hardcode
- 各 section 上下内边距 `py-16` 或 `py-24`
- 单栏最大宽 `max-w-6xl`
- Hero 行高紧凑（leading-tight），其他 section 行高正常

## 反模式

- 不要在 page 里定义具体色值
- 不要加装饰性 SVG（归 style 管）
