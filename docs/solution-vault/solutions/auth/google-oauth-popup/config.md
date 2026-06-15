# 配置说明

## 1. Google Cloud Console 设置

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建或选择项目
3. 启用 **Google Identity** 相关 API
4. 进入 **APIs & Services → Credentials**
5. 创建 **OAuth 2.0 Client ID**，类型选择 **Web application**
6. 设置 **Authorized JavaScript origins**:
   - 开发环境: `http://localhost:5173`（或你的前端端口）
   - 生产环境: `https://your-domain.com`
7. 记下 **Client ID**（形如 `xxxx.apps.googleusercontent.com`）

> 注意：本方案使用 access_token + userinfo API 方式，**不需要配置 Redirect URIs**，也**不需要在后端配置 Client Secret**。

## 2. 前端 index.html

添加两个标签到 `<head>` 中：

```html
<!-- Google Identity Services SDK -->
<script src="https://accounts.google.com/gsi/client" async defer></script>

<!-- 允许 Google CDN 头像正常加载 -->
<meta name="referrer" content="no-referrer" />
```

## 3. 前端 Client ID

在 `frontend-service.ts` 中替换：

```typescript
const GOOGLE_CLIENT_ID = '你的-client-id.apps.googleusercontent.com';
```

## 4. 后端依赖

只需要 `requests` 库（或 `httpx`），不需要 `google-auth` 等专用库：

```
pip install requests
# 或
uv add requests
```

## 5. 数据库

用户表需添加 `google_id` 字段，见 `migration.sql`。
