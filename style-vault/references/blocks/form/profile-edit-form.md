---
id: blocks/form/profile-edit-form
type: block
name: 资料编辑表单
description: avatar picker + 昵称 + bio + 性别 + 生日 + 地区 + 保存，典型"用户资料"多字段表单
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/skillhub-teal-mist
  - components/inputs/soft-form-input
  - components/buttons/dark-primary-cta
  - components/avatars-icons/letter-avatar
preview: /preview/blocks/form/profile-edit-form
---

# Profile Edit Form

> 用户中心编辑资料的表单——**头像选择器 + 昵称 + 简介 textarea + 性别（段控件）+ 生日（DatePicker）+ 地区（Cascader）+ 保存**。示范 Antd 专用组件（Cascader / DatePicker）如何嵌入手写 soft-input 风格。

## 视觉特征

- 顶栏：返回箭头 + 标题 + 保存按钮（`ArrowLeft + 编辑资料 + DarkPrimaryCta`）
- 字段容器：单列 `max-w-2xl mx-auto space-y-6`
- 每字段：label `text-sm font-bold text-slate-900 mb-1.5` + 字段控件
- 危险操作（登出 / 注销）：单独 section 在表单末尾，用 rose 色系分开

### Avatar picker

- 大圆头像 `w-24 h-24`（96px）居中 + hover 覆盖编辑提示
- 下面是 avatar 快选网格：`AVATAR_OPTIONS.map(Icon => <button ...>)` 行内 8-12 个
- 真实上传 `<input type="file">` 藏在 label 里

### Textarea（简介）

沿用 soft-form-input 规则：`rounded-xl px-4 py-3 border-slate-300 focus:primary-500 resize-none`

### 性别（段控件）

```tsx
<div className="flex gap-2 p-1 bg-slate-100 rounded-xl border border-slate-200/60">
  {[['male', '男'], ['female', '女'], ['other', '其他']].map(([v, l]) => (
    <button className={active === v
      ? 'bg-white text-slate-900 shadow-sm ...'
      : 'text-slate-500 hover:text-slate-700 ...'}>{l}</button>
  ))}
</div>
```

### 生日（Antd DatePicker）

Antd DatePicker 强制覆盖为 soft-input 风格：

```tsx
<DatePicker
  size="large"
  style={{
    width: '100%',
    borderRadius: 12,
    borderColor: '#cbd5e1',
    padding: '10px 16px',
    fontSize: 14,
  }}
  onChange={(d) => setBirthday(d?.format('YYYY-MM-DD') ?? null)}
/>
```

### 地区（Antd Cascader）

```tsx
<Cascader
  options={REGIONS}
  size="large"
  placeholder="选择地区"
  style={{ width: '100%' }}
  className="[&_.ant-select-selector]:!rounded-xl [&_.ant-select-selector]:!border-slate-300"
  onChange={(value) => setLocation(value?.join(' / ') ?? null)}
/>
```

## 核心代码（骨架）

