# AdminTableToolbar

> 表格顶部工具栏，搜索+筛选左对齐，功能按钮右对齐

## 技术栈

React + Ant Design + Tailwind CSS

## 预览效果

单行 flex 布局工具栏。左侧依次排列：搜索框（180px）、筛选控件（Select/Input）。右侧放功能按钮（新建、同步等）。所有控件统一 size=small，间距 gap-2，整体底部间距 mb-3。

## 核心代码

> 注意：AdminTableToolbar 与 AdminTable 共享同一个 `ADMIN_THEME` 配置，定义见 [admin-table.md](./admin-table.md)。

```tsx
import { ConfigProvider, Input } from 'antd';

// ADMIN_THEME 与 AdminTable 共享，参见 admin-table.md
const ADMIN_THEME = {
  components: {
    Select: {
      optionSelectedBg: '#e2e8f0',
      optionSelectedColor: '#334155',
      optionActiveBg: '#f1f5f9',
      colorTextQuaternary: '#94a3b8',
      motionDurationMid: '0.2s',
    },
  },
};

interface AdminTableToolbarProps {
  searchPlaceholder?: string;
  searchValue?: string;
  onSearch?: (value: string) => void;
  filters?: React.ReactNode;
  actions?: React.ReactNode;
}

export const AdminTableToolbar = ({ searchPlaceholder, searchValue, onSearch, filters, actions }: AdminTableToolbarProps) => (
  <ConfigProvider theme={ADMIN_THEME}>
    <div className="flex items-center mb-3 gap-2">
      <div className="flex items-center gap-2">
        {onSearch && (
          <Input.Search
            placeholder={searchPlaceholder || '搜索...'}
            allowClear
            size="small"
            style={{ width: 180 }}
            defaultValue={searchValue}
            onSearch={onSearch}
          />
        )}
        {filters}
      </div>
      {actions && (
        <div className="flex items-center gap-2 ml-auto shrink-0">
          {actions}
        </div>
      )}
    </div>
  </ConfigProvider>
);
```

## 样式要点

- 布局原则：筛选相关（搜索框+下拉筛选）全部左对齐，功能按钮（新建、批量操作）右对齐（`ml-auto`）
- 搜索框固定 `width: 180px`，使用 `Input.Search` 带放大镜按钮，`size="small"`
- 筛选控件（Select/Input）统一 `size="small"` + `style={{ width: 110 }}`，保持宽度一致
- 底部间距 `mb-3` 与表格保持适当距离
- 用 `ConfigProvider` 包裹以应用统一的 Select 下拉主题（与 AdminTable 共享 ADMIN_THEME）
- `filters` slot 放左侧紧跟搜索框，`actions` slot 放右侧

## Ant Design 覆盖

与 AdminTable 共享同一个 ADMIN_THEME 配置，参见 [admin-table.md](./admin-table.md)。

## 使用示例

### 1. 纯搜索（最简单）

```tsx
<AdminTableToolbar
  searchPlaceholder="搜索标题..."
  onSearch={(q) => void search(q)}
/>
```

### 2. 搜索 + 筛选 filters

```tsx
import { Select, Input, Space } from 'antd';

<AdminTableToolbar
  searchPlaceholder="搜索技能名称..."
  onSearch={(q) => setKeyword(q)}
  filters={
    <Space size="small">
      <Select
        size="small"
        style={{ width: 110 }}
        placeholder="状态"
        allowClear
        options={[
          { label: '已上线', value: 'online' },
          { label: '已下线', value: 'offline' },
        ]}
        onChange={(v) => setStatus(v)}
      />
      <Input
        size="small"
        style={{ width: 110 }}
        placeholder="作者"
        onChange={(e) => setAuthor(e.target.value)}
      />
    </Space>
  }
/>
```

### 3. 搜索 + 功能按钮 actions

```tsx
import { Button } from 'antd';

<AdminTableToolbar
  searchPlaceholder="搜索标签..."
  onSearch={(q) => setKeyword(q)}
  actions={
    <Button type="primary" size="small">
      新建标签
    </Button>
  }
/>
```
