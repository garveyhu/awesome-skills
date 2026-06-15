---
id: blocks/layout/sage/sidebar-detail-split
type: block
name: 侧栏分屏布局
description: 280px Sidebar + 主区 styled-components 布局骨架，SpaceManagement / AgentStorePage 等管理页通用
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm, serious]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/sage/twelve-theme-spectrum
preview: /preview/blocks/layout/sage/sidebar-detail-split
---

# Sidebar Detail Split

> sage 重型管理页的标准骨架——左 280px Sidebar（标题 + + 按钮 + 搜索框 + 列表）+ 右主区（ContentHeader + DetailSection）。SpaceManagement / AgentStorePage 完全一致用这个；Sidebar 头部按钮（add / sync）用主题色 `${color}10` / `${color}20` hover bg。

## 视觉特征

- Container：styled.div `display: flex; flex: 1; height: 100%; width: 100%; background: #fff; overflow: hidden`
- Sidebar：`width: 280px; min-width: 280px; background: #fff; border-right: 1px solid #e5e5e5; padding: 12px; flex-direction: column`
- sidebar-header：`padding: 0 4px 24px 4px; font-weight: 700; font-size: 16px; color: #171717; letter-spacing: -0.01em; flex justify-between`
- header 右上 add/sync 按钮：`width: 32; height: 32; border-radius: 8; color: ${primaryColor}; background: ${primaryColor}10; hover: bg ${primaryColor}20 + scale(1.05)`
- search-box：`padding: 0 4px 16px 4px`
- search input wrapper（注入 antd `.ant-input-affix-wrapper`）：`border: 1px solid #e5e5e5; background: #fafafa; padding: 8px 12px; border-radius: 10` ; hover bg #fff ; focus bg #fff + `borderColor: ${color}80 + boxShadow: 0 0 0 2px ${color}05`
- 列表区：`flex: 1; overflow-y: auto; padding: 8px` + 4px scrollbar (slate-300)
- SpaceItem / AgentItem：`padding: 12px 16px; border-radius: 12; margin-bottom: 8; transition: all 0.2s ease; background: ${active ? '#f5f5f5' : 'transparent'}; border: 1px solid ${active ? '#e5e5e5' : 'transparent'}; color: ${active ? '#171717' : '#737373'}; position: relative`
- MainContent：`flex: 1; padding: 24px 32px; overflow-y: auto; background: #fff`
- ContentHeader：`display: flex; justify-content: space-between; padding-bottom: 16px; border-bottom: 1px solid #f5f5f5; .agent-title { display: flex; gap: 16px; align-items: center } h2 { font-size: 22; font-weight: 700; letter-spacing: -0.01em }`
- agent-title 左侧 icon：`w-12 h-12 rounded-xl flex center; background: ${color}15; color: ${color}` —— 主题色 8% bg + 主题色 icon
- DetailSection：`padding-top: 16; .section-content { background: #fff }` + 内含 antd Tabs

## 核心代码

```tsx
const Container = styled.div`display: flex; flex: 1; height: 100%; background: #fff;`;
const Sidebar = styled.div<{ $primaryColor: string }>`
  width: 280px;
  border-right: 1px solid #e5e5e5;
  padding: 12px;
  display: flex; flex-direction: column;
  .sidebar-header { font-weight: 700; padding: 0 4px 24px; display: flex; justify-content: space-between; }
  .sidebar-header .add-btn {
    width: 32px; height: 32px; border-radius: 8px; cursor: pointer;
    color: ${p => p.$primaryColor};
    background: ${p => p.$primaryColor}10;
    transition: all 0.2s;
    &:hover { background: ${p => p.$primaryColor}20; transform: scale(1.05); }
  }
`;
const Item = styled.div<{ $active: boolean; $primaryColor: string }>`
  padding: 12px 16px;
  border-radius: 12px;
  margin-bottom: 8px;
  background: ${p => p.$active ? '#f5f5f5' : 'transparent'};
  border: 1px solid ${p => p.$active ? '#e5e5e5' : 'transparent'};
  color: ${p => p.$active ? '#171717' : '#737373'};
  cursor: pointer;
  transition: all 0.2s ease;
  &:hover { background: #f5f5f5; }
`;

<Container>
  <Sidebar $primaryColor={primaryColor}>
    <div className="sidebar-header">
      <span>工作区</span>
      <div className="add-btn"><Plus size={16} /></div>
    </div>
    <Input prefix={<Search size={16} />} placeholder="搜索…" />
    <div className="space-list">{items.map(...)}</div>
  </Sidebar>
  <MainContent>
    <ContentHeader>...</ContentHeader>
    <DetailSection>...</DetailSection>
  </MainContent>
</Container>
```

## 适配指南

- `$primaryColor` 是 hex（不是 Tailwind）：`THEME_HEX_COLORS[themeColor]`
- Sidebar 列表项的"激活感"靠 `bg #f5f5f5 + border 1px #e5e5e5` 而不是阴影 —— 让边界感来自描边而非投影
- ContentHeader 用 `border-bottom: 1px solid #f5f5f5` 极淡分割线，避免硬切

## 反模式

- ❌ 把 Sidebar 和 MainContent 写成 Tailwind 单文件 —— 整段配色都靠 styled-components 的 props 注入主题，纯 className 做不到
- ❌ Sidebar 宽度 < 240px —— 列表项的 12 16 padding + 搜索框就装不下了
