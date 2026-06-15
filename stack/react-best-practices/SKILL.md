---
name: react-best-practices
description: >
  React project initialization, development guidance, and code review based on
  personal architectural conventions (yarn+vite+ts+react+antd+tailwind).
  Use when: (1) Creating/initializing a new React project,
  (2) Adding new pages, components, modules, or API services to an existing React project,
  (3) Reviewing React project structure and code organization,
  (4) Setting up linting/formatting toolchain (eslint, prettier, stylelint, husky, commitlint, ls-lint, lint-staged),
  (5) Configuring routing or HTTP request utilities.
  Supports two project scales: simple (single-module) and complex (multi-module with dynamic route discovery).
  Default UI stack: Antd + Tailwind CSS. Default backend convention: Python (snake_case API with humps auto-conversion).
---

# React Best Practices

## 概述

根据个人架构习惯，提供 React 项目的全生命周期指导：初始化、开发规范、代码审查。

**核心技术栈**: yarn + vite + react + typescript + antd + tailwind CSS

**项目规模**:
- **简单项目**（默认）：单模块，静态路由表，适合大多数场景。详见 [references/simple-project.md](references/simple-project.md)
- **复杂项目**：多模块，动态路由发现（import.meta.glob），适合大型 SPA。详见 [references/complex-project.md](references/complex-project.md)

## 阶段一：初始化新项目（Init）

当用户要求创建新 React 项目时，按以下步骤执行。

### 前置检查

1. 确认 node >= 18、yarn 已安装
2. 询问项目名称和目标目录
3. 询问项目规模（简单/复杂），默认简单

### 步骤 1: 创建 Vite 项目

```bash
yarn create vite {项目名} --template react-ts
cd {项目名}
```

### 步骤 2: 安装编码规范依赖

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

### 步骤 3: 安装功能依赖

```bash
yarn add antd @ant-design/icons react-router-dom axios humps lucide-react less
yarn add -D tailwindcss @tailwindcss/postcss autoprefixer postcss @types/humps
```

### 步骤 4: 复制配置文件

从 `assets/configs/` 复制以下文件到项目根目录：

| 源文件 | 目标 |
|--------|------|
| `eslint.config.js` | `{项目根}/eslint.config.js` |
| `.prettierrc` | `{项目根}/.prettierrc` |
| `.stylelintrc.cjs` | `{项目根}/.stylelintrc.cjs` |
| `.stylelintignore` | `{项目根}/.stylelintignore` |
| `.ls-lint.yml` | `{项目根}/.ls-lint.yml` |
| `.commitlintrc.js` | `{项目根}/.commitlintrc.js` |
| `.lintstagedrc.cjs` | `{项目根}/.lintstagedrc.cjs` |
| `postcss.config.js` | `{项目根}/postcss.config.js` |
| `.vscode/settings.json` | `{项目根}/.vscode/settings.json` |

### 步骤 5: 配置 vite.config.ts

替换为包含以下配置的版本：
- `@vitejs/plugin-react` 插件
- Less 预处理器（`javascriptEnabled: true`）
- 路径别名（`@ → ./src`）
- 开发代理（`/development` → 本地后端）

参考 [references/simple-project.md](references/simple-project.md) 中的完整配置。

### 步骤 6: 配置 tsconfig.app.json

在 `compilerOptions` 中添加路径别名：

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

### 步骤 7: 清理脚手架默认文件 + 创建 src/ 目录结构

**清理**：删除 Vite 脚手架生成的不需要的文件：

```bash
rm -f src/App.css src/index.css public/vite.svg src/assets/react.svg
```

src/ 下只保留 `App.tsx` 和 `main.tsx`，删除其他脚手架生成的文件（如 `App.css`、`index.css`）。

**生成网站图标**：根据项目内容生成一个 SVG 图标，放置到 `public/favicon.svg`，同时更新 `index.html` 中的 `<link rel="icon">` 指向新图标。

