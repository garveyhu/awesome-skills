---
id: pages/form-flow/skillhub/profile-edit
type: page
name: 编辑资料页
description: 单栏长表单（头像 section + 基本信息 section + 危险区），顶部返回 + 保存
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - blocks/nav/skillhub/glass-pill-navbar
  - blocks/form/skillhub/profile-edit-form
  - components/buttons/skillhub/dark-primary-cta
  - tokens/palettes/skillhub/skillhub-teal-mist
preview: /preview/pages/form-flow/skillhub/profile-edit
---

# Profile Edit Page

> `/me/edit`。页面本身很薄——就是给 `blocks/form/skillhub/profile-edit-form` 套一个 navbar + 返回链接 + 容器。

## 页面骨架

```
┌─ GlassPillNavbar ────────────────────────────────────┐
│                                                      │
│  ┌─ 编辑容器 max-w-2xl mx-auto pt-6 pb-16 ─────────┐ │
│  │                                                  │ │
│  │  ← 返回（跳 /me）    编辑资料     [保存]         │ │
│  │                                                  │ │
│  │  ┌─ 头像 section（白卡） ─────────────────┐       │ │
│  │  │  大圆头像 + Avatar Options grid         │       │ │
│  │  └─────────────────────────────────────┘       │ │
│  │                                                  │ │
│  │  ┌─ 基本信息 section（白卡） ──────────────┐     │ │
│  │  │  昵称 / 简介 / 性别 / 生日 / 地区        │     │ │
│  │  └──────────────────────────────────────┘      │ │
│  │                                                  │ │
│  │  ┌─ 危险区（rose border） ────────────────┐      │ │
│  │  │  退出登录                                │      │ │
│  │  └─────────────────────────────────────┘       │ │
│  └──────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────┘
```

## 核心代码

```tsx
export const ProfileEditPage = () => {
  const navigate = useNavigate();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [saving, setSaving] = useState(false);
  const [loading, setLoading] = useState(true);

  const handleSave = async (data) => {
    setSaving(true);
    try {
      await profileService.updateProfile(data);
      message.success('保存成功');
      navigate('/me');
    } catch {
      message.error('保存失败，请重试');
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className="min-h-screen flex items-center justify-center"><Spin /></div>;

  return (
    <>
      <GlassPillNavbar sticky={false} /* ... */ />
      <ProfileEditForm
        profile={profile!}
        onSave={handleSave}
        saving={saving}
      />
    </>
  );
};
```

## 适配指南

- navbar 不 sticky——表单页滚动时不需要挤顶栏
- 头像、基本信息、危险区分 3 段白卡——每段独立 `rounded-2xl border border-slate-200/60 p-6`
- 保存按钮放在**顶栏右侧**（由 form block 实现），不要也塞在表单底
- 保存成功用 Antd message 而不是弹 modal——阻塞太重
- 保存失败显示错误 message + 保持用户的输入（不要 reset form）

## 反模式

- 不要把表单做成左右分栏（左预览 / 右编辑）——太重；资料编辑单栏足够
- 不要每个字段都是一张白卡——字段按语义打包进 2-3 张卡就够
- 不要把"退出登录" / "注销账号"藏在菜单里——这是危险操作但使用频率不低，显式放页尾
