# Google OAuth 弹窗登录 + 账号绑定

> 前端弹出 Google 授权窗口，后端用 access_token 换取用户信息，支持登录和绑定已有账号。

## 适用场景

- 需要给网站接入 Google 第三方登录
- 登录方式为弹窗（非页面跳转），用户体验更好
- 需要支持"已有密码用户绑定 Google"和"Google 直接注册"两种路径
- 同一 Google 账号的邮箱如果已注册，自动关联而非创建新账号

## 技术决策

| 决策 | 选择 | 理由 |
|------|------|------|
| 前端弹窗方式 | `google.accounts.oauth2.initTokenClient` | 弹出独立授权窗口（非 One Tap 右上角小框），体验和主流网站一致 |
| Token 类型 | access_token（非 ID token） | 前端用 OAuth2 implicit 流拿 access_token，后端调 Google userinfo API 获取用户信息，无需在后端配置 client_secret |
| 后端验证方式 | 调 Google userinfo API | 不需要 `google-auth` 库，只用 `requests` 即可，依赖最少 |
| 账号冲突策略 | 按邮箱自动关联 | 同邮箱的已有用户直接绑定 google_id，不创建重复账号 |
| Google 头像显示 | `<meta name="referrer" content="no-referrer">` | Google CDN 图片需要 no-referrer 才能正常加载 |

## 技术栈要求

- **后端**: Python + FastAPI + SQLAlchemy（任何支持 ORM 的 Python Web 框架均可适配）
- **前端**: React + TypeScript（需引入 Google Identity Services SDK）
- **数据库**: 用户表需有 `google_id` 字段

## 文件清单

| 文件 | 说明 |
|------|------|
| `backend-service.py` | GoogleAuthService：token 验证、用户查找/创建、账号绑定 |
| `backend-route.py` | 两个端点：`POST /auth/google`（登录）、`POST /auth/google/bind`（绑定） |
| `backend-dto.py` | 请求 DTO |
| `frontend-service.ts` | Google SDK 初始化、弹窗触发、后端 API 调用 |
| `frontend-button.tsx` | Google 登录按钮组件（带两阶段 loading） |
| `migration.sql` | 用户表添加 google_id 字段 |
| `config.md` | Google Cloud Console 配置、环境变量、index.html 改动 |

## 适配指南

复刻到新项目时需要调整：

1. **Google Client ID** — 替换 `frontend-service.ts` 中的 `GOOGLE_CLIENT_ID`
2. **User 模型** — 替换 `backend-service.py` 中的 `User`、`UserRole` 导入路径和字段名
3. **认证服务** — 替换 `AuthService` 的导入和调用（`create_access_token`、`ensure_default_role` 等）
4. **API 响应格式** — 替换 `Result.ok()` 为项目自己的响应封装
5. **默认头像** — `"icon:leaf"` 是 SkillHub 的 icon 头像系统，替换为你的默认头像逻辑
6. **index.html** — 添加 Google SDK script 和 no-referrer meta tag

所有需要适配的地方在模板代码中用 `# ADAPT:` 或 `// ADAPT:` 标注。

## 注意事项

- Google Identity Services SDK 必须用 `<script>` 标签加载，不能 npm install
- `lh3.googleusercontent.com` 的图片需要 `<meta name="referrer" content="no-referrer">`，否则无法显示
- `google.accounts.oauth2.initTokenClient` 的 `callback` 在用户关闭弹窗时**不会触发**，无法检测取消操作
- 绑定接口要检查该 google_id 是否已被其他账号绑定，避免一个 Google 账号绑定多个系统账号
- 用 access_token 调 userinfo API 方式不需要后端配置 `GOOGLE_CLIENT_ID` 环境变量（ID token 验证方式才需要）
