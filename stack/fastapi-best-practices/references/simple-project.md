# Simple FastAPI Project Reference

单包 FastAPI 项目的完整结构和核心文件模板。

## 目录结构

```
{project}/
├── src/
│   └── {pkg}/
│       ├── __init__.py
│       ├── app/
│       │   ├── __init__.py
│       │   └── main.py              # FastAPI app、startup hooks、middleware
│       ├── api/                     # APIRouter 文件（自动注册）
│       │   ├── __init__.py
│       │   └── user_api.py
│       ├── modules/                 # 业务模块
│       │   └── user/
│       │       ├── service/
│       │       │   └── user_service.py
│       │       └── schemas/
│       │           └── user_dto.py
│       ├── models/                  # SQLAlchemy 数据模型
│       │   ├── __init__.py
│       │   ├── base.py
│       │   └── user.py
│       └── complex/                 # 技术组件（不含业务）
│           ├── config/
│           │   ├── base_settings.py
│           │   ├── constants.py
│           │   ├── settings.py
│           │   ├── inventory.py
│           │   └── request_context.py
│           ├── response/
│           │   ├── code.py
│           │   └── result.py
│           └── database.py          # SQLAlchemy engine + SessionLocal + get_db
├── config/                          # 配置文件（不提交 git，用 *.example 版本控制）
│   ├── app.json
│   ├── app.json.example
│   ├── component.json
│   ├── component.json.example
│   └── .env
├── migrations/
│   ├── versions/
│   └── env.py
├── alembic.ini
├── pyproject.toml
├── scripts/
│   └── run.sh                      # 启动脚本（放 scripts/，不放项目根）
└── .gitignore
```

---

## 核心文件模板

### `pyproject.toml`

```toml
[project]
name = "{project}"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi[all]>=0.116.0",
    "sqlalchemy>=2.0.0",
    "alembic>=1.13.0",
    "loguru>=0.7.0",
    "python-dotenv>=1.0.0",
    "pyyaml>=6.0.0",
    "pymysql>=1.1.0",
]

[dependency-groups]
dev = [
    "ruff>=0.8.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 88
target-version = "py311"
exclude = ["*.pyc", "migrations"]

[tool.ruff.lint]
extend-select = ["I"]

[tool.ruff.lint.isort]
section-order = ["future", "standard-library", "third-party", "first-party", "local-folder"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
line-ending = "auto"
```

---

### `src/{pkg}/complex/config/base_settings.py`

```python
import json
from pathlib import Path

import yaml
from dotenv import dotenv_values


class BaseSettings:
    def __init__(self, data=None):
        self.data = {} if data is None else data

    def __getitem__(self, key):
        return self.get(key)

    def get(self, key):
        keys = key.split(".")
        result = self.data
        for k in keys:
            result = result.get(k, {})
        return result

    def __setitem__(self, key, value):
        self.set(key, value)

    def set(self, key, value):
        keys = key.split(".")
        current = self.data
        for k in keys[:-1]:
            current = current.setdefault(k, {})
        current[keys[-1]] = value

    def to_dict(self):
        return self.data

    @classmethod
    def from_env(cls, env_path: Path):
        data = dotenv_values(env_path)
        return BaseSettings(data)

    @classmethod
    def from_json(cls, json_path: Path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return BaseSettings(data)

    @classmethod
    def from_yaml(cls, yaml_path: Path):
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return BaseSettings(data)
```

---

### `src/{pkg}/complex/config/constants.py`

```python
from pathlib import Path

# 项目根路径（src/{pkg}/complex/config/ 上四级）
ROOT_PATH = Path(__file__).parents[4]
CONFIG_PATH = ROOT_PATH / "config"
```

---

### `src/{pkg}/complex/config/settings.py`

```python
from dotenv import load_dotenv

from .base_settings import BaseSettings
from .constants import CONFIG_PATH

load_dotenv(CONFIG_PATH / ".env")


class AppSettings(BaseSettings):
    """应用配置"""

    def __init__(self):
        super().__init__()
        self.data = self.from_json(CONFIG_PATH / "app.json").data


class ComponentSettings(BaseSettings):
    """组件配置（数据库、Redis 等）"""

    def __init__(self):
        super().__init__()
        self.data = self.from_json(CONFIG_PATH / "component.json").data


app_settings = AppSettings()
component_settings = ComponentSettings()
```

---

