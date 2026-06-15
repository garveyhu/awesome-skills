---
id: components/tags-badges/waveflow/code-status-badge
type: component
name: 执行码状态徽章
description: jobLog 状态徽章 (200 成功 / 0 进行中 / 500 / null) - 浅底 + 深字 + border + px-1.5 紧凑 chip
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [serious]
  stack: [shadcn-radix]
uses: []
preview: /preview/components/tags-badges/waveflow/code-status-badge
---

# Waveflow Code Status Badge

> 日志列表 / 任务集详情列里"成功 / 进行中 / 失败 / 未运行"4 态徽章——和 GlueTypeBadge light 变体同结构，但配色按**执行码**映射（200=emerald / 0=blue / 500+=red / null=stone）。

## 视觉特征

- **基础类**：`inline-flex items-center rounded border px-1.5 py-0.5 text-[11px] font-medium`
- **4 态配色**：
  - **200 成功**：`border-emerald-300 bg-emerald-50 text-emerald-700`
  - **0 进行中**：`border-blue-300 bg-blue-50 text-blue-700`
  - **500 (及其他非 200) 失败**：`border-red-300 bg-red-50 text-red-700`
  - **null/undefined ——**：`border-stone-300 bg-stone-50 text-stone-500`
- font-size 11px 比 GlueType (10.5px) 略大半档——日志列里它就是核心信息

## 核心代码

```tsx
const codeBadge = (code: number) => {
  if (code === 200) return { label: '成功', cls: 'border-emerald-300 bg-emerald-50 text-emerald-700' };
  if (code === 0)   return { label: '进行中', cls: 'border-blue-300 bg-blue-50 text-blue-700' };
  if (code == null) return { label: '—', cls: 'border-stone-300 bg-stone-50 text-stone-500' };
  return { label: '失败', cls: 'border-red-300 bg-red-50 text-red-700' };
};

const CodeBadge: React.FC<{ code: number }> = ({ code }) => {
  const s = codeBadge(code);
  return (
    <span className={cn('inline-flex items-center rounded border px-1.5 py-0.5 text-[11px] font-medium', s.cls)}>
      {s.label}
    </span>
  );
};
```

## 适配指南

- 用法：`<CodeBadge code={record.handleCode} />`——把后端 code 直接喂
- 4 个色不能改——这是 waveflow 状态语言：emerald=好 / blue=进行 / red=坏 / stone=无
- 不要把"成功/失败"渲染成 emoji ✓ ✗ —— 失去 chip 形态

## 反模式

- ❌ 用 GlueTypeBadge solid——会和类型 chip 重复抢视
- ❌ "进行中" 用 amber——和"warning"语义混
- ❌ null 显示空字符串——一行被压扁，留 `—` 保高度
