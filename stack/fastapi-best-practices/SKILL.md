---
name: fastapi-best-practices
description: >
  FastAPI project initialization, development guidance, and code review based on
  personal architectural conventions (uv+fastapi+sqlalchemy+alembic+loguru+ruff).
  Use when: (1) Creating/initializing a new FastAPI project,
  (2) Adding new endpoints, services, modules, or models to an existing FastAPI project,
  (3) Reviewing FastAPI project structure and code organization,
  (4) Setting up database migrations (Alembic), logging (Loguru), or config management,
  (5) Configuring linting/formatting toolchain (ruff).
  Supports two project scales: simple (single-package) and complex (UV workspace multi-package).
  Default API conventions: GET+POST only, Result.ok()/Result.fail() response format, MVC layering.
  Frontend pairing: Designed to work with react-best-practices skill.
---

# FastAPI Best Practices

## 概述

根据个人架构习惯，提供 FastAPI 项目的全生命周期指导：初始化、开发规范、代码审查。

**核心技术栈**: uv + fastapi + sqlalchemy + alembic + loguru + ruff

**项目规模**:
- **简单项目**（默认）：单包，适合大多数新项目。详见 [references/simple-project.md](references/simple-project.md)
- **复杂项目**：UV workspace 多包架构（micro-kernel），适合大型系统。详见 [references/complex-project.md](references/complex-project.md)

---

## 阶段一：初始化新项目（Init）

### 前置检查

1. 确认 Python >= 3.11、uv 已安装
2. 询问项目名称（`{project}` 下划线命名）和目标目录
3. 询问项目规模（简单/复杂），默认简单
4. 询问数据库类型（sqlite/mysql），默认 sqlite

### 步骤 1: 创建 uv 项目

```bash
uv init {项目名} --package
cd {项目名}
```

### 步骤 2: 安装依赖

```bash
# 生产依赖
uv add "fastapi[all]" sqlalchemy alembic loguru python-dotenv pyyaml pymysql

# 开发依赖
uv add ruff --dev
```

### 步骤 3: 配置 pyproject.toml

添加 ruff 配置（`requires-python = ">=3.11"`）：

