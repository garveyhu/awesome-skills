"""
两个端点：
1. POST /xxx-async     — 启动任务，立即返回 task_id
2. GET  /task/{id}/status — 查询进度（所有 task 类型共用）

共用的 status 端点是亮点：task_id 全局唯一，不管是哪种业务任务都用同一个查询接口。
"""

from typing import Optional

# ADAPT: 替换为你项目的 Web 框架导入
from fastapi import APIRouter, Depends, File, Form, UploadFile

# ADAPT: 替换为项目的响应封装、权限、上下文
from app.auth import PermissionChecker
from app.context import get_current_space_id
from app.response import Result

from .backend_task_manager import async_task_manager
from .backend_worker import ImportService

router = APIRouter(prefix="/api/xxx", tags=["XXX"])  # ADAPT: 前缀


@router.post(
    "/import-async",
    response_model=Result,
    dependencies=[Depends(PermissionChecker("xxx:write"))],  # ADAPT: 权限
)
async def import_async(
    file: UploadFile = File(...),
    datasource_id: Optional[int] = Form(None),
):
    """异步导入：立即返回 task_id，前端轮询 /task/{task_id}/status。"""
    space_id = get_current_space_id()

    try:
        content = await file.read()
    except Exception as e:
        return Result.fail(f"无法读取上传文件: {e}")

    task_id = ImportService.import_async(
        file_bytes=content,
        space_id=space_id,
        datasource_id=datasource_id,
    )
    return Result.ok({"task_id": task_id, "message": "任务已启动"})


# 查询进度端点：所有 task 类型共用一个
# ADAPT: 可以放在任何 router 下，只要路径固定即可
@router.get("/task/{task_id}/status", response_model=Result)
def get_task_status(task_id: str):
    task = async_task_manager.get_task(task_id)
    if not task:
        return Result.fail("任务不存在或已过期")
    return Result.ok(task.to_dict())