### `src/{pkg}/complex/config/inventory.py`

```python
import os

from .settings import app_settings, component_settings


class AppSettings:
    """应用配置访问类"""

    LOG_LEVEL = os.getenv("LOG_LEVEL") or app_settings.get("LOG_LEVEL") or "INFO"
    APP_NAME = app_settings.get("APP_NAME") or "{project}"


class DatabaseSettings:
    """数据库配置访问类"""

    _cached_url = None

    @staticmethod
    def get_type() -> str:
        return component_settings.get("database.type") or "sqlite"

    @staticmethod
    def get_url() -> str:
        if DatabaseSettings._cached_url:
            return DatabaseSettings._cached_url

        db_type = DatabaseSettings.get_type()
        if db_type == "sqlite":
            path = component_settings.get("database.sqlite.path") or "sqlite:///./data.db"
            DatabaseSettings._cached_url = path
        elif db_type == "mysql":
            import urllib.parse

            host = os.getenv("MYSQL_HOST") or component_settings.get("database.mysql.host") or "127.0.0.1"
            port = int(os.getenv("MYSQL_PORT") or component_settings.get("database.mysql.port") or 3306)
            db = os.getenv("MYSQL_DB") or component_settings.get("database.mysql.db") or "{project}"
            user = os.getenv("MYSQL_USER") or component_settings.get("database.mysql.user") or "root"
            password = os.getenv("MYSQL_PASSWORD") or component_settings.get("database.mysql.password") or ""
            encoded_user = urllib.parse.quote_plus(user)
            encoded_password = urllib.parse.quote_plus(password)
            DatabaseSettings._cached_url = (
                f"mysql+pymysql://{encoded_user}:{encoded_password}@{host}:{port}/{db}?charset=utf8mb4"
            )
        return DatabaseSettings._cached_url

    @staticmethod
    def is_sqlite() -> bool:
        return DatabaseSettings.get_type() == "sqlite"
```

---

### `src/{pkg}/complex/config/request_context.py`

```python
from contextvars import ContextVar
from typing import Any, Optional

_user_id: ContextVar[Optional[int]] = ContextVar("user_id", default=None)
_current_user: ContextVar[Any] = ContextVar("current_user", default=None)


class RequestContext:
    """请求上下文管理器（ContextVar 实现，异步安全）"""

    @staticmethod
    def get_user_id() -> Optional[int]:
        return _user_id.get()

    @staticmethod
    def set_user_id(user_id: Optional[int]) -> None:
        _user_id.set(user_id)

    @staticmethod
    def get_current_user() -> Any:
        return _current_user.get()

    @staticmethod
    def set_current_user(user: Any) -> None:
        _current_user.set(user)
        if hasattr(user, "id"):
            _user_id.set(user.id)

    @staticmethod
    def clear() -> None:
        _user_id.set(None)
        _current_user.set(None)
```

---

### `src/{pkg}/complex/response/code.py`

```python
from enum import Enum


class ResultCode(Enum):
    SUCCESS = (200, "操作成功")
    FAIL = (400, "操作失败")
    UNAUTHORIZED = (401, "未授权")
    FORBIDDEN = (403, "无权限")
    NOT_FOUND = (404, "资源不存在")
    SYSTEM_INNER_ERROR = (500, "系统内部错误")

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
```

---

### `src/{pkg}/complex/response/result.py`

```python
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, Field

from .code import ResultCode

T = TypeVar("T")


class Result(BaseModel, Generic[T]):
    success: bool = Field(..., description="操作是否成功")
    code: int = Field(..., description="状态码")
    message: str = Field(..., description="响应消息")
    data: Optional[T] = Field(None, description="响应数据")

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def ok(cls, data: Optional[T] = None):
        return cls(
            success=True,
            code=ResultCode.SUCCESS.code,
            message=ResultCode.SUCCESS.message,
            data=data,
        )

    @classmethod
    def fail(cls, message: str = ResultCode.FAIL.message, data: Optional[T] = None):
        return cls(success=False, code=ResultCode.FAIL.code, message=message, data=data)

    @classmethod
    def create(cls, success: bool, data: Optional[T] = None, message: str = ""):
        code = ResultCode.SUCCESS.code if success else ResultCode.FAIL.code
        return cls(success=success, code=code, message=message, data=data)
```

---

### `src/{pkg}/complex/database.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config.inventory import DatabaseSettings

