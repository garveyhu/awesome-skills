---
id: blocks/feedback/sage/delete-confirm-modal
type: block
name: 删除确认弹窗
description: rounded-3xl + AlertTriangle 红圆 icon + slate 暗背 + 双按钮（取消/删除）
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm, serious]
  stack: [react-antd-tailwind]
uses: []
preview: /preview/blocks/feedback/sage/delete-confirm-modal
---

# Delete Confirm Modal

> sage 不用 antd Modal.confirm，自己写一个轻量的删除确认——`rounded-3xl shadow-2xl` 大圆角 + 顶部 12×12 圆形红色 AlertTriangle icon + 短文案 + 灰红双按钮。背景 `slate-900/10 backdrop-blur-[2px]` 极淡蒙层，几乎透明。

## 视觉特征

- 蒙层：`fixed inset-0 z-[60] flex items-center justify-center bg-slate-900/10 backdrop-blur-[2px] animate-in fade-in duration-200`
- 卡片：`bg-white rounded-3xl shadow-2xl p-6 w-full max-w-sm mx-4 transform transition-all scale-100 border border-white/50`
- 顶部 icon：`w-12 h-12 rounded-full bg-red-50 flex items-center justify-center mb-4` + `<AlertTriangle className="text-red-500" size={24} />`
- 标题：`text-lg font-semibold text-slate-900 mb-2`
- 描述：`text-sm text-slate-500 mb-6`
- 按钮组：`flex gap-3 w-full`
- 取消：`flex-1 px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg font-medium transition-colors`
- 删除：`flex-1 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium transition-colors`
- 居中：内容用 `flex flex-col items-center text-center`

## 核心代码

```tsx
import { AlertTriangle } from 'lucide-react';

{deleteConfirmation.isOpen && (
  <div className="fixed inset-0 z-[60] flex items-center justify-center bg-slate-900/10 backdrop-blur-[2px] animate-in fade-in duration-200">
    <div className="bg-white rounded-3xl shadow-2xl p-6 w-full max-w-sm mx-4 transform transition-all scale-100 border border-white/50">
      <div className="flex flex-col items-center text-center">
        <div className="w-12 h-12 rounded-full bg-red-50 flex items-center justify-center mb-4">
          <AlertTriangle className="text-red-500" size={24} />
        </div>
        <h3 className="text-lg font-semibold text-slate-900 mb-2">删除会话？</h3>
        <p className="text-sm text-slate-500 mb-6">此操作无法撤销，对话历史将被永久删除。</p>
        <div className="flex gap-3 w-full">
          <button
            onClick={cancel}
            className="flex-1 px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg font-medium transition-colors"
          >取消</button>
          <button
            onClick={confirm}
            className="flex-1 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium transition-colors"
          >删除</button>
        </div>
      </div>
    </div>
  </div>
)}
```

## 视觉要点

1. **rounded-3xl (24px)** 比常规 modal rounded-2xl/lg 更圆 —— 让"危险操作"看起来温和
2. icon 容器 `bg-red-50` 是 50 阶最浅红，icon `text-red-500` 是 500 阶——双层红色不刺眼
3. 蒙层 `slate-900/10` 只有 10% 不透明 + `backdrop-blur-[2px]` 几乎只有"微微脏"的效果，比 Antd 默认 mask 轻得多
4. **删除按钮固定 red-600**，**永远不走 themeColor**——危险操作不能跟主题"商量"

## 适配指南

- 用受控 isOpen state，外部触发时传具体目标 id
- 关闭后状态：`{ isOpen: false, sessionId: null }`，不要保留 id（防止重复触发）
- 内层不监听 click outside —— 只能通过取消按钮关闭，避免误关

## 反模式

- ❌ 直接用 `<Modal.confirm>` —— 视觉跟 sage 整站对不上（antd 默认风格太冷）
- ❌ 删除按钮用主题色 —— 用户会理解成"主操作"，反而误删