```toml
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

### 步骤 4: 创建目录结构 + 核心文件

读取 [references/simple-project.md](references/simple-project.md)，按其完整结构创建所有目录和文件（复杂项目读 [references/complex-project.md](references/complex-project.md)）。

### 步骤 5: 配置 Alembic

```bash
alembic init migrations
```

修改 `alembic.ini`：
```ini
file_template = %%(year)d%(month).2d%(day).2d_%(slug)s
sqlalchemy.url = sqlite:///./data.db
```

修改 `migrations/env.py`，指向模型 Base：
```python
from {pkg}.complex.database import Base
target_metadata = Base.metadata
```

### 步骤 6: 创建启动脚本

`scripts/run.sh`（放根目录的 `scripts/` 下，不放项目根）：
```bash
#!/bin/bash
cd "$(dirname "$0")/.." || exit 1
uv sync
uv run python -m {pkg}.app.main
```

### 步骤 7: 初始化 git

```bash
git init
```

`.gitignore` 包含：`.venv/`, `*.pyc`, `__pycache__/`, `.env`, `config/*.json`（配置文件通过 `*.json.example` 版本控制）。

### 步骤 8: 格式化 + 验证

```bash
ruff format .
ruff check --fix .
uv run python -m {pkg}.app.main   # 验证启动正常
```

---

## 阶段二：开发指导（Guide）

### HTTP 方法规范

**只允许 GET 和 POST，禁止 PUT/DELETE/PATCH：**

| 操作 | HTTP 方法 | URL 格式 |
|------|-----------|----------|
| 查询列表 | `GET` | `/resource` |
| 查询单个 | `GET` | `/resource/{id}` |
| 创建 | `POST` | `/resource/create` 或 `/resource` |
| 更新 | `POST` | `/resource/{id}/update` |
| 删除 | `POST` | `/resource/{id}/delete` |

### 响应格式

所有接口统一使用 `Result` 包装：

```python
from {pkg}.complex.response.result import Result

return Result.ok(data)           # 成功，data 可为 None
return Result.fail("错误信息")   # 失败
return Result.create(success, data, message)  # 自定义
```

**禁止**直接返回 dict 或 Pydantic model，必须用 `Result` 包装。

### MVC 分层规范

| 层 | 路径 | 职责 | 约束 |
|----|------|------|------|
| API | `{pkg}/api/` | 接口声明、参数校验、调用 Service | 不写业务逻辑，不查数据库 |
| Service | `{pkg}/modules/{模块}/service/` | 业务逻辑实现 | 不处理 HTTP 请求/响应格式 |
| Schema | `{pkg}/modules/{模块}/schemas/` | Pydantic DTO 定义 | 纯数据结构 |
| Model | `{pkg}/models/` | SQLAlchemy 数据模型 | 不写业务逻辑 |

**API 层调用 Service，Service 操作数据库，Schema 定义数据契约。**

### 添加新接口

```python
# {pkg}/api/user_api.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from {pkg}.complex.database import get_db
from {pkg}.complex.response.result import Result
from {pkg}.modules.user.schemas.user_dto import UserCreateDTO
from {pkg}.modules.user.service.user_service import UserService

router = APIRouter(prefix="/user", tags=["用户"])


@router.get("")
def list_users(db: Session = Depends(get_db)):
    return Result.ok(UserService.list(db))


@router.post("/create")
def create_user(dto: UserCreateDTO, db: Session = Depends(get_db)):
    return Result.ok(UserService.create(db, dto))


@router.post("/{user_id}/update")
def update_user(user_id: int, dto: UserCreateDTO, db: Session = Depends(get_db)):
    return Result.ok(UserService.update(db, user_id, dto))


@router.post("/{user_id}/delete")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    UserService.delete(db, user_id)
    return Result.ok()
```

### 添加新 Service

```python
# {pkg}/modules/user/service/user_service.py
from sqlalchemy.orm import Session

from {pkg}.models.user import User
from {pkg}.modules.user.schemas.user_dto import UserCreateDTO


class UserService:
    @staticmethod
    def list(db: Session) -> list[User]:
        return db.query(User).all()

    @staticmethod
    def create(db: Session, dto: UserCreateDTO) -> User:
        user = User(**dto.model_dump())
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete(db: Session, user_id: int) -> None:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
```

### 请求上下文

使用 `ContextVar`（**非** `threading.local()`）实现异步安全上下文：

```python
from {pkg}.complex.config.request_context import RequestContext

# 在 Service 层读取
user_id = RequestContext.get_user_id()
current_user = RequestContext.get_current_user()
```

在中间件中设置，`finally` 块中清理（`RequestContext.clear()`）。

### 配置管理

三层结构：JSON 文件（非敏感）+ `.env`（敏感）+ inventory 类（访问入口）：

```python
# 使用配置
from {pkg}.complex.config.inventory import AppSettings, DatabaseSettings

log_level = AppSettings.LOG_LEVEL
db_url = DatabaseSettings.get_url()
```

配置文件命名约定：
- `config/app.json` — 应用配置（版本控制 `app.json.example`）
- `config/component.json` — 组件配置（数据库、Redis 等）
- `config/.env` — 密钥、密码等敏感信息（不提交 git）

### 日志配置

```python
from loguru import logger

logger.info("服务启动完成")
logger.error(f"操作失败: {e}")
logger.debug(f"查询结果: {result}")
```

启动时配置（`main.py`）：
```python
import sys
from loguru import logger

logger.remove()
logger.add(
    sys.stderr,
    level=AppSettings.LOG_LEVEL,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
)
# 生产环境追加文件日志
# logger.add("logs/{time:YYYY-MM-DD}.log", rotation="00:00", retention="90 days", compression="zip")
```

### 数据库迁移

**流程：修改 Model → 生成迁移 → 启动自动执行**

```bash
# 生成迁移脚本（AI 自动生成 upgrade/downgrade 内容）
alembic revision --autogenerate -m "add_user_table"

# 手动升级（通常由启动脚本自动执行）
alembic upgrade head
```

**SQLite 必须用 `batch_alter_table`（禁止直接操作）：**

```python
# 正确 ✅
with op.batch_alter_table("users") as batch_op:
    batch_op.add_column(sa.Column("age", sa.Integer()))
    batch_op.drop_column("old_field")

# 错误 ❌
op.add_column("users", sa.Column("age", sa.Integer()))
```

启动时自动迁移（`main.py` startup hook）：
```python
from alembic.command import upgrade
from alembic.config import Config

@app.on_event("startup")
def on_startup():
    cfg = Config("alembic.ini")
    upgrade(cfg, "head")
```

### 命名约定

| 类型 | 约定 | 示例 |
|------|------|------|
| 文件名 | snake_case | `user_service.py`, `user_api.py` |
| 类名 | PascalCase | `UserService`, `UserCreateDTO` |
| 函数/方法 | snake_case | `get_user_by_id` |
| 常量 | UPPER_SNAKE_CASE | `LOG_LEVEL`, `DATABASE_URL` |
| DTO 类 | 后缀 DTO | `UserCreateDTO`, `UserQueryDTO` |
| VO 类 | 后缀 VO | `UserVO` |
| API 文件 | `{模块}_api.py` | `user_api.py` |
| Service 文件 | `{模块}_service.py` | `user_service.py` |

### JWT 认证模式

认证逻辑由三个文件协作：

```python
# {pkg}/complex/auth/auth_util.py
from typing import Optional

import jwt
from sqlalchemy.orm import Session
from {pkg}.complex.database import SessionLocal
from {pkg}.models.user import User

SECRET_KEY = "your-secret-key"   # 从 config 读取
ALGORITHM = "HS256"

def verify_token(token: str) -> Optional[str]:
    """验证 JWT，返回 username；无效返回 None"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except Exception:
        return None

def verify_and_get_user(token: str) -> Optional[User]:
    """验证 Token 并返回完整 User 对象"""
    username = verify_token(token)
    if not username:
        return None
    db: Session = SessionLocal()
    try:
        return db.query(User).filter(User.username == username).first()
    finally:
        db.close()
```

```python
# {pkg}/complex/auth/oauth.py
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from {pkg}.complex.auth.auth_util import verify_and_get_user

bearer_scheme = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    """FastAPI 依赖注入：获取当前认证用户"""
    user = verify_and_get_user(credentials.credentials)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user
```

```python
# {pkg}/complex/constants/auth_whitelist.py
class AuthWhitelist:
    _WHITELIST = ["/auth/login", "/auth/register", "/health", "/ping",
                  "/docs", "/redoc", "/openapi.json"]

    @classmethod
    def is_whitelisted(cls, path: str) -> bool:
        return any(path.startswith(r) for r in cls._WHITELIST)
```

中间件使用白名单：
```python
# Required imports in main.py/server.py:
# from starlette.responses import JSONResponse
# from {pkg}.complex.auth.auth_util import verify_and_get_user
# from {pkg}.complex.config.request_context import RequestContext
# from {pkg}.complex.constants.auth_whitelist import AuthWhitelist

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if AuthWhitelist.is_whitelisted(request.url.path):
        try:
            return await call_next(request)
        finally:
            RequestContext.clear()

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(status_code=401,
            content={"success": False, "code": 401, "message": "Missing token"})

    token = auth_header.split(" ", 1)[1]
    user = verify_and_get_user(token)
    if not user:
        return JSONResponse(status_code=401,
            content={"success": False, "code": 401, "message": "Invalid token"})

    RequestContext.set_current_user(user)
    try:
        return await call_next(request)
    finally:
        RequestContext.clear()
```

API 层使用 `get_current_user`：
```python
from {pkg}.complex.auth.oauth import get_current_user

@router.get("/profile")
def get_profile(current_user=Depends(get_current_user)):
    return Result.ok({"id": current_user.id, "username": current_user.username})
```

### 自定义业务异常

业务层抛异常，框架层统一捕获处理：

```python
# {pkg}/complex/response/exception.py
from {pkg}.complex.response.code import ResultCode

class CustomException(Exception):
    def __init__(self, result_code: ResultCode, message: str = None):
        self.result_code = result_code
        self.message = message or result_code.message
        super().__init__(self.message)

# ResultCode 示例（实际定义在 {pkg}/complex/response/code.py）：
# class ResultCode(Enum):
#     SUCCESS = (200, "成功")
#     NOT_FOUND = (404, "资源不存在")
#     UNAUTHORIZED = (401, "未授权")
#
#     def __init__(self, code: int, message: str):
#         self.code = code
#         self.message = message
```

在 `server.py` 的 `create_app()` 中注册处理器：
```python
from {pkg}.complex.response.exception import CustomException

@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.result_code.code,
        content=Result(success=False, code=exc.result_code.code,
                       message=exc.message).model_dump(),
    )
```

业务层使用：
```python
# Service 层
from {pkg}.complex.response.exception import CustomException
from {pkg}.complex.response.code import ResultCode

def get_user(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise CustomException(ResultCode.NOT_FOUND, f"用户 {user_id} 不存在")
    return user
```

### 分页模式

```python
# {pkg}/schemas/common/pagination.py
from typing import Generic, List, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")

class PageParams(BaseModel):
    page: int = Field(1, ge=1, description="页码，从 1 开始")
    page_size: int = Field(10, ge=1, le=100, description="每页数量")

class PageResult(BaseModel, Generic[T]):
    items: List[T] = Field(default_factory=list)
    total: int = Field(0, description="总数")
    page: int = Field(1)
    page_size: int = Field(10)
```

Service 层：
```python
def list_users(db: Session, params: PageParams) -> PageResult[UserVO]:
    query = db.query(User)
    total = query.count()
    users = query.offset((params.page - 1) * params.page_size)\
                 .limit(params.page_size).all()
    items = [UserVO.model_validate(u) for u in users]  # ORM → Pydantic VO
    return PageResult(items=items, total=total,
                      page=params.page, page_size=params.page_size)
```

API 层：
```python
@router.get("")
def list_users(params: PageParams = Depends(), db: Session = Depends(get_db)):
    return Result.ok(UserService.list_users(db, params))
```

### CORS 配置

在 `create_app()` 中注册（中间件顺序：CORS 在 auth 之前）：

```python
from fastapi.middleware.cors import CORSMiddleware

def create_app() -> FastAPI:
    app = FastAPI(...)

    # 开发环境：允许所有来源（不能同时使用 credentials）
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )

    # 生产环境（替换上面的配置）：
    # app.add_middleware(
    #     CORSMiddleware,
    #     allow_origins=["https://yourdomain.com"],
    #     allow_credentials=True,
    #     allow_methods=["GET", "POST"],
    #     allow_headers=["*"],
    # )
```

### SQLAlchemy Model 时间戳与外键约定

**时间戳**（统一使用北京时间 +08:00）：
```python
from sqlalchemy import Column, DateTime, Integer, String, text

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)

    # ✅ 正确：server_default 设置北京时间
    created_at = Column(DateTime(timezone=True),
                        server_default=text("(datetime('now', '+08:00'))"))
    updated_at = Column(DateTime(timezone=True),
                        server_default=text("(datetime('now', '+08:00'))"),
                        onupdate=lambda: datetime.now(tz=timezone(timedelta(hours=8))))
```

> Note: `server_default` uses SQLite syntax for the initial value; `onupdate` uses a Python-side callable for ORM-triggered updates. Add `from datetime import datetime, timedelta, timezone` to imports.
>
> For MySQL/PostgreSQL, use: `server_default=text("NOW()")`.

**禁止物理外键（适用所有数据库类型）**：
```python
# ✅ 正确：逻辑关联，index=True + comment 说明
user_id = Column(Integer, index=True, comment="关联 users 表 ID")
space_id = Column(Integer, index=True, comment="关联 spaces 表 ID")

# ❌ 错误：物理外键约束
# user_id = Column(Integer, ForeignKey("users.id"))
```

原因：统一多数据库适配（SQLite/MySQL/PostgreSQL），避免迁移复杂性，逻辑关联由应用层维护。

### Pydantic Schema 约定

```python
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

# 响应 Schema：from_attributes=True 支持 ORM 对象直接映射
class UserVO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    created_at: datetime = Field(description="创建时间")

# Create DTO：必填字段
class UserCreateDTO(BaseModel):
    username: str = Field(description="用户名")
    password: str = Field(description="密码")

# Update DTO：所有字段 Optional（只传要改的字段）
class UserUpdateDTO(BaseModel):
    username: Optional[str] = Field(None, description="用户名")
    password: Optional[str] = Field(None, description="密码")

# camelCase 别名（前后端字段名不一致时）
class ConfigDTO(BaseModel):
    page_size: int = Field(10, alias="pageSize")
    sort_order: Optional[str] = Field(None, alias="sortOrder")

    model_config = ConfigDict(populate_by_name=True)
```

### 可选工具模式

以下工具按需引入，详见 [references/patterns.md](references/patterns.md)：

| 工具 | 用途 |
|------|------|
| `convert_util.py` | ORM 对象 → 字典/Schema，snake_case → camelCase |
| `time_util.py` | UTC → 北京时间转换，时间范围解析 |
| `request_context_util.py` | 带错误处理的 `get_required_user_id()` 等便捷方法 |
| `crypto_util.py` | AES-256-GCM 可逆加密（存储 API Key 等场景，按需评估） |

---

## 阶段三：代码审查（Review）

### 结构检查

- [ ] 目录结构符合规范（简单/复杂对应结构）
- [ ] `pyproject.toml` 包含 ruff 配置，`requires-python = ">=3.11"`
- [ ] `alembic.ini` 中 `file_template` 包含日期前缀
- [ ] `migrations/env.py` 指向正确的 `Base.metadata`
- [ ] `config/` 下有 `*.json.example`（非敏感默认值版本控制用）
- [ ] `.gitignore` 包含 `.env` 和实际配置 JSON

### HTTP 方法检查

- [ ] 无 `PUT`、`DELETE`、`PATCH` 方法
- [ ] 更新操作：`POST /{id}/update`
- [ ] 删除操作：`POST /{id}/delete`

### 响应格式检查

- [ ] 所有接口返回 `Result.ok()` 或 `Result.fail()`
- [ ] 无直接返回 dict、Pydantic model、或裸数据

### 分层检查

- [ ] API 层无业务逻辑，只校验参数和调用 Service
- [ ] Service 层无 HTTP 相关代码（无 Request/Response 对象）
- [ ] Schema 层只定义数据结构（Pydantic BaseModel）
- [ ] Model 层只定义数据库映射（SQLAlchemy）

### 配置检查

- [ ] 密钥、密码在 `.env`，非敏感配置在 `*.json`
- [ ] `inventory.py` 提供统一配置访问入口（类或函数）
- [ ] 不在代码中硬编码任何配置值

### 数据库检查

- [ ] SQLite 迁移使用 `batch_alter_table`（无直接 `op.add_column` 等）
- [ ] 启动时自动运行 `alembic upgrade head`
- [ ] 所有 Model 继承统一 `Base`
- [ ] `get_db()` 作为 FastAPI 依赖注入（`Depends(get_db)`）

### 请求上下文检查

- [ ] 中间件使用 `ContextVar` 实现（非 `threading.local()`）
- [ ] 请求结束后在 `finally` 中调用 `RequestContext.clear()`

### 代码质量

- [ ] `ruff format .` 无差异
- [ ] `ruff check .` 无报错
- [ ] 命名符合 snake_case 约定
- [ ] 无 `print()` 语句（用 `logger` 替代）

### 认证检查

- [ ] 中间件白名单包含 `/health`、`/ping`、`/docs`
- [ ] API 层使用 `Depends(get_current_user)` 获取用户，不手动解析 Token
- [ ] 业务异常使用 `CustomException(ResultCode.XXX)` 抛出

### 数据库 Schema 检查

- [ ] Model 无 `ForeignKey()` 约束（关联字段只用 `index=True`）
- [ ] 关联字段有 `comment` 注明关联关系
- [ ] `created_at` / `updated_at` 使用 `server_default=text("(datetime('now', '+08:00'))")`

### Schema 检查

- [ ] 响应 Schema 有 `model_config = ConfigDict(from_attributes=True)`
- [ ] Update DTO 所有字段为 `Optional`
- [ ] CORS 已配置；生产环境 `allow_origins` 非 `["*"]`
