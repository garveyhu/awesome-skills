"""
AsyncTaskManager — 进程内单例，管理长耗时任务的状态与进度。

设计要点：
- 单例 + 线程安全初始化（双重检查）
- 任务状态存在进程内 dict；不引入 Redis 等外部依赖
- 后台执行用 threading.Thread(daemon=True)；主进程退出时任务自动终止
- 任务超过上限时删除最旧的一半，内存不会无限增长

生产环境扩展：
- 多进程部署：把 self._tasks 替换成 Redis（接口保持不变）
- 需要取消：加 cancel_event 传给 worker，worker 里定期检查
"""

import threading
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, Optional


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class TaskProgress:
    total: int = 0
    processed: int = 0
    current_item: str = ""

    @property
    def percentage(self) -> float:
        if self.total == 0:
            return 0
        return round(self.processed / self.total * 100, 1)


@dataclass
class AsyncTask:
    task_id: str
    task_type: str  # ADAPT: 业务类型字符串，便于日志和查询
    status: TaskStatus = TaskStatus.PENDING
    progress: TaskProgress = field(default_factory=TaskProgress)
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "task_type": self.task_type,
            "status": self.status.value,
            "progress": {
                "total": self.progress.total,
                "processed": self.progress.processed,
                "current_item": self.progress.current_item,
                "percentage": self.progress.percentage,
            },
            "result": self.result,
            "error": self.error,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }


class AsyncTaskManager:
    """进程内单例任务管理器"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._tasks: Dict[str, AsyncTask] = {}
                    cls._instance._max_tasks = 100
        return cls._instance

    def create_task(self, task_type: str) -> AsyncTask:
        task_id = str(uuid.uuid4())[:8]
        task = AsyncTask(task_id=task_id, task_type=task_type)
        self._cleanup_old_tasks()
        self._tasks[task_id] = task
        return task

    def get_task(self, task_id: str) -> Optional[AsyncTask]:
        return self._tasks.get(task_id)

    def update_progress(
        self,
        task_id: str,
        processed: Optional[int] = None,
        total: Optional[int] = None,
        current_item: Optional[str] = None,
    ):
        """按需更新进度字段。传 None 的字段不动。

        关键约定：processed 必须单调递增。只有真正耗时的阶段才更新它，
        否则会出现"进度先冲到 100% 再重置"的 bug（见 README 陷阱 1）。
        """
        task = self._tasks.get(task_id)
        if task:
            if total is not None:
                task.progress.total = total
            if processed is not None:
                task.progress.processed = processed
            if current_item is not None:
                task.progress.current_item = current_item

    def start_task(self, task_id: str, total: int = 0):
        task = self._tasks.get(task_id)
        if task:
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.now()
            task.progress.total = total

    def complete_task(self, task_id: str, result: Optional[Dict[str, Any]] = None):
        task = self._tasks.get(task_id)
        if task:
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()
            task.result = result
            task.progress.processed = task.progress.total  # 保证 100%

    def fail_task(self, task_id: str, error: str):
        task = self._tasks.get(task_id)
        if task:
            task.status = TaskStatus.FAILED
            task.completed_at = datetime.now()
            task.error = error

    def run_in_background(self, task_id: str, func: Callable, *args, **kwargs):
        """在 daemon 线程跑 worker。worker 异常会自动 fail_task。"""

        def wrapper():
            try:
                func(task_id, *args, **kwargs)
            except Exception as e:
                self.fail_task(task_id, str(e))

        thread = threading.Thread(target=wrapper, daemon=True)
        thread.start()

    def _cleanup_old_tasks(self):
        if len(self._tasks) >= self._max_tasks:
            sorted_tasks = sorted(self._tasks.items(), key=lambda x: x[1].created_at)
            for task_id, _ in sorted_tasks[: len(sorted_tasks) // 2]:
                del self._tasks[task_id]


# 全局单例（import 即可用）
async_task_manager = AsyncTaskManager()
