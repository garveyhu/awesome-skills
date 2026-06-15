# Complex FastAPI Project Reference (UV Workspace)

UV workspace 多包架构，适合大型系统。参考 Sage 项目的 micro-kernel 设计。

## 架构思路

```
{project}-core    → 核心组件（配置、数据库、工具、基础模型）
{project}-app     → 应用入口（FastAPI 启动、中间件、路由注册）
{project}-system  → 业务包（API、Service、Schema）
{project}-agents  → 可选：AI/智能体包
```

模块只依赖 core，app 依赖所有包，实现关注点分离。

---

## 目录结构

```
{project}/
├── {project}-core/
│   └── src/{pkg}/core/
│       ├── complex/                 # 技术组件
│       │   ├── auth/
│       │   │   ├── auth_util.py     # JWT 工具
│       │   │   └── oauth.py         # get_current_user 依赖
│       │   ├── constants/
│       │   │   └── auth_whitelist.py
│       │   ├── config/
│       │   │   ├── base_settings.py
│       │   │   ├── constants.py
│       │   │   ├── settings.py
│       │   │   ├── inventory.py
│       │   │   └── request_context.py
│       │   └── response/
│       │       ├── code.py
│       │       └── result.py
│       ├── components/
│       │   └── database/
│       │       └── sqlalchemy_init.py
│       └── models/                  # 所有 SQLAlchemy 模型
│           └── user/
│               └── user.py
│
├── {project}-system/
│   └── src/{pkg}/system/
│       ├── api/                     # APIRouter（自动注册）
│       │   ├── auth_api.py          # 登录/注册接口
│       │   └── user_api.py
│       └── modules/
│           └── user/
│               ├── service/
│               │   └── user_service.py
│               └── schemas/
│                   └── user_dto.py
│
├── {project}-app/
│   └── src/{pkg}/app/
│       ├── main.py                  # FastAPI 启动、中间件
│       └── server.py                # 动态路由注册
│
├── config/                          # 配置文件（不提交 git）
│   ├── app.json
│   ├── app.json.example
│   ├── component.json
│   ├── component.json.example
│   └── .env
├── migrations/
│   ├── versions/
│   └── env.py
├── alembic.ini
├── pyproject.toml                   # UV workspace 根
└── scripts/
    └── run.sh                       # 启动脚本（放 scripts/，不放项目根）
```

> **禁止物理外键**：所有关联字段只用 `Column(Integer, index=True, comment="关联 xxx 表 ID")`，不使用 `ForeignKey()`。适用于所有数据库类型（SQLite / MySQL / PostgreSQL）。

---

## UV Workspace 配置

### 根 `pyproject.toml`

```toml
[project]
name = "{project}"
version = "1.0.0"
requires-python = ">=3.11,<3.13"
dependencies = [
    "{project}-app",
    "{project}-core",
    "{project}-system",
    "fastapi[all]>=0.116.0",
    "uvicorn>=0.27.0",
    "loguru>=0.7.0",
    "python-dotenv>=1.0.0",
    "sqlalchemy>=2.0.0",
    "alembic>=1.13.0",
    "pyyaml>=6.0.0",
    "pymysql>=1.1.0",
]

[dependency-groups]
dev = ["ruff>=0.8.0"]

[tool.uv.workspace]
members = [
    "{project}-app",
    "{project}-core",
    "{project}-system",
]

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

### 子包 `{project}-core/pyproject.toml`

```toml
[project]
name = "{project}-core"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/{pkg}/core"]
```

---

## 动态路由注册

### `{project}-app/src/{pkg}/app/server.py`

自动扫描所有 `{pkg}.*.api` 包并注册 `APIRouter`，无需手动 include：

```python
import importlib
import pkgutil
from types import ModuleType

from fastapi import APIRouter, FastAPI
from loguru import logger
from starlette.requests import Request
from starlette.responses import JSONResponse

from {pkg}.core.complex.response.code import ResultCode
from {pkg}.core.complex.response.result import Result


