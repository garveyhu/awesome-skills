// 环境配置
export const ENV_CONFIG = {
  PRODUCTION_URL: '/production',
  DEVELOPMENT_URL: '/development',
} as const;

// API 配置
export const API_CONFIG = {
  TIMEOUT: 60000,
  CONTENT_TYPE: 'application/json;charset=UTF-8',
} as const;

// 认证配置
export const AUTH_CONFIG = {
  AUTHORIZATION_HEADER: 'Authorization',
  TOKEN_PREFIX: 'Bearer',
  USER_TOKEN_KEY: 'user_token',
  USER_INFO_KEY: 'user_info',
  LOGIN_REDIRECT: '/login',
} as const;

// 错误消息
export const ERROR_MESSAGES = {
  REQUEST_FAILED: '请求失败',
  REQUEST_TIMEOUT: '请求超时',
  NETWORK_ERROR: '网络错误',
  UNKNOWN_ERROR: 'Error',
} as const;
