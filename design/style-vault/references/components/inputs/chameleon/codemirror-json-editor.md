---
id: components/inputs/chameleon/codemirror-json-editor
type: component
name: CodeMirror JSON 编辑器
description: 透明底嵌入式 CodeMirror 6（语法高亮 + 实时校验 + 一键格式化）+ 顶栏标签/格式化按钮 + rose 错误条
platforms:
- web
theme: light
tags:
  aesthetic:
  - industrial
  - minimal
  mood:
  - serious
  stack:
  - shadcn-radix
preview: /preview/components/inputs/chameleon/codemirror-json-editor
---

# Chameleon CodeMirror JSON 编辑器

> 专业 JSON 编辑器（CodeMirror 6 + `@codemirror/lang-json`）：语法高亮 + 实时校验 + 一键格式化 + 底部 rose 错误条 + 顶部标签栏（label + 格式化按钮）+ 行号/折叠槽。编辑器主题刻意透明底嵌入外框，外框统一 `rounded-md border border-stone-200`。评测样本「输入 / 预期输出」、节点配置等重型 JSON 编辑场景用（只读表格展示仍用 json-cell）。

## 视觉特征

- **外框**：`overflow-hidden rounded-md(6px) border border-stone-200`
- **顶栏**：`flex items-center justify-between border-b border-stone-100 bg-stone-50/80 px-2(8px) py-1(4px)`
  - label：`text-[10.5px] font-medium text-stone-500`（默认 `'JSON'`）
  - 格式化按钮：`text-[10.5px] text-stone-500 hover:text-stone-800`（readOnly 时不渲染）
- **CodeMirror editorTheme**：
  - `& { fontSize: 12px; backgroundColor: transparent }`
  - `.cm-content { fontFamily: ui-monospace, SFMono-Regular, Menlo, monospace }`
  - `.cm-gutters { backgroundColor: transparent; border: none }`
  - `&.cm-focused { outline: none }`
  - `minHeight: 110px`，`maxHeight: 320px`
  - basicSetup：`lineNumbers, foldGutter, autocompletion:false`；`wrap` 时加 `EditorView.lineWrapping`
- **错误条**：`border-t border-rose-100 bg-rose-50 px-2 py-1 text-[10.5px] text-rose-600`，显 `⚠ JSON 语法错误：{error}`（实时 `JSON.parse` 失败时）

## 核心代码

```tsx
const editorTheme = EditorView.theme({
  '&': { fontSize: '12px', backgroundColor: 'transparent' },
  '.cm-content': { fontFamily: 'ui-monospace, SFMono-Regular, Menlo, monospace' },
  '.cm-gutters': { backgroundColor: 'transparent', border: 'none' },
  '&.cm-focused': { outline: 'none' },
});

const handleChange = (v: string) => {
  onChange(v);
  if (!v.trim()) return setError(null);
  try { JSON.parse(v); setError(null); } catch (e) { setError((e as Error).message); }
};

<div className="overflow-hidden rounded-md border border-stone-200">
  <div className="flex items-center justify-between border-b border-stone-100 bg-stone-50/80 px-2 py-1">
    <span className="text-[10.5px] font-medium text-stone-500">{label ?? 'JSON'}</span>
    {!readOnly && <button onClick={format} className="text-[10.5px] text-stone-500 hover:text-stone-800">格式化</button>}
  </div>
  <CodeMirror value={value} onChange={handleChange} editable={!readOnly} extensions={extensions}
    minHeight="110px" maxHeight="320px"
    basicSetup={{ lineNumbers:true, foldGutter:true, autocompletion:false }} />
  {error && <div className="border-t border-rose-100 bg-rose-50 px-2 py-1 text-[10.5px] text-rose-600">⚠ JSON 语法错误：{error}</div>}
</div>
```

## 适配指南

- label 传场景名（「输入」「预期输出」「参数」），不要全留默认 'JSON'——多个编辑器并排时分不清
- 格式化按钮做兜底：用户粘贴压缩 JSON 后一键展开成 2 空格缩进
- 错误条用 rose（不是站点主红）——温和提示而非阻断，用户改对即消失
- 只读展示（表格行内）用 json-cell 不用本组件——CodeMirror 重，列表里 N 个实例会卡
- 长文本只读用 `wrap` 加 `lineWrapping`，避免横向滚动看不全

## 反模式

- ❌ 列表 / 表格行内嵌大量本组件——CodeMirror 是重型件，多实例拖慢页面
- ❌ 关掉行号 / 折叠槽——JSON 多行编辑没行号定位困难
- ❌ 错误条用站点主红 `red-600`——会显得像致命错误，rose 更贴「语法提示」语义
- ❌ 编辑器给实底色——刻意透明底融入外框，给底色会和顶栏 stone-50 割裂