```tsx
export const ProfileEditForm = ({ profile, onSave, saving }: Props) => {
  const [nickname, setNickname] = useState(profile.nickname);
  const [bio, setBio] = useState(profile.bio ?? '');
  const [avatarUrl, setAvatarUrl] = useState(profile.avatarUrl);
  const [gender, setGender] = useState(profile.gender);
  const [birthday, setBirthday] = useState(profile.birthday);
  const [location, setLocation] = useState(profile.location);

  return (
    <div className="max-w-2xl mx-auto space-y-6 py-8 px-4">
      {/* 顶栏 */}
      <div className="flex items-center justify-between mb-4">
        <button onClick={() => history.back()}
          className="inline-flex items-center gap-2 text-slate-500 hover:text-slate-900">
          <ArrowLeft size={18} /> 返回
        </button>
        <h1 className="text-2xl font-extrabold text-slate-900">编辑资料</h1>
        <DarkPrimaryCta size="md" onClick={() => onSave({ nickname, bio, avatarUrl, gender, birthday, location })}
          disabled={saving}>
          {saving ? '保存中...' : '保存'}
        </DarkPrimaryCta>
      </div>

      {/* 头像 */}
      <section className="bg-white rounded-2xl border border-slate-200/60 p-6">
        <label className="text-sm font-bold text-slate-900 mb-4 block">头像</label>
        <div className="flex flex-col items-center gap-4">
          <div className="w-24 h-24 rounded-full overflow-hidden ring-2 ring-slate-100">
            {/* 真实头像 或 LetterAvatar */}
          </div>
          <div className="grid grid-cols-8 gap-2">
            {AVATAR_OPTIONS.map((opt) => (
              <button key={opt.name}
                onClick={() => setAvatarUrl(toIconAvatarUrl(opt.name))}
                className={`w-10 h-10 rounded-lg flex items-center justify-center transition-all
                            ${avatarUrl === toIconAvatarUrl(opt.name)
                              ? 'ring-2 ring-teal-500 bg-teal-50'
                              : 'hover:bg-slate-50'}`}>
                {opt.icon}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* 基本信息 */}
      <section className="bg-white rounded-2xl border border-slate-200/60 p-6 space-y-5">
        <SoftFormInput label="昵称" value={nickname} onChange={(e) => setNickname(e.target.value)} />
        <div>
          <label className="block text-sm font-bold text-slate-900 mb-1.5">简介</label>
          <textarea
            value={bio} onChange={(e) => setBio(e.target.value)}
            rows={3} maxLength={200}
            className="w-full bg-white border border-slate-300 rounded-xl px-4 py-3 text-sm
                       focus:ring-2 focus:border-teal-500 focus:ring-teal-500/20
                       transition-all outline-none resize-none"
          />
          <div className="text-right text-xs text-slate-400 mt-1">{bio.length}/200</div>
        </div>

        <div>
          <label className="block text-sm font-bold text-slate-900 mb-1.5">性别</label>
          <div className="flex gap-2 p-1 bg-slate-100 rounded-xl border border-slate-200/60">
            {([['male', '男'], ['female', '女'], ['other', '其他']] as const).map(([v, l]) => (
              <button key={v} onClick={() => setGender(v)}
                className={`flex-1 py-2 text-sm font-semibold rounded-lg transition-all ${
                  gender === v ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500'
                }`}>{l}</button>
            ))}
          </div>
        </div>

        {/* 生日 · 地区 参见上面 Antd DatePicker / Cascader 覆盖 */}
      </section>

      {/* 危险区 */}
      <section className="bg-white rounded-2xl border border-rose-200/60 p-6">
        <label className="text-sm font-bold text-rose-700 mb-2 block">账号</label>
        <p className="text-xs text-slate-500 mb-4">退出登录后本设备的会话会失效。</p>
        <button className="px-4 py-2 rounded-xl border border-rose-300 text-rose-600
                           hover:bg-rose-50 text-sm font-medium transition-all">
          退出登录
        </button>
      </section>
    </div>
  );
};
```

## 适配指南

- 多字段表单按"语义分区"拆 section，每 section 一个白卡 + `rounded-2xl border`——不要把所有字段塞在一张卡里，6+ 字段时太拥挤
- Antd 组件（DatePicker / Cascader / Select）必须用 className override 把 border 拉到 slate-300 + rounded-xl + padding 对齐——否则会显得"插入物"
- 保存按钮放在顶栏右侧（不是表单底）——让用户在任何时候都能提交
- 头像区单独一个 section（不塞在基本信息里）——视觉重量大，独立容器更稳
- 危险区（退出 / 删除账号）用 rose border + rose text 分开——语义色带入，不至于误点

## 反模式

- 不要把所有字段 grid 2×N 铺——单列阅读节奏更稳定
- 不要给表单加 "未保存更改" 提示条并 sticky 到顶——本 style 不走这种 dashboard 硬告警
- 不要把 Cascader 换成自写 Select 堆叠——REGIONS 是层级数据，Cascader 更合
- 不要把"退出登录"和"保存"并列放顶栏——动作语义不同，必须分区
