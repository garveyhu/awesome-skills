---
id: blocks/form/skillhub/profile-edit-form
type: block
name: 资料编辑表单
description: iOS 风列表点击编辑——每行 [label · value · ChevronRight]，点击弹独立 modal 修改
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/skillhub/skillhub-teal-mist
  - components/avatars-icons/skillhub/letter-avatar
preview: /preview/blocks/form/skillhub/profile-edit-form
---

# Profile Edit Form

> 名字叫 "form"，但**本质不是传统表单**——skillhub 真实用的是 **iOS 设置列表点击模式**：一屏显示所有字段行，每行 `label · value · ChevronRight`，点击行弹独立 modal 改该字段。没有"保存"按钮（modal 里改完立即保存）。

**如果你想做传统长表单 + 保存按钮那种形态，这个 block 不是；那种该另开一个 block**。

## 视觉特征

### Sticky 顶栏 · `max-w-lg h-12`
- 左 `ArrowLeft + 返回`（`text-slate-600 hover:text-slate-900`）
- 中间居中 `h1 text-sm font-bold text-slate-900` = "编辑资料"
- 右 `w-12` 空占位（对称平衡，没有保存按钮）

### 头像 section · 整块 button
- 居中大头像 80×80 ring-4 ring-slate-100
- 下方小字 `text-xs text-slate-400 "点击更换头像"`
- 整个 section 是 `<button>` · hover `bg-slate-50/50`
- 点击弹 **头像选择 modal**（5 列 grid 的 icon 头像）

### 字段列表 · `divide-y divide-slate-50 border-t border-slate-100`
每行格式（横向）：
```
[w-20 text-right text-slate-500 · label][mr-6][flex-1 text-left text-slate-900 truncate][ChevronRight text-slate-300]
```

- label 固定 `w-20` 右对齐——让所有 label 尾部对齐，视觉锚
- value `truncate`——长内容省略号
- 只读行（如 UID）**无 ChevronRight**——用缺失的 chevron 暗示"点不了"
- 未设置态 value 用 `text-slate-400`（如 "未设置"、"未填写"）

### 默认列表（skillhub 实际 7 行）
1. **UID** - 只读 · mono 字
2. **名字** - 必填
3. **简介** - 选填（可空显示"未填写"）
4. **性别** - 男/女/其他
5. **生日** - DatePicker modal
6. **所在地** - Cascader modal（省·市）
7. **Google** - 绑定态带 Google 四色 logo + `text-green-600 "已绑定"`

### Modal 形态
每字段独立 Modal：

- **头像 modal**：5 列 grid · icon 头像选项 · 带 Google 头像（如有）· 选中项 `ring-2 ring-indigo-400 bg-indigo-50`
- **Nickname modal**：Input + showCount 120 上限 · 底部 `取消 / 保存`
- **Bio modal**：Textarea rows=4 + showCount 200 · 底部 `取消 / 保存`
- **Gender modal**：垂直 button 列表 · 选中 `bg-indigo-50 text-indigo-700 font-semibold` · 点击即选即关（无保存按钮）
- **Birthday modal**：Antd DatePicker size=large · 选中即保存关闭
- **Location modal**：Antd Cascader size=large expandTrigger=hover · 选到二级（省·市）即保存关闭

**关键**：**gender/birthday/location/avatar** 这 4 个 modal **选择即保存即关闭**（无保存按钮）；**nickname/bio** 有 input 需显式保存按钮。

## 核心代码（骨架）

