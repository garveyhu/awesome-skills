---
id: pages/list-table/sage/admin-table-management
type: page
name: 管理后台通用表格
description: ManagementLayout + Antd Table + 操作列 通用模板，UserManagement / RoleManagement / Collections 共用
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm]
  stack: [react-antd-tailwind]
uses:
  - blocks/layout/sage/management-layout-header
  - blocks/feedback/sage/delete-confirm-modal
preview: /preview/pages/list-table/sage/admin-table-management
---

# Admin Table Management

> sage 多个管理后台共用此模板：UserManagement (用户) / RoleManagement (角色) / Collections (收藏) / 知识库 BusinessRule / PrefabSql。`<ManagementLayout title=... rightActions={<+ 新建>}>` + `<Table />` + 操作列（编辑 / 分配 / 删除）+ 编辑 Modal + 用户分配 Modal。

## 页面骨架

### Layout
```tsx
<ManagementLayout
  title={t('用户管理')}
  searchPlaceholder="搜索用户名 / 邮箱 / 角色"
  onSearch={fn}
  themeColor={themeColor}
  rightActions={
    <Button type="primary" icon={<Plus className="w-4 h-4" />} onClick={handleAdd} className={tc.bg}>
      + 新建用户
    </Button>
  }
>
  <Table columns={columns} dataSource={users} pagination={...} size="middle" />
</ManagementLayout>
```

### 通用列设计
- **ID** `width: 80, render: text => <span className="text-gray-500 pl-4">{text}</span>`
- **主标识列**（用户名 / 角色名）：avatar/icon themed + `font-medium` 名 + 副 description（slate-500 text-xs）
- **状态/类型** `<Tag style={{ backgroundColor: primary, color: '#fff', borderColor: primary }}>` 主题色 Tag
- **启用 Switch**：`<Switch size="small" checked onChange />`
- **创建时间** `width: 160, render: ts => new Date(ts).toLocaleString()`
- **操作** `width: 180, render: <Space size="small">` + 多个 `<Button type="text" size="small" icon={Settings/Users/Trash2 size 16}>` （Trash2 加 `danger` prop）

### Modal 模板
- 编辑 Modal：基本信息 + 关联资源选择
- UserAssignmentModal：Transfer 穿梭框（左未分配 / 右已分配） + 角色多选

## 视觉要点

1. **Antd Table 整体不自定义样式** —— 走 ManagementLayout 注入的 ConfigProvider 主题
2. **操作 icon 用 lucide-react size 16 stroke 默认** —— 不用 antd 自带 icon
3. **table size="middle"** —— sage 选 middle 而不是 large/small；middle 给到合适密度
4. **showTotal**：`pagination.showTotal: total => `共 ${total} 条`` —— 给上下文
5. **删除走 antd `modal.confirm`**（不是 sage 自定义的 delete-confirm-modal）—— 因为 admin 操作通常用 antd 标准
6. **PermissionGuard 包裹** —— 进 admin overlay 时已经有 RoleGuard 拦截，但表内某些操作（如删除）再加一层细粒度 permission

## 反模式

- ❌ 各管理页自己写 header / search —— 一定走 ManagementLayout
- ❌ 操作列用 Antd 默认 `<Tag>` icon —— 视觉重；用 type="text" + lucide icon 更轻
