import { lazy } from 'react';

import type { RouteConfig } from '@/types/router';

const routes: RouteConfig[] = [
  {
    path: '/',
    component: lazy(() => import('@/components/layout/MainLayout')),
    meta: { auth: true },
    children: [
      {
        index: true,
        redirect: '/home',
        component: lazy(() => import('@/pages/home')),
      },
      // 在此添加更多页面路由
      // {
      //   path: '/example',
      //   component: lazy(() => import('@/pages/example')),
      //   meta: { title: '示例页面' },
      // },
    ],
  },
  {
    path: '/login',
    component: lazy(() => import('@/pages/login')),
    meta: { auth: false, forbidRepeatLogin: true },
  },
  {
    path: '*',
    component: lazy(() => import('@/pages/404')),
    meta: { title: '404', auth: false },
  },
];

export default routes;