```tsx
type ModalKey = 'avatar' | 'nickname' | 'bio' | 'gender' | 'birthday' | 'location' | null;

export const ProfileEditForm = ({ profile, onSave }) => {
  const [modal, setModal] = useState<ModalKey>(null);
  // 各字段本地 state 省略...

  const rows = [
    { key: 'uid',      label: 'UID',     value: profile.uid,        editable: false, mono: true },
    { key: 'nickname', label: '名字',    value: nickname,            editable: true },
    { key: 'bio',      label: '简介',    value: bio || '未填写',     editable: true, empty: !bio },
    { key: 'gender',   label: '性别',    value: GENDER_MAP[gender] || '未设置', editable: true, empty: !gender },
    { key: 'birthday', label: '生日',    value: birthday || '未设置', editable: true, empty: !birthday },
    { key: 'location', label: '所在地',  value: location || '未设置', editable: true, empty: !location },
  ];

  return (
    <div className="min-h-screen bg-white font-sans pb-24">
      {/* Sticky 顶栏 */}
      <div className="sticky top-0 z-20 bg-white border-b border-slate-100">
        <div className="max-w-lg mx-auto flex items-center h-12 px-4">
          <button onClick={() => history.back()}
            className="flex items-center gap-1 text-sm text-slate-600 hover:text-slate-900 -ml-1">
            <ArrowLeft size={18} /> 返回
          </button>
          <h1 className="flex-1 text-center text-sm font-bold text-slate-900">编辑资料</h1>
          <div className="w-12" />
        </div>
      </div>

      <div className="max-w-lg mx-auto">
        {/* 头像 button */}
        <button onClick={() => setModal('avatar')}
          className="w-full flex flex-col items-center py-8 hover:bg-slate-50/50 transition-colors">
          {/* avatar · 80×80 ring-4 ring-slate-100 */}
          <span className="text-xs text-slate-400 mt-2">点击更换头像</span>
        </button>

        {/* 字段列表 */}
        <div className="divide-y divide-slate-50 border-t border-slate-100">
          {/* UID 只读 */}
          <div className="flex items-center px-5 py-4">
            <span className="w-20 text-sm text-slate-500 shrink-0 text-right mr-6">UID</span>
            <span className="flex-1 text-sm text-slate-900 font-mono">{profile.uid}</span>
          </div>

          {/* 可点击行 */}
          {rows.filter(r => r.editable).map(row => (
            <button key={row.key}
              onClick={() => setModal(row.key as ModalKey)}
              className="w-full flex items-center px-5 py-4 hover:bg-slate-50 transition-colors">
              <span className="w-20 text-sm text-slate-500 shrink-0 text-right mr-6">{row.label}</span>
              <span className={`flex-1 text-sm text-left truncate ${row.empty ? 'text-slate-400' : 'text-slate-900'}`}>
                {row.value}
              </span>
              <ChevronRight size={16} className="text-slate-300 shrink-0" />
            </button>
          ))}

          {/* Google 绑定行（特殊）*/}
          <div className="flex items-center px-5 py-4">
            <span className="w-20 text-sm text-slate-500 shrink-0 text-right mr-6">Google</span>
            {profile.googleId ? (
              <span className="flex-1 flex items-center gap-1.5 text-sm text-green-600">
                <GoogleIcon size={14} /> 已绑定
              </span>
            ) : (
              <button onClick={handleBindGoogle}
                className="flex-1 text-sm text-slate-400 text-left hover:text-indigo-500">
                去绑定
              </button>
            )}
            <ChevronRight size={16} className="text-slate-300 shrink-0" />
          </div>
        </div>
      </div>

      {/* Modals · 各字段独立（省略具体内容）*/}
      <AvatarModal open={modal === 'avatar'} onClose={() => setModal(null)} /* ... */ />
      <NicknameModal open={modal === 'nickname'} /* ... */ />
      {/* ... 等等 */}
    </div>
  );
};
```

## 适配指南

- 列表宽度 **`max-w-lg`** (512px) 而不是更宽——iOS 设置列表感 + 手机友好
- label 列固定 `w-20`（80px）——所有 label 对齐的视觉锚
- **列表 divider 用 `divide-y divide-slate-50`**——极淡的分割，不要用 slate-200
- **顶部 border 用 `border-t border-slate-100`** 稍深一点与列表内部 divider 形成层次
- hover `bg-slate-50`（不是 slate-100）——极轻 hover 反馈
- 所有 modal 都是 antd Modal + 自定义内容。nickname/bio 用 `onOk` 保存；其它字段（gender / birthday / location / avatar）用**选中时直接调 onSave + close**，跳过保存按钮
- 头像 modal 里 Google 头像可作为第一选项（如用户绑过 Google 账号）
- `hover:bg-slate-50/50` 头像区的 hover 是半透明——和纯灰行的 hover 区分

## 反模式

- ❌ **不要做成一屏长 form + 顶部保存按钮**——真实 skillhub 不是这样。一屏 form 是 Material 范式，iOS 列表点击更克制
- ❌ **不要把多个字段塞在一张白卡里**——每行独立是 divide-y 体系的核心
- ❌ **不要用 teal focus ring** 在 input 里——这里的 modal 是 antd Modal，用 antd 默认的 focus（会被 ConfigProvider 覆盖为 slate）
- ❌ **不要给 label 加 `font-bold`**——真实 label 是 `text-sm text-slate-500`（中等权重灰字），不是加粗黑字
- ❌ **不要在列表行里放图标前缀**（如字段图标）——iOS 列表的克制感关键在于"就是 label + value"，不加装饰
- ❌ **不要用"必填 / 可选"徽标标注**——列表模式下未填字段 `text-slate-400` 就足够表达
