# 复杂项目规范（多模块）

## 目录

1. [多模块 src/ 目录结构](#多模块-src-目录结构)
2. [动态路由发现](#动态路由发现)
3. [模块路由文件示例](#模块路由文件示例)
4. [请求封装完整版](#请求封装完整版)
5. [状态管理模式](#状态管理模式)
6. [Context 层设计](#context-层设计)
7. [组件分层](#组件分层)
8. [模块自注册模式](#模块自注册模式)

---

## 多模块 src/ 目录结构

```
src/
├── core/                            # 核心框架（所有模块共享）
│   ├── assets/                     # 静态资源（样式、字体、图片）
│   │   └── styles/
│   │       └── index.less          # 全局样式
│   ├── components/                 # 核心组件
│   │   ├── auth/                  # 认证组件（Login、RoleGuard）
│   │   ├── common/                # 通用工具组件（Loading、Modal）
│   │   └── layout/                # 布局组件（MainLayout、Menu）
│   ├── constants/                 # 应用常量（API配置、认证设置）
│   │   ├── app.constants.ts
│   │   └── http-status.enum.ts
│   ├── context/                   # React Context
│   ├── hooks/                     # 共享 Hooks
│   ├── pages/                     # 核心页面（404）
│   ├── services/                  # 核心 API
│   ├── types/                     # 核心类型定义（api、router）
│   │   ├── api.ts
│   │   └── router.ts
│   └── utils/                     # 工具函数（request、theme）
│       └── request.ts             # HTTP 请求封装
│
├── system/                         # 系统模块（按功能组织）
│   ├── auth/                      # 认证模块
│   │   ├── components/            # 模块组件
│   │   ├── pages/                 # 模块页面
│   │   ├── services/              # 模块 API
│   │   ├── types/                 # 模块类型
│   │   └── routes.ts              # 模块路由（自动发现）
│   ├── admin/                     # 管理模块
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── types/
│   │   └── routes.ts
│   └── {module-name}/             # 其他业务模块...
│       ├── components/
│       ├── hooks/                 # 模块级 Hooks
│       ├── pages/
│       ├── services/
│       ├── types/
│       └── routes.ts
│
├── router/                         # 路由（动态发现）
│   ├── index.ts                   # 路由构建（import.meta.glob）
│   └── init.tsx                   # 路由初始化（RouteWrapper）
│
├── App.tsx                         # 根组件
└── main.tsx                        # 入口文件
```

### 核心原则

- `core/` 不依赖任何 `system/` 模块，只提供基础设施
- `system/` 每个模块自包含：组件、页面、服务、类型、路由
- 模块间通信通过 Context 或事件总线，不直接 import

## 动态路由发现

使用 Vite 的 `import.meta.glob` 自动发现所有模块的路由文件：

```typescript
// src/router/index.ts
import { lazy } from 'react';

import type { ModuleRouteConfig, RouteConfig } from '@/core/types/router';

// 自动导入所有模块的路由
const routeModules = import.meta.glob<
  { default: ModuleRouteConfig } | { [key: string]: ModuleRouteConfig }
>(['../system/**/routes.ts'], { eager: true });

// 收集所有模块路由
const moduleRoutes: ModuleRouteConfig[] = [];

for (const path in routeModules) {
  const module = routeModules[path];

  if ('default' in module) {
    moduleRoutes.push(module.default);
  } else {
    for (const key in module) {
      const value = module[key];
      if (value && typeof value === 'object' && 'moduleId' in value && 'routes' in value) {
        moduleRoutes.push(value as ModuleRouteConfig);
        break;
      }
    }
  }
}

// 按 parentPath 分组
function groupRoutesByParent(modules: ModuleRouteConfig[]): Map<string, RouteConfig[]> {
  const groups = new Map<string, RouteConfig[]>();

  for (const module of modules) {
    const parentPath = module.parentPath ?? '/';
    const existing = groups.get(parentPath) || [];
    groups.set(parentPath, [...existing, ...module.routes]);
  }

  return groups;
}

// 构建最终路由树
export function buildRoutes(): RouteConfig[] {
  const grouped = groupRoutesByParent(moduleRoutes);

  const routes: RouteConfig[] = [
    {
      path: '/',
      component: lazy(() => import('@/core/components/layout/MainLayout')),
      meta: { auth: true },
      children: [
        {
          index: true,
          redirect: '/home',
          component: lazy(() => import('@/core/pages/NotFound')),
        },
        ...(grouped.get('/') || []),
      ],
    },
    ...(grouped.get('') || []),
    {
      path: '*',
      component: lazy(() => import('@/core/pages/NotFound')),
      meta: { title: '404', auth: false },
    },
  ];

  return routes;
}

export { moduleRoutes };
export default buildRoutes;
```

路由初始化 `init.tsx` 与简单项目一致，只是改为调用 `buildRoutes()` 而非静态导入。

## 模块路由文件示例

每个模块导出一个 `ModuleRouteConfig`：

```typescript
// src/system/admin/routes.ts
import { lazy } from 'react';

import type { ModuleRouteConfig } from '@/core/types/router';

const adminRoutes: ModuleRouteConfig = {
  moduleId: 'admin',
  parentPath: '/',
  routes: [
    {
      path: '/admin/users',
      component: lazy(() => import('./pages/user-list')),
      meta: { title: '用户管理', auth: true, roles: ['admin'] },
    },
    {
      path: '/admin/roles',
      component: lazy(() => import('./pages/role-list')),
      meta: { title: '角色管理', auth: true, roles: ['admin'] },
    },
  ],
};

export default adminRoutes;
```

无 parent 的路由（如登录页）设置 `parentPath: ''`：

```typescript
// src/system/auth/routes.ts
import { lazy } from 'react';

import type { ModuleRouteConfig } from '@/core/types/router';

const authRoutes: ModuleRouteConfig = {
  moduleId: 'auth',
  parentPath: '',
  routes: [
    {
      path: '/login',
      component: lazy(() => import('./pages/login')),
      meta: { auth: false, forbidRepeatLogin: true },
    },
  ],
};

export default authRoutes;
```

## 请求封装完整版

复杂项目在简单版本基础上增加以下能力：

### humps URL 排除规则

某些 API 返回的字段需要保留原始 key（如数据库字段名），通过 URL 匹配排除：

```typescript
// src/core/utils/humps-exclusions.ts
import humps from 'humps';

// 定义需要排除 camelCase 转换的 URL 和字段
const exclusionRules: Record<string, string[]> = {
  '/data/query': ['column_name', 'table_name'],
  '/data/schema': ['*'], // 排除所有字段
};

export function createCamelizeForUrl(url?: string): (data: any) => any {
  if (!url) return humps.camelizeKeys;

  const matchedRule = Object.entries(exclusionRules).find(([pattern]) =>
    url.includes(pattern)
  );

  if (!matchedRule) return humps.camelizeKeys;

  const [, excludeFields] = matchedRule;

  if (excludeFields.includes('*')) {
    return (data: any) => data; // 不转换
  }

  return (data: any) =>
    humps.camelizeKeys(data, (key, convert) =>
      excludeFields.includes(key) ? key : convert(key)
    );
}
```

### 请求封装中使用

```typescript
// 在 response interceptor 中替换 humps.camelizeKeys
import { createCamelizeForUrl } from './humps-exclusions';

// response interceptor
const camelize = createCamelizeForUrl(response.config?.url);
const responseData = camelize(response.data) as ResultVO;
```

## 状态管理模式

复杂项目使用 **Hooks-based 状态管理**（无 Redux/Zustand），按职责拆分：

### 模式：三 Hook 拆分

```
useXxxState     → 核心状态（所有 useState、useRef）
useXxxSession   → 数据加载（API 调用、缓存管理）
useXxxAction    → 用户操作（发送、删除、更新等副作用）
```

### 示例

```typescript
// hooks/use-chat-state.ts
export function useChatState() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [currentSession, setCurrentSession] = useState<string | null>(null);

  // Refs 用于高频更新（避免不必要的 re-render）
  const messagesRef = useRef(messages);
  messagesRef.current = messages;

  return {
    messages, setMessages,
    loading, setLoading,
    currentSession, setCurrentSession,
    messagesRef,
  };
}
```

```typescript
// hooks/use-chat-session.ts
export function useChatSession(state: ReturnType<typeof useChatState>) {
  const loadSession = useCallback(async (sessionId: string) => {
    state.setLoading(true);
    try {
      const [config, messages] = await Promise.all([
        chatApi.getConfig(sessionId),
        chatApi.getMessages(sessionId),
      ]);
      state.setMessages(messages.data);
      state.setCurrentSession(sessionId);
    } finally {
      state.setLoading(false);
    }
  }, []);

  return { loadSession };
}
```

```typescript
// hooks/use-chat-action.ts
export function useChatAction(state: ReturnType<typeof useChatState>) {
  const sendMessage = useCallback(async (content: string) => {
    // 乐观更新
    const tempMessage = createTempMessage(content);
    state.setMessages(prev => [...prev, tempMessage]);

    const response = await chatApi.send({ content, sessionId: state.currentSession });
    // 替换临时消息为真实消息
    state.setMessages(prev =>
      prev.map(m => m.id === tempMessage.id ? response.data : m)
    );
  }, [state.currentSession]);

  return { sendMessage };
}
```

### 在页面中组合

```tsx
function ChatPage() {
  const state = useChatState();
  const { loadSession } = useChatSession(state);
  const { sendMessage } = useChatAction(state);

  return <div>...</div>;
}
```

## Context 层设计

### 何时使用 Context

| 场景 | 方案 |
|------|------|
| 全局配置（主题、语言） | Context |
| 跨组件共享的认证状态 | Context |
| 页面内状态 | Hooks（不需要 Context） |
| 组件间数据传递 | Props（优先）或 Context |

### Context 示例

```tsx
// src/core/context/AuthContext.tsx
interface AuthContextType {
  user: User | null;
  login: (token: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  const login = useCallback((token: string) => {
    localStorage.setItem(AUTH_CONFIG.USER_TOKEN_KEY, token);
    // 获取用户信息...
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem(AUTH_CONFIG.USER_TOKEN_KEY);
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
}
```

## 组件分层

```
src/
├── core/components/               # 全局共享组件
│   ├── auth/                     # 认证相关
│   ├── common/                   # 通用工具（Loading、Modal、ConfirmDialog）
│   └── layout/                   # 布局（MainLayout、Sidebar、Header）
│
└── system/{module}/components/    # 模块私有组件
    ├── XxxList.tsx               # 列表组件
    ├── XxxForm.tsx               # 表单组件
    └── XxxDetail.tsx             # 详情组件
```

### 规则

- **core/components/**: 至少被 2 个以上模块使用才放这里
- **system/{module}/components/**: 只在本模块内使用的组件
- 组件文件不超过 **800 行**，超过则拆分为子组件或抽取 Hook

## 模块自注册模式

每个模块通过 `index.ts` 导出 manifest，在 `main.tsx` 中统一注册：

```typescript
// src/system/admin/index.ts
export const adminModule = {
  id: 'admin',
  name: '系统管理',
  routes: () => import('./routes'),
};
```

```typescript
// src/main.tsx
import { adminModule } from '@/system/admin';
import { authModule } from '@/system/auth';

const modules = [adminModule, authModule];

// 模块初始化逻辑...
```

注意：如果使用了动态路由发现（import.meta.glob），路由注册是自动的，`index.ts` 的 manifest 主要用于模块元信息（名称、图标、权限等）。
