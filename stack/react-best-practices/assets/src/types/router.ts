import type { ComponentType, LazyExoticComponent } from 'react';

export interface RouteMeta {
  title?: string;
  auth?: boolean;
  roles?: string[];
  forbidRepeatLogin?: boolean;
  hidden?: boolean;
}

export interface RouteConfig {
  path?: string;
  index?: boolean;
  component: LazyExoticComponent<ComponentType<any>>;
  children?: RouteConfig[];
  meta?: RouteMeta;
  redirect?: string;
  guard?: string;
}

export interface ModuleRouteConfig {
  moduleId: string;
  parentPath?: string;
  routes: RouteConfig[];
}
