# AdminTable

> 管理后台无边框表格，统一分页、中文本地化、行 hover 减淡

## 技术栈

React + Ant Design + Tailwind CSS

## 预览效果

无边框无竖线表格，底部分页栏带"共 N 条"总数显示、页大小切换（10/15/20/50 条/页）、"跳至 X 页"快速跳转。行 hover 时背景变为极浅灰色，选中行为浅蓝，展开行为浅灰。表格不被任何边框容器包裹，直接渲染在面板中。

## 核心代码

```tsx
import { ConfigProvider, Table } from 'antd';
import type { TableProps } from 'antd';

const ADMIN_PAGINATION = {
  defaultPageSize: 10,
  showSizeChanger: true,
  showQuickJumper: true,
  pageSizeOptions: ['10', '15', '20', '50'],
  showTotal: (total: number) => `共 ${total} 条`,
  size: 'small' as const,
  style: { paddingRight: 16 },
  locale: {
    jump_to: '跳至',
    page: '页',
    items_per_page: '条/页',
  },
};

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

function AdminTable<T extends object>(props: TableProps<T>) {
  return (
    <ConfigProvider theme={ADMIN_THEME}>
      <Table<T>
        size="small"
        bordered={false}
        {...props}
        className={`[&_.ant-table]:!border-0 [&_.ant-table-container]:!border-0 [&_.ant-table-cell]:!border-inline-end-0 [&_.ant-table-row:hover>*]:!bg-slate-50/80 [&_.ant-table-row-selected>*]:!bg-blue-50/50 [&_.ant-table-expanded-row>*]:!bg-slate-50/50 ${props.className || ''}`}
        pagination={props.pagination === false ? false : { ...ADMIN_PAGINATION, ...(typeof props.pagination === 'object' ? props.pagination : {}) }}
      />
    </ConfigProvider>
  );
}

export default AdminTable;
```

## 样式要点

- `bordered={false}` + Tailwind CSS override 去掉 Ant Design 表格的所有边框线（外框、容器框、单元格竖线），实现完全无边框效果
- 行 hover 用 `bg-slate-50/80` 半透明浅灰，比 Ant Design 默认的深灰轻很多，不喧宾夺主
- 选中行 `bg-blue-50/50`、展开行 `bg-slate-50/50`，都用半透明保持轻盈
- 分页栏 `paddingRight: 16` 防止分页控件粘着表格右边框
- 中文 locale（跳至/页/条/页）替换 Ant Design 默认的英文 "Go to"/"page"
- 默认每页 10 条，可选 10/15/20/50
- 用 `ConfigProvider` 包裹以覆盖 Select 下拉面板样式（选中项、hover 背景色）
- pagination 支持外部覆盖：传入的 pagination props 会与默认配置合并，传 `false` 则完全隐藏分页

## Ant Design 覆盖

```ts
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
```

- `optionSelectedBg: '#e2e8f0'` -- Select 下拉已选中项背景色（slate-200，比默认浅）
- `optionActiveBg: '#f1f5f9'` -- Select 下拉 hover 背景色（slate-100）
- `optionSelectedColor: '#334155'` -- 已选中项文字色（slate-700）
- `colorTextQuaternary: '#94a3b8'` -- 四级文字色（slate-400）
- `motionDurationMid: '0.2s'` -- hover 过渡动画时长

## 使用示例

```tsx
import AdminTable from './AdminTable';

const columns = [
  { title: '名称', dataIndex: 'name', key: 'name' },
  { title: '状态', dataIndex: 'status', key: 'status' },
  { title: '创建时间', dataIndex: 'createdAt', key: 'createdAt' },
];

function UserListPage() {
  const [data, setData] = useState<User[]>([]);

  return (
    <AdminTable
      dataSource={data}
      rowKey="id"
      columns={columns}
    />
  );
}
```

无需手动传 `pagination` 或 `size` 属性，AdminTable 已内置合理的默认值。如需自定义分页，可传入 `pagination` 对象与默认配置合并；传 `pagination={false}` 则完全隐藏分页栏。
