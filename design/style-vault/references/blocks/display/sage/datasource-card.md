---
id: blocks/display/sage/datasource-card
type: block
name: 数据源卡片
description: 数据库 logo + 名称 + 默认 tag + hover 操作 + 表数信息，sage 数据源 list 唯一卡片形态
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/sage/twelve-theme-spectrum
preview: /preview/blocks/display/sage/datasource-card
---

# Datasource Card

> sage 数据源 list 用 4 列网格，每个卡片的结构：① 顶行（数据库 logo + 名称 + 默认 tag + hover 操作组）② 描述（line-clamp-2）③ 底栏（表数信息 + 同步状态，hover 跳到表管理）。视觉特别处：操作按钮 hover 时整组从 opacity 0 → 1 浮现，类似 Notion table action。

## 视觉特征

- 卡片：`bg-white rounded-xl border border-slate-200 p-5 cursor-pointer transition-all duration-200 hover:shadow-lg hover:border-slate-300`
- grid container：`grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5`
- 顶行：`flex items-center gap-3`
  - logo：`width: 36, height: 36, objectFit: contain, flexShrink: 0`，`onError` fallback 到 mysql icon
  - 名称区：`flex-1 min-w-0` + `font-semibold text-slate-800 truncate`
  - 默认 tag（仅当 isDefault）：`shrink-0 inline-flex items-center gap-0.5 rounded-full bg-green-50 px-1.5 py-0.5 text-[10px] font-medium text-green-700 ring-1 ring-green-200` + `<CheckCircleFilled style={{ fontSize: 10 }} />` + "默认"
  - 类型副标题：`text-xs text-slate-500 uppercase`（如 MYSQL / POSTGRESQL）
  - 操作组：`flex gap-1 transition-opacity duration-200 mb-5` + inline `style={{ opacity: hover ? 1 : 0 }}` 控制
  - 操作按钮：antd `<Button type="text" size="small" icon={...} style={{ color: '#64748b' }} />` ; 其中 hover delete 按钮加 `className="hover:!text-red-500"`
- 描述：`mt-3 text-sm text-slate-600 line-clamp-2 min-h-[40px]`
- 底栏：`mt-4 pt-3 border-t border-slate-100 flex items-center gap-2 text-sm text-slate-500 hover:text-slate-700 transition-colors`
- 默认 tag 中"⭐ 设为默认 / 取消默认"toggle：图标 `<StarOutlined />`；`color: isDefault ? primaryColor : '#64748b'`

## 核心代码

```tsx
<div
  className="bg-white rounded-xl border border-slate-200 p-5 cursor-pointer transition-all duration-200 hover:shadow-lg hover:border-slate-300"
  onMouseEnter={() => setHover(item.id)}
  onMouseLeave={() => setHover(null)}
  onClick={() => navigate(`/datasource/${item.id}`)}
>
  <div className="flex items-center gap-3">
    <img src={getIconByType(item.type)} style={{ width: 36, height: 36, objectFit: 'contain', flexShrink: 0 }} />
    <div className="flex-1 min-w-0">
      <div className="flex items-center gap-1.5">
        <div className="font-semibold text-slate-800 truncate">{item.name}</div>
        {isDefault && (
          <span className="shrink-0 inline-flex items-center gap-0.5 rounded-full bg-green-50 px-1.5 py-0.5 text-[10px] font-medium text-green-700 ring-1 ring-green-200">
            <CheckCircleFilled style={{ fontSize: 10 }} /> 默认
          </span>
        )}
      </div>
      <div className="text-xs text-slate-500 uppercase">{item.type}</div>
    </div>
    <div className="flex gap-1 transition-opacity duration-200 mb-5" style={{ opacity: hover === item.id ? 1 : 0 }}>
      <Tooltip title="设为默认"><Button type="text" size="small" icon={<StarOutlined />} style={{ color: isDefault ? primary : '#64748b' }} /></Tooltip>
      <Tooltip title="快捷提问"><Button type="text" size="small" icon={<MessageOutlined />} style={{ color: '#64748b' }} /></Tooltip>
      <Tooltip title="编辑"><Button type="text" size="small" icon={<EditOutlined />} style={{ color: '#64748b' }} /></Tooltip>
      <Tooltip title="删除"><Button type="text" size="small" icon={<DeleteOutlined />} style={{ color: '#64748b' }} className="hover:!text-red-500" /></Tooltip>
    </div>
  </div>

  <div className="mt-3 text-sm text-slate-600 line-clamp-2 min-h-[40px]">
    {item.description || '无描述'}
  </div>

  <div className="mt-4 pt-3 border-t border-slate-100 flex items-center gap-2 text-sm text-slate-500 hover:text-slate-700 transition-colors" onClick={e => { e.stopPropagation(); navigate(`/datasource/${item.id}/tables`); }}>
    <TableOutlined />
    <span>已同步 {syncedCount} / 共 {totalCount} 表</span>
  </div>
</div>
```

## 视觉要点

1. logo 用 36×36 真实数据库图标（mysql / postgresql / oracle / dameng / clickhouse / doris / starrocks / es / redshift / excel ...）—— sage 内置 12 种数据库 logo
2. 默认 tag 用 emerald 50/700/200 三阶 + `[10px]` 极小字号——是"角标"非"主标"
3. 操作按钮 mb-5 而不是 0 —— 让按钮稍微往上"浮起"，避免遮住名称 truncate 的省略号
4. 底栏 `border-t` 分隔器只 1px slate-100 —— sage 风格"硬不起眼但确实存在"
5. 描述 `min-h-[40px]` 占位，避免不同卡片高度不齐

## 适配指南

- isDefault 通过 `spaceCoreConfig?.defaultDataSourceId === item.id` 判断
- 类型 fallback：未知类型 logo 用 mysql 图，因为 mysql 是最通用感
- 操作按钮 stopPropagation —— 否则会冒泡到卡片 onClick 进详情

## 反模式

- ❌ 默认 tag 用主题色 —— 主题色和"是否默认"无关；用 emerald 强语义
- ❌ hover 时显示完整描述 —— sage 让用户"点进详情看"，hover 只浮按钮