db_url = DatabaseSettings.get_url()

if DatabaseSettings.is_sqlite():
    engine = create_engine(
        db_url,
        connect_args={"check_same_thread": False},
        pool_size=5,
        max_overflow=10,
    )
else:
    engine = create_engine(
        db_url,
        pool_size=10,
        max_overflow=20,
        pool_timeout=60,
        pool_recycle=3600,
        pool_pre_ping=True,
    )

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """FastAPI 依赖注入用数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

### `src/{pkg}/complex/auth/auth_util.py`

```python
from typing import Optional
import datetime

import jwt
from sqlalchemy.orm import Session

from {pkg}.complex.config.inventory import AppSettings
from {pkg}.complex.database import SessionLocal
from {pkg}.models.user import User

SECRET_KEY = AppSettings.SECRET_KEY   # config/app.json 中配置
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 小时


def create_access_token(username: str) -> str:
    """生成 JWT Token"""
    payload = {
        "sub": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> Optional[str]:
    """验证 Token，返回 username；失败返回 None"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except Exception:
        return None


def verify_and_get_user(token: str) -> Optional[User]:
    """验证 Token 并返回 User 对象"""
    username = verify_token(token)
    if not username:
        return None
    db: Session = SessionLocal()
    try:
        return db.query(User).filter(User.username == username).first()
    finally:
        db.close()
```

安装 JWT 库：`uv add pyjwt`

---

### `src/{pkg}/complex/auth/oauth.py`

```python
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from {pkg}.complex.auth.auth_util import verify_and_get_user
from {pkg}.models.user import User

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> User:
    """FastAPI 依赖注入：验证 Token 并返回当前用户"""
    if not credentials:
        raise HTTPException(status_code=401, detail="Missing token")
    user = verify_and_get_user(credentials.credentials)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user
```

---

### `src/{pkg}/complex/constants/auth_whitelist.py`

```python
class AuthWhitelist:
    """认证白名单：这些路由跳过 JWT 验证"""

    _WHITELIST = [
        "/auth/login",
        "/auth/register",
        "/health",
        "/ping",
        "/docs",
        "/redoc",
        "/openapi.json",
    ]

    @classmethod
    def is_whitelisted(cls, path: str) -> bool:
        return any(path.startswith(route) for route in cls._WHITELIST)

    @classmethod
    def get_all(cls) -> list[str]:
        return cls._WHITELIST.copy()
```

---

### `src/{pkg}/complex/response/exception.py`

```python
from {pkg}.complex.response.code import ResultCode


class CustomException(Exception):
    """业务异常：携带 ResultCode 和自定义消息，由全局 exception_handler 捕获"""

    def __init__(self, result_code: ResultCode, message: str = None):
        self.result_code = result_code
        self.message = message if message else result_code.message
        super().__init__(self.message)
```

在 `server.py` `create_app()` 中注册：
```python
from {pkg}.complex.response.exception import CustomException

@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.result_code.code,
        content=Result(
            success=False, code=exc.result_code.code, message=exc.message
        ).model_dump(),
    )
```

---

### `src/{pkg}/schemas/common/pagination.py`

```python
from typing import Generic, List, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PageParams(BaseModel):
    """分页查询参数（通过 Depends() 注入）"""

    page: int = Field(1, ge=1, description="页码，从 1 开始")
    page_size: int = Field(10, ge=1, le=100, description="每页数量，最大 100")


class PageResult(BaseModel, Generic[T]):
    """分页查询结果（包裹在 Result.ok() 中返回）"""

    items: List[T] = Field(default_factory=list, description="数据列表")
    total: int = Field(0, description="总记录数")
    page: int = Field(1, description="当前页码")
    page_size: int = Field(10, description="每页数量")
```

---

### `src/{pkg}/models/base.py`

```python
from {pkg}.complex.database import Base

__all__ = ["Base"]
```

---

### `src/{pkg}/models/user.py`（示例）

```python
from sqlalchemy import Boolean, Column, DateTime, Integer, String, text
from datetime import datetime, timedelta, timezone

from {pkg}.complex.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    # 逻辑外键：不使用 ForeignKey()，用 index=True + comment
    role_id = Column(Integer, index=True, comment="关联 roles 表 ID")

    created_at = Column(
        DateTime(timezone=True),
        server_default=text("(datetime('now', '+08:00'))"),
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=text("(datetime('now', '+08:00'))"),
        onupdate=lambda: datetime.now(tz=timezone(timedelta(hours=8))),
    )
