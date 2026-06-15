---
id: blocks/form/chameleon/generation-panel
type: block
name: 声明式生图参数面板
description: 按后端 param-spec 动态渲染的生图/视频参数面板——首帧上传 + 提示词 + 紫色风格 chip + aspect_ratio 预设 chip 与自定义宽高 + select/toggle/text/seed(骰子)/int/float 字段 + 高级参数折叠
platforms:
- web
theme: light
tags:
  aesthetic:
  - minimal
  - industrial
  mood:
  - calm
  - serious
  stack:
  - shadcn-radix
uses:
- blocks/form/waveflow/dialog-vertical-form
- tokens/palettes/waveflow/warm-paper-ink-blue
preview: /preview/blocks/form/chameleon/generation-panel
---

# 声明式生图参数面板

> Chameleon 的 `GenerationPanel`（`core/components/common/generation-panel.tsx`）——按后端 param-spec 动态渲染生图 / 视频的参数面板。`forwardRef` 暴露 `getRequest()` 拼出 `{ prompt(已并风格), params, input_images }`。模型测试 / Playground / 文生图工作台共用。垂直 `space-y-3` 字段流，signature 是**紫色 chip 预设**（风格 / 比例）与 **虚线首帧上传框**。

## 视觉特征

- **外容器**：`space-y-3`（12px 字段间距），每字段块自身 `space-y-1.5`（label 与控件 6px）
- **chip**（风格 / 比例预设）：`rounded-full border px-2.5 py-1 text-[11.5px] transition`
  - active：`border-violet-500 bg-violet-50 text-violet-700`（#8b5cf6 / #f5f3ff / #6d28d9）
  - idle：`border-stone-200 text-stone-600 hover:border-stone-300`
- **Label**：`text-[12px] text-stone-600`（#57534e）
- **首帧 / 参考图上传**（视频必填 / i2i 可选时显示）：
  - 占位：`flex h-24 w-32 flex-col items-center justify-center gap-1 rounded-md border border-dashed border-stone-300 text-stone-400 transition hover:border-stone-400`（96×128px），内 `ImagePlus h-5 w-5`（上传中换 `Loader2 h-5 w-5 animate-spin`）+ `span.text-[11px]` 文案
  - 已传：`img h-24 w-auto rounded-md border border-stone-200 object-cover` + 右上删除按钮 `absolute -top-2 -right-2 flex h-5 w-5 items-center justify-center rounded-full bg-stone-700 text-white` 内 `X h-3 w-3`
- **提示词 Textarea**：`rows={3}` + `text-[12.5px]`
- **aspect_ratio 自定义宽高**：两个 `Input type="number" className="h-8 text-[12px]"`（高 32px）+ `span.text-stone-400` 的 `×` 分隔 + `span.ml-1 shrink-0 text-[10.5px] text-stone-400` 显示「px（{lo}–{hi}）」
- **select 字段**：SelectTrigger `h-8 text-[12px]`，SelectItem `text-[12px]`
- **toggle 字段**：`label.flex items-center gap-2 text-[12px] text-stone-700` + 原生 checkbox
- **text 字段**：`Textarea rows={2} text-[12px]`
- **seed 字段**：`flex gap-1.5` → `Input type="number" placeholder="随机" h-8 text-[12px]` + 骰子按钮 `flex h-8 w-8 shrink-0 items-center justify-center rounded-md border border-stone-200 text-stone-500 hover:border-stone-300` 内 `Dices h-3.5 w-3.5`
- **int / float 字段**：`Input type="number" h-8 text-[12px]`，step 整数 1 / 浮点 0.1
- **高级折叠**：`border-t border-stone-100 pt-2`，触发按钮 `text-[11.5px] text-stone-500 hover:text-stone-700`，文案 `showAdvanced ? '▾ 收起高级参数' : '▸ 高级参数'`（纯文本三角字形前缀，**无 lucide icon**），展开区 `mt-2 space-y-3`
- **lucide**：`Dices` / `ImagePlus` / `Loader2` / `X`（折叠器不用 icon，纯文本 ▾ / ▸）

## 核心代码

```tsx
const chipCls = (active: boolean) => cn(
  'rounded-full border px-2.5 py-1 text-[11.5px] transition',
  active ? 'border-violet-500 bg-violet-50 text-violet-700'
         : 'border-stone-200 text-stone-600 hover:border-stone-300',
);

// 首帧上传占位
<button className="flex h-24 w-32 flex-col items-center justify-center gap-1 rounded-md border border-dashed border-stone-300 text-stone-400 transition hover:border-stone-400">
  {uploading ? <Loader2 className="h-5 w-5 animate-spin" /> : <ImagePlus className="h-5 w-5" />}
  <span className="text-[11px]">上传首帧图</span>
</button>

// seed 骰子
<div className="flex gap-1.5">
  <Input type="number" placeholder="随机" className="h-8 text-[12px]" />
  <button className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md border border-stone-200 text-stone-500 hover:border-stone-300">
    <Dices className="h-3.5 w-3.5" />
  </button>
</div>

// 高级折叠
<div className="border-t border-stone-100 pt-2">
  <button className="text-[11.5px] text-stone-500 transition hover:text-stone-700">
    {showAdvanced ? '▾ 收起高级参数' : '▸ 高级参数'}
  </button>
  {showAdvanced && <div className="mt-2 space-y-3">{advanced.map(...)}</div>}
</div>
```

## 适配指南

- field 按 `group: 'basic' | 'advanced'` 拆两段——basic 直出、advanced 折叠
- `getRequest()` 把 styleId 对应的 `suffix` 拼到 prompt 尾（`base, suffix`），merged params 剔除空值
- `showImageInput = mediaKind === 'video' || (mediaKind === 'image' && supportsI2i)`——视频首帧必填、图生图参考图可选
- `hidePrompt` 模式（Playground）提示词走聊天框，面板只调参数；受控用 `onChange` 把 `{ params, input_images }` 提升到父级
- 风格 chip 是 violet 系——区别于全站 blue 主色，因为它是「创作 / 多媒体」语义专属

## 反模式

- ❌ 把 advanced 参数也直出——param-spec 设了 group 就该折叠，避免参数表过长
- ❌ chip 用 blue（主色）——violet 是多媒体创作专属的语义色，别混
- ❌ 上传框用实线 border——虚线 + ImagePlus 才是「待上传」的占位语义
- ❌ seed 不给骰子——随机种子是高频操作，必须有一键随机
