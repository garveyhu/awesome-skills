---
id: styles/saas-tool/sage-multitheme-data-platform
type: style
name: 多主题切换工作台
description: 12 主题色用户切换 + 9 阶手调灰阶 + 单字体 Inter + 一处装饰彩蛋的 SaaS 工具型整套设计语言
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm, confident, dreamy]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/sage/twelve-theme-spectrum
  - tokens/palettes/sage/neutral-rgb-ladder
  - tokens/typography/pairs/sage/inter-stack
  - tokens/motion/sage/animate-in-suite
  - tokens/motion/sage/styled-keyframes
  - components/buttons/sage/theme-bg-cta
  - components/buttons/sage/icon-circle-ghost
  - components/buttons/sage/stop-pulse-button
  - components/inputs/sage/glow-border-textarea
  - components/inputs/sage/icon-prefix-input
  - components/avatars-icons/sage/themed-circle-avatar
  - components/indicators/sage/crystal-progress-bar
  - components/indicators/sage/hairline-scrollbar
  - blocks/nav/sage/themed-sidebar-shell
  - blocks/nav/sage/sidebar-session-row
  - blocks/nav/sage/space-switcher-dropdown
  - blocks/nav/sage/revolver-menu-fab
  - blocks/nav/sage/command-palette
  - blocks/layout/sage/management-layout-header
  - blocks/layout/sage/sidebar-detail-split
  - blocks/feedback/sage/spin-fullscreen-loader
  - blocks/feedback/sage/delete-confirm-modal
  - blocks/feedback/sage/admin-overlay-modal
  - blocks/marketing/sage/auth-emerald-card
  - blocks/form/sage/chat-composer
  - blocks/display/sage/datasource-card
  - pages/auth/sage/login-emerald-card
  - pages/dashboard/sage/agent-chat-stream
  - pages/list-table/sage/datasource-grid
  - pages/form-flow/sage/rule-set-stepper-modal
  - pages/list-table/sage/agent-store-split-tabs
  - pages/list-table/sage/space-management-split
  - pages/list-table/sage/admin-table-management
  - pages/dashboard/sage/analytics-feedback
  - pages/dashboard/sage/analytics-usage
  - pages/empty-error/sage/crt-tv-404
preview: /preview/styles/saas-tool/sage-multitheme-data-platform
---

# Sage Multi-Theme Data Platform

> 多智能体数据问答平台的整套视觉语言——**12 主题色用户切换 + 9 阶手调 RGB 灰阶 + 单 Inter 字体 + tailwindcss-animate 动效套件 + 雪人飘雪 FAB 彩蛋 + 复古 CRT 404**。给"严肃数据分析"加了一点"愿意陪你玩"的体温。

## 设计哲学

### ① 主题色是"我的工具"（不是"品牌"）
sage 没有"品牌色"——12 个主题色（blue / green / yellow / pink / orange / gray / purple / red / indigo / teal / cyan / rose）由用户在自己的菜单选择，整站每一处带颜色的元素（CTA / 主按钮 / focus ring / 图标 / 进度条 / 选中态）都通过 `THEME_CLASSES[themeColor]` 动态查表着色——出现 119 处。这是 sage 视觉系统的根原语：**用户用自己喜欢的颜色工作**。

### ② 灰阶要细到能感觉到状态变化
9 阶手调 RGB（`rgb(231,231,231)` → `rgb(252,252,252)`）填补 Tailwind slate-50 与 slate-100 之间的空隙，让侧栏 idle / hover / selected / deep-hover 四档微差都能看出来但不刺眼。**两阶之间只差 2-3 个点位**。

### ③ 单字体不分场景
只用 Inter（本地化避开 Google Fonts），不分"sans + mono"。CJK 由系统 fallback 接管。整站气质统一，不在代码块跟正文切字体。

### ④ 弹层入场快、装饰性慢
弹层 `animate-in fade-in zoom-in-95 100ms`（菜单）/ `300ms slide-in-from-bottom-4`（用户菜单从底部升起）；装饰性动画用 styled-components keyframes（`bling 1s` / `earthSpin 8s` / `snowFall 4-12s` / `wobble 0.6s` / `shimmer 1.5s` / `pulse 2s` / `stripes 1s`）。**前者瞬间，后者氛围**。

### ⑤ 严肃 + 一处彩蛋
chat / 仪表盘 / 表格 / 表单 全部克制极简；但 RevolverMenu（雪人飘雪 FAB · 屏幕右下）和 NotFound（复古橘色 CRT 电视机）是两个"开发者性格出口"——告诉用户"我们不是冷冰冰的工具"。

### ⑥ AntD + Tailwind 混搭
重型组件（Table / Form / Select / Modal / Transfer / Dropdown）用 AntD 6，**外面包 ConfigProvider 注入主题色 token**；轻量 UI（按钮 / 卡片 / 侧栏 / 输入区）用 Tailwind v4 + lucide-react 自己写。**用户的输入框走自定义霓虹光晕，提交按钮 antd type="primary"**——两套体系明确分工。

## 整站气质

- **aesthetic**：minimal（信息密度优先 + 不使用装饰元素，除两处彩蛋）
- **mood**：calm（基调）/ confident（管理后台）/ dreamy（彩蛋区）
- **density**：中等偏紧（text-sm 主、行高 1.5、padding 8-12）
- **rhythm**：1px 极淡分割线（slate-100/200）替代阴影做切割；卡片靠 `rounded-xl/2xl/3xl` 软圆角差异分层

## Token 三件套

- 调色板 1：`tokens/palettes/sage/twelve-theme-spectrum` · 12 主题色
- 调色板 2：`tokens/palettes/sage/neutral-rgb-ladder` · 9 阶灰阶 + slate
- 字体：`tokens/typography/pairs/sage/inter-stack` · Inter 单栈
- 动效 1：`tokens/motion/sage/animate-in-suite` · tailwindcss-animate
- 动效 2：`tokens/motion/sage/styled-keyframes` · 7 段彩蛋 keyframes

## 组件 8 件（详见 components/buttons/sage/* + inputs/* + avatars-icons/* + indicators/*）

主题色 CTA / 透明圆形 ghost / 停止脉冲 / 霓虹 textarea / 图标前缀 input / 主题头像 / 玻璃进度条 / 极细滚动条

## Block 13 件（详见 blocks/nav/* + layout/* + feedback/* + marketing/* + form/* + display/*）

主侧栏 / 会话项 / 空间切换 / 雪人 FAB / 命令面板 / 管理 header / 侧栏分屏 / Loading / 删除确认 / Admin overlay / 登录卡 / Chat 输入腰带 / 数据源卡

## Page 10 类（详见 pages/auth/* + dashboard/* + list-table/* + form-flow/* + empty-error/*）

登录 / Chat / 数据源网格 / 规则集 stepper modal / Agent Store / Space 管理 / Admin 表管理 / 反馈分析 / 用量分析 / CRT 404

## 适用场景

- AI 应用 / 数据问答平台
- 多空间 / 多租户 SaaS
- 需要给用户"个性化感"的工具型产品
- 不想要 Linear 的冷峻、不想要 Notion 的圆润、要"有温度的工具"

## 反模式

- ❌ 把 12 主题色当作"必须支持"——sage 选这套是因为多空间多用户场景；单租户产品收敛到 3-4 色更合理
- ❌ 跳过雪人 / CRT 彩蛋——这两处是 sage 的灵魂，去掉后整套语言会变冷
- ❌ 添加第三套字体（mono / display）——Inter 已经撑起来了
