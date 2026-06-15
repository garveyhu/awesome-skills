// ADAPT: 替换导入路径 + 请求封装
import { get, postFormData } from '@/core/utils/request';
import type { ResultVO } from '@/core/types/api';
import type { AsyncTask, AsyncTaskStartResponse } from './frontend-types';

export const asyncTaskApi = {
  /**
   * 启动异步导入任务
   * ADAPT: 替换端点路径
   */
  startImport: (file: File, datasourceId?: number) => {
    const formData = new FormData();
    formData.append('file', file);
    if (datasourceId) formData.append('datasource_id', String(datasourceId));
    return postFormData<ResultVO<AsyncTaskStartResponse>>(
      '/api/xxx/import-async',
      formData,
    );
  },

  /**
   * 查询任务进度（所有 task 类型共用）
   * ADAPT: 如果你的状态端点路径不同，改这里
   */
  getTaskStatus: <TResult = Record<string, unknown>>(taskId: string) => {
    return get<ResultVO<AsyncTask<TResult>>>(`/api/xxx/task/${taskId}/status`);
  },
};
