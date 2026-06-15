---
id: blocks/nav/sage/command-palette
type: block
name: 命令面板
description: Linear / Raycast 风全局命令面板，分组列表 + 键盘导航 + 状态栏，admin 专属
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/sage/twelve-theme-spectrum
  - tokens/motion/sage/animate-in-suite
preview: /preview/blocks/nav/sage/command-palette
---

# Command Palette

> Ctrl/Cmd+P 唤起的全局命令面板（admin 专属）。640px 宽 + 顶部 15% 居中弹出 + Antd Modal 容器（rounded-[20px]）+ 顶部 Search Input + 分组列表 + 底部状态栏（带 ↑↓ ↵ 提示）。无 mask（可以隔着透出后面操作），ESC 关闭。

## 视觉特征

- 触发条件：`(e.ctrlKey || e.metaKey) && e.key === 'p'` + `user.roles.some(r => r.name === 'admin')`
- Modal 容器：`mask={false} closable={false} width={640} style={{ top: '15%' }} rootClassName="command-palette-modal"`
- Modal CSS（注入 `<style>`）：
  - `.ant-modal-content { borderRadius: 20px; border: 1px solid rgba(0,0,0,0.06); box-shadow: 0 24px 48px -12px rgba(0,0,0,0.18), 0 12px 24px -12px rgba(0,0,0,0.1) }`
- Search Input：`padding: 16px 20px; border: none; border-bottom: 1px solid rgba(0,0,0,0.06); background: transparent`
- ESC 角标：`px-1.5 py-0.5 bg-gray-100 rounded text-[10px] text-gray-400 font-medium`
- 列表容器：`flex-1 overflow-y-auto p-1 space-y-0.5` + 完全隐藏滚动条 (`.command-palette-list`)
- 分组标题：`px-3 py-2 text-xs font-medium text-gray-400 select-none`
- 列表项 active：`bg-gray-50/80 ${themeClasses.text}` （主题色文字）
- 列表项 idle：`text-gray-600 hover:bg-gray-50/50`
- 列表项 icon 容器：`w-8 h-8 rounded-md flex items-center justify-center` + active 时 `bg-white shadow-sm ring-1 ring-gray-900/5`
- 列表项内容：title 14px font-medium leading-tight + description 12px font-light truncate text-gray-400
- active 右侧：`<CornerDownLeft size={14} className="text-gray-300" />`
- 空态：`<Command size={40} strokeWidth={1} className="text-gray-200" />` + 14px font-light "No results"
- 底部状态栏：`px-4 py-2.5 bg-gray-50/50 border-t border-gray-100 + backdrop-blur-sm + rounded-b-[20px]` 含 Cmd 标识 + ↑↓ navigate + ↵ open

## 核心代码

完整 393 行见 `core/components/common/CommandPalette.tsx`。关键部分：

```tsx
<Modal
  open={isOpen}
  onCancel={() => setIsOpen(false)}
  footer={null}
  closable={false}
  mask={false}
  width={640}
  style={{ top: '15%' }}
  rootClassName="command-palette-modal"
  destroyOnHidden
>
  <div className="flex flex-col max-h-[550px]">
    <div className="command-palette-input">
      <Input
        ref={inputRef}
        placeholder="Search…"
        prefix={<Search className="text-gray-300 mr-2" size={18} />}
        suffix={<span className="px-1.5 py-0.5 bg-gray-100 rounded text-[10px] text-gray-400 font-medium">ESC</span>}
        value={search}
        onChange={e => setSearch(e.target.value)}
        allowClear
      />
    </div>
    <div ref={listRef} className="command-palette-list flex-1 overflow-y-auto p-1 space-y-0.5">
      <div className="px-3 py-2 text-xs font-medium text-gray-400 select-none">应用</div>
      {filtered.map((item, i) => (
        <div className={`group flex items-center gap-2.5 px-2.5 py-2 rounded-lg cursor-pointer transition-all duration-200 ${
          i === selectedIndex ? `bg-gray-50/80 ${tc.text}` : 'text-gray-600 hover:bg-gray-50/50'
        }`}>
          <div className={`w-8 h-8 rounded-md flex items-center justify-center ${i === selectedIndex ? 'bg-white shadow-sm ring-1 ring-gray-900/5' : 'group-hover:bg-gray-100'}`}>{icon}</div>
          <div className="flex-1 min-w-0">
            <div className={`text-[14px] font-medium leading-tight ${i === selectedIndex ? tc.text : 'text-gray-700'}`}>{item.title}</div>
            <div className="text-[12px] truncate text-gray-400 mt-0.5 font-light">{item.description}</div>
          </div>
          {i === selectedIndex && <CornerDownLeft size={14} className="text-gray-300" />}
        </div>
      ))}
    </div>
    <div className="px-4 py-2.5 bg-gray-50/50 border-t border-gray-100 flex items-center justify-between text-[11px] text-gray-400 select-none backdrop-blur-sm rounded-b-[20px]">
      <span><Command size={12} className="mr-1" /> Sage Command</span>
      <span>↑↓ navigate · ↵ open</span>
    </div>
  </div>
</Modal>
```

## 视觉要点

1. **borderRadius 20** 比常规 Antd Modal 的 8px 大很多——配合 `box-shadow` 双层（24/48px 大投 + 12/24px 中投）让面板"飘起来"
2. ESC chip 用 `text-[10px]`（不是常规 12）——故意比正文小一档，强调它是"快捷键提示"而非内容
3. icon container 的 `ring-1 ring-gray-900/5` 是几乎不可见的灰圈，但选中态会让 icon 看起来像凸起的"按钮"
4. description 用 `font-light`（300）——和 title 600 形成大反差，提示"次要信息"
5. 整个 list 隐藏滚动条（`scrollbar-width: none`）—— 操作时滚动条出现会破坏空气感

## 适配指南

- 商品列表的 commands 用 useMemo + i18n key 维护
- 键盘 ↑↓ 循环导航，hover 鼠标不会打断键盘 selectedIndex（用 `isMouseSelection.current` 标记）
- 选中后 ↵ 不直接 navigate，而是调 `onSelect(module)` 让父级决定（admin overlay 弹一个 module / navigate 到一个 route）

## 反模式

- ❌ 给所有用户开 Cmd+P —— sage 选择只给 admin（一般用户用侧栏导航足够）
- ❌ 加 mask —— 隔断了"快速跳"的体验，sage 的设计是"边看边跳"