**编写 README.md**：覆盖脚手架默认的 README.md，根据实际项目内容编写，包含项目简介、技术栈、启动方式、目录结构等。

**创建目录结构**：

**简单项目**：读取 [references/simple-project.md](references/simple-project.md) 中的目录结构，创建所有目录。

**复杂项目**：读取 [references/complex-project.md](references/complex-project.md) 中的目录结构，创建 core/ + system/ + router/ 结构。

### 步骤 8: 复制封装代码

从 `assets/src/` 复制模板文件到项目 `src/` 对应位置：

**简单项目**:

| 源文件 | 目标 |
|--------|------|
| `constants/app.constants.ts` | `src/constants/app.constants.ts` |
| `constants/http-status.enum.ts` | `src/constants/http-status.enum.ts` |
| `types/api.ts` | `src/types/api.ts` |
| `types/router.ts` | `src/types/router.ts` |
| `services/index.ts` | `src/services/index.ts` |
| `router/index.tsx` | `src/router/index.tsx` |
| `router/init.tsx` | `src/router/init.tsx` |

**复杂项目**:

将文件复制到 `src/core/` 下对应路径，并参考 [references/complex-project.md](references/complex-project.md) 替换路由为动态发现版本。

### 步骤 9: 配置 Tailwind 入口

创建 `src/assets/styles/index.less`：

```css
@import (css) 'tailwindcss';
```

在 `src/App.tsx` 中引入：

```typescript
import '@/assets/styles/index.less';
```

### 步骤 10: 初始化 Husky + Git Hooks

```bash
git init
npx husky-init && yarn
yarn husky add .husky/pre-commit 'yarn lint-staged'
yarn husky add .husky/commit-msg 'yarn commitlint'
```

### 步骤 11: 配置 package.json scripts

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

### 步骤 12: 格式化 + 验证

初始化完成后，先执行一次全量格式化，消除脚手架和模板代码的格式差异：

```bash
yarn lint:prettier
```

然后验证：

1. `yarn dev` — 开发服务器正常启动
2. `yarn lint:eslint` — 无报错
3. `yarn build` — 构建成功

---

## 阶段二：开发指导（Guide）

当用户在已有 React 项目中添加功能时，按以下规范指导。

### 添加新页面

1. 在 `src/pages/{页面名}/` 下创建 `index.tsx`
2. 注册路由：
   - 简单项目：在 `src/router/index.tsx` 的 children 中添加
   - 复杂项目：在对应模块的 `routes.ts` 中添加
3. 页面组件不超过 800 行

```tsx
// src/pages/user/index.tsx
const UserPage = () => {
  return <div>用户页面</div>;
};

export default UserPage;
```

### 添加新组件

组件分三类：

| 类型 | 目录 | 说明 |
|------|------|------|
| 业务组件 | `components/business/` | 特定业务逻辑 |
| 综合组件 | `components/complex/` | 可复用的复合组件 |
| 布局组件 | `components/layout/` | 页面布局结构 |

命名规范：
- 文件名：**PascalCase**（如 `UserList.tsx`）或 **kebab-case**（如 `user-list.tsx`）
- 组件名：**PascalCase**（如 `UserList`）
- 样式文件：与组件同名（如 `user-list.less`）

### 添加新 API 服务

1. 在 `src/types/{模块}/{实体}/` 下定义类型：
   - `{entity}.d.ts` — 实体对象
   - `{entity}.dto.d.ts` — 数据传输对象（请求参数）
   - `{entity}.vo.d.ts` — 视图对象（响应数据）
2. 在 `src/services/{模块}/` 下创建服务文件
3. 服务只做 API 调用，不包含业务逻辑

```typescript
// src/services/admin/user.ts
import { post } from '@/services';
import type { ResultVO } from '@/types/api';
import type { UserQueryDTO } from '@/types/admin/user/user.dto';
import type { UserVO } from '@/types/admin/user/user.vo';

export const userService = {
  page: (query: UserQueryDTO): Promise<ResultVO<UserVO[]>> => {
    return post('/user/page', query);
  },
};
```

