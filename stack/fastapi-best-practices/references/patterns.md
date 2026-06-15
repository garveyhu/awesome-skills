# Optional Patterns Reference

以下工具模式按需使用，不属于基础项目结构。使用前确认已安装对应依赖。

---

## convert_util.py — 数据转换工具

**额外依赖**：无

```python
# {pkg}/complex/utils/convert_util.py
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar

T = TypeVar("T")
S = TypeVar("S")


def model_to_dict(
    model: Any,
    include: Optional[List[str]] = None,
    exclude: Optional[List[str]] = None,
    extra: Optional[Dict[str, Any]] = None,
    converters: Optional[Dict[str, Callable[[Any], Any]]] = None,
) -> Dict[str, Any]:
    """SQLAlchemy ORM 对象 → 字典。datetime 自动转为 ISO 字符串。"""
    from sqlalchemy import inspect
    mapper = inspect(type(model))
    result = {}
    for column in mapper.columns:
        key = column.key
        if include and key not in include:
            continue
        if exclude and key in exclude:
            continue
        value = getattr(model, key)
        if converters and key in converters:
            value = converters[key](value)
        elif hasattr(value, "isoformat"):
            value = value.isoformat()
        result[key] = value
    if extra:
        result.update(extra)
    return result


def model_to_schema(model: Any, schema_class: Type[S], extra: Optional[Dict] = None) -> S:
    """SQLAlchemy ORM 对象 → Pydantic Schema"""
    data = model_to_dict(model, extra=extra)
    return schema_class.model_validate(data)


def row_to_dict(
    row: Any,
    keys: Optional[List[str]] = None,
    converters: Optional[Dict[str, Callable]] = None,
) -> Dict[str, Any]:
    """原始 SQL 查询行结果 → 字典（非 ORM 对象）"""
    result = dict(row._mapping) if hasattr(row, "_mapping") else dict(row)
    if keys:
        result = {k: result[k] for k in keys if k in result}
    if converters:
        for k, fn in converters.items():
            if k in result:
                result[k] = fn(result[k])
    return result


def to_camel_case(snake_str: str) -> str:
    """snake_case → camelCase（用于前后端字段名转换）"""
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def to_camel_case_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """递归转换字典所有键为 camelCase"""
    result = {}
    for k, v in data.items():
        new_key = to_camel_case(k)
        result[new_key] = to_camel_case_dict(v) if isinstance(v, dict) else v
    return result
```

---

## time_util.py — 时间工具

**额外依赖**：无

适用场景：前端传 UTC ISO 格式时间，数据库存储北京时间（+08:00）。

```python
# {pkg}/complex/utils/time_util.py
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple

BEIJING_TZ = timezone(timedelta(hours=8))


def parse_time_range(
    start_time: Optional[str],
    end_time: Optional[str],
    days: int = 7,
) -> Tuple[datetime, datetime]:
    """
    解析 ISO 8601 格式时间范围，返回北京时间 datetime 对象。
    参数无效时默认返回最近 N 天。

    前端传入示例: "2024-01-01T00:00:00Z" 或 "2024-01-01T08:00:00+08:00"
    """
    now = datetime.now(BEIJING_TZ)

    def parse(s: str) -> Optional[datetime]:
        if not s:
            return None
        try:
            s = s.replace("Z", "+00:00")
            dt = datetime.fromisoformat(s)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=BEIJING_TZ)
            return dt.astimezone(BEIJING_TZ)
        except ValueError:
            return None

    end = parse(end_time) or now
    start = parse(start_time) or (end - timedelta(days=days))
    return start, end


def utc_to_beijing(dt: datetime) -> datetime:
    """UTC datetime → 北京时间"""
    return dt.replace(tzinfo=timezone.utc).astimezone(BEIJING_TZ)
```

---

## request_context_util.py — 请求上下文便捷方法

**额外依赖**：无（依赖 `RequestContext`）

```python
# {pkg}/complex/utils/request_context_util.py
from typing import Optional

from fastapi import HTTPException

from {pkg}.complex.config.request_context import RequestContext


def get_required_user_id() -> int:
    """获取当前用户 ID（必须已认证，否则抛 401）"""
    user_id = RequestContext.get_user_id()
    if user_id is None:
        raise HTTPException(status_code=401, detail="User authentication required")
    return user_id


def get_optional_user_id() -> Optional[int]:
    """获取当前用户 ID（未认证时返回 None）"""
    return RequestContext.get_user_id()
```

---

## crypto_util.py — AES 加密工具

**额外依赖**：`uv add cryptography`

> ⚠️ **注意**：此模式仅提供实现思路，不保证安全合规性。生产环境使用前请自行评估加密强度和密钥管理方案。

适用场景：在数据库中存储第三方 API Key 等需要可逆加密的敏感字段。

```python
# {pkg}/complex/utils/crypto_util.py
import base64
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# 从环境变量或配置读取，32 字节 (256 位)
_ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "").encode() or os.urandom(32)


def encrypt(plaintext: str) -> str:
    """加密字符串，返回 'ENC:{base64}' 格式"""
    aesgcm = AESGCM(_ENCRYPTION_KEY)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, plaintext.encode(), None)
    encoded = base64.b64encode(nonce + ct).decode()
    return f"ENC:{encoded}"


def decrypt(ciphertext: str) -> str:
    """解密 'ENC:{base64}' 格式字符串"""
    if not ciphertext.startswith("ENC:"):
        return ciphertext  # 未加密，直接返回
    encoded = ciphertext[4:]
    data = base64.b64decode(encoded)
    nonce, ct = data[:12], data[12:]
    aesgcm = AESGCM(_ENCRYPTION_KEY)
    return aesgcm.decrypt(nonce, ct, None).decode()


def is_encrypted(text: str) -> bool:
    return text.startswith("ENC:")
```
