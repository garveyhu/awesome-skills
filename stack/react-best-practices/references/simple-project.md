# 简单项目规范（单模块）

## 目录

1. [完整 src/ 目录结构](#完整-src-目录结构)
2. [vite.config.ts 配置](#viteconfigts-配置)
3. [tsconfig.app.json 别名配置](#tsconfigappjson-别名配置)
4. [依赖安装命令](#依赖安装命令)
5. [Husky 初始化](#husky-初始化)
6. [package.json scripts](#packagejson-scripts)
7. [Tailwind 入口样式](#tailwind-入口样式)
8. [路由使用示例](#路由使用示例)
9. [API 服务编写示例](#api-服务编写示例)
10. [类型定义规范](#类型定义规范)

---

## 完整 src/ 目录结构

```
src/
├── services/                    # API请求封装
│   ├── admin/                   # 按模块划分
│   │  ├── user.ts               # 用户相关API
│   │  └── role.ts               # 角色相关API
│   └── index.ts                 # API封装
│
├── assets/                      # 静态资源
│   ├── fonts/                   # 字体文件
│   ├── images/                  # 图片资源
│   └── styles/                  # 全局样式
│       └── index.less           # 全局样式
│
├── constants/                   # 常量
│   ├── app.constants.ts         # 应用常量
│   └── http-status.enum.ts      # HTTP 状态枚举
│
├── components/                  # 组件
│   ├── business/                # 业务组件
│   ├── complex/                 # 综合组件
│   │   └── loading.tsx          # loading组件
│   └── layout/                  # 布局组件
│       └── MainLayout.tsx       # 主布局
│
├── config/                      # 项目配置
│   ├── env.ts                   # 环境变量处理
│   └── settings.ts              # 应用常量配置
│
├── hooks/                       # 自定义Hook
│   ├── use-pagination.ts        # 分页Hook
│   └── use-permission.ts        # 权限Hook
│
├── pages/                       # 页面
│   ├── 404.tsx                  # 404组件
│   ├── login/                   # 登录页面
│   │   └── index.tsx
│   └── home/                    # 首页页面
│       ├── index.less           # home样式
│       └── index.tsx            # home组件
│
├── router/                      # 路由
│   ├── index.tsx                # 路由表
│   └── init.tsx                 # 路由注册
│
├── types/                       # 类型定义
│   ├── api.ts                   # API通用类型
│   ├── router.ts                # 路由类型
│   └── admin/                   # admin模块
│       └── user/                # 用户相关类型
│           ├── user.d.ts        # 实体对象
│           ├── user.dto.d.ts    # 数据传输对象
│           └── user.vo.d.ts     # 视图对象
│
├── App.tsx                      # 根组件
└── main.tsx                     # 项目入口文件
```

## vite.config.ts 配置

```typescript
import react from '@vitejs/plugin-react';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'vite';

const __dirname = dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  plugins: [react()],
  css: {
    preprocessorOptions: {
      less: {
        javascriptEnabled: true,
      },
    },
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
    },
  },
  server: {
    proxy: {
      '/development': {
        target: 'http://127.0.0.1:8888',
        changeOrigin: true,
        rewrite: path => path.replace(/^\/development/, ''),
      },
      '/production': {
        target: 'https://www.example.com',
        changeOrigin: true,
        rewrite: path => path.replace(/^\/production/, ''),
      },
    },
  },
});
```

## tsconfig.app.json 别名配置

在 `compilerOptions` 中添加：

```json
{
  "compilerOptions": {
    "baseUrl": "./",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

## 依赖安装命令

### 编码规范（devDependencies）

```bash
yarn add -D eslint @eslint/js @typescript-eslint/eslint-plugin @typescript-eslint/parser \
  eslint-plugin-react eslint-plugin-react-hooks eslint-plugin-react-refresh \
  eslint-plugin-prettier eslint-config-prettier prettier globals \
  prettier-plugin-tailwindcss @trivago/prettier-plugin-sort-imports \
  stylelint stylelint-config-standard stylelint-order stylelint-prettier \
  @ls-lint/ls-lint \
  husky lint-staged \
  @commitlint/cli @commitlint/config-conventional
```

### 功能依赖（dependencies）

```bash
yarn add antd @ant-design/icons react-router-dom axios humps lucide-react less
```

### 功能依赖（devDependencies）

```bash
yarn add -D tailwindcss @tailwindcss/postcss autoprefixer postcss @types/humps
```

## Husky 初始化

确保项目已 `git init`，然后执行：

```bash
# 安装 husky（Windows PowerShell）
npx husky-init; if ($?) { yarn }

# 配置 pre-commit 钩子
yarn husky add .husky/pre-commit 'yarn lint-staged'

# 配置 commit-msg 钩子
yarn husky add .husky/commit-msg 'yarn commitlint'
```

确保 `.husky/pre-commit` 内容：

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

yarn lint-staged
```

确保 `.husky/commit-msg` 内容：

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

yarn commitlint
```

## package.json scripts

```json
{
  "scripts": {
    "dev": "vite --host",
    "build": "tsc -b && vite build",
    "preview": "vite preview",
    "lint:eslint": "eslint \"src/**/*.{ts,tsx}\" --fix",
    "lint:prettier": "prettier . --write",
    "lint:stylelint": "stylelint \"src/**/*.{css,less,scss,vue}\" --fix",
    "lint:ls-lint": "ls-lint",
    "lint-staged": "lint-staged -c .lintstagedrc.cjs --allow-empty",
    "commitlint": "commitlint --config .commitlintrc.js --edit",
    "prepare": "husky install"
  }
}
```

## Tailwind 入口样式

在 `src/assets/styles/index.less` 中添加：

```css
@import (css) 'tailwindcss';
```

在 `src/App.tsx` 中引入：

```typescript
import '@/assets/styles/index.less';
```

## App.tsx 模板

完整的 `src/App.tsx`，包含全局 Loading、ConfigProvider、AntdApp 封装：

```tsx
import { App as AntdApp, ConfigProvider, Spin } from 'antd';
import { Suspense } from 'react';
import { RouterProvider } from 'react-router-dom';

import { router } from '@/router';
import '@/assets/styles/index.less';

const LoadingFallback = () => (
  <div
    style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #f0f9ff 0%, #e8f4fd 50%, #f0f0ff 100%)',
    }}
  >
    <div style={{ textAlign: 'center' }}>
      <Spin size="large" />
      <div
        style={{
          marginTop: 16,
          fontSize: 15,
          fontWeight: 500,
          color: '#64748b',
          letterSpacing: '0.5px',
        }}
      >
        加载中...
      </div>
    </div>
  </div>
);

const App = () => (
  <ConfigProvider theme={{ token: { colorPrimary: '#0ea5e9', borderRadius: 8 } }}>
    <AntdApp message={{ duration: 1.5, maxCount: 2, top: 72 }}>
      <Suspense fallback={<LoadingFallback />}>
        <RouterProvider router={router} />
      </Suspense>
    </AntdApp>
  </ConfigProvider>
);

export default App;
```

> `colorPrimary` 根据项目主题调整；`Suspense` 配合路由 `lazy()` 在页面切换时自动触发全屏 Loading。

## 路由使用示例

### 添加新页面路由

1. 在 `src/pages/` 下创建页面组件
2. 在 `src/router/index.tsx` 的 children 中添加路由

```tsx
// src/router/index.tsx
{
  path: '/user',
  component: lazy(() => import('@/pages/user')),
  meta: { title: '用户管理', auth: true },
},
```

### 需要角色守卫的路由

```tsx
{
  path: '/admin',
  component: lazy(() => import('@/pages/admin')),
  meta: { title: '管理后台', auth: true, roles: ['admin'] },
},
```

## API 服务编写示例

### 1. 定义类型

```typescript
// src/types/admin/user/user.d.ts
export interface User {
  userId: number;
  userName: string;
  email: string;
  password: string;
  createTime: Date | null;
  updateTime: Date | null;
}
```

```typescript
// src/types/admin/user/user.dto.d.ts
import { type PaginationParams } from '@/types/api';
import { type User } from './user';

export interface UserSaveDTO extends User {}
export interface UserQueryDTO extends User, PaginationParams {}
```

```typescript
// src/types/admin/user/user.vo.d.ts
import { type User } from './user';

export interface UserVO extends User {}
```

### 2. 编写 API 服务

```typescript
// src/services/admin/user.ts
import { post } from '@/services';
import type { UserQueryDTO, UserSaveDTO } from '@/types/admin/user/user.dto';
import type { UserVO } from '@/types/admin/user/user.vo';
import type { ResultVO } from '@/types/api';

export const userService = {
  insert: (user: UserSaveDTO): Promise<ResultVO<any>> => {
    return post('/user/insert', user);
  },
  update: (user: UserSaveDTO): Promise<ResultVO<any>> => {
    return post('/user/update', user);
  },
  delete: (requestVO: UserQueryDTO): Promise<ResultVO<any>> => {
    return post('/user/delete', requestVO);
  },
  get: (requestVO: UserQueryDTO): Promise<ResultVO<UserVO>> => {
    return post('/user/get', requestVO);
  },
  page: (requestVO: UserQueryDTO): Promise<ResultVO<UserVO[]>> => {
    return post('/user/page', requestVO);
  },
};

export default userService;
```

## 类型定义规范

| 类型 | 文件后缀 | 说明 |
|------|---------|------|
| 实体对象 | `.d.ts` | 数据库表映射，字段与后端一致 |
| 数据传输对象 | `.dto.d.ts` | 请求参数，继承实体 + 分页等扩展 |
| 视图对象 | `.vo.d.ts` | 响应数据，继承实体 + 前端扩展 |

目录组织：
```
src/types/
├── api.ts                # 通用 API 类型（ResultVO、Pagination 等）
├── router.ts             # 路由类型
└── {module}/             # 按业务模块分组
    └── {entity}/         # 按实体分组
        ├── {entity}.d.ts
        ├── {entity}.dto.d.ts
        └── {entity}.vo.d.ts
```
