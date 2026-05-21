---
id: pages/detail/waveflow/log-viewer-pre
type: page
name: 任务日志详情（pre viewer 全屏）
description: 独立无 Layout 路由 /data/log - URL query 携带 executor/triggerTime/id - 简单 section 套 log-pre-viewer block - h-calc(100vh-180px) 高显示
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, industrial]
  mood: [serious]
  stack: [shadcn-radix]
uses:
  - blocks/feedback/waveflow/log-pre-viewer
preview: /preview/pages/detail/waveflow/log-viewer-pre
---

# Waveflow Log Viewer Pre Page

> waveflow 任务日志独立详情页 (`/data/log`)——**不嵌 Layout**（route 列表里在 Layout 外平铺），让用户从其它页 `window.open(href, '_blank')` 新窗口直接看大 log。**整页 `h-full px-6 py-4`** + 一个独立 section 套 `log-pre-viewer` block（refresh header + pre 内容区）。从 URL 取 `executorAddress / triggerTime / id / fromLineNum` 参数 fetch 日志内容。

## 页面骨架

```tsx
const JobLogDetail: React.FC = () => {
  const query = new URLSearchParams(location.search);
  const executorAddress = query.get('executorAddress') || '';
  const triggerTime = Number(query.get('triggerTime')) || 0;
  const logId = Number(query.get('id')) || 0;
  const fromLineNum = Number(query.get('fromLineNum')) || 1;

  const [logContent, setLogContent] = useState('');
  const [loading, setLoading] = useState(false);

  const loadLog = async () => {
    setLoading(true);
    try {
      const res = await jobLogService.viewJobLog(executorAddress, triggerTime, logId, fromLineNum);
      if (res.success && res.data?.logContent !== '\n') {
        setLogContent(res.data.logContent);
      }
    } catch (e) { toast.error('获取日志失败') }
    finally { setLoading(false) }
  };

  useEffect(() => { loadLog() }, []);

  return (
    <div className="h-full px-6 py-4">
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
            <div className="flex h-full items-center justify-center text-stone-400"><Loader2 className="h-4 w-4 animate-spin" /></div>
          ) : (
            <pre className="m-0 whitespace-pre-wrap break-words font-mono text-[11.5px] leading-relaxed text-stone-700">
              {logContent || '暂无日志内容'}
            </pre>
          )}
        </div>
      </section>
    </div>
  );
};
```

## 视觉要点

1. **route 不嵌 Layout**：让用户新窗口看大 log（没有 sidebar 占空间）
2. **核心高度 calc(100vh-180px)**：180 = page padding + header 高度 + 余量
3. **bg-stone-50 灰底 pre**：让用户视觉切到"日志窗口"模式
4. **`whitespace-pre-wrap`**：保留换行 + 长行自动 wrap（不横滚）
5. **RefreshCw 在 loading 时 spin**：`cn(..., loading && 'animate-spin')` 双语句
6. **#logId 显示在标题**：用户开多个新窗口能区分

## 适配指南

- 跳转方式：从其它页 `window.open(`/data/log?executorAddress=${addr}&triggerTime=${t}&id=${id}&fromLineNum=1`, '_blank')` 拼参数
- 长日志（> 50KB）建议虚拟滚动—— waveflow 当前不做（admin 场景日志通常 < 10KB）
- 增量加载：fromLineNum 让后端支持"上次到哪了"—— waveflow 简单刷新整页

## 反模式

- ❌ 嵌进 Layout—— 失去"独立大窗口"语义
- ❌ pre 用 white bg—— 失去"日志窗"沉浸感
- ❌ 不带 #logId—— 多 tab 时分不清
