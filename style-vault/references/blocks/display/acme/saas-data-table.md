---
id: blocks/display/acme/saas-data-table
type: block
name: SaaS 数据表格
description: 行高 40px 紧凑表格 · status pulse 左 · 等宽数字右对齐 · hover 显 ghost icon-button
platforms: [web]
theme: dark
tags:
  aesthetic: [minimal, industrial]
  mood: [cold, serious]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/acme/slate-cyan-ice
  - tokens/typography/pairs/acme/ibm-plex-duo
  - components/indicators/acme/status-pulse
  - components/buttons/acme/ghost-button
preview: /preview/blocks/display/acme/saas-data-table
---

# SaaS Data Table

> 监控 / 事件 / 服务列表的高密度表格：等宽数字、状态可见、列分明。

## 视觉特征

- 行高 40px（密集）/ 48px（标准）；header 32px
- header `text-[11px] uppercase tracking-wider text-slate-500`，边框 1px slate-800 底
- 行 zebra subtle：偶数行 `bg-slate-900/40`，奇数行透明
- hover 行高亮 `bg-slate-800/50`，并显示尾列的 ghost icon-button 组（详情 / 静音 / 关闭）
- 列对齐：text 列左 / 数字 / 时间戳列右；状态列窄（48px）
- 状态列在最左侧，用 `<StatusPulse />`，size=6（紧凑）
- 数字列必 `font-mono text-right`

**与 blocks/display/skillhub/table 区分**：那条是 Antd 主题化的管理后台表格（浅底 + Antd ConfigProvider 覆盖），用于业务管理页；本条是工业冷感的纯监控表格（暗底 + 自定义 div 实现 / 不依赖 Antd），用于 dashboard / incident。

## 核心代码

```tsx
import { StatusPulse } from '../../components/indicators/acme/status-pulse';

interface Column<T> {
  key: keyof T;
  label: string;
  align?: 'left' | 'right';
  mono?: boolean;
  width?: number;
}

export function SaasDataTable<T extends { id: string }>({
  columns,
  rows,
  density = 'compact',
}: {
  columns: Column<T>[];
  rows: T[];
  density?: 'compact' | 'normal';
}) {
  const rowH = density === 'compact' ? 'h-10' : 'h-12';
  return (
    <div className="font-sans bg-slate-950">
      {/* header */}
      <div
        className="grid bg-slate-900 border-b border-slate-800 text-[11px] uppercase tracking-wider text-slate-500"
        style={{ gridTemplateColumns: gridTemplate(columns) }}
      >
        {columns.map((c) => (
          <div
            key={String(c.key)}
            className={`h-8 px-3 flex items-center ${c.align === 'right' ? 'justify-end' : ''}`}
          >
            {c.label}
          </div>
        ))}
      </div>
      {/* rows */}
      {rows.map((r, i) => (
        <div
          key={r.id}
          className={`grid ${rowH} text-[13px] text-slate-200 hover:bg-slate-800/50 ${
            i % 2 === 1 ? 'bg-slate-900/40' : ''
          }`}
          style={{ gridTemplateColumns: gridTemplate(columns) }}
        >
          {columns.map((c) => (
            <div
              key={String(c.key)}
              className={`px-3 flex items-center ${
                c.align === 'right' ? 'justify-end font-mono' : ''
              } ${c.mono ? 'font-mono' : ''}`}
            >
              {String(r[c.key])}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}

function gridTemplate(cols: Column<any>[]) {
  return cols.map((c) => (c.width ? `${c.width}px` : '1fr')).join(' ');
}
```

## 适配指南

- 状态列固定 48px，名字列 `1fr`，数字列 80-120px 视位数
- 时间戳用 ISO 短格式（`02:14:08`）+ 尾部 UTC 标注；不要 `2 minutes ago` 那种相对时间——服务运维要绝对时间
- 行不加阴影 / 不加圆角；视觉重量靠 1px hairline + zebra
- 高负载场景（>200 行）请套虚拟滚动（react-window），样式不变

## 反模式

- 不要 `bordered={true}` 风格的全 border 网格——破坏冷感
- 不要给行加圆角
- 不要列间用粗 vertical divider —— 1px slate-800 hairline 已足够
- 不要让行高 < 36px——可读性塌
