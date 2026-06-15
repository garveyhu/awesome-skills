---
id: blocks/form/chameleon/json-schema-dynamic-form
type: block
name: JSON Schema 动态表单引擎
description: 把后端 Pydantic JSON Schema 渲染成受控 React 表单——SchemaField 按 type 派发到 6 个 widget(string/number/boolean/enum/object/array)，object/array 递归，嵌套对象浅卡片层级，array add/remove，不支持类型 amber fallback
platforms:
- web
theme: light
tags:
  aesthetic:
  - industrial
  - minimal
  mood:
  - calm
  - serious
  stack:
  - shadcn-radix
uses:
- components/inputs/waveflow/blue-focus-input
- components/toggles/waveflow/emerald-switch
- tokens/palettes/waveflow/warm-paper-ink-blue
preview: /preview/blocks/form/chameleon/json-schema-dynamic-form
---

# JSON Schema 动态表单引擎

> Chameleon 的 `JSONSchemaForm`（`core/components/form/json-schema-form.tsx` + `schema-field.tsx` + `widgets/*`）——把后端 Pydantic JSON Schema 渲染成受控 React 表单。`SchemaField` 按 type 派发到 6 个 widget（string / number / boolean / enum / object / array），object 与 array 递归回 `SchemaField`，支持 Optional anyOf 解包、嵌套对象浅卡片层级、array add / remove、format 路由（textarea / password / email / url）、`enumNames` 自定义显示名。waveflow 无对应——Chameleon 独有的 schema-driven 表单引擎。

## 视觉特征

- **顶层容器**：空 schema → `div rounded-md border border-stone-200/70 bg-stone-50/30 px-3 py-2 text-[12px] text-stone-500`「Schema 内没有字段定义。」；否则顶层 object 直接 `ObjectWidget` 展开 properties，外层 className 默认 `space-y-3`（12px）
- **SchemaField 布局**：boolean 类 label 与 widget **同行**（`flex items-center justify-between gap-3 py-1`），其他在 widget 之上（`space-y-1`）
  - **Label**：`text-[12.5px] text-stone-700`（#44403c），required `span.ml-0.5 text-rose-500` 星号
  - **description**：非 boolean 同行 `span.text-[11px] text-stone-400` 前缀「· 」；boolean 下方 `div.text-[11px] text-stone-400`
  - **error**：`div.text-[11px] text-rose-500`
  - **不支持类型 fallback**：`div rounded border border-amber-200 bg-amber-50/40 px-2 py-1 text-[11px] text-amber-700`
- **ObjectWidget**：depth0 `space-y-3`；depth≥1 浅卡片 `space-y-3 rounded-md border border-stone-200/70 bg-stone-50/40 p-3`（12px）；空字段 `div.text-[11px] italic text-stone-400`「（此对象无字段定义）」
- **ArrayWidget**：`space-y-2`，每项 `flex items-start gap-2 rounded-md border border-stone-200/70 bg-paper p-2`，删除按钮 `mt-0.5 rounded p-1 text-stone-400 hover:bg-stone-100 hover:text-rose-600` 内 `Trash2 h-3.5 w-3.5`；底部 `Button variant="outline" size="sm"` + `Plus h-3.5 w-3.5`「添加一项」
- **string widget**：format=textarea → `Textarea rows={3}`；否则 `Input`（password / email / url 走对应 htmlType）
- **number widget**：`Input type="number"`，step 整数 1 / 浮点 'any'
- **boolean widget**：`Switch`
- **enum widget**：`Select`，placeholder「选择…」，支持 `enumNames` 按 index 映射显示名
- **lucide**：`Plus` / `Trash2`；复用 ui：Input / Textarea / Select / Switch / Label / Button

## 核心代码

```tsx
// SchemaField 派发 + label/desc/error 包装
const labelInline = kind === 'boolean';
<div className={labelInline ? 'flex items-center justify-between gap-3 py-1' : 'space-y-1'}>
  <div className={labelInline ? 'space-y-0.5' : 'flex items-baseline gap-1.5'}>
    <Label className="text-[12.5px] text-stone-700">
      {title}{required && <span className="ml-0.5 text-rose-500">*</span>}
    </Label>
    {description && !labelInline && <span className="text-[11px] text-stone-400">· {description}</span>}
  </div>
  <div className={labelInline ? 'shrink-0' : ''}>{widget}</div>
  {error && <div className="text-[11px] text-rose-500">{error}</div>}
</div>

// ObjectWidget depth>=1 浅卡片
const containerCls = depth === 0
  ? 'space-y-3'
  : 'space-y-3 rounded-md border border-stone-200/70 bg-stone-50/40 p-3';

// ArrayWidget item + remove
<div className="flex items-start gap-2 rounded-md border border-stone-200/70 bg-paper p-2">
  <div className="flex-1"><SchemaField .../></div>
  <button className="mt-0.5 rounded p-1 text-stone-400 transition hover:bg-stone-100 hover:text-rose-600">
    <Trash2 className="h-3.5 w-3.5" />
  </button>
</div>
<Button variant="outline" size="sm" onClick={add}><Plus className="h-3.5 w-3.5" /> 添加一项</Button>

// 不支持类型 fallback
<div className="rounded border border-amber-200 bg-amber-50/40 px-2 py-1 text-[11px] text-amber-700">
  不支持的 schema 类型：{props.schema.type || '(unknown)'}
</div>
```

## 适配指南

- 受控：外部传 `value + onChange`，组件不持有 form state；后端 Pydantic 是 truth source，前端只做 UX 级提示
- 空串与 undefined 区分：string widget 空串 → undefined，让上层决定是否走默认值；object 剔除 undefined 子键
- 嵌套对象用 depth 控制浅卡片层级——depth0 平铺、depth≥1 套 `stone-50/40` 浅卡片做视觉分组
- array item 用 index 当 key（无 id），add 推 undefined 占位让 widget 内部显示空态
- enum 的 `enumNames` 必须与 `enum` 等长才生效，否则裸显 value

## 反模式

- ❌ 嵌套对象不分层级——depth≥1 必套浅卡片，否则深层字段视觉糊成一团
- ❌ boolean 也把 label 放上方——Switch 类天然横向，label 与控件同行才省纵向空间
- ❌ 不支持类型静默丢弃——必须 amber fallback 显式提示「schema 类型不支持」
- ❌ 组件内自持 form state——必须受控，让后端 schema + 父级 value 为单一真相源
