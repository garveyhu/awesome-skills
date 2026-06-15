import { message } from 'antd';
import axios from 'axios';
import type { AxiosRequestConfig, AxiosResponse, InternalAxiosRequestConfig } from 'axios';
import humps from 'humps';

import {
  API_CONFIG,
  AUTH_CONFIG,
  ENV_CONFIG,
  ERROR_MESSAGES,
} from '@/constants/app.constants';
import { HttpStatus } from '@/constants/http-status.enum';
import type { ResultVO } from '@/types/api';

const isPrd = import.meta.env.PROD;
export const basicUrl = isPrd ? ENV_CONFIG.PRODUCTION_URL : ENV_CONFIG.DEVELOPMENT_URL;

const service = axios.create({
  baseURL: basicUrl,
  timeout: API_CONFIG.TIMEOUT,
  headers: {
    'Content-Type': API_CONFIG.CONTENT_TYPE,
  },
});

const clearAuthAndRedirect = () => {
  window.localStorage.removeItem(AUTH_CONFIG.USER_TOKEN_KEY);
  window.localStorage.removeItem(AUTH_CONFIG.USER_INFO_KEY);
  window.sessionStorage.removeItem(AUTH_CONFIG.USER_TOKEN_KEY);
  window.sessionStorage.removeItem(AUTH_CONFIG.USER_INFO_KEY);

  const baseUrl = import.meta.env.BASE_URL || '/';
  const loginPath = `${baseUrl}login`.replace(/\/+/g, '/');

  if (!window.location.pathname.endsWith('/login')) {
    window.location.href = loginPath;
  } else {
    window.location.reload();
  }
};

service.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token =
      window.localStorage.getItem(AUTH_CONFIG.USER_TOKEN_KEY) ||
      window.sessionStorage.getItem(AUTH_CONFIG.USER_TOKEN_KEY);

    if (token) {
      config.headers = config.headers || {};
      config.headers[AUTH_CONFIG.AUTHORIZATION_HEADER] = `${AUTH_CONFIG.TOKEN_PREFIX} ${token}`;
    }

    // 自动将请求数据从 camelCase 转换为 snake_case（后端 Python 规范）
    if (config.data && typeof config.data === 'object') {
      config.data = humps.decamelizeKeys(config.data);
    }
    if (config.params && typeof config.params === 'object') {
      config.params = humps.decamelizeKeys(config.params);
    }

    return config;
  },
  error => {
    return Promise.reject(error);
  },
);

service.interceptors.response.use(
  (response: AxiosResponse<ResultVO>) => {
    // 自动将响应数据从 snake_case 转换为 camelCase（前端 JS 规范）
    const responseData = humps.camelizeKeys(response.data) as ResultVO;
    const { code, message: msg } = responseData;

    if (code && code !== HttpStatus.SUCCESS.code && code !== HttpStatus.OK.code) {
      if (response.config?.headers?.['X-Skip-Global-Error'] === 'true') {
        return responseData as any;
      }

      if (code === HttpStatus.UNAUTHORIZED.code) {
        clearAuthAndRedirect();
      }

      message.error(msg || ERROR_MESSAGES.REQUEST_FAILED);
      return Promise.reject(new Error(msg || ERROR_MESSAGES.REQUEST_FAILED));
    }

    return responseData as any;
  },
  error => {
    if (error.config?.headers?.['X-Skip-Global-Error'] === 'true') {
      return Promise.reject(error);
    }

    const status = error.response?.status;
    const serverMessage = error.response?.data?.message;
    const statusEntry = status
      ? Object.values(HttpStatus).find(item => item.code === status)
      : null;

    if (status === HttpStatus.UNAUTHORIZED.code) {
      clearAuthAndRedirect();
    }

    message.error(serverMessage || statusEntry?.message || ERROR_MESSAGES.UNKNOWN_ERROR);
    return Promise.reject(error);
  },
);

export function get<T = any>(url: string, params?: any, config?: AxiosRequestConfig): Promise<T> {
  return request<T>({
    method: 'get',
    url,
    params,
    ...config,
  });
}

export function post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
  return request<T>({
    method: 'post',
    url,
    data,
    ...config,
  });
}

export function request<T = any>(config: AxiosRequestConfig): Promise<T> {
  return service(config).then(res => res as T);
}

export default service;
