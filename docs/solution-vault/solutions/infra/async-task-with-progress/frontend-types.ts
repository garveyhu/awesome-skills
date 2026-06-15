// ADAPT: 放到你项目的 types 目录。与后端 task.to_dict() 结构对齐。
// 注意：用 camelCase（假设项目用 humps 或类似的自动 case 转换）

export type TaskStatus = 'pending' | 'running' | 'completed' | 'failed';

export interface TaskProgress {
  total: number;
  processed: number;
  currentItem: string;
  percentage: number;
}

export interface AsyncTask<TResult = Record<string, unknown>> {
  taskId: string;
  taskType: string;
  status: TaskStatus;
  progress: TaskProgress;
  result?: TResult;
  error?: string;
  createdAt?: string;
  startedAt?: string;
  completedAt?: string;
}

export interface AsyncTaskStartResponse {
  taskId: string;
  message: string;
}