### 添加新模块（仅复杂项目）

参考 [references/complex-project.md](references/complex-project.md)：

1. 在 `src/system/{模块名}/` 下创建标准目录结构
2. 创建 `routes.ts` 导出 `ModuleRouteConfig`
3. 路由会被 `import.meta.glob` 自动发现

### 全局加载状态

**两层 Loading 规范**：

**层 1：全局路由切换 Loading**（App.tsx）

用 `React.Suspense` 包裹 `RouterProvider`，路由懒加载时自动展示全屏 Loading：

```tsx
// src/App.tsx
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

路由文件中使用 `lazy()` 做代码分割，配合 Suspense 触发 Loading：

```tsx
// src/router/index.tsx
import { lazy } from 'react';
const HomePage = lazy(() => import('@/pages/home'));
```

**层 2：页面内数据加载 Loading**

页面初始加载数据时，在内容区居中展示 Spin，避免空白闪烁：

```tsx
// src/pages/orders/index.tsx
const OrdersPage = () => {
  const [loading, setLoading] = useState(true);
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    orderService.list().then(res => {
      setOrders(res.data);
    }).finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 400 }}>
        <Spin size="large" />
      </div>
    );
  }

  return <div>{/* 页面内容 */}</div>;
};
```

### 命名约定

| 类型 | 约定 | 示例 |
|------|------|------|
| 文件名 | kebab-case 或 PascalCase | `user-list.tsx` 或 `UserList.tsx` |
| 组件名 | PascalCase | `UserList` |
| Hook | use + PascalCase | `useChatState` |
| 类型文件 | kebab-case + 后缀 | `user.d.ts`、`user.dto.d.ts` |
| 常量文件 | kebab-case | `app.constants.ts` |
| 样式文件 | kebab-case | `user-list.less` |

### 分层原则

| 层 | 目录 | 职责 | 约束 |
|-----|------|------|------|
| 页面 | `pages/` | 页面容器，组合组件和 Hooks | ≤ 800 行 |
| 组件 | `components/` | UI 展示，接收 Props | 可复用 |
| Hooks | `hooks/` | 逻辑抽取，状态管理 | 无 UI |
| 服务 | `services/` | API 调用 | 无业务逻辑 |
| 类型 | `types/` | TypeScript 类型定义 | 按模块/实体组织 |
| 常量 | `constants/` | 常量和枚举 | 不可变 |

---

## 阶段三：代码审查（Review）

当用户要求审查项目时，按以下清单检查。

### 结构检查

- [ ] src/ 目录结构是否符合规范（简单/复杂项目对应结构）
- [ ] 配置文件是否齐全（eslint、prettier、stylelint、ls-lint、commitlint、lint-staged、postcss、husky）
- [ ] vite.config.ts 是否包含别名配置和代理配置
- [ ] tsconfig.app.json 是否包含路径别名

### 命名检查

- [ ] 文件名是否符合 kebab-case 或 PascalCase 约定
- [ ] 组件名是否使用 PascalCase
- [ ] Hook 是否以 use 开头
- [ ] 类型文件是否使用正确后缀（.d.ts / .dto.d.ts / .vo.d.ts）

### 代码质量

- [ ] 组件文件行数 ≤ 800 行
- [ ] 服务层无业务逻辑（只做 API 调用）
- [ ] 不硬编码颜色值（使用 Tailwind 类名或 Antd 主题）
- [ ] 路由正确注册（简单项目在 index.tsx，复杂项目在模块 routes.ts）
- [ ] 类型定义完整（请求/响应都有类型）

### 配置一致性

- [ ] eslint.config.js 内容与模板一致
- [ ] .prettierrc 内容与模板一致
- [ ] package.json scripts 是否包含所有 lint 脚本
