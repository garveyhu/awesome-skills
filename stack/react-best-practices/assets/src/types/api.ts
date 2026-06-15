/**
 * 通用 API 类型定义
 */

/**
 * 标准响应结构
 */
export interface ResultVO<T = any> {
  success: boolean;
  code?: number;
  message?: string;
  data: T;
}

/**
 * 分页请求参数
 */
export interface PaginationParams {
  page?: number;
  pageSize?: number;
}

/**
 * 分页响应
 */
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
}

/**
 * 时间范围参数
 */
export interface TimeRangeParams {
  startTime?: string;
  endTime?: string;
  days?: number;
}
