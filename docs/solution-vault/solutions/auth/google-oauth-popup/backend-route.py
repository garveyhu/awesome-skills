"""
Google OAuth 路由 — 登录 + 绑定

两个端点：
- POST /auth/google      — Google 登录（无需登录态）
- POST /auth/google/bind  — 绑定 Google 到已登录用户（需登录态）
"""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# ADAPT: 替换为你的依赖注入
from app.database import get_db
from app.services.auth_service import AuthService
# ADAPT: 替换为你的响应封装
from app.response import Result

from .google_auth_dto import GoogleLoginDTO
from .google_auth_service import GoogleAuthService

# ADAPT: 替换为你的路由前缀和认证依赖
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/google")
def google_login(dto: GoogleLoginDTO, db: Annotated[Session, Depends(get_db)]) -> dict:
    """Google 登录：验证 access_token，查找或创建用户，返回 JWT。"""
    user, access_token, is_new_user = GoogleAuthService.google_login(db, dto.access_token)
    # ADAPT: 替换为你的用户序列化逻辑
    roles = AuthService.get_roles(db, user.id)
    return Result.ok(
        {
            "access_token": access_token,
            "user": {
                "id": user.id,
                "email": user.email,
                "nickname": user.nickname,
                "avatar_url": user.avatar_url,
                "roles": roles,
            },
            "is_new_user": is_new_user,
        }
    )


@router.post("/google/bind")
def google_bind(
    dto: GoogleLoginDTO,
    # ADAPT: 替换为你的"获取当前登录用户"依赖
    user: Annotated[object, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> dict:
    """绑定 Google 到已登录用户。"""
    updated = GoogleAuthService.bind_google(db, user, dto.access_token)
    # ADAPT: 替换为你的用户详情序列化
    return Result.ok(get_full_profile(db, updated))