```

---

### `src/{pkg}/modules/user/schemas/user_dto.py`

```python
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserVO(BaseModel):
    """用户视图对象（响应）"""
    model_config = ConfigDict(from_attributes=True)  # 支持 ORM 对象直接映射

    id: int
    username: str
    is_active: bool
    created_at: datetime = Field(description="创建时间")


class UserCreateDTO(BaseModel):
    """创建用户（必填字段）"""
    username: str = Field(description="用户名，唯一")
    password: str = Field(description="明文密码，服务层负责加密")


class UserUpdateDTO(BaseModel):
    """更新用户（所有字段 Optional，只传要改的）"""
    username: Optional[str] = Field(None, description="用户名")
    password: Optional[str] = Field(None, description="新密码")
    is_active: Optional[bool] = Field(None, description="是否启用")
```

---

### `src/{pkg}/app/main.py`

```python
import sys

from alembic.command import upgrade
from alembic.config import Config
from fastapi import APIRouter, FastAPI, Request
from loguru import logger
from starlette.responses import JSONResponse

from {pkg}.complex.config.inventory import AppSettings
from {pkg}.complex.config.request_context import RequestContext
from {pkg}.complex.response.code import ResultCode
from {pkg}.complex.response.result import Result

# 日志配置
logger.remove()
logger.add(
    sys.stderr,
    level=AppSettings.LOG_LEVEL,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
)


def create_app() -> FastAPI:
    app = FastAPI(title=AppSettings.APP_NAME)

    # 全局异常处理
    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception):
        logger.exception(exc)
        return JSONResponse(
            status_code=500,
            content=Result(
                success=False, code=ResultCode.SYSTEM_INNER_ERROR.code, message=str(exc)
            ).model_dump(),
        )

    # 注册路由
    _register_routers(app)

    return app


def _register_routers(app: FastAPI):
    """自动扫描 {pkg}/api/ 下所有 APIRouter 并注册"""
    import importlib
    import pkgutil

    import {pkg}.api as api_pkg

    for _, name, _ in pkgutil.walk_packages(api_pkg.__path__, api_pkg.__name__ + "."):
        try:
            module = importlib.import_module(name)
            for attr_name in dir(module):
                obj = getattr(module, attr_name)
                if isinstance(obj, APIRouter):
                    app.include_router(obj)
                    logger.info(f"Registered router: {name}")
        except Exception as e:
            logger.error(f"Failed to register router {name}: {e}")


def run_migrations():
    try:
        cfg = Config("alembic.ini")
        upgrade(cfg, "head")
        logger.info("Migrations completed.")
    except Exception as e:
        logger.error(f"Migration failed: {e}")


app = create_app()


@app.on_event("startup")
def on_startup():
    run_migrations()
    logger.info("Application started.")


@app.middleware("http")
async def context_middleware(request: Request, call_next):
    """请求上下文中间件"""
    # 在此处可解析 JWT、设置 RequestContext
    try:
        return await call_next(request)
    finally:
        RequestContext.clear()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

---

### `migrations/env.py`（关键修改）

```python
from {pkg}.complex.database import Base

# 替换默认的 target_metadata = None
target_metadata = Base.metadata
```

---

### `config/app.json.example`

```json
{
    "APP_NAME": "{project}",
    "LOG_LEVEL": "INFO"
}
```

### `config/component.json.example`

```json
{
    "database": {
        "type": "sqlite",
        "sqlite": {
            "path": "sqlite:///./data.db"
        },
        "mysql": {
            "host": "127.0.0.1",
            "port": 3306,
            "db": "{project}",
            "user": "root",
            "password": ""
        }
    }
}
```

### `config/.env`（不提交 git）

```bash
# 覆盖 JSON 配置中的敏感值
# MYSQL_HOST=
# MYSQL_PASSWORD=
# LOG_LEVEL=DEBUG
```

---

### `scripts/run.sh`

放在根目录 `scripts/` 下；脚本先 `cd` 到项目根，便于在任意位置调用：

```bash
#!/bin/bash
cd "$(dirname "$0")/.." || exit 1
uv sync
uv run python -m {pkg}.app.main
```

---

### `.gitignore`

```
.venv/
*.pyc
__pycache__/
.env
config/*.json
!config/*.json.example
data.db
*.log
logs/
```
