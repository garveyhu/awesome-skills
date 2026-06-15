---
id: products/acme-cold-saas
type: product
name: Acme · 冷感工业 SaaS
description: 冷感工业型监控 SaaS——把注意力留给数据本身，等宽数字 / 状态脉冲 / 零装饰。
platforms: [web]
theme: dark
category: productivity
refs:
  style: styles/saas-tool/cold-industrial-saas
  pages:
    - pages/landing/acme/saas-landing
    - pages/auth/acme/auth-cold-split
    - pages/dashboard/acme/saas-monitor-overview
    - pages/list-table/acme/saas-incident-list
    - pages/pricing/acme/saas-cold-pricing
  blocks:
    - blocks/nav/acme/saas-cold-topbar
    - blocks/display/acme/saas-metric-grid
    - blocks/display/acme/saas-data-table
    - blocks/feedback/acme/saas-status-banner
  components:
    - components/buttons/acme/ghost-button
    - components/buttons/acme/cyan-cta
    - components/inputs/acme/mono-input
    - components/indicators/acme/status-pulse
  tokens:
    palette: tokens/palettes/acme/slate-cyan-ice
    typography: tokens/typography/pairs/acme/ibm-plex-duo
tags:
  aesthetic: [minimal, industrial]
  mood: [cold, serious]
  stack: [react-antd-tailwind]
uses: []
---

## 设计叙事

Acme（ICEOPS）是为 DevOps / SRE 团队打造的冷感观测平台——所有视觉决策服从「信息密度优先」与「告警不打扰」两个原则。

- **数据是主角**：Plex Mono 等宽数字 + 右对齐 + 36-48px 大号 KPI，让数字本身成为视觉重心
- **状态是产品**：healthy 持续呼吸、degraded / critical 静态——异常态绝不闪烁
- **切割不靠阴影**：1px slate-800 hairline 处处分块；圆角 ≤ 4px；全站零阴影
- **单色高亮**：cyan-400 是唯一品牌交互色，承担 CTA / focus / 选中 / 关键 dot
- **零浪漫动效**：100/150/200ms ease-out，无 bounce / 无 scale / 无回弹

## 组成（Tier 2 · 14 条聚合）

### Style
- `styles/saas-tool/cold-industrial-saas` · 整站调性

### Pages · 5 条
| 路由 | Page | 用途 |
|---|---|---|
| `/` | `pages/landing/acme/saas-landing` | 营销落地页（hero + features + pricing strip + CTA）|
| `/login` | `pages/auth/acme/auth-cold-split` | 60/40 双栏登录，仅 SSO + email |
| `/dashboard` | `pages/dashboard/acme/saas-monitor-overview` | 主页 · KPI grid + latency 图 + 服务表 |
| `/incidents` | `pages/list-table/acme/saas-incident-list` | 全量事件列表 · filter chip + 高密度表格 |
| `/pricing` | `pages/pricing/acme/saas-cold-pricing` | 3 档方案 + 完整 feature matrix + FAQ |

### Blocks · 4 条
- `blocks/nav/acme/saas-cold-topbar` · 56px 全局顶栏（logo + breadcrumb + ⌘K + status pill + avatar）
- `blocks/display/acme/saas-metric-grid` · KPI 网格 4 列
- `blocks/display/acme/saas-data-table` · 行高 40px 紧凑表格
- `blocks/feedback/acme/saas-status-banner` · 32px 三态告警条

### Components · 4 条
- `components/buttons/acme/ghost-button` · 次要 CTA / 取消 / 探索
- `components/buttons/acme/cyan-cta` · 主 CTA（cyan-400 实色填充）
- `components/inputs/acme/mono-input` · 数字 / 阈值 / 端口字段
- `components/indicators/acme/status-pulse` · 四态状态点（healthy 独享呼吸光晕）

### Tokens
- `tokens/palettes/acme/slate-cyan-ice` · 配色
- `tokens/typography/pairs/acme/ibm-plex-duo` · 字体
- `tokens/motion/acme/instant-snap` · 动效（通过 style.uses 引入）