def register_routers(app: FastAPI):
    """动态扫描并注册所有 {pkg}.* 下的 APIRouter"""
    import {pkg}

    loaded_routers = set()

    def recursive_scan(package):
        if not hasattr(package, "__path__"):
            return
        for _, name, ispkg in pkgutil.iter_modules(package.__path__, package.__name__ + "."):
            if name.endswith(".__main__"):
                continue
            try:
                module = importlib.import_module(name)
            except Exception:
                continue
            if name.endswith(".api"):
                scan_api_module(module, app)
            elif ispkg:
                recursive_scan(module)

    def scan_api_module(module: ModuleType, app: FastAPI):
        if hasattr(module, "__path__"):
            for _, subname, _ in pkgutil.walk_packages(module.__path__, module.__name__ + "."):
                load_routers_from_name(subname, app)
        else:
            load_routers_from_module(module, app)

    def load_routers_from_name(module_name: str, app: FastAPI):
        try:
            lib = importlib.import_module(module_name)
            load_routers_from_module(lib, app)
        except Exception as e:
            logger.error(f"Failed to load routers from {module_name}: {e}")

    def load_routers_from_module(lib: ModuleType, app: FastAPI):
        for name in dir(lib):
            obj = getattr(lib, name)
            if isinstance(obj, APIRouter) and id(obj) not in loaded_routers:
                app.include_router(obj)
                loaded_routers.add(id(obj))
                logger.info(f"Registered router from {lib.__name__}")

    recursive_scan({pkg})


def create_app() -> FastAPI:
    app = FastAPI(title="{Project} API")

    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception):
        logger.exception(exc)
        return JSONResponse(
            status_code=500,
            content=Result(
                success=False, code=ResultCode.SYSTEM_INNER_ERROR.code, message=str(exc)
            ).model_dump(),
        )

    register_routers(app)
    return app
```

### `{project}-app/src/{pkg}/app/main.py`

```python
import sys

from alembic.command import upgrade
from alembic.config import Config
from fastapi import Request
from loguru import logger

from {pkg}.app.server import create_app
from {pkg}.core.complex.config.inventory import AppSettings
from {pkg}.core.complex.config.request_context import RequestContext

# 日志配置
logger.remove()
logger.add(
    sys.stderr,
    level=AppSettings.LOG_LEVEL,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
)

app = create_app()


def run_migrations():
    try:
        cfg = Config("alembic.ini")
        upgrade(cfg, "head")
        logger.info("Migrations completed.")
    except Exception as e:
        logger.error(f"Migration failed: {e}")


@app.on_event("startup")
def on_startup():
    run_migrations()
    # 可在此处添加：init_default_data()、preload_models() 等
    logger.info("Application started.")


@app.middleware("http")
async def auth_and_context_middleware(request: Request, call_next):
    """
    统一认证 + 上下文设置中间件
    在此处验证 JWT、解析用户信息、设置 RequestContext
    """
    # 白名单路由直接放行
    # auth_header = request.headers.get("Authorization")
    # user = verify_token(auth_header)
    # RequestContext.set_current_user(user)
    try:
        return await call_next(request)
    finally:
        RequestContext.clear()
```

---

## constants.py（子包路径适配）

不同子包的 constants.py 需要根据实际目录深度调整 `parents` 数量：

```python
# {project}-core/src/{pkg}/core/complex/config/constants.py
# 路径：src/{pkg}/core/complex/config/ → 根目录需要向上 5 级
from pathlib import Path

ROOT_PATH = Path(__file__).parents[5]  # 到 {project}-core/
PROJECT_ROOT = ROOT_PATH.parent         # 到 workspace 根
CONFIG_PATH = PROJECT_ROOT / "config"
```

---

## 包间依赖规则

| 包 | 可依赖 | 不可依赖 |
|----|--------|---------|
| `{project}-core` | 第三方库 | 其他子包 |
| `{project}-system` | `{project}-core` | `{project}-app` |
| `{project}-app` | 所有包 | — |

### 认证规范

JWT 认证工具在 `{project}-core` 中实现（`complex/auth/`），`{project}-system` 通过 `get_current_user` 依赖注入获取当前用户。参考 `references/simple-project.md` 中的 auth 相关模板。

---

## 新增业务模块流程

1. 在 `{project}-system/src/{pkg}/system/modules/{module}/` 下创建：
   - `service/{module}_service.py`
   - `schemas/{module}_dto.py`

2. 在 `{project}-system/src/{pkg}/system/api/{module}_api.py` 定义 `APIRouter`

3. 在 `{project}-core/src/{pkg}/core/models/{module}/{module}.py` 定义 SQLAlchemy Model

4. 生成 Alembic 迁移：`alembic revision --autogenerate -m "add_{module}_table"`

5. 路由自动被 `server.py` 的动态扫描注册，无需修改 `main.py`
