"""
Google OAuth Service — token 验证、用户查找/创建、账号绑定

核心逻辑：
1. 用 access_token 调 Google userinfo API 获取用户信息
2. 按 google_id → email 顺序查找用户，找不到则创建
3. 支持已登录用户绑定 Google 账号
"""

import requests
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

# ADAPT: 替换为你的 User 模型和相关模型的导入路径
from app.models import User, UserRole
# ADAPT: 替换为你的认证服务（提供 create_access_token、ensure_default_role 等方法）
from app.services.auth_service import AuthService

OAUTH_NO_PASSWORD = "OAUTH_NO_PASSWORD"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"


class GoogleAuthService:
    @staticmethod
    def fetch_google_user(access_token: str) -> dict:
        """用 access_token 调用 Google userinfo API 获取用户信息。

        返回 dict 包含: sub, email, name, picture 等字段。
        """
        resp = requests.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10,
        )
        if resp.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Google access token",
            )
        return resp.json()

    @staticmethod
    def find_or_create_user(
        db: Session, google_id: str, email: str, name: str, picture: str | None
    ) -> tuple[User, bool]:
        """按 google_id 或 email 查找用户，找不到则创建。返回 (user, is_new_user)。"""
        # 先按 google_id 查找（已绑定的用户）
        user = db.query(User).filter(User.google_id == google_id).first()
        if user:
            return user, False

        # 再按 email 查找（已有邮箱密码用户 → 自动关联）
        user = db.query(User).filter(User.email == email).first()
        if user:
            user.google_id = google_id
            if not user.avatar_url and picture:
                user.avatar_url = picture
            db.commit()
            db.refresh(user)
            return user, False

        # 创建新用户
        # ADAPT: 替换为你的用户创建逻辑（角色分配、UID 生成、默认头像等）
        default_role = AuthService.ensure_default_role(db)
        user = User(
            email=email,
            nickname=name or email.split("@")[0],
            password_hash=OAUTH_NO_PASSWORD,
            google_id=google_id,
            avatar_url=picture,  # ADAPT: 可设置默认头像 fallback
            is_active=True,
        )
        db.add(user)
        db.flush()
        db.add(UserRole(user_id=user.id, role_id=default_role.id))
        db.commit()
        db.refresh(user)
        return user, True

    @staticmethod
    def google_login(db: Session, access_token: str) -> tuple[User, str, bool]:
        """完整的 Google 登录流程。返回 (user, jwt_token, is_new_user)。"""
        user_info = GoogleAuthService.fetch_google_user(access_token)

        google_id = user_info["sub"]
        email = user_info["email"]
        name = user_info.get("name", "")
        picture = user_info.get("picture")

        user, is_new_user = GoogleAuthService.find_or_create_user(
            db, google_id, email, name, picture
        )

        # ADAPT: 替换为你的 token 生成方法
        jwt_token = AuthService.create_access_token(user)
        return user, jwt_token, is_new_user

    @staticmethod
    def bind_google(db: Session, user: User, access_token: str) -> User:
        """将 Google 账号绑定到已登录用户。"""
        if user.google_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="已绑定 Google 账号",
            )

        user_info = GoogleAuthService.fetch_google_user(access_token)
        google_id = user_info["sub"]
        picture = user_info.get("picture")

        # 检查该 google_id 是否已被其他账号绑定
        existing = db.query(User).filter(User.google_id == google_id).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该 Google 账号已被其他用户绑定",
            )

        user.google_id = google_id
        # ADAPT: 替换默认头像判断逻辑
        if not user.avatar_url and picture:
            user.avatar_url = picture
        db.commit()
        db.refresh(user)
        return user
