import React from 'react';
import { Navigate, type RouteObject } from 'react-router-dom';

import { AUTH_CONFIG } from '@/constants/app.constants';
import type { RouteConfig, RouteMeta } from '@/types/router';

import routes from './index';

export function init(): RouteObject[] {
  return transformRoutes(routes);
}

function transformRoutes(list: RouteConfig[]): RouteObject[] {
  return list.map(item => {
    const route: Partial<RouteObject> = {};

    if (item.redirect) {
      route.element = <Navigate to={item.redirect} replace />;
    } else {
      route.element = (
        <RouteWrapper component={item.component} meta={item.meta} />
      );
    }

    if (item.index) {
      route.index = true;
    } else if (item.path) {
      route.path = item.path;
    }

    if (item.children) {
      route.children = transformRoutes(item.children);
    }

    return route;
  }) as RouteObject[];
}

interface RouteWrapperProps {
  component: React.LazyExoticComponent<React.ComponentType<any>>;
  meta?: RouteMeta;
}

const RouteWrapper: React.FC<RouteWrapperProps> = ({ component: Component, meta }) => {
  React.useEffect(() => {
    if (meta?.title) {
      document.title = meta.title;
    }
  }, [meta?.title]);

  // 认证校验
  if (meta?.auth && !isAuthenticated()) {
    return <Navigate to={AUTH_CONFIG.LOGIN_REDIRECT} replace />;
  }
  if (meta?.forbidRepeatLogin && isAuthenticated()) {
    return <Navigate to="/" replace />;
  }

  return <Component />;
};

function isAuthenticated(): boolean {
  return (
    !!sessionStorage.getItem(AUTH_CONFIG.USER_TOKEN_KEY) ||
    !!localStorage.getItem(AUTH_CONFIG.USER_TOKEN_KEY)
  );
}

export default init;
