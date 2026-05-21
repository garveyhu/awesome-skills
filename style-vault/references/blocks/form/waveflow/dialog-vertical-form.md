---
id: blocks/form/waveflow/dialog-vertical-form
type: block
name: Dialog 垂直表单
description: Radix Dialog (rounded-2xl + paper + pop shadow) + 5px Header (border-b-100) + Body space-y-3.5 vertical fields (Label[required] + Input/Textarea + error) + Footer warm-2/40 ghost+primary 按钮
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm, serious]
  stack: [shadcn-radix]
uses:
  - components/inputs/waveflow/blue-focus-input
  - components/buttons/waveflow/cva-engineer-button
preview: /preview/blocks/form/waveflow/dialog-vertical-form
---

# Waveflow Dialog Vertical Form

> waveflow 所有 admin 表单弹窗的统一形态——Radix Dialog 包装：`max-w-md` 默认（复杂表单覆写 max-w-lg/xl/2xl）+ rounded-2xl + paper bg + pop shadow。内部 Header (title + 关闭 X) / Body (space-y-3.5 垂直字段) / Footer (warm-2/40 底 + ghost 取消 + primary 主操作)。`useConfirm()` hook 提供命令式 await confirm({...})。

## 页面骨架

```tsx
<Dialog open={open} onOpenChange={v => !v && !loading && onClose()}>
  <DialogContent className="!max-w-md">       {/* fixed center + rounded-2xl border-stone-200/60 bg-paper shadow-pop + zoom-in animate */}
    <DialogHeader>                            {/* flex border-b border-stone-100 px-5 py-3.5 */}
      <DialogTitle>添加项目</DialogTitle>     {/* 15px font-semibold tracking-tight stone-900 */}
      <DialogCloseIcon />
    </DialogHeader>

    <DialogBody className="space-y-3.5">       {/* max-h-[70vh] overflow-y-auto px-5 py-4 */}
      <div>
        <Label htmlFor="name" required>项目名称</Label>
        <Input id="name" value={formData.name} onChange={...} error={!!errors.name} placeholder="例如：浙有善育" autoFocus />
        {errors.name && <div className="mt-1 text-[11px] text-red-600">{errors.name}</div>}
      </div>
      <div>
        <Label htmlFor="desc" required>项目描述</Label>
        <Textarea id="desc" rows={3} value={formData.description} onChange={...} error={!!errors.description} />
        {errors.description && <div className="mt-1 text-[11px] text-red-600">{errors.description}</div>}
      </div>
    </DialogBody>

    <DialogFooter>                            {/* flex justify-end gap-2 border-t border-stone-100 bg-warm-2/40 px-5 py-3 */}
      <Button variant="ghost" onClick={onClose} disabled={loading}>取消</Button>
      <Button variant="primary" onClick={handleSave} loading={loading}>
        {mode === 'create' ? '创建' : '保存'}
      </Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

## 视觉特征

- **DialogContent 默认 max-w-md (28rem = 448px)**：标准短表单
- **DialogContent rounded-2xl (16px)**：比 admin 常规卡片 `rounded-xl` 大一档——dialog 是 modal 层级，更"独立"
- **DialogContent border-stone-200/60**：比 admin section 的 /40 略深——更明显的"分隔"
- **Header / Body / Footer 由独立组件管 padding**：Header `px-5 py-3.5` / Body `px-5 py-4` / Footer `px-5 py-3`
- **Footer 底色 warm-2/40**：让"取消/确定"区有"沉底感"
- **disabled close on loading**：`onOpenChange={v => !v && !loading && onClose()}` 防中途关
- **autoFocus 第一个 Input**：用户开 dialog 直接打字
- **错误显示行 `mt-1 text-[11px] text-red-600`**：比正文小一档，红色
- **Textarea 同款 Input 样式**：error/mono 两 prop 通用

## 适配指南

- 字段过多（> 6）时把 max-w 升到 lg/xl/2xl，Body 自带 `max-h-[70vh] overflow-y-auto`
- 危险确认走 `<ConfirmDialog>` （独立条目 `danger-confirm-modal`），不要在 normal form 内做"确认删除"
- Reset 字段：`useEffect` 监听 open + mode 切换时重 init formData
- 命令式调用：`const { confirm, dialog } = useConfirm(); const ok = await confirm({ title, description, danger: true })`

## 反模式

- ❌ Body 不限高—— 弹出超出屏幕
- ❌ Footer 用 white bg—— 失去"底层"语义
- ❌ Label 不带 required—— 必填字段视觉不明确
- ❌ 提交失败不 setLoading(false)—— 按钮永远 spin
