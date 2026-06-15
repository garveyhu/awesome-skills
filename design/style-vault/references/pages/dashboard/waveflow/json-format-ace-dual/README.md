---
id: pages/dashboard/waveflow/json-format-ace-dual
type: page
name: 双 ACE Editor JSON 格式化工具
description: 标题 + 双面板镜像 (左输入 ACE + 右只读格式化 ACE) + 错误 footer (red-50 + red-700 错误信息) + 内置 DataX 示例 JSON
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, industrial]
  mood: [serious]
  stack: [shadcn-radix]
uses: []
preview: /preview/pages/dashboard/waveflow/json-format-ace-dual
---

# Waveflow JSON Format ACE Dual

> waveflow 工具页 (`/tool/jsonFormat`)——双 ACE editor 镜像 JSON 格式化工具。**整页 `flex h-full flex-col px-6 py-4`**：上方 16px 标题"JSON 格式化工具" + 下方 `flex flex-1 gap-3 overflow-hidden` 双 Panel 横向铺：**左** Panel "输入 JSON"（可编辑 ACE editor + 解析错误显示 footer red-50/red-700）+ **右** Panel "格式化结果"（readOnly ACE，自动随左输入解析+缩进 2 输出）。

## 页面骨架

```tsx
<div className="flex h-full flex-col px-6 py-4">
  <h2 className="mb-3 text-[16px] font-semibold tracking-tight text-stone-900">JSON 格式化工具</h2>
  <div className="flex flex-1 gap-3 overflow-hidden">
    <Panel title="输入 JSON" footer={error && <ErrorFooter>{error}</ErrorFooter>}>
      <AceEditor mode="json" theme="github" value={originText} onChange={setOriginText} fontSize={13} showGutter highlightActiveLine width="100%" height="100%" />
    </Panel>
    <Panel title="格式化结果">
      <AceEditor mode="json" theme="github" value={formattedValue} fontSize={13} showGutter highlightActiveLine width="100%" height="100%" readOnly />
    </Panel>
  </div>
</div>

// Panel 单卡
const Panel = ({ title, children, footer }) => (
  <div className="flex flex-1 flex-col overflow-hidden rounded-xl border border-stone-200/40 bg-[var(--color-paper)] shadow-[var(--shadow-soft)]">
    <div className="border-b border-stone-100 bg-[var(--color-warm-2)]/40 px-3 py-2 text-[12px] font-medium text-stone-600">{title}</div>
    <div className="relative flex-1">{children}</div>
    {footer}
  </div>
);
```

## 视觉要点

1. **双 Panel 各 50% 宽**：`flex-1 + gap-3` 自动平分
2. **Panel header 用 warm-2/40 底 + 12px font-medium stone-600**：弱化 title 视觉，让 editor 是主体
3. **ACE editor**：mode='json' / theme='github' / fontSize=13 / showLineNumbers + tabSize=2 / useWorker: false（避免独立 worker 加载）
4. **错误 footer**: `border-t border-red-200 bg-red-50 px-3 py-1.5 text-[11.5px] text-red-700` —— 失败时显示
5. **内置示例 JSON**：DataX 实际配置（mysqlreader + mysqlwriter + connection 全套）—— 用户进来就有 useful payload
6. **解析容错**：JSON.parse 失败时保留原文本 + 显错（不清空用户输入）
7. **整页 `overflow-hidden + flex flex-1`**：editor 高度自适应剩余空间

## 适配指南

- 工具类页面（JSON 格式化 / Base64 / URL 编码 等）都可以套用本骨架：双 Panel + 标题 + 工具栏
- ace-builds basePath 配 CDN（waveflow 走 `https://cdn.jsdelivr.net/npm/ace-builds@1.32.6/src-noconflict/`）—— 内网部署需切自托管路径
- 复制按钮可加：在 Panel header 右侧
- 用 react-ace 而非 monaco —— monaco 太大（1MB+），ace 仅 100KB

## 反模式

- ❌ 用 textarea 替 ACE —— 失去 syntax highlight 和行号
- ❌ 错误 footer 用红边 border-2 —— 太重，浅红底 + 深红文已足
- ❌ Panel header 用 dark bg—— 失去暖底气质
