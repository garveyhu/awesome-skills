---
id: blocks/feedback/waveflow/log-pre-viewer
type: block
name: pre 日志查看器
description: header (13px 标题 + #N mono + RefreshCw 按钮 spinning) + h-calc(100vh-180px) overflow-auto bg-stone-50 + pre font-mono 11.5px stone-700 日志正文
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, industrial]
  mood: [serious]
  stack: [shadcn-radix]
uses: []
preview: /preview/blocks/feedback/waveflow/log-pre-viewer
---

# Waveflow Log Pre Viewer

> 任务日志详情页 (`/data/log`) 的 pre 显示器——整体外框走 admin section（rounded-xl border paper shadow-soft），内部：**header bar**（13px 标题 "日志详情" + 小灰 `#logId` mono + RefreshCw 刷新按钮 + 可 spin）+ **scroll 容器**（`h-[calc(100vh-180px)] overflow-auto bg-stone-50 px-3 py-2` 浅灰底）+ **pre 内容**（`whitespace-pre-wrap break-words font-mono text-[11.5px] leading-relaxed text-stone-700`）。

## 视觉特征

```tsx
<section className="overflow-hidden rounded-xl border border-stone-200/40 bg-[var(--color-paper)] shadow-[var(--shadow-soft)]">
  <header className="flex items-center justify-between border-b border-stone-100 bg-[var(--color-warm-2)]/40 px-4 py-2.5">
    <div className="text-[13px] font-semibold text-stone-800">
      日志详情
      {logId ? <span className="ml-2 font-mono text-[11.5px] text-stone-500">#{logId}</span> : null}
    </div>
    <Button variant="primary" size="sm" onClick={loadLog} disabled={loading}>
      <RefreshCw className={cn('h-3.5 w-3.5', loading && 'animate-spin')} /> 刷新日志
    </Button>
  </header>

  <div className="h-[calc(100vh-180px)] overflow-auto bg-stone-50 px-3 py-2">
    {loading && !logContent ? (
      <div className="flex h-full items-center justify-center text-stone-400">
        <Loader2 className="h-4 w-4 animate-spin" />
      </div>
    ) : (
      <pre className="m-0 whitespace-pre-wrap break-words font-mono text-[11.5px] leading-relaxed text-stone-700">
        {logContent || '暂无日志内容'}
      </pre>
    )}
  </div>
</section>
```

## 视觉特征

- **header 用 warm-2/40 底**：和主区 stone-50 浅灰底形成"卡片头 vs 内容"分层
- **#logId mono**：用 `font-mono text-[11.5px] text-stone-500` —— ID 是辅助信息
- **RefreshCw 在 loading 时 spin**：用 `cn('h-3.5 w-3.5', loading && 'animate-spin')` 双语句
- **pre `whitespace-pre-wrap`**：保留换行 + 自动换行长行——避免横滚
- **pre `font-mono leading-relaxed`**：mono + 1.625 行高——适合日志阅读
- **空态 "暂无日志内容"**：直接在 pre 内显示
- **loading 态**：spin Loader2 居中

## 适配指南

- 高度计算 `h-[calc(100vh-180px)]` —— 180 = topbar 48 + page padding 16+16 + section header ~48 + 余量
- 长日志（> 50KB）建议虚拟滚动——但 waveflow 不做（admin 场景日志通常 < 10KB）
- 复制按钮：右上 RefreshCw 旁加 Copy 按钮，调 `navigator.clipboard.writeText(logContent)`
- 不染色 / 不 syntax highlight—— 保持工程师裸文本视感

## 反模式

- ❌ 用 ansi-to-html 染色—— 服务器日志格式不稳定，染色出错难看
- ❌ pre 用 white bg—— 失去"日志窗"的灰底沉浸
- ❌ header 没 #logId—— 用户从多个 tab 打开多个日志时分不清
